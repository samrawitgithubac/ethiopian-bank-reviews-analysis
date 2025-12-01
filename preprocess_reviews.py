"""
Preprocessing script for Ethiopian Bank Reviews
Task 1 - Data Collection & Preprocessing

This script:
- Removes duplicate reviews
- Drops empty or missing review text
- Converts dates to YYYY-MM-DD format
- Renames columns to match requirements
- Saves cleaned data to cleaned_reviews.csv
"""

import pandas as pd
from datetime import datetime

def preprocess_reviews(input_file="ethiopian_bank_reviews.csv", output_file="cleaned_reviews.csv"):
    """
    Preprocess the scraped reviews data.
    
    Args:
        input_file: Path to the raw scraped reviews CSV
        output_file: Path to save the cleaned reviews CSV
    """
    print("=" * 60)
    print("REVIEWS PREPROCESSING")
    print("=" * 60)
    
    # Load the data
    print(f"\n📥 Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        print(f"   ✓ Loaded {len(df)} rows")
    except FileNotFoundError:
        print(f"   ❌ Error: {input_file} not found!")
        print("   Please run scrape_reviews.py first to generate the data.")
        return
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return
    
    print(f"\n📊 Original data shape: {df.shape}")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
    
    # Step 1: Remove duplicates
    print(f"\n🔍 Step 1: Removing duplicates...")
    initial_count = len(df)
    df = df.drop_duplicates()
    duplicates_removed = initial_count - len(df)
    print(f"   ✓ Removed {duplicates_removed} duplicate rows")
    print(f"   Remaining: {len(df)} rows")
    
    # Step 2: Drop rows with empty or missing review text
    print(f"\n🔍 Step 2: Removing empty or missing review text...")
    before_drop = len(df)
    df = df.dropna(subset=['content'])  # Drop rows where content is NaN
    df = df[df['content'].astype(str).str.strip() != '']  # Drop empty strings
    after_drop = len(df)
    empty_removed = before_drop - after_drop
    print(f"   ✓ Removed {empty_removed} rows with empty/missing review text")
    print(f"   Remaining: {len(df)} rows")
    
    # Step 3: Convert dates to YYYY-MM-DD format
    print(f"\n🔍 Step 3: Converting dates to YYYY-MM-DD format...")
    try:
        # Convert 'at' column to datetime, then format to YYYY-MM-DD
        df['at'] = pd.to_datetime(df['at'], errors='coerce')
        df['date'] = df['at'].dt.strftime('%Y-%m-%d')
        
        # Drop rows where date conversion failed
        date_failed = df['date'].isna().sum()
        if date_failed > 0:
            print(f"   ⚠ Warning: {date_failed} rows have invalid dates and will be removed")
            df = df.dropna(subset=['date'])
        
        print(f"   ✓ Dates converted successfully")
        print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    except Exception as e:
        print(f"   ❌ Error converting dates: {e}")
        return
    
    # Step 4: Rename columns to match requirements
    print(f"\n🔍 Step 4: Renaming columns...")
    column_mapping = {
        'content': 'review_text',
        'score': 'rating',
        'date': 'date',  # Already renamed in step 3
        'bank': 'bank',
        'source': 'source'
    }
    
    # Keep only the required columns and rename
    df_cleaned = df[['content', 'score', 'date', 'bank', 'source']].copy()
    df_cleaned = df_cleaned.rename(columns=column_mapping)
    
    # Ensure rating is numeric
    df_cleaned['rating'] = pd.to_numeric(df_cleaned['rating'], errors='coerce')
    
    # Drop rows with invalid ratings
    invalid_ratings = df_cleaned['rating'].isna().sum()
    if invalid_ratings > 0:
        print(f"   ⚠ Warning: {invalid_ratings} rows have invalid ratings and will be removed")
        df_cleaned = df_cleaned.dropna(subset=['rating'])
    
    print(f"   ✓ Columns renamed:")
    print(f"     {', '.join(df_cleaned.columns.tolist())}")
    
    # Step 5: Final data quality check
    print(f"\n📊 Final data quality check:")
    print(f"   Total rows: {len(df_cleaned)}")
    print(f"   Missing values:")
    for col in df_cleaned.columns:
        missing = df_cleaned[col].isna().sum()
        if missing > 0:
            print(f"     - {col}: {missing} missing values")
        else:
            print(f"     - {col}: ✓ No missing values")
    
    # Check rating distribution
    print(f"\n   Rating distribution:")
    rating_counts = df_cleaned['rating'].value_counts().sort_index()
    for rating, count in rating_counts.items():
        print(f"     {int(rating)} stars: {count} reviews")
    
    # Check bank distribution
    print(f"\n   Reviews per bank:")
    bank_counts = df_cleaned['bank'].value_counts()
    for bank, count in bank_counts.items():
        print(f"     {bank}: {count} reviews")
    
    # Step 6: Save cleaned data
    print(f"\n💾 Saving cleaned data to {output_file}...")
    try:
        df_cleaned.to_csv(output_file, index=False, encoding='utf-8')
        print(f"   ✓ Successfully saved {len(df_cleaned)} rows to {output_file}")
    except Exception as e:
        print(f"   ❌ Error saving file: {e}")
        return
    
    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE!")
    print("=" * 60)
    print(f"\n✅ Summary:")
    print(f"   Original rows: {initial_count}")
    print(f"   Final rows: {len(df_cleaned)}")
    print(f"   Rows removed: {initial_count - len(df_cleaned)}")
    print(f"   Data quality: {len(df_cleaned)/initial_count*100:.1f}% of data retained")
    
    return df_cleaned

if __name__ == "__main__":
    preprocess_reviews()

