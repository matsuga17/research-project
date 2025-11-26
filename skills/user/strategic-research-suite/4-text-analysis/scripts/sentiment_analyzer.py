"""
sentiment_analyzer.py

Financial Sentiment Analysis for Strategic Research

This module provides comprehensive sentiment analysis tools for financial texts,
including:
- VADER sentiment (general purpose)
- Loughran-McDonald sentiment (financial domain)
- Custom dictionary-based analysis
- Batch processing for large corpora

Usage:
    from sentiment_analyzer import FinancialSentimentAnalyzer
    
    analyzer = FinancialSentimentAnalyzer()
    result = analyzer.analyze_text("The company showed strong performance...")
    print(result['sentiment'])  # 'positive', 'negative', or 'neutral'
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import re
import logging
from pathlib import Path

# Sentiment analysis libraries
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    logging.warning("vaderSentiment not installed. Install with: pip install vaderSentiment")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoughranMcDonaldDictionary:
    """
    Loughran-McDonald Financial Sentiment Dictionary
    
    Source: https://sraf.nd.edu/loughranmcdonald-master-dictionary/
    """
    
    def __init__(self):
        """Initialize with basic financial sentiment word lists"""
        # Simplified word lists (full version should load from external files)
        self.positive_words = {
            'profit', 'profitable', 'profitability', 'growth', 'increase',
            'strong', 'improvement', 'success', 'gain', 'positive',
            'achieve', 'excellent', 'outstanding', 'superior', 'advantage',
            'leading', 'innovation', 'innovative', 'competitive', 'efficient',
            'effective', 'strength', 'opportunity', 'expansion', 'momentum'
        }
        
        self.negative_words = {
            'loss', 'losses', 'decline', 'decrease', 'weak', 'weakness',
            'poor', 'negative', 'fail', 'failure', 'risk', 'risks',
            'concern', 'concerns', 'challenge', 'challenges', 'difficult',
            'difficulty', 'uncertain', 'uncertainty', 'adverse', 'adversely',
            'impair', 'impairment', 'restructuring', 'litigation', 'default'
        }
        
        self.uncertainty_words = {
            'may', 'might', 'could', 'possibly', 'perhaps', 'uncertain',
            'uncertainty', 'risk', 'risks', 'depend', 'depends', 'conditional',
            'approximately', 'estimate', 'estimated', 'believe', 'believes'
        }
        
        logger.info("Loughran-McDonald dictionary initialized")
        logger.info(f"Positive words: {len(self.positive_words)}")
        logger.info(f"Negative words: {len(self.negative_words)}")
        logger.info(f"Uncertainty words: {len(self.uncertainty_words)}")
    
    def count_sentiment(self, text: str) -> Dict[str, int]:
        """Count sentiment word occurrences"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        return {
            'positive': sum(1 for w in words if w in self.positive_words),
            'negative': sum(1 for w in words if w in self.negative_words),
            'uncertainty': sum(1 for w in words if w in self.uncertainty_words),
            'total_words': len(words)
        }


class FinancialSentimentAnalyzer:
    """
    Comprehensive sentiment analyzer for financial texts
    
    Combines multiple sentiment methods:
    - VADER (general purpose, good for social media/informal text)
    - Loughran-McDonald (financial domain-specific)
    - Custom scoring
    """
    
    def __init__(self, method: str = 'both'):
        """
        Initialize sentiment analyzer
        
        Args:
            method: 'vader', 'loughran-mcdonald', or 'both'
        """
        self.method = method
        
        # Initialize VADER
        if method in ['vader', 'both'] and VADER_AVAILABLE:
            self.vader = SentimentIntensityAnalyzer()
            logger.info("VADER sentiment analyzer initialized")
        else:
            self.vader = None
        
        # Initialize Loughran-McDonald
        if method in ['loughran-mcdonald', 'both']:
            self.lm = LoughranMcDonaldDictionary()
        else:
            self.lm = None
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Input text
        
        Returns:
            Dictionary with sentiment scores and classification
        """
        results = {
            'text_length': len(text),
            'word_count': len(text.split())
        }
        
        # VADER analysis
        if self.vader:
            vader_scores = self.vader.polarity_scores(text)
            results['vader'] = vader_scores
            results['vader_compound'] = vader_scores['compound']
            
            # Classification based on compound score
            if vader_scores['compound'] >= 0.05:
                results['vader_sentiment'] = 'positive'
            elif vader_scores['compound'] <= -0.05:
                results['vader_sentiment'] = 'negative'
            else:
                results['vader_sentiment'] = 'neutral'
        
        # Loughran-McDonald analysis
        if self.lm:
            lm_counts = self.lm.count_sentiment(text)
            results['lm_counts'] = lm_counts
            
            # Calculate sentiment ratios
            total_sentiment_words = lm_counts['positive'] + lm_counts['negative']
            if total_sentiment_words > 0:
                results['lm_positive_ratio'] = lm_counts['positive'] / total_sentiment_words
                results['lm_negative_ratio'] = lm_counts['negative'] / total_sentiment_words
            else:
                results['lm_positive_ratio'] = 0.0
                results['lm_negative_ratio'] = 0.0
            
            # Net sentiment score
            results['lm_net_sentiment'] = lm_counts['positive'] - lm_counts['negative']
            
            # Classification
            if lm_counts['positive'] > lm_counts['negative']:
                results['lm_sentiment'] = 'positive'
            elif lm_counts['positive'] < lm_counts['negative']:
                results['lm_sentiment'] = 'negative'
            else:
                results['lm_sentiment'] = 'neutral'
            
            # Uncertainty score
            if lm_counts['total_words'] > 0:
                results['lm_uncertainty_ratio'] = lm_counts['uncertainty'] / lm_counts['total_words']
            else:
                results['lm_uncertainty_ratio'] = 0.0
        
        return results
    
    def analyze_batch(self, texts: List[str]) -> pd.DataFrame:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of texts
        
        Returns:
            DataFrame with sentiment scores for each text
        """
        logger.info(f"Analyzing {len(texts)} texts...")
        
        results = []
        for i, text in enumerate(texts):
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(texts)} texts")
            
            result = self.analyze_text(text)
            result['text_id'] = i
            results.append(result)
        
        df = pd.DataFrame(results)
        logger.info(f"✓ Batch analysis complete: {len(df)} texts")
        
        return df


# Usage example
if __name__ == "__main__":
    # Example texts
    texts = [
        "The company reported strong revenue growth and exceeded expectations.",
        "Declining sales and operational challenges led to significant losses.",
        "Uncertainty remains regarding future market conditions and profitability."
    ]
    
    # Initialize analyzer
    analyzer = FinancialSentimentAnalyzer(method='both')
    
    # Analyze single text
    print("\n" + "="*80)
    print("SINGLE TEXT ANALYSIS EXAMPLE")
    print("="*80)
    result = analyzer.analyze_text(texts[0])
    print(f"\nText: {texts[0]}")
    print(f"\nVADER Sentiment: {result.get('vader_sentiment', 'N/A')}")
    print(f"VADER Compound Score: {result.get('vader_compound', 'N/A'):.3f}")
    print(f"\nLM Sentiment: {result.get('lm_sentiment', 'N/A')}")
    print(f"LM Net Sentiment: {result.get('lm_net_sentiment', 'N/A')}")
    print(f"LM Uncertainty Ratio: {result.get('lm_uncertainty_ratio', 0):.3f}")
    
    # Batch analysis
    print("\n" + "="*80)
    print("BATCH ANALYSIS EXAMPLE")
    print("="*80)
    df_results = analyzer.analyze_batch(texts)
    
    print("\nResults Summary:")
    print(df_results[['vader_sentiment', 'lm_sentiment', 'lm_net_sentiment']].to_string())
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
