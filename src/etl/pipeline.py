from ..etl.extract import extract
from ..etl.transform import ImputeMedian, RemoveOutliersIQR, FeatureEngineering, Pipeline
from ..etl.load import load
from ..utils.logger import get_logger, load_config
from ..utils import validation

logger = get_logger(__name__)


def run_pipeline():
    logger.info("Starting Wine ETL pipeline")

    # -------------------------------------------------
    # 1) Load config
    # -------------------------------------------------
    cfg = load_config()

    required = cfg.get("validation", {}).get("required_columns", [])
    k = cfg.get("pipeline", {}).get("outlier_k", 3.0)

    # -------------------------------------------------
    # 2) Extract
    # -------------------------------------------------
    df = extract()
    logger.info(f"Extracted dataframe shape: {df.shape}")

    # -------------------------------------------------
    # 3) Row count validation
    # -------------------------------------------------
    rc = validation.validate_row_count(df, min_rows=1)
    if not rc["valid"]:
        raise validation.ValidationError(f"Row count too small: {rc['details']}")

    # -------------------------------------------------
    # 4) Required column validation
    # -------------------------------------------------
    rc2 = validation.validate_required_columns(df, required)
    if not rc2["valid"]:
        raise validation.ValidationError(f"Missing required columns: {rc2['missing']}")

    # -------------------------------------------------
    # 5) Numeric range validations (non-blocking)
    # -------------------------------------------------
    numeric_cols = [
        c for c in df.select_dtypes(include=["int64", "float64"]).columns
        if c != "quality"
    ]

    ranges = validation.compute_iqr_ranges(df, numeric_cols, k=k)

    # FIXED: Do NOT stop pipeline for numeric violations
    validation.validate_numeric_ranges(
        df,
        ranges,
        max_allowed_violations=1000  # <-- UPDATED HERE
    )

    # -------------------------------------------------
    # 6) Feature engineering pipeline
    # -------------------------------------------------
    imputer = ImputeMedian(cols=numeric_cols)
    outlier_remover = RemoveOutliersIQR(cols=numeric_cols, k=k)
    fe = FeatureEngineering()

    steps = [imputer, outlier_remover, fe]
    pipe = Pipeline(steps)
    pipe.fit(df)
    df_processed = pipe.transform(df)

    # -------------------------------------------------
    # 7) Load / Save processed dataset
    # -------------------------------------------------
    load(df_processed)
    logger.info("Wine ETL pipeline completed successfully")

    return df_processed


if __name__ == "__main__":
    run_pipeline()
