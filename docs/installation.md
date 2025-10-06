# Installation and Setup Guide

This guide will walk you through setting up the UFC Fight Analysis project.

## Prerequisites

- Python 3.8 or higher
- Git
- A Kaggle account (for data access)

## Step 1: Clone the Repository

```bash
git clone https://github.com/GreeneMason/cs_330.git
cd cs_330
```

## Step 2: Set Up Virtual Environment

### On Windows
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 4: Kaggle Authentication

1. Go to [Kaggle Settings](https://www.kaggle.com/settings)
2. Click on "Create New API Token"
3. Move the downloaded `kaggle.json` to the `.kaggle` directory in the project
4. Ensure the file has the correct permissions:
   - Windows: No additional steps needed
   - Linux/macOS: `chmod 600 .kaggle/kaggle.json`

## Step 5: Download UFC Dataset

```bash
python scripts/download_dataset.py
```

## Step 6: Create Database

```bash
python scripts/create_database.py
```

## Step 7: Package Installation (for Development)

```bash
pip install -e .
```

## Common Issues and Solutions

### Issue: "kaggle.json not found"
- Make sure you've downloaded your Kaggle API token
- Check if the file is in the correct location (.kaggle directory)
- Verify file permissions

### Issue: Import Errors
- Ensure you've activated the virtual environment
- Verify all dependencies are installed: `pip list`
- Try reinstalling requirements: `pip install -r requirements.txt --force-reinstall`

### Issue: Database Errors
- Check if the UFC dataset was downloaded correctly
- Verify database file permissions
- Try deleting and recreating the database