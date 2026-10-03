import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Financial Performance Dashboard", layout="wide")

@st.cache_data
def load_data():
    sales = pd.read_csv('Sales.csv', sep='\t')
    product = pd.read_csv('Product.csv', sep='\t')
    region = pd.read_csv('Region.csv', sep='\t')
    reseller = pd.read_csv('Reseller.csv', sep='\t')
    salesperson = pd.read_csv('Salesperson.csv', sep='\t')
    targets = pd.read_csv('Targets.csv', sep='\t')
    
    sales = sales.rename(columns={'Sales': 'SalesAmount', 'Cost': 'TotalProductCost', 'Unit Price': 'UnitPrice'})
    reseller = reseller.rename(columns={'Reseller': 'ResellerName'})
    salesperson = salesperson.rename(columns={'Salesperson': 'FullName'})
    targets = targets.rename(columns={'Target': 'TargetAmount'})
    
    for col in ['SalesAmount', 'TotalProductCost', 'UnitPrice']:
        if col in sales.columns:
            sales[col] = sales[col].astype(str).str.replace(r'[$,]', '', regex=True)
            sales[col] = pd.to_numeric(sales[col], errors='coerce').fillna(0)
            
    if 'TargetAmount' in targets.columns:
        targets['TargetAmount'] = targets['TargetAmount'].astype(str).str.replace(r'[$,]', '', regex=True)
        targets['TargetAmount'] = pd.to_numeric(targets['TargetAmount'], errors='coerce').fillna(0)
    else:
        targets['TargetAmount'] = 0.0

    df = sales.merge(product, on='ProductKey', how='left')
    df = df.merge(region, on='SalesTerritoryKey', how='left')
    df = df.merge(reseller, on='ResellerKey', how='left')
    df = df.merge(salesperson, on='EmployeeKey', how='left')
    
    if 'EmployeeID' in df.columns and 'EmployeeID' in targets.columns:
        df = df.merge(targets[['EmployeeID', 'TargetAmount']], on='EmployeeID', how='left')
    else:
        df['TargetAmount'] = 0.0
        
    df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    df['SalesAmount'] = pd.to_numeric(df['SalesAmount'], errors='coerce').fillna(0)
    df['TotalProductCost'] = pd.to_numeric(df['TotalProductCost'], errors='coerce').fillna(0)
    df['TargetAmount'] = pd.to_numeric(df['TargetAmount'], errors='coerce').fillna(0)
    
    return df

df = load_data()

df['Profit'] = df['SalesAmount'] - df['TotalProductCost']
df['Year'] = df['OrderDate'].dt.year

total_revenue = df['SalesAmount'].sum()
total_profit = total_revenue - df['TotalProductCost'].sum()
profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
total_target = df['TargetAmount'].sum()

current_year = df['Year'].max()
current_year_revenue = df[df['Year'] == current_year]['SalesAmount'].sum()
last_year_revenue = df[df['Year'] == current_year - 1]['SalesAmount'].sum()
yoy_growth = ((current_year_revenue - last_year_revenue) / last_year_revenue) * 100 if last_year_revenue > 0 else 0

st.title("Financial Performance Dashboard")
st.markdown("### AdventureWorks 2022 | Python & Streamlit Implementation")

st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect("Select Year", options=sorted(df['Year'].dropna().unique()), default=sorted(df['Year'].dropna().unique())[-2:])
region_col = 'Country' if 'Country' in df.columns else 'Region'
selected_region = st.sidebar.multiselect("Select Region", options=sorted(df[region_col].dropna().unique()), default=sorted(df[region_col].dropna().unique()))

filtered_df = df[(df['Year'].isin(selected_year)) & (df[region_col].isin(selected_region))]

f_revenue = filtered_df['SalesAmount'].sum()
f_profit = filtered_df['Profit'].sum()
f_margin = (f_profit / f_revenue) * 100 if f_revenue > 0 else 0
f_target = filtered_df['TargetAmount'].sum()

tab1, tab2, tab3 = st.tabs(["Executive Summary", "Regional Performance", "Product & Targets"])
fast_config = {'displayModeBar': False, 'responsive': True}

with tab1:
    st.subheader("High-Level Financial Health")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${f_revenue:,.0f}")
    col2.metric("Total Profit", f"${f_profit:,.0f}")
    col3.metric("Profit Margin", f"{f_margin:.1f}%")
    col4.metric("YoY Growth", f"{yoy_growth:.1f}%")
    
    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Revenue vs Cost Over Time")
        monthly_trend = filtered_df.groupby(filtered_df['OrderDate'].dt.to_period('M')).agg({'SalesAmount': 'sum', 'TotalProductCost': 'sum'}).reset_index()
        monthly_trend['OrderDate'] = monthly_trend['OrderDate'].astype(str)
        fig_trend = px.line(monthly_trend, x='OrderDate', y=['SalesAmount', 'TotalProductCost'], title="Monthly Revenue vs Cost", markers=True)
        st.plotly_chart(fig_trend, width="stretch", config=fast_config)
        
    with col_chart2:
        st.subheader("Profit by Product Category")
        cat_col = 'Category' if 'Category' in filtered_df.columns else 'Subcategory'
        cat_profit = filtered_df.groupby(cat_col)['Profit'].sum().reset_index()
        fig_cat = px.bar(cat_profit, x=cat_col, y='Profit', title="Total Profit by Category", color='Profit', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_cat, width="stretch", config=fast_config)

with tab2:
    st.subheader("Geographic & Reseller Breakdown")
    col_map, col_table = st.columns(2)
    
    with col_map:
        st.subheader("Revenue by Country")
        region_rev = filtered_df.groupby(region_col)['SalesAmount'].sum().reset_index()
        fig_region = px.bar(region_rev, x='SalesAmount', y=region_col, orientation='h', title="Total Revenue by Country", color='SalesAmount', color_continuous_scale='Blues')
        fig_region.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_region, width="stretch", config=fast_config)
        
    with col_table:
        st.subheader("Top 10 Resellers by Revenue")
        reseller_col = 'ResellerName' if 'ResellerName' in filtered_df.columns else 'Reseller'
        reseller_rev = filtered_df.groupby(reseller_col)['SalesAmount'].sum().reset_index()
        reseller_rev = reseller_rev.sort_values('SalesAmount', ascending=False).head(10)
        st.dataframe(reseller_rev, width="stretch")

with tab3:
    st.subheader("Target Variance & Salesperson Performance")
    st.subheader("Overall Target Achievement")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta", value=f_revenue, domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Actual Revenue vs Target"}, delta={'reference': f_target},
        gauge={'axis': {'range': [None, f_target * 1.2]}, 'bar': {'color': "darkblue"},
               'steps': [{'range': [0, f_target * 0.8], 'color': "lightgray"}, {'range': [f_target * 0.8, f_target], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': f_target}}))
    st.plotly_chart(fig_gauge, width="stretch", config=fast_config)
    
    st.subheader("Salesperson Target Variance")
    name_col = 'FullName' if 'FullName' in filtered_df.columns else 'Salesperson'
    
    sp_perf = filtered_df.groupby(name_col).agg({'SalesAmount': 'sum', 'TargetAmount': 'sum'}).reset_index()
    sp_perf['Variance %'] = 0.0
    mask = sp_perf['TargetAmount'] > 0
    sp_perf.loc[mask, 'Variance %'] = ((sp_perf.loc[mask, 'SalesAmount'] - sp_perf.loc[mask, 'TargetAmount']) / sp_perf.loc[mask, 'TargetAmount']) * 100
    sp_perf = sp_perf.sort_values('SalesAmount', ascending=False)
    
    st.dataframe(
        sp_perf[[name_col, 'SalesAmount', 'TargetAmount', 'Variance %']].style.format({
            'SalesAmount': '${:,.0f}',
            'TargetAmount': '${:,.0f}',
            'Variance %': '{:.1f}%'
        }),
        width="stretch"
    )
