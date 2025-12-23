"""
Insert Reviews into PostgreSQL Database
Task 3 - Store Cleaned Data in PostgreSQL

This script:
- Reads cleaned review data (with sentiment and themes if available)
- Maps bank names to bank_ids
- Inserts reviews into the PostgreSQL database
- Verifies data integrity
"""

import psycopg2
import pandas as pd
import sys
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',  # Change this to your PostgreSQL password
    'database': 'bank_reviews'
}

# Bank name mapping (from CSV to database)
BANK_NAME_MAPPING = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'Dashen': 'Dashen Bank'
}


def get_bank_id_map(cursor):
    """Get mapping of bank names to bank_ids from database."""
    cursor.execute("SELECT bank_id, bank_name FROM banks")
    rows = cursor.fetchall()
    return {name: bank_id for bank_id, name in rows}


def insert_reviews(input_file="data/processed/reviews_with_themes.csv", fallback_file="data/cleaned/cleaned_reviews.csv"):
    """
    Insert reviews into PostgreSQL database.
    
    Args:
        input_file: Primary file to read (should have sentiment and themes)
        fallback_file: Fallback file if primary doesn't exist
    """
    print("=" * 60)
    print("INSERTING REVIEWS INTO POSTGRESQL")
    print("=" * 60)
    
    # Load data
    print(f"\n📥 Loading review data...")
    try:
        df = pd.read_csv(input_file)
        print(f"   ✓ Loaded {len(df)} reviews from {input_file}")
    except FileNotFoundError:
        print(f"   ⚠ {input_file} not found, trying {fallback_file}...")
        try:
            df = pd.read_csv(fallback_file)
            print(f"   ✓ Loaded {len(df)} reviews from {fallback_file}")
        except FileNotFoundError:
            print(f"   ❌ Error: Neither {input_file} nor {fallback_file} found!")
            print("   Please run preprocessing and analysis scripts first.")
            return False
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return False
    
    # Connect to database
    print(f"\n🔌 Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("   ✓ Connected successfully")
    except psycopg2.Error as e:
        print(f"   ❌ Error connecting to database: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure PostgreSQL is running")
        print("   2. Check database credentials in DB_CONFIG")
        print("   3. Make sure database 'bank_reviews' exists (run database_setup.py)")
        return False
    
    # Get bank_id mapping
    print(f"\n🔍 Getting bank ID mapping...")
    bank_id_map = get_bank_id_map(cursor)
    print(f"   ✓ Found {len(bank_id_map)} banks in database")
    
    # Map bank names from CSV to database names
    if 'bank' in df.columns:
        df['bank_name'] = df['bank'].map(BANK_NAME_MAPPING)
        df['bank_name'] = df['bank_name'].fillna(df['bank'])  # Use original if not in mapping
    
    # Check if we have required columns
    required_cols = ['review_text', 'rating', 'date', 'bank_name']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"   ❌ Missing required columns: {missing_cols}")
        return False
    
    # Prepare data for insertion
    print(f"\n📦 Preparing data for insertion...")
    
    # Check if sentiment columns exist
    has_sentiment = 'sentiment_label' in df.columns and 'sentiment_score' in df.columns
    has_theme = 'theme' in df.columns
    
    if has_sentiment:
        print("   ✓ Sentiment data found")
    else:
        print("   ⚠ No sentiment data - will insert NULL values")
    
    if has_theme:
        print("   ✓ Theme data found")
    else:
        print("   ⚠ No theme data - will insert NULL values")
    
    # Check for review_id column
    if 'review_id' not in df.columns:
        df['review_id'] = range(1, len(df) + 1)
    
    # Insert reviews
    print(f"\n💾 Inserting reviews into database...")
    
    inserted_count = 0
    skipped_count = 0
    error_count = 0
    
    for idx, row in df.iterrows():
        try:
            # Get bank_id
            bank_name = row['bank_name']
            if bank_name not in bank_id_map:
                print(f"   ⚠ Warning: Bank '{bank_name}' not found in database, skipping review {idx+1}")
                skipped_count += 1
                continue
            
            bank_id = bank_id_map[bank_name]
            
            # Prepare values
            review_text = str(row['review_text']) if pd.notna(row['review_text']) else ''
            rating = int(row['rating']) if pd.notna(row['rating']) else None
            review_date = pd.to_datetime(row['date']).date() if pd.notna(row['date']) else None
            
            sentiment_label = row.get('sentiment_label') if has_sentiment else None
            sentiment_score = float(row.get('sentiment_score')) if has_sentiment and pd.notna(row.get('sentiment_score')) else None
            theme = row.get('theme') if has_theme else None
            source = row.get('source', 'Google Play')
            
            # Check if review already exists (by review_text and bank_id)
            cursor.execute("""
                SELECT review_id FROM reviews 
                WHERE review_text = %s AND bank_id = %s
            """, (review_text[:500], bank_id))  # Limit text length for comparison
            
            if cursor.fetchone():
                skipped_count += 1
                continue
            
            # Insert review
            cursor.execute("""
                INSERT INTO reviews (
                    bank_id, review_text, rating, review_date,
                    sentiment_label, sentiment_score, theme, source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bank_id, review_text, rating, review_date,
                sentiment_label, sentiment_score, theme, source
            ))
            
            inserted_count += 1
            
            if (idx + 1) % 100 == 0:
                print(f"   Processed {idx + 1}/{len(df)} reviews... (Inserted: {inserted_count}, Skipped: {skipped_count})")
                conn.commit()  # Commit in batches
            
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Print first 5 errors
                print(f"   ⚠ Error inserting review {idx+1}: {e}")
            continue
    
    # Final commit
    conn.commit()
    
    print(f"\n✅ Insertion complete!")
    print(f"   Total processed: {len(df)}")
    print(f"   Inserted: {inserted_count}")
    print(f"   Skipped (duplicates): {skipped_count}")
    print(f"   Errors: {error_count}")
    
    # Verify data integrity
    print(f"\n🔍 Verifying data integrity...")
    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cursor.fetchone()[0]
    print(f"   ✓ Total reviews in database: {total_reviews}")
    
    cursor.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as review_count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_id, b.bank_name
        ORDER BY b.bank_name
    """)
    bank_counts = cursor.fetchall()
    print(f"\n   Reviews per bank:")
    for bank_name, count in bank_counts:
        print(f"     {bank_name}: {count}")
    
    cursor.execute("SELECT AVG(rating) FROM reviews WHERE rating IS NOT NULL")
    avg_rating = cursor.fetchone()[0]
    print(f"\n   Average rating: {avg_rating:.2f}")
    
    if has_sentiment:
        cursor.execute("""
            SELECT sentiment_label, COUNT(*) 
            FROM reviews 
            WHERE sentiment_label IS NOT NULL
            GROUP BY sentiment_label
        """)
        sentiment_counts = cursor.fetchall()
        print(f"\n   Sentiment distribution:")
        for label, count in sentiment_counts:
            print(f"     {label}: {count}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Data insertion and verification complete!")
    return True


if __name__ == "__main__":
    # Check if user wants to update password
    if len(sys.argv) > 1:
        DB_CONFIG['password'] = sys.argv[1]
    
    # Check if custom input file provided
    input_file = sys.argv[2] if len(sys.argv) > 2 else "reviews_with_themes.csv"
    
    success = insert_reviews(input_file=input_file)
    if not success:
        print("\n❌ Failed to insert reviews. Please check the errors above.")
        sys.exit(1)

