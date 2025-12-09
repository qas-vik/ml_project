# ml_project_ETL_wine

ETL pipeline adapted to Wine Quality dataset (winequalityN.csv).

Quickstart:
1. Put your winequalityN.csv into data/raw/
2. Create virtual environment & install dependencies:
   python -m venv .venv
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt

3. Run the pipeline:
   python -m src.etl.pipeline

4. Run tests:
   pytest -q

Output produced: data/processed/wine_processed.csv
