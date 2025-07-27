import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================
# ✅ Helper Functions
# ==========================

def clean_for_plotting(df, required_columns):
    """
    Cleans dataframe for Plotly plotting:
    - Drops rows with NaN in required columns
    - Fills population (if present) with 1 to avoid size errors
    """
    df_clean = df.dropna(subset=required_columns).copy()

    if "population" in required_columns and "population" in df_clean.columns:
        df_clean["population"] = df_clean["population"].fillna(1)

    return df_clean


@st.cache_data
def load_data():
    """Load processed combined data"""
    df = pd.read_csv("data/processed/combined_data.csv")
    return df


# ==========================
# ✅ Streamlit App
# ==========================

st.set_page_config(page_title="CO₂ Emissions Dashboard", layout="wide")

st.title("🌍 CO₂ Emissions: Interactive Data Story")
st.markdown("Analyze relationships between **GDP, Pollution, and CO₂ emissions**.")

# ---- Load Data ----
df = load_data()

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filters")
income_groups = st.sidebar.multiselect(
    "Select Income Groups",
    options=df["income_group"].dropna().unique(),
    default=df["income_group"].dropna().unique()
)

regions = st.sidebar.multiselect(
    "Select Regions",
    options=df["region"].dropna().unique(),
    default=df["region"].dropna().unique()
)

filtered_df = df[(df["income_group"].isin(income_groups)) & (df["region"].isin(regions))]

st.markdown(f"**Showing {len(filtered_df)} records after filtering.**")

# ==========================
# ✅ PLOTS
# ==========================

# --- 1. CO₂ vs GDP Scatter ---
plot_df = clean_for_plotting(filtered_df, ["gdp", "co2", "population"])
fig1 = px.scatter(
    plot_df,
    x="gdp",
    y="co2",
    color="income_group",
    size="population",
    hover_name="country",
    title="CO₂ Emissions vs GDP",
    size_max=60
)
st.plotly_chart(fig1, use_container_width=True)

# --- 2. CO₂ Emissions by Income Group (Bar Chart) ---
plot_df = clean_for_plotting(filtered_df, ["income_group", "co2"])
fig2 = px.bar(
    plot_df.groupby("income_group", as_index=False)["co2"].mean(),
    x="income_group",
    y="co2",
    color="income_group",
    title="Average CO₂ Emissions by Income Group"
)
st.plotly_chart(fig2, use_container_width=True)

# --- 3. PM2.5 Pollution by Income Group (Bar Chart) ---
if "pm2_5" in filtered_df.columns:
    plot_df = clean_for_plotting(filtered_df, ["income_group", "pm2_5"])
    fig3 = px.bar(
        plot_df.groupby("income_group", as_index=False)["pm2_5"].mean(),
        x="income_group",
        y="pm2_5",
        color="income_group",
        title="Average PM2.5 Pollution by Income Group"
    )
    st.plotly_chart(fig3, use_container_width=True)

# --- 4. GDP vs PM2.5 Scatter (Optional Extra Insight) ---
if "pm2_5" in filtered_df.columns:
    plot_df = clean_for_plotting(filtered_df, ["gdp", "pm2_5"])
    fig4 = px.scatter(
        plot_df,
        x="gdp",
        y="pm2_5",
        color="income_group",
        hover_name="country",
        title="GDP vs PM2.5 Pollution"
    )
    st.plotly_chart(fig4, use_container_width=True)

# ==========================
# ✅ Display Regression Summary (Optional)
# ==========================

if os.path.exists("outputs/tables/regression_summary_q1_multiple.csv"):
    st.subheader("📑 Regression Summary (Q1: Multiple Regression)")
    summary_df = pd.read_csv("outputs/tables/regression_summary_q1_multiple.csv")
    st.dataframe(summary_df)
