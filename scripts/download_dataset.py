import kagglehub

# Download latest version
path = kagglehub.dataset_download("maksbasher/ufc-complete-dataset-all-events-1996-2024")

print("Path to dataset files:", path)