import pandas as pd

# 1. Clean CO₂ Emissions Dataset

def clean_co2_data(df):

    df = df.copy()  # ADD THIs
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()
    
    # Drop rows missing key data
    df = df.dropna(subset=["country", "year", "co2"])
    
    # Keep only necessary columns for analysis (you can still customize this)
    keep_cols = ["country", "year", "co2", "co2_per_capita", "gdp", "population", "iso_code"]
    df = df[[col for col in keep_cols if col in df.columns]]

    # Convert year to int
    df["year"] = df["year"].astype(int)

    # Clean country names
    df["country"] = df["country"].str.strip()

    # Filter year range
    df = df[df["year"] >= 1990]

    return df


# 2. Clean Air Pollution Dataset


def clean_pollution_data(df):
    df = df.copy()  # ADD THIs
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Rename for consistency
    df.rename(columns={"country_name": "country", "pm25_concentration": "pm2_5"}, inplace=True)

    # Drop missing rows
    df = df.dropna(subset=["country", "year", "pm2_5"])

    # Convert year to int
    df["year"] = df["year"].astype(int)

    # Keep only the columns you care about
    keep_cols = ["country", "year", "pm2_5", "latitude", "longitude"]
    df = df[[col for col in keep_cols if col in df.columns]]

    df["country"] = df["country"].str.strip()

    return df


# 3. Clean Income Group Dataset


def clean_income_group_data(df):
    df = df.copy()  # ADD THIs
    df.columns = df.columns.str.lower().str.strip()
    df.rename(columns={"economy": "country", "income group": "income_group"}, inplace=True)

    df = df.dropna(subset=["country", "income_group"])
    df["country"] = df["country"].str.strip()
    df["income_group"] = df["income_group"].str.title()

    return df


# 4. Clean Temperature Dataset

def clean_temperature_data(df):
    df = df.copy()  # ADD THIs
    df.columns = df.columns.str.lower().str.strip()
    df.rename(columns={"anomaly": "temperature"}, inplace=True)

    df = df.dropna(subset=["year", "temperature"])
    df["year"] = df["year"].astype(int)

    return df
