<<<<<<< HEAD
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
=======


This repository hosts reusable scaffolding for machine learning services. It demonstrates a clean Git workflow, a reproducible file layout, and collaboration guardrails (branching, commits, and code reviews).

## Project Layout
- src/: production-ready Python modules
- scripts/: automation helpers (training, evaluation, deployment)
- 
otebooks/: exploratory data analysis and experiments
- docs/: collaboration policies, design notes, and ADRs
- data/, models/, logs/: ignored by Git; local artifacts only

## Getting Started
1. Clone the repository and create a virtual environment (e.g., python -m venv .venv).
2. Install dependencies once a 
equirements.txt is published.
3. Create a feature branch from main that follows the naming rules in docs/CONTRIBUTING.md.
4. Develop, test, and document your work. Keep large artifacts out of Git.
5. Open a pull request and request review from at least one teammate before merging.

See docs/CONTRIBUTING.md for detailed branching, commit, and review expectations.
>>>>>>> c2981f3df888ceba422873168dfb336f9d20fbea
