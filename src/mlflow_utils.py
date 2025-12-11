import mlflow
from pathlib import Path

# Use raw string for Windows path (NO backslash escaping issues)
MLFLOW_TRACKING_DIR = r"D:\ML_Services\ml_ETL_project\mlruns"

# Convert Windows path → MLflow URI
MLFLOW_URI = "file:///" + MLFLOW_TRACKING_DIR.replace("\\", "/")

# Set tracking URI once
mlflow.set_tracking_uri(MLFLOW_URI)


def start_run(run_name: str, experiment: str = "wine_quality"):
    mlflow.set_experiment(experiment)
    return mlflow.start_run(run_name=run_name)


def log_params(params: dict):
    for k, v in params.items():
        mlflow.log_param(k, v)


def log_metrics(metrics: dict):
    for k, v in metrics.items():
        mlflow.log_metric(k, v)


def log_file(filepath: str):
    p = Path(filepath)
    if p.exists():
        mlflow.log_artifact(str(p))


def log_directory(dirpath: str):
    p = Path(dirpath)
    if p.exists():
        mlflow.log_artifacts(str(p))
