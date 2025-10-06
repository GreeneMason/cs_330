# UFC Fight Analysis Documentation

Welcome to the UFC Fight Analysis documentation. This project provides tools for analyzing UFC fighter statistics and predicting fight outcomes using machine learning.

## Documentation Contents

1. [Installation Guide](installation.md)
   - Prerequisites
   - Setup instructions
   - Common issues and solutions

2. [Tutorial](tutorial.md)
   - Basic usage examples
   - Advanced analysis
   - Visualization examples
   - Best practices

3. [API Documentation](api.md)
   - UFCAnalyzer class reference
   - Method descriptions
   - Parameters and return values
   - Example usage

4. [Analysis Guide](analysis.md)
   - Available analyses
   - Interpretation guide
   - Visualization options
   - Working with results

5. [Contributing Guide](contributing.md)
   - Development setup
   - Code style guidelines
   - Testing procedures
   - Documentation guidelines

## Quick Start

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

## Project Structure

```
cs_330/
├── data/                  # Data files and database
├── docs/                 # Documentation
├── notebooks/           # Jupyter notebooks
├── scripts/             # Utility scripts
├── src/                 # Source code
├── tests/              # Unit tests
├── requirements.txt    # Dependencies
└── README.md          # Project overview
```

## Getting Help

If you encounter any issues or have questions:

1. Check the [Installation Guide](installation.md) for setup issues
2. Review the [Tutorial](tutorial.md) for usage examples
3. Consult the [API Documentation](api.md) for detailed reference
4. See the [Contributing Guide](contributing.md) for development questions

## License

This project is licensed under the MIT License. See the LICENSE file for details.