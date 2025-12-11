import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error."""
    pass


# ---------------------------------------------------
# ROW COUNT VALIDATION
# ---------------------------------------------------

def validate_row_count(df: pd.DataFrame, min_rows: int = 1):
    """
    Validate that DataFrame has at least `min_rows`.
    Raises ValidationError if check fails.
    Returns {"valid": True, "rows": row_count}
    """
    row_count = len(df)

    if row_count < min_rows:
        msg = f"Row count {row_count} is less than required minimum {min_rows}"
        logger.error(msg)
        raise ValidationError(msg)

    return {"valid": True, "rows": row_count}


# ---------------------------------------------------
# REQUIRED COLUMNS VALIDATION
# ---------------------------------------------------

def validate_required_columns(df: pd.DataFrame, required_cols: list):
    """
    Check that all required columns are present.
    Returns {"valid": True} or {"valid": False, "missing": [...]}
    """
    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        logger.error(f"Missing required columns: {missing}")
        return {"valid": False, "missing": missing}

    return {"valid": True, "missing": []}


# ---------------------------------------------------
# COMPUTE IQR NUMERIC RANGES
# ---------------------------------------------------

def compute_iqr_ranges(df: pd.DataFrame, cols: list, k: float = 1.5):
    """
    Compute IQR-based numeric limits.
    Returns dict {col: (low, high)}
    """
    ranges = {}

    for col in cols:
        if col not in df.columns:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        low = q1 - k * iqr
        high = q3 + k * iqr

        ranges[col] = (low, high)

    return ranges


# ---------------------------------------------------
# NUMERIC RANGE VALIDATION
# ---------------------------------------------------

def validate_numeric_ranges(
    df: pd.DataFrame,
    ranges: dict,
    max_allowed_violations: int = 0
):
    """
    Validate numeric ranges.
    Raises ValidationError only if violations > max_allowed_violations.
    Returns {"valid": True, "total_violations": n, "details": {...}}
    """

    total_violations = 0
    details = {}

    for col, (low, high) in ranges.items():
        if col not in df.columns:
            continue

        below = (df[col] < low).sum()
        above = (df[col] > high).sum()

        violations = below + above
        total_violations += violations

        if violations > 0:
            details[col] = {"below": below, "above": above}

    logger.info(f"Numeric violations: {total_violations}")

    if total_violations > max_allowed_violations:
        msg = (
            f"Numeric violations exceeded limit: "
            f"{total_violations} > {max_allowed_violations}"
        )
        logger.error(msg)
        logger.error(details)
        raise ValidationError(msg)

    return {
        "valid": True,
        "total_violations": total_violations,
        "details": details
    }
