'''
http://stackoverflow.com/questions/30328646/python-pandas-group-by-in-group-by-and-average
http://stackoverflow.com/questions/25473153/python-pandas-iterrows-with-previous-values
http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
http://stackoverflow.com/questions/14247586/python-pandas-how-to-select-rows-with-one-or-more-nulls-from-a-dataframe-without
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.copy.html
'''

import pandas as pd
import statsmodels.formula.api as sm
from sklearn.metrics import accuracy_score

try:
    from data_analytics import clean_csvs
    from data_analytics import clean_ground_truth
    from data_analytics import clean_timetable
except ImportError:
    import clean_csvs
    import clean_ground_truth
    import clean_timetable


def get_average(df):
    '''
    get average value of dataframe per hour
    ignore minute values, look at hour, groupby and get mean
    '''
    # copy dataframe so old dataframe is not overwritten!
    df_new = df.copy(deep=True)

    # get just hour value for logs time: drop minutes, add 00 as new minutes value
    df_new["time"] = df_new["time"].apply(lambda x: x.split(":")[0] + ":00")
    # get average of every row where time and date are the same
    avg = df_new.groupby(['time', 'date', 'room'], as_index=False).mean()

    # check that rows are merge on hour
    # print(len(df), len(avg))
    return avg


def get_average_range(df, min, max):
    # find rows whos minute values are within min and max
    data_list = []
    for i, row in df.iterrows():
        if min <= int(row["time"].split(":")[1]) <= max:
            data_list.append(row)

    # add valid rows to new_df, use old df columns
    df_new = pd.DataFrame(data=data_list, columns=df.columns)

    avg = get_average(df_new)
    return avg


def get_first_time(df):
    # copy dataframe so old dataframe is not overwritten!
    df_new = df.copy(deep=True)

    df_new["time"] = df_new["time"].apply(lambda x: x.split(":")[0] + ":00")
    # keep first unique value for date, time and room
    df_new.drop_duplicates(subset=["time", "date", "room"], keep="first", inplace=True)
    # print(logs.loc[logs['time'] == "10:00"])
    return df_new


def merge_logs_gt(logs, gt):
    # inner merge to keep only common values between logs and ground truth
    result = pd.merge(logs, gt, how="inner", on=["room", "time", "date"])
    # print(result[result.isnull().any(axis=1)])#[["time", "date"]])
    return result


def run_regression(df, target, independent):
    chosen_features = df[[target, independent]]
    linm = sm.ols(formula=(target + "~(" + independent + ")"),
                  data=chosen_features).fit()
    print(linm.summary())
    return linm


def predict_occupancy(linm, df, independent):
    predictions = linm.predict(df[independent])
    # # normalise predictions
    for i in range(len(predictions)):
        if predictions.iloc[i] < 0.125:
            predictions.iloc[i] = 0.00
        elif predictions.iloc[i] < 0.275:
            predictions.iloc[i] = 0.25
        elif predictions.iloc[i] < 0.75:
            predictions.iloc[i] = 0.50
        else:
            predictions.iloc[i] = 1.0
    predictions.reset_index(inplace=True, drop=True)
    print(predictions)
    return predictions

if __name__ == "__main__":
    logs_b002 = clean_csvs.importer("./data/CSI WiFiLogs/B-02/")[0]

    avg_b002 = get_average(logs_b002)
    first_b002 = get_first_time(logs_b002)

    ground_truth = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")[0]
    gt_b002 = ground_truth.loc[ground_truth["room"] == "B002"]

    first_test = merge_logs_gt(first_b002, gt_b002)
    avg_test = merge_logs_gt(avg_b002, gt_b002)

    avg_range_test = get_average_range(logs_b002, 15, 45)

    # first_linm_associated = run_regression(first_test, "occupancy", "associated_client_count")
    # first_linm_authenticated = run_regression(first_test, "occupancy", "authenticated_client_count")
    #
    # avg_linm_associated = run_regression(avg_test, "occupancy", "associated_client_count")
    # avg_linm_associated = run_regression(avg_test, "occupancy", "authenticated_client_count")



    # -------------------------------------------------
    # avg_test = merge_logs_gt(avg_b002, gt_b002)
    # avg_linm = run_regression(avg_test)

    # logs_b003 = clean_csvs.importer("./data/CSI WiFiLogs/B-03/")[0]
    # first_b003 = get_first_time(logs_b003)
    # avg_b003 = get_average(logs_b003)
    #
    # gt_b003 = ground_truth.loc[ground_truth["room"] == "B003"]
    # first_predict_b003 = predict_occupancy(first_linm, first_b003)
    # avg_predict_b003 = predict_occupancy(avg_linm, avg_b003)

    #test accuracy
    # print("length\n", len(gt_b002), len(gt_b003))
    # print(accuracy_score(gt_b003["occupancy"], first_predict_b003))
    # print(accuracy_score(gt_b003["occupancy"], avg_predict_b003))
