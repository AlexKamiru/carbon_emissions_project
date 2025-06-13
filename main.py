import os
import pandas as pd

#data loading
from scripts.load_data import (
    load_co2_data,
    load_air_pollution_data,
    load_temperature_data,
    load_income_group_data)

#data cleaning
from scripts.clean_data import (
    clean_co2_data,
    clean_pollution_data,
    clean_income_group_data,
    clean_temperature_data
)

#data merging
from scripts.merge_data import merge_datasets

#Analysis
from scripts.analyze_data import (
    rich_countries_co2_share,
    co2_vs_gdp_growth,
    industrializing_poor_countries,
    pm25_exposure_by_income
)

#Visualisation
from scripts.visualize import (
    plot_income_group_co2_share,
    plot_co2_vs_gdp,
    plot_poor_countries_industrialization,
    plot_pm25_by_income)


def main():
    # 1. Load raw data
    co2 = load_co2_data("data/raw/co2_emissions.csv")
    pollution = load_air_pollution_data("data/raw/air_pollution.csv")
    temperature = load_temperature_data("data/raw/temperature_data.csv")
    income = load_income_group_data("data/raw/income_group.csv")

    # 2. Clean each dataset
    co2_clean = clean_co2_data(co2)
    pollution_clean = clean_pollution_data(pollution)
    temp_clean = clean_temperature_data(temperature)
    income_clean = clean_income_group_data(income)

    # 3. Merge all datasets
    combined_df = merge_datasets(co2_clean, pollution_clean, temp_clean, income_clean)

    # 4. Save final dataset
    combined_df.to_csv("data/processed/combined_data.csv", index=False)

    # 5. Summary
    print("Data pipeline complete!")
    print(f"Combined dataset shape: {combined_df.shape}")
    print(f"Columns: {list(combined_df.columns)}")
    print(combined_df.head())

    #---------------------------------
          #ANALYSIS AND VISUALIZATION
    #---------------------------------
          

        #ANALYSIS 1: Are rich countries causing most of the CO2 emissions? ===
    co2_by_income = rich_countries_co2_share(combined_df)
    print("\n CO2 Emissions by Income Group:")
    print(co2_by_income)
        #visualisation
    plot_income_group_co2_share(co2_by_income) 


        #ANALYSIS 2: Is economic growth always tied to pollution? ===
    gdp_co2_corr,gdp_co2_df = co2_vs_gdp_growth(combined_df)
    print(f"\n Correlation between GDP and CO2 Growth: {gdp_co2_corr:.3f}")
        #visualisation
    plot_co2_vs_gdp(gdp_co2_df)


        #ANALYSIS 3a: Are poor countries punished for industrializing?(Growth view) ===
    poor_countries_summary = industrializing_poor_countries(combined_df)
    print("\n Industrializing Poor Countries Summary:")
    print(poor_countries_summary.head())
        # visualisation
    plot_poor_countries_industrialization(poor_countries_summary)


        #ANALYSIS 3b: Are poor countries punished?( Air quality view) ===
    pm25_summary = pm25_exposure_by_income(combined_df)
    print("\n PM2.5 Exposure by Income Group:")
    print(pm25_summary)
        #visualization
    plot_pm25_by_income(combined_df)


    # all analyses complete! Visualisations saved to outputs/plots

# ensure output directories exist
os.makedirs("outputs/plots", mode=0o777, exist_ok=True)
os.makedirs("outputs/tables",mode=0o777,exist_ok=True)

if __name__ == "__main__":
    main()
