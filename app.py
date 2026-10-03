import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("Financial Performance Dashboard")

sales = pd.read_csv("Sales.csv", sep="\t")
product = pd.read_csv("Product.csv", sep="\t")
region = pd.read_csv("Region.csv", sep="\t")
reseller = pd.read_csv("Reseller.csv", sep="\t")
salesperson = pd.read_csv("Salesperson.csv", sep="\t")

sales = sales.rename(columns={"Sales": "Revenue", "Cost": "TotalCost"})
reseller = reseller.rename(columns={"Reseller": "ResellerName"})
salesperson = salesperson.rename(columns={"Salesperson": "FullName"})

sales["Revenue"] = pd.to_numeric(sales["Revenue"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce").fillna(0)
sales["TotalCost"] = pd.to_numeric(sales["TotalCost"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce").fillna(0)

df = sales.merge(product, on="ProductKey", how="left")
df = df.merge(region, on="SalesTerritoryKey", how="left")
df = df.merge(reseller, on="ResellerKey", how="left")
df = df.merge(salesperson, on="EmployeeKey", how="left")

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["Year"] = df["OrderDate"].dt.year
df["Profit"] = df["Revenue"] - df["TotalCost"]

region_col = "Country" if "Country" in df.columns else "Region"
cat_col = "Category" if "Category" in df.columns else "ProductKey"
name_col = "FullName" if "FullName" in df.columns else "ResellerName"

years = sorted(df["Year"].dropna().unique().tolist())
regions = sorted(df[region_col].dropna().unique().tolist())

st.sidebar.header("Filters")
year_pick = st.sidebar.multiselect("Select Year", options=years, default=years[-2:] if len(years) > 1 else years)
region_pick = st.sidebar.multiselect("Select Region", options=regions, default=regions)

view = df[df["Year"].isin(year_pick)]
view = view[view[region_col].isin(region_pick)]

rev = float(view["Revenue"].sum())
prof = float(view["Profit"].sum())
margin = (prof / rev * 100.0) if rev > 0 else 0.0

last_y = max(years) if years else 2020
cur = float(df[df["Year"] == last_y]["Revenue"].sum())
prev = float(df[df["Year"] == last_y - 1]["Revenue"].sum())
yoy = ((cur - prev) / prev * 100.0) if prev > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${rev:,.0f}")
c2.metric("Total Profit", f"${prof:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("YoY Growth", f"{yoy:+.1f}%")

st.header("Revenue vs Cost Over Time")
monthly = view.copy()
monthly["Month"] = monthly["OrderDate"].dt.to_period("M").astype(str)
monthly = monthly.groupby("Month")[["Revenue", "TotalCost"]].sum().reset_index()
fig1 = px.line(monthly, x="Month", y=["Revenue", "TotalCost"], title="Monthly Trend", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.header("Profit by Category")
catg = view.groupby(cat_col)["Profit"].sum().reset_index()
fig2 = px.bar(catg, x=cat_col, y="Profit", title="Profit by Category", color="Profit", color_continuous_scale="RdYlGn")
st.plotly_chart(fig2, use_container_width=True)

st.header("Top 10 Performers")
res = view.groupby(name_col)["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(10)
st.dataframe(res, use_container_width=True)
