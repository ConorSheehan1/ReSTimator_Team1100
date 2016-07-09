import pandas as pd
try:
    from data_analytics import predict
except ImportError:
    import predict


def test_get_average():
    test_df = pd.DataFrame([["09:00", "0", "B002", i] for i in range(5)], columns=["time", "date", "room", "count"])
    avg_df = predict.get_average(test_df)
    # dataframe count is [0, 1, 2, 3, 4], sum = 10, numbers = 5, so average should == 2
    assert avg_df["count"].loc[0] == 2
