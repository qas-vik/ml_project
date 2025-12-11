import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error."""
    pass


# ---------------- ROW COUNT VALIDATION ---------------- #

def validate_row_count(df: pd.DataFrame, min_rows: int = 1):
    """
    Validate that DataFrame has at least `min_rows`.
    Returns dict with validation result.
    Raises ValidationError if check fails.
    """

    row_count = len(df)

    if row_count < min_rows:
        msg = f"Row count {row_count} is less than required minimum {min_rows}"
        logger.error(msg)
        raise ValidationError(msg)

    return {"valid": True, "rows": row_count}


# ---------------- NUMERIC RANGE VALIDATION ---------------- #

def validate_numeric_ranges(df: pd.DataFrame, ranges: dict, strict: bool = True, max_allowed_violations: int = 0):
    """
    Validate numeric ranges.
    - strict=True → ANY violation raises an error
    - max_allowed_violations → how many violations allowed before raising

    Returns dict summary if valid.
    Raises ValidationError if too many violations.
    """
    total_violations = 0
    details = {}

    for col, (low, high) in ranges.items():
        if col not in df.columns:
            continue

        below = df[col] < low
        above = df[col] > high

        violations = below.sum() + above.sum()
        total_violations += violations

        if violations > 0:
            details[col] = {
                "below": below.sum(),
                "above": above.sum()
            }

    logger.info(f"Numeric ranges OK: total_violations={total_violations}")

    if strict or total_violations > max_allowed_violations:
        if total_violations > max_allowed_violations:
            msg = f"Numeric range violations exceeded allowed limit: {total_violations} > {max_allowed_violations}"
            logger.warning(msg)
            logger.warning(f"Details: {details}")
            raise ValidationError(msg)

    return {
        "valid": True,
        "total_violations": total_violations,
        "details": details
    }
