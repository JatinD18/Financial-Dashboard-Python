# 💰 Financial Performance Dashboard (Python + Streamlit)

An interactive executive P&L dashboard built on the **Adventure Works** sample dataset,
turning raw sales and cost tables into a filterable, decision-ready financial view.

🔗 **Live app:** [Financial Performance Dashboard](https://financial-dashboard-py-str.streamlit.app)

📦 **Code:** [Financial Performance Dashboard - GitHub Repository (app.py)](https://github.com/JatinD18/Financial-Dashboard-Python)

🗃️ **Dataset:** [Adventure Works (Excel tables) on Kaggle](https://www.kaggle.com/datasets/algorismus/adventure-works-in-excel-tables)

---

## Overview

The dashboard answers one question a CFO asks every month: *where is money being made,
and where is it leaking?* It exposes total revenue, profit, margin and year-over-year
growth, then lets a user slice the entire view by **Year (2017–2020)** and **Region**
(Australia, Canada, France, Germany, United Kingdom, United States — the six markets in
the Adventure Works geography dimension).

Unlike a static report, every filter recomputes the KPI cards and redraws the charts live.

### Headline KPIs (default view)

| KPI | Value |
|---|---:|
| Total Revenue | $77,548,570 |
| Total Profit | $999,495 |
| Profit Margin | 1.3% |
| YoY Growth | −61.1% |

*Reconciliation (pure arithmetic on the displayed figures):*
margin = 999,495 ÷ 77,548,570 ≈ **1.3%**, implying total cost ≈ **$76,549,075**
(77,548,570 − 999,495). The KPI row is internally consistent.

### Why these numbers are the point
A thin **1.3% margin** paired with a **−61.1% YoY** contraction is *not* a flattering
dashboard — and that is deliberate. The tool is built to surface a business under
pressure (barely breaking even, revenue falling year over year) so attention lands on the
regions and product categories driving the squeeze, rather than on a celebratory trend line.

---

## Views

- **Revenue vs Cost Over Time** — interactive line/area trend of top-line and expense across the filtered period (Plotly: hover, zoom, legend toggle).
- **Profit by Category** — where margin is created or eroded, broken down by Adventure Works product categories.
- **Top 10 Performers** — ranked contributors within the current filter.

All charts are rendered with **`plotly.express`**, so they are fully interactive in the
browser (hover tooltips, pan/zoom, click-to-toggle series) instead of flat images.

---

## Filters (sidebar)

| Filter | Options |
|---|---|
| Year | 2017, 2018, 2019, 2020 |
| Region | Australia, Canada, France, Germany, United Kingdom, United States |

Selecting a year/region re-runs the aggregation and updates every KPI card and chart.

---

## Tech stack

- **Python + Pandas** — data loading, joins across the star-schema tables, revenue/profit/margin/YoY aggregation
- **Plotly Express** — interactive charts
- **Streamlit** — sidebar slicers, `st.metric` KPI cards, multi-chart layout
- **Streamlit Cloud** — deployment
- **Adventure Works** — Microsoft's canonical sample warehouse (fact + dimension tables), used here as a realistic enterprise schema rather than a single flat CSV

---

## How to run locally

```bash
git clone https://github.com/JatinD18/Financial-Dashboard-Python.git
cd Financial-Dashboard-Python
pip install -r requirements.txt
streamlit run app.py
```

`requirements.txt` (typical):

```text
streamlit
pandas
plotly
```

> Adjust `app.py` / filenames to match the actual entry point in the repo.

---

## Repository structure

```text
Financial-Dashboard-Python/
│
├── app.py                  # Streamlit entry point
├── requirements.txt        # streamlit, pandas, plotly
└── README.md
```

> Align the file names above with what is actually committed.

---

## Author

**🤵🏼Jatin Naresh Dolas**
[LinkedIn](https://www.linkedin.com/in/jatin-dolas) | [GitHub](https://github.com/JatinD18)
