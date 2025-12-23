-- PostgreSQL Database Schema for Bank Reviews Analysis
-- Task 3 - Store Cleaned Data in PostgreSQL

-- Create database (run this manually or use database_setup.py)
-- CREATE DATABASE bank_reviews;

-- Banks table: Stores information about the banks
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table: Stores the scraped and processed review data
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
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
CREATE INDEX IF NOT EXISTS idx_reviews_theme ON reviews(theme);

-- Insert bank information
INSERT INTO banks (bank_name, app_name) VALUES
    ('Commercial Bank of Ethiopia', 'Commercial Bank of Ethiopia Mobile'),
    ('Bank of Abyssinia', 'BoA Mobile'),
    ('Dashen Bank', 'Dashen Mobile')
ON CONFLICT (bank_name) DO NOTHING;

-- Example queries for verification:

-- Count reviews per bank
-- SELECT b.bank_name, COUNT(r.review_id) as review_count
-- FROM banks b
-- LEFT JOIN reviews r ON b.bank_id = r.bank_id
-- GROUP BY b.bank_id, b.bank_name
-- ORDER BY review_count DESC;

-- Average rating per bank
-- SELECT b.bank_name, AVG(r.rating) as avg_rating, COUNT(r.review_id) as count
-- FROM banks b
-- LEFT JOIN reviews r ON b.bank_id = r.bank_id
-- WHERE r.rating IS NOT NULL
-- GROUP BY b.bank_id, b.bank_name
-- ORDER BY avg_rating DESC;

-- Sentiment distribution
-- SELECT sentiment_label, COUNT(*) as count
-- FROM reviews
-- WHERE sentiment_label IS NOT NULL
-- GROUP BY sentiment_label
-- ORDER BY count DESC;

