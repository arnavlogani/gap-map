"""Takes direct (PLACES) and indirect (6 ACS datasets) z-score measurements
of food insecurity for each Long Island Zip Code Tabulation area,
combines them into one table, cleans, and implements a weighted sum to determine
need layer food insecurity (via z-score)

Null rule (decided before computing, rule 7 in the 2026-11-09 journal entry):
- both sides present: need_score = W_DIRECT * z_direct + (1 - W_DIRECT) * z_indirect,
  re-standardized across those rows so it has mean 0 and std 1
- one side null: need_score = the other side alone, flagged low_confidence
- both sides null: need_score is null ("no data" on the map), flagged low_confidence
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]

DIRECT_FI = REPO_ROOT / "data" / "processed" / "need_direct.csv"
INDIRECT_FI = REPO_ROOT / "data" / "processed" / "need_indirect.csv"
OUTPUT = REPO_ROOT / "data" / "processed"

W_DIRECT = 0.6  # weight on z_direct; z_indirect gets 1 - W_DIRECT (rules 5-6)


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


def combine(df, w):
    """need_score for one weight w. Phase 4 calls this once per w in the grid."""
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


def main():

    # zcta5 read as text so it matches across files
    dfd = pd.read_csv(DIRECT_FI, dtype={"zcta5": str})  # dataframe direct
    dfi = pd.read_csv(INDIRECT_FI, dtype={"zcta5": str})  # dataframe indirect

    for d in (dfd, dfi):
        check_inputs(d)
        check_primary_key(d)

    dfd = dfd[["zcta5", "adults", "fi_rate", "low_confidence", "z_direct"]]
    dfi = dfi[["zcta5", "n_indicators", "z_indirect"]]

    df = pd.merge(dfd, dfi, on="zcta5", how="left")  # dataframe with the columns.

    # run health checks now.
    check_inputs(df)
    check_primary_key(df)
    check_null_count(df)

    df["need_score"], both = combine(df, W_DIRECT)
    df["low_confidence"] = df["low_confidence"] | ~both  # rule 7

    check_need_score(df)

    print(df["low_confidence"].sum(), "ZCTAs flagged low_confidence")
    print(
        f"need_score on combined rows: mean {df.loc[both, 'need_score'].mean():.2f}, "
        f"std {df.loc[both, 'need_score'].std():.2f}"
    )

    # step 20: ZCTAs furthest from the diagonal (z_direct = z_indirect)
    df["disagreement"] = df["z_direct"] - df["z_indirect"]
    furthest = df.loc[both].sort_values("disagreement", key=abs, ascending=False)
    print("\n10 ZCTAs where direct and indirect disagree most:")
    print(furthest[["zcta5", "adults", "z_direct", "z_indirect", "disagreement"]].head(10).to_string(index=False))

    df.to_csv(OUTPUT / "need_score.csv", index=False)


if __name__ == "__main__":
    main()
