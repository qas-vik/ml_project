from pathlib import Path
from ..utils.logger import get_logger, load_config

logger = get_logger(__name__)

def load(df, path: str = None):
    cfg = load_config()
    path = path or cfg.get("processed_path")
    if not path:
        raise ValueError("Processed path not configured")
    full = (Path(__file__).resolve().parents[3] / path).resolve()
    full.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f"Saving processed data to: {full}")
    df.to_csv(full, index=False)
    logger.info("Saved processed dataset")
