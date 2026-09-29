<<<<<<< HEAD
# 🍬 Nassau Candy Distributor — Shipping Route Efficiency Dashboard

An interactive **Streamlit** analytics dashboard that turns raw order and shipment data into route-level operational intelligence for Nassau Candy Distributor — a national candy distributor shipping from five factories to customers across the US and Canada.

Built as part of the **Unified Mentor** internship program (Data Analytics track).

---

## 📌 Problem Statement

Nassau Candy Distributor ships products from multiple factories to customers nationwide but lacks visibility into:

- Which factory-to-customer routes are consistently efficient
- Which routes experience frequent delays
- How shipping performance varies by region, state, and ship mode
- Where operational bottlenecks exist geographically

This project transforms raw order/shipment data into actionable, route-level logistics intelligence — enabling data-driven rather than reactive optimization decisions.

---

## ✨ Features

| Module | Description |
|---|---|
| **Route Efficiency Overview** | Leaderboard of Factory → State/Region routes ranked by a normalized Efficiency Score, with Top 10 / Bottom 10 tables |
| **Geographic Shipping Map** | US choropleth colorable by avg lead time, delay frequency, or shipment volume, with factory locations overlaid and an auto-flagged bottleneck table |
| **Ship Mode Comparison** | Lead-time distribution (box plots), delay frequency by mode, and a descriptive cost-vs-time tradeoff scatter |
| **Route Drill-Down** | Order-level view for any Factory → State pair: KPIs, shipment timeline, ship-mode split, and product mix |

**Interactive filters:** order date range, country/region, region, state/province, ship mode, factory, and an adjustable delay-threshold slider that drives the "delayed shipment" flag across every module.

---

## 🗂️ Repository Structure

```
nassau-shipping-dashboard/
├── app.py                              # Main Streamlit application
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
=======
# Nassau Candy Distributor — Shipping Route Efficiency Dashboard

Streamlit dashboard for the Factory-to-Customer Shipping Route Efficiency Analysis project.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Folder structure

```
nassau_app/
├── app.py                              # Main Streamlit application
├── requirements.txt
├── README.md
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
└── data/
    └── Nassau_Candy_Distributor.csv    # Source dataset
```

<<<<<<< HEAD
---

## 🧮 Methodology

1. **Data Cleaning & Validation** — date parsing, removal of invalid/negative lead times, whitespace/casing standardization on geographic fields.
2. **Feature Engineering** — Shipping Lead Time (Ship Date − Order Date), Factory → Region and Factory → State route keys (derived from the product-to-factory correlation table), US state abbreviation mapping for geospatial rendering.
3. **Route Aggregation** — total shipments, average lead time, lead-time variability, and delay frequency computed per route.
4. **Efficiency Benchmarking** — routes ranked via a normalized 0–100 Efficiency Score (lower average lead time → higher score); compared across ship modes.
5. **Geographic Bottleneck Analysis** — states flagged when both shipment volume and average lead time exceed the median, surfacing congestion-prone regions.
6. **Ship Mode Performance Analysis** — Standard vs. Expedited-class comparison, with a descriptive cost-time tradeoff view.

### Data Quality Note

The source file's `Order Date` values fall in 2024–2025 while `Ship Date` values fall in 2026–2030, so raw lead-time figures (~900–1,640 days) do not represent realistic shipping durations. All KPIs are computed consistently from the data as provided, so **relative comparisons** (route vs. route, mode vs. mode) remain valid — absolute day counts should simply not be read as real-world shipping times. This is also surfaced as an in-app notice.

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — web application framework
- **[Pandas](https://pandas.pydata.org/)** — data cleaning and aggregation
- **[Plotly](https://plotly.com/python/)** — interactive charts and US choropleth mapping

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>/nassau-shipping-dashboard

# (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

> **Note:** `app.py` expects the dataset at `data/Nassau_Candy_Distributor.csv`, relative to the directory you run `streamlit run` from. Keep the folder structure intact.

---

## 📊 Dataset

| Field | Description |
|---|---|
| Row ID / Order ID | Unique row / order identifiers |
| Order Date / Ship Date | Dates driving the Shipping Lead Time calculation |
| Ship Mode | Shipping method (Standard/First/Second Class, Same Day) |
| Customer ID, Country/Region, City, State/Province, Postal Code | Customer geography |
| Division, Product ID, Product Name | Product classification |
| Region | Customer region (Pacific, Atlantic, Interior, Gulf) |
| Sales, Units, Gross Profit, Cost | Financial metrics |

Factory locations and the product-to-factory correlation table used for route derivation are embedded directly in `app.py`.

---

## 📦 Deliverables

- ✅ Interactive Streamlit dashboard (this repository)
- 📄 Research paper — EDA, insights, and recommendations
- 📋 Executive summary for stakeholders

---

## 📄 License

This project was developed for educational purposes as part of the Unified Mentor internship program.

---

## 🙋 Author

**Suryansh**
Pursuing Senior Manager, Technology Strategy & Transformation
=======
## What's inside

- **Route Efficiency Overview** — leaderboard of routes (Factory → State/Region) ranked
  by a normalized Efficiency Score, with Top 10 / Bottom 10 tables and a lead-time bar chart.
- **Geographic Shipping Map** — US state choropleth colorable by avg lead time, delay
  frequency, or shipment volume, with factory locations overlaid and a bottleneck table
  (states above median volume AND above median lead time).
- **Ship Mode Comparison** — lead-time distribution (box plot), delay frequency, and a
  descriptive cost-vs-time scatter across Standard/First/Second Class and Same Day.
- **Route Drill-Down** — pick a factory + customer state to see order-level KPIs, a
  shipment timeline scatter against the delay threshold, ship-mode split, and product mix.

## Filters (sidebar)

Order date range, Country/Region, Region, State/Province, Ship Mode, Factory, and an
adjustable delay-threshold slider that drives the "Delayed" flag used across all tabs.

## Data quality note

Order Dates in the source file fall in 2024–2025 while Ship Dates fall in 2026–2030, so
raw lead-time values (~900–1,640 days) are not realistic shipping durations. All KPIs are
computed consistently from the data as provided — relative comparisons (route vs. route,
mode vs. mode) remain valid, but absolute day counts should not be read as real-world
shipping times. This is called out in an in-app expander as well.
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
