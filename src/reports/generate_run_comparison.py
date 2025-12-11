import mlflow
import pandas as pd
from pathlib import Path
from src.mlflow_utils import MLFLOW_TRACKING_DIR

def generate_report(experiment_name="wine_quality", output="reports/run_comparison.csv"):

    # Use fixed MLflow tracker
    mlflow.set_tracking_uri(f"file:///{MLFLOW_TRACKING_DIR.replace('\\', '/')}")

    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)

    if not experiment:
        raise ValueError(f"Experiment {experiment_name} does not exist.")

    runs = client.search_runs(experiment.experiment_id)

    records = []
    for r in runs:
        data = {
            "run_id": r.info.run_id,
            "status": r.info.status,
            **r.data.params,
            **r.data.metrics,
        }
        records.append(data)

    df = pd.DataFrame(records)
    Path("reports").mkdir(exist_ok=True)
    df.to_csv(output, index=False)

    print(f"Comparison report generated: {output}")


if __name__ == "__main__":
    generate_report()
