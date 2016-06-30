'''
Notes:
ground_truth[0]

check scalability vs concurrency of db
entities? real life??
'''

try:
    from data_analytics import clean_ground_truth
except ImportError:
    import clean_ground_truth


def test_ground_truth():
    ground_truth = clean_ground_truth.import_ground_truth("../data/CSI Occupancy report.xlsx", False)
    expected_length = 0
    for value in ground_truth[2]:
        expected_length += value

    # length of ground_truth[1](capacity) is number of rooms
    assert len(ground_truth[0]) == expected_length*len(ground_truth[1])

if __name__ == "__main__":
    test_ground_truth()
