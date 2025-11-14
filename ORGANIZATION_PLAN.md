# UFC Prediction Repository Organization Plan

## Current Issues
- Frontend and backend code mixed together
- Data scattered across multiple directories
- No clear development workflow
- Path references are confusing
- Hard to navigate and maintain

## Proposed New Structure
```
ufc-prediction-system/
├── README.md                     # Main project overview
├── package.json                  # Root package management
├── .gitignore                    # Unified git ignore
├── dev-scripts/                  # Development workflow scripts
│   ├── start-dev.bat            # Start both frontend and backend
│   ├── build.bat                # Build production version
│   └── test.bat                 # Run all tests
│
├── backend/                      # Python ML Backend
│   ├── README.md                # Backend documentation
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Backend environment variables
│   ├── app.py                   # Main Flask/FastAPI server
│   ├── src/                     # Source code
│   │   ├── __init__.py
│   │   ├── models/              # ML model definitions
│   │   ├── prediction/          # Prediction logic
│   │   ├── training/            # Model training scripts
│   │   ├── analysis/            # Data analysis
│   │   └── utils/               # Utility functions
│   ├── trained_models/          # Saved model files
│   │   ├── ensemble/
│   │   ├── neural_network/
│   │   └── individual/
│   ├── tests/                   # Backend tests
│   └── scripts/                 # Backend utility scripts
│
├── frontend/                     # Next.js Frontend
│   ├── README.md                # Frontend documentation
│   ├── package.json             # Frontend dependencies
│   ├── next.config.ts           # Next.js configuration
│   ├── app/                     # Next.js app directory
│   ├── components/              # React components
│   ├── lib/                     # Frontend utilities
│   ├── public/                  # Static assets
│   └── __tests__/               # Frontend tests
│
├── shared/                       # Shared Resources
│   ├── data/                    # All datasets and data files
│   │   ├── raw/                 # Original datasets
│   │   ├── processed/           # Cleaned/processed data
│   │   ├── fighters/            # Fighter database files
│   │   └── exports/             # Generated exports
│   ├── docs/                    # Documentation
│   │   ├── api/                 # API documentation
│   │   ├── ml/                  # ML model documentation
│   │   ├── frontend/            # Frontend documentation
│   │   └── deployment/          # Deployment guides
│   └── config/                  # Shared configuration
│
└── tools/                        # Development Tools
    ├── data-processing/          # Data processing scripts
    ├── visualization/            # Visualization tools
    ├── database/                # Database management
    └── deployment/               # Deployment scripts
```

## Benefits of This Structure

### 1. **Clear Separation of Concerns**
- Backend: All Python/ML code in one place
- Frontend: All React/Next.js code in one place
- Shared: Data and docs accessible to both

### 2. **Easy Development Workflow**
- `dev-scripts/start-dev.bat` - One command to start everything
- Clear entry points for each component
- Simplified path management

### 3. **Better Maintainability**
- Logical grouping of related files
- Easy to find and modify components
- Clear dependencies between parts

### 4. **Scalability**
- Easy to add new features
- Simple to onboard new developers
- Clean testing structure

## Migration Steps
1. Create new directory structure
2. Move backend Python code to `backend/`
3. Move frontend Next.js code to `frontend/`
4. Move all data to `shared/data/`
5. Update all path references
6. Create development scripts
7. Test everything works
8. Update documentation

## Development Workflow After Organization
```bash
# Start development environment
./dev-scripts/start-dev.bat

# This will:
# 1. Start backend Python server on port 8000
# 2. Start frontend Next.js dev server on port 3000  
# 3. Both will automatically reload on changes
```

## Path Examples After Organization
```python
# Backend importing data
data_path = "../shared/data/processed/event_normalized_large_dataset.csv"

# Backend saving models  
model_path = "./trained_models/ensemble/"

# Frontend API calls
fetch('/api/predict')  # Proxied to backend:8000
```