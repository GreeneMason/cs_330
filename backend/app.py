"""
UFC Prediction System Backend API Server
Serves ML prediction endpoints and handles data processing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from prediction.predict_ensemble import UFCWeightedEnsemblePredictor

app = Flask(__name__)
CORS(app)

# Initialize the predictor
predictor = None

def get_predictor():
    global predictor
    if predictor is None:
        model_dir = os.path.join(os.path.dirname(__file__), 'trained_models', 'ensemble')
        predictor = UFCWeightedEnsemblePredictor(model_dir=model_dir)
        predictor.load_ensemble()
    return predictor

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'UFC Prediction Backend',
        'version': '1.0.0'
    })

@app.route('/predict', methods=['POST'])
def predict_fight():
    """Predict fight outcome between two fighters"""
    try:
        data = request.get_json()
        
        if not data or 'redFighter' not in data or 'blueFighter' not in data:
            return jsonify({'error': 'Missing redFighter or blueFighter data'}), 400
        
        red_fighter_name = data['redFighter']['name'] if isinstance(data['redFighter'], dict) else data['redFighter']
        blue_fighter_name = data['blueFighter']['name'] if isinstance(data['blueFighter'], dict) else data['blueFighter']
        
        # Get predictor and make prediction
        pred = get_predictor()
        result = pred.predict_fighters(red_fighter_name, blue_fighter_name)
        
        return jsonify({
            'success': True,
            'prediction': result,
            'fighters': {
                'red': data['redFighter'],
                'blue': data['blueFighter']
            }
        })
        
    except Exception as e:
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
            fighter_file = os.path.join(os.path.dirname(__file__), '..', 'ufc-prediction-frontend', 'public', 'fighters.json')
        
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
    print("🥊 Starting UFC Prediction Backend Server...")
    print("🔗 API will be available at: http://localhost:8000")
    print("📊 Endpoints:")
    print("   - GET  /health     - Health check")
    print("   - POST /predict    - Predict fight outcome")
    print("   - GET  /fighters   - Get available fighters")
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)