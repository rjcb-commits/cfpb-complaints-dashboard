# CFPB Consumer Complaints Dashboard

A Tableau dashboard built on the public CFPB Consumer Complaint Database. Surfaces the products, issues, and companies driving consumer financial complaints from 2012 to present.

**Live dashboard:** _coming soon (Tableau Public)_

## What it shows

Every consumer complaint filed against a US bank since 2012, sliced by:

- Trends over time, with drill-down by product (Credit card, Mortgage, EFT, etc.)
- Top complaint issues across the industry, filterable by company
- State-level complaint rates (per capita, not raw counts)
- Resolution outcomes — what fraction of complaints close with monetary relief vs explanation only
- Timely-response rates by company

## Why this dataset

I work consumer dispute analytics at a top-10 US bank. The bank-internal disputes I handle are the volume that *doesn't* escalate to the CFPB. This dashboard surfaces what does — the products and complaint types that drive regulatory escalation, and how outcomes vary by company. Electronic-fund-transfer complaints have grown sharply since 2018, which is the trend behind why Reg-E modeling work has gotten more attention industry-wide.

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
