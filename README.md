# Customer Experience Analytics for Fintech Apps

## Project Overview
This project is a **real-world data engineering challenge** focused on analyzing customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

As a Data Analyst at **Omega Consultancy**, the goal is to scrape app reviews, analyze sentiments and themes, store data in PostgreSQL, and provide actionable recommendations to improve customer experience and retention.

---

## Business Objective
- Collect and preprocess Google Play Store reviews.
- Analyze sentiment (positive, negative, neutral) and extract themes such as bugs, UI, or feature requests.
- Identify satisfaction drivers (e.g., speed) and pain points (e.g., app crashes).
- Store cleaned review data in a PostgreSQL database.
- Deliver visualizations and a report with actionable recommendations.

---

## Scenarios
1. **Retaining Users:** Analyze slow loading or transfer complaints to identify widespread issues.
2. **Enhancing Features:** Extract requested features to help banks stay competitive.
3. **Managing Complaints:** Cluster common complaints to guide AI chatbot integration and support improvements.

---

## Dataset Overview
- **Review Text:** User feedback (e.g., "Love the UI, but it crashes often").
- **Rating:** 1–5 stars.
- **Date:** Posting date.
- **Bank/App Name:** E.g., “Commercial Bank of Ethiopia Mobile”.
- **Source:** Google Play.
- **Minimum Reviews:** 400 per bank (1,200 total).

---

## Task 1: Data Collection and Preprocessing

### Steps
1. **Git Setup**
   - Create a GitHub repository.
   - Include `.gitignore` and `requirements.txt`.
   - Work in `task-1` branch, commit frequently with meaningful messages.

2. **Web Scraping**
   - Use `google-play-scraper` to collect reviews, ratings, dates, and app names for the three banks.
   - Collect at least 400 reviews per bank.

3. **Preprocessing**
   - Remove duplicates and handle missing data.
   - Normalize dates (YYYY-MM-DD).
   - Save cleaned dataset as CSV with columns: `review`, `rating`, `date`, `bank`, `source`.

### KPIs
- Collect 1,200+ clean reviews.
- Maintain <5% missing data.
- Well-organized Git repo with clear commits.

---

## Task 2: Sentiment and Thematic Analysis
- **Sentiment Analysis:** Use libraries like VADER, TextBlob, or transformers (`distilbert-base-uncased-finetuned-sst-2-english`).
- **Thematic Analysis:** Extract keywords and cluster into themes like:
  - Account Access Issues
  - Transaction Performance
  - User Interface & Experience
  - Customer Support
  - Feature Requests
- Save results as CSV with review ID, text, sentiment, and themes.

---

## Task 3: PostgreSQL Database

### Steps
1. **Install PostgreSQL**
   - Download and install PostgreSQL from https://www.postgresql.org/download/
   - Note your PostgreSQL password (default user is `postgres`)

2. **Database Setup**
   - Run `python database_setup.py` to create database and tables
   - Or manually run `schema.sql` in PostgreSQL

3. **Insert Data**
   - Run `python insert_reviews.py` to insert cleaned review data
   - Script automatically handles sentiment and theme data if available

4. **Verify**
   - Run `python verify_database.py` to check data integrity

### Database Schema
- **Database:** `bank_reviews`
- **Tables:**
  - `banks`: `bank_id` (PK), `bank_name`, `app_name`, `created_at`
  - `reviews`: `review_id` (PK), `bank_id` (FK), `review_text`, `rating`, `review_date`, `sentiment_label`, `sentiment_score`, `theme`, `source`, `created_at`
- Uses `psycopg2` for database operations

---

## Task 4: Insights and Recommendations
- Identify 2+ **drivers** and **pain points** per bank.
- Create 3–5 visualizations (Matplotlib, Seaborn):
  - Sentiment trends
  - Rating distributions
  - Keyword clouds
- Provide practical app improvement suggestions.

---

## Technologies & Libraries
- Python: `pandas`, `google-play-scraper`, `dateutil`
- NLP & Sentiment: `TextBlob`, `VADER`, `transformers`, `spaCy`
- Database: PostgreSQL, `psycopg2`
- Visualization: Matplotlib, Seaborn
- Git & GitHub for version control
- Unit testing: `pytest`, `unittest`

---

## Project Structure

```
ethiopian-bank-reviews-analysis/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── data/                        # Data files
│   ├── raw/                     # Raw scraped data
│   │   └── ethiopian_bank_reviews.csv
│   ├── cleaned/                 # Cleaned/preprocessed data
│   │   └── cleaned_reviews.csv
│   └── processed/               # Processed data with sentiment/themes
│       ├── reviews_with_sentiment.csv
│       └── reviews_with_themes.csv
│
├── scripts/                      # Python scripts organized by task
│   ├── task1_data_collection/
│   │   ├── scrape_reviews.py    # Web scraping script
│   │   ├── preprocess_reviews.py # Data cleaning script
│   │   ├── find_app_id.py       # Helper script
│   │   └── test_boa_apps.py     # Testing script
│   │
│   ├── task2_analysis/
│   │   ├── sentiment_analysis.py # Sentiment analysis
│   │   └── thematic_analysis.py  # Theme extraction
│   │
│   └── task3_database/
│       ├── database_setup.py    # Database creation
│       ├── insert_reviews.py    # Data insertion
│       └── verify_database.py    # Verification queries
│
├── database/                    # Database files
│   └── schema.sql               # PostgreSQL schema
│
└── docs/                        # Documentation
    ├── TASK_REVIEW_SUMMARY.md
    ├── TASK3_SETUP_GUIDE.md
    └── Readmetask1.txt
```

## Getting Started

1. **Clone repository**
```bash
git clone <repo-url>
cd ethiopian-bank-reviews-analysis
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # For thematic analysis
```

3. **Run Task 1: Data Collection**
```bash
python scripts/task1_data_collection/scrape_reviews.py
python scripts/task1_data_collection/preprocess_reviews.py
```

4. **Run Task 2: Analysis**
```bash
python scripts/task2_analysis/sentiment_analysis.py
python scripts/task2_analysis/thematic_analysis.py
```

5. **Run Task 3: Database Setup**
```bash
python scripts/task3_database/database_setup.py
python scripts/task3_database/insert_reviews.py
python scripts/task3_database/verify_database.py
```