"""
Data Processing Module
Handles web scraping and data preprocessing for Ethiopian Bank Reviews
"""

import pandas as pd
import os
from google_play_scraper import reviews, Sort, app
import time


def scrape_reviews(output_file="data/raw/ethiopian_bank_reviews.csv"):
    """
    Scrape reviews from Google Play Store for Ethiopian banks.
    
    Args:
        output_file: Path to save scraped reviews CSV
        
    Returns:
        DataFrame with scraped reviews
    """
    from google_play_scraper import reviews, Sort, app
    
    # App IDs for Ethiopian banks
    APPS = {
        "CBE": ["com.combanketh.mobilebanking", "com.cbe.eBanking"],
        "BOA": ["com.boa.boaMobileBanking", "com.ambel.mobile.android"],
        "Dashen": ["com.cr2.amolelight", "com.dashen.mobilebanking", "com.dashenbank.mwallet"]
    }
    
    def scrape_bank_reviews(bank_name, app_id, total=400):
        """Scrape reviews for a single bank."""
        print(f"\n🔍 Scraping {bank_name} (App ID: {app_id})...")
        all_reviews = []
        token = None
        batch_size = 200
        attempts = 0
        max_attempts = 10

        while len(all_reviews) < total and attempts < max_attempts:
            try:
                if token is None:
                    result, token = reviews(
                        app_id, lang='en', country='us',
                        sort=Sort.NEWEST, count=batch_size
                    )
                else:
                    result, token = reviews(
                        app_id, lang='en', country='us',
                        sort=Sort.NEWEST, count=batch_size,
                        continuation_token=token
                    )
                
                attempts += 1
                if not result or len(result) == 0:
                    break

                for r in result:
                    all_reviews.append({
                        "content": r.get("content", ""),
                        "score": r.get("score", None),
                        "at": r.get("at", None),
                        "bank": bank_name,
                        "source": "Google Play"
                    })

                time.sleep(2)
                if token is None:
                    break
            except Exception as e:
                print(f"⚠ Error: {e}")
                break

        print(f"✅ Finished: {bank_name} → {len(all_reviews)} reviews")
        return all_reviews
    
    # Scrape all banks
    all_data = []
    for bank, app_id_list in APPS.items():
        app_id = app_id_list[0] if isinstance(app_id_list, list) else app_id_list
        bank_reviews = scrape_bank_reviews(bank, app_id, total=400)
        if bank_reviews:
            all_data.extend(bank_reviews)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(all_data)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"\n✅ Data saved to: {output_file}")
    return df


def preprocess_reviews(input_file="data/raw/ethiopian_bank_reviews.csv", 
                      output_file="data/cleaned/cleaned_reviews.csv"):
    """
    Preprocess scraped reviews data.
    
    Args:
        input_file: Path to raw scraped reviews CSV
        output_file: Path to save cleaned reviews CSV
        
    Returns:
        DataFrame with cleaned reviews
    """
    print("=" * 60)
    print("REVIEWS PREPROCESSING")
    print("=" * 60)
    
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    
    # Load data
    print(f"\n📥 Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        print(f"   ✓ Loaded {len(df)} rows")
    except FileNotFoundError:
        print(f"   ❌ Error: {input_file} not found!")
        return None
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return None
    
    initial_count = len(df)
    
    # Remove duplicates
    print(f"\n🔍 Removing duplicates...")
    df = df.drop_duplicates()
    
    # Remove empty reviews
    print(f"🔍 Removing empty reviews...")
    df = df.dropna(subset=['content'])
    df = df[df['content'].astype(str).str.strip() != '']
    
    # Normalize dates
    print(f"🔍 Normalizing dates...")
    df['at'] = pd.to_datetime(df['at'], errors='coerce')
    df['date'] = df['at'].dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['date'])
    
    # Rename columns
    df_cleaned = df[['content', 'score', 'date', 'bank', 'source']].copy()
    df_cleaned = df_cleaned.rename(columns={
        'content': 'review_text',
        'score': 'rating'
    })
    
    # Validate ratings
    df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce')
    df_cleaned = df_cleaned.dropna(subset=['rating'])
    
    # Save
    df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Preprocessing complete!")
    print(f"   Original: {initial_count} rows")
    print(f"   Final: {len(df_cleaned)} rows")
    
    return df_cleaned
