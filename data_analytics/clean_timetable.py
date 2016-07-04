'''

'''

import pandas as pd
import openpyxl


def fix_merged_cells(file_path, file_name):
    workbook = openpyxl.load_workbook(file_path + file_name)
    for sheet in workbook:
        if sheet.title != "All":
            for cell in sheet.merged_cells:
                if sheet[cell].value is None:
                    letter = cell[0]
                    number = int(cell[1:])
                    # exclude index columns and first row
                    if (letter != 'A' and letter != 'M') and number > 1:
                        previous_cell = letter + str(number-1)
                        if sheet[previous_cell].value is not None:
                            sheet[cell].value = sheet[previous_cell].value
                            # print(cell, previous_cell)
                            # print(sheet[cell].value, sheet[previous_cell].value)
        workbook.save(file_path + "Fixed_" + file_name)


def read_timetable(file_path, sheet, last_column=10):
    df = pd.read_excel(file_path, sheetname=sheet, skiprows=1, skip_footer=3, parse_cols=last_column)
    df.rename(columns={df.columns[0]: "time"}, inplace=True)
    for i in range(1, len(df.columns)):
        if i % 2 == 0:
            df.rename(columns={df.columns[i]: df.columns[i-1] + " No.Students"}, inplace=True)

    print(df)

if __name__ == "__main__":
    fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx")
    read_timetable("./data/Fixed_B0.02 B0.03 B0.04 Timetable.xlsx", "B0.02")