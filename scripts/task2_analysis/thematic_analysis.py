"""
Thematic Analysis Module
Extracts themes from bank reviews using keyword extraction and rule-based clustering
"""

import pandas as pd
import os
import sys
import re
from pathlib import Path
from collections import Counter

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# Theme keywords mapping
THEME_KEYWORDS = {
    'Account Access Issues': [
        'login', 'password', 'access', 'account', 'sign in', 'signin', 'authentication',
        'locked', 'blocked', 'cannot access', "can't access", 'forgot password',
        'wrong password', 'login error', 'access denied', 'unable to login'
    ],
    'Transaction Performance': [
        'transfer', 'transaction', 'payment', 'send money', 'receive', 'slow',
        'fast', 'speed', 'quick', 'delay', 'failed', 'error', 'timeout',
        'processing', 'pending', 'complete', 'success', 'money transfer',
        'transfer money', 'bill payment', 'transaction failed'
    ],
    'User Interface & Experience': [
        'ui', 'interface', 'design', 'layout', 'user friendly', 'easy to use',
        'difficult', 'confusing', 'navigation', 'menu', 'button', 'screen',
        'appearance', 'look', 'feel', 'experience', 'usability', 'intuitive',
        'cluttered', 'clean', 'modern', 'outdated'
    ],
    'Customer Support': [
        'support', 'help', 'service', 'customer service', 'assistance',
        'contact', 'response', 'complaint', 'issue', 'problem', 'resolve',
        'fix', 'helpful', 'unhelpful', 'no response', 'slow response'
    ],
    'Feature Requests': [
        'feature', 'add', 'need', 'want', 'missing', 'should have', 'wish',
        'request', 'suggest', 'improve', 'enhance', 'new feature', 'option',
        'functionality', 'capability', 'fingerprint', 'biometric', 'face id'
    ],
    'App Reliability': [
        'crash', 'crashing', 'freeze', 'freezing', 'bug', 'bugs', 'error',
        'not working', "doesn't work", 'broken', 'glitch', 'issue', 'problem',
        'stable', 'unstable', 'reliable', 'unreliable', 'close', 'close unexpectedly'
    ],
    'Security & Privacy': [
        'security', 'secure', 'safe', 'privacy', 'data', 'information',
        'protection', 'hack', 'breach', 'trust', 'trustworthy', 'secure transaction'
    ]
}


def preprocess_text(text):
    """
    Preprocess text for keyword matching.
    
    Args:
        text: Raw text
        
    Returns:
        Preprocessed text
    """
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def identify_theme(review_text):
    """
    Identify theme for a single review using keyword matching.
    
    Args:
        review_text: Review text
        
    Returns:
        Theme label
    """
    if pd.isna(review_text) or not review_text:
        return 'Other'
    
    text = preprocess_text(review_text)
    
    # Count keyword matches for each theme
    theme_scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        theme_scores[theme] = score
    
    # Get theme with highest score
    max_score = max(theme_scores.values())
    
    if max_score == 0:
        return 'Other'
    
    # Return theme with highest score
    for theme, score in theme_scores.items():
        if score == max_score:
            return theme
    
    return 'Other'


def extract_keywords_tfidf(df, n_keywords=20):
    """
    Extract top keywords using TF-IDF.
    
    Args:
        df: DataFrame with review_text column
        n_keywords: Number of keywords to extract
        
    Returns:
        List of top keywords
    """
    if not SKLEARN_AVAILABLE:
        return []
    
    try:
        # Combine all reviews
        texts = df['review_text'].fillna('').astype(str).tolist()
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=n_keywords,
            stop_words='english',
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=2  # Word must appear in at least 2 documents
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top keywords
        keywords = feature_names.tolist()
        
        return keywords
    except Exception as e:
        print(f"⚠️  Error extracting keywords: {e}")
        return []


def perform_thematic_analysis(input_file="data/processed/reviews_with_sentiment.csv",
                              output_file="data/processed/reviews_with_themes.csv"):
    """
    Perform thematic analysis on reviews with sentiment.
    
    Args:
        input_file: Path to reviews with sentiment CSV
        output_file: Path to save results
        
    Returns:
        DataFrame with thematic analysis results
    """
    print("=" * 70)
    print("THEMATIC ANALYSIS")
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
    
    # Ensure review_id exists
    if 'review_id' not in df.columns:
        df['review_id'] = range(1, len(df) + 1)
    
    # Identify themes
    print(f"\n🔍 Identifying themes...")
    themes = []
    
    for idx, row in df.iterrows():
        review_text = str(row.get('review_text', ''))
        theme = identify_theme(review_text)
        themes.append(theme)
        
        # Progress indicator
        if (idx + 1) % 100 == 0:
            print(f"   Processed {idx + 1}/{len(df)} reviews...")
    
    # Add themes to dataframe
    df['theme'] = themes
    
    # Extract keywords using TF-IDF
    print(f"\n🔑 Extracting keywords using TF-IDF...")
    keywords = extract_keywords_tfidf(df, n_keywords=30)
    
    # Save results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n✅ Thematic analysis complete!")
    print(f"   Results saved to: {output_file}")
    
    print(f"\n📊 Theme Distribution:")
    theme_counts = df['theme'].value_counts()
    for theme, count in theme_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {theme}: {count} ({percentage:.1f}%)")
    
    if keywords:
        print(f"\n🔑 Top Keywords:")
        print(f"   {', '.join(keywords[:10])}")
    
    # Theme distribution by bank
    print(f"\n📊 Theme Distribution by Bank:")
    if 'bank' in df.columns:
        bank_theme = pd.crosstab(df['bank'], df['theme'])
        print(bank_theme)
    
    return df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Perform thematic analysis on reviews")
    parser.add_argument("-i", "--input", default="data/processed/reviews_with_sentiment.csv",
                       help="Input CSV file with sentiment analysis")
    parser.add_argument("-o", "--output", default="data/processed/reviews_with_themes.csv",
                       help="Output CSV file with thematic analysis")
    
    args = parser.parse_args()
    
    perform_thematic_analysis(args.input, args.output)

