'''
http://stackoverflow.com/questions/30328646/python-pandas-group-by-in-group-by-and-average
http://stackoverflow.com/questions/25473153/python-pandas-iterrows-with-previous-values
http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
http://stackoverflow.com/questions/14247586/python-pandas-how-to-select-rows-with-one-or-more-nulls-from-a-dataframe-without
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.copy.html
'''

import pandas as pd
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt

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


def get_max(df):
    df_new = df.copy(deep=True)
    df_new["time"] = df_new["time"].apply(lambda x: x.split(":")[0] + ":00")
    df_max = df_new.groupby(['time', 'date', 'room'], as_index=False).max()
    return df_max


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


def get_half_hour(df):
    data_list = []
    for i, row in df.iterrows():
        if row["time"].split(":")[1][0] == "3":
            data_list.append(row)

    df_half_hour = pd.DataFrame(data=data_list, columns=df.columns)
    df_half_hour = get_first_time(df_half_hour)

    # df_half_hour.drop_duplicates(subset=["time", "date", "room"], keep="first", inplace=True)
    # df_half_hour = df_new.groupby(['time', 'date', 'room'], as_index=False).mean()

    # print(df_half_hour["time"])
    return df_half_hour


def merge_logs_gt(logs, gt):
    # inner merge to keep only common values between logs and ground truth
    result = pd.merge(logs, gt, how="inner", on=["room", "time", "date"])
    # print(result[result.isnull().any(axis=1)])#[["time", "date"]])
    return result


def run_regression(df, target, independent):
    chosen_features = df[[target, independent]]
    linm = sm.ols(formula=(target + "~(" + independent + ")"),
                  data=chosen_features).fit()
    # print(linm.summary())
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


def mean_squared_error(df, linm):
    return ((df["occupancy"] - linm.predict(df)) ** 2).mean()


def create_graph(df, linm, feature, name):
    # First, plot the observed data
    df.plot(kind='scatter', x=feature, y='occupancy')

    X_minmax = pd.DataFrame({feature: [df[feature].min(), df[feature].max()]})

    # Next, plot the regression line, in red.
    plt.plot(X_minmax, linm.predict(X_minmax), c='red', linewidth=2)

    plt.savefig("data/plots/formatted/" + name + "_" + feature + '.png', dpi=100)
    # plt.show()

if __name__ == "__main__":
    logs_b002 = clean_csvs.importer("./data/CSI WiFiLogs/B-02/")[0]

    first_b002 = get_first_time(logs_b002)
    avg_b002 = get_average(logs_b002)
    avg_range_b002 = get_average_range(logs_b002, 15, 45)
    max_b002 = get_max(logs_b002)
    half_hour_b002 = get_half_hour(logs_b002)

    logs_b003 = clean_csvs.importer("./data/CSI WiFiLogs/B-03/")[0]

    first_b003 = get_first_time(logs_b003)
    avg_b003 = get_average(logs_b003)
    avg_range_b003 = get_average_range(logs_b003, 15, 45)
    max_b003 = get_max(logs_b003)
    half_hour_b003 = get_half_hour(logs_b003)

    # vars = [first_b002, avg_b002, avg_range_b002, max_b002, half_hour_b002, first_b003]
    # for var in vars:
    #     print(var.shape)

    ground_truth = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")[0]
    gt_b002 = ground_truth.loc[ground_truth["room"] == "B002"]

    first_test = merge_logs_gt(first_b002, gt_b002)
    avg_test = merge_logs_gt(avg_b002, gt_b002)
    avg_range_test = merge_logs_gt(avg_range_b002, gt_b002)
    max_test = merge_logs_gt(max_b002, gt_b002)
    half_hour_test = merge_logs_gt(half_hour_b002, gt_b002)

    gt_b003 = ground_truth.loc[ground_truth["room"] == "B003"]
    first_test_b003 = merge_logs_gt(first_b003, gt_b003)
    avg_test_b003 = merge_logs_gt(avg_b003, gt_b003)
    avg_range_test_b003 = merge_logs_gt(avg_range_b003, gt_b003)
    max_test_b003 = merge_logs_gt(max_b003, gt_b003)
    half_hour_test_b003 = merge_logs_gt(half_hour_b003, gt_b003)

    list_of_features = ["authenticated_client_count", "associated_client_count"]
    for feature in list_of_features:
        print("FIRST TIME", feature)
        first_regression = run_regression(first_test, "occupancy", feature)
        print(mean_squared_error(first_test_b003, first_regression), "\n")
        # create_graph(first_test_b003, first_regression, feature, "first_time")
        create_graph(avg_test_b003, first_regression, feature, "first_time")

        print("AVG", feature)
        avg_regression = run_regression(avg_test, "occupancy",  feature)
        print(mean_squared_error(avg_test_b003, avg_regression), "\n")
        # create_graph(avg_test_b003, avg_regression, feature, "avg")
        create_graph(avg_test_b003, avg_regression, feature, "avg")

        print("AVG RANGE", feature)
        range_regression = run_regression(avg_range_test, "occupancy",  feature)
        print(mean_squared_error(avg_range_test_b003, range_regression), "\n")
        # create_graph(avg_range_test_b003, range_regression, feature, "avg_15-45")
        create_graph(avg_test_b003, range_regression, feature, "avg_15-45")

        print("MAX", feature)
        max_regression = run_regression(max_test, "occupancy",  feature)
        print(mean_squared_error(max_test_b003, max_regression), "\n")
        # create_graph(max_test_b003, max_regression, feature, "max")
        create_graph(avg_test_b003, max_regression, feature, "max")

        print("HALF HOUR", feature)
        half_hour_regression = run_regression(half_hour_test, "occupancy",  feature)
        print(mean_squared_error(half_hour_test_b003, half_hour_regression), "\n")
        create_graph(half_hour_test_b003, half_hour_regression, feature, "half_hour")

        create_graph(avg_test_b003, half_hour_regression, feature, "half_hour")
