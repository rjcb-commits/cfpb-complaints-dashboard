# CFPB Consumer Complaints Dashboard

A Tableau dashboard on five years of CFPB consumer complaint data. Surfaces a structural gap in monetary relief rates between P2P / money-transfer disputes and card disputes, and the company-level pattern that drives it.

**Live dashboard:** [public.tableau.com/app/profile/raymond.jack6785/viz/CFPBP2PResolutionGap](https://public.tableau.com/app/profile/raymond.jack6785/viz/CFPBP2PResolutionGap/CFPBP2PComplaints)

## The finding

P2P / money-transfer disputes close with monetary relief just 4.96% of the time. Credit card disputes resolve at 14.5%, debit at 18.0%, prepaid at 23.0%. The gap has held for the full five-year window and is dominated at the bottom by P2P-native platforms (Block / Cash App, Early Warning Services / Zelle, Robinhood) that resolve almost zero complaints with monetary relief.

The Q1 2025 spike in P2P volume (13x normal) followed CFPB's $175M enforcement against Block. Block closed 99% of those complaints with explanation only. Macro restitution and individual relief outcomes moved in opposite directions.

## What's in the dashboard

Single screen, four panels:

- Headline callout with the 4.96% number and a key-takeaway summary
- Monetary relief rate by product (horizontal bar, P2P highlighted in red)
- Monetary relief rate trend (quarterly line, five-year window, P2P highlighted in red, end-of-line labels)
- Top 10 P2P companies by complaint volume vs relief rate (scatter, dot size = volume, zero-relief outliers in red, inline annotation on Block)

## Why this dataset

I work consumer dispute analytics at a top-10 US bank. The bank-internal disputes I handle are the volume that *doesn't* escalate to the CFPB. This dashboard surfaces what does, focused on the payment-product categories my Reg-E modeling work actually touches. Building it on public data lets me show the analytical thinking I apply at work without exposing anything internal.

## Stack

- Python (pandas, pyarrow) for data prep
- Tableau Public for the dashboard
- Source data: [CFPB Consumer Complaint Database](https://www.consumerfinance.gov/data-research/consumer-complaints/)

## Local setup

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Get the data

The CFPB publishes the full dataset as a single CSV. Download once:

1. Go to https://www.consumerfinance.gov/data-research/consumer-complaints/
2. Click "Download" -> "All complaints in CSV" (or use the direct link below)
3. Direct: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
4. Unzip; place `complaints.csv` in `data/`

The raw file is ~3 GB uncompressed, ~5M rows. The prep script slims it down to the columns and time window the dashboard needs.

## Prep the data for Tableau

```bash
python scripts/prepare_data.py --years 5
```

Reads `data/complaints.csv`, filters to the last `--years` years (default 5), drops unused columns, fixes date types, and writes `prepared/complaints.parquet` (smaller and faster than CSV for Tableau).

## Build the dashboard

Open Tableau Public Desktop, connect to `prepared/complaints.parquet`, and build the dashboard. See `tableau/notes.md` for the panel structure and design notes.

When done, publish to Tableau Public and replace the "coming soon" link in this README with the public URL.

## Project layout

```
data/                   raw CSV (gitignored)
prepared/               aggregated/cleaned files for Tableau (gitignored)
scripts/
  prepare_data.py       slims raw CSV into Tableau-ready parquet
notebooks/
  01_explore.ipynb      EDA on the raw data
tableau/
  notes.md              dashboard panel design notes
  *.twbx                packaged workbook (committed once stable)
```

## License

All rights reserved.
