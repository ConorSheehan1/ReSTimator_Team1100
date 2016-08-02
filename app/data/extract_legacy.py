import pandas as pd


def extract(excelfile, sheet):
	''''''
	xls = pd.ExcelFile(excelfile)
	df = xls.parse(sheet)
	return df

if __name__ == "__main__":
	df_gt = extract("./legacy_data/legacy_data.xlsx", "ground_truth")
	print(df_gt)

	df_mod = extract("./legacy_data/legacy_data.xlsx", "modules")
	print(df_mod)

	df_loc = extract("./legacy_data/legacy_data.xlsx", "location")
	print(df_loc)
