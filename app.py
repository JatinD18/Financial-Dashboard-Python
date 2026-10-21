import os
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Dashboard", layout="wide")

# ---------- 1. Resolve files robustly (fixes Bug #1) ----------
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SEARCH_DIRS = [BASE_DIR, BASE_DIR / "data", Path.cwd(), Path.cwd() / "data"]

def find_file(name: str):
    for d in SEARCH_DIRS:                      # exact match
        if (d / name).exists():
            return d / name
    for d in SEARCH_DIRS:                      # case-insensitive fallback (Linux vs Windows)
        if d.exists():
            for f in d.iterdir():
                if f.name.lower() == name.lower():
                    return f
    return None

# ---------- 2. Auto-detect delimiter (fixes Bug #2) ----------
@st.cache_data(show_spinner=False)
def smart_read(name: str) -> pd.DataFrame:
    path = find_file(name)
    if path is None:
        raise FileNotFoundError(f"Could not find '{name}'. Searched: {[str(d) for d in SEARCH_DIRS]}")
    best = None
    for sep in [",", "\t", ";"]:
        try:
            t = pd.read_csv(path, sep=sep, encoding="utf-8-sig")
            t.columns = [str(c).strip() for c in t.columns]
            if best is None or t.shape[1] > best.shape[1]:   # keep the delimiter giving most columns
                best = t
        except Exception:
            continue
    if best is None:
        raise ValueError(f"Could not parse '{name}'.")
    return best

# ---------- 3. Column alias resolver (fixes Bug #3) ----------
ALIASES = {
    "Revenue": ["sales amount", "sales", "revenue", "extended amount"],
    "TotalCost": ["total product cost", "cost", "totalcost", "product standard cost"],
    "OrderDate": ["order date", "orderdate"],
    "ProductKey": ["product key", "productkey"],
    "SalesTerritoryKey": ["sales territory key", "salesterritorykey"],
    "ResellerKey": ["reseller key", "resellerkey"],
    "EmployeeKey": ["employee key", "employeekey"],
    "Country": ["country", "country region name", "sales territory country", "region"],
    "Category": ["category", "product category", "product line"],
    "FullName": ["full name", "fullname", "salesperson"],
    "ResellerName": ["reseller name", "resellername", "reseller"],
}

def resolve(df, key):
    lk = {str(c).strip().lower(): c for c in df.columns}
    for a in ALIASES.get(key, []):
        if a in lk:
            return lk[a]
    return None

def std(df, key):
    real = resolve(df, key)
    return df.rename(columns={real: key}) if (real is not None and real != key) else df

def safe_merge(left, right, key):
    if key in left.columns and key in right.columns:
        return left.merge(right, on=key, how="left")
    return left

# ---------- 4. Load + build dataset (with clean error messages) ----------
try:
    sales = smart_read("Sales.csv")
    for k in ["Revenue", "TotalCost", "OrderDate", "ProductKey", "SalesTerritoryKey", "ResellerKey", "EmployeeKey"]:
        sales = std(sales, k)
    sales["Revenue"] = pd.to_numeric(sales["Revenue"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce").fillna(0)
    sales["TotalCost"] = pd.to_numeric(sales["TotalCost"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce").fillna(0)

    df = sales
    for fname, keys in [("Product.csv", ["ProductKey"]), ("Region.csv", ["SalesTerritoryKey"]),
                        ("Reseller.csv", ["ResellerKey"]), ("Salesperson.csv", ["EmployeeKey"])]:
        try:
            aux = smart_read(fname)
            for k in keys + ["Country", "Category", "FullName", "ResellerName", "ProductKey"]:
                aux = std(aux, k)
            df = safe_merge(df, aux, keys[0])
        except FileNotFoundError:
            pass  # optional dimension file missing -> keep going

    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df["Year"] = df["OrderDate"].dt.year
    df["Profit"] = df["Revenue"] - df["TotalCost"]
except Exception as e:
    st.error(f"Data load failed: {type(e).__name__}: {e}")
    st.info("Make sure Sales.csv, Product.csv, Region.csv, Reseller.csv, Salesperson.csv are committed to the repo (correct casing).")
    st.stop()

st.title("Financial Performance Dashboard")

region_col = "Country" if "Country" in df.columns else ("Region" if "Region" in df.columns else None)
cat_col = "Category" if "Category" in df.columns else None
name_col = "FullName" if "FullName" in df.columns else ("ResellerName" if "ResellerName" in df.columns else None)

years = sorted(df["Year"].dropna().astype(int).unique().tolist())

# ---------- 5. Filters ----------
st.sidebar.header("Filters")
year_pick = st.sidebar.multiselect("Select Year", options=years, default=years[-2:] if len(years) > 1 else years)
region_pick = st.sidebar.multiselect("Select Region", options=(sorted(df[region_col].dropna().unique().tolist()) if region_col else []),
                                     default=(sorted(df[region_col].dropna().unique().tolist()) if region_col else []))

view = df[df["Year"].isin(year_pick)]
if region_col:
    view = view[view[region_col].isin(region_pick)]

# ---------- 6. KPIs (all from the SAME filtered view -> fixes Bug #4) ----------
rev = float(view["Revenue"].sum())
prof = float(view["Profit"].sum())
margin = (prof / rev * 100.0) if rev > 0 else 0.0

sel_years = sorted(view["Year"].dropna().astype(int).unique().tolist())
if len(sel_years) >= 2:
    cur = float(view[view["Year"] == sel_years[-1]]["Revenue"].sum())
    prev = float(view[view["Year"] == sel_years[-2]]["Revenue"].sum())
    yoy = ((cur - prev) / prev * 100.0) if prev > 0 else 0.0
else:
    yoy = 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${rev:,.0f}")
c2.metric("Total Profit", f"${prof:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("YoY Growth", f"{yoy:+.1f}%")

# ---------- 7. Charts ----------
st.header("Revenue vs Cost Over Time")
monthly = view.copy()
monthly["Month"] = monthly["OrderDate"].dt.to_period("M").astype(str)
monthly = monthly.groupby("Month")[["Revenue", "TotalCost"]].sum().reset_index()
fig1 = px.line(monthly, x="Month", y=["Revenue", "TotalCost"], title="Monthly Trend", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.header("Profit by Category")
if cat_col:                                   # fixes Bug #5: warn instead of silently charting IDs
    catg = view.groupby(cat_col)["Profit"].sum().reset_index()
    fig2 = px.bar(catg, x=cat_col, y="Profit", title="Profit by Category", color="Profit", color_continuous_scale="RdYlGn")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No 'Category' column found — add one to the Product table to enable this chart.")

st.header("Top 10 Performers")
if name_col:
    res = view.groupby(name_col)["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(10)
    st.dataframe(res, use_container_width=True)
else:
    st.warning("No performer-name column found.")
