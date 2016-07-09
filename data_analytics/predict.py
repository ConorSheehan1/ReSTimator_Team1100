'''
http://stackoverflow.com/questions/30328646/python-pandas-group-by-in-group-by-and-average
http://stackoverflow.com/questions/25473153/python-pandas-iterrows-with-previous-values
http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
'''

import pandas as pd

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

    # get just hour value for logs time
    logs["time"] = logs["time"].apply(lambda x: x.split(":")[0])
    # get average of every row where time and date are the same
    avg = logs.groupby(['time', 'date', 'room'], as_index=False).mean()
    print(avg.loc[avg['time'] == "09"])

    return avg

if __name__ == "__main__":
    df_logs = clean_csvs.importer("./data/CSI WiFiLogs/B-02/")[0]
    get_average(df_logs)