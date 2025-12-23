"""
Model Training Script
Performs sentiment and thematic analysis on reviews
"""

import pandas as pd
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import preprocess_reviews


def train_sentiment_model(input_file="data/cleaned/cleaned_reviews.csv",
                          output_file="data/processed/reviews_with_sentiment.csv"):
    """
    Train/apply sentiment analysis model.
    
    Args:
        input_file: Path to cleaned reviews
        output_file: Path to save results
    """
    # Import sentiment analysis functions
    from scripts.task2_analysis.sentiment_analysis import perform_sentiment_analysis
    
    return perform_sentiment_analysis(input_file, output_file)


def train_thematic_model(input_file="data/processed/reviews_with_sentiment.csv",
                         output_file="data/processed/reviews_with_themes.csv"):
    """
    Train/apply thematic analysis model.
    
    Args:
        input_file: Path to reviews with sentiment
        output_file: Path to save results
    """
    # Import thematic analysis functions
    from scripts.task2_analysis.thematic_analysis import perform_thematic_analysis
    
    return perform_thematic_analysis(input_file, output_file)


if __name__ == "__main__":
    # Run sentiment analysis
    print("Training sentiment model...")
    train_sentiment_model()
    
    # Run thematic analysis
    print("\nTraining thematic model...")
    train_thematic_model()

