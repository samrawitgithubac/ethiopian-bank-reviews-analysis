"""
Prediction Script
Predicts sentiment and themes for new reviews
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def predict_sentiment(review_text):
    """
    Predict sentiment for a single review.
    
    Args:
        review_text: Text of the review
        
    Returns:
        Tuple of (label, score)
    """
    from scripts.task2_analysis.sentiment_analysis import (
        initialize_sentiment_analyzer,
        analyze_sentiment_distilbert,
        analyze_sentiment_vader
    )
    
    analyzer_type, analyzer = initialize_sentiment_analyzer()
    
    if analyzer_type == "distilbert":
        return analyze_sentiment_distilbert(review_text, analyzer)
    else:
        return analyze_sentiment_vader(review_text, analyzer)


def predict_theme(review_text):
    """
    Predict theme for a single review.
    
    Args:
        review_text: Text of the review
        
    Returns:
        Theme label
    """
    from scripts.task2_analysis.thematic_analysis import identify_theme
    
    return identify_theme(review_text)


def predict_batch(input_file, output_file=None):
    """
    Predict sentiment and themes for a batch of reviews.
    
    Args:
        input_file: Path to CSV with reviews
        output_file: Path to save predictions (optional)
        
    Returns:
        DataFrame with predictions
    """
    df = pd.read_csv(input_file)
    
    # Predict sentiment
    sentiments = []
    scores = []
    themes = []
    
    for text in df['review_text']:
        label, score = predict_sentiment(str(text))
        theme = predict_theme(str(text))
        sentiments.append(label)
        scores.append(score)
        themes.append(theme)
    
    df['sentiment_label'] = sentiments
    df['sentiment_score'] = scores
    df['theme'] = themes
    
    if output_file:
        df.to_csv(output_file, index=False)
    
    return df


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Predict sentiment and themes")
    parser.add_argument("input", help="Input CSV file")
    parser.add_argument("-o", "--output", help="Output CSV file")
    
    args = parser.parse_args()
    
    result = predict_batch(args.input, args.output)
    print(f"\n✅ Predictions complete!")
    print(f"   Processed {len(result)} reviews")

