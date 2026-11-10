"""Takes direct (PLACES) and indirect (6 ACS datasets) z-score measurements
of food insecurity for each Long Island Zip Code Tabulation area,
combines them into one table, cleans, and implements a weighted sum to determine
need layer food insecurity (via z-score). Then tests how sensitive the result
is to the weight, picks the weight, and writes the final need table.

Null rule (decided before computing, rule 7 in the 2026-11-09 journal entry):
- both sides present: need_score = w * z_direct + (1 - w) * z_indirect,
  re-standardized across those rows so it has mean 0 and std 1
- one side null: need_score = the other side alone, flagged low_confidence
- both sides null: need_score is null ("no data" on the map), flagged low_confidence

Weight rule: pick the w in the grid where need_score agrees equally with both
sources (rank correlation with z_direct closest to rank correlation with z_indirect).
That gives w = 0.6. Rule 6 fails (26.6% of ZCTAs change quintile across the grid),
but we keep w = 0.6: only one ZCTA moves more than one quintile.

Disagreement flag: ZCTAs where z_direct and z_indirect are 1.5 or more apart
are also flagged low_confidence (the 9 largest disagreements).
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]

DIRECT_FI = REPO_ROOT / "data" / "processed" / "need_direct.csv"
INDIRECT_FI = REPO_ROOT / "data" / "processed" / "need_indirect.csv"
OUTPUT = REPO_ROOT / "data" / "processed"

W_GRID = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8]  # rule 5: lean direct
STABILITY_LIMIT = 0.10  # rule 6: under 10% of ZCTAs may change quintile
DISAGREEMENT_LIMIT = 1.5  # |z_direct - z_indirect| at or above this is flagged

INDICATORS = [
    "z_snap_rate",
    "z_poverty_rate",
    "z_child_poverty_rate",
    "z_senior_poverty_rate",
    "z_median_income",
    "z_severe_burden_rate",
    "z_no_vehicle_rate",
]

FINAL_COLUMNS = [
    "zcta5",
    "fi_rate",
    "est_food_insecure_adults",
    "z_direct",
    "z_indirect",
    "need_score",
    "need_quintile",
    "n_indicators",
    "low_confidence",
]

# every null in the final table, with the reason (step 27)
EXPECTED_NULLS = {
    "fi_rate": (4, "no PLACES estimate: 11042, 11931, 11947, 11973"),
    "est_food_insecure_adults": (4, "same 4 as fi_rate"),
    "z_direct": (4, "same 4 as fi_rate"),
    "z_indirect": (6, "under 4 of 7 ACS indicators: 11042, 11549, 11717, 11794, 11798, 11973"),
    "need_score": (2, "both sides null: 11042, 11973"),
    "need_quintile": (2, "no need_score"),
}


# ---------- health checks ----------


def check_inputs(df):
    assert len(df) == 175, f"expected 175 rows, got {len(df)}"


def check_primary_key(df):
    assert df["zcta5"].is_unique, "duplicate zcta5 values"


def check_null_count(df):
    nulls = df["fi_rate"].isna().sum()
    assert nulls == 4, f"expected 4 null fi_rate values, got {nulls}"


def check_need_score(df):
    nulls = df["need_score"].isna().sum()
    assert nulls == 2, f"expected 2 null need_score values (11042, 11973), got {nulls}"


def check_final(df):
    check_inputs(df)
    check_primary_key(df)

    print("\nNulls per column:")
    for col in FINAL_COLUMNS:
        nulls = df[col].isna().sum()
        expected, reason = EXPECTED_NULLS.get(col, (0, ""))
        assert nulls == expected, f"{col}: expected {expected} nulls, got {nulls}"
        if nulls:
            print(f"  {col}: {nulls} ({reason})")

    mean = df["need_score"].mean()
    assert abs(mean) < 0.1, f"need_score mean {mean:.2f} is not near 0"
    print(f"need_score mean: {mean:.3f}")

    sizes = df["need_quintile"].value_counts().sort_index()
    assert sizes.between(34, 35).all(), f"uneven quintiles: {sizes.to_dict()}"
    print("Quintile sizes:", {int(k): int(v) for k, v in sizes.items()})

    flagged = df.loc[df["low_confidence"], "zcta5"].tolist()
    print(f"{len(flagged)} flagged low_confidence:", ", ".join(flagged))


# ---------- scoring ----------


def spearman(a, b):
    # same as Series.corr(method="spearman"), which needs scipy
    return a.rank().corr(b.rank())


def combine(df, w):
    """need_score for one weight w. Returns the score and the rows with both sides."""
    both = df["z_direct"].notna() & df["z_indirect"].notna()
    direct_only = df["z_direct"].notna() & df["z_indirect"].isna()
    indirect_only = df["z_direct"].isna() & df["z_indirect"].notna()

    score = pd.Series(float("nan"), index=df.index)

    # weighted sum, then re-standardize using only the rows that have both sides
    weighted = w * df.loc[both, "z_direct"] + (1 - w) * df.loc[both, "z_indirect"]
    score[both] = (weighted - weighted.mean()) / weighted.std()

    # one-sided rows filled in after, so they don't affect the mean and std above
    score[direct_only] = df.loc[direct_only, "z_direct"]
    score[indirect_only] = df.loc[indirect_only, "z_indirect"]

    return score, both


def quintiles(score):
    # rank first so ties split evenly; 1 = lowest need, 5 = highest
    return pd.qcut(score.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype("Int64")


def z_indirect_without(ind, drop):
    """Recompute z_indirect with one indicator left out (same rules as indirect_acs.py)."""
    cols = [c for c in INDICATORS if c != drop]
    z_mean = ind[cols].mean(axis=1)
    z_mean[ind[cols].notna().sum(axis=1) < 4] = None  # rule 3
    return (z_mean - z_mean.mean()) / z_mean.std()


# ---------- phase 4: sensitivity ----------


def sensitivity(df, ind):
    runs = {}
    print("\nWeight grid:")
    print("  w     rho vs direct  rho vs indirect")
    for w in W_GRID:
        score, both = combine(df, w)
        runs[f"w_{w:.2f}"] = quintiles(score)
        print(
            f"  {w:.2f}  {spearman(score[both], df.loc[both, 'z_direct']):.3f}"
            f"          {spearman(score[both], df.loc[both, 'z_indirect']):.3f}"
        )

    q = pd.DataFrame(runs)
    q.insert(0, "zcta5", df["zcta5"])
    q_runs = q.drop(columns="zcta5").dropna()

    changed = q_runs.nunique(axis=1) > 1
    pct = changed.mean()
    spread = (q_runs.max(axis=1) - q_runs.min(axis=1))
    print(f"\n{pct:.1%} of ZCTAs change quintile somewhere across the grid ({changed.sum()} of {len(q_runs)})")
    print(f"  moved 1 quintile: {(spread == 1).sum()}, moved 2+: {(spread >= 2).sum()}")
    print("  changed:", ", ".join(q.loc[changed[changed].index, "zcta5"]))

    print("\nSpearman between runs (quintiles):")
    print(q_runs.corr(method="spearman").round(3).to_string())

    # step 24: leave one indicator out, at the chosen weight
    print("\nLeave-one-out (w = 0.60), ZCTAs that change quintile vs all 7:")
    base = q["w_0.60"]
    for drop in INDICATORS:
        loo = df.copy()
        loo["z_indirect"] = z_indirect_without(ind, drop)
        score, _ = combine(loo, 0.6)
        moved = (quintiles(score) != base) & base.notna()
        print(f"  without {drop[2:]:<20} {moved.sum():>3}")

    return q, pct


def choose_weight(df):
    # rank correlation with each source; pick the w where they are closest
    gaps = {}
    for w in W_GRID:
        score, both = combine(df, w)
        gaps[w] = abs(
            spearman(score[both], df.loc[both, "z_direct"])
            - spearman(score[both], df.loc[both, "z_indirect"])
        )
    return min(gaps, key=gaps.get)


# ---------- main ----------


def main():

    # zcta5 read as text so it matches across files
    dfd = pd.read_csv(DIRECT_FI, dtype={"zcta5": str})  # dataframe direct
    dfi = pd.read_csv(INDIRECT_FI, dtype={"zcta5": str})  # dataframe indirect

    for d in (dfd, dfi):
        check_inputs(d)
        check_primary_key(d)

    dfd = dfd[["zcta5", "adults", "fi_rate", "low_confidence", "z_direct"]]
    ind = dfi[["zcta5"] + INDICATORS]  # kept for leave-one-out
    dfi = dfi[["zcta5", "n_indicators", "z_indirect"]]

    df = pd.merge(dfd, dfi, on="zcta5", how="left")  # dataframe with the columns.
    ind = df[["zcta5"]].merge(ind, on="zcta5", how="left")  # same row order as df

    # run health checks now.
    check_inputs(df)
    check_primary_key(df)
    check_null_count(df)

    # phase 3, step 20: ZCTAs furthest from the diagonal (z_direct = z_indirect)
    df["disagreement"] = df["z_direct"] - df["z_indirect"]
    furthest = df.dropna(subset=["disagreement"]).sort_values("disagreement", key=abs, ascending=False)
    print("10 ZCTAs where direct and indirect disagree most:")
    print(furthest[["zcta5", "adults", "z_direct", "z_indirect", "disagreement"]].head(10).to_string(index=False))

    # phase 4: sensitivity
    q, pct = sensitivity(df, ind)
    stable = pct < STABILITY_LIMIT
    print(f"\nRule 6 (under {STABILITY_LIMIT:.0%} change): {'PASS' if stable else 'FAIL'} at {pct:.1%}")
    q.to_csv(OUTPUT / "sensitivity.csv", index=False)

    w = choose_weight(df)
    print(f"Chosen weight: w = {w:.2f} (need_score agrees equally with both sources)")

    # phase 5: final table
    df["need_score"], both = combine(df, w)
    disagree = df["disagreement"].abs() >= DISAGREEMENT_LIMIT
    df["low_confidence"] = df["low_confidence"] | ~both | disagree  # rule 7 + disagreement
    print(f"\n{disagree.sum()} ZCTAs flagged for disagreement:", ", ".join(df.loc[disagree, "zcta5"]))
    check_need_score(df)

    df["need_quintile"] = quintiles(df["need_score"])
    df["est_food_insecure_adults"] = (df["fi_rate"] / 100 * df["adults"]).round()

    final = df[FINAL_COLUMNS]
    check_final(final)

    final.to_csv(OUTPUT / "need_final.csv", index=False)  # zcta5 written as text
    print(f"\nWrote {len(final)} rows to need_final.csv and sensitivity.csv")


if __name__ == "__main__":
    main()
