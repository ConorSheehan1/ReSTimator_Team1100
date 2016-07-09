'''
References:
http://stackoverflow.com/questions/19112398/getting-list-of-lists-into-pandas-dataframe
http://stackoverflow.com/questions/4179176/python-incrementing-a-character-string
http://chrisalbon.com/python/pandas_list_unique_values_in_column.html
https://automatetheboringstuff.com/chapter12/
'''

import pandas as pd
import openpyxl


def format_date(unformatted_date):
    # remove leading and trailing white space .strip()
    values = unformatted_date.strip().split(" ")
    # default value for year 2015
    date, year = None, "2015"

    # get first 3 letters of first split in lowercase
    month = values[0][:3].lower()
    if len(values) >= 2:
        date = values[1].strip()
        # add leading zero if leading zero isn't already there
        if int(date) <= 9:
            # cast to int removes leading zeros, add one leading 0: date can never be more than 2 digits
            date = "0" + str(int(date))

    if len(values) >= 3:
        year = values[2]

    month_dict = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
                  "jul": "07", "aug": "08", "sept": "09", "oct": "10", "nov": "11", "dec": "12"}

    try:
        # print(unformatted_date, int(year + month_dict[month] + date))
        return int(year + month_dict[month] + date)
    except TypeError:
        return "Error no month or date passed"


def fix_merged_cells(file_path, file_name, do_print=False):
    '''
    fix practical v lecture?
    '''
    if do_print:
        print("Opening", "{0:>60}".format((file_path + file_name)))
    workbook = openpyxl.load_workbook(file_path + file_name)
    # remove irrelevant sheet
    workbook.remove_sheet(workbook["All"])
    for sheet in workbook:
        # unmerge cells
        if do_print:
            print("unmerging: ", end="")
        for cell in sheet.merged_cells:
            letter = sheet[cell].column
            number = sheet[cell].row
            if sheet[cell].value is None:
                # exclude index columns and first row
                if (letter != 'A' and letter != 'M') and number > 1:
                    previous_cell = letter + str(number-1)
                    if sheet[previous_cell].value is not None:
                        if do_print:
                            print(letter + str(number) + ", ", end="")
                        sheet[cell].value = sheet[previous_cell].value
        print()
        # fix dates
        for row in sheet['N2':'W2']:
            for cell in row:
                # skip no.reg students
                if cell.value is not None and "." not in cell.value:
                    date_number = int(cell.value.split(" ")[1][0])
                    # update to check date above?
                    cell.value = cell.value.split(" ")[0] + " " + str(date_number+7) + "th"
                    if do_print:
                        print("date fixed", cell.value)

    # save fixed xlsx to new file
    fixed_path = file_path + "Fixed_" + file_name

    if do_print:
        print("Saving unmerged version to {0:>47}".format(fixed_path))
    workbook.save(fixed_path)

    list_of_sheets = [sheet.title for sheet in workbook]

    # create one large dataframe
    df_total_module = read_timetable(fixed_path, list_of_sheets[0])
    for sheet in list_of_sheets[1:]:
        df_total_module = pd.concat([df_total_module, read_timetable(fixed_path, sheet),
                                     read_timetable(fixed_path, sheet, 13)])

    # drop nans to be able to convert floats to int
    df_total_module.dropna(inplace=True)
    df_total_module["reg_students"] = df_total_module["reg_students"].astype(int)

    # match room code format with ground truth
    df_total_module["room"] = df_total_module["room"].apply(lambda x: x.replace(".", ""))

    return df_total_module


def read_timetable(file_path, sheet, last_column=0):
    '''
    change list_of_modules to set? solved with drop_duplicates? runtime?
    currently only checking first week in sheet (last_column=10) check for difference in next week?
    '''

    list_of_modules = []
    df = pd.read_excel(file_path, sheetname=sheet, skiprows=1, skip_footer=3, parse_cols=last_column+10)
    header = pd.read_excel(file_path, sheetname=sheet, skip_footer=len(df)+4, parse_cols=2)
    month = header.columns[1].split(" ")[1]

    for tuple in df.itertuples():
        for i in range(len(tuple)):
            if i % 2 == 0:
                if type(tuple[i]) == str:
                    # choose start of class as time, strip twice to account for 2 digit numbers
                    list_of_modules.append([tuple[1].split(" - ")[0], #df.columns[i-1].strip()[:3],
                                            format_date(month + " " + df.columns[i-1].strip()[-4:-2].strip()),
                                            sheet.strip(), tuple[i], tuple[i+1]])

    # df_module = pd.DataFrame(list_of_modules, columns=["time", "day", "date", "room", "module_code", "reg_students"])
    df_module = pd.DataFrame(list_of_modules, columns=["time", "date", "room", "module_code", "reg_students"])
    return df_module


if __name__ == "__main__":
    # print(format_date("Jan 2"))
    fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx", True)

