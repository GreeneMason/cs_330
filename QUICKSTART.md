# 🥊 UFC Fight Predictor - Quick Start Guide

## **⚡ Can't Activate Virtual Environment?**

**Don't worry! Use the full Python path instead:**
```powershell
# No activation needed - just use the full path to Python:
C:\Users\mason\OneDrive\Documents\GitHub\cs_330\venv\Scripts\python.exe predict_simple.py --interactive
```

**Or fix activation once and for all:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1
```

---

## **TL;DR - Predict a Fight Right Now:**

```powershell
# 1. Activate your environment
.\venv\Scripts\Activate.ps1
# OR if that doesn't work:
# venv\Scripts\Activate.ps1

# 2. Predict a fight
python predict_simple.py --interactive
```

---

## **Complete Setup (First Time Only):**

### **1. Clone the Repository**
```bash
git clone https://github.com/GreeneMason/cs_330.git
cd cs_330
```

### **2. Create Virtual Environment**
```powershell
python -m venv venv

# Activate (choose one method):

# Method 1: PowerShell (recommended)
.\venv\Scripts\Activate.ps1

# Method 2: If execution policy blocked
powershell -ExecutionPolicy Bypass -File venv\Scripts\Activate.ps1

# Method 3: Use full path
C:\Users\mason\OneDrive\Documents\GitHub\cs_330\venv\Scripts\python.exe

# Method 4: Command Prompt (if PowerShell fails)
venv\Scripts\activate.bat
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Set Up Kaggle (Optional - for fresh data)**
```bash
# Only if you want to download new data
# 1. Get API key from kaggle.com/account
# 2. Create .kaggle folder and add kaggle.json
# 3. Run: python scripts/download_dataset.py
```

**⚠️ Note:** The repo already includes trained models and databases, so you can skip this!

---

## **Daily Usage - 3 Main Tasks:**

### **📊 Task 1: Predict Fight Outcomes**

**Interactive Mode (Easiest):**
```bash
python predict_simple.py --interactive
```
- Choose Option 1: Look up fighters from database (2,479 fighters available)
- Choose Option 2: Enter stats manually for new fighters

**Command Line Mode (Quick):**
```bash
python predict_simple.py --red-fighter "Jon Jones" --blue-fighter "Daniel Cormier"
```

**Output:** Winner prediction, win probabilities, confidence level, key advantages

---

### **🤖 Task 2: Retrain Models (If You Update Data)**

```bash
python train_simple_model.py
```

**What it does:**
- Loads 7,439 historical fights
- Trains 3 models (Logistic Regression, Random Forest, XGBoost)
- Saves best model to `models/best_model.pkl`
- Takes ~2-3 minutes

**When to do this:**
- After adding new fight data
- To experiment with different features
- To improve model accuracy

---

### **📈 Task 3: Create Visualizations**

```bash
python scripts/create_visualizations.py
```

**Generates 10 charts:**
- Winner distribution
- Finish methods
- Physical attributes comparison
- Striking statistics
- Grappling statistics
- Correlation heatmap
- And more!

**Output:** Saved in `visualizations/` folder as PNG files

---

## **Project Structure:**

```
cs_330/
├── predict_simple.py         # ⭐ Main prediction tool
├── train_simple_model.py     # ⭐ Train ML models
├── data/
│   ├── ufc_database.db       # 2,479 fighters
│   └── normalized_ufc.db     # 7,439 fights
├── models/
│   └── best_model.pkl        # Trained XGBoost (74.87% accuracy)
├── scripts/
│   ├── create_visualizations.py
│   └── normalize_large_dataset.py
└── docs/
    └── prediction_guide.md   # Detailed documentation
```

---

## **Most Common Use Cases:**

### **1. Predict Next Week's UFC Event**

```bash
python predict_simple.py --interactive

# Option 1: Database lookup
Enter Red Corner fighter name: Conor McGregor
Enter Blue Corner fighter name: Dustin Poirier

# Get instant prediction!
```

### **2. Batch Predict Multiple Fights**

Create a simple script:
```python
from predict_simple import SimpleFightPredictor

predictor = SimpleFightPredictor()

fights = [
    ("Jon Jones", "Stipe Miocic"),
    ("Islam Makhachev", "Charles Oliveira"),
    ("Alexander Volkanovski", "Ilia Topuria")
]

for red, blue in fights:
    red_fighter = predictor.get_fighter_from_db(red)
    blue_fighter = predictor.get_fighter_from_db(blue)
    predictor.predict(red_fighter, blue_fighter)
```

### **3. Analyze a Specific Fighter**

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('data/ufc_database.db')
fighter = pd.read_sql_query(
    "SELECT * FROM fighter_stats WHERE name LIKE '%Jon Jones%'", 
    conn
)
print(fighter)
```

---

## **Tips & Tricks:**

### **💡 Best Practices:**

1. **Always activate venv first:**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Use interactive mode for exploration:**
   - Try different fighter matchups
   - See confidence levels
   - Understand key factors

3. **Check feature importance:**
   ```bash
   # View what matters most
   start models/feature_importance.png
   ```

4. **Database has 2,479 fighters:**
   - All UFC fighters from the dataset
   - Historical stats through ~2021
   - Use partial names for search

### **⚠️ Common Issues:**

**"Cannot activate venv" or "execution policy" error**
```powershell
# Solution 1: Bypass execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1

# Solution 2: Use full Python path (no activation needed!)
C:\Users\mason\OneDrive\Documents\GitHub\cs_330\venv\Scripts\python.exe predict_simple.py --interactive

# Solution 3: Use Command Prompt instead of PowerShell
# Open CMD (not PowerShell) and run:
venv\Scripts\activate.bat
```

**"Model not found"**
```bash
# Solution: Train the model first
python train_simple_model.py
```

**"Fighter not found"**
```bash
# Solution: Use interactive mode Option 2 to enter stats manually
python predict_simple.py --interactive
```

**Import errors**
```bash
# Solution: Activate virtual environment
.\venv\Scripts\Activate.ps1
```

---

## **Quick Reference Commands:**

```bash
# Predict fight (interactive)
python predict_simple.py --interactive

# Predict fight (command line)
python predict_simple.py --red-fighter "Name" --blue-fighter "Name"

# Train new model
python train_simple_model.py

# Create visualizations
python scripts/create_visualizations.py

# Update from GitHub
git pull origin main

# Check what's changed
git status
```

---

## **What's Inside the Models:**

- **Trained on:** 7,439 UFC fights
- **Accuracy:** 74.87% (XGBoost model)
- **Features:** 46 (physical attributes, striking stats, grappling stats, experience)
- **Most important feature:** Win rate difference
- **Can predict:** Red win, Blue win, Draw

---

## **Need More Help?**

📖 **Detailed Guides:**
- `docs/prediction_guide.md` - Complete prediction documentation
- `docs/ml_pipeline.md` - How the ML works
- `docs/database_er_diagrams.md` - Database structure

🐛 **Troubleshooting:**
- Check `CLEANUP_PLAN.md` for repo structure
- Ensure virtual environment is activated
- Verify all files in data/ and models/ exist

💬 **Questions?**
- Review docs/ folder for detailed explanations
- Check models/features.txt for list of all features
- Examine visualizations/ for data insights

---

## **Next Steps:**

1. ✅ **Try a prediction** - Start with interactive mode
2. 📊 **Explore visualizations** - See the data patterns
3. 🔬 **Experiment** - Try different fighter matchups
4. 📈 **Improve** - Add new data and retrain models
5. 🚀 **Build** - Create your own analysis tools

**Happy predicting!** 🥊
