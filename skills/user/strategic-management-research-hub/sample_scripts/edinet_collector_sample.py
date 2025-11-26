"""
Sample Data Collection Script for Japanese Firms
EDINET API Integration for Strategic Management Research

This script demonstrates how to collect financial data from EDINET
(Electronic Disclosure for Investors' NETwork), Japan's official
corporate disclosure system.

Usage:
    python edinet_collector_sample.py --start_date 2020-01-01 --end_date 2023-12-31

Author: Strategic Management Research Hub v3.0
License: MIT
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EDINETCollector:
    """
    EDINET API client for collecting Japanese corporate financial data.
    
    Data Sources:
    - Financial statements (BS, PL, CF)
    - Corporate governance reports
    - Segment information (for diversification analysis)
    """
    
    BASE_URL = "https://disclosure2.edinet-fsa.go.jp/api/v2"
    
    def __init__(self, rate_limit: int = 10):
        """
        Initialize EDINET collector.
        
        Args:
            rate_limit: Max requests per minute (default: 10 for free tier)
        """
        self.rate_limit = rate_limit
        self.request_count = 0
        self.last_request_time = datetime.now()
        
    def _rate_limit_check(self):
        """Enforce rate limiting."""
        self.request_count += 1
        
        # Reset counter every minute
        if (datetime.now() - self.last_request_time).seconds >= 60:
            self.request_count = 0
            self.last_request_time = datetime.now()
        
        # Wait if limit reached
        if self.request_count >= self.rate_limit:
            wait_time = 60 - (datetime.now() - self.last_request_time).seconds
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = datetime.now()
    
    def get_document_list(self, date: str, doc_type: int = 2) -> Optional[Dict]:
        """
        Get list of documents submitted on a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            doc_type: 2 = 有価証券報告書 (Annual Securities Report)
        
        Returns:
            JSON response with document list
        """
        self._rate_limit_check()
        
        endpoint = f"{self.BASE_URL}/documents.json"
        params = {
            'date': date,
            'type': doc_type
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching document list for {date}: {e}")
            return None
    
    def extract_financials(self, doc_id: str) -> Optional[Dict]:
        """
        Extract financial data from a document.
        
        Args:
            doc_id: EDINET document ID
        
        Returns:
            Dictionary with extracted financial metrics
        """
        self._rate_limit_check()
        
        endpoint = f"{self.BASE_URL}/documents/{doc_id}"
        params = {'type': 5}  # XBRL format
        
        try:
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XBRL (simplified - use xbrl-parser for production)
            # This is a placeholder - actual XBRL parsing is complex
            financials = self._parse_xbrl_simple(response.content)
            return financials
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching document {doc_id}: {e}")
            return None
    
    def _parse_xbrl_simple(self, xbrl_content: bytes) -> Dict:
        """
        Simplified XBRL parser for demonstration.
        
        For production use, consider:
        - Arelle (Python XBRL processor)
        - py-xbrl library
        
        Returns:
            Dictionary with key financial metrics
        """
        # This is a simplified placeholder
        # Real implementation would parse XBRL tags properly
        return {
            'total_assets': None,
            'sales': None,
            'net_income': None,
            'operating_income': None,
            'total_liabilities': None,
            'shareholders_equity': None,
            'rd_expenditure': None,
            'num_employees': None
        }
    
    def collect_sample(
        self, 
        start_date: str, 
        end_date: str,
        industry_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Collect financial data for a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            industry_codes: List of industry codes to filter (optional)
        
        Returns:
            DataFrame with collected financial data
        """
        logger.info(f"Collecting data from {start_date} to {end_date}")
        
        # Generate date range
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        all_data = []
        total_docs = 0
        successful = 0
        
        for date in date_range:
            date_str = date.strftime('%Y-%m-%d')
            logger.info(f"Processing {date_str}...")
            
            # Get document list for this date
            doc_list = self.get_document_list(date_str)
            
            if not doc_list or 'results' not in doc_list:
                continue
            
            # Process each document
            for doc in doc_list['results']:
                total_docs += 1
                
                # Industry filter (if specified)
                if industry_codes and doc.get('ordinanceCode') not in industry_codes:
                    continue
                
                # Extract financials
                financials = self.extract_financials(doc['docID'])
                
                if financials:
                    # Add metadata
                    financials['doc_id'] = doc['docID']
                    financials['company_code'] = doc.get('edinetCode')
                    financials['company_name'] = doc.get('filerName')
                    financials['fiscal_year_end'] = doc.get('periodEnd')
                    financials['submission_date'] = date_str
                    
                    all_data.append(financials)
                    successful += 1
                
                # Respectful delay
                time.sleep(0.5)
        
        logger.info(f"Completed: {successful}/{total_docs} documents processed")
        
        return pd.DataFrame(all_data)


def construct_strategy_variables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construct strategic management research variables.
    
    Args:
        df: Raw financial data DataFrame
    
    Returns:
        DataFrame with constructed variables
    """
    logger.info("Constructing strategic variables...")
    
    df = df.copy()
    
    # Performance variables
    df['roa'] = df['net_income'] / df['total_assets']
    df['ros'] = df['net_income'] / df['sales']
    df['asset_turnover'] = df['sales'] / df['total_assets']
    
    # Financial controls
    df['leverage'] = df['total_liabilities'] / df['total_assets']
    df['firm_size'] = np.log(df['total_assets'])
    
    # Innovation intensity
    df['rd_intensity'] = df['rd_expenditure'] / df['sales']
    df['rd_intensity'].fillna(0, inplace=True)
    df['rd_missing'] = df['rd_expenditure'].isna().astype(int)
    
    # Winsorize continuous variables
    from scipy.stats.mstats import winsorize
    continuous_vars = ['roa', 'ros', 'leverage']
    
    for var in continuous_vars:
        df[f'{var}_winsor'] = winsorize(
            df[var].dropna(), 
            limits=[0.01, 0.01]
        )
    
    logger.info("Variable construction complete")
    
    return df


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Collect financial data from EDINET'
    )
    parser.add_argument(
        '--start_date', 
        type=str, 
        required=True,
        help='Start date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--end_date', 
        type=str, 
        required=True,
        help='End date (YYYY-MM-DD)'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='edinet_data.csv',
        help='Output file path'
    )
    parser.add_argument(
        '--industries',
        type=str,
        nargs='+',
        help='Industry codes to filter (e.g., 010 for manufacturing)'
    )
    
    args = parser.parse_args()
    
    # Initialize collector
    collector = EDINETCollector(rate_limit=10)
    
    # Collect data
    df_raw = collector.collect_sample(
        start_date=args.start_date,
        end_date=args.end_date,
        industry_codes=args.industries
    )
    
    if df_raw.empty:
        logger.error("No data collected. Check date range and filters.")
        return
    
    # Construct variables
    df_final = construct_strategy_variables(df_raw)
    
    # Save
    df_final.to_csv(args.output, index=False, encoding='utf-8-sig')
    logger.info(f"Data saved to {args.output}")
    logger.info(f"Total observations: {len(df_final)}")
    logger.info(f"Unique companies: {df_final['company_code'].nunique()}")


if __name__ == "__main__":
    import numpy as np
    main()
