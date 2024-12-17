import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Scientific sentiment indicators combining VADER, Yu, and Athar approaches
SCIENTIFIC_INDICATORS = {
    'positive': {
        'breakthrough': 4.0,
        'revolutionary': 4.0,
        'exceptional': 4.0,
        'outperform': 3.0,
        'superior': 3.0,
        'novel': 3.0,
        'innovative': 3.0,
        'improve': 2.0,
        'enhance': 2.0,
        'efficient': 2.0,
        'effective': 2.0,
        'successful': 2.0,
        'promising': 1.0,
        'consistent': 1.0,
        'reasonable': 1.0
    },
    'negative': {
        'incorrect': -4.0,
        'invalid': -4.0,
        'mistake': -4.0,
        'fail': -3.0,
        'poor': -3.0,
        'defect': -3.0,
        'limited': -2.0,
        'difficult': -2.0,
        'challenge': -2.0,
        'problem': -2.0,
        'unclear': -1.0,
        'although': -1.0,
        'however': -1.0
    },
    'intensifiers': {
        'significantly': 0.293,
        'substantially': 0.293,
        'considerably': 0.293,
        'clearly': 0.267,
        'particularly': 0.267,
        'especially': 0.267,
        'generally': -0.293,
        'relatively': -0.293,
        'somewhat': -0.293
    },
    'result_markers': {
        'demonstrate': 0.8,
        'prove': 1.0,
        'show': 0.6,
        'indicate': 0.4,
        'suggest': 0.2,
        'may': -0.2,
        'might': -0.2,
        'could': -0.2
    }
}

class ScientificSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def _count_citations(self, text):
        """Count number of citations as a measure of scholarly impact"""
        citation_pattern = r'\[\d+\]|\(\d{4}\)'
        return len(re.findall(citation_pattern, text))

    def _analyze_technical_confidence(self, text):
        """Analyze the confidence level in technical claims"""
        words = text.lower().split()
        score = 0

        for word in words:
            for category, indicators in SCIENTIFIC_INDICATORS.items():
                if word in indicators:
                    score += indicators[word]

        return max(min(score / 5, 1), -1)

    def _analyze_result_strength(self, text):
        """Analyze the strength of reported results"""
        quant_pattern = r'\d+(\.\d+)?%|p\s*<\s*0\.\d+|>\s*\d+(\.\d+)?'
        statistical_terms = r'\b(significant|correlation|confidence|precision|accuracy)\b'
        
        quant_count = len(re.findall(quant_pattern, text, re.IGNORECASE))
        stat_count = len(re.findall(statistical_terms, text, re.IGNORECASE))
        
        return min((quant_count + stat_count) / 5, 1)

    def analyze_sentiment(self, text):
        """Comprehensive scientific sentiment analysis"""
        base_scores = self.sia.polarity_scores(text)
        technical_confidence = self._analyze_technical_confidence(text)
        result_strength = self._analyze_result_strength(text)
        citation_impact = min(self._count_citations(text) / 10, 1)

        compound_score = (
            base_scores['compound'] * 0.2 +     # Base sentiment
            technical_confidence * 0.5 +         # Technical confidence
            result_strength * 0.25 +            # Result strength
            citation_impact * 0.05              # Citation impact
        )

        return {
            'compound': compound_score,
            'technical_confidence': technical_confidence,
            'result_strength': result_strength,
            'citation_impact': citation_impact,
            'base_sentiment': base_scores['compound']
        }

def categorize_scientific_sentiment(scores):
    """Categorize sentiment with scientific context"""
    compound = scores['compound']
    confidence = scores['technical_confidence']
    
    if compound >= 0.1 and confidence > 0:
        if compound >= 0.3:
            return 'Strong Positive'
        return 'Moderate Positive'
    elif compound <= -0.1 and confidence < 0:
        if compound <= -0.3:
            return 'Strong Negative'
        return 'Moderate Negative'
    return 'Neutral'

def analyze_sentiment_dataframe(df):
    """Apply scientific sentiment analysis to the dataframe"""
    analyzer = ScientificSentimentAnalyzer()
    logging.info("Performing scientific sentiment analysis...")
    
    df['sentiment_scores'] = df['abstract'].apply(analyzer.analyze_sentiment)
    df['compound_score'] = df['sentiment_scores'].apply(lambda x: x['compound'])
    df['technical_confidence'] = df['sentiment_scores'].apply(lambda x: x['technical_confidence'])
    df['result_strength'] = df['sentiment_scores'].apply(lambda x: x['result_strength'])
    df['citation_impact'] = df['sentiment_scores'].apply(lambda x: x['citation_impact'])
    df['sentiment_category'] = df['sentiment_scores'].apply(categorize_scientific_sentiment)
    
    return df

if __name__ == "__main__":
    df = pd.read_csv('arxiv_semiconductors_preprocessed.csv')
    df_with_sentiment = analyze_sentiment_dataframe(df)
    
    output_file = f'arxiv_semiconductors_with_sentiment.csv'
    df_with_sentiment.to_csv(output_file, index=False)

    print("\nScientific Sentiment Analysis Summary:")
    print(f"Total papers analyzed: {len(df_with_sentiment)}")
    print("\nSentiment Distribution:")
    print(df_with_sentiment['sentiment_category'].value_counts(normalize=True).round(3))
    
    print("\nAverage Metrics:")
    print(f"Technical Confidence: {df_with_sentiment['technical_confidence'].mean():.3f}")
    print(f"Result Strength: {df_with_sentiment['result_strength'].mean():.3f}")
    print(f"Citation Impact: {df_with_sentiment['citation_impact'].mean():.3f}")
    
    print("\nExample of Strong Positive Paper:")
    positive_example = df_with_sentiment[df_with_sentiment['sentiment_category'] == 'Strong Positive'].iloc[0]
    print(f"Title: {positive_example['title']}")
    print(f"Scores: {positive_example['sentiment_scores']}\n")
    
    print("\nExample of Strong Negative Paper:")
    negative_example = df_with_sentiment[df_with_sentiment['sentiment_category'] == 'Strong Negative'].iloc[0]
    print(f"Title: {negative_example['title']}")
    print(f"Scores: {negative_example['sentiment_scores']}")

    logging.info("Analysis complete!")