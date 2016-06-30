'''toy test to check the length of the list in shuffle doesn't change'''
try:
    from data_analytics import shuffle
except ImportError:
    import shuffle


def test_length():
    '''test length'''
    assert len(shuffle.mylist) == 4
