import pandas as pd
import pytest
from src.utils import validation
from src.utils.validation import validate_row_count



def test_validate_row_count_ok():
    df = pd.DataFrame({"a": [1,2,3]})
    result = validation.validate_row_count(df, min_rows=1)
    assert result["valid"] is True


def test_validate_row_count_fail():
    df = pd.DataFrame({"a": []})
    with pytest.raises(validation.ValidationError):
        validation.validate_row_count(df, min_rows=1)


def test_numeric_ranges_violation():
    df = pd.DataFrame({"alcohol": [1000]})  # extreme outlier
    ranges = {"alcohol": (0, 50)}           # allowed bounds

    with pytest.raises(validation.ValidationError):
        validation.validate_numeric_ranges(df, ranges, max_allowed_violations=0)
