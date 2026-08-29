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
└── data/
    └── Nassau_Candy_Distributor.csv    # Source dataset
```

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
