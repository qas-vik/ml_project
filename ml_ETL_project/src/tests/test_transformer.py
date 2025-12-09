import pandas as pd
from src.etl.transform import ImputeMedian

def test_impute_median():
    df = pd.DataFrame({
        "a": [1, None, 3],
        "b": [4, 5, 6]
    })
    imputer = ImputeMedian(cols=["a"])
    imputer.fit(df)
    df2 = imputer.transform(df)

    assert df2["a"].isna().sum() == 0
