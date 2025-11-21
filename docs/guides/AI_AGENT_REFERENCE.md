# 🤖 AI Agent Reference Guide

**Quick orientation guide for AI agents working with the UFC Prediction System**

## 🚀 Immediate Context

### What's Working Right Now
- ✅ **Neural Network**: 89.50% accuracy achieved with fighter-aware architecture
- ✅ **Environment**: Python 3.11 + TensorFlow 2.20.0 + Keras Tuner 1.4.8
- ✅ **Data Pipeline**: 7,439 fights with 90 numeric features ready
- ✅ **Model Saving**: All models saved with proper metadata

### Current Repository State
```
REORGANIZED STRUCTURE (November 12, 2025):
├── training/    # All model training scripts (moved from root)
├── prediction/  # All prediction scripts (moved from root) 
├── analysis/    # Analysis tools (moved from root)
├── scripts/     # Utility scripts (enhanced)
├── data/        # Datasets (unchanged)
├── models/      # Saved models (organized by type)
└── docs/        # Documentation (comprehensive)
```

## 📋 Key Files for AI Agents

### 1. Status & Progress Documents
- **`NEURAL_NETWORK_PROGRESS_REPORT.md`** - Complete implementation status, results, next steps
- **`NEURAL_NETWORK_TRAINING_GUIDE.md`** - Step-by-step implementation methodology
- **`README.md`** - Main entry point with quick commands

### 2. Working Code (Ready to Execute)
- **`training/train_neural_network_hypertuned.py`** - Best performing model (89.50%)
- **`prediction/predict_neural_network.py`** - Neural network prediction interface
- **`training/train_event_normalized_model.py`** - Ensemble baseline (~85%)

### 3. Data & Models
- **`data/event_normalized_large_dataset.csv`** - Main training dataset
- **`models/neural_network/`** - Saved neural network models and metadata
- **`models/`** - Other model types for comparison

## 🎯 Common AI Agent Tasks

### Task 1: Model Comparison
```bash
# Goal: Compare neural network vs ensemble models
python training/train_event_normalized_model.py  # Train baseline
python analysis/compare_datasets.py              # Compare performance
```

### Task 2: Enhanced Predictions
```bash
# Goal: Make predictions with best model
python prediction/predict_neural_network.py      # Neural network (89.50%)
python prediction/predict_event_normalized.py    # Ensemble baseline
```

### Task 3: Model Improvement
```bash
# Goal: Tune or modify models
python training/train_neural_network_hypertuned.py  # Re-tune parameters
# Edit training scripts to modify architecture
```

### Task 4: Analysis & Visualization
```bash
# Goal: Analyze model performance
python analysis/analyze_events.py               # Event analysis
python scripts/create_visualizations.py         # Generate charts
```

## 🔧 Technical Quick Reference

### Environment Commands
```bash
# Activate environment
.venv\Scripts\activate

# Check TensorFlow
python -c "import tensorflow as tf; print(f'TF: {tf.__version__}')"

# Verify data
python -c "import pandas as pd; print(pd.read_csv('data/event_normalized_large_dataset.csv').shape)"
```

### Model Loading
```python
# Neural Network
from training.train_neural_network_hypertuned import HyperparameterTunedNeuralNetwork
tuner = HyperparameterTunedNeuralNetwork()

# Ensemble  
from training.train_event_normalized_model import EventNormalizedModel
model = EventNormalizedModel()
```

## 🚨 Known Issues & Solutions

### Issue 1: Categorical Data Preprocessing
- **Problem**: String columns ('Orthodox', 'Southpaw') cause errors
- **Solution**: Use encoded versions (`r_stance_encoded`, `b_stance_encoded`)
- **Code Fix**: Exclude raw string columns in feature selection

### Issue 2: Unicode Display in Terminal
- **Problem**: Terminal encoding issues with progress bars
- **Solution**: Output captured in logs, functionality not affected
- **Workaround**: Check model files in `models/` directory for results

### Issue 3: Path Dependencies
- **Problem**: Scripts expect to run from root directory
- **Solution**: Always run from `cs_330/` root, not subdirectories
- **Example**: `python training/script.py` not `cd training; python script.py`

## 📊 Performance Benchmarks

### Current Best Results
```
Model                    | Accuracy | Training Time | Status
------------------------|----------|---------------|--------
Neural Network (Tuned)  | 89.50%   | ~4 minutes   | ✅ Best
Event Normalized        | ~85%     | ~2 minutes   | ✅ Baseline  
Simple Decision Tree    | ~75%     | ~30 seconds  | ✅ Fast
```

### Feature Engineering Status
```
Feature Type            | Count | Status
------------------------|-------|--------
Red Fighter Features    | 28    | ✅ Ready
Blue Fighter Features   | 28    | ✅ Ready  
Differential Features   | 27    | ✅ Ready
Categorical (Encoded)   | 7     | ✅ Ready
Total Numeric Features  | 90    | ✅ Validated
```

## 🔮 Next Development Priorities

### Phase 1: Model Comparison (Immediate)
1. Create unified comparison script
2. Generate side-by-side performance reports
3. Identify optimal model selection criteria

### Phase 2: Production Integration (Short-term)
1. Build unified prediction interface
2. Add model confidence scoring
3. Implement prediction explanation features

### Phase 3: Advanced Features (Medium-term)
1. Ensemble model combinations
2. Multi-task learning (predict method, round, time)
3. Live data integration pipeline

## 💡 AI Agent Best Practices

### When Starting Work
1. **Check Status**: Read `NEURAL_NETWORK_PROGRESS_REPORT.md` first
2. **Verify Environment**: Ensure virtual environment is active
3. **Validate Data**: Confirm datasets are in `data/` directory
4. **Review Code**: Check recent changes in target directories

### When Training Models
1. **Use Organized Structure**: Scripts in `training/` directory
2. **Save Properly**: Models go in `models/[type]/` subdirectories
3. **Document Changes**: Update progress report if significant improvements
4. **Validate Results**: Cross-reference with existing benchmarks

### When Making Predictions
1. **Use Best Model**: Neural network (89.50%) unless specific requirements
2. **Interface Consistency**: Maintain same API across prediction scripts
3. **Error Handling**: Graceful fallback if models fail to load
4. **Performance Logging**: Track prediction speed and accuracy

---

*AI Agent Reference Guide*  
*Last Updated: November 12, 2025*  
*Repository Status: Reorganized and Optimized*  
*Best Model: Neural Network (89.50% accuracy)*