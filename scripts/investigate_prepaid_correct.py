"""Investigate the prepaid spike using ONLY 'Prepaid card' product (matches Raymond's calc)."""
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
PARQ = REPO / "prepared" / "complaints.parquet"

df = pd.read_parquet(PARQ)

prepaid = df[df["product"] == "Prepaid card"].copy()
prepaid["quarter"] = prepaid["date_received"].dt.to_period("Q")
prepaid["relief"] = prepaid["company_response"] == "Closed with monetary relief"

print(f"Total 'Prepaid card' complaints: {len(prepaid):,}")
print()

print("=== Prepaid quarterly (Prepaid card only) ===")
qtr = prepaid.groupby("quarter", observed=True).agg(
    n=("complaint_id", "count"),
    relief_n=("relief", "sum"),
)
qtr["relief_rate"] = (qtr["relief_n"] / qtr["n"] * 100).round(2)
print(qtr.to_string())
print()

# Zoom on spike window
print("=== Per-quarter top companies (spike window) ===")
for q in ["2023Q3", "2023Q4", "2024Q1", "2024Q2", "2024Q3"]:
    sub = prepaid[prepaid["quarter"] == q]
    if len(sub) == 0:
        continue
    print(f"\n--- {q} (n={len(sub):,}, relief_rate={sub['relief'].mean()*100:.2f}%) ---")
    top = sub.groupby("company", observed=True).agg(
        n=("complaint_id", "count"),
        relief_n=("relief", "sum"),
    )
    top["rate"] = (top["relief_n"] / top["n"] * 100).round(1)
    print(top.sort_values("n", ascending=False).head(10).to_string())

print("\n=== 2024 Q1 Prepaid card: response distribution ===")
q1 = prepaid[prepaid["quarter"] == "2024Q1"]
print((q1["company_response"].value_counts(normalize=True) * 100).round(1).to_string())

print("\n=== 2024 Q1 Prepaid card: top issues ===")
print(q1["issue"].value_counts(dropna=False).head(10).to_string())

print("\n=== 2024 Q1 Prepaid card: top sub-products ===")
print(q1["sub_product"].value_counts(dropna=False).head(10).to_string())
