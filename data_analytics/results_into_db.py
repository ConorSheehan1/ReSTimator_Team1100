import sqlite3
try:
    from data_analytics import df_fix_data, regression
except ImportError:
    import df_fix_data, regression

def populate_results_table(df):
    """Adds predicted results to database"""
    
    # create db connection
    con = sqlite3.connect('../app/project/sample.db')
    # add day, hourly_time, room, module_code, and results to results table in database
    # df[["day", "hourly_time", "room", "module_code", "predicted_occupancy", "binned_predicted"]].to_sql("results", con, if_exists='append', index=False)
    df.to_sql("results", con, if_exists='append', index=False)
    con.close()
    
if __name__ == "__main__":
    df = df_fix_data.create_df()
    df = df_fix_data.fill_cols(df)
    df = df_fix_data.add_day(df)
    df = df_fix_data.remove_null(df)
    df = df[df["time"].str.contains(":[1-5]", regex=True)]
    # df = df.groupby(["room", "day", "hourly_time", "date"], as_index=False).mean()
    df = df.groupby(["room","module_code", "day", "date", "hourly_time"], as_index=False).mean()
    df = df_fix_data.cli_count_divided_by_occ(df)
    df = regression.run_regression(df)
    df = regression.bin_prediction(df)
    df = df.groupby(["room", "day", "hourly_time"], as_index=False).mean()
    # print(df)
    populate_results_table(df)