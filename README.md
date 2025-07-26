```markdown
# 🌍 Carbon Emissions & Inequality Analysis  

This project investigates how **CO₂ emissions**, **economic growth (GDP)**, and **air pollution (PM2.5)** vary across income groups.  
It aims to answer key questions:

1. **Who emits the most CO₂ – rich or poor countries?**  
2. **Is economic growth tied to rising emissions?**  
3. **Are low-income countries punished for industrializing?**  
4. **Which factors (GDP, population, PM2.5) are strongest predictors of CO₂ emissions?**

---

##  **Project Structure**

```

carbon\_emissions\_project/
│
├── data/
│   ├── raw/                         # Original datasets
│   │   ├── co2\_emissions.csv
│   │   ├── air\_pollution.csv
│   │   ├── income\_group.csv
│   │   └── temperature\_data.csv
│   └── processed/
│       └── combined\_data.csv        # Cleaned + merged dataset (29k rows, 15 cols)
│
├── outputs/
│   ├── plots/                       # Visual & regression outputs
│   │   ├── co2\_income\_share.png
│   │   ├── co2\_vs\_gdp\_scatter.png
│   │   ├── industrializing\_poor\_countries.png
│   │   ├── pm25\_exposure\_by\_income.png
│   │   ├── gdp\_distribution.png
│   │   ├── q1\_simple\_regression.png
│   │   ├── q1\_multiple\_actual\_vs\_pred.png
│   │   ├── q2\_polynomial.png
│   │   ├── regression\_q3\_actual\_vs\_predicted.png
│   │   ├── regression\_q3\_feature\_importance.png
│   │   ├── regression\_q4\_actual\_vs\_predicted.png
│   │   └── regression\_q4\_feature\_importance.png
│   │
│   ├── tables/                      # CSV + Statsmodels summaries
│   │   ├── regression\_summary\_q1\_simple.csv
│   │   ├── regression\_summary\_q1\_multiple.csv
│   │   ├── regression\_summary\_q2\_polynomial.csv
│   │   ├── regression\_summary\_q3\_income\_group.csv
│   │   ├── regression\_summary\_q4\_standardized.csv
│   │   └── \*.txt (Statsmodels detailed summaries)
│   │
│   └── text\_summaries/
│       └── regression\_summary\_q4\_standardized.txt
│
├── scripts/
│   ├── clean\_data.py
│   ├── load\_data.py
│   ├── merge\_data.py
│   ├── analyze\_data.py              # Exploratory & descriptive stats
│   ├── visualize.py                 # Bar/Scatter/Box plots
│   └── regression\_models.py         # Q1–Q4 regression models
│
├── utils/                           # Helper functions (optional)
├── main.py                          # Main execution pipeline
├── requirements.txt                 # Python dependencies
└── README.md                        # You're here!

````

---

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

##  **How to Run**

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/carbon_emissions_project.git
   cd carbon_emissions_project
````

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
