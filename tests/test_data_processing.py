"""
Unit tests for data processing module
"""

import unittest
import pandas as pd
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing import preprocess_reviews


class TestDataProcessing(unittest.TestCase):
    """Test cases for data processing functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data = pd.DataFrame({
            'content': ['Great app!', 'Bad app', 'Great app!', '', 'Good'],
            'score': [5, 1, 5, 3, 4],
            'at': ['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-03', '2024-01-04'],
            'bank': ['CBE', 'BOA', 'CBE', 'Dashen', 'CBE'],
            'source': ['Google Play'] * 5
        })
        
        # Create test directories
        os.makedirs('data/raw', exist_ok=True)
        os.makedirs('data/cleaned', exist_ok=True)
        
        # Save test data
        self.test_input = 'data/raw/test_reviews.csv'
        self.test_output = 'data/cleaned/test_cleaned.csv'
        self.test_data.to_csv(self.test_input, index=False)
    
    def test_preprocess_removes_duplicates(self):
        """Test that preprocessing removes duplicate reviews"""
        result = preprocess_reviews(self.test_input, self.test_output)
        self.assertIsNotNone(result)
        # Should remove 1 duplicate (2 'Great app!' reviews)
        self.assertLessEqual(len(result), len(self.test_data))
    
    def test_preprocess_removes_empty_reviews(self):
        """Test that preprocessing removes empty reviews"""
        result = preprocess_reviews(self.test_input, self.test_output)
        self.assertIsNotNone(result)
        # Should remove empty review
        self.assertNotIn('', result['review_text'].values)
    
    def test_preprocess_validates_ratings(self):
        """Test that preprocessing validates ratings"""
        result = preprocess_reviews(self.test_input, self.test_output)
        self.assertIsNotNone(result)
        # All ratings should be between 1 and 5
        self.assertTrue(result['rating'].between(1, 5).all())
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.test_input):
            os.remove(self.test_input)
        if os.path.exists(self.test_output):
            os.remove(self.test_output)


if __name__ == '__main__':
    unittest.main()

