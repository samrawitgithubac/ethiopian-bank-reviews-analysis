"""
Task 3: Insert Review Data into PostgreSQL
Reads cleaned review data and inserts it into the PostgreSQL database.
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os
from pathlib import Path
from datetime import datetime


def get_db_connection():
    """Create a connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'bank_reviews'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')  # Change this to your password
        )
        return conn
    except psycopg2.Error as e:
        print(f"❌ Error connecting to database: {e}")
        raise


def get_bank_ids(conn):
    """Get bank_id mapping from bank names."""
    cursor = conn.cursor()
    cursor.execute("SELECT bank_id, bank_name FROM banks;")
    bank_mapping = {row[1]: row[0] for row in cursor.fetchall()}
    cursor.close()
    return bank_mapping


def load_review_data():
    """Load processed review data with themes."""
    data_path = Path(__file__).parent.parent.parent / 'data' / 'processed' / 'reviews_with_themes.csv'
    
    if not data_path.exists():
        raise FileNotFoundError(f"Review data not found at: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✅ Loaded {len(df)} reviews from CSV")
    return df


def insert_reviews(conn, df, bank_mapping, batch_size=100):
    """
    Insert reviews into the database.
    Uses batch insert for better performance.
    """
    cursor = conn.cursor()
    
    # Prepare data for insertion
    insert_query = """
        INSERT INTO reviews (
            bank_id, review_text, rating, review_date,
            sentiment_label, sentiment_score, theme, source
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
    """
    
    records = []
    skipped = 0
    
    for _, row in df.iterrows():
        bank_name = row['bank']
        
        # Map bank name to bank_id
        if bank_name not in bank_mapping:
            print(f"⚠️  Warning: Bank '{bank_name}' not found in database. Skipping review.")
            skipped += 1
            continue
        
        bank_id = bank_mapping[bank_name]
        
        # Prepare record
        record = (
            bank_id,
            str(row['review_text'])[:10000],  # Limit text length
            int(row['rating']) if pd.notna(row['rating']) else None,
            pd.to_datetime(row['date']).date() if pd.notna(row['date']) else None,
            str(row['sentiment_label']) if pd.notna(row['sentiment_label']) else None,
            float(row['sentiment_score']) if pd.notna(row['sentiment_score']) else None,
            str(row['theme']) if pd.notna(row['theme']) else None,
            str(row.get('source', 'Google Play'))
        )
        
        records.append(record)
    
    # Batch insert
    try:
        execute_batch(cursor, insert_query, records, page_size=batch_size)
        conn.commit()
        
        inserted_count = len(records) - skipped
        print(f"✅ Successfully inserted {inserted_count} reviews")
        if skipped > 0:
            print(f"⚠️  Skipped {skipped} reviews (bank not found)")
        
        return inserted_count
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"❌ Error inserting reviews: {e}")
        raise
    finally:
        cursor.close()


def check_existing_reviews(conn):
    """Check if reviews already exist in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews;")
    count = cursor.fetchone()[0]
    cursor.close()
    return count


def main():
    """Main function to insert review data."""
    print("=" * 70)
    print("Insert Review Data into PostgreSQL - Task 3")
    print("=" * 70)
    
    conn = None
    try:
        # Connect to database
        print("\n1️⃣ Connecting to database...")
        conn = get_db_connection()
        print("✅ Connected!")
        
        # Check existing reviews
        existing_count = check_existing_reviews(conn)
        if existing_count > 0:
            print(f"\n⚠️  Warning: Database already contains {existing_count} reviews")
            response = input("Do you want to continue? (y/n): ").strip().lower()
            if response != 'y':
                print("❌ Insertion cancelled.")
                return
        
        # Get bank mappings
        print("\n2️⃣ Loading bank information...")
        bank_mapping = get_bank_ids(conn)
        print(f"✅ Found {len(bank_mapping)} banks: {list(bank_mapping.keys())}")
        
        # Load review data
        print("\n3️⃣ Loading review data from CSV...")
        df = load_review_data()
        
        # Insert reviews
        print("\n4️⃣ Inserting reviews into database...")
        inserted_count = insert_reviews(conn, df, bank_mapping)
        
        # Verify insertion
        final_count = check_existing_reviews(conn)
        print(f"\n✅ Total reviews in database: {final_count}")
        
        print("\n" + "=" * 70)
        print("✅ Data insertion complete!")
        print("=" * 70)
        print("\nNext step:")
        print("  Run: python scripts/task3_database/verify_database.py")
        
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
        print("\n💡 Make sure you've run Task 2 to generate reviews_with_themes.csv")
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\n💡 Make sure:")
        print("  1. Database 'bank_reviews' exists")
        print("  2. Tables 'banks' and 'reviews' are created")
        print("  3. Connection credentials are correct")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        
    finally:
        if conn:
            conn.close()
            print("\n🔌 Database connection closed.")


if __name__ == '__main__':
    main()

