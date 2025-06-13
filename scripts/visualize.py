import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib 
matplotlib.use('Agg')

from scripts.analyze_data import (
    rich_countries_co2_share,
    co2_vs_gdp_growth,
    industrializing_poor_countries,
    pm25_exposure_by_income,
)

# Set default Seaborn style
sns.set(style="whitegrid")

# Output path for saving plots
OUTPUT_DIR = r"C:\Users\USER\Desktop\carbon_emissions_project\outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_income_group_co2_share(co2_by_income):
    """
    Visualizes CO2 emissions share by income group as a bar plot.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=co2_by_income.reset_index(),
        x="income_group",
        y="percent_share",
        palette="coolwarm"
    )
    plt.title("Share of Global CO₂ Emissions by Income Group")
    plt.xlabel("Income Group")
    plt.ylabel("Percent Share (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    output_path = os.path.join("outputs", "plots", "co2_income_share.png")
    plt.savefig(output_path)
    plt.close()

def plot_co2_vs_gdp(filtered_df):
    """Scatter plot of CO2 per capita vs GDP with correlation annotation."""
    output_path = os.path.join(OUTPUT_DIR, "co2_vs_gdp_scatter.png")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=filtered_df, x="gdp", y="co2_per_capita", alpha=0.5)
    plt.title("CO₂ per Capita vs GDP")
    plt.xlabel("GDP")
    plt.ylabel("CO₂ per Capita")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_poor_countries_industrialization(summary):
    """Bar plot for average CO2 growth in poor countries."""
    #summary = industrializing_poor_countries(poor_countries_summary)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="co2_growth_prct", y="country", data=summary.sort_values("co2_growth_prct", ascending=False), palette="viridis")
    plt.title("Average CO₂ Growth in Low-Income Countries")
    plt.xlabel("Average CO₂ Growth (%)")
    plt.ylabel("Country")
    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "industrializing_poor_countries.png"))
    plt.close()


def plot_pm25_by_income(combined_df):
    """Bar plot of PM2.5 exposure by income group."""
    exposure = pm25_exposure_by_income(combined_df)

    plt.figure(figsize=(8, 6))
    sns.barplot(x="income_group", y="avg_pm2_5", data=exposure, palette="magma")
    plt.title("Average PM2.5 Exposure by Income Group")
    plt.xlabel("Income Group")
    plt.ylabel("Average PM2.5 Concentration")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "pm25_exposure_by_income.png"))
    plt.close()


def generate_all_visualizations(combined_df):
    """Run all visualizations using the cleaned combined data."""
    plot_income_group_co2_share(combined_df)
    plot_co2_vs_gdp(combined_df)
    plot_poor_countries_industrialization(combined_df)
    plot_pm25_by_income(combined_df)
