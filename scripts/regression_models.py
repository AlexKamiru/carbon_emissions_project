#contains regression functions for carbon emissions Project.
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import os

##Fetch the data
def load_processed_data():
    """load the combined data .csv"""
    df= pd.read_csv("data/processed/combined_data.csv")
    return df

#===============
 #Regression
#===============

#Q1 – Do Rich Countries Have High CO₂ Emissions?

#===SIMPLE LINEAR REGRESSION===
def run_q1_simple_regression(df):
    """
    -simple linear regression: GDP -> co2 emissions.
    -Returns model, x_test, y_test, y_pred for visualization.
    """
    
            #selecting the features and target  
    df= df.dropna(subset=["gdp","co2"]) #drop rows with missing values
    x= df[["gdp"]] #predictor
    y= df["co2"]     #Response/ target
 
            # train-test split(80% train,20% test, shuffle for randomness)
    x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2, random_state=42, shuffle=True)

            #fit model (sklearn)
    model= LinearRegression().fit(x_train,y_train)

            #predict the fitted model
    y_pred=model.predict(x_test)
            #evaluation
    r2= r2_score(y_test,y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\nQ1 - SIMPLE LINEAR REGRESSION: GDP -> C02 Emissions")
    print(f"R^2 Score:{r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Intercept:{model.intercept_:.3f}")
    print(f"Coefficient/slope(GDP):{model.coef_[0]:.6f}")

            #statsmodels for detailed interpretation(p-values,CI)
    X_sm= sm.add_constant(x) #adding an intercept term
    sm_model= sm.OLS(y,X_sm).fit()
    print("\nStatsmodels Summary:\n",sm_model.summary())

            #save results to csv 
    os.makedirs("outputs/tables", exist_ok=True)
    summary= pd.DataFrame({
                "Metric":["R2","RMSE","Intercept","GDP_Coefficient"],
                "Value":[r2,rmse,model.intercept_,model.coef_[0]]
            })
    summary.to_csv("outputs/tables/regression_summary_q1_simple.csv", index=False)
    
    # Statsmodels full text & coefficients table
    with open("outputs/tables/regression_summary_q1_simple_statsmodels.txt", "w") as f:
        f.write(sm_model.summary().as_text())
    
    # === Embedded Visualization ===
    os.makedirs("outputs/plots", exist_ok=True)
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="gdp", y="co2", data=df, alpha=0.5, label="Actual")
    plt.plot(df["gdp"], model.predict(x), color="red", lw=2, label="Fitted Line")
    plt.title("Q1: Simple Linear Regression (GDP → CO₂ Emissions)")
    plt.xlabel("GDP")
    plt.ylabel("CO₂ Emissions")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/plots/q1_simple_regression.png", dpi=300)
    plt.close()
    print("Saved → outputs/plots/q1_simple_regression.png")

    return model, x_test,y_test,y_pred


#===MULTIPLE LINEAR REGRESSION===
def run_q1_multiple_regression(df):
    """
    Multiple Linear Regression (GDP+ Population+ pm2_5->co2 Emissions)
    """
        # Select features & target
    data= df.dropna(subset=["gdp","population","pm2_5","co2"]) #Drop the rows with missing values
    x = data[["gdp", "population", "pm2_5"]] #predictor
    y = data["co2"] #Target

        #Train-Test split(80%train,20%test)
    x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2, random_state=42, shuffle=True)
        
        #fit the model
    model= LinearRegression().fit(x_train,y_train) 
        #predict
    y_pred= model.predict(x_test)   

        #Evaluation
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))    
    
    print("\nQ1: MULTIPLE LINEAR REGRESSION (GDP, Population, pm2_5 → CO₂)")
    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")
    for feature, coef in zip(x.columns, model.coef_):
        print(f"{feature} Coefficient: {coef:.6f}")

        #Statsmodels for detailed interpretation
    X_sm = sm.add_constant(x)
    ols_model = sm.OLS(y, X_sm).fit()
    print("\n--- Statsmodels Summary\n",ols_model.summary())

    #===save results to csv===
    os.makedirs("outputs/tables",exist_ok=True)

    summary= pd.DataFrame({
        "Metric": ["R2", "RMSE", "Intercept"] + [f"{feature}_Coefficient" for feature in x.columns],
        "Value": [r2, rmse, model.intercept_] + list(model.coef_)
    })
    summary.to_csv("outputs/tables/regression_summary_q1_multiple.csv", index=False)   

    #===save statsmodels summary
    with open("outputs/tables/regression_summary_q1_multiple_statsmodels.txt","w") as f:
        f.write(ols_model.summary().as_text())



    # === Embedded Visualization (Actual vs Predicted) ===
    os.makedirs("outputs/plots", exist_ok=True)
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             'r--', lw=2)
    plt.title("Q1: Actual vs Predicted CO₂ (Multiple Regression)")
    plt.xlabel("Actual CO₂")
    plt.ylabel("Predicted CO₂")
    plt.tight_layout()
    plt.savefig("outputs/plots/q1_multiple_actual_vs_pred.png", dpi=300)
    plt.close()
    print("Saved → outputs/plots/q1_multiple_actual_vs_pred.png")

        
    return model, x_test, y_test, y_pred
   



#Q2: IS ECONOMIC GROWTH TIED TO POLLUTION?
  
def check_gdp_distribution(df):
    gdp_data = df["gdp"].dropna()

    print("\n=== GDP Distribution Check ===")
    print(gdp_data.describe())
    skewness = gdp_data.skew()
    print(f"Skewness: {skewness:.2f}")

    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,4))
    plt.hist(gdp_data, bins=50, color='skyblue', edgecolor='black')
    plt.title("GDP Distribution")
    plt.xlabel("GDP")
    plt.ylabel("Frequency")
    plt.savefig("outputs/plots/gdp_distribution.png")
    plt.close()
    print("Saved histogram → outputs/plots/gdp_distribution.png")

    return skewness

#Function for the polynomial regression using log transformation.
def run_q2_polynomial_regression(df):
    """
    Q2: Polynomial Regression (log(GDP) → CO₂ Emissions)
    Checks if economic growth (GDP) has a nonlinear relationship with CO₂ emissions.
    """

    # 1. Data Preparation 
    data = df.dropna(subset=["gdp", "co2"])
    data=data.copy()
    data.loc[:,"log_gdp"] = np.log1p(data["gdp"])  # log(1+gdp)

    X = data[["log_gdp"]]
    y = data["co2"]

    # 2. Polynomial Transformation (degree=2) 
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)  # Creates [log_gdp, log_gdp^2]

    # 3. Train-Test Split 
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X_poly, y, test_size=0.2, random_state=42, shuffle=True
    )

    # 4. Fit the Model 
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 5. Predictions & Evaluation
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print("\nQ2: POLYNOMIAL REGRESSION (log(GDP) → CO₂)")
    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")
    for feature, coef in zip(["log_gdp", "log_gdp^2"], model.coef_):
        print(f"{feature} Coefficient: {coef:.6f}")

    # 6. Statsmodels Summary 
    X_sm = sm.add_constant(X_poly)
    ols_model = sm.OLS(y, X_sm).fit()
    print("\n--- Statsmodels Summary ---\n", ols_model.summary())

    # 7. Save Results 
    os.makedirs("outputs/tables", exist_ok=True)

    # Save metrics & coefficients
    summary = pd.DataFrame({
        "Metric": ["R2", "RMSE", "Intercept", "log_gdp_Coefficient", "log_gdp^2_Coefficient"],
        "Value": [r2, rmse, model.intercept_, model.coef_[0], model.coef_[1]]
    })
    summary.to_csv("outputs/tables/regression_summary_q2_polynomial.csv", index=False)

    # Save statsmodels summary (TXT)
    with open("outputs/tables/regression_summary_q2_polynomial_statsmodels.txt", "w") as f:
        f.write(ols_model.summary().as_text())


    #  Visualization 
    os.makedirs("outputs/plots", exist_ok=True)
    # Scatter + polynomial regression curve
    plt.figure(figsize=(7, 5))
    plt.scatter(X["log_gdp"], y, alpha=0.3, label="Actual", color="skyblue")
    
    # Generate smooth curve for polynomial
    log_gdp_range = np.linspace(X["log_gdp"].min(), X["log_gdp"].max(), 300).reshape(-1, 1)
    log_gdp_poly = poly.transform(log_gdp_range)
    plt.plot(log_gdp_range, model.predict(log_gdp_poly), color="red", linewidth=2, label="Polynomial Fit")

    plt.title("Q2: Polynomial Regression (log(GDP) → CO₂ Emissions)")
    plt.xlabel("log(GDP)")
    plt.ylabel("CO₂ Emissions")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("outputs/plots/regression_q2_polynomial.png")
    plt.close()
    print("Saved plot → outputs/plots/regression_q2_polynomial.png")   

    return model, X_test, y_test, y_pred



#Q3...ARE POOR COUNTRIES PUNISHED FOR INDUSTRIALIZING?

def run_q3_income_group_regression(df):
    """
    its a multiple  regression with one-hot encoding(Income Group+GDP+PM2_5 -> co2)
    """

    #data preparation
    data=df.dropna(subset=["gdp","pm2_5","income_group","co2"]).copy()

    #one-hot encode income_group
    """drop_first=True to avoid dummy variable trap"""
    income_encoded = pd.get_dummies(data["income_group"], drop_first=True)

    #combine encoded categories with numerical predictors(gdp+pm2_5)
    x= pd.concat([data[["gdp","pm2_5"]], income_encoded], axis=1)
    y= data["co2"]

    #Train_test_split 
    x_train, x_test, y_train, y_test= train_test_split(x,y,test_size=0.2, random_state=42,shuffle=True)

    #fit the model
    model= LinearRegression().fit(x_train, y_train)

    #predictions and evaluation
    y_pred= model.predict(x_test)
    r2= r2_score(y_test,y_pred)
    rmse= np.sqrt(mean_squared_error(y_test, y_pred))

    print("\nQ3: MULTIPLE REGRESSION (Income Group + GDP + pm2_5 → CO₂)")
    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")
    for feature, coef in zip(x.columns, model.coef_):
        print(f"{feature} Coefficient: {coef:.6f}")


    #statsmodels for interpretation
    X_sm = sm.add_constant(x)
    X_sm = X_sm.apply(pd.to_numeric, errors='coerce').astype(float)  # convert objects to numeric
    y = pd.to_numeric(y, errors='coerce').astype(float)
    valid_idx = X_sm.notnull().all(axis=1) & y.notnull() # Drop any remaining NaN rows (just in case)
    X_sm = X_sm.loc[valid_idx]
    y = y.loc[valid_idx]

    ols_model = sm.OLS(y.values, X_sm.values).fit()
    print("\n--- Statsmodels Summary ---\n", ols_model.summary())    
    
    #save results
    os.makedirs("outputs/tables", exist_ok=True)

    #save metrics and coefficients
    summary = pd.DataFrame({
        "Metric": ["R2", "RMSE", "Intercept"] + [f"{feature}_Coefficient" for feature in x.columns],
        "Value": [r2, rmse, model.intercept_] + list(model.coef_)
    })
    summary.to_csv("outputs/tables/regression_summary_q3_income_group.csv", index=False)

    # Save Statsmodels Summary (TXT)
    with open("outputs/tables/regression_summary_q3_income_group_statsmodels.txt", "w") as f:
        f.write(ols_model.summary().as_text())

    # === Visualization ===
    os.makedirs("outputs/plots", exist_ok=True)
    # (A) Actual vs Predicted Scatter Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, y_pred, alpha=0.4, color="purple", edgecolors="black")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Prediction")
    plt.xlabel("Actual CO₂ Emissions")
    plt.ylabel("Predicted CO₂ Emissions")
    plt.title("Q3: Actual vs Predicted CO₂ Emissions")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("outputs/plots/regression_q3_actual_vs_predicted.png")
    plt.close()
    print("Saved plot → outputs/plots/regression_q3_actual_vs_predicted.png")
    
     # (B) Coefficient Importance Bar Plot
    coef_df = pd.DataFrame({"Feature": x.columns, "Coefficient": model.coef_})
    coef_df = coef_df.sort_values(by="Coefficient", ascending=False)

    plt.figure(figsize=(7, 4))
    plt.barh(coef_df["Feature"], coef_df["Coefficient"], color="teal")
    plt.xlabel("Coefficient Value")
    plt.title("Q3: Feature Importance (Are Poor Countries Punished?)")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.savefig("outputs/plots/regression_q3_feature_importance.png")
    plt.close()
    print("Saved plot → outputs/plots/regression_q3_feature_importance.png")


    return model, x_test,y_test, y_pred 


#Q4: WHICH FACTOR(gdp,population or pm2.5) is the strongest predictor.

def run_q4_feature_importance_regression(df):
    """
    Q4: Multiple Linear Regression with standardized coefficients
    (GDP, Population, pm2_5 → CO₂ Emissions)
    """
    print("\n=== Q4: Feature Importance (Standardized Multiple Linear Regression) ===")

    # 1. Select relevant columns & drop missing values
    data = df.dropna(subset=["gdp", "population", "pm2_5", "co2"])
    x = data[["gdp", "population", "pm2_5"]]
    y = data["co2"]

    # 2. Standardize features
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    # 3. Train-test split
    x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42, shuffle=True)

    # 4. Fit the model
    model = LinearRegression().fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # 5. Evaluation metrics
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"R² Score: {r2:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"Intercept: {model.intercept_:.3f}")
    for feature, coef in zip(["gdp", "population", "pm2_5"], model.coef_):
        print(f"{feature} (Standardized Coefficient): {coef:.4f}")

    # 6. Statsmodels for detailed interpretation
    X_sm = sm.add_constant(x_scaled)
    ols_model = sm.OLS(y, X_sm).fit()
    print("\n--- Statsmodels Summary ---")
    print(ols_model.summary())

    # 7. Save results to CSV (including standardized coefficients)
    os.makedirs("outputs/tables", exist_ok=True)
    summary = pd.DataFrame({
        "Metric": ["R2", "RMSE", "Intercept"] + [f"{f}_Std_Coefficient" for f in ["gdp", "population", "pm2_5"]],
        "Value": [r2, rmse, model.intercept_] + list(model.coef_)
    })
    summary.to_csv("outputs/tables/regression_summary_q4_standardized.csv", index=False)

    # 8. Save statsmodels summary as text file
    os.makedirs("outputs/text_summaries", exist_ok=True)
    with open("outputs/text_summaries/regression_summary_q4_standardized.txt", "w") as f:
        f.write(ols_model.summary().as_text())
    
    # ===  Visualization ===
    os.makedirs("outputs/plots", exist_ok=True)

    # (A) Actual vs Predicted Scatter Plot
    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, y_pred, alpha=0.5, color="darkgreen", edgecolors="black")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Prediction")
    plt.xlabel("Actual CO₂ Emissions")
    plt.ylabel("Predicted CO₂ Emissions")
    plt.title("Q4: Actual vs Predicted CO₂ Emissions")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig("outputs/plots/regression_q4_actual_vs_predicted.png")
    plt.close()
    print("Saved plot → outputs/plots/regression_q4_actual_vs_predicted.png")

    # (B) Standardized Coefficient Importance
    coef_df = pd.DataFrame({"Feature": ["gdp", "population", "pm2_5"], "Std_Coefficient": model.coef_})
    coef_df = coef_df.sort_values(by="Std_Coefficient", ascending=True)

    plt.figure(figsize=(6, 4))
    plt.barh(coef_df["Feature"], coef_df["Std_Coefficient"], color="orange")
    plt.xlabel("Standardized Coefficient")
    plt.title("Q4: Feature Importance (Standardized)")
    plt.grid(axis="x", linestyle="--", alpha=0.6)
    plt.savefig("outputs/plots/regression_q4_feature_importance.png")
    plt.close()
    print("Saved plot → outputs/plots/regression_q4_feature_importance.png")

    return model, x_test, y_test, y_pred





    



