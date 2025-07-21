#contains regression functions for carbon emissions Project.
import pandas as pd
import numpy as np 
import statsmodels.api as sm
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

#Function for the regression using log transformation.
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

    return model, X_test, y_test, y_pred