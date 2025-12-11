import pandas as pd
from pathlib import Path
from ..utils.logger import get_logger, load_config

logger = get_logger(__name__)

def extract(path: str = None):
    cfg = load_config()
    raw_path = path or cfg.get("raw_path")

    if not raw_path:
        raise ValueError("Raw path not configured in config.yaml")

    # Build absolute path relative to project root
    project_root = Path(__file__).resolve().parents[3]
    full = (project_root / raw_path).resolve()

    logger.info(f"Extracting data from: {full}")

    if not full.exists():
        raise FileNotFoundError(f"Raw data file not found: {full}")

    df = pd.read_csv(full)

    # Parse any date columns (just in case)
    for col in df.columns:
        if "date" in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

    logger.info(f"Extracted {df.shape[0]} rows and {df.shape[1]} columns")
    return df
