"""
Sentiment Analysis Script for Ethiopian Bank Reviews
Task 2 - Sentiment and Thematic Analysis

This script:
- Performs sentiment analysis using distilbert-base-uncased-finetuned-sst-2-english
- Falls back to VADER if transformers is not available
- Computes sentiment scores (positive, negative, neutral)
- Saves results with sentiment labels and scores
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Try to import transformers for distilbert
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠ transformers not available, will use VADER instead")

# Try to import VADER as fallback
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    print("⚠ VADER not available, please install vaderSentiment")

def initialize_sentiment_analyzer():
    """Initialize the sentiment analyzer (prefer distilbert, fallback to VADER)."""
    if TRANSFORMERS_AVAILABLE:
        try:
            print("📦 Loading distilbert-base-uncased-finetuned-sst-2-english...")
            classifier = pipeline("sentiment-analysis", 
                                model="distilbert-base-uncased-finetuned-sst-2-english")
            print("✅ distilbert model loaded successfully")
            return "distilbert", classifier
        except Exception as e:
            print(f"⚠ Error loading distilbert: {e}")
            print("   Falling back to VADER...")
    
    if VADER_AVAILABLE:
        print("📦 Using VADER sentiment analyzer...")
        analyzer = SentimentIntensityAnalyzer()
        return "vader", analyzer
    
    raise ImportError("Neither transformers nor vaderSentiment is available. Please install one of them.")


def analyze_sentiment_distilbert(text: str, classifier) -> Tuple[str, float]:
    """
    Analyze sentiment using distilbert model.
    
    Returns:
        Tuple of (label, score) where label is 'POSITIVE' or 'NEGATIVE'
        and score is confidence (0-1)
    """
    if pd.isna(text) or str(text).strip() == "":
        return "NEUTRAL", 0.5
    
    try:
        result = classifier(str(text))[0]
        label = result['label']
        score = result['score']
        
        # Convert to standard format
        if label == 'POSITIVE':
            return "POSITIVE", float(score)
        elif label == 'NEGATIVE':
            return "NEGATIVE", float(score)
        else:
            return "NEUTRAL", 0.5
    except Exception as e:
        print(f"⚠ Error analyzing text: {e}")
        return "NEUTRAL", 0.5


def analyze_sentiment_vader(text: str, analyzer) -> Tuple[str, float]:
    """
    Analyze sentiment using VADER.
    
    Returns:
        Tuple of (label, score) where label is 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
        and score is compound score (-1 to 1)
    """
    if pd.isna(text) or str(text).strip() == "":
        return "NEUTRAL", 0.0
    
    try:
        scores = analyzer.polarity_scores(str(text))
        compound = scores['compound']
        
        # Classify based on compound score
        if compound >= 0.05:
            label = "POSITIVE"
            score = compound
        elif compound <= -0.05:
            label = "NEGATIVE"
            score = abs(compound)  # Make it positive for consistency
        else:
            label = "NEUTRAL"
            score = abs(compound)
        
        return label, float(score)
    except Exception as e:
        print(f"⚠ Error analyzing text: {e}")
        return "NEUTRAL", 0.0


def perform_sentiment_analysis(input_file="data/cleaned/cleaned_reviews.csv", output_file="data/processed/reviews_with_sentiment.csv"):
    """
    Perform sentiment analysis on cleaned reviews.
    
    Args:
        input_file: Path to cleaned reviews CSV
        output_file: Path to save reviews with sentiment analysis
    """
    print("=" * 60)
    print("SENTIMENT ANALYSIS")
    print("=" * 60)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    
    # Load data
    print(f"\n📥 Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        print(f"   ✓ Loaded {len(df)} reviews")
    except FileNotFoundError:
        print(f"   ❌ Error: {input_file} not found!")
        print("   Please run preprocess_reviews.py first.")
        return None
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return None
    
    # Initialize analyzer
    analyzer_type, analyzer = initialize_sentiment_analyzer()
    
    # Add review_id if not present
    if 'review_id' not in df.columns:
        df['review_id'] = range(1, len(df) + 1)
    
    # Perform sentiment analysis
    print(f"\n🔍 Analyzing sentiment using {analyzer_type}...")
    print("   This may take a few minutes...")
    
    sentiment_labels = []
    sentiment_scores = []
    
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"   Processed {idx + 1}/{len(df)} reviews...")
        
        text = row['review_text']
        
        if analyzer_type == "distilbert":
            label, score = analyze_sentiment_distilbert(text, analyzer)
        else:
            label, score = analyze_sentiment_vader(text, analyzer)
        
        sentiment_labels.append(label)
        sentiment_scores.append(score)
    
    # Add sentiment columns
    df['sentiment_label'] = sentiment_labels
    df['sentiment_score'] = sentiment_scores
    
    # Convert sentiment_label to standard format (POSITIVE, NEGATIVE, NEUTRAL)
    # distilbert only returns POSITIVE/NEGATIVE, so we'll keep it as is
    # but add a neutral category based on score threshold if needed
    if analyzer_type == "distilbert":
        # For distilbert, we can consider low confidence scores as neutral
        df.loc[df['sentiment_score'] < 0.6, 'sentiment_label'] = 'NEUTRAL'
    
    # Save results
    print(f"\n💾 Saving results to {output_file}...")
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"   ✓ Successfully saved {len(df)} reviews with sentiment analysis")
    except Exception as e:
        print(f"   ❌ Error saving file: {e}")
        return None
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SENTIMENT ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"\nTotal reviews analyzed: {len(df)}")
    print(f"\nSentiment distribution:")
    sentiment_counts = df['sentiment_label'].value_counts()
    for label, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {label}: {count} ({percentage:.1f}%)")
    
    print(f"\nAverage sentiment scores:")
    avg_scores = df.groupby('sentiment_label')['sentiment_score'].mean()
    for label, score in avg_scores.items():
        print(f"   {label}: {score:.3f}")
    
    print(f"\nSentiment by bank:")
    bank_sentiment = pd.crosstab(df['bank'], df['sentiment_label'], normalize='index') * 100
    print(bank_sentiment.round(1))
    
    print(f"\nSentiment by rating:")
    rating_sentiment = pd.crosstab(df['rating'], df['sentiment_label'], normalize='index') * 100
    print(rating_sentiment.round(1))
    
    print("\n✅ Sentiment analysis complete!")
    
    return df


if __name__ == "__main__":
    perform_sentiment_analysis()

