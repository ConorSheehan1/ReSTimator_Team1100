'''
Decisions:
I have chosen to drop the rows which show the capacity of the room. We only need this information once,
not in every record, so I have extracted it and then removed the duplicate info for each dataframe.

References:
http://stackoverflow.com/questions/20025882/append-string-to-the-start-of-each-value-in-a-said-column-of-a-pandas-dataframe
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.ExcelFile.parse.html
'''
import pandas as pd


def find_lines(file_path):
    start_rows = []
    df = pd.read_excel(file_path, 'CSI')
    for i, row in df.iterrows():
        if "OCCUPANCY" in str(row[0]):
            start_rows.append(i)
    return start_rows


def get_room_capacity(excel_file, start, stop):
    '''
    try to update to use names rather than indexes!
    parse_cols="Room No.,B004,B002,B003", index_col=None)
    check wifi logs for room names and if they exist parse them from ground truth, otherwise disregard
    '''
    stop -= (start+10)
    capacity = excel_file.parse(sheetname='CSI', skiprows=start, skip_footer=stop+9, parse_cols=[2, 4, 5])
    return capacity


def get_date(excel_file, start, stop):
    '''
    try to update to return date/time in exact same format as WiFi logs
    '''
    header = excel_file.parse(sheetname='CSI', skiprows=start-3, skip_footer=stop+11)
    day = header["Unnamed: 0"][0][:3]
    date = header["Unnamed: 0"][1]
    date_time = day + " " + date + " "
    return date_time


def format_df(df):
    '''
    convert room columns to rows
    '''
    new_df = pd.DataFrame(columns=["Time", "Occupancy", "Room"])

    # loop through rows in df, convert room columns to rows
    count = 0
    for i, row in df.iterrows():
        for column in df.columns[1:]:
            new_df.loc[count] = [row["Time"], row[column], column]
            count += 1

    return new_df


def import_ground_truth(file_path, do_print=False):
    list_of_df_lengths = []
    valid_lines = find_lines(file_path)
    xl_occupancy = pd.ExcelFile(file_path)
    capacity = get_room_capacity(xl_occupancy, valid_lines[0]+5, len(pd.read_excel(file_path, sheetname='CSI')))

    def clean(index):
        start = valid_lines[index]+5
        stop = len(pd.read_excel(file_path, sheetname='CSI'))-(start + 10)

        date = get_date(xl_occupancy, start, stop)
        if do_print:
            print("importing ground_truth for {0:2}".format(date))

        # update parse_cols to use column name rather than index?
        ground_truth = xl_occupancy.parse(sheetname='CSI', skiprows=start, skip_footer=stop, parse_cols=[0, 2, 4, 5])
        ground_truth.drop(ground_truth.index[[0, 1]], inplace=True)
        ground_truth.rename(columns={ground_truth.columns[0]: 'Time'}, inplace=True)
        ground_truth["Time"] = date + ground_truth["Time"].astype(str)

        # count length of each dataframe to see that all lines are added to larger df
        list_of_df_lengths.append(len(ground_truth))
        return ground_truth

    # clean first chunk of data, then concat each subsequent chunk to first chunk
    total_ground_truth = clean(0)
    for i in range(1, len(valid_lines)):
        total_ground_truth = pd.concat([total_ground_truth, clean(i)])

    total_ground_truth = format_df(total_ground_truth)

    # convert rows to columns
    capacity = capacity.T
    capacity.reset_index(inplace=True)
    capacity.rename(columns={capacity.columns[0]: "Room", capacity.columns[1]: "Capacity"}, inplace=True)

    if do_print:
        print(total_ground_truth, capacity)

    return total_ground_truth, capacity, list_of_df_lengths


if __name__ == "__main__":
    import_ground_truth("./data/CSI Occupancy report.xlsx", True)
