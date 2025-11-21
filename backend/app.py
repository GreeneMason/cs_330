"""
Fight Prediction System Backend API Server
Serves ML prediction endpoints and handles data processing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from prediction.predict_ensemble import FightWeightedEnsemblePredictor
from prediction.predict_neural_network import EventNormalizedNeuralNetworkPredictor
from prediction.predict_event_normalized import EventNormalizedPredictor

app = Flask(__name__)
CORS(app)

# Initialize the predictors
ensemble_predictor = None
nn_predictor = None
xgboost_predictor = None

def get_ensemble_predictor():
    global ensemble_predictor
    if ensemble_predictor is None:
        # Use default path which is now correct in the class
        ensemble_predictor = FightWeightedEnsemblePredictor()
        ensemble_predictor.load_ensemble()
    return ensemble_predictor

def get_nn_predictor():
    global nn_predictor
    if nn_predictor is None:
        nn_predictor = EventNormalizedNeuralNetworkPredictor()
        nn_predictor.load_model()
    return nn_predictor

def get_xgboost_predictor():
    global xgboost_predictor
    if xgboost_predictor is None:
        xgboost_predictor = EventNormalizedPredictor()
        xgboost_predictor.load_model()
    return xgboost_predictor

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Fight Prediction Backend',
        'version': '1.0.0'
    })

import numpy as np

def convert_to_serializable(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    return obj

@app.route('/predict', methods=['POST'])
def predict_fight():
    """Predict fight outcome between two fighters"""
    try:
        data = request.get_json()
        
        if not data or 'redFighter' not in data or 'blueFighter' not in data:
            return jsonify({'error': 'Missing redFighter or blueFighter data'}), 400
        
        red_fighter_name = data['redFighter']['name'] if isinstance(data['redFighter'], dict) else data['redFighter']
        blue_fighter_name = data['blueFighter']['name'] if isinstance(data['blueFighter'], dict) else data['blueFighter']
        
        # Get predictors
        ensemble = get_ensemble_predictor()
        nn = get_nn_predictor()
        xgb = get_xgboost_predictor()
        
        # 1. Ensemble Prediction (also gets features)
        ensemble_result = ensemble.predict_fighters(red_fighter_name, blue_fighter_name)
        fight_data = ensemble_result.get('fight_data', {})
        
        # 2. NN Prediction
        nn_result = nn.predict_single_fight(fight_data)
        
        # 3. XGBoost Prediction
        xgb_result = xgb.predict_dict(fight_data)
        
        # Construct response with all models
        response = {
            'success': True,
            'prediction': ensemble_result, # Main result (backward compatibility)
            'models': {
                'ensemble': {
                    'name': 'Weighted Ensemble',
                    'winner': ensemble_result['prediction'],
                    'probability': ensemble_result['probability'],
                    'confidence': ensemble_result['confidence'],
                    'accuracy': '91.3%'
                },
                'neural_network': {
                    'name': 'Neural Network',
                    'winner': nn_result['predicted_winner'] if nn_result else 'Unknown',
                    'probability': (nn_result['blue_win_probability'] if nn_result['predicted_winner'] == 'Blue' else nn_result['red_win_probability']) if nn_result else 0,
                    'confidence': nn_result['confidence'] if nn_result else 0,
                    'accuracy': '91.4%'
                },
                'xgboost': {
                    'name': 'XGBoost',
                    'winner': xgb_result['prediction'] if xgb_result else 'Unknown',
                    'probability': xgb_result['probability'] if xgb_result else 0,
                    'confidence': xgb_result['confidence'] if xgb_result else 0,
                    'accuracy': '91.1%'
                }
            },
            'fighters': {
                'red': data['redFighter'],
                'blue': data['blueFighter']
            }
        }
        
        # Convert all numpy types to native Python types
        response = convert_to_serializable(response)
        
        return jsonify(response)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False
        }), 500

@app.route('/fighters', methods=['GET'])
def get_fighters():
    """Get list of all available fighters"""
    try:
        # Load fighter data from the shared data directory
        fighter_file = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data', 'fighters.json')
        
        # Also try the old location as fallback
        if not os.path.exists(fighter_file):
            fighter_file = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'fighters.json')
        
        if os.path.exists(fighter_file):
            import json
            with open(fighter_file, 'r') as f:
                fighters = json.load(f)
            return jsonify({'fighters': fighters, 'count': len(fighters)})
        else:
            return jsonify({'error': f'Fighter data not found. Looked for: {fighter_file}'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Failed to load fighters: {str(e)}'}), 500

if __name__ == '__main__':
    print("🥊 Starting Fight Prediction Backend Server...")
    print("🔗 API will be available at: http://localhost:8000")
    print("📊 Endpoints:")
    print("   - GET  /health     - Health check")
    print("   - POST /predict    - Predict fight outcome")
    print("   - GET  /fighters   - Get available fighters")
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)