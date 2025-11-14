"""
UFC Fight Prediction Dashboard
Basic web interface for the ensemble prediction system
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
import json
from datetime import datetime
import pandas as pd

# Add parent directory to path to import prediction modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prediction.predict_ensemble import UFCWeightedEnsemblePredictor

app = Flask(__name__)

# Global predictor instance
predictor = None

def load_predictor():
    """Load the ensemble predictor"""
    global predictor
    if predictor is None:
        predictor = UFCWeightedEnsemblePredictor()
    return predictor

@app.route('/')
def index():
    """Main dashboard page"""
    pred = load_predictor()
    ensemble_info = pred.get_ensemble_info()
    return render_template('index.html', ensemble_info=ensemble_info)

@app.route('/api/ensemble_status')
def ensemble_status():
    """API endpoint for ensemble status"""
    pred = load_predictor()
    return jsonify(pred.get_ensemble_info())

@app.route('/api/model_performance')
def model_performance():
    """API endpoint for model performance data"""
    pred = load_predictor()
    info = pred.get_ensemble_info()
    
    if info.get('status') != 'trained':
        return jsonify({'error': 'Models not trained'})
    
    # Extract performance data for charts
    individual_accuracies = info.get('individual_accuracies', {})
    ensemble_accuracy = info.get('accuracy', 'N/A')
    
    performance_data = {
        'models': list(individual_accuracies.keys()),
        'accuracies': [float(acc.replace('%', '')) for acc in individual_accuracies.values()],
        'ensemble_accuracy': float(ensemble_accuracy.replace('%', '')) if ensemble_accuracy != 'N/A' else 0,
        'model_weights': info.get('model_weights', {})
    }
    
    return jsonify(performance_data)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page"""
    if request.method == 'POST':
        # Handle prediction request
        # For now, just use sample data since we need actual fight data structure
        pred = load_predictor()
        
        try:
            # Load sample data to get the right structure
            sample_data = pred.load_and_prepare_data()
            if sample_data:
                X, y = sample_data
                # Use first row as sample prediction
                sample_row = X.iloc[0:1]
                
                if pred.is_trained:
                    result = pred.predict_single(sample_row)
                    return jsonify({
                        'success': True,
                        'prediction': result['prediction'],
                        'probability': result['probability'],
                        'confidence': result['confidence']
                    })
                else:
                    # Load models first
                    pred.load_ensemble()
                    result = pred.predict_single(sample_row)
                    return jsonify({
                        'success': True,
                        'prediction': result['prediction'],
                        'probability': result['probability'],
                        'confidence': result['confidence']
                    })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('predict.html')

@app.route('/train', methods=['POST'])
def train_model():
    """Train the ensemble model"""
    try:
        pred = load_predictor()
        # This would take a while, so in production you'd want to do this async
        success = pred.train_ensemble()
        return jsonify({'success': success, 'message': 'Training completed' if success else 'Training failed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)