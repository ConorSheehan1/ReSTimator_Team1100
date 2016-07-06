'''
References:
http://stackoverflow.com/questions/19112398/getting-list-of-lists-into-pandas-dataframe
http://stackoverflow.com/questions/4179176/python-incrementing-a-character-string
http://chrisalbon.com/python/pandas_list_unique_values_in_column.html
'''

import pandas as pd
import openpyxl


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
        for cell in sheet.merged_cells:
            if sheet[cell].value is None:
                letter = cell[0]
                number = int(cell[1:])
                # exclude index columns and first row
                if (letter != 'A' and letter != 'M') and number > 1:
                    previous_cell = letter + str(number-1)
                    if sheet[previous_cell].value is not None:
                        sheet[cell].value = sheet[previous_cell].value

    # save fixed xlsx to new file
    fixed_path = file_path + "Fixed_" + file_name

    if do_print:
        print("Saving unmerged version to {0:>47}".format(fixed_path))
    workbook.save(fixed_path)

    list_of_sheets = [sheet.title for sheet in workbook]

    # create one large dataframe
    df_total_module = read_timetable(fixed_path, list_of_sheets[0])
    for sheet in list_of_sheets[1:]:
        df_total_module = pd.concat([df_total_module, read_timetable(fixed_path, sheet)])

    # drop duplicates and nans
    df_total_module.drop_duplicates(inplace=True)
    df_total_module.dropna(inplace=True)

    # convert floats to int
    df_total_module["reg_students"] = df_total_module["reg_students"].astype(int)

    # print(df_total_module)
    return df_total_module


def read_timetable(file_path, sheet, last_column=10):
    '''
    change list_of_modules to set? solved with drop_duplicates? runtime?
    currently only checking first week in sheet (last_column=10) check for difference in next week?
    '''

    list_of_modules = []
    df = pd.read_excel(file_path, sheetname=sheet, skiprows=1, skip_footer=3, parse_cols=last_column)

    for tuple in df.itertuples():
        for i in range(len(tuple)):
            if i % 2 == 0:
                if type(tuple[i]) == str:
                    # print(tuple[i], tuple[i+1])
                    list_of_modules.append([tuple[i], tuple[i+1]])

    df_module = pd.DataFrame(list_of_modules, columns=["module_code", "reg_students"])

    return df_module

if __name__ == "__main__":
    fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx", True)
