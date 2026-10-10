# CyberSentinel AI

**An educational AI/ML cybersecurity project for network-flow threat analysis.**

CyberSentinel AI is a Python and Streamlit application that analyses network-flow CSV data, classifies records as benign or potentially malicious, flags unusual records, and helps prioritise investigation through an explainable risk dashboard.

> **Scope and safety:** This is a student research/demo project. It analyses CSV files supplied by the user; it does not capture packets, monitor live networks, or replace professional security tools. Predictions and anomaly flags are not proof of compromise.

## Features

- Binary benign/attack classification and multiclass attack-category prediction.
- Random Forest classifier with a Logistic Regression baseline.
- Isolation Forest anomaly flagging.
- Configurable 0–100 risk prioritisation score.
- Interactive Streamlit dashboard, filters, charts, record details, and CSV export.
- Model evaluation on a held-out split and synthetic demo data for testing the workflow.

## Technology stack

Python · Streamlit · pandas · NumPy · scikit-learn · Plotly · joblib · pytest

## Project structure

```text
CyberSentinel-AI/
├── app.py
├── config.py
├── requirements.txt
├── pytest.ini
├── RUN_ON_WINDOWS.txt
├── .env.example
├── .streamlit/config.toml
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   ├── anomaly_detection.py
│   ├── risk_assessment.py
│   ├── explainability.py
│   ├── evaluation.py
│   └── demo_data.py
├── tests/test_core.py
├── docs/
│   ├── dataset_guide.md
│   ├── limitations.md
│   └── project_architecture.md
├── data/    # local datasets excluded from Git
└── models/  # trained model artifacts excluded from Git
```

## Quick start (Windows / VS Code)

Use Python 3.11 and run these commands from the project folder in the VS Code terminal:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.train_model --demo --mode both
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually http://localhost:8501. To run tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

If the Python launcher is unavailable, install Python 3.11 and ensure it is available in PATH. See [RUN_ON_WINDOWS.txt](RUN_ON_WINDOWS.txt) for the expanded guide.

## Real network-flow data

The pipeline is intended for CIC-IDS2017-style flow CSVs. Read [docs/dataset_guide.md](docs/dataset_guide.md) before using a dataset. Ensure the input contains the features expected by the trained model and follow the dataset's terms and attribution requirements.

Example training command after placing suitable CSVs under `data/cicids2017`:

```powershell
.\.venv\Scripts\python.exe -m src.train_model --data data\cicids2017 --mode both --sample-size 300000
```

## How it works

1. Validate and load flow records.
2. Clean and prepare feature columns.
3. Split labelled data and train classification models.
4. Evaluate the models on a held-out split.
5. Optionally flag unusual records with Isolation Forest.
6. Display predictions, risk prioritisation, and downloadable results in Streamlit.

## Evaluation caveat

Synthetic demo data is only intended to validate the end-to-end workflow. Very high metrics on synthetic data do **not** establish real-world cybersecurity performance. Test with appropriately licensed, representative data and report the dataset, split strategy, class balance, precision, recall, F1-score, and false-positive rate. Risk scores are prioritisation aids, not calibrated probabilities of compromise.

## Security and responsible use

- Do not commit credentials, `.env` files, private traffic captures, or sensitive datasets.
- Generated model files are excluded from version control.
- Only load trusted model artifacts.
- Use the project only on data you are authorised to analyse.

## Roadmap

- Add screenshots from a locally running dashboard.
- Add reproducible benchmark results on a clearly documented public dataset.
- Expand unit and integration test coverage.
- Consider model-drift checks and improved calibration.

## License

MIT. See [LICENSE](LICENSE).

## Author

**Tejashvi Sindhu** · [GitHub](https://github.com/Tejashvi-Sindhu)
