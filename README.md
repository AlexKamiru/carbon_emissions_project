#  Carbon Emissions & Inequality Analysis

This project explores how CO₂ emissions, air pollution (PM2.5), and GDP relate across countries of different income levels. The aim is to analyze whether poorer countries are disproportionately impacted as they industrialize.

##  Project Structure
carbon_emissions_project/
│
├── data/
│ ├── raw/ # Original datasets
│ │ ├── co2_emissions.csv
│ │ ├── air_pollution.csv
│ │ ├── temperature_data.csv
│ │ └── income_group.csv
│ └── processed/
│ └── combined_data.csv # Merged and cleaned dataset
│
├── outputs/
│ ├── plots/
│ │ ├── co2_income_share.png
│ │ ├── co2_vs_gdp_scatter.png
│ │ ├── industrializing_poor_countries.png
│ │ └── pm25_exposure_by_income.png
│ └── tables/
│ └── ()
│
├── scripts/
│ ├── clean_data.py
│ ├── load_data.py
│ ├── merge_data.py
│ ├── analyze_data.py
│ └── visualize.py
│
├── utils/ # Helper functions (optional)
│
├── main.py # Main execution script
├── requirements.txt # Python package dependencies
└── README.md # You're here!



## Key Analyses & Visualizations

- **CO₂ Emissions by Income Group**  
  `outputs/plots/co2_income_share.png`

- **GDP vs CO₂ Emissions Growth**  
  `outputs/plots/co2_vs_gdp_scatter.png`

- **Are Poor Countries Punished for Industrializing?**  
  `outputs/plots/industrializing_poor_countries.png`

- **PM2.5 Exposure by Income Group**  
  `outputs/plots/pm25_exposure_by_income.png`

##  How to Run

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/carbon_emissions_project.git
   cd carbon_emissions_project

2. **Set up a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/Scripts/activate  # On Windows

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Run the main script**
    ```bash
    python main.py


 **Features**
1. Data Cleaning & Merging (across climate, pollution, and    economic indicators)

2. Growth analysis: CO₂ vs GDP

3. Exposure analysis: PM2.5 vs income

4. Industrialization stress on low-income countries

5. Insightful Seaborn plots        


**Datasets Used**
Our World in Data – CO₂ Emissions(https://ourworldindata.org/co2-emissions)

World Bank – PM2.5 Air Pollution(https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)

World Bank – Income Groups(https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups)


**Author**
Created by Alex Kamiru – aspiring data scientist passionate about global sustainability, economics, and storytelling with data.

