# UFC Fight Prediction Guide

## Overview
This guide explains how to predict upcoming UFC fights using the trained machine learning model.

## Prerequisites
1. **Trained Model Required**: You must first train a model by running:
   ```bash
   python src/ufc_analysis/ml_pipeline.py
   ```
   This creates `models/best_model.pkl`

2. **Fighter Database**: The `data/ufc_database.db` database contains historical fighter statistics

## How to Predict Fights

### Method 1: Interactive Mode (Recommended)

This is the easiest way to predict fights. It provides a menu-driven interface:

```bash
python predict_fight.py --interactive
```

**You'll have two options:**

#### Option 1: Database Lookup
- Search for fighters by name from the historical database
- Great for predicting matchups between known fighters
- Automatically loads all fighter statistics

**Example:**
```
Enter Red Corner fighter name: Conor McGregor
Enter Blue Corner fighter name: Khabib Nurmagomedov
```

#### Option 2: Manual Entry
- Manually enter all fighter statistics
- Perfect for new fighters not in the database
- Useful for hypothetical matchups

**Required Statistics:**
- Name
- Total Wins & Losses
- Height (cm)
- Weight (kg)
- Reach (cm)
- Age
- Stance (Orthodox, Southpaw, Switch, Open Stance)
- **Striking Stats:**
  - SLpM (Strikes Landed per Minute)
  - Significant Strike Accuracy (%)
  - SApM (Strikes Absorbed per Minute)
  - Strike Defense (%)
- **Grappling Stats:**
  - Takedown Average (per 15 min)
  - Takedown Accuracy (%)
  - Takedown Defense (%)
  - Submission Average (per 15 min)

### Method 2: Command Line

Quick predictions from the command line:

```bash
python predict_fight.py --red-fighter "Fighter Name" --blue-fighter "Fighter Name"
```

**Example:**
```bash
python predict_fight.py --red-fighter "Jon Jones" --blue-fighter "Daniel Cormier"
```

### Method 3: Custom Model

Use a different trained model:

```bash
python predict_fight.py --interactive --model "path/to/custom_model.pkl"
```

## Understanding the Output

### Prediction Results

```
🏆 Predicted Winner: Red Corner

Win Probabilities:
   🔴 Red Corner:  65.32%
   🔵 Blue Corner: 32.15%
   🤝 Draw:        2.53%

📊 Prediction Confidence: MODERATE (65.32%)
```

**Confidence Levels:**
- **HIGH** (≥70%): Strong confidence in prediction
- **MODERATE** (55-69%): Reasonable confidence
- **LOW** (<55%): Close fight, could go either way

### Key Advantages

The predictor identifies which fighter has advantages in:
- **Physical Attributes**: Height, reach, experience
- **Striking**: Offensive output, accuracy, defense
- **Grappling**: Takedowns, submissions, defense

**Example:**
```
KEY ADVANTAGES
✓ Red has significant height advantage (+10.2 cm)
✓ Red has striking advantage (efficiency: 15.3%)
✓ Blue has more experience (+8 fights)
✓ Blue has grappling advantage (efficiency: 12.7%)
```

## Where to Find Fighter Stats

### For Fighters in Database
- Simply use their name in interactive mode
- The script will look them up automatically

### For New/Upcoming Fighters

Get statistics from these sources:

1. **UFC Official Stats**: [ufcstats.com](http://ufcstats.com)
   - Most comprehensive official source
   - Includes all required statistics

2. **Sherdog**: [sherdog.com](http://sherdog.com)
   - Fighter profiles with detailed stats
   - Good for historical data

3. **Tapology**: [tapology.com](http://tapology.com)
   - Up-to-date fighter information
   - Good for upcoming fights

4. **ESPN MMA**: [espn.com/mma](http://espn.com/mma)
   - Current UFC fighter stats
   - Easy to navigate

### Converting Units

If stats are in imperial units:

**Height:**
- Inches to cm: multiply by 2.54
- Example: 70 inches × 2.54 = 177.8 cm

**Weight:**
- Pounds to kg: multiply by 0.453592
- Example: 185 lbs × 0.453592 = 83.9 kg

**Reach:**
- Inches to cm: multiply by 2.54
- Example: 74 inches × 2.54 = 188.0 cm

## Tips for Better Predictions

### 1. Use Recent Statistics
- Fighter stats change over time
- Use their most recent performance data
- Consider if they've moved weight classes

### 2. Consider Context
- Training camp reports
- Recent injuries
- Style matchups
- Home advantage

### 3. Watch for Outliers
- Very high confidence (>90%) may indicate data issues
- Verify input statistics are correct
- Check for typos in manual entry

### 4. Understand Limitations
- Model is trained on historical data
- Cannot account for:
  - Day-of weight cuts
  - Psychological factors
  - Corner strategies
  - Referee/judging factors
  - Cage rust (long layoffs)

## Example Walkthrough

Let's predict a hypothetical fight:

### Step 1: Start Interactive Mode
```bash
python predict_fight.py --interactive
```

### Step 2: Choose Input Method
```
Options:
1. Look up fighters from database
2. Manually enter fighter statistics
3. Exit

Select option (1-3): 1
```

### Step 3: Enter Fighter Names
```
Enter Red Corner fighter name: Israel Adesanya
Enter Blue Corner fighter name: Alex Pereira
```

### Step 4: Review Prediction
```
FIGHT PREDICTION
════════════════════════════════════════════════════════════

🔴 Red Corner: Israel Adesanya
   Record: 24-2
   Win Rate: 92.3%

🔵 Blue Corner: Alex Pereira
   Record: 8-2
   Win Rate: 80.0%

════════════════════════════════════════════════════════════
PREDICTION RESULTS
════════════════════════════════════════════════════════════

🏆 Predicted Winner: Red Corner

Win Probabilities:
   🔴 Red Corner:  58.23%
   🔵 Blue Corner: 39.41%
   🤝 Draw:        2.36%

📊 Prediction Confidence: MODERATE (58.23%)

════════════════════════════════════════════════════════════
KEY ADVANTAGES
════════════════════════════════════════════════════════════
✓ Red has more experience (+14 fights)
✓ Red has striking advantage (efficiency: 8.5%)
✓ Blue has grappling advantage (efficiency: 5.2%)
```

## Troubleshooting

### "Model not found" Error
**Solution:** Train the model first:
```bash
python src/ufc_analysis/ml_pipeline.py
```

### "Fighter not found" Error
**Solution:** 
- Check spelling
- Try partial name (last name only)
- Use manual entry option

### Multiple Fighters Found
**Solution:**
- Interactive mode will show all matches
- Select the correct fighter by number
- Include full name for better matching

### Import Errors
**Solution:** Activate virtual environment:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Or use direct path
C:/path/to/venv/Scripts/python.exe predict_fight.py --interactive
```

## Advanced Usage

### Python Script Integration

You can use the predictor in your own scripts:

```python
from predict_fight import FightPredictor
import pandas as pd

# Initialize predictor
predictor = FightPredictor()

# Create fighter data
red_fighter = pd.Series({
    'name': 'Fighter A',
    'wins': 20, 'losses': 3,
    'height': 180, 'weight': 77,
    'reach': 185, 'age': 28,
    'stance': 'Orthodox',
    'SLpM': 4.5, 'sig_str_accuracy': 55,
    'SApM': 3.2, 'str_def': 60,
    'td_avg': 2.5, 'td_accuracy': 45,
    'td_def': 75, 'sub_avg': 0.8
})

blue_fighter = pd.Series({
    'name': 'Fighter B',
    'wins': 18, 'losses': 5,
    'height': 175, 'weight': 77,
    'reach': 180, 'age': 30,
    'stance': 'Southpaw',
    'SLpM': 3.8, 'sig_str_accuracy': 48,
    'SApM': 4.1, 'str_def': 55,
    'td_avg': 3.2, 'td_accuracy': 50,
    'td_def': 70, 'sub_avg': 1.2
})

# Make prediction
prediction, probabilities = predictor.predict(red_fighter, blue_fighter)
```

## Next Steps

1. **Train the model** if you haven't already
2. **Test predictions** on recent fights to gauge accuracy
3. **Compare predictions** with betting odds for validation
4. **Track your predictions** to measure performance over time

## Support

For issues or questions:
1. Check that the model is trained
2. Verify fighter statistics are correct
3. Ensure database exists at `data/ufc_database.db`
4. Review error messages carefully

---

**Disclaimer**: This tool is for educational and entertainment purposes. Predictions are based on historical data and statistical analysis. Actual fight outcomes depend on many factors not captured by the model. Always do your own research and never rely solely on automated predictions for betting or other decisions.
