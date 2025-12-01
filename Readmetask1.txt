Task 1 — Data Collection & Preprocessing (Week 2 Challenge)
Customer Experience Analytics for Fintech Apps — Google Play Review Scraping

This repository contains the implementation for Task 1 of the Week 2 Omega Consultancy Data Challenge.
The goal of this task is to scrape Google Play Store reviews for three Ethiopian banking apps, clean the data, and prepare it for sentiment and thematic analysis.

🚀 1. Objective

The main goal of Task 1 is to:

✔ Scrape 400+ reviews per bank from Google Play
✔ Preprocess and clean the dataset
✔ Save a combined CSV file with all banks
✔ Maintain clean Git workflow (task-1 branch)

This task lays the foundation for Task 2 (NLP), Task 3 (Database), and Task 4 (Insights).

🏦 2. Target Banking Apps

We scrape reviews for the following banks:

Bank	Google Play App Name	Example Package ID
Commercial Bank of Ethiopia	CBE Mobile Banking	com.cbe.eBanking
Bank of Abyssinia	BOA Mobile Banking	com.bankOfAbyssinia.mobilebanking
Dashen Bank	Amole / Dashen Mobile Banking	com.dashen.mobilebanking

📌 Exact package IDs may differ — verify from Google Play Store before scraping.

🛠️ 3. Technologies Used
Tool	Purpose
google-play-scraper	Scraping reviews
Python	Main programming language
Pandas	Data cleaning & preprocessing
Git & GitHub	Version control
Virtual Environment	Dependency isolation
📦 4. Project Setup
4.1 Clone the Repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

4.2 Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

4.3 Install Dependencies
pip install -r requirements.txt

4.4 Install Scraper
pip install google-play-scraper

📥 5. Scraping Script

The main script for scraping reviews is:

📄 scrape_reviews.py

This script:

✔ Scrapes reviews (ratings, dates, content)
✔ Saves data to Pandas DataFrame
✔ Adds an additional column bank
✔ Merges all banks into one CSV file

Example code block used:
from google_play_scraper import reviews
import pandas as pd

def scrape_bank(app_id, bank_name, count=500):
    data, _ = reviews(
        app_id,
        lang="en",
        country="us",
        count=count,
        sort=reviews.Sort.NEWEST
    )

    df = pd.DataFrame(data)
    df["bank"] = bank_name
    df["source"] = "Google Play"

    return df

🧹 6. Preprocessing Steps

The cleaning script is located in:

📄 preprocess_reviews.py

Cleaning Includes:

✔ Remove duplicate reviews
✔ Drop empty or missing review text
✔ Convert dates to format YYYY-MM-DD
✔ Keep relevant columns only:

review_text  
rating  
date  
bank  
source  

📁 7. Output Files

The final cleaned dataset is saved as:

📄 cleaned_reviews.csv

This file contains:

Column	Description
review	The review text
rating	Star rating (1–5)
date	Normalized date
bank	Bank name
source	“Google Play”

Minimum rows required → 1200+ reviews.

🔀 8. Git Workflow for Task 1

Work was done on a dedicated branch:

git checkout -b task-1


After completing scraping + preprocessing:

git add .
git commit -m "Completed Task 1 - scraping and preprocessing"
git push origin task-1


Then a Pull Request was created and merged to main.

✅ 9. Deliverables Completed
✔ GitHub repo created
✔ Clean folder structure
✔ Scraper implemented
✔ Preprocessing completed
✔ Clean CSV generated
✔ README updated
📚 10. How to Run Entire Task 1
python scrape_reviews.py
python preprocess_reviews.py


This will generate:

raw_reviews.csv
cleaned_reviews.csv