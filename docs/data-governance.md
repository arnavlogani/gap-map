# Data governance

## Never committed to this repository

- Anything from Echos (code, data, configuration, screenshots of internal systems).
- Island Harvest partner data, or any data received under an MOU or non-public agreement.
- Raw 211 call records. Only published aggregate counts are used.
- API keys, tokens, Foundry credentials, `.env` files.
- The datasets themselves, raw or processed. `data/sources.md` is the record; the files stay in Foundry and local storage.

`.gitignore` enforces the last two mechanically. The rest are enforced by reading this file before every commit.

## Public data only

Every input is a public dataset with a URL in `data/sources.md`. If a dataset can't be linked, it isn't used.

## Geography floor

No analysis below the smallest public geography for a given source (ZCTA, tract, or school district). No household-level inference.

## What is public here

- Code copied out of Foundry Code Repositories.
- Pipeline Builder graphs as screenshots and step descriptions.
- Methodology, decisions, and rejected alternatives.
- Map images.
