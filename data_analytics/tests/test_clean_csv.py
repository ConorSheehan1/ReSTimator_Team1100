'''
Usage
This test must be run in the tests directory!
If not it will fail
I will try to update this in future so running py.test from the outer directory works.

Check context

This test checks that all files in a given directory are imported to a dataframe
It takes quite a long time unfortunately
Hopefully I'll find a way to speed it up in future
'''

import glob
try:
    from data_analytics.clean_csvs import importer
except ImportError:
    from clean_csvs import importer


def get_values(path):
    file_dir_length = 0
    num_files_imported = importer("../data/CSI WiFiLogs/"+path)[1]

    for filename in glob.iglob("../data/CSI WiFiLogs/" + path + "*.csv"):
        file_dir_length += 1
    print(file_dir_length, num_files_imported)
    return file_dir_length, num_files_imported


# might be a better way of doing this (use classes?)
# find way to pass params to tests
def test_b02_import():
    b02 = get_values("B-02/")
    assert b02[0] == b02[1]


def test_b03_import():
    b03 = get_values("B-03/")
    assert b03[0] == b03[1]


def test_b04_import():
    b04 = get_values("B-04/")
    assert b04[0] == b04[1]

if __name__ == "__main__":
    test_b02_import()
    test_b03_import()
    test_b04_import()
