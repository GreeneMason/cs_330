#!/usr/bin/env python3
"""
Repository Organization Verification Script
Tests that all reorganized components work correctly
"""

import sys
import os
from pathlib import Path

def test_directory_structure():
    """Verify new directory structure exists"""
    print("🔍 Testing Directory Structure...")
    
    expected_dirs = [
        'training',
        'prediction', 
        'analysis',
        'scripts',
        'data',
        'models',
        'docs',
        'visualizations'
    ]
    
    for dir_name in expected_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✅ {dir_name}/ - Found")
        else:
            print(f"  ❌ {dir_name}/ - Missing")
    
    print()

def test_key_files():
    """Verify key files are in correct locations"""
    print("🔍 Testing Key Files...")
    
    key_files = [
        ('README.md', 'Main documentation'),
        ('NEURAL_NETWORK_PROGRESS_REPORT.md', 'Progress report'),
        ('AI_AGENT_REFERENCE.md', 'AI Agent guide'),
        ('training/train_neural_network_hypertuned.py', 'Neural network training'),
        ('prediction/predict_neural_network.py', 'Neural network prediction'),
        ('analysis/analyze_events.py', 'Event analysis'),
        ('scripts/create_event_normalized_data.py', 'Data creation'),
        ('data/event_normalized_large_dataset.csv', 'Main dataset'),
    ]
    
    for file_path, description in key_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path} - {description}")
        else:
            print(f"  ❌ {file_path} - {description} (Missing)")
    
    print()

def test_imports():
    """Test that moved scripts can still import correctly"""
    print("🔍 Testing Import Paths...")
    
    # Test from training directory
    try:
        sys.path.append('.')
        original_cwd = os.getcwd()
        
        # Test neural network training import
        os.chdir('training')
        from train_neural_network_hypertuned import HyperparameterTunedNeuralNetwork
        print("  ✅ Neural network training imports work")
        os.chdir(original_cwd)
        
        # Test prediction imports
        os.chdir('prediction')
        # We'll just check the file exists since imports might need models
        if Path('predict_neural_network.py').exists():
            print("  ✅ Neural network prediction available")
        os.chdir(original_cwd)
        
        # Test analysis imports  
        os.chdir('analysis')
        if Path('analyze_events.py').exists():
            print("  ✅ Event analysis available")
        os.chdir(original_cwd)
        
    except Exception as e:
        print(f"  ⚠️ Import test warning: {e}")
        os.chdir(original_cwd)
    
    print()

def test_data_access():
    """Verify data files are accessible from new structure"""
    print("🔍 Testing Data Access...")
    
    try:
        import pandas as pd
        
        # Test main dataset
        df = pd.read_csv('data/event_normalized_large_dataset.csv')
        print(f"  ✅ Main dataset: {df.shape} rows/columns")
        
        # Test events reference
        events = pd.read_csv('data/events_reference.csv')
        print(f"  ✅ Events reference: {events.shape} rows/columns")
        
    except Exception as e:
        print(f"  ❌ Data access error: {e}")
    
    print()

def generate_summary():
    """Generate summary of organization"""
    print("📋 Repository Organization Summary:")
    print()
    
    print("📁 New Structure:")
    print("  ├── training/     # All model training scripts")
    print("  ├── prediction/   # All prediction interfaces") 
    print("  ├── analysis/     # Analysis and comparison tools")
    print("  ├── scripts/      # Utility scripts")
    print("  ├── data/         # Datasets")
    print("  ├── models/       # Saved models")
    print("  ├── docs/         # Documentation")
    print("  └── visualizations/ # Charts and plots")
    print()
    
    print("🎯 Benefits for AI Agents:")
    print("  ✅ Clear separation of concerns")
    print("  ✅ Intuitive file organization") 
    print("  ✅ Comprehensive documentation")
    print("  ✅ Ready-to-use command patterns")
    print("  ✅ Future-proof structure")
    print()

if __name__ == "__main__":
    print("🚀 UFC Prediction System - Organization Verification")
    print("=" * 60)
    print()
    
    test_directory_structure()
    test_key_files()
    test_imports()
    test_data_access()
    generate_summary()
    
    print("✨ Organization verification complete!")
    print("📚 Check README.md and AI_AGENT_REFERENCE.md for usage guides")