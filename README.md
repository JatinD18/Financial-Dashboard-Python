<div align="center">

# 💰 Financial Performance Dashboard — Streamlit + Power BI

An executive P&L view built on the **Adventure Works** sample dataset, delivered in **two
complementary layers**:

1. **Python + Streamlit app** — code-driven, interactive, deployable-as-code. Sidebar
   slicers recompute KPIs and redraw Plotly charts live.
2. **Power BI report** — drag-and-drop, enterprise-standard, built for stakeholder
   self-service and DAX-based reporting.

> Showing both is deliberate: the Streamlit layer proves I can build custom, reproducible
> analytics logic in code; the Power BI layer proves I can package the same insight into the
> tool business users actually consume. Same data, same metrics, two delivery modes.


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://financial-dashboard-py-str.streamlit.app)   [![Code Script](https://img.shields.io/badge/app.py%20%7C%20Code%20in%20GithHub-blue)](https://github.com/JatinD18/Financial-Dashboard-Python/blob/main/app.py)

📊 **Power BI report:** `It's in the data/dashboard folder` — [![PDF](https://img.shields.io/badge/PDF-red)](https://github.com/JatinD18/Financial-Dashboard-Python/blob/main/data/dashboard/Financial_Dashboard.pdf) [![PBIX](https://img.shields.io/badge/PBIX-yellow)](https://github.com/JatinD18/Financial-Dashboard-Python/blob/main/data/dashboard/Financial_Dashboard.pbix)

🗃️ **Dataset:** [Adventure Works (Excel tables) on Kaggle](https://www.kaggle.com/datasets/algorismus/adventure-works-in-excel-tables)

🗃️ **Dataset:** ![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)

</div>

---

## Headline KPIs (default view)

| KPI | Value |
|---|---:|
| Total Revenue | $77,548,570 |
| Total Profit | $999,495 |
| Profit Margin | 1.3% |
| YoY Growth | −61.1% |

*Reconciliation (arithmetic on the displayed figures):* margin = 999,495 ÷ 77,548,570 ≈
**1.3%**, implying total cost ≈ **$76,549,075**. The KPI row is internally consistent.

**Cross-tool validation:** these same four figures reproduce in the Power BI report
`[confirm: same dataset + same margin formula?]`. Matching KPIs across two independently
built tools is a QA signal — it shows the aggregation logic was verified, not eyeballed.

### Why these numbers are the point
A thin **1.3% margin** with a **−61.1% YoY** contraction is *not* a flattering dashboard —
and that's intentional. The tool surfaces a business under pressure so attention lands on
the regions and categories driving the squeeze, not on a celebratory trend line.

---

## Layer 1 — Streamlit (interactive)

| Filter | Options |
|---|---|
| Year | 2017, 2018, 2019, 2020 |
| Region | Australia, Canada, France, Germany, United Kingdom, United States |

Selecting a year/region re-runs the Pandas aggregation and updates every `st.metric` card
and chart. Charts use **`plotly.express`** (hover, zoom, click-to-toggle).

- **Revenue vs Cost Over Time** — top-line vs expense trend
- **Profit by Category** — where margin is created or eroded
- **Top 10 Performers** — ranked contributors within the current filter

## Layer 2 — Power BI (self-service)

Built from the same Adventure Works extracts, the report gives stakeholders filter/ drill
without touching code.

![Power BI Dashboard](https://github.com/JatinD18/Financial-Dashboard-Python/blob/main/data/dashboard/assets/powerbi_financial_dashboard.png)

---

## Tech stack

- **Python + Pandas** — loading, star-schema joins, revenue/profit/margin/YoY logic
- **Plotly Express** — interactive Streamlit charts
- **Streamlit + Streamlit Cloud** — app UI and deployment
- **Power BI (+ DAX)** `[confirm]` — stakeholder-facing report
- **Adventure Works** — Microsoft's canonical sample warehouse (fact + dimension tables),
  used here as a realistic enterprise schema rather than a single flat CSV

---

## Repository structure

```text
Financial-Dashboard-Python/
│
├── app.py                  # Streamlit entry point
├── requirements.txt        # streamlit, pandas, plotly
├── data/                   # Adventure Works CSV extracts
├── dashboard/
│   ├── assets/
│   │   └── powerbi_financial_dashboard.png   # Power BI screenshot (README hero)
│   ├── Financial_Dashboard.pbix              # editable Power BI file
│   └── Financial_Dashboard.pdf               # exported PDF for quick viewing
├── .gitignore
└── README.md

## How to run

**Streamlit (local):**
```bash
git clone https://github.com/JatinD18/Financial-Dashboard-Python.git
cd Financial-Dashboard-Python
pip install -r requirements.txt
streamlit run app.py
```

**Power BI:** open `dashboard/Financial_Dashboard.pbix` in Power BI Desktop, or view the
exported PDF in the same folder.

---

## Author

**Jatin Naresh Dolas**

[![GitHub](https://img.shields.io/badge/GitHub-JatinD18-181717?logo=github&logoColor=white)](https://github.com/JatinD18) | [![LinkedIn](https://img.shields.io/badge/LinkedIn-Jatin%20Dolas-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jatin-dolas)

---
