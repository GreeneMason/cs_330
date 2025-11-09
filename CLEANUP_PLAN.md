# Repository Cleanup Plan for cs_330

## Issues Found:

### 🔴 **High Priority - Security/Privacy**
1. **`kaggle.json` in root** - Contains API credentials, should be git-ignored
2. **`.kaggle/` folder tracked** - Personal credentials exposed

### 🟡 **Medium Priority - Organization**
3. **Duplicate/redundant scripts** in root:
   - `predict_fight.py` (broken) vs `predict_simple.py` (working) ✓
   - `ufc_prediction.py` (old) vs `train_simple_model.py` (working) ✓
   - `improved_feature_analysis.py` (standalone) vs integrated in pipeline

4. **Utility scripts scattered in root**:
   - `create_visualizations.py` should be in `scripts/`
   - `extract_diagrams.py` should be in `scripts/`
   - `inspect_db.py` should be in `scripts/`
   - `run_complete_analysis.py` should be in `scripts/`

5. **Random image file**:
   - `success_factors.png` in root (should be in visualizations/)

### 🟢 **Low Priority - Best Practices**
6. **Empty/underutilized directories**:
   - `tests/` folder exists but no tests
   - `notebooks/` folder exists but empty

7. **Documentation could be consolidated**:
   - Multiple similar docs could be organized better

---

## Recommended Actions:

### **Step 1: Security Fix (URGENT)** 🔒
```bash
# Remove sensitive files from git history
git rm --cached kaggle.json
git rm --cached -r .kaggle/

# Update .gitignore to ensure they stay ignored
echo "kaggle.json" >> .gitignore
echo ".kaggle/" >> .gitignore
```

### **Step 2: Organize Scripts** 📁
```bash
# Move utility scripts to scripts/
git mv create_visualizations.py scripts/
git mv extract_diagrams.py scripts/
git mv inspect_db.py scripts/
git mv run_complete_analysis.py scripts/

# Remove broken/old scripts
git rm predict_fight.py  # Broken version (predict_simple.py works)
git rm ufc_prediction.py  # Old version (train_simple_model.py is better)
git rm improved_feature_analysis.py  # Redundant with ML pipeline

# Move image to correct folder
git mv success_factors.png visualizations/
```

### **Step 3: Update README** 📝
Add clear project structure and usage instructions

### **Step 4: Clean Up Empty Directories** 🗑️
```bash
# Either add placeholder files or remove empty directories
# tests/ - Add: touch tests/__init__.py and tests/README.md
# notebooks/ - Add: touch notebooks/README.md (for future analysis)
```

### **Step 5: Improve .gitignore** ⚙️
Add these patterns:
```
# Credentials
kaggle.json
*.json.secret
.kaggle/

# Models (too large for git)
models/*.pkl
models/*.joblib

# Large datasets
*.csv
data/*.csv
data/normalized_large_dataset.csv

# Generated files
diagrams/*.png
diagrams/*.svg
diagrams/*.mmd
```

---

## Clean Directory Structure (After Cleanup):

```
cs_330/
├── .gitignore              # Updated with better patterns
├── README.md               # Enhanced with structure info
├── requirements.txt
├── setup.py
│
├── data/                   # Data files (git-ignored)
│   ├── ufc_database.db
│   └── normalized_ufc.db
│
├── models/                 # Trained models (git-ignored)
│   ├── best_model.pkl
│   └── feature_importance.png
│
├── scripts/                # All utility scripts
│   ├── download_dataset.py
│   ├── create_database.py
│   ├── normalize_large_dataset.py
│   ├── create_visualizations.py    # MOVED
│   ├── extract_diagrams.py         # MOVED
│   ├── inspect_db.py               # MOVED
│   └── run_complete_analysis.py    # MOVED
│
├── src/ufc_analysis/       # Main package
│   ├── __init__.py
│   ├── analyzer.py
│   └── ml_pipeline.py
│
├── docs/                   # Documentation
│   ├── index.md
│   ├── prediction_guide.md
│   ├── ml_pipeline.md
│   ├── normalization_guide.md
│   ├── database_er_diagrams.md
│   └── export_diagrams_guide.md
│
├── visualizations/         # Generated plots
│   ├── success_factors.png         # MOVED
│   └── *.png (10 charts)
│
├── tests/                  # Unit tests (to be added)
│   ├── __init__.py
│   └── test_predictor.py
│
├── notebooks/              # Jupyter notebooks (future)
│   └── exploratory_analysis.ipynb
│
├── train_simple_model.py   # Main training script
└── predict_simple.py       # Main prediction script
```

---

## Benefits After Cleanup:

✅ **Security**: No exposed credentials  
✅ **Organization**: Clear separation of concerns  
✅ **Maintainability**: Easy to find files  
✅ **Professional**: Follows Python project best practices  
✅ **Smaller repo**: Remove redundant/broken files  
✅ **Better .gitignore**: Don't track large files  

---

## Execute Cleanup?

Run this script to perform all cleanup actions:
```bash
# Save this as cleanup.sh or run commands one by one
git rm --cached kaggle.json
git rm --cached -r .kaggle/
git mv create_visualizations.py scripts/
git mv extract_diagrams.py scripts/
git mv inspect_db.py scripts/
git mv run_complete_analysis.py scripts/
git mv success_factors.png visualizations/
git rm predict_fight.py
git rm ufc_prediction.py
git rm improved_feature_analysis.py
git commit -m "Clean up repository structure and remove sensitive files"
git push origin main
```

**Recommendation**: Run cleanup now before the repo gets larger!
