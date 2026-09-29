"""
Nassau Candy Distributor — Factory-to-Customer Shipping Route Efficiency Dashboard
Streamlit application.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --------------------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Nassau Candy | Shipping Route Efficiency",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------------------
<<<<<<< HEAD
# Custom CSS — enlarge layout to fill a 1920x1080 display
# --------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
        /* Widen the main content area and use more of the screen */
        .block-container {
            max-width: 1850px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Slightly larger base font across the app */
        html, body, [class*="css"]  {
            font-size: 17px;
        }

        /* Bigger headings */
        h1 { font-size: 2.4rem !important; }
        h2, h3 { font-size: 1.6rem !important; }

        /* Bigger KPI metric cards */
        div[data-testid="stMetric"] {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem 1rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 1rem !important;
        }

        /* Wider sidebar */
        section[data-testid="stSidebar"] {
            width: 380px !important;
        }

        /* Make dataframes/tables a bit taller by default */
        div[data-testid="stDataFrame"] {
            font-size: 0.95rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------------------
=======
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
# Static reference data (from project technical documentation)
# --------------------------------------------------------------------------------------
FACTORY_COORDS = {
    "Lot's O' Nuts": (32.881893, -111.768036),
    "Wicked Choccy's": (32.076176, -81.088371),
    "Sugar Shack": (48.11914, -96.18115),
    "Secret Factory": (41.446333, -90.565487),
    "The Other Factory": (35.1175, -89.971107),
}

PRODUCT_FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

US_STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
    "Wyoming": "WY", "District of Columbia": "DC",
}

DATA_PATH = "data/Nassau_Candy_Distributor.csv"


# --------------------------------------------------------------------------------------
# Data loading & feature engineering
# --------------------------------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # --- Data cleaning & validation ---
    df.columns = [c.strip() for c in df.columns]
    for col in ["Country/Region", "City", "State/Province", "Division", "Region",
                "Product Name", "Ship Mode"]:
        df[col] = df[col].astype(str).str.strip()

    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["Order Date", "Ship Date"])

    # --- Feature engineering ---
    df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df[df["Lead Time"] >= 0].copy()  # remove invalid/negative lead times

    df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY_MAP)
    df = df.dropna(subset=["Factory"])

    df["Route (Region)"] = df["Factory"] + " → " + df["Region"]
    df["Route (State)"] = df["Factory"] + " → " + df["State/Province"]

    df["Factory Lat"] = df["Factory"].map(lambda f: FACTORY_COORDS[f][0])
    df["Factory Lon"] = df["Factory"].map(lambda f: FACTORY_COORDS[f][1])

    df["State Abbr"] = df["State/Province"].map(US_STATE_ABBR)

    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Order Year"] = df["Order Date"].dt.year

    return df


df_raw = load_data(DATA_PATH)

# --------------------------------------------------------------------------------------
# Sidebar — global filters
# --------------------------------------------------------------------------------------
st.sidebar.title("🍬 Nassau Candy")
st.sidebar.caption("Shipping Route Efficiency Analysis")
st.sidebar.divider()

st.sidebar.subheader("Filters")

min_date, max_date = df_raw["Order Date"].min().date(), df_raw["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

country_options = sorted(df_raw["Country/Region"].unique())
selected_countries = st.sidebar.multiselect("Country/Region", country_options, default=country_options)

region_options = sorted(df_raw["Region"].unique())
selected_regions = st.sidebar.multiselect("Region", region_options, default=region_options)

state_options = sorted(df_raw[df_raw["Region"].isin(selected_regions)]["State/Province"].unique())
selected_states = st.sidebar.multiselect("State/Province", state_options, default=state_options)

ship_mode_options = sorted(df_raw["Ship Mode"].unique())
selected_ship_modes = st.sidebar.multiselect("Ship Mode", ship_mode_options, default=ship_mode_options)

factory_options = sorted(df_raw["Factory"].unique())
selected_factories = st.sidebar.multiselect("Factory", factory_options, default=factory_options)

st.sidebar.divider()
lead_time_threshold = st.sidebar.slider(
    "Delay threshold (days)",
    min_value=int(df_raw["Lead Time"].min()),
    max_value=int(df_raw["Lead Time"].quantile(0.95)),
    value=int(df_raw["Lead Time"].median()),
    help="Shipments with lead time above this are counted as 'delayed' for the Delay Frequency KPI.",
)

st.sidebar.divider()
with st.sidebar.expander("⚠️ Data quality note"):
    st.caption(
        "Order Dates fall in 2024–2025 while Ship Dates fall in 2026–2030 in the source "
        "file, so raw lead-time values (~900–1,640 days) are not realistic shipping "
        "durations. All KPIs here are computed consistently from the data as provided, "
        "so relative comparisons (fastest vs. slowest routes, mode vs. mode) remain valid "
        "even though absolute day counts should not be read as real-world shipping times."
    )

# --------------------------------------------------------------------------------------
# Apply filters
# --------------------------------------------------------------------------------------
mask = (
    (df_raw["Order Date"].dt.date >= start_date)
    & (df_raw["Order Date"].dt.date <= end_date)
    & (df_raw["Country/Region"].isin(selected_countries))
    & (df_raw["Region"].isin(selected_regions))
    & (df_raw["State/Province"].isin(selected_states))
    & (df_raw["Ship Mode"].isin(selected_ship_modes))
    & (df_raw["Factory"].isin(selected_factories))
)
df = df_raw[mask].copy()

if df.empty:
    st.warning("No shipments match the current filters. Adjust filters in the sidebar.")
    st.stop()

df["Delayed"] = df["Lead Time"] > lead_time_threshold

# --------------------------------------------------------------------------------------
# Header + top-line KPIs
# --------------------------------------------------------------------------------------
st.title("Factory-to-Customer Shipping Route Efficiency")
st.caption("Nassau Candy Distributor — route-level operational intelligence")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Shipments", f"{len(df):,}")
k2.metric("Avg Lead Time", f"{df['Lead Time'].mean():.1f} days")
k3.metric("Delay Frequency", f"{df['Delayed'].mean()*100:.1f}%")
k4.metric("Active Routes (State)", f"{df['Route (State)'].nunique():,}")
k5.metric("Total Sales", f"${df['Sales'].sum():,.0f}")

st.divider()

# --------------------------------------------------------------------------------------
# Tabs
# --------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Route Efficiency Overview", "🗺️ Geographic Shipping Map",
     "🚚 Ship Mode Comparison", "🔍 Route Drill-Down"]
)

# ---------------------------------------------------------------------
# TAB 1: Route Efficiency Overview
# ---------------------------------------------------------------------
with tab1:
    st.subheader("Route Performance Leaderboard")

    granularity = st.radio(
        "Route granularity", ["State", "Region"], horizontal=True, key="gran1"
    )
    route_col = "Route (State)" if granularity == "State" else "Route (Region)"

    route_agg = (
        df.groupby(route_col)
        .agg(
            Total_Shipments=("Row ID", "count"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Lead_Time_StdDev=("Lead Time", "std"),
            Delay_Frequency=("Delayed", "mean"),
            Total_Sales=("Sales", "sum"),
        )
        .reset_index()
    )
    route_agg["Lead_Time_StdDev"] = route_agg["Lead_Time_StdDev"].fillna(0)
    route_agg["Delay_Frequency"] = (route_agg["Delay_Frequency"] * 100).round(1)

    min_lt, max_lt = route_agg["Avg_Lead_Time"].min(), route_agg["Avg_Lead_Time"].max()
    if max_lt > min_lt:
        route_agg["Efficiency Score"] = (
            100 * (1 - (route_agg["Avg_Lead_Time"] - min_lt) / (max_lt - min_lt))
        ).round(1)
    else:
        route_agg["Efficiency Score"] = 100.0

    route_agg = route_agg.sort_values("Efficiency Score", ascending=False)
    route_agg_display = route_agg.rename(columns={
        route_col: "Route", "Total_Shipments": "Shipments",
        "Avg_Lead_Time": "Avg Lead Time (days)", "Lead_Time_StdDev": "Lead Time Std Dev",
        "Delay_Frequency": "Delay Frequency (%)", "Total_Sales": "Total Sales ($)",
    })

    min_shipments = st.slider(
        "Minimum shipments per route (for leaderboard significance)",
        1, int(route_agg["Total_Shipments"].max()), 5, key="minship1"
    )
    sig_routes = route_agg_display[route_agg_display["Shipments"] >= min_shipments]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🏆 Top 10 Most Efficient Routes**")
        top10 = sig_routes.nlargest(10, "Efficiency Score")
        st.dataframe(
            top10[["Route", "Shipments", "Avg Lead Time (days)", "Delay Frequency (%)", "Efficiency Score"]]
            .round(1), hide_index=True, use_container_width=True
        )
    with c2:
        st.markdown("**🐌 Bottom 10 Least Efficient Routes**")
        bottom10 = sig_routes.nsmallest(10, "Efficiency Score")
        st.dataframe(
            bottom10[["Route", "Shipments", "Avg Lead Time (days)", "Delay Frequency (%)", "Efficiency Score"]]
            .round(1), hide_index=True, use_container_width=True
        )

    st.markdown("**Average Lead Time by Route** (top 20 by shipment volume)")
    top_volume = route_agg_display.nlargest(20, "Shipments").sort_values("Avg Lead Time (days)")
    fig = px.bar(
        top_volume, x="Avg Lead Time (days)", y="Route", orientation="h",
        color="Efficiency Score", color_continuous_scale="RdYlGn",
        hover_data=["Shipments", "Delay Frequency (%)"],
    )
<<<<<<< HEAD
    fig.update_layout(height=700, yaxis_title="", margin=dict(l=0, r=0, t=10, b=0))
=======
    fig.update_layout(height=600, yaxis_title="", margin=dict(l=0, r=0, t=10, b=0))
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 2: Geographic Shipping Map
# ---------------------------------------------------------------------
with tab2:
    st.subheader("US Heatmap — Shipping Efficiency by State")

    us_df = df[df["Country/Region"] == "United States"].dropna(subset=["State Abbr"])
    if us_df.empty:
        st.info("No United States shipments in the current filter selection.")
    else:
        state_agg = (
            us_df.groupby(["State/Province", "State Abbr"])
            .agg(
                Avg_Lead_Time=("Lead Time", "mean"),
                Shipments=("Row ID", "count"),
                Delay_Frequency=("Delayed", "mean"),
            )
            .reset_index()
        )
        state_agg["Delay_Frequency"] = (state_agg["Delay_Frequency"] * 100).round(1)

        map_metric = st.radio(
            "Color by", ["Avg Lead Time (days)", "Delay Frequency (%)", "Shipment Volume"],
            horizontal=True,
        )
        metric_col = {
            "Avg Lead Time (days)": "Avg_Lead_Time",
            "Delay Frequency (%)": "Delay_Frequency",
            "Shipment Volume": "Shipments",
        }[map_metric]
        color_scale = "Reds" if map_metric != "Shipment Volume" else "Blues"

        fig_map = go.Figure(data=go.Choropleth(
            locations=state_agg["State Abbr"],
            z=state_agg[metric_col],
            locationmode="USA-states",
            colorscale=color_scale,
            colorbar_title=map_metric,
            text=state_agg["State/Province"],
            hovertemplate="%{text}<br>" + map_metric + ": %{z:.1f}<extra></extra>",
        ))

        # Overlay factory locations
        fig_map.add_trace(go.Scattergeo(
            lon=[FACTORY_COORDS[f][1] for f in FACTORY_COORDS],
            lat=[FACTORY_COORDS[f][0] for f in FACTORY_COORDS],
            text=list(FACTORY_COORDS.keys()),
            mode="markers+text",
            textposition="top center",
            marker=dict(size=12, color="black", symbol="star"),
            name="Factories",
        ))

        fig_map.update_layout(
            geo=dict(scope="usa", projection_type="albers usa"),
<<<<<<< HEAD
            height=680, margin=dict(l=0, r=0, t=10, b=0),
=======
            height=550, margin=dict(l=0, r=0, t=10, b=0),
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
        )
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("**Geographic Bottlenecks** — high volume + poor performance")
        median_lt = state_agg["Avg_Lead_Time"].median()
        median_vol = state_agg["Shipments"].median()
        bottlenecks = state_agg[
            (state_agg["Avg_Lead_Time"] > median_lt) & (state_agg["Shipments"] > median_vol)
        ].sort_values("Avg_Lead_Time", ascending=False)
        st.dataframe(
            bottlenecks.rename(columns={
                "State/Province": "State", "Avg_Lead_Time": "Avg Lead Time (days)",
                "Delay_Frequency": "Delay Frequency (%)",
            })[["State", "Shipments", "Avg Lead Time (days)", "Delay Frequency (%)"]],
            hide_index=True, use_container_width=True,
        )
        st.caption("States above median shipment volume AND above median lead time — candidates for logistics review.")

# ---------------------------------------------------------------------
# TAB 3: Ship Mode Comparison
# ---------------------------------------------------------------------
with tab3:
    st.subheader("Shipping Efficiency by Ship Mode")

    mode_agg = (
        df.groupby("Ship Mode")
        .agg(
            Shipments=("Row ID", "count"),
            Avg_Lead_Time=("Lead Time", "mean"),
            Median_Lead_Time=("Lead Time", "median"),
            Delay_Frequency=("Delayed", "mean"),
            Avg_Cost=("Cost", "mean"),
            Avg_Sales=("Sales", "mean"),
        )
        .reset_index()
        .sort_values("Avg_Lead_Time")
    )
    mode_agg["Delay_Frequency"] = (mode_agg["Delay_Frequency"] * 100).round(1)

    c1, c2 = st.columns(2)
    with c1:
        fig_box = px.box(
            df, x="Ship Mode", y="Lead Time", color="Ship Mode",
            title="Lead Time Distribution by Ship Mode",
            category_orders={"Ship Mode": mode_agg["Ship Mode"].tolist()},
        )
<<<<<<< HEAD
        fig_box.update_layout(showlegend=False, height=500)
=======
        fig_box.update_layout(showlegend=False, height=420)
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
        st.plotly_chart(fig_box, use_container_width=True)
    with c2:
        fig_bar = px.bar(
            mode_agg, x="Ship Mode", y="Delay_Frequency", color="Ship Mode",
            title="Delay Frequency by Ship Mode (%)",
            category_orders={"Ship Mode": mode_agg["Ship Mode"].tolist()},
        )
<<<<<<< HEAD
        fig_bar.update_layout(showlegend=False, height=500, yaxis_title="Delay Frequency (%)")
=======
        fig_bar.update_layout(showlegend=False, height=420, yaxis_title="Delay Frequency (%)")
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("**Cost–Time Tradeoff (descriptive)**")
    st.caption(
        "Cost here is manufacturing cost, not a shipping-carrier fee, so this reflects the "
        "value of goods moving through each mode rather than a true freight cost comparison."
    )
    fig_scatter = px.scatter(
        mode_agg, x="Avg_Lead_Time", y="Avg_Cost", size="Shipments", color="Ship Mode",
        text="Ship Mode", labels={"Avg_Lead_Time": "Avg Lead Time (days)", "Avg_Cost": "Avg Cost ($)"},
    )
    fig_scatter.update_traces(textposition="top center")
<<<<<<< HEAD
    fig_scatter.update_layout(height=500)
=======
    fig_scatter.update_layout(height=420)
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("**Summary table**")
    st.dataframe(
        mode_agg.rename(columns={
            "Avg_Lead_Time": "Avg Lead Time (days)", "Median_Lead_Time": "Median Lead Time (days)",
            "Delay_Frequency": "Delay Frequency (%)", "Avg_Cost": "Avg Cost ($)", "Avg_Sales": "Avg Sales ($)",
        }).round(2), hide_index=True, use_container_width=True,
    )

# ---------------------------------------------------------------------
# TAB 4: Route Drill-Down
# ---------------------------------------------------------------------
with tab4:
    st.subheader("Route Drill-Down")

    dd_col1, dd_col2 = st.columns(2)
    with dd_col1:
        dd_factory = st.selectbox("Factory", sorted(df["Factory"].unique()))
    with dd_col2:
        state_choices = sorted(df[df["Factory"] == dd_factory]["State/Province"].unique())
        dd_state = st.selectbox("Customer State", state_choices)

    route_df = df[(df["Factory"] == dd_factory) & (df["State/Province"] == dd_state)]

    if route_df.empty:
        st.info("No shipments for this factory/state combination in the current filters.")
    else:
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Shipments", f"{len(route_df):,}")
        r2.metric("Avg Lead Time", f"{route_df['Lead Time'].mean():.1f} days")
        r3.metric("Lead Time Std Dev", f"{route_df['Lead Time'].std():.1f}")
        r4.metric("Delay Frequency", f"{route_df['Delayed'].mean()*100:.1f}%")

        st.markdown(f"**Order-Level Shipment Timeline: {dd_factory} → {dd_state}**")
        fig_timeline = px.scatter(
            route_df.sort_values("Order Date"), x="Order Date", y="Lead Time",
            color="Ship Mode", size="Sales", hover_data=["Order ID", "City", "Product Name"],
        )
        fig_timeline.add_hline(
            y=lead_time_threshold, line_dash="dash", line_color="red",
            annotation_text="Delay threshold",
        )
<<<<<<< HEAD
        fig_timeline.update_layout(height=550, yaxis_title="Lead Time (days)")
=======
        fig_timeline.update_layout(height=450, yaxis_title="Lead Time (days)")
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
        st.plotly_chart(fig_timeline, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Ship Mode Split**")
            mode_split = route_df["Ship Mode"].value_counts().reset_index()
            mode_split.columns = ["Ship Mode", "Count"]
            fig_pie = px.pie(mode_split, names="Ship Mode", values="Count", hole=0.4)
<<<<<<< HEAD
            fig_pie.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0))
=======
            fig_pie.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
            st.plotly_chart(fig_pie, use_container_width=True)
        with c2:
            st.markdown("**Product Mix**")
            prod_split = (
                route_df.groupby("Product Name")["Units"].sum()
                .sort_values(ascending=False).reset_index()
            )
            fig_prod = px.bar(prod_split, x="Units", y="Product Name", orientation="h")
<<<<<<< HEAD
            fig_prod.update_layout(height=400, yaxis_title="", margin=dict(l=0, r=0, t=10, b=0))
=======
            fig_prod.update_layout(height=320, yaxis_title="", margin=dict(l=0, r=0, t=10, b=0))
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
            st.plotly_chart(fig_prod, use_container_width=True)

        with st.expander("View raw order-level records"):
            st.dataframe(
                route_df[["Order ID", "Order Date", "Ship Date", "Lead Time", "Ship Mode",
                          "City", "Product Name", "Units", "Sales", "Gross Profit"]]
                .sort_values("Order Date"),
                hide_index=True, use_container_width=True,
            )

st.divider()
st.caption(
    "Nassau Candy Distributor — Factory-to-Customer Shipping Route Efficiency Analysis · "
    f"Data as of {datetime.now().strftime('%B %Y')}"
<<<<<<< HEAD
)
=======
)
>>>>>>> 51c19d553478f65f4904926d2182d4d7aab7394a
