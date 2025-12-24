# Task 3: PostgreSQL Database Setup Guide

## Overview

This guide helps you complete Task 3: Store Cleaned Data in PostgreSQL. The scripts automate the database setup, data insertion, and verification processes.

## Prerequisites

1. ✅ PostgreSQL installed and running
2. ✅ Database `bank_reviews` created (you've already done this)
3. ✅ Python dependencies installed (`pip install -r requirements.txt`)

## Quick Start

### Step 1: Set Database Credentials

The scripts use environment variables for database credentials. You can either:

**Option A: Set environment variables (recommended)**
```bash
# Windows PowerShell
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "bank_reviews"
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_password_here"

# Linux/Mac
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=bank_reviews
export DB_USER=postgres
export DB_PASSWORD=your_password_here
```

**Option B: Edit scripts directly**
- Open `scripts/task3_database/database_setup.py`
- Modify the `get_db_connection()` function with your credentials

### Step 2: Create Tables

Run the database setup script to create tables:

```bash
python scripts/task3_database/database_setup.py
```

This will:
- Connect to your PostgreSQL database
- Create `banks` and `reviews` tables
- Insert bank information
- Create indexes for better performance

### Step 3: Insert Review Data

Insert the processed review data:

```bash
python scripts/task3_database/insert_reviews.py
```

This will:
- Load `data/processed/reviews_with_themes.csv`
- Map bank names to bank_ids
- Insert all reviews with sentiment and theme data
- Show progress and count of inserted reviews

### Step 4: Verify Data Integrity

Verify that data was inserted correctly:

```bash
python scripts/task3_database/verify_database.py
```

This will run verification queries:
- Total review count
- Reviews per bank
- Average rating per bank
- Sentiment distribution
- Theme distribution
- Data completeness
- Date range

## Scripts Overview

### `database_setup.py`
- Creates database schema (tables, indexes)
- Inserts bank information
- Verifies table creation

### `insert_reviews.py`
- Reads processed review data from CSV
- Maps bank names to bank_ids
- Batch inserts reviews (100 at a time for performance)
- Handles missing data gracefully

### `verify_database.py`
- Runs comprehensive verification queries
- Checks data completeness
- Validates KPIs (≥1,000 reviews)
- Displays formatted results

## Database Schema

### `banks` Table
- `bank_id` (PRIMARY KEY, SERIAL)
- `bank_name` (VARCHAR, UNIQUE)
- `app_name` (VARCHAR)
- `created_at` (TIMESTAMP)

### `reviews` Table
- `review_id` (PRIMARY KEY, SERIAL)
- `bank_id` (FOREIGN KEY → banks.bank_id)
- `review_text` (TEXT)
- `rating` (INTEGER, 1-5)
- `review_date` (DATE)
- `sentiment_label` (VARCHAR)
- `sentiment_score` (DECIMAL)
- `theme` (VARCHAR)
- `source` (VARCHAR, default: 'Google Play')
- `created_at` (TIMESTAMP)

## Troubleshooting

### Connection Errors

**Error: "could not connect to server"**
- Make sure PostgreSQL is running
- Check if PostgreSQL service is started:
  ```bash
  # Windows
  Get-Service postgresql*
  
  # Linux
  sudo systemctl status postgresql
  ```

**Error: "database does not exist"**
- Create the database manually:
  ```sql
  CREATE DATABASE bank_reviews;
  ```

**Error: "password authentication failed"**
- Check your PostgreSQL password
- Update credentials in the script or environment variables

### Data Insertion Errors

**Error: "relation 'banks' does not exist"**
- Run `database_setup.py` first to create tables

**Error: "foreign key constraint violation"**
- Make sure bank data is inserted first
- Check that bank names in CSV match those in database

**Error: "duplicate key value violates unique constraint"**
- Scripts use `ON CONFLICT DO NOTHING` to handle duplicates
- Safe to run multiple times

### Verification Issues

**Less than 400 reviews inserted**
- Check if CSV file exists: `data/processed/reviews_with_themes.csv`
- Verify CSV has data (run Task 2 first)
- Check for errors during insertion

## Manual SQL Queries

You can also run queries manually in PostgreSQL:

```sql
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

## KPIs Checklist

- ✅ Working database connection + insert script
- ✅ Tables populated with >1,000 review entries (or ≥400 minimum)
- ✅ SQL dump or schema file committed to GitHub (`database/schema.sql`)

## Next Steps

After completing Task 3:
1. ✅ Verify data integrity (run `verify_database.py`)
2. ✅ Commit scripts to GitHub
3. ✅ Move to Task 4: Insights and Recommendations

## Support

If you encounter issues:
1. Check error messages carefully
2. Verify PostgreSQL is running
3. Check database credentials
4. Ensure CSV file exists and has data
5. Review the troubleshooting section above

