import os, zipfile, glob, csv, sqlite3, shutil
import pandas as pd
import calendar
import datetime

def convert_month(month_string):
    '''Input: abbreviated month name

    Output: numerical month representation
    '''
    # abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    # return abbr_to_num[month_string]
    month = list(calendar.month_abbr).index(month_string)
    if month < 10:
        return "0" + str(month)
    return str(list(calendar.month_abbr).index(month_string))


def count_bad_lines(path):
    '''Input: file path

    Output: number of rows to skip
    '''
    count = 0
    with open(path, "r") as f:
        content = f.readlines()
        for line in content:
            if "Key" in line:
                break
            else:
                count += 1
    return count


def extract_csvs(path):
    '''
    Input: path where zip file is
    Extract zips from master zip and extract csv files from zips
    '''
    absolute_path = os.path.abspath(path)

    # while there are things in the folder other than csvs
    while [file for file in glob.glob(path + "*") if file not in glob.glob(path + "*.csv")]:

        # iterate over every file
        for file in glob.glob(path + "*"):

            # if the file is a zip, extract and then delete it
            if file.endswith(".zip"):
                zipfile.ZipFile(file).extractall(path)
                os.remove(file)

            # if the file is a directory, move files out of it, then delete it
            elif os.path.isdir(file):
                # add / because file is really a directory
                for sub_file in glob.glob(file + "/*"):
                    file_name = os.path.basename(sub_file)
                    shutil.move(sub_file, absolute_path + "/" + file_name)
                os.rmdir(file)

def delete_csvs(path):
    '''Input: directory containing csvs

    Delete csv files
    '''
    for file in glob.glob(path + "*.csv"):
        os.remove(file)

def format(date_string):
    '''Input: date string

    Output: formated date string
    '''
    if len(date_string) == 7:
        date_string = "0" + date_string
    date_string = date_string[4:] + "-" + date_string[2:4] + "-" + date_string[:2]
    return str(date_string)

# include varibale path, default value is empty string
def log_df(path=""):
    '''Input: path with csv files

    Output: dataframe of data from csv files
    '''
    df = pd.DataFrame() # create empty dataframe object

    for file in glob.glob(path + "*.csv"): # iterate through csv files
        skip = count_bad_lines(file) # start of data
        data = pd.read_csv(file, skiprows=skip, index_col=False) # extract data
        data.columns = [c.replace(' ', '_') for c in data.columns]  # Column names: replace spaces with underscores
        df = df.append(data, ignore_index=True) # append data to dataframe

    df["campus"], df["building"], df["room"] = zip(*df["Key"].apply(lambda x: x.split(" > ", 2))) # split out Key column

    # rename column names to match db column names
    df = df.rename(columns = {"Associated_Client_Count":"associated_client_count"})
    df = df.rename(columns = {"Authenticated_Client_Count":"authenticated_client_count"})

    # extract relevant information for db
    df["day"], df["month"], df["month_day"], df["time"], df["GMT"], df["year"] = zip(*df["Event_Time"].apply(lambda x: x.split(" ", 5))) # split out Event_Time column
    df["month"] = df["month"].apply(lambda x: convert_month(x)) # convert month abbreviation into numerical value
    df["date"] = df[["month_day", "month", "year"]].apply(lambda x: "".join(x.dropna().astype(str)), axis=1) # join year, month and date into single value to represent time
    df["date"] = df["date"].apply(lambda x: format(x))

    # delete redundant information
    df["time"] = df["time"].apply(lambda x: x[:-3])
    del df["Key"] 
    del df["Event_Time"]
    del df["GMT"]

    df = df[["room", "date", "time", "associated_client_count", "authenticated_client_count"]] # reorder colummns
    return df

if __name__ == "__main__":
    extract_csvs("./log_data")
    print(log_df())
    delete_csvs()
