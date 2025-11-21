import kagglehub

# Current Dataset (Might be outdated, check Kaggle)
# path = kagglehub.dataset_download("maksbasher/ufc-complete-dataset-all-events-1996-2024")

# Alternative Newer Datasets (Uncomment to use):
# 1. Ultimate UFC Dataset (Often updated)
# path = kagglehub.dataset_download("mdabbert/ultimate-ufc-dataset")
# 2. UFC Complete Dataset V2
# path = kagglehub.dataset_download("alexandroszigiriadis/ufc-complete-dataset-1996-2024-v2")

# Defaulting to the one currently used in the project for stability
path = kagglehub.dataset_download("maksbasher/ufc-complete-dataset-all-events-1996-2024")

print("Path to dataset files:", path)