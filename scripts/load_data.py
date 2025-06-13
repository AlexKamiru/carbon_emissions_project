import pandas as pd

def load_co2_data(path='data/raw/co2_emissions.csv'):
    """Load CO2 emissions dataset."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[Error] File not found: {path}")
        return pd.DataFrame()  # Or raise exception, depending on your use case

def load_air_pollution_data(path='data/raw/air_pollution.csv'):
    """Load air pollution dataset (PM2.5) from a CSV file."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[Error] File not found: {path}")
        return pd.DataFrame()

def load_temperature_data(path='data/raw/temperature_data.csv'):
    """Load temperature anomaly dataset from a CSV file."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[Error] File not found: {path}")
        return pd.DataFrame()

def load_income_group_data(path='data/raw/income_group.csv'):
    """Load World Bank income group classification dataset from a CSV file."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"[Error] File not found: {path}")
        return pd.DataFrame()