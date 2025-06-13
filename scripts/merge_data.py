import pandas as pd

def merge_datasets(co2_clean, pollution_clean, temp_clean, income_clean):
    # Merge CO2 and pollution on country + year
    merged = pd.merge(co2_clean, pollution_clean, on=["country", "year"], how="outer")

    # Merge with temperature on year (no country)
    merged = pd.merge(merged, temp_clean, on="year", how="left")

    # Merge with income group on country
    merged = pd.merge(merged, income_clean, on="country", how="left")

    return merged
