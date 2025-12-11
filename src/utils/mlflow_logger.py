import mlflow

MLFLOW_DIR = "file:///D:/ML_Services/ml_ETL_project/mlruns"

def configure_mlflow(experiment_name: str):
    mlflow.set_tracking_uri(MLFLOW_DIR)
    mlflow.set_experiment(experiment_name)
