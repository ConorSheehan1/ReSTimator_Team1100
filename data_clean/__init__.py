import pandas as pd
import os, zipfile, glob, csv, sqlite3, shutil
import calendar
import sqlite3

def extract_legacy(excelfile, sheet):
	'''extract legacy data'''
	xls = pd.ExcelFile(excelfile)
	df = xls.parse(sheet)
	return df

def convert_month(month_string):
    '''Input: abbreviated month name

    Output: numerical month representation
    '''
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    return abbr_to_num[month_string]

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
    '''Input: path where zip file is

    Extract zips from master zip and extract csv files from zips
    '''
    os.chdir(path)
    for file in glob.glob("*.zip"):
        zipfile.ZipFile(file).extractall()

    for file in glob.glob("*.csv.zip"):
        zipfile.ZipFile(file).extractall()

def delete_csvs():
    '''Input: directory containing csvs

    Delete csv files
    '''
    for file in glob.glob("*.csv"):
        os.remove(file)

def delete_zips():
    '''Input: directory containing zips

    Delete zip files
    '''
    for file in glob.glob("*.zip"):
        os.remove(file)

def leading_zero(date_string):
    '''add leading zero to day of month for date format'''
    if len(date_string) == 7:
        date_string = date_string[:5] + "0" + date_string[-1]
    return date_string

def log_df():
    '''Input: path with csv files

    Output: dataframe of data from csv files
    '''
    df = pd.DataFrame() # create empty dataframe object

    for file in glob.glob("*.csv"): # iterate through csv files
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
    df["date"] = df[["year", "month", "month_day"]].apply(lambda x: "".join(x.dropna().astype(int).astype(str)), axis=1) # join year, month and date into single value to represent time
    df["date"] = df["date"].apply(lambda x: int(leading_zero(x)))

    # delete redundant information
    df["time"] = df["time"].apply(lambda x: x[:-3])
    del df["Key"] 
    del df["Event_Time"]
    del df["GMT"]

    df = df[["room", "date", "time", "associated_client_count", "authenticated_client_count"]] # reorder colummns
    return df

def populate_db(df, table_name, db_path):
	'''Connect to database and append data to table'''
	conn = sqlite3.connect(db_path)
	df.to_sql(name=table_name, flavor="sqlite", con=conn, if_exists="append", index=False)
	conn.close()