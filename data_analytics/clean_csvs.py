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
except ImportError:
    from relative_unzipper import fix_windows_path


def importer(path, do_print=False):
    list_ = []
    count = 0
    for file_path in glob.iglob(path + "*.csv"):
        file_path = fix_windows_path(file_path)

        if do_print:
            print("importing", file_path, count)

        skip = count_bad_lines(file_path)
        df = pd.read_csv(file_path, skiprows=skip, index_col=False)

        list_.append(df)
        count += 1

    result = pd.concat(list_)
    # replace spaces with underscores in column names so sql will work
    result.columns = [x.strip().replace(' ', '_') for x in result.columns]

    # split key into three columns, drop previous column
    result['campus'], result['building'], result['room'] = zip(*result['Key'].apply(lambda x: x.split(' > ')))
    result.drop("Key", axis=1, inplace=True)

    # make all columns lowercase
    result.columns = map(str.lower, result.columns)

    return result, count


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

if __name__ == "__main__":
    b02 = importer("./data/CSI WiFiLogs/B-02/", True)[0]
    b03 = importer("./data/CSI WiFiLogs/B-03/", True)[0]
    b04 = importer("./data/CSI WiFiLogs/B-04/", True)[0]

    all_rooms = pd.concat([b02, b03, b04])

    # reorder columns

    print(all_rooms.head(10))
