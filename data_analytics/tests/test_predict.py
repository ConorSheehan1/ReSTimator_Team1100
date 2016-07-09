import pandas as pd
try:
    from data_analytics import predict
except ImportError:
    import predict

'''
dataframe count is [0, 1, 2, 3, 4], sum = 10, numbers = 5, so average should == 2
unique values should be the same length as drop duplicates if room date and time are the same
(which they are)
'''
test_df = pd.DataFrame([["09:00", "0", "B002", i] for i in range(5)], columns=["time", "date", "room", "count"])


def test_get_average():
    avg_df = predict.get_average(test_df)
    assert avg_df["count"].loc[0] == 2


def test_get_first_time():
    no_duplicates = predict.get_first_time(test_df)
    unique = test_df["time"].unique()
    assert len(no_duplicates) == len(unique)

if __name__ == "__main__":
    test_get_average()
    test_get_first_time()

