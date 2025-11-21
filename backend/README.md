# Fight Prediction Backend

Python-based machine learning backend for fight prediction.

## Features
- 91.33% accurate weighted ensemble model
- RESTful API endpoints
- Real-time fight predictions
- Fighter database integration

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run server: `python app.py`
3. API available at: `http://localhost:8000`

## API Endpoints

### Health Check
```
GET /health
```

### Predict Fight
```
POST /predict
Body: {
  "redFighter": {"name": "Fighter A"},
  "blueFighter": {"name": "Fighter B"}
}
```

### Get Fighters
```
GET /fighters
```

## Model Architecture
- Gradient Boosting (25.1% weight)
- Random Forest (24.7% weight) 
- SVM (25.1% weight)
- Neural Network (25.1% weight)

Weighted ensemble achieves 91.33% accuracy on test data.