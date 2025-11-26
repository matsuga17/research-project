"""
analyze_earnings_calls.py

Sentiment Analysis of Earnings Call Transcripts - Basic Example

This script demonstrates how to:
1. Load earnings call transcripts
2. Analyze sentiment using both VADER and Loughran-McDonald
3. Track sentiment changes over time
4. Visualize results

Usage:
    cd 4-text-analysis/examples/sentiment_analysis_basic/
    python3 analyze_earnings_calls.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from sentiment_analyzer import FinancialSentimentAnalyzer

# Optional: matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not installed. Visualizations disabled.")


def generate_sample_transcripts():
    """Generate sample earnings call excerpts for demonstration"""
    transcripts = [
        {
            'quarter': 'Q1 2023',
            'text': 'We delivered strong performance with revenue growth exceeding expectations. Our innovative products gained significant market share, and profitability improved substantially.'
        },
        {
            'quarter': 'Q2 2023',
            'text': 'Revenue continued to grow, although at a slower pace. Market uncertainty affected our expansion plans, but we remain cautiously optimistic about the future.'
        },
        {
            'quarter': 'Q3 2023',
            'text': 'We faced significant challenges this quarter. Declining sales and increased competition led to disappointing results. We are implementing restructuring measures to address these issues.'
        },
        {
            'quarter': 'Q4 2023',
            'text': 'After a difficult period, we see signs of recovery. Our strategic initiatives are beginning to show positive results, with improved operational efficiency and customer satisfaction.'
        }
    ]
    
    return pd.DataFrame(transcripts)


def main():
    print("=" * 80)
    print("EARNINGS CALL SENTIMENT ANALYSIS EXAMPLE")
    print("=" * 80)
    
    # Step 1: Generate sample data
    print("\n[Step 1] Loading earnings call transcripts...")
    df = generate_sample_transcripts()
    print(f"✓ Loaded {len(df)} quarterly transcripts")
    
    # Step 2: Initialize sentiment analyzer
    print("\n[Step 2] Initializing sentiment analyzer...")
    analyzer = FinancialSentimentAnalyzer(method='both')
    print("✓ Analyzer initialized (VADER + Loughran-McDonald)")
    
    # Step 3: Analyze sentiment
    print("\n[Step 3] Analyzing sentiment...")
    results = analyzer.analyze_batch(df['text'].tolist())
    
    # Combine with original data
    df_analysis = pd.concat([df.reset_index(drop=True), results], axis=1)
    
    # Step 4: Display results
    print("\n[Step 4] Results Summary")
    print("-" * 80)
    print("\nSentiment Scores by Quarter:")
    print(df_analysis[['quarter', 'vader_compound', 'lm_net_sentiment', 
                       'vader_sentiment', 'lm_sentiment']].to_string(index=False))
    
    # Step 5: Save results
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    df_analysis.to_csv(output_dir / 'sentiment_analysis_results.csv', index=False)
    print(f"\n✓ Results saved to: {output_dir / 'sentiment_analysis_results.csv'}")
    
    # Step 6: Visualize (if matplotlib available)
    if MATPLOTLIB_AVAILABLE:
        print("\n[Step 5] Creating visualization...")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # VADER sentiment over time
        ax1.plot(df_analysis['quarter'], df_analysis['vader_compound'], 'bo-', linewidth=2)
        ax1.axhline(y=0, color='r', linestyle='--', alpha=0.3)
        ax1.set_xlabel('Quarter')
        ax1.set_ylabel('VADER Compound Score')
        ax1.set_title('VADER Sentiment Trend')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Loughran-McDonald sentiment over time
        ax2.plot(df_analysis['quarter'], df_analysis['lm_net_sentiment'], 'go-', linewidth=2)
        ax2.axhline(y=0, color='r', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Quarter')
        ax2.set_ylabel('LM Net Sentiment')
        ax2.set_title('Loughran-McDonald Sentiment Trend')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_dir / 'sentiment_trend.png', dpi=300, bbox_inches='tight')
        print(f"✓ Visualization saved to: {output_dir / 'sentiment_trend.png'}")
        plt.close()
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)


if __name__ == "__main__":
    main()
