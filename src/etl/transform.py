import pandas as pd
from dataclasses import dataclass
from ..utils.logger import get_logger, load_config
from sklearn.preprocessing import MinMaxScaler

logger = get_logger(__name__)

class Transformer:
    def fit(self, df: pd.DataFrame):
        return self
    def transform(self, df: pd.DataFrame):
        raise NotImplementedError


# ------------------------------------------------------------------------------
# IMPUTE MEDIAN
# ------------------------------------------------------------------------------
@dataclass
class ImputeMedian(Transformer):
    cols: list = None
    medians: dict = None

    def fit(self, df: pd.DataFrame):
        self.medians = {}
        for c in self.cols:
            if c in df.columns:
                self.medians[c] = float(df[c].median())
        logger.info(f"Imputer medians: {self.medians}")
        return self

    def transform(self, df: pd.DataFrame):
        out = df.copy()
        for c, m in self.medians.items():
            out[c] = out[c].fillna(m)
        return out


# ------------------------------------------------------------------------------
# REMOVE OUTLIERS
# ------------------------------------------------------------------------------
@dataclass
class RemoveOutliersIQR(Transformer):
    cols: list = None
    k: float = 3.0

    def transform(self, df: pd.DataFrame):
        out = df.copy()
        for c in self.cols:
            if c not in out.columns:
                continue
            q1 = out[c].quantile(0.25)
            q3 = out[c].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - self.k * iqr
            upper = q3 + self.k * iqr
            before = len(out)
            out = out[(out[c] >= lower) & (out[c] <= upper)]
            after = len(out)
            logger.info(f"Outlier removal on {c}: removed {before - after} rows (bounds {lower:.4f}..{upper:.4f})")
        return out


# ------------------------------------------------------------------------------
# FEATURE ENGINEERING + CATEGORICAL ENCODING
# ------------------------------------------------------------------------------
@dataclass
class FeatureEngineering(Transformer):
    def transform(self, df: pd.DataFrame):
        out = df.copy()

        # 1) ACIDITY RATIO
        if "fixed acidity" in out.columns and "volatile acidity" in out.columns:
            out["acidity_ratio"] = out["fixed acidity"] / (out["volatile acidity"] + 1e-6)

        # 2) NORMALIZED ALCOHOL
        if "alcohol" in out.columns:
            scaler = MinMaxScaler()
            out["alcohol_norm"] = scaler.fit_transform(out[["alcohol"]])

        # 3) QUALITY LABEL
        if "quality" in out.columns:
            out["quality_label"] = out["quality"].apply(
                lambda q: "low" if q <= 4 else ("high" if q >= 7 else "medium")
            )

        # 4) CATEGORICAL ENCODING (Fix for 'type' column)
        categorical_cols = out.select_dtypes(include=["object", "category"]).columns.tolist()
        if categorical_cols:
            logger.info(f"Encoding categorical columns: {categorical_cols}")
            out = pd.get_dummies(out, columns=categorical_cols, drop_first=True)

        return out


# ------------------------------------------------------------------------------
# PIPELINE WRAPPER
# ------------------------------------------------------------------------------
class Pipeline:
    def __init__(self, steps: list):
        self.steps = steps

    def fit(self, df: pd.DataFrame):
        for s in self.steps:
            if hasattr(s, "fit"):
                s.fit(df)
        return self

    def transform(self, df: pd.DataFrame):
        out = df
        for s in self.steps:
            out = s.transform(out)
        return out
