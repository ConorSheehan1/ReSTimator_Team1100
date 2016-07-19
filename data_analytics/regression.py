import statsmodels.formula.api as sm
try:
    from data_analytics import df_fix_data
except ImportError:
    import df_fix_data

def run_regression(df):
    """sfggrtwrtg"""

    lm = sm.ols(formula="occupancy ~ cli_cnt_cap - 1", data=df).fit()
    print(lm.summary())

    # add column for values of prediction of target feature
    df['predicted_occupancy'] = lm.predict(df)
    
    return df

def bin_prediction(df):
    """Sorts predicted occupancy into the bins used in ground truth"""
    
    binned_predicted = []
    
    for i in range(len(df)):
        if df.predicted_occupancy.iloc[i] < 0.125:
            binned_predicted.append(0.00)
        elif df.predicted_occupancy.iloc[i] < 0.375:
            binned_predicted.append(0.25)
        elif df.predicted_occupancy.iloc[i] < 0.625:
            binned_predicted.append(0.50)
        elif df.predicted_occupancy.iloc[i] < 0.875:
            binned_predicted.append(0.75)
        else:
            binned_predicted.append(1.0)

    print(binned_predicted)
    df["binned_predicted"] = binned_predicted
    return df

def score(df):
    """Shows the accuracy score of model"""
    
    # Print number of correctly binned predictions
    binned_correct = 0
    for i in range(len(df)):
        # Count number of correctly binned predictions
        row = df.iloc[i]
        if row["binned_predicted"] == row["occupancy"]:
            binned_correct += 1
    print("Percentage of predictions correctly binned:", (binned_correct / len(df)) * 100)
    
    # Print the Mean Absolute Error of the model on the training set
    mae = abs(df.predicted_occupancy - df.occupancy).mean()
    print("\nMean Absolute Error:", mae)
    
    # Print the Mean Squared Error of the model on the training set
    mse = ((df.predicted_occupancy - df.occupancy)** 2).mean()
    print("\nMean Squared Error:", mse)

if __name__ == "__main__":
    df = df_fix_data.create_df()
    df = df_fix_data.fill_cols(df)
    df = df_fix_data.add_day(df)
    df = df_fix_data.remove_null(df)
    df = df_fix_data.cli_count_divided_by_occ(df)
    df = run_regression(df)
    df = bin_prediction(df)
    score(df)