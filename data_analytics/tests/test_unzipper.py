'''
Usage:
cd to directory in cms and use py.test
This test checks that every zip produces exactly one csv

This can easily be modified to check each zip produces at least one csv (== to <=) to account for future uplaods,
But for now because every zip should produce exactly one csv, we check for that.
'''

import glob
try:
    from data_analytics import relative_unzipper
except ImportError:
    import relative_unzipper


# context: run unzipper before counting files, initialise counters to 0
relative_unzipper.unzipper_outer("../data/")
count_zips, count_csvs = 0, 0


def count_files(counter, path, extension):
    full_path = "../data/CSI WiFilogs/" + path
    print(full_path)
    for filename in glob.iglob(full_path + "*" + extension):
        counter += 1
    return counter

count_zips = count_files(count_zips, "", ".zip")
csv_count_generator = map(count_files, [count_csvs]*3, ["B-02/", "B-03/", "B-04/"], [".csv"]*3)
for value in csv_count_generator:
    count_csvs += value


def test_unzipper():
    assert count_zips == count_csvs

if __name__ == "__main__":
    print(count_zips, "should equal", count_csvs)
