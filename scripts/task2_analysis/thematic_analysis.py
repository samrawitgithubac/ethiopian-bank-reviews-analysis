"""
Thematic Analysis Script for Ethiopian Bank Reviews
Task 2 - Sentiment and Thematic Analysis

This script:
- Extracts keywords using TF-IDF and spaCy
- Clusters keywords into themes (3-5 per bank)
- Identifies themes like: Account Access Issues, Transaction Performance, UI/UX, Customer Support, Feature Requests
- Saves results with identified themes
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

# Try to import spaCy
try:
    import spacy
    SPACY_AVAILABLE = True
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("⚠ spaCy English model not found. Please run: python -m spacy download en_core_web_sm")
        SPACY_AVAILABLE = False
except ImportError:
    SPACY_AVAILABLE = False
    print("⚠ spaCy not available, will use TF-IDF only")

# Try to import scikit-learn for TF-IDF
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.decomposition import LatentDirichletAllocation, NMF
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠ scikit-learn not available, will use simple keyword extraction")

# Theme keywords mapping (rule-based clustering)
THEME_KEYWORDS = {
    'Account Access Issues': [
        'login', 'password', 'pin', 'access', 'account', 'locked', 'blocked', 
        'verification', 'authenticate', 'security', 'biometric', 'fingerprint',
        'face', 'id', 'credentials', 'sign in', 'sign out', 'session'
    ],
    'Transaction Performance': [
        'transfer', 'transaction', 'payment', 'slow', 'fast', 'speed', 
        'timeout', 'failed', 'error', 'processing', 'pending', 'complete',
        'money', 'send', 'receive', 'balance', 'amount', 'fee', 'charge'
    ],
    'User Interface & Experience': [
        'ui', 'interface', 'design', 'layout', 'user friendly', 'easy', 
        'difficult', 'confusing', 'navigate', 'menu', 'button', 'screen',
        'appearance', 'look', 'feel', 'modern', 'outdated', 'cluttered'
    ],
    'Customer Support': [
        'support', 'help', 'service', 'customer', 'contact', 'response',
        'assistance', 'issue', 'problem', 'complaint', 'resolve', 'fix',
        'chat', 'call', 'email', 'response time', 'wait', 'queue'
    ],
    'Feature Requests': [
        'feature', 'add', 'need', 'want', 'missing', 'suggest', 'request',
        'improve', 'enhance', 'update', 'new', 'functionality', 'option',
        'budget', 'savings', 'investment', 'loan', 'bill', 'notification'
    ],
    'App Reliability': [
        'crash', 'bug', 'error', 'freeze', 'hang', 'close', 'stop',
        'working', 'broken', 'not working', 'issue', 'problem', 'glitch',
        'stable', 'reliable', 'unstable', 'force close', 'restart'
    ]
}

def preprocess_text(text: str) -> str:
    """Basic text preprocessing."""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def extract_keywords_tfidf(texts: list, max_features: int = 50) -> list:
    """Extract keywords using TF-IDF."""
    if not SKLEARN_AVAILABLE:
        return []
    
    try:
        vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),  # Include unigrams and bigrams
            min_df=2,  # Word must appear in at least 2 documents
            max_df=0.95  # Ignore words that appear in >95% of documents
        )
        
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get top keywords by average TF-IDF score
        scores = tfidf_matrix.mean(axis=0).A1
        top_indices = scores.argsort()[-max_features:][::-1]
        keywords = [feature_names[i] for i in top_indices]
        
        return keywords
    except Exception as e:
        print(f"⚠ Error in TF-IDF extraction: {e}")
        return []


def extract_keywords_spacy(texts: list, max_keywords: int = 50) -> list:
    """Extract keywords using spaCy (nouns, adjectives, verbs)."""
    if not SPACY_AVAILABLE:
        return []
    
    keywords = []
    pos_tags = ['NOUN', 'ADJ', 'VERB']  # Focus on meaningful parts of speech
    
    for text in texts:
        if not text or pd.isna(text):
            continue
        
        try:
            doc = nlp(str(text))
            for token in doc:
                if (token.pos_ in pos_tags and 
                    not token.is_stop and 
                    not token.is_punct and
                    len(token.text) > 2):
                    keywords.append(token.lemma_.lower())
        except Exception as e:
            continue
    
    # Count and return most common keywords
    keyword_counts = Counter(keywords)
    top_keywords = [word for word, count in keyword_counts.most_common(max_keywords)]
    return top_keywords


def identify_theme(review_text: str) -> str:
    """
    Identify theme for a review based on keyword matching.
    Returns the theme with the highest match score.
    """
    if pd.isna(review_text):
        return "Other"
    
    text_lower = str(review_text).lower()
    theme_scores = {}
    
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text_lower:
                score += 1
        theme_scores[theme] = score
    
    # Return theme with highest score, or "Other" if no match
    if max(theme_scores.values()) > 0:
        return max(theme_scores, key=theme_scores.get)
    else:
        return "Other"


def perform_thematic_analysis(input_file="data/processed/reviews_with_sentiment.csv", output_file="data/processed/reviews_with_themes.csv"):
    """
    Perform thematic analysis on reviews with sentiment.
    
    Args:
        input_file: Path to reviews with sentiment CSV
        output_file: Path to save reviews with themes
    """
    print("=" * 60)
    print("THEMATIC ANALYSIS")
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
        print("   Please run sentiment_analysis.py first.")
        return None
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return None
    
    # Preprocess texts
    print(f"\n🔍 Preprocessing review texts...")
    df['processed_text'] = df['review_text'].apply(preprocess_text)
    
    # Extract keywords per bank
    print(f"\n🔍 Extracting keywords per bank...")
    bank_keywords = {}
    
    for bank in df['bank'].unique():
        bank_reviews = df[df['bank'] == bank]['processed_text'].tolist()
        bank_reviews = [r for r in bank_reviews if r.strip()]
        
        print(f"\n   Analyzing {bank}...")
        
        # Extract keywords using TF-IDF
        if SKLEARN_AVAILABLE:
            keywords_tfidf = extract_keywords_tfidf(bank_reviews, max_features=30)
            print(f"     TF-IDF keywords: {', '.join(keywords_tfidf[:10])}...")
        
        # Extract keywords using spaCy
        if SPACY_AVAILABLE:
            keywords_spacy = extract_keywords_spacy(bank_reviews, max_keywords=30)
            print(f"     spaCy keywords: {', '.join(keywords_spacy[:10])}...")
        
        # Combine keywords
        all_keywords = []
        if SKLEARN_AVAILABLE:
            all_keywords.extend(keywords_tfidf)
        if SPACY_AVAILABLE:
            all_keywords.extend(keywords_spacy)
        
        bank_keywords[bank] = list(set(all_keywords))[:20]  # Top 20 unique keywords
    
    # Identify themes for each review
    print(f"\n🔍 Identifying themes for each review...")
    df['theme'] = df['review_text'].apply(identify_theme)
    
    # Print theme distribution
    print("\n" + "=" * 60)
    print("THEME DISTRIBUTION")
    print("=" * 60)
    
    print(f"\nOverall theme distribution:")
    theme_counts = df['theme'].value_counts()
    for theme, count in theme_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {theme}: {count} ({percentage:.1f}%)")
    
    print(f"\nTheme distribution by bank:")
    for bank in df['bank'].unique():
        print(f"\n   {bank}:")
        bank_df = df[df['bank'] == bank]
        bank_themes = bank_df['theme'].value_counts()
        for theme, count in bank_themes.items():
            percentage = (count / len(bank_df)) * 100
            print(f"     {theme}: {count} ({percentage:.1f}%)")
    
    # Print top keywords per bank
    print(f"\n📊 Top keywords per bank:")
    for bank, keywords in bank_keywords.items():
        print(f"\n   {bank}:")
        print(f"     {', '.join(keywords[:15])}")
    
    # Save results
    print(f"\n💾 Saving results to {output_file}...")
    try:
        # Drop processed_text column before saving
        df_output = df.drop(columns=['processed_text'], errors='ignore')
        df_output.to_csv(output_file, index=False, encoding='utf-8')
        print(f"   ✓ Successfully saved {len(df_output)} reviews with themes")
    except Exception as e:
        print(f"   ❌ Error saving file: {e}")
        return None
    
    print("\n✅ Thematic analysis complete!")
    
    return df


if __name__ == "__main__":
    perform_thematic_analysis()

