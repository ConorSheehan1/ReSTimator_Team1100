import sqlite3
try:
    from data_analytics import df_fix_data, regression
except ImportError:
    import df_fix_data, regression

def populate_results_table(df):
    """Adds predicted results to database"""
    
    # create db connection
    con = sqlite3.connect('./data/ucd_occupancy.db')
    # add day, hourly_time, room, module_code, and results to results table in database
    df[["day", "hourly_time", "room", "module_code", "predicted_occupancy", "binned_predicted"]].to_sql("results", con, if_exists='append', index=False)
    con.close()
    
if __name__ == "__main__":
    df = df_fix_data.create_df()
    df = df_fix_data.fill_cols(df)
    df = df_fix_data.add_day(df)
    df = df_fix_data.remove_null(df)
    df = df_fix_data.cli_count_divided_by_occ(df)
    df = regression.run_regression(df)
    df = regression.bin_prediction(df)
    populate_results_table(df)