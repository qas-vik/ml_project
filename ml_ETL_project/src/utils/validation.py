import numpy as np
from .logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation failures."""
    pass


def compute_iqr_ranges(df, cols, k: float = 3.0):
    """
    Compute lower/upper allowed bounds using the IQR rule.
    Returns a dict: {col: {"low": float, "high": float}, ...}
    """
    ranges = {}
    for col in cols:
        s = df[col].dropna()
        if s.empty:
            # return sensible defaults for empty column
            ranges[col] = {"low": float("-inf"), "high": float("inf")}
            continue
        q1 = float(s.quantile(0.25))
        q3 = float(s.quantile(0.75))
        iqr = q3 - q1
        low = q1 - k * iqr
        high = q3 + k * iqr
        ranges[col] = {"low": low, "high": high}
    return ranges


def validate_row_count(df, min_rows: int = 1):
    """
    Validate row count. Returns dict with result and details.
    """
    ok = len(df) >= min_rows
    details = {"rows": len(df), "min_rows": min_rows}
    if ok:
        logger.info(f"Row count validation OK: {details}")
    else:
        logger.warning(f"Row count validation FAILED: {details}")
    return {"valid": ok, "details": details}


def validate_required_columns(df, required_cols):
    """
    Validate required columns exist. Returns {'valid': bool, 'missing': [...]}
    """
    missing = [c for c in required_cols if c not in df.columns]
    ok = len(missing) == 0
    if ok:
        logger.info("Required column validation OK.")
    else:
        logger.warning(f"Missing required columns: {missing}")
    return {"valid": ok, "missing": missing}


def validate_numeric_ranges(df, ranges, max_allowed_violations: int = 50):
    """
    Validate numeric ranges, but do not stop pipeline by default.
    Returns {'valid': bool, 'total_violations': int, 'per_column': {...}}.

    The caller can choose to raise based on returned dict.
    """
    per_col = {}
    total = 0
    for col, bounds in ranges.items():
        low = bounds.get("low", float("-inf"))
        high = bounds.get("high", float("inf"))
        if col not in df.columns:
            per_col[col] = {"below": 0, "above": 0}
            continue
        s = df[col].dropna()
        below = int((s < low).sum())
        above = int((s > high).sum())
        per_col[col] = {"below": below, "above": above}
        total += below + above

    valid = total <= max_allowed_violations
    if valid:
        logger.info(f"Numeric ranges OK: total_violations={total}")
    else:
        logger.warning(
            f"Numeric ranges exceeded allowed limit: total_violations={total} > {max_allowed_violations}"
        )

    return {"valid": valid, "total_violations": total, "per_column": per_col}
