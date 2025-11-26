"""
edinet_collector.py

EDINET Data Collector for Japanese Firms

This module collects financial statement data from EDINET (Electronic Disclosure 
for Investors' NETwork), Japan's corporate disclosure system operated by FSA.

Features:
- Document list retrieval
- Securities report collection
- Panel dataset construction
- Automatic rate limiting
- Error handling and retry logic

API Documentation:
https://disclosure.edinet-fsa.go.jp/EKW0EZ0001.html

Usage:
    from edinet_collector import EDINETCollector
    
    collector = EDINETCollector()
    df_docs = collector.get_document_list('2024-01-10')
    df_panel = collector.collect_sample('2024-01-01', '2024-01-31')
"""

import requests
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EDINETCollector:
    """
    Collect financial data from EDINET (Japan)
    
    Attributes:
        api_key: Optional API key (not required for basic access)
        base_url: EDINET API base URL
        rate_limit_delay: Delay between API calls (seconds)
    """
    
    def __init__(self, api_key: Optional[str] = None, rate_limit_delay: float = 1.0):
        """
        Initialize EDINET collector
        
        Args:
            api_key: Optional API key (not required since 2023)
                     If not provided, will try to read from EDINET_API_KEY environment variable
            rate_limit_delay: Delay between API calls in seconds
        """
        import os
        
        # Try to get API key from: 1) parameter, 2) environment variable, 3) None
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('EDINET_API_KEY', None)
        
        self.base_url = "https://disclosure.edinet-fsa.go.jp/api/v1"
        self.rate_limit_delay = rate_limit_delay
        
        logger.info("EDINETCollector initialized")
        logger.info(f"API base URL: {self.base_url}")
        logger.info(f"Rate limit delay: {rate_limit_delay}s")
    
    def get_document_list(self, date: str, doc_type: Optional[str] = None) -> pd.DataFrame:
        """
        Get list of documents submitted on specified date
        
        Args:
            date: Date in 'YYYY-MM-DD' format
            doc_type: Optional document type filter (e.g., '120' for securities report)
        
        Returns:
            DataFrame with document information
        
        Raises:
            requests.exceptions.RequestException: If API call fails
        """
        logger.info(f"Fetching document list for {date}")
        
        # Convert date format: YYYY-MM-DD → YYYYMMDD
        date_formatted = date.replace('-', '')
        
        url = f"{self.base_url}/documents.json"
        params = {
            'date': date_formatted,
            'type': 2  # Type 2: Metadata + Submitted documents
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' not in data or not data['results']:
                logger.warning(f"No documents found for {date}")
                return pd.DataFrame()
            
            df = pd.DataFrame(data['results'])
            
            # Filter by document type if specified
            if doc_type and 'docTypeCode' in df.columns:
                df = df[df['docTypeCode'] == doc_type]
            
            logger.info(f"Retrieved {len(df)} documents")
            
            # Add date column for tracking
            df['retrieval_date'] = date
            
            return df
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout fetching documents for {date}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching documents for {date}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Error parsing JSON response: {e}")
            raise
    
    def collect_sample(self, 
                      start_date: str,
                      end_date: str,
                      doc_type: Optional[str] = '120',
                      delay: Optional[float] = None) -> pd.DataFrame:
        """
        Collect documents over a date range
        
        Args:
            start_date: Start date 'YYYY-MM-DD'
            end_date: End date 'YYYY-MM-DD'
            doc_type: Document type code (default: '120' = securities report)
            delay: Override default rate limit delay
        
        Returns:
            Concatenated DataFrame of all documents
        
        Example:
            collector = EDINETCollector()
            df = collector.collect_sample('2024-01-01', '2024-01-31', doc_type='120')
        """
        logger.info(f"Collecting documents from {start_date} to {end_date}")
        
        if delay is None:
            delay = self.rate_limit_delay
        
        # Generate date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        all_data = []
        success_count = 0
        error_count = 0
        
        for i, date in enumerate(dates, 1):
            date_str = date.strftime('%Y-%m-%d')
            
            try:
                logger.info(f"Processing {date_str} ({i}/{len(dates)})...")
                
                df_docs = self.get_document_list(date_str, doc_type=doc_type)
                
                if len(df_docs) > 0:
                    all_data.append(df_docs)
                    success_count += 1
                
                # Rate limiting
                if i < len(dates):  # Don't delay after last request
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Failed to process {date_str}: {e}")
                error_count += 1
                continue
        
        logger.info(f"Collection completed: {success_count} successful, {error_count} errors")
        
        if all_data:
            df_result = pd.concat(all_data, ignore_index=True)
            logger.info(f"Total documents collected: {len(df_result)}")
            return df_result
        else:
            logger.warning("No documents collected")
            return pd.DataFrame()
    
    def get_securities_reports(self, 
                               edinet_codes: List[str],
                               start_year: int,
                               end_year: int) -> pd.DataFrame:
        """
        Get securities reports for specified firms and years
        
        Note: This is a placeholder for XBRL parsing functionality.
        Full implementation requires XBRL document parsing which is complex.
        
        Args:
            edinet_codes: List of EDINET codes (e.g., ['E01234', 'E05678'])
            start_year: Start year
            end_year: End year
        
        Returns:
            DataFrame with financial data (placeholder structure)
        """
        logger.info(f"Fetching securities reports for {len(edinet_codes)} firms")
        logger.info(f"Year range: {start_year}-{end_year}")
        
        # Placeholder: In production, this would parse XBRL documents
        # For now, return expected structure with NaN values
        
        data = []
        for code in edinet_codes:
            for year in range(start_year, end_year + 1):
                data.append({
                    'edinetCode': code,
                    'year': year,
                    'sales': np.nan,
                    'operating_income': np.nan,
                    'net_income': np.nan,
                    'total_assets': np.nan,
                    'total_equity': np.nan,
                    'total_liabilities': np.nan,
                    'num_employees': np.nan,
                    'rd_expense': np.nan
                })
        
        df = pd.DataFrame(data)
        
        logger.warning("XBRL parsing not implemented - returning placeholder data")
        logger.info(f"Created placeholder dataset: {len(df)} firm-year observations")
        
        return df
    
    def filter_by_industry(self, df: pd.DataFrame, industry_codes: List[str]) -> pd.DataFrame:
        """
        Filter documents by industry classification
        
        Args:
            df: DataFrame from get_document_list() or collect_sample()
            industry_codes: List of industry codes (EDINET classification)
        
        Returns:
            Filtered DataFrame
        """
        if 'industryCode' not in df.columns:
            logger.warning("industryCode column not found - returning original DataFrame")
            return df
        
        df_filtered = df[df['industryCode'].isin(industry_codes)]
        
        logger.info(f"Filtered by industry: {len(df)} → {len(df_filtered)} documents")
        
        return df_filtered
    
    def filter_securities_reports(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter for securities reports (有価証券報告書) only
        
        Args:
            df: DataFrame from get_document_list() or collect_sample()
        
        Returns:
            Filtered DataFrame containing only securities reports
        """
        if 'docDescription' not in df.columns:
            logger.warning("docDescription column not found")
            return df
        
        # Filter for securities reports
        mask = df['docDescription'].str.contains('有価証券報告書', na=False)
        df_filtered = df[mask]
        
        logger.info(f"Filtered for securities reports: {len(df)} → {len(df_filtered)}")
        
        return df_filtered
    
    def extract_firm_list(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract unique firm information from document list
        
        Args:
            df: DataFrame from collect_sample()
        
        Returns:
            DataFrame with unique firms (edinetCode, filerName, etc.)
        """
        if 'edinetCode' not in df.columns:
            logger.error("edinetCode column not found")
            return pd.DataFrame()
        
        # Select relevant columns
        firm_cols = ['edinetCode', 'filerName', 'secCode', 'JCN']
        available_cols = [col for col in firm_cols if col in df.columns]
        
        df_firms = df[available_cols].drop_duplicates(subset=['edinetCode'])
        
        logger.info(f"Extracted {len(df_firms)} unique firms")
        
        return df_firms
    
    def build_panel_dataset(self,
                           edinet_codes: List[str],
                           start_year: int,
                           end_year: int) -> pd.DataFrame:
        """
        Build panel dataset for specified firms and time period
        
        Note: This is a simplified version. Full implementation requires
        XBRL document retrieval and parsing.
        
        Args:
            edinet_codes: List of EDINET codes
            start_year: Start year
            end_year: End year
        
        Returns:
            Panel dataset (firm-year level)
        
        Example:
            collector = EDINETCollector()
            df_panel = collector.build_panel_dataset(
                edinet_codes=['E01234', 'E05678'],
                start_year=2018,
                end_year=2023
            )
        """
        logger.info(f"Building panel dataset...")
        logger.info(f"  Firms: {len(edinet_codes)}")
        logger.info(f"  Years: {start_year}-{end_year}")
        
        df = self.get_securities_reports(edinet_codes, start_year, end_year)
        
        # Add firm_id for consistency with other tools
        df['firm_id'] = pd.Categorical(df['edinetCode']).codes + 1
        
        logger.info(f"Panel dataset created: {len(df)} observations")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filepath: str, **kwargs):
        """
        Save DataFrame to CSV with logging
        
        Args:
            df: DataFrame to save
            filepath: Output file path
            **kwargs: Additional arguments for pd.to_csv()
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(filepath, index=False, **kwargs)
        
        logger.info(f"Data saved to: {filepath}")
        logger.info(f"  Rows: {len(df):,}")
        logger.info(f"  Columns: {len(df.columns)}")


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("EDINET Collector - Example Usage")
    print("=" * 80)
    print()
    
    # Initialize collector
    collector = EDINETCollector(rate_limit_delay=1.0)
    
    # Example 1: Get documents for a single day
    print("[Example 1] Fetching documents for 2024-01-10...")
    try:
        df_single = collector.get_document_list('2024-01-10')
        print(f"✓ Found {len(df_single)} documents")
        
        if len(df_single) > 0:
            print("\nSample documents:")
            print(df_single[['filerName', 'docDescription']].head())
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "-" * 80)
    
    # Example 2: Collect documents over date range (3 days for demo)
    print("[Example 2] Collecting documents for 2024-01-10 to 2024-01-12...")
    try:
        df_range = collector.collect_sample(
            start_date='2024-01-10',
            end_date='2024-01-12',
            doc_type='120'  # Securities reports only
        )
        print(f"✓ Collected {len(df_range)} documents over 3 days")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "-" * 80)
    
    # Example 3: Filter for securities reports
    if len(df_range) > 0:
        print("[Example 3] Filtering for securities reports...")
        df_reports = collector.filter_securities_reports(df_range)
        print(f"✓ Securities reports: {len(df_reports)}")
        
        # Extract firm list
        df_firms = collector.extract_firm_list(df_reports)
        print(f"✓ Unique firms: {len(df_firms)}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Use collect_sample() for longer date ranges")
    print("  2. Extract EDINET codes from document list")
    print("  3. Build panel dataset with build_panel_dataset()")
    print("  4. Implement XBRL parsing for financial data extraction")
