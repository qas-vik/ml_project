import mlflow
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.mlflow_utils import MLFLOW_TRACKING_DIR

def compare_experiments(experiments, output_dir="reports"):
    """
    Compares metrics from multiple MLflow experiments and produces:
      1. A combined CSV comparison table
      2. A bar chart comparing metrics across experiments
    """
    # Set fixed MLflow tracking path
    mlflow.set_tracking_uri(f"file:///{MLFLOW_TRACKING_DIR.replace('\\', '/')}")

    client = mlflow.tracking.MlflowClient()
    records = []

    # Collect metrics for each experiment
    for name in experiments:
        exp = client.get_experiment_by_name(name)

        if not exp:
            print(f"[SKIP] Experiment '{name}' not found.")
            continue

        runs = client.search_runs(exp.experiment_id)
        if not runs:
            print(f"[SKIP] No runs found for experiment '{name}'")
            continue

        # Pick the best run (highest R2)
        best_run = max(runs, key=lambda r: r.data.metrics.get("r2", -1))

        records.append({
            "experiment": name,
            "run_id": best_run.info.run_id,
            "r2": best_run.data.metrics.get("r2", None),
            "rmse": best_run.data.metrics.get("rmse", None),
            **best_run.data.params
        })

    # Convert to dataframe
    df = pd.DataFrame(records)

    # Prepare output directory
    out = Path(output_dir)
    out.mkdir(exist_ok=True)

    # Save CSV report
    csv_path = out / "experiment_comparison.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved comparison table → {csv_path}")

    # Generate comparison chart
    if not df.empty:
        plt.figure(figsize=(8, 5))
        df.plot(x="experiment", y=["r2", "rmse"], kind="bar")
        plt.title("Experiment Performance Comparison")
        plt.ylabel("Score")
        plt.xticks(rotation=45)

        chart_path = out / "experiment_comparison.png"
        plt.savefig(chart_path, bbox_inches="tight")
        plt.close()
        print(f"Saved comparison chart → {chart_path}")

    return df


if __name__ == "__main__":
    compare_experiments([
        "wine_quality",
        "rf_tuned",
        "xgboost_exp",
        "baseline"
    ])
