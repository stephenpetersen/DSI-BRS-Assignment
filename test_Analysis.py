# test that load_data() pull in a dataframe of correct size (8 lists of 15 books)
import pandas as pd
from pytest import raises
from Analysis import Analysis

analysis = Analysis('configs/analysis_config.yml')

def test_check_data_frame() :
    analysis.load_data()
    # expected values
    rows = 120
    cols = 26
    expected_shape = (rows, cols)

    # test
    assert analysis.df.shape == expected_shape, f'Not correct data frame shape, it should be {rows} rows and {cols} columns'

def test_api_pull_exception_error() :
    # test
    with raises(Exception) :
        analysis.load_data(1) # pause time set to 1 second (too fast for NYT API)

