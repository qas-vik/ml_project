import pandas as pd
from src.etl.transform import ImputeMedian, FeatureEngineering

def sample_df():
    return pd.DataFrame({
        'alcohol':[12.5, None, 10.0],
        'fixed acidity':[7.4,8.0,6.9],
        'volatile acidity':[0.7,0.6,0.65],
        'quality':[5,6,5]
    })

def test_impute_median():
    df = sample_df()
    imputer = ImputeMedian(cols=['alcohol'])
    imputer.fit(df)
    out = imputer.transform(df)
    assert out['alcohol'].isnull().sum() == 0

def test_feature_engineering():
    df = sample_df()
    fe = FeatureEngineering()
    out = fe.transform(df)
    assert ('acidity_ratio' in out.columns) or ('alcohol_norm' in out.columns)
