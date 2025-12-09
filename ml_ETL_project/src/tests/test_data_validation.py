import pandas as pd
import pytest
from src.utils import validation
from src.utils.validation import validate_row_count



def test_numeric_ranges_violation():
    df = pd.DataFrame({"alcohol": [1000]})  # extreme outlier
    ranges = {"alcohol": (0, 50)}

    with pytest.raises(validation.ValidationError):
        validation.validate_numeric_ranges(df, ranges, strict=True)
