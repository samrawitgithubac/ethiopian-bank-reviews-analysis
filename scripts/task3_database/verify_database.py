"""
Database Verification Script
Task 3 - Verify PostgreSQL Database Setup

This script runs SQL queries to verify data integrity and provides statistics.
"""

import psycopg2
import pandas as pd

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'bank_reviews'
}


def verify_database():
    """Run verification queries on the database."""
    print("=" * 60)
    print("DATABASE VERIFICATION")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("\n✅ Connected to database successfully\n")
    except psycopg2.Error as e:
        print(f"\n❌ Error connecting to database: {e}")
        return
    
    # Query 1: Count reviews per bank
    print("1. Reviews per bank:")
    print("-" * 60)
    cursor.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as review_count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_id, b.bank_name
        ORDER BY review_count DESC
    """)
    results = cursor.fetchall()
    for bank_name, count in results:
        print(f"   {bank_name}: {count} reviews")
    
    # Query 2: Average rating per bank
    print("\n2. Average rating per bank:")
    print("-" * 60)
    cursor.execute("""
        SELECT b.bank_name, AVG(r.rating) as avg_rating, COUNT(r.review_id) as count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        WHERE r.rating IS NOT NULL
        GROUP BY b.bank_id, b.bank_name
        ORDER BY avg_rating DESC
    """)
    results = cursor.fetchall()
    for bank_name, avg_rating, count in results:
        print(f"   {bank_name}: {avg_rating:.2f} ({count} reviews)")
    
    # Query 3: Rating distribution
    print("\n3. Overall rating distribution:")
    print("-" * 60)
    cursor.execute("""
        SELECT rating, COUNT(*) as count
        FROM reviews
        WHERE rating IS NOT NULL
        GROUP BY rating
        ORDER BY rating DESC
    """)
    results = cursor.fetchall()
    total = sum(count for _, count in results)
    for rating, count in results:
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"   {rating} stars: {count} ({percentage:.1f}%)")
    
    # Query 4: Sentiment distribution (if available)
    print("\n4. Sentiment distribution:")
    print("-" * 60)
    cursor.execute("""
        SELECT sentiment_label, COUNT(*) as count
        FROM reviews
        WHERE sentiment_label IS NOT NULL
        GROUP BY sentiment_label
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    if results:
        total = sum(count for _, count in results)
        for label, count in results:
            percentage = (count / total) * 100 if total > 0 else 0
            print(f"   {label}: {count} ({percentage:.1f}%)")
    else:
        print("   No sentiment data available")
    
    # Query 5: Theme distribution (if available)
    print("\n5. Theme distribution:")
    print("-" * 60)
    cursor.execute("""
        SELECT theme, COUNT(*) as count
        FROM reviews
        WHERE theme IS NOT NULL
        GROUP BY theme
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    if results:
        for theme, count in results:
            print(f"   {theme}: {count}")
    else:
        print("   No theme data available")
    
    # Query 6: Date range
    print("\n6. Review date range:")
    print("-" * 60)
    cursor.execute("""
        SELECT MIN(review_date) as min_date, MAX(review_date) as max_date, COUNT(*) as total
        FROM reviews
        WHERE review_date IS NOT NULL
    """)
    result = cursor.fetchone()
    if result and result[0]:
        print(f"   From: {result[0]}")
        print(f"   To: {result[1]}")
        print(f"   Total reviews: {result[2]}")
    
    # Query 7: Missing data check
    print("\n7. Data quality check:")
    print("-" * 60)
    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE review_text IS NULL OR review_text = ''")
    missing_text = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE rating IS NULL")
    missing_rating = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE review_date IS NULL")
    missing_date = cursor.fetchone()[0]
    
    print(f"   Total reviews: {total_reviews}")
    print(f"   Missing review text: {missing_text} ({missing_text/total_reviews*100:.1f}%)" if total_reviews > 0 else "   No reviews found")
    print(f"   Missing ratings: {missing_rating} ({missing_rating/total_reviews*100:.1f}%)" if total_reviews > 0 else "")
    print(f"   Missing dates: {missing_date} ({missing_date/total_reviews*100:.1f}%)" if total_reviews > 0 else "")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    verify_database()

