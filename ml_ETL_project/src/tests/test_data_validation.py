import pandas as pd
import pytest
from src.utils import validation

def test_required_columns_and_row_count():
    df = pd.DataFrame({'quality':[5], 'alcohol':[10]})
    assert validation.validate_required_columns(df, ['quality','alcohol'])
    assert validation.validate_row_count(df, min_rows=1)

def test_numeric_ranges_violation():
    df = pd.DataFrame({'alcohol':[1000]})
    with pytest.raises(validation.ValidationError):
        validation.validate_numeric_ranges(df, {'alcohol': {'lower':0, 'upper':50}})
