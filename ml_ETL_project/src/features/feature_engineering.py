import pandas as pd
from dataclasses import dataclass

@dataclass
class PHBucket:
    def transform(self, df: pd.DataFrame):
        out = df.copy()
        if "pH" in out.columns:
            out["pH_bucket"] = pd.cut(out["pH"], bins=[0,3,3.5,4,10], labels=["very_acidic","acidic","neutral","basic"])
        return out
