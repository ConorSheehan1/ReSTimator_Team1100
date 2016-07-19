import sqlite3
import pandas as pd
from datetime import date
#import numpy as np
#import statsmodels.formula.api as sm
#from sklearn.metrics import accuracy_score



# create ADT dataframe from database
def create_df():
    """Creates an ADT dataframe with all information from tables in database"""
    
    # create db connection
    con = sqlite3.connect('./data/ucd_occupancy.db')
    df = pd.read_sql_query("SELECT L.room, L.capacity, L.campus, L.building, O.module_code, M.reg_students, O.time,\
    O.date, O.occupancy, O.associated_client_count, O.authenticated_client_count \
    FROM occupy O \
    LEFT JOIN location L \
    ON L.room = O.room \
    LEFT JOIN module M \
    ON O.module_code = M.module_code \
    ", con)
    
    con.close()
    return df

def fill_cols(df):
    """
    Adds occupancy ground truth data to every entry in an hour that has ground truth.
    Adds module code and registered students to every entry that has a module.
    """
    
    # create db connection
    con = sqlite3.connect('./data/ucd_occupancy.db')
    
    #copy df so it isn't overwritten
    df_new = df.copy(deep=True)
    
    # get just hour value for logs time: drop minutes, add 00 as new minutes value
    if 'hourly_time' not in df.columns:
        df_new["hourly_time"] = df_new["time"].apply(lambda x: x.split(":")[0] + ":00")
    
    occ = pd.read_sql_query("\
    SELECT occupancy AS occ, time AS hourly_time, date, room \
    FROM occupy \
    WHERE occupancy IS NOT NULL", con)
    #print(len(occ))

    df_new = df_new.merge(occ, how='left', on=["hourly_time", "date", "room"])
    df_new['occupancy'] = df_new['occ']
    df_new.drop('occ', axis=1, inplace=True)
    #print(len(df_new.occupancy))

    modules = pd.read_sql_query("\
    SELECT module_code AS module, time AS hourly_time, date, room \
    FROM occupy \
    WHERE module_code IS NOT NULL", con)
    #print(len(modules))

    df_new = df_new.merge(modules, how='left', on=["hourly_time", "date", "room"])
    df_new['module_code'] = df_new['module']
    df_new.drop('module', axis=1, inplace=True)
    #print(len(df_new.module_code))

    students = pd.read_sql_query("\
    SELECT module_code, reg_students AS students \
    FROM module", con)
    #print(len(students))

    df_new = df_new.merge(students, how='left', on="module_code")
    df_new['reg_students'] = df_new['students']
    df_new.drop('students', axis=1, inplace=True)
    #print(len(df_new.reg_students))
    
    con.close()
    return df_new

def add_day(df):
    """Adds Day column to df.
    
    Uses the int date column to find the weekday it refers to."""
    
    # copy df so it isn't overwritten
    df_new = df.copy(deep=True)
    
    # get day from date, add to df
    if 'day' not in df_new.columns:
        days = []
        for i in range(len(df_new)):
            days.append(get_day(df_new.date.iloc[i]))
        df_new["day"] = days
    else:
        for i in range(len(df_new)):
            if pd.isnull(df_new.day.iloc[i]):
                df_new["day"].iloc[i] = get_day(df_new.date.iloc[i])
    return df_new
                
def get_day(date_int):
    """Takes date int in format yyyymmdd and returns weekday string.
    
    Uses datetime.date"""
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    year = date_int // 10000
    month = (date_int % 10000) // 100
    day = date_int % 100
    
    # return index of weekdays list, which is the correct weekday. Uses datetime.date
    try:
        return weekdays[date(year, month, day).weekday()]
    except ValueError:
        return "Incorrect number of days/months"
    
def remove_null(df):
    """Removes rows with null values in occupancy and client count"""
    
    #copy df so it isn't overwritten
    df_new = df.copy(deep=True)

    
    df_new = df_new[pd.notnull(df_new.occupancy)]
    df_new = df_new[pd.notnull(df_new.associated_client_count)]
    df_new = df_new[pd.notnull(df_new.authenticated_client_count)]
    
    return df_new

def cli_count_divided_by_occ(df):
    """Adds column for client count divided by occupancy"""
    
    # client count divided by capacity to account for room difference
    df['cli_cnt_cap'] = df.associated_client_count.div(df.capacity)
    
    return df