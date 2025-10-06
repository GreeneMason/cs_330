# UFC Fight Analysis

A Python project for analyzing UFC fighter statistics and predicting fight outcomes using machine learning.

## Project Structure

```
cs_330/
├── data/                  # Data files and database
│   ├── UFC dataset/      # Raw UFC dataset
│   └── ufc_database.db   # SQLite database
├── docs/                 # Documentation
├── notebooks/           # Jupyter notebooks for analysis
├── scripts/             # Utility scripts
│   ├── check_columns.py
│   ├── create_database.py
│   ├── download_dataset.py
│   └── download_and_import.py
├── src/                 # Source code
│   └── ufc_analysis/    # Main package
│       ├── __init__.py
│       └── analyzer.py
├── tests/              # Unit tests
├── requirements.txt    # Project dependencies
├── README.md          # This file
└── .gitignore        # Git ignore file
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Kaggle authentication:
   - Place your `kaggle.json` (Kaggle API token) in the `.kaggle` directory
   - Get your API token from https://www.kaggle.com/settings
pip install -r requirements.txt
```

2. Download a dataset and import CSVs into SQLite. Replace the slug with the dataset you want.

```powershell
python download_and_import.py owner/dataset
```

The script will download files into `./data/` and create `data/dataset.db` containing a table for each CSV.

Security note: `kaggle.json` is sensitive. This repo's `.gitignore` excludes it by default. Remove `kaggle.json` from git history if you already committed it.
# CS 330 - Machine Learning Project: UFC Fight Prediction

## Project Overview
This repository contains my machine learning project for CS 330. The project focuses on analyzing UFC (Ultimate Fighting Championship) data to create predictive models for fight outcomes.

## Project Goals
- Develop machine learning models to predict UFC fight outcomes
- Analyze fighter statistics and historical data
- Apply various machine learning techniques learned in CS 330
- Create meaningful insights from UFC fight data

## Technologies
- Python
- Machine Learning Libraries (to be determined)
- Data Analysis Tools
- UFC Dataset (Kaggle)

## Structure
First thoughts;
- Use SportsBERT from Google
- Take the summary from SportsBERT and feed it with fighter stats to XGBoost or LightGBM
- Engineer features to account for winstreaks, fight camp lenght, fight camp location

