"""
PostgreSQL Database Setup Script
Task 3 - Store Cleaned Data in PostgreSQL

This script:
- Creates the bank_reviews database (if it doesn't exist)
- Creates banks and reviews tables with proper schema
- Inserts bank information
- Provides functions to insert review data
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import sql
import pandas as pd
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',  # Default PostgreSQL user
    'password': 'postgres',  # Change this to your PostgreSQL password
    'database': 'postgres'  # Connect to default database first
}

TARGET_DB = 'bank_reviews'

# Bank information
BANKS_DATA = [
    {
        'bank_name': 'Commercial Bank of Ethiopia',
        'app_name': 'Commercial Bank of Ethiopia Mobile'
    },
    {
        'bank_name': 'Bank of Abyssinia',
        'app_name': 'BoA Mobile'
    },
    {
        'bank_name': 'Dashen Bank',
        'app_name': 'Dashen Mobile'
    }
]


def create_database():
    """Create the bank_reviews database if it doesn't exist."""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (TARGET_DB,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            print(f"📦 Creating database '{TARGET_DB}'...")
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(TARGET_DB)
            ))
            print(f"   ✓ Database '{TARGET_DB}' created successfully")
        else:
            print(f"   ✓ Database '{TARGET_DB}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"   ❌ Error creating database: {e}")
        return False


def create_tables():
    """Create banks and reviews tables."""
    try:
        # Connect to bank_reviews database
        config = DB_CONFIG.copy()
        config['database'] = TARGET_DB
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Create banks table
        print("\n📦 Creating 'banks' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(100) NOT NULL UNIQUE,
                app_name VARCHAR(200) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✓ 'banks' table created")
        
        # Create reviews table
        print("\n📦 Creating 'reviews' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INTEGER NOT NULL,
                review_text TEXT NOT NULL,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                review_date DATE NOT NULL,
                sentiment_label VARCHAR(20),
                sentiment_score DECIMAL(5, 4),
                theme VARCHAR(100),
                source VARCHAR(50) DEFAULT 'Google Play',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bank_id) REFERENCES banks(bank_id) ON DELETE CASCADE
            )
        """)
        print("   ✓ 'reviews' table created")
        
        # Create indexes for better query performance
        print("\n📦 Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date)")
        print("   ✓ Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"   ❌ Error creating tables: {e}")
        return False


def insert_banks():
    """Insert bank information into the banks table."""
    try:
        config = DB_CONFIG.copy()
        config['database'] = TARGET_DB
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        print("\n📦 Inserting bank information...")
        
        bank_id_map = {}
        
        for bank_data in BANKS_DATA:
            # Check if bank already exists
            cursor.execute(
                "SELECT bank_id FROM banks WHERE bank_name = %s",
                (bank_data['bank_name'],)
            )
            existing = cursor.fetchone()
            
            if existing:
                bank_id = existing[0]
                print(f"   ✓ {bank_data['bank_name']} already exists (ID: {bank_id})")
            else:
                cursor.execute("""
                    INSERT INTO banks (bank_name, app_name)
                    VALUES (%s, %s)
                    RETURNING bank_id
                """, (bank_data['bank_name'], bank_data['app_name']))
                bank_id = cursor.fetchone()[0]
                print(f"   ✓ Inserted {bank_data['bank_name']} (ID: {bank_id})")
            
            bank_id_map[bank_data['bank_name']] = bank_id
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return bank_id_map
        
    except psycopg2.Error as e:
        print(f"   ❌ Error inserting banks: {e}")
        return None


def setup_database():
    """Main function to set up the database."""
    print("=" * 60)
    print("POSTGRESQL DATABASE SETUP")
    print("=" * 60)
    
    print("\n⚠ Note: Make sure PostgreSQL is running and credentials are correct.")
    print(f"   Current config: host={DB_CONFIG['host']}, user={DB_CONFIG['user']}")
    
    # Step 1: Create database
    if not create_database():
        print("\n❌ Failed to create database. Please check PostgreSQL connection.")
        return False
    
    # Step 2: Create tables
    if not create_tables():
        print("\n❌ Failed to create tables.")
        return False
    
    # Step 3: Insert banks
    bank_id_map = insert_banks()
    if bank_id_map is None:
        print("\n❌ Failed to insert banks.")
        return False
    
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE!")
    print("=" * 60)
    print(f"\n✅ Database '{TARGET_DB}' is ready")
    print(f"✅ Tables created: banks, reviews")
    print(f"✅ Banks inserted: {len(bank_id_map)}")
    
    return True, bank_id_map


if __name__ == "__main__":
    # Check if user wants to update password
    if len(sys.argv) > 1:
        DB_CONFIG['password'] = sys.argv[1]
    
    success, bank_id_map = setup_database()
    if success:
        print("\n💡 Next step: Run insert_reviews.py to populate the reviews table")
    else:
        print("\n❌ Database setup failed. Please check the errors above.")

