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
- **Database:** `bank_reviews`
- **Tables:**
  - `banks`: `bank_id` (PK), `bank_name`, `app_name`
  - `reviews`: `review_id` (PK), `bank_id` (FK), `review_text`, `rating`, `review_date`, `sentiment_label`, `sentiment_score`, `source`
- Use Python (`psycopg2` or SQLAlchemy) to insert cleaned data.

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

## Getting Started

1. **Clone repository**
```bash
git clone <repo-url>
cd <repo-folder>
Install dependencies

pip install -r requirements.txt


Run scraping and preprocessing script

python task1_scraper.py