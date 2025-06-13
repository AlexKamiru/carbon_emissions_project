import pandas as pd

# Utility function to drop rows with missing values in specified columns
def clean_for_columns(df, columns):
    """Drop rows where any of the listed columns have missing values."""
    return df.dropna(subset=columns)


# 1. Are rich countries causing most of the CO2 emissions?
def rich_countries_co2_share(combined_df):
    """
    Compare total CO2 emissions across income groups.
    Returns a DataFrame showing total emissions and percentage share by group.
    """
    # Clean data for relevant columns
    columns_needed = ["co2", "income_group"]
    df_clean = clean_for_columns(combined_df, columns_needed)
    
    # Aggregate CO2 by income group
    co2_sum = df_clean.groupby("income_group")["co2"].sum().sort_values(ascending=False)
    
    # Calculate each group's share of total emissions
    co2_percent = 100 * co2_sum / co2_sum.sum()
    
    # Combine results into a single DataFrame
    result = pd.DataFrame({"total_co2": co2_sum, "percent_share": co2_percent})
    return result


# 2. Is economic growth always tied to pollution?
def co2_vs_gdp_growth(combined_df):
    """
    Calculate the correlation between GDP and CO2 per capita.
    Returns a single correlation value (Pearson coefficient).
    """
    filtered_df = combined_df[["co2_per_capita", "gdp"]].dropna()
    corr = filtered_df["co2_per_capita"].corr(filtered_df["gdp"])
    return corr, filtered_df


# 3a. Are poor countries punished for industrializing? (Growth perspective)
def industrializing_poor_countries(combined_df):
    """
    Analyze how low-income countries' CO2 per capita and GDP are evolving.
    Returns a country-level summary of average CO2 growth, emissions, and GDP.
    """
    # Step 1: Sort and calculate CO2 growth percentage by country
    combined_df = combined_df.sort_values(by=["country", "year"])
    combined_df["co2_growth_prct"] = combined_df.groupby("country")["co2"].pct_change() * 100

    # Step 2: Clean data for relevant columns (after growth is calculated)
    columns_needed = ["income_group", "co2_growth_prct", "co2_per_capita", "gdp", "country"]
    df_clean = clean_for_columns(combined_df, columns_needed)

    # Step 3: Focus only on low-income countries
    df_poor = df_clean[df_clean["income_group"] == "Low Income"]

    # Step 4: Group by country and compute mean values for each indicator
    summary = df_poor.groupby("country").agg({
        "co2_growth_prct": "mean",
        "co2_per_capita": "mean",
        "gdp": "mean"
    }).reset_index()

    return summary


# 3b. Are poor countries punished for industrializing? (Air quality perspective)
def pm25_exposure_by_income(combined_df):
    """
    Evaluate average PM2.5 air pollution exposure by income group.
    Returns a DataFrame with average PM2.5 concentration per group.
    """
    # Clean data for relevant columns
    columns_needed = ["income_group", "pm2_5"]
    df_clean = clean_for_columns(combined_df, columns_needed)
    
    # Compute average PM2.5 for each income group
    exposure = df_clean.groupby("income_group")["pm2_5"].mean().reset_index()
    exposure.columns = ["income_group", "avg_pm2_5"]
    
    return exposure
