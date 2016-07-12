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
# add minute each time loop runs
test_df = pd.DataFrame([["09:0" + str(i), "0", "B002", i] for i in range(5)], columns=["time", "date", "room", "count"])


def test_get_average():
    avg_df = predict.get_average(test_df)
    # 0 + 1 + 2 + 3 + 4 = 10
    # 10/5 == 2
    assert avg_df["count"].loc[0] == 2


def test_get_first_time():
    no_duplicates = predict.get_first_time(test_df)
    # only 1 hour in example df, get_first_time should return one value for each hour
    assert len(no_duplicates) == 1


def test_get_average_range():
    avg_df = predict.get_average_range(test_df, 2, 3)
    # only 09:02 and 09:03 should be included
    # count = 2 + 3
    # avg 5/2 = 2.5
    assert avg_df["count"].loc[0] == 2.5

if __name__ == "__main__":
    test_get_average()
    test_get_first_time()
    test_get_average_range()

