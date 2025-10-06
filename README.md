# UFC Fight Analysis

A Python project for analyzing UFC fighter statistics and predicting fight outcomes using machine learning.

## Development Log

### October 6, 2025

#### Initial Setup and Data Collection
- Created Python virtual environment
- Set up Kaggle authentication
- Downloaded UFC dataset from Kaggle (maksbasher/ufc-complete-dataset-all-events-1996-2024)
- Created initial data download and import scripts

#### Database Creation
- Created SQLite database for UFC fighter statistics
- Implemented database creation script
- Successfully imported fighter statistics data

#### Machine Learning Implementation
- Implemented XGBoost-based analysis system
- Created feature importance analysis with:
  - SHAP values for interpretability
  - Cross-validation for robustness
  - Confidence intervals for importance scores
  - Stability analysis across different data splits

#### Project Organization
- Reorganized project structure into proper package format
- Created directory structure:
  ```
  cs_330/
  ├── data/                  # Data files and database
  │   ├── UFC dataset/      # Raw UFC dataset
  │   └── ufc_database.db   # SQLite database
  ├── docs/                 # Documentation
  ├── notebooks/           # Jupyter notebooks
  ├── scripts/             # Utility scripts
  ├── src/                 # Source code
  │   └── ufc_analysis/    # Main package
  ├── tests/              # Unit tests
  ```
- Set up proper Python package structure with setup.py

#### Documentation
- Created comprehensive documentation including:
  - Installation guide
  - API documentation
  - Analysis guide
  - Contributing guidelines
  - Tutorial with examples
  - Main documentation index

## Features

### Data Analysis
- Fighter statistics analysis
- Win probability prediction
- Fighting style classification
- Success factor analysis

### Visualization
- Feature importance plots
- Fighting style distribution
- Success correlation analysis
- Performance metrics visualization

### Machine Learning
- XGBoost-based prediction models
- SHAP value analysis
- Cross-validated feature importance
- Style classification using clustering

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

4. Download and set up the database:
```bash
python scripts/download_dataset.py
python scripts/create_database.py
```

## Usage

Basic example:
```python
from ufc_analysis import UFCAnalyzer

# Initialize analyzer
analyzer = UFCAnalyzer()

# Predict fight outcome
prediction = analyzer.predict_win_probability("Fighter A", "Fighter B")
print(f"Win probability: {prediction['win_probability']:.2%}")

# Analyze success factors
factors = analyzer.analyze_success_factors()
print(factors['interpretation'])
```

## Documentation

Detailed documentation is available in the `docs/` directory:
- [Installation Guide](docs/installation.md)
- [Tutorial](docs/tutorial.md)
- [API Documentation](docs/api.md)
- [Analysis Guide](docs/analysis.md)
- [Contributing Guide](docs/contributing.md)

## Future Plans
- Implement more advanced prediction models
- Add time-series analysis for fighter progression
- Include fight event context in predictions
- Add interactive visualization dashboard
- Implement automated testing suite

## Technologies Used
- Python 3.8+
- XGBoost
- scikit-learn
- pandas
- numpy
- SQLite
- matplotlib/seaborn
- SHAP

## License
MIT License

