"""Investigate the P2P relief-rate drop to ~0% in 2025 Q1."""
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parent.parent
PARQ = REPO / "prepared" / "complaints.parquet"

df = pd.read_parquet(PARQ)

# Identify the P2P product. CFPB labels it "Money transfer, virtual currency,
# or money service" with sub-product variations. Try the common patterns.
print("=== Products in data ===")
print(df["product"].value_counts().to_string())
print()

# Filter to payment products (the four in the dashboard).
# P2P generally lives in "Money transfer, virtual currency, or money service".
P2P_PRODUCTS = [
    p for p in df["product"].cat.categories
    if "money transfer" in p.lower() or "virtual currency" in p.lower()
]
print(f"P2P product matches: {P2P_PRODUCTS}")
print()

p2p = df[df["product"].isin(P2P_PRODUCTS)].copy()
p2p["quarter"] = p2p["date_received"].dt.to_period("Q")

# Define monetary relief
relief_values = ["Closed with monetary relief"]
p2p["relief"] = p2p["company_response"].isin(relief_values)

print("=== P2P quarterly: count, relief count, relief rate ===")
qtr = p2p.groupby("quarter", observed=True).agg(
    n=("complaint_id", "count"),
    relief_n=("relief", "sum"),
)
qtr["relief_rate"] = qtr["relief_n"] / qtr["n"]
print(qtr.to_string())
print()

# Zoom into 2025 Q1
print("=== 2025 Q1 P2P breakdown ===")
q1_2025 = p2p[p2p["quarter"] == "2025Q1"].copy()
print(f"Total P2P complaints in 2025 Q1: {len(q1_2025):,}")
print()
print("Company response distribution:")
print(q1_2025["company_response"].value_counts(dropna=False).to_string())
print()
print("Top companies in 2025 Q1 P2P:")
print(q1_2025["company"].value_counts().head(15).to_string())
print()
print("Sub-products in 2025 Q1 P2P:")
print(q1_2025["sub_product"].value_counts(dropna=False).head(15).to_string())
print()
print("Top issues in 2025 Q1 P2P:")
print(q1_2025["issue"].value_counts(dropna=False).head(15).to_string())
print()

# Compare to 2024 Q4 and 2025 Q2 for context
print("=== Comparison: surrounding quarters' company-response mix ===")
for q in ["2024Q3", "2024Q4", "2025Q1", "2025Q2", "2025Q3"]:
    sub = p2p[p2p["quarter"] == q]
    if len(sub) == 0:
        print(f"{q}: 0 complaints")
        continue
    print(f"\n{q} (n={len(sub):,})")
    print((sub["company_response"].value_counts(normalize=True) * 100).round(1).head(6).to_string())

# Is the dataset truncated?
print("\n=== Date range overall ===")
print(f"Min date: {df['date_received'].min()}")
print(f"Max date: {df['date_received'].max()}")
print(f"P2P max date: {p2p['date_received'].max()}")
