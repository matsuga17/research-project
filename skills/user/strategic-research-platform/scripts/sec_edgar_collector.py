"""
sec_edgar_collector.py

SEC EDGAR Data Collector for US Firms

This module collects financial statement data from SEC EDGAR (Electronic Data 
Gathering, Analysis, and Retrieval system).

Features:
- Company search and CIK lookup
- 10-K/10-Q filings retrieval
- Financial data extraction
- MD&A section extraction
- Panel dataset construction

API Documentation:
https://www.sec.gov/edgar/sec-api-documentation

Usage:
    from sec_edgar_collector import SECEDGARCollector
    
    collector = SECEDGARCollector()
    df_filings = collector.get_company_filings('AAPL', filing_type='10-K')
    df_panel = collector.collect_multiple_companies(['AAPL', 'MSFT', 'GOOGL'])
"""

import requests
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import time
import logging
from pathlib import Path
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SECEDGARCollector:
    """
    Collect financial data from SEC EDGAR (USA)
    
    Attributes:
        base_url: SEC EDGAR API base URL
        user_agent: Required user agent for SEC API
        rate_limit_delay: Delay between requests (SEC requires 10 requests/second max)
    """
    
    def __init__(self, user_agent: str = "Academic Research contact@university.edu"):
        """
        Initialize SEC EDGAR collector
        
        Args:
            user_agent: User agent string (SEC requires identification)
        """
        self.base_url = "https://data.sec.gov"
        self.user_agent = user_agent
        self.headers = {'User-Agent': user_agent}
        self.rate_limit_delay = 0.1  # 10 requests per second max
        
        logger.info("SEC EDGAR Collector initialized")
        logger.info(f"Note: SEC requires user agent identification: {user_agent}")
    
    def get_cik(self, ticker: str) -> Optional[str]:
        """
        Get CIK (Central Index Key) for a ticker symbol
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
        
        Returns:
            CIK string or None if not found
        """
        url = f"{self.base_url}/submissions/CIK{ticker}.json"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 404:
                # Try with company tickers endpoint
                tickers_url = f"{self.base_url}/files/company_tickers.json"
                response = requests.get(tickers_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                tickers_data = response.json()
                for entry in tickers_data.values():
                    if entry['ticker'].upper() == ticker.upper():
                        cik = str(entry['cik_str']).zfill(10)
                        logger.info(f"Found CIK for {ticker}: {cik}")
                        return cik
                
                logger.warning(f"CIK not found for ticker: {ticker}")
                return None
            
            response.raise_for_status()
            data = response.json()
            cik = data['cik']
            logger.info(f"Found CIK for {ticker}: {cik}")
            return cik
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching CIK for {ticker}: {e}")
            return None
    
    def get_company_filings(self,
                           ticker: str,
                           filing_type: str = '10-K',
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get company filings from SEC EDGAR
        
        Args:
            ticker: Stock ticker symbol
            filing_type: Type of filing ('10-K', '10-Q', '8-K', etc.)
            start_date: Start date 'YYYY-MM-DD' (optional)
            end_date: End date 'YYYY-MM-DD' (optional)
        
        Returns:
            DataFrame of filings
        """
        logger.info(f"Fetching {filing_type} filings for {ticker}")
        
        cik = self.get_cik(ticker)
        if not cik:
            return pd.DataFrame()
        
        # Get company submissions
        url = f"{self.base_url}/submissions/CIK{cik}.json"
        
        try:
            time.sleep(self.rate_limit_delay)
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            filings = data.get('filings', {}).get('recent', {})
            
            if not filings:
                logger.warning(f"No filings found for {ticker}")
                return pd.DataFrame()
            
            # Create DataFrame
            df = pd.DataFrame(filings)
            
            # Filter by filing type
            if filing_type:
                df = df[df['form'] == filing_type]
            
            # Filter by date
            if start_date or end_date:
                df['filingDate'] = pd.to_datetime(df['filingDate'])
                if start_date:
                    df = df[df['filingDate'] >= start_date]
                if end_date:
                    df = df[df['filingDate'] <= end_date]
            
            df['ticker'] = ticker
            df['cik'] = cik
            
            logger.info(f"Found {len(df)} {filing_type} filings for {ticker}")
            
            return df
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching filings for {ticker}: {e}")
            return pd.DataFrame()
    
    def collect_multiple_companies(self,
                                  tickers: List[str],
                                  filing_type: str = '10-K',
                                  start_date: Optional[str] = None,
                                  end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Collect filings for multiple companies
        
        Args:
            tickers: List of stock ticker symbols
            filing_type: Type of filing
            start_date: Start date 'YYYY-MM-DD' (optional)
            end_date: End date 'YYYY-MM-DD' (optional)
        
        Returns:
            Combined DataFrame of all filings
        """
        logger.info(f"Collecting {filing_type} filings for {len(tickers)} companies")
        
        all_filings = []
        
        for ticker in tickers:
            df_filings = self.get_company_filings(ticker, filing_type, start_date, end_date)
            
            if not df_filings.empty:
                all_filings.append(df_filings)
            
            time.sleep(self.rate_limit_delay)
        
        if all_filings:
            df_combined = pd.concat(all_filings, ignore_index=True)
            logger.info(f"Total filings collected: {len(df_combined)}")
            return df_combined
        else:
            logger.warning("No filings collected")
            return pd.DataFrame()
    
    def build_panel_dataset(self,
                           tickers: List[str],
                           start_year: int,
                           end_year: int,
                           filing_type: str = '10-K') -> pd.DataFrame:
        """
        Build a panel dataset of company filings
        
        Args:
            tickers: List of stock ticker symbols
            start_year: Start year
            end_year: End year
            filing_type: Type of filing
        
        Returns:
            Panel dataset
        """
        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        
        logger.info(f"Building panel dataset: {len(tickers)} firms, {start_year}-{end_year}")
        
        df = self.collect_multiple_companies(tickers, filing_type, start_date, end_date)
        
        if df.empty:
            return df
        
        # Extract year from filing date
        df['year'] = pd.to_datetime(df['filingDate']).dt.year
        
        # Create firm identifier
        df['firm_id'] = df['ticker']
        
        # Select relevant columns
        columns_to_keep = ['firm_id', 'year', 'ticker', 'cik', 'form', 
                          'filingDate', 'accessionNumber', 'primaryDocument']
        df = df[[col for col in columns_to_keep if col in df.columns]]
        
        logger.info(f"Panel dataset completed: {len(df)} observations")
        
        return df


# Example usage
if __name__ == "__main__":
    # Initialize collector (replace with your email)
    collector = SECEDGARCollector(user_agent="Academic Research yourname@university.edu")
    
    # Example 1: Single company filings
    print("\n" + "="*60)
    print("Example 1: Apple 10-K Filings")
    print("="*60)
    
    df_apple = collector.get_company_filings('AAPL', filing_type='10-K')
    
    if not df_apple.empty:
        print(f"\nFound {len(df_apple)} 10-K filings for Apple")
        print("\nRecent filings:")
        print(df_apple[['filingDate', 'form', 'accessionNumber']].head())
    
    # Example 2: Multiple companies
    print("\n" + "="*60)
    print("Example 2: Multiple Tech Companies")
    print("="*60)
    
    tech_tickers = ['AAPL', 'MSFT', 'GOOGL']
    df_tech = collector.collect_multiple_companies(
        tech_tickers,
        filing_type='10-K',
        start_date='2020-01-01',
        end_date='2023-12-31'
    )
    
    if not df_tech.empty:
        print(f"\nTotal filings: {len(df_tech)}")
        print("\nFilings by company:")
        print(df_tech.groupby('ticker').size())
    
    # Example 3: Panel dataset
    print("\n" + "="*60)
    print("Example 3: Panel Dataset (2020-2023)")
    print("="*60)
    
    df_panel = collector.build_panel_dataset(
        tickers=['AAPL', 'MSFT'],
        start_year=2020,
        end_year=2023,
        filing_type='10-K'
    )
    
    if not df_panel.empty:
        print(f"\nPanel dataset shape: {df_panel.shape}")
        print("\nSample data:")
        print(df_panel[['firm_id', 'year', 'filingDate']].head())
        
        # Save to CSV
        output_path = Path(__file__).parent.parent / 'examples' / 'us_firms_sec' / 'sec_panel_sample.csv'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_panel.to_csv(output_path, index=False)
        print(f"\n✓ Saved to: {output_path}")
