# CFPB Consumer Complaints Dashboard

A Tableau dashboard comparing recorded monetary-relief outcomes across selected payment-product categories in the CFPB Consumer Complaint Database, covering April 2021 through December 2025.

**Live dashboard:** [public.tableau.com/app/profile/raymond.jack6785/viz/CFPBP2PResolutionGap](https://public.tableau.com/app/profile/raymond.jack6785/viz/CFPBP2PResolutionGap/CFPBP2PComplaints)

## The finding

In the analyzed records, P2P / money-transfer complaints closed with monetary relief at a rate of 4.96%, compared with 14.52% for the credit-card group, 18.01% for the debit-labelled group, and 22.95% for prepaid.

Q1 2025 accounted for 42.8% of the P2P / money-transfer complaint total. Excluding that quarter, the group's monetary-relief rate was 8.07%. Complaint volume rose from 4,597 in Q4 2024 to 58,903 in Q1 2025, while recorded monetary-relief outcomes rose from 386 to 488.

These are outcomes recorded in CFPB complaints, not a measure of all consumer reimbursement or proof of a regulatory or operational cause. Category definitions and reporting coverage differ: the debit-labelled group includes a checking-account charge-issue category, historical combined credit-card/prepaid records are assigned to credit, and standalone prepaid coverage begins in Q3 2023.

## What's in the dashboard

Single screen, four panels:

- Headline callout with the 4.96% number and a key-takeaway summary
- Monetary relief rate by product (horizontal bar, P2P highlighted in red)
- Monetary relief rate trend (quarterly line, five-year window, P2P highlighted in red, end-of-line labels)
- Top 10 P2P companies by complaint volume vs relief rate (scatter, dot size = volume, companies with near-zero recorded monetary-relief rates in red, inline annotation on Block)

## Why this dataset

I work in consumer dispute analytics. This project uses public CFPB data to explore complaint outcomes across payment-product categories without using employer data or materials.

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

The published source grows over time; the current uncompressed size and row count depend on when you download it. The prep script slims the raw file to the columns and time window the dashboard needs.

## Prep the data for Tableau

```bash
python scripts/prepare_data.py --years 5
python scripts/prepare_data.py --since 2021-04-01  # or an explicit cutoff
```

Reads `data/complaints.csv`, filters by either a rolling window (`--years`, default 5) or an explicit cutoff (`--since YYYY-MM-DD`), drops unused columns, fixes date types, and writes `prepared/complaints.parquet`. Credit-reporting complaints are excluded by default; add `--include-credit-reporting` to keep them.

## Build the dashboard

Open Tableau Public Desktop, connect to `prepared/complaints.parquet`, and build. The published version is linked at the top of this README.

## Reproducing the published analysis

The published dashboard was built on a snapshot covering **April 2021 through December 2025**, with credit-reporting complaints excluded. Product mappings and the outcome definition used in the published workbook:

- **P2P / money transfer** = CFPB product `Money transfer, virtual currency, or money service`
- **Credit card** = `Credit card` combined with the historical `Credit card or prepaid card` dual-label category
- **Debit card / unauthorized** = subset of `Checking or savings account` filtered to debit/ATM issue codes
- **Prepaid card** = CFPB product `Prepaid card`
- **Monetary relief** = `company_response == "Closed with monetary relief"`

To recreate the published analysis period from a newer raw file, run `python scripts/prepare_data.py --since 2021-04-01` and then filter to `date_received <= 2025-12-31` inside Tableau. A rolling `--years 5` at a later date will not reproduce the same window. The exact snapshot used to publish the dashboard is not committed here.

## Project layout

```
data/                   raw CSV (gitignored)
prepared/               aggregated/cleaned files for Tableau (gitignored)
scripts/
  prepare_data.py       slims raw CSV into Tableau-ready parquet
```

## License

All rights reserved.
