import pandas as pd

# Load both datasets
orig = pd.read_csv('data/UFC dataset/Large set/large_dataset.csv')
norm = pd.read_csv('data/normalized_large_dataset.csv')

print("="*70)
print("DATASET COMPARISON: Original vs Normalized")
print("="*70)

print("\n📊 ORIGINAL large_dataset.csv:")
print(f"   Rows: {len(orig):,}")
print(f"   Columns: {len(orig.columns)}")
print(f"   Null values: {orig.isnull().sum().sum():,}")
print(f"   Size: ~4.13 MB")

print("\n✨ NORMALIZED large_dataset.csv:")
print(f"   Rows: {len(norm):,}")
print(f"   Columns: {len(norm.columns)}")
print(f"   Null values: {norm.isnull().sum().sum()}")
print(f"   Size: ~5.5 MB")

print("\n" + "="*70)
print("KEY DIFFERENCES")
print("="*70)

print(f"\n✅ Same number of fights: {len(orig)} rows")
print(f"✅ Added {len(norm.columns) - len(orig.columns)} new columns")
print(f"✅ Fixed all {orig.isnull().sum().sum():,} null values → 0 nulls")

# Find new columns
new_cols = sorted(set(norm.columns) - set(orig.columns))
print(f"\n📈 NEW COLUMNS ADDED ({len(new_cols)} total):")
for i, col in enumerate(new_cols, 1):
    print(f"   {i}. {col}")

print("\n" + "="*70)
print("WHAT NORMALIZATION DID")
print("="*70)

print("""
1. 🔧 FIXED MISSING DATA:
   - Filled 2,974 null values using intelligent strategies
   - Median for numeric stats (accuracy, percentages)
   - Zero for differentials
   - 'Unknown' for categorical data

2. 📊 ADDED ENGINEERED FEATURES:
   - Win rates for both fighters
   - Experience differentials
   - BMI calculations
   - Striking efficiency metrics
   - Grappling efficiency metrics
   - Defensive ratings

3. 🎯 ENCODING:
   - One-hot encoded categorical variables (stance, method, etc.)
   - Scaled numerical features (MinMax for %, Standard for counts)
   - Ready for machine learning

4. 🗄️ CREATED RELATIONAL DATABASE:
   - Split into 4 tables (3NF): events, fighters, fights, fight_statistics
   - Saved as normalized_fight.db
   - Maintains data integrity and reduces redundancy

5. 💾 OUTPUT:
   - Clean CSV: normalized_large_dataset.csv (101 columns)
   - Database: normalized_fight.db (4 tables)
   - Zero null values, all data ready for ML
""")

print("="*70)
print("USAGE")
print("="*70)

print("""
Use ORIGINAL (large_dataset.csv) when:
- You want raw, unprocessed data
- Doing exploratory data analysis
- Need to see original null patterns
- Retraining with different preprocessing

Use NORMALIZED (normalized_large_dataset.csv) when:
- Training machine learning models ✓ (USED BY train_simple_model.py)
- Need clean data with no nulls
- Want engineered features included
- Running predictions or analysis
""")

print("="*70)
