import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("Financial Performance Dashboard")

@st.cache_data
def load_data():
    sales = pd.read_csv('Sales.csv', sep='\t')
    sales = sales.rename(columns={'Sales': 'SalesAmount', 'Cost': 'TotalProductCost'})
    for col in ['SalesAmount', 'TotalProductCost']:
        sales[col] = sales[col].astype(str).str.replace(r'[$,]', '', regex=True)
        sales[col] = pd.to_numeric(sales[col], errors='coerce').fillna(0)
    sales['Profit'] = sales['SalesAmount'] - sales['TotalProductCost']
    return sales

df = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['SalesAmount'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
margin = (df['Profit'].sum() / df['SalesAmount'].sum() * 100) if df['SalesAmount'].sum() > 0 else 0
col3.metric("Profit Margin", f"{margin:.1f}%")

chart_data = df.groupby('ProductKey')['SalesAmount'].sum().reset_index()
fig = px.bar(chart_data, x='ProductKey', y='SalesAmount', title="Sales by Product Key")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data Preview")
st.dataframe(df.head())