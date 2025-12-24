"""
Task 3: Verify Database Integrity
Runs SQL queries to verify data integrity and completeness.
"""

import psycopg2
import os
from tabulate import tabulate


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


def verify_review_count(conn):
    """Verify total review count."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews;")
    count = cursor.fetchone()[0]
    cursor.close()
    return count


def verify_reviews_per_bank(conn):
    """Count reviews per bank."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.bank_name,
            COUNT(r.review_id) as review_count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_id, b.bank_name
        ORDER BY review_count DESC;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    return results


def verify_average_rating(conn):
    """Calculate average rating per bank."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.bank_name,
            ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
            COUNT(r.review_id) as review_count
        FROM banks b
        LEFT JOIN reviews r ON b.bank_id = r.bank_id
        WHERE r.rating IS NOT NULL
        GROUP BY b.bank_id, b.bank_name
        ORDER BY avg_rating DESC;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    return results


def verify_sentiment_distribution(conn):
    """Check sentiment label distribution."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            sentiment_label,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews WHERE sentiment_label IS NOT NULL), 2) as percentage
        FROM reviews
        WHERE sentiment_label IS NOT NULL
        GROUP BY sentiment_label
        ORDER BY count DESC;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    return results


def verify_theme_distribution(conn):
    """Check theme distribution."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            theme,
            COUNT(*) as count
        FROM reviews
        WHERE theme IS NOT NULL
        GROUP BY theme
        ORDER BY count DESC
        LIMIT 10;
    """)
    
    results = cursor.fetchall()
    cursor.close()
    return results


def verify_data_completeness(conn):
    """Check data completeness (missing values)."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_reviews,
            COUNT(review_text) as has_text,
            COUNT(rating) as has_rating,
            COUNT(review_date) as has_date,
            COUNT(sentiment_label) as has_sentiment,
            COUNT(sentiment_score) as has_sentiment_score,
            COUNT(theme) as has_theme
        FROM reviews;
    """)
    
    result = cursor.fetchone()
    cursor.close()
    
    total = result[0]
    completeness = {
        'review_text': (result[1], result[1] / total * 100 if total > 0 else 0),
        'rating': (result[2], result[2] / total * 100 if total > 0 else 0),
        'review_date': (result[3], result[3] / total * 100 if total > 0 else 0),
        'sentiment_label': (result[4], result[4] / total * 100 if total > 0 else 0),
        'sentiment_score': (result[5], result[5] / total * 100 if total > 0 else 0),
        'theme': (result[6], result[6] / total * 100 if total > 0 else 0)
    }
    
    return total, completeness


def verify_date_range(conn):
    """Check review date range."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            MIN(review_date) as earliest_date,
            MAX(review_date) as latest_date,
            COUNT(DISTINCT review_date) as unique_dates
        FROM reviews
        WHERE review_date IS NOT NULL;
    """)
    
    result = cursor.fetchone()
    cursor.close()
    return result


def main():
    """Main function to verify database integrity."""
    print("=" * 70)
    print("Database Integrity Verification - Task 3")
    print("=" * 70)
    
    conn = None
    try:
        # Connect to database
        print("\n1️⃣ Connecting to database...")
        conn = get_db_connection()
        print("✅ Connected!")
        
        # 1. Total review count
        print("\n2️⃣ Verifying total review count...")
        total_reviews = verify_review_count(conn)
        print(f"   Total Reviews: {total_reviews}")
        
        if total_reviews < 400:
            print(f"   ⚠️  Warning: Less than 400 reviews (minimum requirement)")
        elif total_reviews >= 1000:
            print(f"   ✅ Meets KPI requirement (>1,000 reviews)")
        else:
            print(f"   ✅ Meets minimum requirement (≥400 reviews)")
        
        # 2. Reviews per bank
        print("\n3️⃣ Reviews per bank:")
        reviews_per_bank = verify_reviews_per_bank(conn)
        table_data = [[row[0], row[1]] for row in reviews_per_bank]
        print(tabulate(table_data, headers=['Bank', 'Review Count'], tablefmt='grid'))
        
        # 3. Average rating per bank
        print("\n4️⃣ Average rating per bank:")
        avg_ratings = verify_average_rating(conn)
        table_data = [[row[0], row[1], row[2]] for row in avg_ratings]
        print(tabulate(table_data, headers=['Bank', 'Avg Rating', 'Count'], tablefmt='grid'))
        
        # 4. Sentiment distribution
        print("\n5️⃣ Sentiment distribution:")
        sentiment_dist = verify_sentiment_distribution(conn)
        table_data = [[row[0], row[1], f"{row[2]}%"] for row in sentiment_dist]
        print(tabulate(table_data, headers=['Sentiment', 'Count', 'Percentage'], tablefmt='grid'))
        
        # 5. Theme distribution (top 10)
        print("\n6️⃣ Top 10 themes:")
        theme_dist = verify_theme_distribution(conn)
        table_data = [[row[0], row[1]] for row in theme_dist]
        print(tabulate(table_data, headers=['Theme', 'Count'], tablefmt='grid'))
        
        # 6. Data completeness
        print("\n7️⃣ Data completeness:")
        total, completeness = verify_data_completeness(conn)
        table_data = [[field, count, f"{pct:.1f}%"] for field, (count, pct) in completeness.items()]
        print(tabulate(table_data, headers=['Field', 'Count', 'Percentage'], tablefmt='grid'))
        
        # 7. Date range
        print("\n8️⃣ Review date range:")
        date_range = verify_date_range(conn)
        if date_range[0]:
            print(f"   Earliest Date: {date_range[0]}")
            print(f"   Latest Date: {date_range[1]}")
            print(f"   Unique Dates: {date_range[2]}")
        
        # Summary
        print("\n" + "=" * 70)
        print("✅ Verification Complete!")
        print("=" * 70)
        
        # Check KPIs
        print("\n📊 KPI Status:")
        kpi_met = True
        
        if total_reviews >= 1000:
            print("   ✅ Total reviews ≥ 1,000 (KPI met)")
        else:
            print(f"   ⚠️  Total reviews: {total_reviews} (KPI: ≥1,000)")
            if total_reviews >= 400:
                print("   ✅ Meets minimum requirement (≥400)")
            else:
                print("   ❌ Below minimum requirement")
                kpi_met = False
        
        # Check data quality
        min_completeness = min([pct for _, pct in completeness.values()])
        if min_completeness >= 95:
            print(f"   ✅ Data completeness: {min_completeness:.1f}% (≥95%)")
        else:
            print(f"   ⚠️  Data completeness: {min_completeness:.1f}% (target: ≥95%)")
        
        if kpi_met:
            print("\n🎉 All requirements met!")
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\n💡 Make sure:")
        print("  1. Database is set up (run database_setup.py)")
        print("  2. Data is inserted (run insert_reviews.py)")
        print("  3. Connection credentials are correct")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        
    finally:
        if conn:
            conn.close()
            print("\n🔌 Database connection closed.")


if __name__ == '__main__':
    main()

