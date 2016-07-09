'''
http://stackoverflow.com/questions/30328646/python-pandas-group-by-in-group-by-and-average
http://stackoverflow.com/questions/25473153/python-pandas-iterrows-with-previous-values
http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
http://stackoverflow.com/questions/14247586/python-pandas-how-to-select-rows-with-one-or-more-nulls-from-a-dataframe-without
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


def get_average(logs):
    # assume
    # reset logs index
    logs.reset_index(drop=True, inplace=True)

    # get just hour value for logs time: drop minutes, add 00 as new minutes value
    logs["time"] = logs["time"].apply(lambda x: x.split(":")[0]+":00")
    # get average of every row where time and date are the same
    avg = logs.groupby(['time', 'date', 'room'], as_index=False).mean()
    # print(avg.loc[avg['time'] == "09:00"])
    return avg


def get_first_time(logs):
    logs["time"] = logs["time"].apply(lambda x: x.split(":")[0]+":00")
    # keep first unique value for date, time and room
    logs.drop_duplicates(subset=["time", "date", "room"], keep="first", inplace=True)
    # print(logs.loc[logs['time'] == "10:00"])
    return logs


def merge_logs_gt(logs, gt):
    # inner merge to keep only common values between logs and ground truth
    result = pd.merge(logs, gt, how="inner", on=["room", "time", "date"])
    # print(result[result.isnull().any(axis=1)])#[["time", "date"]])
    return result


def run_regression(df):
    # occupancy = target feature
    chosen_features = df[["occupancy", "associated_client_count", "authenticated_client_count"]]
    print(chosen_features)
    linm = sm.ols(formula=("occupancy ~(associated_client_count + authenticated_client_count)"),
                  data=chosen_features).fit()
    print(linm.summary())
    return linm


def predict_occupancy(linm, df):
    predictions = linm.predict(df[["associated_client_count", "authenticated_client_count"]])
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
    first_linm = run_regression(first_test)

    avg_test = merge_logs_gt(avg_b002, gt_b002)
    avg_linm = run_regression(avg_test)

    logs_b003 = clean_csvs.importer("./data/CSI WiFiLogs/B-03/")[0]
    first_b003 = get_first_time(logs_b003)
    avg_b003 = get_average(logs_b003)

    gt_b003 = ground_truth.loc[ground_truth["room"] == "B003"]
    first_predict_b003 = predict_occupancy(first_linm, first_b003)
    avg_predict_b003 = predict_occupancy(avg_linm, avg_b003)

    #test accuracy
    print("length\n", len(gt_b002), len(gt_b003))
    # print(accuracy_score(gt_b003["occupancy"], first_predict_b003))
    # print(accuracy_score(gt_b003["occupancy"], avg_predict_b003))
