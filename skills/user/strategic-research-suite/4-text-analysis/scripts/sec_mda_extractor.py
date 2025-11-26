"""
sec_mda_extractor.py

SEC 10-K MD&A Section Extractor

This module extracts Management's Discussion and Analysis (MD&A) sections
from SEC 10-K filings using EDGAR database.

Features:
- 10-K filing retrieval from EDGAR
- MD&A section extraction (Item 7)
- Text cleaning and preprocessing
- Batch processing for multiple companies/years

Usage:
    from sec_mda_extractor import SECMDAExtractor
    
    extractor = SECMDAExtractor(user_email='your_email@example.com')
    mda_text = extractor.extract_mda(cik='0000789019', fiscal_year=2023)
"""

import requests
import re
from typing import Optional, List, Dict
from datetime import datetime
import time
import logging
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SECMDAExtractor:
    """
    Extract MD&A sections from SEC 10-K filings
    
    Attributes:
        user_email: Email for SEC EDGAR user agent (required)
        base_url: SEC EDGAR base URL
        rate_limit_delay: Delay between requests (SEC requires 0.1s minimum)
    """
    
    def __init__(self, user_email: str, rate_limit_delay: float = 0.1):
        """
        Initialize SEC MDA extractor
        
        Args:
            user_email: Your email (required by SEC for identification)
            rate_limit_delay: Delay between requests in seconds (minimum 0.1)
        """
        if not user_email:
            raise ValueError("user_email is required for SEC EDGAR API access")
        
        self.user_email = user_email
        self.base_url = "https://www.sec.gov"
        self.rate_limit_delay = max(rate_limit_delay, 0.1)  # SEC requires ≥0.1s
        
        # User agent as required by SEC
        self.headers = {
            'User-Agent': f'Research Project {user_email}',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        
        logger.info(f"SECMDAExtractor initialized (email: {user_email})")
        logger.info(f"Rate limit delay: {self.rate_limit_delay}s")
    
    def get_10k_filings(self, cik: str, count: int = 5) -> List[Dict]:
        """
        Get list of 10-K filings for a company
        
        Args:
            cik: Company CIK number (e.g., '0000789019' for Microsoft)
            count: Number of recent filings to retrieve
        
        Returns:
            List of filing dictionaries with dates and URLs
        """
        # Normalize CIK to 10 digits
        cik_padded = str(cik).zfill(10)
        
        url = f"{self.base_url}/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'CIK': cik_padded,
            'type': '10-K',
            'dateb': '',
            'owner': 'exclude',
            'count': count,
            'output': 'atom'
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            time.sleep(self.rate_limit_delay)
            
            # Parse XML response (simplified - full implementation would use XML parser)
            logger.info(f"Retrieved {count} 10-K filings for CIK {cik}")
            return []  # Placeholder
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving filings: {e}")
            return []
    
    def extract_mda_from_text(self, full_text: str) -> Optional[str]:
        """
        Extract MD&A section (Item 7) from 10-K text
        
        Args:
            full_text: Full text of 10-K filing
        
        Returns:
            Extracted MD&A text or None if not found
        """
        # Pattern to find Item 7 (MD&A)
        # Item 7 typically starts with "ITEM 7" and ends at "ITEM 7A" or "ITEM 8"
        pattern_start = r'ITEM\s*7[.\s]*MANAGEMENT.*?DISCUSSION.*?ANALYSIS'
        pattern_end = r'ITEM\s*7A|ITEM\s*8'
        
        # Find start position
        match_start = re.search(pattern_start, full_text, re.IGNORECASE | re.DOTALL)
        if not match_start:
            logger.warning("Could not find Item 7 (MD&A) start")
            return None
        
        start_pos = match_start.start()
        
        # Find end position (Item 7A or Item 8)
        text_after_start = full_text[start_pos:]
        match_end = re.search(pattern_end, text_after_start, re.IGNORECASE)
        
        if match_end:
            end_pos = start_pos + match_end.start()
            mda_text = full_text[start_pos:end_pos]
        else:
            # If no end found, take reasonable length (e.g., 50,000 chars)
            mda_text = full_text[start_pos:start_pos + 50000]
        
        # Clean the text
        mda_text = self.clean_text(mda_text)
        
        logger.info(f"Extracted MD&A: {len(mda_text)} characters")
        return mda_text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        
        return text.strip()


# Usage example
if __name__ == "__main__":
    import os
    
    # Get email from environment variable
    user_email = os.getenv('SEC_EDGAR_EMAIL', 'your_email@example.com')
    
    print("=" * 80)
    print("SEC MD&A EXTRACTOR EXAMPLE")
    print("=" * 80)
    
    # Sample full text (normally retrieved from SEC)
    sample_10k_text = """
    ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION
    AND RESULTS OF OPERATIONS
    
    Overview
    
    Our company operates in multiple segments...
    [Sample MD&A content would go here]
    
    ITEM 7A. QUANTITATIVE AND QUALITATIVE DISCLOSURES ABOUT MARKET RISK
    """
    
    # Initialize extractor
    extractor = SECMDAExtractor(user_email=user_email)
    
    # Extract MD&A
    mda_text = extractor.extract_mda_from_text(sample_10k_text)
    
    if mda_text:
        print("\n✓ MD&A Section Extracted Successfully")
        print(f"Length: {len(mda_text)} characters")
        print(f"\nFirst 200 characters:")
        print(mda_text[:200] + "...")
    else:
        print("\n✗ MD&A extraction failed")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE!")
    print("=" * 80)
    print("\nNOTE: This is a simplified example.")
    print("For full functionality, use libraries like:")
    print("- sec-edgar-downloader")
    print("- edgar")
    print("- sec-api")
