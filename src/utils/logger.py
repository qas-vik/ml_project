import logging, sys, yaml
from pathlib import Path

def load_config(path: str = None):
    """
    Load config.yaml reliably from project root.
    Works regardless of nesting level.
    """
    # Start from the directory where logger.py lives
    current = Path(__file__).resolve()

    # Walk upward until we find folder that contains "config/config.yaml"
    while current != current.parent:
        cfg_path = current / "config" / "config.yaml"
        if cfg_path.exists():
            break
        current = current.parent
    else:
        print("CONFIG NOT FOUND IN ANY PARENT DIRECTORY")
        return {}

    if path:
        cfg_path = Path(path)

    print("USING CONFIG:", cfg_path)

    with open(cfg_path, "r") as f:
        return yaml.safe_load(f)


def get_logger(name: str, level: str = None):
    cfg = load_config()

    level = level or cfg.get("logging", {}).get("level", "INFO")

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger
