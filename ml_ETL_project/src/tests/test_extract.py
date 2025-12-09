import pandas as pd
from src.etl.extract import extract
from src.utils.validation import validate_row_count


def test_extract_loads_dataframe():
    df = extract()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
