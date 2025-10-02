# Kaggle dataset downloader and SQLite importer

Place your `kaggle.json` (Kaggle API token) in this directory or in `~/.kaggle/kaggle.json`.

Steps:

1. Create and activate a Python virtual environment.

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
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

