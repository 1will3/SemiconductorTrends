import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Color schemes
SENTIMENT_COLORS = {
    'Strong Negative': '#8b0000',    # dark red
    'Moderate Negative': '#ff6666',  # light red
    'Neutral': '#808080',           # grey
    'Moderate Positive': '#90EE90',  # light green
    'Strong Positive': '#006400'     # dark green
}

# Colors will be dynamically assigned to topics based on names in the data
TOPIC_COLORS = {}

def assign_topic_colors(df):
    """Dynamically assign colors to topics from color palette"""
    unique_topics = df['topic_name'].unique()
    palette = sns.color_palette("husl", n_colors=len(unique_topics))
    return dict(zip(unique_topics, palette))

def plot_sentiment_distribution(df):
    plt.figure(figsize=(10, 6))
    order = ['Strong Negative', 'Moderate Negative', 'Neutral', 
             'Moderate Positive', 'Strong Positive']
    
    sentiment_counts = df['sentiment_category'].value_counts()
    total = len(df)
    
    ax = sns.barplot(x=order, 
                    y=[sentiment_counts.get(cat, 0) for cat in order],
                    palette=[SENTIMENT_COLORS[cat] for cat in order])
    
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        ax.annotate(percentage, (p.get_x() + p.get_width()/2., p.get_height()),
                   ha='center', va='bottom')
    
    plt.title('Distribution of Sentiment in Research Papers')
    plt.xlabel('Sentiment Category')
    plt.ylabel('Number of Papers')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sentiment_distribution.png')
    plt.close()

def plot_sentiment_over_time(df):
    df['year'] = pd.to_datetime(df['published']).dt.year
    yearly_sentiment = df.groupby('year')['compound_score'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly_sentiment, x='year', y='compound_score', marker='o')
    plt.title('Average Sentiment Over Time')
    plt.xlabel('Year')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('sentiment_over_time.png')
    plt.close()

def plot_technical_confidence(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='technical_confidence', bins=20)
    plt.title('Distribution of Technical Confidence')
    plt.xlabel('Technical Confidence Score')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('technical_confidence.png')
    plt.close()

def plot_result_strength_impact(df):
    plt.figure(figsize=(10, 6))
    plt.hexbin(df['result_strength'], df['citation_impact'],
               gridsize=20, cmap='YlOrRd', mincnt=1)
    plt.colorbar(label='Number of Papers')
    
    plt.title('Result Strength vs Citation Impact')
    plt.xlabel('Result Strength')
    plt.ylabel('Citation Impact')
    plt.tight_layout()
    plt.savefig('result_strength_impact.png')
    plt.close()

def plot_publication_trend(df):
    """Visualize the number of publications over time with enhanced styling"""
    df['year'] = pd.to_datetime(df['published']).dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    
    # Create line plot with points
    plt.plot(yearly_counts.index, yearly_counts.values, 
            marker='o', color='#2E86C1', linewidth=2, markersize=8)
    
    # Calculate year-over-year growth
    yoy_growth = yearly_counts.pct_change() * 100
    
    # Annotate with growth rates
    for i in range(1, len(yearly_counts)):
        if not np.isnan(yoy_growth.iloc[i]):
            plt.annotate(f'{yoy_growth.iloc[i]:.1f}%', 
                        (yearly_counts.index[i], yearly_counts.iloc[i]),
                        textcoords="offset points", 
                        xytext=(0,10), 
                        ha='center')
    
    plt.title('Number of Publications Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.grid(True, alpha=0.3)
    
    # Add total publications count
    total_pubs = len(df)
    plt.text(0.02, 0.98, f'Total Publications: {total_pubs:,}',
             transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    plt.tight_layout()
    plt.savefig('publication_trend.png')
    plt.close()

def plot_topic_distribution(df, topic_colors):
    plt.figure(figsize=(12, 6))
    topic_counts = df['topic_name'].value_counts()
    
    ax = sns.barplot(x=topic_counts.index, y=topic_counts.values,
                    palette=[topic_colors[topic] for topic in topic_counts.index])
    
    total = len(df)
    for p in ax.patches:
        percentage = f'{100 * p.get_height() / total:.1f}%'
        ax.annotate(percentage, (p.get_x() + p.get_width()/2., p.get_height()),
                   ha='center', va='bottom')
    
    plt.title('Distribution of Research Topics')
    plt.xlabel('Topic')
    plt.ylabel('Number of Papers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('topic_distribution.png')
    plt.close()

def plot_topics_over_time(df, topic_colors):
    df['year'] = pd.to_datetime(df['published']).dt.year
    topic_year_counts = df.groupby(['year', 'topic_name']).size().unstack(fill_value=0)
    topic_year_props = topic_year_counts.div(topic_year_counts.sum(axis=1), axis=0)
    
    plt.figure(figsize=(12, 6))
    for topic in topic_year_props.columns:
        plt.plot(topic_year_props.index, topic_year_props[topic],
                marker='o', label=topic, color=topic_colors[topic])
    
    plt.title('Topic Proportions Over Time')
    plt.xlabel('Year')
    plt.ylabel('Proportion of Topics')
    plt.legend(title='Topic', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('topics_over_time.png')
    plt.close()

def plot_topic_sentiment_correlation(df, topic_colors):
    topic_sentiment = df.groupby('topic_name')['compound_score'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='topic_name', y='compound_score', data=topic_sentiment,
                    palette=[topic_colors[topic] for topic in topic_sentiment['topic_name']])
    
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    
    # Add sentiment level indicators
    plt.text(plt.xlim()[1], 0.3, 'Strong Positive (>0.3)', ha='right')
    plt.text(plt.xlim()[1], 0.1, 'Moderate Positive (0.1-0.3)', ha='right')
    plt.text(plt.xlim()[1], 0, 'Neutral (-0.1-0.1)', ha='right')
    plt.text(plt.xlim()[1], -0.2, 'Moderate Negative (-0.3--0.1)', ha='right')
    plt.text(plt.xlim()[1], -0.4, 'Strong Negative (<-0.3)', ha='right')
    
    plt.title('Average Sentiment by Topic')
    plt.xlabel('Topic')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('topic_sentiment_correlation.png')
    plt.close()

if __name__ == "__main__":
    logging.info("Loading data...")
    df = pd.read_csv('arxiv_semiconductors_with_topics.csv')
    
    # Assign colors to topics
    topic_colors = assign_topic_colors(df)
    
    logging.info("Creating sentiment visualizations...")
    plot_sentiment_distribution(df)
    plot_sentiment_over_time(df)
    plot_technical_confidence(df)
    plot_result_strength_impact(df)
    
    logging.info("Creating publication trend visualization...")
    plot_publication_trend(df)
    
    logging.info("Creating topic visualizations...")
    plot_topic_distribution(df, topic_colors)
    plot_topics_over_time(df, topic_colors)
    plot_topic_sentiment_correlation(df, topic_colors)
    
    logging.info("All visualizations completed!")