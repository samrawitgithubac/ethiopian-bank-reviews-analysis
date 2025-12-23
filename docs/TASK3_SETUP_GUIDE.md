# Task 3 Setup Guide - PostgreSQL Database

## Prerequisites

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - During installation, remember your PostgreSQL password (default user is `postgres`)
   - Make sure PostgreSQL service is running

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   This will install `psycopg2-binary` for PostgreSQL connectivity.

## Configuration

Before running the scripts, you may need to update the database credentials in:
- `database_setup.py`
- `insert_reviews.py`
- `verify_database.py`

Default configuration:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres',  # Change this to your PostgreSQL password
    'database': 'bank_reviews'
}
```

**Or** pass the password as a command-line argument:
```bash
python database_setup.py your_password
python insert_reviews.py your_password
```

## Step-by-Step Setup

### Step 1: Create Database and Tables

Run the database setup script:
```bash
python database_setup.py
```

This will:
- Create the `bank_reviews` database (if it doesn't exist)
- Create `banks` and `reviews` tables with proper schema
- Insert bank information
- Create indexes for better query performance

**Expected Output:**
```
============================================================
POSTGRESQL DATABASE SETUP
============================================================

📦 Creating database 'bank_reviews'...
   ✓ Database 'bank_reviews' created successfully

📦 Creating 'banks' table...
   ✓ 'banks' table created

📦 Creating 'reviews' table...
   ✓ 'reviews' table created

📦 Creating indexes...
   ✓ Indexes created

📦 Inserting bank information...
   ✓ Inserted Commercial Bank of Ethiopia (ID: 1)
   ✓ Inserted Bank of Abyssinia (ID: 2)
   ✓ Inserted Dashen Bank (ID: 3)
```

### Step 2: Insert Review Data

Run the insert script:
```bash
python insert_reviews.py
```

This will:
- Load review data from `reviews_with_themes.csv` (or `cleaned_reviews.csv` as fallback)
- Map bank names to bank_ids
- Insert reviews into the database
- Skip duplicates
- Verify data integrity

**Expected Output:**
```
============================================================
INSERTING REVIEWS INTO POSTGRESQL
============================================================

📥 Loading review data...
   ✓ Loaded 1200 reviews from reviews_with_themes.csv

🔌 Connecting to PostgreSQL database...
   ✓ Connected successfully

🔍 Getting bank ID mapping...
   ✓ Found 3 banks in database

💾 Inserting reviews into database...
   Processed 100/1200 reviews... (Inserted: 100, Skipped: 0)
   ...
   ✅ Insertion complete!
   Total processed: 1200
   Inserted: 1200
   Skipped (duplicates): 0
   Errors: 0
```

### Step 3: Verify Database

Run the verification script:
```bash
python verify_database.py
```

This will display:
- Reviews per bank
- Average ratings per bank
- Rating distribution
- Sentiment distribution (if available)
- Theme distribution (if available)
- Date range
- Data quality metrics

## Manual SQL Queries

You can also connect to PostgreSQL using `psql` or pgAdmin and run queries:

```sql
-- Connect to database
\c bank_reviews

-- Count reviews per bank
SELECT b.bank_name, COUNT(r.review_id) as review_count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
GROUP BY b.bank_id, b.bank_name
ORDER BY review_count DESC;

-- Average rating per bank
SELECT b.bank_name, AVG(r.rating) as avg_rating, COUNT(r.review_id) as count
FROM banks b
LEFT JOIN reviews r ON b.bank_id = r.bank_id
WHERE r.rating IS NOT NULL
GROUP BY b.bank_id, b.bank_name
ORDER BY avg_rating DESC;

-- Sentiment distribution
SELECT sentiment_label, COUNT(*) as count
FROM reviews
WHERE sentiment_label IS NOT NULL
GROUP BY sentiment_label
ORDER BY count DESC;
```

## Troubleshooting

### Error: "could not connect to server"
- Make sure PostgreSQL service is running
- Check if PostgreSQL is listening on port 5432
- Verify host and port in DB_CONFIG

### Error: "password authentication failed"
- Update the password in DB_CONFIG or pass it as command-line argument
- Default PostgreSQL user is `postgres`

### Error: "database does not exist"
- Run `database_setup.py` first to create the database

### Error: "relation does not exist"
- Run `database_setup.py` to create tables
- Or manually run `schema.sql`

### Error: "duplicate key value violates unique constraint"
- This is normal if you're re-running the scripts
- The scripts handle duplicates gracefully

## Schema Reference

### Banks Table
```sql
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Reviews Table
```sql
CREATE TABLE reviews (
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
);
```

## Next Steps

After completing Task 3:
1. ✅ Database is set up and populated
2. ✅ Data integrity verified
3. ➡️ Proceed to Task 4: Insights and Recommendations

