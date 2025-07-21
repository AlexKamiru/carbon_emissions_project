#contains regression functions for carbon emissions Project.
import pandas as pd
import numpy as np 
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import os

##Fetch the data
def load_processed_data():
    """load the combined data .csv"""
    df= pd.read_csv("data/processed/combined_data.csv")
    return df


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
   