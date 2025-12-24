"""
Task 3: PostgreSQL Database Setup
Creates the database schema and tables for storing bank reviews.
Note: Assumes PostgreSQL is already installed and database 'bank_reviews' exists.
"""

import psycopg2
from psycopg2 import sql
import os
from pathlib import Path


def get_db_connection():
    """
    Create a connection to PostgreSQL database.
    Modify these credentials based on your PostgreSQL setup.
    """
    try:
        # Default PostgreSQL connection parameters
        # Modify these if your setup is different
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
        print("\n💡 Make sure:")
        print("   1. PostgreSQL is running")
        print("   2. Database 'bank_reviews' exists")
        print("   3. Credentials are correct")
        print("\n   You can set environment variables:")
        print("   - DB_HOST (default: localhost)")
        print("   - DB_PORT (default: 5432)")
        print("   - DB_NAME (default: bank_reviews)")
        print("   - DB_USER (default: postgres)")
        print("   - DB_PASSWORD (default: postgres)")
        raise


def create_schema(conn):
    """Create database schema from schema.sql file."""
    try:
        # Read schema.sql file
        schema_path = Path(__file__).parent.parent.parent / 'database' / 'schema.sql'
        
        if not schema_path.exists():
            print(f"❌ Schema file not found at: {schema_path}")
            return False
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolons and execute each statement
        cursor = conn.cursor()
        
        # Remove comments and split statements
        statements = [s.strip() for s in schema_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                except psycopg2.Error as e:
                    # Ignore "already exists" errors
                    if 'already exists' not in str(e).lower():
                        print(f"⚠️  Warning executing statement: {e}")
        
        conn.commit()
        cursor.close()
        print("✅ Database schema created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        conn.rollback()
        return False


def verify_tables(conn):
    """Verify that tables were created successfully."""
    try:
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('banks', 'reviews')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        cursor.close()
        
        if 'banks' in table_names and 'reviews' in table_names:
            print("✅ Both tables (banks, reviews) exist!")
            return True
        else:
            print(f"⚠️  Missing tables. Found: {table_names}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False


def main():
    """Main function to set up database."""
    print("=" * 70)
    print("PostgreSQL Database Setup - Task 3")
    print("=" * 70)
    
    conn = None
    try:
        # Connect to database
        print("\n1️⃣ Connecting to PostgreSQL database...")
        conn = get_db_connection()
        print("✅ Connected successfully!")
        
        # Create schema
        print("\n2️⃣ Creating database schema...")
        if create_schema(conn):
            # Verify tables
            print("\n3️⃣ Verifying tables...")
            verify_tables(conn)
            
            print("\n" + "=" * 70)
            print("✅ Database setup complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("  1. Run: python scripts/task3_database/insert_reviews.py")
            print("  2. Run: python scripts/task3_database/verify_database.py")
        else:
            print("\n❌ Schema creation failed. Please check the errors above.")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure PostgreSQL is installed and running")
        print("  2. Create database manually: CREATE DATABASE bank_reviews;")
        print("  3. Update connection credentials in this script")
        
    finally:
        if conn:
            conn.close()
            print("\n🔌 Database connection closed.")


if __name__ == '__main__':
    main()

