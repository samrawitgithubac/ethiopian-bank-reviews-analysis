"""
Task 4: Insights and Recommendations Analysis
Identifies satisfaction drivers, pain points, and provides recommendations for each bank.
"""

import pandas as pd
import numpy as np
from collections import Counter
import re


def load_data():
    """Load processed review data with sentiment and themes."""
    df = pd.read_csv('../../data/processed/reviews_with_themes.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df


def calculate_bank_metrics(df, bank_name):
    """Calculate key metrics for a specific bank."""
    bank_df = df[df['bank'] == bank_name].copy()
    
    metrics = {
        'total_reviews': len(bank_df),
        'avg_rating': bank_df['rating'].mean(),
        'positive_sentiment_pct': (bank_df['sentiment_label'] == 'POSITIVE').sum() / len(bank_df) * 100,
        'negative_sentiment_pct': (bank_df['sentiment_label'] == 'NEGATIVE').sum() / len(bank_df) * 100,
        'avg_sentiment_score': bank_df['sentiment_score'].mean(),
        'rating_distribution': bank_df['rating'].value_counts().to_dict(),
    }
    
    return metrics, bank_df


def identify_drivers(bank_df, top_n=3):
    """
    Identify satisfaction drivers (positive themes/features).
    Drivers are themes with high positive sentiment and high ratings.
    """
    # Filter positive reviews (rating >= 4 and positive sentiment)
    positive_reviews = bank_df[
        (bank_df['rating'] >= 4) & 
        (bank_df['sentiment_label'] == 'POSITIVE')
    ]
    
    # Count themes in positive reviews
    theme_counts = positive_reviews['theme'].value_counts()
    
    # Calculate theme metrics
    drivers = []
    for theme in theme_counts.index:
        theme_reviews = positive_reviews[positive_reviews['theme'] == theme]
        if len(theme_reviews) > 0:
            avg_rating = theme_reviews['rating'].mean()
            count = len(theme_reviews)
            percentage = (count / len(positive_reviews)) * 100
            
            # Get sample positive review
            sample_review = theme_reviews['review_text'].iloc[0] if len(theme_reviews) > 0 else ""
            
            drivers.append({
                'theme': theme,
                'count': count,
                'percentage': percentage,
                'avg_rating': avg_rating,
                'sample_review': sample_review[:150]  # First 150 chars
            })
    
    # Sort by count and return top N
    drivers = sorted(drivers, key=lambda x: x['count'], reverse=True)
    return drivers[:top_n]


def identify_pain_points(bank_df, top_n=3):
    """
    Identify pain points (negative themes/issues).
    Pain points are themes with high negative sentiment and low ratings.
    """
    # Filter negative reviews (rating <= 2 or negative sentiment)
    negative_reviews = bank_df[
        (bank_df['rating'] <= 2) | 
        (bank_df['sentiment_label'] == 'NEGATIVE')
    ]
    
    # Count themes in negative reviews
    theme_counts = negative_reviews['theme'].value_counts()
    
    # Calculate theme metrics
    pain_points = []
    for theme in theme_counts.index:
        theme_reviews = negative_reviews[negative_reviews['theme'] == theme]
        if len(theme_reviews) > 0:
            avg_rating = theme_reviews['rating'].mean()
            count = len(theme_reviews)
            percentage = (count / len(negative_reviews)) * 100
            
            # Get sample negative review
            sample_review = theme_reviews['review_text'].iloc[0] if len(theme_reviews) > 0 else ""
            
            pain_points.append({
                'theme': theme,
                'count': count,
                'percentage': percentage,
                'avg_rating': avg_rating,
                'sample_review': sample_review[:150]  # First 150 chars
            })
    
    # Sort by count and return top N
    pain_points = sorted(pain_points, key=lambda x: x['count'], reverse=True)
    return pain_points[:top_n]


def extract_keywords_from_reviews(reviews, min_freq=3):
    """Extract common keywords from reviews."""
    # Common banking-related keywords to look for
    keywords_patterns = {
        'transfer': ['transfer', 'send money', 'send', 'transaction'],
        'login': ['login', 'sign in', 'access', 'password', 'pin'],
        'slow': ['slow', 'loading', 'lag', 'delay', 'wait'],
        'crash': ['crash', 'error', 'bug', 'not working', 'freeze'],
        'ui': ['interface', 'ui', 'design', 'user friendly', 'easy'],
        'support': ['support', 'help', 'customer service', 'assistance'],
        'security': ['security', 'safe', 'secure', 'verification'],
        'update': ['update', 'upgrade', 'version'],
        'feature': ['feature', 'functionality', 'option', 'tool'],
    }
    
    keyword_counts = Counter()
    review_text = ' '.join(reviews.str.lower().astype(str))
    
    for keyword, patterns in keywords_patterns.items():
        for pattern in patterns:
            count = len(re.findall(pattern, review_text))
            if count >= min_freq:
                keyword_counts[keyword] += count
    
    return dict(keyword_counts.most_common(10))


def compare_banks(df):
    """Compare performance metrics across all banks."""
    banks = df['bank'].unique()
    comparison = {}
    
    for bank in banks:
        metrics, _ = calculate_bank_metrics(df, bank)
        comparison[bank] = metrics
    
    return comparison


def generate_recommendations(drivers, pain_points, bank_name):
    """Generate actionable recommendations based on drivers and pain points."""
    recommendations = []
    
    # Recommendations based on pain points
    for pain_point in pain_points[:2]:  # Top 2 pain points
        theme = pain_point['theme']
        
        if theme == 'Account Access Issues':
            recommendations.append({
                'priority': 'High',
                'category': 'Account Access',
                'recommendation': 'Implement biometric authentication (fingerprint/face ID) and improve PIN recovery process. Add remote verification options for users abroad.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) mention account access problems."
            })
        elif theme == 'Transaction Performance':
            recommendations.append({
                'priority': 'High',
                'category': 'Performance',
                'recommendation': 'Optimize transaction processing speed and reduce loading times. Implement offline transaction queuing for poor connectivity.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) complain about slow transactions."
            })
        elif theme == 'User Interface & Experience':
            recommendations.append({
                'priority': 'Medium',
                'category': 'UX',
                'recommendation': 'Redesign UI for better usability. Conduct user testing sessions and implement user feedback loops.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) mention UI/UX issues."
            })
        elif theme == 'Customer Support':
            recommendations.append({
                'priority': 'High',
                'category': 'Support',
                'recommendation': 'Integrate AI chatbot for 24/7 support. Reduce response time and improve support ticket resolution.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) mention support issues."
            })
        elif theme == 'App Reliability':
            recommendations.append({
                'priority': 'Critical',
                'category': 'Reliability',
                'recommendation': 'Fix app crashes and stability issues. Implement comprehensive error handling and monitoring.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) report reliability problems."
            })
        elif theme == 'Feature Requests':
            recommendations.append({
                'priority': 'Medium',
                'category': 'Features',
                'recommendation': 'Prioritize most requested features. Consider adding budgeting tools, bill payments, and investment tracking.',
                'rationale': f"{pain_point['count']} reviews ({pain_point['percentage']:.1f}%) request new features."
            })
    
    # Recommendations based on drivers (enhance strengths)
    for driver in drivers[:1]:  # Top driver
        theme = driver['theme']
        
        if theme == 'Transaction Performance':
            recommendations.append({
                'priority': 'Low',
                'category': 'Enhancement',
                'recommendation': 'Continue optimizing transaction speed. Add transaction scheduling and recurring payment features.',
                'rationale': f"Users appreciate fast transactions ({driver['count']} positive mentions)."
            })
        elif theme == 'User Interface & Experience':
            recommendations.append({
                'priority': 'Low',
                'category': 'Enhancement',
                'recommendation': 'Maintain current UI improvements. Consider adding dark mode and customization options.',
                'rationale': f"UI is well-received ({driver['count']} positive mentions)."
            })
    
    return recommendations


def analyze_all_banks(df):
    """Perform comprehensive analysis for all banks."""
    banks = df['bank'].unique()
    results = {}
    
    for bank in banks:
        print(f"\n{'='*70}")
        print(f"Analyzing {bank}")
        print(f"{'='*70}")
        
        metrics, bank_df = calculate_bank_metrics(df, bank)
        drivers = identify_drivers(bank_df, top_n=3)
        pain_points = identify_pain_points(bank_df, top_n=3)
        recommendations = generate_recommendations(drivers, pain_points, bank)
        
        # Extract keywords
        positive_reviews = bank_df[bank_df['sentiment_label'] == 'POSITIVE']['review_text']
        negative_reviews = bank_df[bank_df['sentiment_label'] == 'NEGATIVE']['review_text']
        
        positive_keywords = extract_keywords_from_reviews(positive_reviews)
        negative_keywords = extract_keywords_from_reviews(negative_reviews)
        
        results[bank] = {
            'metrics': metrics,
            'drivers': drivers,
            'pain_points': pain_points,
            'recommendations': recommendations,
            'positive_keywords': positive_keywords,
            'negative_keywords': negative_keywords
        }
        
        # Print summary
        print(f"\nMetrics:")
        print(f"  Average Rating: {metrics['avg_rating']:.2f}")
        print(f"  Positive Sentiment: {metrics['positive_sentiment_pct']:.1f}%")
        print(f"  Negative Sentiment: {metrics['negative_sentiment_pct']:.1f}%")
        
        print(f"\nTop Drivers:")
        for i, driver in enumerate(drivers, 1):
            print(f"  {i}. {driver['theme']} ({driver['count']} mentions, {driver['percentage']:.1f}%)")
        
        print(f"\nTop Pain Points:")
        for i, pain_point in enumerate(pain_points, 1):
            print(f"  {i}. {pain_point['theme']} ({pain_point['count']} mentions, {pain_point['percentage']:.1f}%)")
    
    return results


def save_insights_to_csv(results, output_path='../../data/processed/bank_insights.csv'):
    """Save insights to CSV for reporting."""
    insights_data = []
    
    for bank, data in results.items():
        # Drivers
        for driver in data['drivers']:
            insights_data.append({
                'bank': bank,
                'type': 'Driver',
                'theme': driver['theme'],
                'count': driver['count'],
                'percentage': driver['percentage'],
                'avg_rating': driver['avg_rating'],
                'sample_review': driver['sample_review']
            })
        
        # Pain points
        for pain_point in data['pain_points']:
            insights_data.append({
                'bank': bank,
                'type': 'Pain Point',
                'theme': pain_point['theme'],
                'count': pain_point['count'],
                'percentage': pain_point['percentage'],
                'avg_rating': pain_point['avg_rating'],
                'sample_review': pain_point['sample_review']
            })
    
    insights_df = pd.DataFrame(insights_data)
    insights_df.to_csv(output_path, index=False)
    print(f"\nInsights saved to {output_path}")
    return insights_df


if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    
    print(f"Total reviews: {len(df)}")
    print(f"Banks: {df['bank'].unique()}")
    
    print("\nPerforming comprehensive analysis...")
    results = analyze_all_banks(df)
    
    print("\nSaving insights...")
    insights_df = save_insights_to_csv(results)
    
    print("\nAnalysis complete!")
    print(f"\nSummary:")
    print(f"  Total reviews analyzed: {len(df)}")
    print(f"  Banks analyzed: {len(results)}")
    print(f"  Insights generated: {len(insights_df)}")

