# UFC Fight Prediction Analysis System

🥊 **Advanced Machine Learning System for UFC Fight Outcome Prediction**

This repository contains a comprehensive ML pipeline for UFC fight analysis with multiple model types including decision trees, ensemble methods, and neural networks achieving up to **89.50% accuracy**.

## 🚀 Quick Start for AI Agents

### Repository Structure Overview
```
cs_330/
├── 📚 DOCUMENTATION/           # Main reference docs for AI agents
│   ├── README.md              # This file - main entry point
│   ├── NEURAL_NETWORK_PROGRESS_REPORT.md  # Complete implementation status
│   ├── NEURAL_NETWORK_TRAINING_GUIDE.md   # Step-by-step neural network guide
│   ├── EVENT_NORMALIZATION.md             # Event normalization methodology
│   └── QUICKSTART.md                      # Rapid setup guide
│
├── 🏋️ training/               # All model training scripts
│   ├── train_simple_model.py              # Basic decision tree
│   ├── train_event_normalized_model.py    # Enhanced ensemble model  
│   ├── train_neural_network_model.py      # Basic neural network
│   └── train_neural_network_hypertuned.py # Optimized neural network (89.50%)
│
├── 🔮 prediction/             # Prediction interfaces
│   ├── predict_simple.py                  # Basic predictions
│   ├── predict_event_normalized.py        # Ensemble predictions
│   └── predict_neural_network.py          # Neural network predictions
│
├── 📊 analysis/               # Analysis and comparison tools
│   ├── analyze_events.py                  # Event analysis
│   └── compare_datasets.py                # Dataset comparison
│
├── 🛠️ scripts/               # Utility scripts
├── 📁 data/                  # Datasets (7,439 fights, 90+ features)
├── 🤖 models/                # Saved models and metadata
├── 📖 docs/                  # Detailed documentation
└── 📈 visualizations/        # Generated plots and charts
```

### Model Performance Summary
| Model Type | Accuracy | Features | Status |
|------------|----------|----------|--------|
| Simple Decision Tree | ~75% | Basic | ✅ Complete |
| Event Normalized Ensemble | ~85% | Enhanced | ✅ Complete |
| **Neural Network (Optimized)** | **89.50%** | Fighter-Aware | ✅ **BEST** |

## 🎯 Current Status & Next Steps

### ✅ Completed
- **Neural Network Implementation**: 89.50% accuracy achieved
- **Fighter-Aware Architecture**: Separate processing branches for red/blue fighters
- **Hyperparameter Optimization**: Automated tuning with Keras Tuner
- **Production-Ready Code**: Model saving, loading, and prediction interfaces

### 🚧 Next Priority (Phase 1)
1. **Model Comparison Framework** - Compare neural network vs ensemble models
2. **Unified Prediction Interface** - Single interface supporting all model types
3. **Performance Validation** - Cross-validation on identical test sets

### 🔮 Future Development (Phases 2-4)
- Ensemble model combinations and stacking
- Production deployment with monitoring
- Continuous learning with live data

## 🤖 AI Agent Quick Commands

### Environment Setup
```bash
# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Model Training
```bash
# Train best performing model (Neural Network)
python training/train_neural_network_hypertuned.py

# Train ensemble model for comparison
python training/train_event_normalized_model.py
```

### Predictions
```bash
# Neural network predictions (best accuracy)
python prediction/predict_neural_network.py

# Ensemble predictions (for comparison)
python prediction/predict_event_normalized.py
```

### Analysis
```bash
# Compare datasets
python analysis/compare_datasets.py

# Analyze fight events
python analysis/analyze_events.py
```

## 📚 Key Documentation for AI Agents

### Primary References
1. **[NEURAL_NETWORK_PROGRESS_REPORT.md](./NEURAL_NETWORK_PROGRESS_REPORT.md)** 
   - Complete implementation status and results
   - Technical architecture details  
   - Future development roadmap

2. **[NEURAL_NETWORK_TRAINING_GUIDE.md](./NEURAL_NETWORK_TRAINING_GUIDE.md)**
   - Step-by-step implementation guide
   - Architecture options (Simple → Advanced → Fighter-Aware)
   - Hyperparameter tuning methodology

3. **[EVENT_NORMALIZATION.md](./EVENT_NORMALIZATION.md)**
   - Event normalization methodology
   - Feature engineering details
   - Data preprocessing pipeline

### Technical Specifications
- **Dataset**: 7,439 UFC fights with 90+ engineered features
- **Best Model**: Fighter-aware neural network with hyperparameter optimization
- **Architecture**: Separate branches for red/blue fighters + decision layers
- **Framework**: TensorFlow 2.20.0 with Keras Tuner
- **Validation**: Stratified K-fold cross-validation

## 🔧 Development Environment

### Requirements
- **Python**: 3.11+ (tested with 3.11.0)
- **TensorFlow**: 2.20.0 
- **Keras Tuner**: 1.4.8
- **Core ML**: pandas, scikit-learn, matplotlib, seaborn

### Virtual Environment
```bash
# Windows PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Data Location
- **Training Data**: `data/event_normalized_large_dataset.csv`
- **Reference Data**: `data/events_reference.csv`  
- **Models**: `models/` directory with subdirectories by type

## 🎯 AI Agent Usage Patterns

### For Model Development
1. **Check Progress**: Read `NEURAL_NETWORK_PROGRESS_REPORT.md`
2. **Understand Architecture**: Review `NEURAL_NETWORK_TRAINING_GUIDE.md`
3. **Run Training**: Execute scripts in `training/` directory
4. **Validate Results**: Use scripts in `analysis/` directory

### For Predictions
1. **Load Models**: Use scripts in `prediction/` directory
2. **Compare Models**: Run both neural network and ensemble predictions
3. **Analyze Results**: Use visualization tools in `scripts/`

### For Extension
1. **Add New Models**: Follow patterns in `training/` directory
2. **Enhance Features**: Modify data pipeline in `scripts/`
3. **Improve Interface**: Extend prediction scripts in `prediction/`

## 📈 Performance Benchmarks

### Neural Network (Current Best)
- **Validation Accuracy**: 89.50%
- **Training Time**: ~4 minutes (hyperparameter tuning)
- **Inference Speed**: <100ms per prediction
- **Memory Usage**: <1GB RAM

### Comparison Baseline
- **Ensemble Model**: ~85% accuracy
- **Simple Model**: ~75% accuracy
- **All models use identical feature engineering and validation**

---

## 📞 Quick Help

### Common Tasks
- **Train new model**: Use scripts in `training/` directory
- **Make predictions**: Use scripts in `prediction/` directory  
- **Compare models**: Check `analysis/` directory
- **Add features**: Modify scripts in `scripts/` directory

### Troubleshooting
- **Environment Issues**: Check virtual environment activation
- **Data Issues**: Verify files in `data/` directory exist
- **Model Issues**: Check `models/` directory for saved models
- **Performance Issues**: Review `NEURAL_NETWORK_PROGRESS_REPORT.md`

*Last Updated: November 12, 2025*  
*Current Status: Neural Network Implementation Complete (89.50% accuracy)*  
*Next Phase: Model Comparison Framework*