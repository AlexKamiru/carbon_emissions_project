```markdown
# 🌍 Carbon Emissions & Inequality Analysis  

This project explores the relationship between CO₂ emissions, economic growth, and air pollution across different income groups. Using data storytelling, statistical analysis, and regression modeling, it uncovers key insights into how industrialization and wealth distribution contribute to environmental inequality.

Key Questions Addressed
✔ Do richer countries produce higher CO₂ emissions?
✔ Is economic growth strongly tied to pollution levels?
✔ Are poorer countries penalized for industrializing?
✔ Which factor—GDP, population, or air pollution (PM2.5)—is the strongest predictor of CO₂ emissions?

Highlights
Data Pipeline: Automated cleaning, merging, and processing of raw datasets (CO₂ emissions, GDP, PM2.5, and climate data).

Exploratory Analysis & Visualizations: Income-group comparisons, correlation analysis, and pollution exposure trends.

Regression Modeling:

Simple & Multiple Linear Regression

Polynomial Regression (log-transformed GDP)

Standardized Feature Importance Analysis

Outputs: Publication-ready plots, statistical summaries, and feature importance rankings.

Tech Stack
Python (pandas, seaborn, matplotlib, scikit-learn, statsmodels)

Data Sources: World Bank, Climate & Air Pollution Datasets

Environment: Virtual environment (.venv) with reproducible dependencies (requirements.txt)
---

##  **Project Structure**

```markdown 

carbon_emissions_project/
│
├── data/
│   ├── raw/
│   │   ├── air_pollution.csv
│   │   ├── co2_emissions.csv
│   │   ├── income_group.csv
│   │   └── temperature_data.csv
│   └── processed/
│       └── combined_data.csv
│
├── models/
│   ├── q1_simple_regression_model.pkl
│   ├── q1_multiple_regression_model.pkl
│   ├── q2_polynomial_regression_model.pkl
│   ├── q3_income_group_regression_model.pkl
│   ├── q4_standardized_regression_model.pkl
│   └── q4_standardized_scaler.pkl
│
├── outputs/
│   ├── plots/
│   │   ├── regression_q4_actual_vs_predicted.png
│   │   └── regression_q4_feature_importance.png
│   ├── tables/
│   │   ├── regression_summary_q1_simple_statsmodels.txt
│   │   ├── regression_summary_q1_multiple_statsmodels.txt
│   │   ├── regression_summary_q2_polynomial_statsmodels.txt
│   │   └── regression_summary_q3_income_group_statsmodels.txt
│   └── text_summaries/
│       └── regression_summary_q4_standardized.txt
│
├── scripts/
│   ├── load_data.py
│   ├── clean_data.py
│   ├── merge_data.py
│   ├── analyze_data.py
│   └── regression_models.py
│
├── README.md                 (documentation)
├── requirements.txt           
├── .gitignore
└── venv/ (or .venv)           

```

```markdown

##  **Key Analyses & Findings**

### **1. CO₂ Emissions by Income Group**
- **Upper Middle-Income countries** dominate global emissions (~89%).  
- **Low-income countries** contribute almost **0%**, yet face severe climate impacts.  
  *Plot:* `outputs/plots/co2_income_share.png`

---

### **2. GDP vs CO₂ Emissions Growth**
- Weak overall correlation (**r ≈ 0.06**), but…  
- **Industrializing poor countries** (e.g., Chad, Burkina Faso) show sharp **CO₂ growth despite low GDP**.  
  *Plots:*  
`outputs/plots/co2_vs_gdp_scatter.png`  
`outputs/plots/industrializing_poor_countries.png`

---

### **3. PM2.5 Exposure by Income**
- **Low- & lower-middle-income groups** face **4–5× higher PM2.5 levels** than high-income countries.  
  *Plot:* `outputs/plots/pm25_exposure_by_income.png`

---

### **4. Regression Models (Q1–Q4)**

| **Question** | **Model** | **R²** | **RMSE** | **Key Insight** |
|--------------|-----------|-------:|---------:|-----------------|
| **Q1** | Simple Linear Regression (GDP → CO₂) | 0.97 | 586 | GDP alone explains most variation in emissions |
| **Q1** | Multiple Linear (GDP, Population, PM2.5 → CO₂) | 0.98 | 486 | Population matters significantly |
| **Q2** | Polynomial (log(GDP)² → CO₂) | 0.83 | 1598 | Emissions accelerate non-linearly with GDP |
| **Q3** | Multiple (Income Group + GDP + PM2.5 → CO₂) | 0.98 | 523 | **Upper Middle-Income** drives emissions |
| **Q4** | Feature Importance (Standardized) | 0.98 | 488 | **GDP strongest predictor**, followed by Population, PM2.5 |

 *Regression Plots:* Located in `outputs/plots/`

 *Statsmodels Summaries:* Located in `outputs/tables/`

---
```
##  **How to Run**

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/carbon_emissions_project.git
   cd carbon_emissions_project
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the pipeline**

   ```bash
   python main.py
   ```

   The script will clean, merge, analyze, and save all plots & regression outputs in `outputs/`.

---

## **Datasets**

* [Our World in Data – CO₂ Emissions](https://ourworldindata.org/co2-emissions)
* [World Bank – PM2.5 Air Pollution](https://data.worldbank.org/indicator/EN.ATM.PM25.MC.M3)
* [World Bank – Income Groups](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups)

---

## 👨‍💻 **Author**

Created by **Alex Kamiru** – aspiring data scientist passionate about **global sustainability**, **economics**, and **storytelling with data**.

---
