# Project Structure

Clean, industry-standard project structure for Ethiopian Bank Reviews Analysis.

```
ethiopian-bank-reviews-analysis/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline
│
├── data/                             # Data files (gitignored)
│   ├── raw/                         # Raw scraped data
│   ├── cleaned/                     # Cleaned/preprocessed data
│   └── processed/                   # Processed data with analysis
│
├── notebooks/                        # Jupyter notebooks
│   ├── eda.ipynb                    # Exploratory data analysis
│   └── show_results.py              # Quick results viewer
│
├── src/                              # Source code
│   ├── __init__.py
│   ├── data_processing.py           # Data collection & preprocessing
│   ├── train.py                     # Model training
│   ├── predict.py                   # Prediction functions
│   └── api/                         # FastAPI application
│       ├── __init__.py
│       ├── main.py                  # FastAPI app
│       └── pydantic_models.py       # API data models
│
├── tests/                            # Unit tests
│   ├── __init__.py
│   └── test_data_processing.py      # Tests for data processing
│
├── database/                         # Database files
│   └── schema.sql                   # PostgreSQL schema
│
├── docs/                             # Documentation
│   └── TASK3_SETUP_GUIDE.md         # Database setup guide
│
├── Dockerfile                        # Docker configuration
├── docker-compose.yml               # Docker Compose setup
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # Project documentation
```

## Key Directories

- **`src/`**: All production code (data processing, training, prediction, API)
- **`notebooks/`**: Exploratory analysis and visualization
- **`tests/`**: Unit tests for code quality
- **`data/`**: Data files (gitignored, not tracked)
- **`database/`**: Database schema and setup files
- **`docs/`**: Project documentation

## Usage

See `README.md` for detailed usage instructions.

