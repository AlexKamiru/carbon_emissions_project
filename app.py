import streamlit as st

# -------------------------
# 📌 INTRODUCTION SECTION
# -------------------------
st.title("🌍 CO₂ Emissions Analysis & Prediction")
st.markdown("""
Welcome to this interactive dashboard exploring **global CO₂ emissions** and their relationship with key socioeconomic and environmental factors.

---

### 🔍 **Why This Project?**

Climate change is one of the most pressing challenges of our time. Understanding the **drivers of CO₂ emissions** helps policymakers, researchers, and citizens make informed decisions for a sustainable future.

---

### 📊 **What You'll Find Here:**

- Insights on how GDP, PM2.5, and population impact CO₂ emissions
- Visual analysis by **country**, **region**, and **income group**
- Regression models to predict emissions
- A full walkthrough from data cleaning to model comparison

---

### 🛠️ **Tools & Techniques Used:**

- Python (pandas, scikit-learn, seaborn, plotly)
- Regression modeling: Linear, Ridge, Lasso
- Data visualization (Plotly)
- Streamlit for interactivity

---

""")

# -------------------------
# 📊 DATA SOURCES & OVERVIEW
# -------------------------
st.header("📊 Data Sources & Overview")

st.markdown("""
This project combines multiple open datasets to explore the factors influencing **CO₂ emissions** across countries and over time.

---

### 📚 **Datasets Used:**

- **CO₂ Emissions Data:** Global emissions by country and year (Our World in Data)
- **PM2.5 Air Pollution:** Fine particulate matter concentrations (World Bank)
- **GDP & Population:** Economic and demographic data (World Bank)
- **Income Groups & Regions:** World Bank classification

---

All data is preprocessed and merged into a single dataset (`combined_data.csv`) for analysis.
""")

# Load Data
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/combined_data.csv")
    return df

df = load_data()

# Optional Filters
st.subheader("🔎 Explore the Dataset")
region_filter = st.selectbox("Filter by region (optional):", ["All"] + sorted(df["region"].dropna().unique()))
income_filter = st.selectbox("Filter by income_group (optional):", ["All"] + sorted(df["income_group"].dropna().unique()))

# Apply filters
filtered_df = df.copy()
if region_filter != "All":
    filtered_df = filtered_df[filtered_df["region"] == region_filter]
if income_filter != "All":
    filtered_df = filtered_df[filtered_df["income_group"] == income_filter]

# Show data
st.dataframe(filtered_df.head(50), use_container_width=True)


import plotly.express as px
import pandas as pd

from scripts.analyze_data import (
    rich_countries_co2_share,
    co2_vs_gdp_growth,
    industrializing_poor_countries,
    pm25_exposure_by_income
)

# Load cleaned data
df = pd.read_csv("data/processed/combined_data.csv")

st.set_page_config(page_title="CO₂ Emissions Analysis", layout="wide")
st.title("🌍 Guided Analysis: CO₂ Emissions, Economics, and Equity")

st.markdown("""
Explore key questions at the intersection of **climate, economics, and justice**:
- Are rich countries causing most of the emissions?
- Is economic growth always tied to pollution?
- Are poor countries punished for industrializing?
""")

# ------------------------------------------------
# Q1: Are Rich Countries Causing Most of the CO₂ Emissions?
# ------------------------------------------------
st.header("1️⃣ Are Rich Countries Causing Most of the CO₂ Emissions?")
st.markdown("""
This analysis investigates whether wealthier nations contribute more to global CO₂ emissions. 
It’s crucial for assessing global responsibility and equity in climate action.
""")

co2_share_df = rich_countries_co2_share(df)

fig_q1 = px.bar(
    co2_share_df.reset_index(),
    x="income_group",
    y="percent_share",
    color="income_group",
    text="percent_share",
    title="CO₂ Emissions Share by Income Group",
    labels={"percent_share": "Share of Global Emissions (%)"}
)

st.plotly_chart(fig_q1, use_container_width=True)

st.dataframe(co2_share_df.style.format({"total_co2": "{:,.0f}", "percent_share": "{:.2f}%"}))

st.markdown("✅ **Insight:** High-income and upper-middle-income countries account for a significant share of global CO₂ emissions, despite having lower populations compared to lower-income regions.")

# ------------------------------------------------
# Q2: Is Economic Growth Always Tied to Pollution?
# ------------------------------------------------
st.header("2️⃣ Is Economic Growth Always Tied to Pollution?")
st.markdown("""
This section explores the **correlation between GDP and CO₂ emissions per capita** to examine if economic progress inevitably increases pollution — or if countries are decoupling growth from emissions.
""")

correlation_value, scatter_df = co2_vs_gdp_growth(df)

fig_q2 = px.scatter(
    scatter_df,
    x="gdp",
    y="co2_per_capita",
    log_x=True,
    trendline="ols",
    title=f"GDP vs CO₂ per Capita (Correlation: {correlation_value:.2f})",
    labels={"gdp": "GDP (log scale)", "co2_per_capita": "CO₂ Emissions per Capita"}
)

st.plotly_chart(fig_q2, use_container_width=True)

st.markdown(f"✅ **Insight:** The Pearson correlation coefficient is **{correlation_value:.2f}**, suggesting that while emissions generally increase with GDP, **some economies may decouple growth from pollution**.")

# ------------------------------------------------
# Q3: Are Poor Countries Punished for Industrializing?
# ------------------------------------------------
st.header("3️⃣ Are Poor Countries Punished for Industrializing?")
st.markdown("""
We analyze two dimensions:
1. **Growth Penalty** – Do low-income countries face higher emissions growth as they industrialize?
2. **Air Quality Exposure** – Are poorer regions more exposed to pollution like PM2.5?
""")

# -- 3a: Growth Penalty
st.subheader("📈 Industrial Growth vs Emissions in Low-Income Countries")

poor_growth_summary = industrializing_poor_countries(df)

fig_q3a = px.scatter(
    poor_growth_summary,
    x="gdp",
    y="co2_growth_prct",
    size="co2_per_capita",
    hover_name="country",
    title="GDP vs CO₂ Growth in Low-Income Countries",
    labels={"gdp": "Average GDP", "co2_growth_prct": "Avg CO₂ Growth (%)"}
)

st.plotly_chart(fig_q3a, use_container_width=True)

st.markdown("✅ **Insight:** Many poor countries are growing economically and increasing emissions — but still contribute **very little** overall. Growth can mean trade-offs without the right support.")

# -- 3b: Air Quality
st.subheader("🌫️ Air Quality: PM2.5 Exposure by Income Group")

pm25_df = pm25_exposure_by_income(df)

fig_q3b = px.bar(
    pm25_df,
    x="income_group",
    y="avg_pm2_5",
    color="income_group",
    title="Average PM2.5 Exposure by Income Group",
    labels={"avg_pm2_5": "PM2.5 Concentration (μg/m³)"}
)

st.plotly_chart(fig_q3b, use_container_width=True)

st.markdown("""
✅ **Insight:** Despite contributing less to global emissions, **low-income groups experience higher exposure to air pollution**. This reflects global environmental injustice.
""")

# ------------------------------------------------
# End Note
# ------------------------------------------------
st.markdown("""
---
📘 Curious to explore the models behind this dashboard?  
See the code in `analyze_data.py` and other modules for detailed logic and preprocessing.

🔍 Built with: `pandas`, `plotly`, `Streamlit`
""")


# Regression Analysis Section
st.header("📊 Regression Analysis")
st.markdown("""
This section explores four key questions using regression models to understand the drivers of CO₂ emissions:
1. Do rich countries have high CO₂ emissions?
2. Is economic growth always tied to pollution?
3. Are poor countries punished for industrializing?
4. Which factor (GDP, population, PM2.5) is the strongest predictor?

We use different regression models (linear, polynomial, and one-hot encoded) to provide insights.
""")

## Q1 – Do Rich Countries Have High CO₂ Emissions?
st.header("Q1: Do Rich Countries Have High CO₂ Emissions?")
st.markdown("""
**Hypothesis:** Rich countries, with higher GDPs, emit more CO₂.

We'll test this with:
- ✅ Simple Linear Regression: `GDP → CO₂`
- ✅ Multiple Linear Regression: `GDP + Population + PM2.5 → CO₂`
""")

# --- Load data
df= pd.read_csv("data/processed/combined_data.csv").copy()  # Assuming combined_df is already loaded and preprocessed

from scripts.regression_models import run_q1_simple_regression, run_q1_multiple_regression

# --- Run models
simple_model, x_test_simple, y_test_simple, y_pred_simple = run_q1_simple_regression(df)
multi_model, x_test_multi, y_test_multi, y_pred_multi = run_q1_multiple_regression(df)

# === SIMPLE REGRESSION OUTPUTS ===
st.subheader("1. Simple Linear Regression (GDP → CO₂ Emissions)")

# Metrics
st.markdown("**Evaluation Metrics:**")
q1_simple_metrics = pd.read_csv("outputs/tables/regression_summary_q1_simple.csv")
st.dataframe(q1_simple_metrics, use_container_width=True)

# Plot
st.image("outputs/plots/q1_simple_regression.png", caption="Fitted Line: GDP vs CO₂")

# Insight
st.markdown("""
**Insight:**  
This model captures the general upward trend, but GDP alone doesn't explain all variation in emissions (as reflected in R² and RMSE).  
""")

# === MULTIPLE REGRESSION OUTPUTS ===
st.subheader("2. Multiple Linear Regression (GDP + Population + PM2.5 → CO₂)")

# Metrics
st.markdown("**Evaluation Metrics:**")
q1_multi_metrics = pd.read_csv("outputs/tables/regression_summary_q1_multiple.csv")
st.dataframe(q1_multi_metrics, use_container_width=True)

# Plot
st.image("outputs/plots/q1_multiple_actual_vs_pred.png", caption="Actual vs Predicted CO₂ Emissions")

# Insight
st.markdown("""
**Insight:**  
Adding **population** and **air pollution (PM2.5)** improves model performance (higher R², lower RMSE).  
This suggests that CO₂ emissions are more strongly influenced by **a combination of economic size and environmental/population pressures**, not GDP alone.
""")

# ==============================
# Q2: IS ECONOMIC GROWTH TIED TO POLLUTION?
# ==============================
st.markdown("## Q2: Is Economic Growth Tied to Pollution?")
st.markdown("""
We explore whether **economic growth (GDP)** has a **nonlinear relationship** with CO₂ emissions using a **2nd-degree polynomial regression** model. 
Due to skewed GDP distribution, we apply a **log transformation** to the predictor before fitting the model.
""")

from scripts.regression_models import check_gdp_distribution, run_q2_polynomial_regression 

# Show GDP distribution
with st.expander("See GDP Distribution"):
    skewness = check_gdp_distribution(df)
    st.image("outputs/plots/gdp_distribution.png", caption="Histogram of GDP (Skewed Distribution)", use_container_width=True)
    st.markdown(f"**Skewness:** {skewness:.2f}")
    if skewness > 1:
        st.warning("GDP is highly skewed → log transformation applied before modeling.")

# Run polynomial regression
model, X_test, y_test, y_pred = run_q2_polynomial_regression(df)

# Display results
st.image("outputs/plots/regression_q2_polynomial.png", caption="Polynomial Fit: log(GDP) vs CO₂", use_container_width=True)

st.markdown("### Model Performance")
summary_q2 = pd.read_csv("outputs/tables/regression_summary_q2_polynomial.csv")
st.dataframe(summary_q2, use_container_width=True)

with st.expander("See Statsmodels OLS Summary (Q2)"):
    with open("outputs/tables/regression_summary_q2_polynomial_statsmodels.txt", "r") as f:
        st.text(f.read())

st.markdown("""
### ✅ Insight
The **polynomial regression curve** suggests that the relationship between GDP and CO₂ emissions is **non-linear**. 
Higher GDP tends to correlate with higher emissions, but the rate of increase may vary.
""")


# =========================
# Q3: Are Poor Countries Punished for Industrializing?
# =========================
st.header("📉 Q3: Are Poor Countries Punished for Industrializing?")
st.markdown("""
In this section, we investigate whether **low-income countries are penalized with higher CO₂ emissions as they industrialize**.
We use a **multiple linear regression** model that includes:
- **GDP** (economic indicator)
- **PM2.5** (pollution)
- **Income group** (one-hot encoded)

This helps us assess if income classification influences emissions **after accounting for economic growth and pollution**.
""")

from scripts.regression_models import run_q3_income_group_regression

# Run model
model_q3, x_test_q3, y_test_q3, y_pred_q3 = run_q3_income_group_regression(df)

# === Visuals ===
col1, col2 = st.columns(2)

# (A) Actual vs Predicted Scatter Plot
with col1:
    st.subheader("🔍 Actual vs Predicted CO₂ Emissions")
    st.image("outputs/plots/regression_q3_actual_vs_predicted.png", use_column_width=True)
    st.caption("This scatter plot compares predicted CO₂ emissions with actual values. \
A tighter diagonal pattern indicates better model performance.")

# (B) Feature Importance
with col2:
    st.subheader("📊 Feature Importance (Coefficient Size)")
    st.image("outputs/plots/regression_q3_feature_importance.png", use_column_width=True)
    st.caption("The bar plot displays the regression coefficients. \
Larger absolute values indicate stronger influence on CO₂ emissions.")

# === Insight ===
st.markdown("""
#### 💡 Insight:
The regression suggests that **GDP and PM2.5** remain strong predictors of CO₂ emissions.  
However, income group dummies (e.g., "Upper middle income", "High income") also show measurable impact—indicating **systemic inequality** in emission contributions and consequences.

This could imply that **lower-income countries**, despite emitting less, may experience disproportionate burdens as they industrialize.
""")
