'''
Usage:
Pass directory of csvs to importer

Output:
One pandas dataframe containing data from all csvs from all directories passed to importer

Notes:
I chose to drop authenticated client count, because it contains the same info as associated.
This may be changed in future if we expect to find logs where the counts are different

References
http://www.swegler.com/becky/blog/2014/08/06/useful-pandas-snippets/
http://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
http://stackoverflow.com/questions/19726029/python-make-pandas-dataframe-column-headers-all-lowercase

Update: handle dat/time iso 8601??
'''

import pandas as pd
import glob

try:
    from data_analytics.relative_unzipper import fix_windows_path
    from data_analytics.clean_timetable import format_date
except ImportError:
    from relative_unzipper import fix_windows_path
    from clean_timetable import format_date


def count_bad_lines(path):
    count = 0
    with open(path, "r") as f:
        content = f.readlines()
        for line in content:
            # print(line)
            if "Key" in line:
                break
            else:
                count += 1
    return count


def get_date(date):
    '''
    month, date, year, day_name
    '''
    parts = date.split(" ")
    return parts[1] + " " + parts[2] + " " + parts[-1]


def get_time(time):
    time_list = time.split(" ")[3].split(":")[:-1]
    return time_list[0] + ":" + time_list[1]


def get_room(full_location):
    room = full_location.split(" > ")[-1]
    return room.replace("-", "")


def importer(path, do_print=False):
    print(path)
    df_list = []
    count = 0
    for file_path in glob.iglob(path + "*.csv"):
        file_path = fix_windows_path(file_path)

        if do_print:
            print("importing", file_path, count)

        skip = count_bad_lines(file_path)
        df = pd.read_csv(file_path, skiprows=skip, index_col=False)

        df_list.append(df)
        count += 1

    result = pd.concat(df_list)
    # replace spaces with underscores in column names so sql will work
    result.columns = [x.strip().replace(' ', '_') for x in result.columns]

    # create new df for location data
    location = pd.DataFrame(result["Key"].unique(), columns=["Key"])

    # split key into three columns, drop previous column
    location['campus'], location['building'], location['room'] = zip(*location['Key'].apply(lambda x: x.split(' > ')))

    # format room to match data from ground truth
    location["room"] = location["room"].apply(lambda x: x.replace("-", ""))
    location.drop("Key", axis=1, inplace=True)

    result["room"] = result['Key'].apply(get_room)
    result.drop("Key", axis=1, inplace=True)

    # make all columns lowercase
    result.columns = map(str.lower, result.columns)

    # convert event_time to date, and date to int
    dates = result["event_time"].map(get_date)
    result["date"] = dates.map(format_date)

    result["event_time"] = result["event_time"].map(get_time)
    result.rename(columns={result.columns[0]: 'time'}, inplace=True)

    return result, count, location


def concat_log_dfs(list_of_paths, do_print=False):
    prefix = "./data/CSI WiFiLogs/"
    logs_iter = importer(prefix + list_of_paths[0] + "/", do_print)
    df_logs = logs_iter[0]
    df_location = logs_iter[2]
    for path in list_of_paths[1:]:
        logs_iter2 = importer(prefix + path + "/", do_print)
        df_logs = pd.concat([df_logs, logs_iter2[0]])
        df_location = pd.concat([df_location, logs_iter2[2]])

    # if do_print:
    #     print(df_logs, df_location)
    return df_logs, df_location

if __name__ == "__main__":
    my_list = ["B-02", "B-03", "B-04"]
    concat_log_dfs(my_list, True)


