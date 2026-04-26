"""Slim the raw CFPB Consumer Complaint CSV into a Tableau-ready parquet.

Reads data/complaints.csv (which you download separately from
https://files.consumerfinance.gov/ccdb/complaints.csv.zip), filters to a
configurable date window, drops the columns the dashboard does not use,
fixes types, and writes prepared/complaints.parquet.

Usage:
    python scripts/prepare_data.py              # default last 5 years
    python scripts/prepare_data.py --years 10
    python scripts/prepare_data.py --since 2018-01-01
"""
from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "complaints.csv"
OUT = REPO / "prepared" / "complaints.parquet"

# Columns to keep — everything the dashboard actually needs
KEEP = [
    "Date received",
    "Product",
    "Sub-product",
    "Issue",
    "Sub-issue",
    "Company",
    "State",
    "ZIP code",
    "Submitted via",
    "Date sent to company",
    "Company response to consumer",
    "Timely response?",
    "Consumer disputed?",
    "Complaint ID",
]

# Renames for cleaner Tableau field names
RENAME = {
    "Date received": "date_received",
    "Product": "product",
    "Sub-product": "sub_product",
    "Issue": "issue",
    "Sub-issue": "sub_issue",
    "Company": "company",
    "State": "state",
    "ZIP code": "zip",
    "Submitted via": "submitted_via",
    "Date sent to company": "date_sent_to_company",
    "Company response to consumer": "company_response",
    "Timely response?": "timely_response",
    "Consumer disputed?": "consumer_disputed",
    "Complaint ID": "complaint_id",
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--years", type=int, default=5,
                   help="Keep only complaints received in the last N years")
    p.add_argument("--since", type=str, default=None,
                   help="Override --years with an explicit YYYY-MM-DD cutoff")
    p.add_argument("--include-credit-reporting", action="store_true",
                   help="Keep credit-reporting complaints (vs Equifax / Experian / "
                        "TransUnion). Default excludes them since they dominate the "
                        "dataset (~85%) and aren't banking complaints.")
    return p.parse_args()


CREDIT_REPORTING_PRODUCTS = {
    "Credit reporting or other personal consumer reports",
    "Credit reporting, credit repair services, or other personal consumer reports",
    "Credit reporting",
}


def main():
    args = parse_args()

    if not RAW.exists():
        raise FileNotFoundError(
            f"{RAW} not found. Download from "
            "https://files.consumerfinance.gov/ccdb/complaints.csv.zip "
            "and place complaints.csv in data/."
        )

    cutoff = (
        pd.to_datetime(args.since)
        if args.since
        else pd.to_datetime(date.today() - timedelta(days=365 * args.years))
    )
    print(f"Cutoff: {cutoff.date()}")

    print(f"Reading {RAW}...")
    df = pd.read_csv(RAW, usecols=KEEP, low_memory=False)
    print(f"  raw: {len(df):,} rows")

    df = df.rename(columns=RENAME)
    df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce")
    df["date_sent_to_company"] = pd.to_datetime(
        df["date_sent_to_company"], errors="coerce"
    )

    df = df[df["date_received"] >= cutoff].copy()
    print(f"  after date filter: {len(df):,} rows")

    if not args.include_credit_reporting:
        before = len(df)
        df = df[~df["product"].isin(CREDIT_REPORTING_PRODUCTS)].copy()
        print(f"  after dropping credit-reporting: {len(df):,} rows ({before - len(df):,} removed)")

    # Cast small categorical fields for parquet compactness
    for col in [
        "product", "sub_product", "issue", "sub_issue",
        "state", "submitted_via", "company_response",
        "timely_response", "consumer_disputed",
    ]:
        df[col] = df[col].astype("category")

    # Trim company names with extreme cardinality — keep top 100 by volume,
    # everything else becomes "Other (smaller companies)". Optional; comment
    # out if you want every company in the dashboard's filter dropdown.
    top_companies = df["company"].value_counts().head(100).index
    df["company"] = df["company"].where(
        df["company"].isin(top_companies), "Other (smaller companies)"
    ).astype("category")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT, index=False, compression="snappy")
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
    print()
    print("Top 10 products:")
    print(df["product"].value_counts().head(10).to_string())
    print()
    print(f"Date range: {df['date_received'].min().date()} -> {df['date_received'].max().date()}")


if __name__ == "__main__":
    main()
