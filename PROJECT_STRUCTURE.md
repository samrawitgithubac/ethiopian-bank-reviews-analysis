# Project Structure Documentation

This document describes the organized folder structure of the Ethiopian Bank Reviews Analysis project.

## Directory Structure

```
ethiopian-bank-reviews-analysis/
│
├── README.md                          # Main project documentation
├── requirements.txt                   # Python package dependencies
├── .gitignore                        # Git ignore rules
├── PROJECT_STRUCTURE.md              # This file
│
├── data/                              # All data files
│   ├── raw/                          # Raw scraped data (Task 1 output)
│   │   └── ethiopian_bank_reviews.csv
│   │
│   ├── cleaned/                      # Cleaned/preprocessed data (Task 1 output)
│   │   └── cleaned_reviews.csv
│   │
│   └── processed/                    # Processed data with analysis (Task 2 output)
│       ├── reviews_with_sentiment.csv
│       └── reviews_with_themes.csv
│
├── scripts/                          # All Python scripts organized by task
│   │
│   ├── task1_data_collection/        # Task 1: Web scraping and preprocessing
│   │   ├── scrape_reviews.py         # Scrapes reviews from Google Play Store
│   │   ├── preprocess_reviews.py     # Cleans and preprocesses scraped data
│   │   ├── find_app_id.py            # Helper script to find app IDs
│   │   └── test_boa_apps.py          # Testing script for app verification
│   │
│   ├── task2_analysis/               # Task 2: Sentiment and thematic analysis
│   │   ├── sentiment_analysis.py     # Performs sentiment analysis (distilbert/VADER)
│   │   └── thematic_analysis.py      # Extracts keywords and identifies themes
│   │
│   └── task3_database/                # Task 3: PostgreSQL database operations
│       ├── database_setup.py         # Creates database and tables
│       ├── insert_reviews.py         # Inserts review data into database
│       └── verify_database.py        # Verifies data integrity with SQL queries
│
├── database/                         # Database-related files
│   └── schema.sql                    # PostgreSQL schema definition
│
└── docs/                             # Documentation files
    ├── TASK_REVIEW_SUMMARY.md        # Summary of task completion status
    ├── TASK3_SETUP_GUIDE.md         # Detailed guide for Task 3 setup
    └── Readmetask1.txt               # Task 1 specific notes
```

## File Descriptions

### Root Files
- **README.md**: Main project documentation with overview, setup instructions, and task descriptions
- **requirements.txt**: Lists all Python package dependencies needed for the project
- **.gitignore**: Specifies files and directories to ignore in Git
- **PROJECT_STRUCTURE.md**: This documentation file

### Data Directory (`data/`)
Contains all CSV data files organized by processing stage:
- **raw/**: Original scraped data from Google Play Store
- **cleaned/**: Preprocessed data after cleaning and normalization
- **processed/**: Final data with sentiment labels and themes added

### Scripts Directory (`scripts/`)
Contains all Python scripts organized by task:
- **task1_data_collection/**: Scripts for scraping and preprocessing
- **task2_analysis/**: Scripts for sentiment and thematic analysis
- **task3_database/**: Scripts for database operations

### Database Directory (`database/`)
Contains database schema and setup files:
- **schema.sql**: SQL script to create database tables manually

### Docs Directory (`docs/`)
Contains additional documentation:
- Task summaries, setup guides, and project notes

## Running Scripts

All scripts should be run from the project root directory. The scripts use relative paths to access data files.

### Example:
```bash
# From project root
python scripts/task1_data_collection/scrape_reviews.py
python scripts/task2_analysis/sentiment_analysis.py
python scripts/task3_database/database_setup.py
```

## Benefits of This Structure

1. **Organization**: Clear separation of data, scripts, and documentation
2. **Scalability**: Easy to add new tasks or scripts
3. **Maintainability**: Related files are grouped together
4. **Clarity**: Easy to understand project structure at a glance
5. **Best Practices**: Follows standard Python project structure conventions

## Notes

- All scripts use relative paths, so they should be run from the project root
- Data files are organized by processing stage for easy tracking
- Scripts are organized by task for clear workflow understanding
- Documentation is centralized in the `docs/` folder

