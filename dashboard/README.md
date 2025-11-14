# UFC Fight Prediction Dashboard

A basic web interface for the UFC fight prediction ensemble system.

## Features

### 🏠 Dashboard (Main Page)
- **System Status**: Shows if models are trained and ready
- **Performance Metrics**: Ensemble accuracy, AUC score, feature count
- **Training Information**: When models were last trained, sample count
- **Performance Charts**: 
  - Bar chart comparing individual model accuracies vs ensemble
  - Pie chart showing model weights in ensemble
- **Quick Actions**: Predict fights, refresh data, retrain models

### 🔮 Prediction Page
- **Sample Prediction**: Demo using real fight data structure  
- **Prediction Results**: Winner, probability, confidence level
- **Model Breakdown**: Shows how each model contributes to final decision
- **Interactive Interface**: Clean form-based input (currently using sample data)

## Current Capabilities

### ✅ Working Features
- Real-time system status monitoring
- Live performance visualization with Chart.js
- Sample predictions using trained ensemble
- Model weight and accuracy displays
- Responsive Bootstrap design

### 🚧 Future Enhancements
- [ ] Manual fighter input forms
- [ ] Historical fight lookup and analysis
- [ ] Batch prediction uploads
- [ ] Model training progress tracking
- [ ] Fighter database integration
- [ ] Advanced analytics and insights
- [ ] Real-time fight odds comparison
- [ ] Performance tracking over time

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5 + Chart.js
- **ML Integration**: Direct import of ensemble prediction system
- **Data**: Uses existing UFC dataset and trained models

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start dashboard
python app.py

# Open browser
http://localhost:5000
```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /predict` - Prediction interface  
- `POST /predict` - Make prediction (currently sample data)
- `GET /api/ensemble_status` - Get system status JSON
- `GET /api/model_performance` - Get performance data for charts
- `POST /train` - Trigger model retraining (takes several minutes)

## Dashboard Structure

```
dashboard/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies  
├── templates/
│   ├── index.html        # Main dashboard page
│   └── predict.html      # Prediction interface
└── README.md             # This file
```

## Integration Notes

The dashboard directly imports and uses:
- `prediction/predict_ensemble.py` - Main ensemble predictor
- `models/ensemble/` - Trained model files
- `data/event_normalized_large_dataset.csv` - Training data

## Performance Display

Currently showing the trained ensemble performance:
- **Ensemble Accuracy**: 91.33% 
- **Individual Models**:
  - Gradient Boosting: 90.99% (weight: 0.251)
  - SVM: 90.79% (weight: 0.251) 
  - Neural Network: 90.73% (weight: 0.251)
  - Random Forest: 89.31% (weight: 0.247)

## Usage Examples

### View System Status
Navigate to the main dashboard to see:
- Training status and model readiness
- Performance metrics and charts
- Last training date and sample count

### Make Predictions  
Go to `/predict` to:
- See sample prediction demonstration
- View prediction confidence and breakdown
- Understand how ensemble models contribute

### Monitor Performance
The dashboard automatically loads and displays:
- Real-time accuracy comparisons
- Model weight distributions  
- Training metadata and statistics