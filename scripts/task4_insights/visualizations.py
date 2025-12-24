"""
Task 4: Visualizations for Insights and Recommendations
Creates stakeholder-friendly visualizations for the final report.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from wordcloud import WordCloud
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Create output directory
os.makedirs('../../reports/figures', exist_ok=True)


def load_data():
    """Load processed review data."""
    df = pd.read_csv('../../data/processed/reviews_with_themes.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df


def plot_sentiment_distribution_by_bank(df, save_path='../../reports/figures/sentiment_by_bank.png'):
    """Plot sentiment distribution for each bank."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    banks = df['bank'].unique()
    
    for idx, bank in enumerate(banks):
        bank_df = df[df['bank'] == bank]
        sentiment_counts = bank_df['sentiment_label'].value_counts()
        
        colors = {'POSITIVE': '#2ecc71', 'NEGATIVE': '#e74c3c', 'NEUTRAL': '#95a5a6'}
        colors_list = [colors.get(x, '#3498db') for x in sentiment_counts.index]
        
        axes[idx].bar(sentiment_counts.index, sentiment_counts.values, color=colors_list)
        axes[idx].set_title(f'{bank}\nSentiment Distribution', fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Sentiment', fontsize=10)
        axes[idx].set_ylabel('Count', fontsize=10)
        axes[idx].grid(axis='y', alpha=0.3)
        
        # Add percentage labels
        total = sentiment_counts.sum()
        for i, (label, count) in enumerate(sentiment_counts.items()):
            percentage = (count / total) * 100
            axes[idx].text(i, count + 5, f'{percentage:.1f}%', 
                          ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_rating_distribution_by_bank(df, save_path='../../reports/figures/rating_distribution.png'):
    """Plot rating distribution for each bank."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    banks = df['bank'].unique()
    x = np.arange(len(banks))
    width = 0.15
    
    # Create grouped bar chart
    ratings = [1, 2, 3, 4, 5]
    colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#27ae60']
    
    for i, rating in enumerate(ratings):
        counts = [len(df[(df['bank'] == bank) & (df['rating'] == rating)]) 
                 for bank in banks]
        ax.bar(x + i*width, counts, width, label=f'{rating} Star', color=colors[i])
    
    ax.set_xlabel('Bank', fontsize=11, fontweight='bold')
    ax.set_ylabel('Number of Reviews', fontsize=11, fontweight='bold')
    ax.set_title('Rating Distribution by Bank', fontsize=13, fontweight='bold')
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(banks)
    ax.legend(title='Rating', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_sentiment_trends(df, save_path='../../reports/figures/sentiment_trends.png'):
    """Plot sentiment trends over time."""
    # Group by month and bank
    df['month'] = df['date'].dt.to_period('M')
    monthly_sentiment = df.groupby(['month', 'bank', 'sentiment_label']).size().unstack(fill_value=0)
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    banks = df['bank'].unique()
    
    for idx, bank in enumerate(banks):
        bank_monthly = monthly_sentiment.xs(bank, level='bank')
        
        if 'POSITIVE' in bank_monthly.columns:
            axes[idx].plot(bank_monthly.index.astype(str), bank_monthly['POSITIVE'], 
                          marker='o', label='Positive', color='#2ecc71', linewidth=2)
        if 'NEGATIVE' in bank_monthly.columns:
            axes[idx].plot(bank_monthly.index.astype(str), bank_monthly['NEGATIVE'], 
                          marker='s', label='Negative', color='#e74c3c', linewidth=2)
        
        axes[idx].set_title(f'{bank} - Sentiment Trends Over Time', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Month', fontsize=10)
        axes[idx].set_ylabel('Number of Reviews', fontsize=10)
        axes[idx].legend(fontsize=9)
        axes[idx].grid(alpha=0.3)
        axes[idx].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_theme_distribution(df, save_path='../../reports/figures/theme_distribution.png'):
    """Plot theme distribution by bank."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    banks = df['bank'].unique()
    
    for idx, bank in enumerate(banks):
        bank_df = df[df['bank'] == bank]
        theme_counts = bank_df['theme'].value_counts()
        
        axes[idx].barh(theme_counts.index, theme_counts.values, color='teal')
        axes[idx].set_title(f'{bank}\nTheme Distribution', fontsize=11, fontweight='bold')
        axes[idx].set_xlabel('Count', fontsize=10)
        axes[idx].set_ylabel('Theme', fontsize=10)
        axes[idx].invert_yaxis()
        axes[idx].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def plot_bank_comparison(df, save_path='../../reports/figures/bank_comparison.png'):
    """Create comparison chart of key metrics across banks."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    banks = df['bank'].unique()
    
    # 1. Average Rating
    avg_ratings = [df[df['bank'] == bank]['rating'].mean() for bank in banks]
    axes[0, 0].bar(banks, avg_ratings, color=['#3498db', '#9b59b6', '#e67e22'])
    axes[0, 0].set_title('Average Rating by Bank', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Average Rating', fontsize=10)
    axes[0, 0].set_ylim([0, 5])
    axes[0, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(avg_ratings):
        axes[0, 0].text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Positive Sentiment Percentage
    pos_sentiment = [(df[(df['bank'] == bank)]['sentiment_label'] == 'POSITIVE').sum() / 
                     len(df[df['bank'] == bank]) * 100 for bank in banks]
    axes[0, 1].bar(banks, pos_sentiment, color=['#2ecc71', '#27ae60', '#16a085'])
    axes[0, 1].set_title('Positive Sentiment Percentage', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Percentage (%)', fontsize=10)
    axes[0, 1].set_ylim([0, 100])
    axes[0, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate(pos_sentiment):
        axes[0, 1].text(i, v + 2, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Review Count
    review_counts = [len(df[df['bank'] == bank]) for bank in banks]
    axes[1, 0].bar(banks, review_counts, color=['#e74c3c', '#c0392b', '#a93226'])
    axes[1, 0].set_title('Total Reviews Collected', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Number of Reviews', fontsize=10)
    axes[1, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(review_counts):
        axes[1, 0].text(i, v + 10, f'{v}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Average Sentiment Score
    avg_sentiment = [df[df['bank'] == bank]['sentiment_score'].mean() for bank in banks]
    axes[1, 1].bar(banks, avg_sentiment, color=['#f39c12', '#e67e22', '#d35400'])
    axes[1, 1].set_title('Average Sentiment Score', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Sentiment Score', fontsize=10)
    axes[1, 1].set_ylim([0, 1])
    axes[1, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate(avg_sentiment):
        axes[1, 1].text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved: {save_path}")
    plt.close()


def create_wordcloud(df, bank_name, sentiment='POSITIVE', save_path=None):
    """Create word cloud for a specific bank and sentiment."""
    bank_df = df[(df['bank'] == bank_name) & (df['sentiment_label'] == sentiment)]
    
    if len(bank_df) == 0:
        print(f"No {sentiment} reviews for {bank_name}")
        return
    
    # Combine all review texts
    text = ' '.join(bank_df['review_text'].astype(str).str.lower())
    
    # Remove common stopwords and short words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
                 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
                 'this', 'that', 'these', 'those', 'it', 'its', 'app', 'bank', 'very'}
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, 
                         background_color='white',
                         stopwords=stopwords,
                         max_words=100,
                         colormap='viridis').generate(text)
    
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'{bank_name} - {sentiment} Reviews Word Cloud', 
              fontsize=14, fontweight='bold', pad=20)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close()


def generate_all_visualizations(df):
    """Generate all visualizations for the report."""
    print("Generating visualizations...")
    
    # 1. Sentiment distribution by bank
    plot_sentiment_distribution_by_bank(df)
    
    # 2. Rating distribution
    plot_rating_distribution_by_bank(df)
    
    # 3. Sentiment trends
    plot_sentiment_trends(df)
    
    # 4. Theme distribution
    plot_theme_distribution(df)
    
    # 5. Bank comparison
    plot_bank_comparison(df)
    
    # 6. Word clouds for each bank (positive reviews)
    banks = df['bank'].unique()
    for bank in banks:
        save_path = f'../../reports/figures/wordcloud_{bank}_positive.png'
        create_wordcloud(df, bank, sentiment='POSITIVE', save_path=save_path)
    
    print("\nAll visualizations generated successfully!")


if __name__ == '__main__':
    print("Loading data...")
    df = load_data()
    
    print(f"Total reviews: {len(df)}")
    print(f"Banks: {df['bank'].unique()}")
    
    generate_all_visualizations(df)

