"""
Sentiment Analysis Module
Performs sentiment analysis on bank reviews using transformers (DistilBERT) or VADER
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


def initialize_sentiment_analyzer():
    """
    Initialize sentiment analyzer (prefer DistilBERT, fallback to VADER).
    
    Returns:
        Tuple of (analyzer_type, analyzer)
    """
    if TRANSFORMERS_AVAILABLE:
        try:
            print("📦 Loading DistilBERT sentiment analyzer...")
            analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=False
            )
            print("✅ DistilBERT loaded successfully")
            return "distilbert", analyzer
        except Exception as e:
            print(f"⚠️  DistilBERT failed to load: {e}")
            print("   Falling back to VADER...")
    
    if VADER_AVAILABLE:
        print("📦 Loading VADER sentiment analyzer...")
        analyzer = SentimentIntensityAnalyzer()
        print("✅ VADER loaded successfully")
        return "vader", analyzer
    
    raise ImportError("Neither transformers nor vaderSentiment is available. Please install one.")


def analyze_sentiment_distilbert(text, analyzer):
    """
    Analyze sentiment using DistilBERT.
    
    Args:
        text: Review text
        analyzer: DistilBERT pipeline
        
    Returns:
        Tuple of (label, score)
    """
    try:
        result = analyzer(text[:512])  # Limit to 512 tokens
        label = result[0]['label']
        score = result[0]['score']
        
        # Normalize label to POSITIVE/NEGATIVE
        if label.upper() == 'POSITIVE':
            return 'POSITIVE', score
        elif label.upper() == 'NEGATIVE':
            return 'NEGATIVE', score
        else:
            return 'NEUTRAL', score
    except Exception as e:
        print(f"⚠️  Error analyzing sentiment: {e}")
        return 'NEUTRAL', 0.5


def analyze_sentiment_vader(text, analyzer):
    """
    Analyze sentiment using VADER.
    
    Args:
        text: Review text
        analyzer: VADER SentimentIntensityAnalyzer
        
    Returns:
        Tuple of (label, score)
    """
    try:
        scores = analyzer.polarity_scores(text)
        compound = scores['compound']
        
        # Classify based on compound score
        if compound >= 0.05:
            label = 'POSITIVE'
            score = scores['pos']
        elif compound <= -0.05:
            label = 'NEGATIVE'
            score = scores['neg']
        else:
            label = 'NEUTRAL'
            score = scores['neu']
        
        return label, score
    except Exception as e:
        print(f"⚠️  Error analyzing sentiment: {e}")
        return 'NEUTRAL', 0.5


def perform_sentiment_analysis(input_file="data/cleaned/cleaned_reviews.csv",
                               output_file="data/processed/reviews_with_sentiment.csv"):
    """
    Perform sentiment analysis on cleaned reviews.
    
    Args:
        input_file: Path to cleaned reviews CSV
        output_file: Path to save results
        
    Returns:
        DataFrame with sentiment analysis results
    """
    print("=" * 70)
    print("SENTIMENT ANALYSIS")
    print("=" * 70)
    
    # Load data
    print(f"\n📥 Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        print(f"   ✓ Loaded {len(df)} reviews")
    except FileNotFoundError:
        print(f"   ❌ Error: {input_file} not found!")
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
    print(f"\n🔍 Analyzing sentiment using {analyzer_type.upper()}...")
    sentiments = []
    scores = []
    
    for idx, row in df.iterrows():
        review_text = str(row.get('review_text', ''))
        
        if analyzer_type == "distilbert":
            label, score = analyze_sentiment_distilbert(review_text, analyzer)
        else:
            label, score = analyze_sentiment_vader(review_text, analyzer)
        
        sentiments.append(label)
        scores.append(score)
        
        # Progress indicator
        if (idx + 1) % 100 == 0:
            print(f"   Processed {idx + 1}/{len(df)} reviews...")
    
    # Add results to dataframe
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    
    # Save results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Sentiment analysis complete!")
    print(f"   Results saved to: {output_file}")
    print(f"\n📊 Sentiment Distribution:")
    sentiment_counts = df['sentiment_label'].value_counts()
    for label, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {label}: {count} ({percentage:.1f}%)")
    
    return df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Perform sentiment analysis on reviews")
    parser.add_argument("-i", "--input", default="data/cleaned/cleaned_reviews.csv",
                       help="Input CSV file with cleaned reviews")
    parser.add_argument("-o", "--output", default="data/processed/reviews_with_sentiment.csv",
                       help="Output CSV file with sentiment analysis")
    
    args = parser.parse_args()
    
    perform_sentiment_analysis(args.input, args.output)

