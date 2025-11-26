"""
Data Collection Template for Strategic & Organizational Research
=================================================================

This script provides a template for collecting firm-level data
from multiple free sources for strategy research.

Author: Strategic & Organizational Research Hub
License: Apache 2.0
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import List, Dict, Optional

# ============================================================================
# Configuration
# ============================================================================

CONFIG = {
    "output_dir": "data/",
    "log_file": "data_collection.log",
    "rate_limit_delay": 1.0,  # seconds between API requests
    "max_retries": 3,
    "timeout": 30  # seconds
}

# ============================================================================
# Utility Functions
# ============================================================================

def log_message(message: str, level: str = "INFO"):
    """Log a message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    # Append to log file
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def safe_api_call(url: str, params: Dict = None, headers: Dict = None, 
                  method: str = "GET") -> Optional[requests.Response]:
    """
    Make an API call with error handling and retry logic
    """
    for attempt in range(CONFIG["max_retries"]):
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, 
                                      timeout=CONFIG["timeout"])
            elif method == "POST":
                response = requests.post(url, json=params, headers=headers, 
                                       timeout=CONFIG["timeout"])
            
            response.raise_for_status()
            time.sleep(CONFIG["rate_limit_delay"])  # Rate limiting
            return response
            
        except requests.exceptions.RequestException as e:
            log_message(f"Attempt {attempt + 1} failed: {e}", "WARNING")
            if attempt == CONFIG["max_retries"] - 1:
                log_message(f"All retries failed for {url}", "ERROR")
                return None
            time.sleep(2 ** attempt)  # Exponential backoff

# ============================================================================
# SEC EDGAR Data Collection (U.S. Companies)
# ============================================================================

class SECEDGARCollector:
    """
    Collect data from SEC EDGAR (free, no API key required)
    """
    
    def __init__(self):
        self.base_url = "https://www.sec.gov"
        self.headers = {
            "User-Agent": "YourUniversity Research [email@university.edu]"
        }
        
    def get_company_cik(self, ticker: str) -> Optional[str]:
        """Get CIK (Central Index Key) from ticker symbol"""
        # Using SEC's company tickers JSON file
        url = "https://www.sec.gov/files/company_tickers.json"
        response = safe_api_call(url, headers=self.headers)
        
        if response:
            companies = response.json()
            for company in companies.values():
                if company['ticker'].upper() == ticker.upper():
                    cik = str(company['cik_str']).zfill(10)
                    return cik
        return None
    
    def get_10k_filings(self, cik: str, count: int = 10) -> List[Dict]:
        """
        Get list of 10-K filings for a company
        """
        url = f"{self.base_url}/cgi-bin/browse-edgar"
        params = {
            "action": "getcompany",
            "CIK": cik,
            "type": "10-K",
            "count": count,
            "output": "atom"
        }
        
        response = safe_api_call(url, params=params, headers=self.headers)
        if response:
            # Parse XML/Atom feed (simplified)
            log_message(f"Retrieved 10-K filings for CIK {cik}")
            # Implementation would parse XML here
            return []
        return []

# ============================================================================
# USPTO Patent Data Collection
# ============================================================================

class USPTOPatentCollector:
    """
    Collect patent data from USPTO PatentsView API (free)
    """
    
    def __init__(self):
        self.base_url = "https://api.patentsview.org/patents/query"
    
    def get_patents_by_assignee(self, company_name: str, 
                                 start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get patents for a company in a date range
        
        Args:
            company_name: Company name (e.g., "Apple Inc")
            start_date: YYYY-MM-DD
            end_date: YYYY-MM-DD
        """
        query = {
            "q": {
                "_and": [
                    {"assignee_organization": company_name},
                    {"_gte": {"patent_date": start_date}},
                    {"_lte": {"patent_date": end_date}}
                ]
            },
            "f": [
                "patent_number",
                "patent_title",
                "patent_date",
                "cited_patent_count",
                "assignee_organization",
                "cpc_section_id"
            ],
            "o": {
                "per_page": 10000
            }
        }
        
        response = safe_api_call(self.base_url, params=query, method="POST")
        
        if response:
            data = response.json()
            patents = data.get("patents", [])
            log_message(f"Retrieved {len(patents)} patents for {company_name}")
            return pd.DataFrame(patents)
        
        return pd.DataFrame()
    
    def calculate_patent_metrics(self, patents_df: pd.DataFrame) -> Dict:
        """
        Calculate patent-based innovation metrics
        """
        if patents_df.empty:
            return {
                "patent_count": 0,
                "citation_weighted_patents": 0,
                "tech_diversity": 0
            }
        
        metrics = {
            "patent_count": len(patents_df),
            "citation_weighted_patents": patents_df["cited_patent_count"].sum(),
            "tech_diversity": patents_df["cpc_section_id"].nunique()
        }
        
        return metrics

# ============================================================================
# World Bank Data Collection
# ============================================================================

class WorldBankCollector:
    """
    Collect macroeconomic data from World Bank (free)
    """
    
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
    
    def get_indicator(self, country_code: str, indicator: str, 
                     start_year: int, end_year: int) -> pd.DataFrame:
        """
        Get World Bank indicator data
        
        Args:
            country_code: ISO 3-letter code (e.g., "USA", "JPN")
            indicator: Indicator code (e.g., "NY.GDP.MKTP.CD" for GDP)
            start_year: Start year
            end_year: End year
        """
        url = f"{self.base_url}/country/{country_code}/indicator/{indicator}"
        params = {
            "date": f"{start_year}:{end_year}",
            "format": "json",
            "per_page": 1000
        }
        
        response = safe_api_call(url, params=params)
        
        if response and response.json():
            data = response.json()[1]  # Skip metadata
            df = pd.DataFrame(data)
            df = df[["date", "value"]].rename(columns={"date": "year", "value": indicator})
            log_message(f"Retrieved {indicator} for {country_code}")
            return df
        
        return pd.DataFrame()

# ============================================================================
# EDINET Data Collection (Japan)
# ============================================================================

class EDINETCollector:
    """
    Collect data from Japan's EDINET system (free)
    """
    
    def __init__(self):
        self.base_url = "https://disclosure2.edinet-fsa.go.jp/api/v2"
    
    def get_documents_by_date(self, date: str, doc_type: int = 2) -> List[Dict]:
        """
        Get documents submitted on a specific date
        
        Args:
            date: YYYY-MM-DD
            doc_type: 2 = 有価証券報告書 (Annual Report)
        """
        url = f"{self.base_url}/documents.json"
        params = {
            "date": date,
            "type": doc_type
        }
        
        response = safe_api_call(url, params=params)
        
        if response:
            data = response.json()
            documents = data.get("results", [])
            log_message(f"Retrieved {len(documents)} documents for {date}")
            return documents
        
        return []

# ============================================================================
# Data Integration
# ============================================================================

class DataIntegrator:
    """
    Integrate data from multiple sources
    """
    
    @staticmethod
    def merge_firm_data(financial_df: pd.DataFrame, patent_df: pd.DataFrame,
                       merge_key: str = "company_name") -> pd.DataFrame:
        """
        Merge financial and patent data
        """
        merged = financial_df.merge(patent_df, on=merge_key, how="left")
        log_message(f"Merged data: {len(merged)} observations")
        return merged
    
    @staticmethod
    def add_macro_controls(firm_df: pd.DataFrame, macro_df: pd.DataFrame,
                          country_col: str, year_col: str) -> pd.DataFrame:
        """
        Add country-level macroeconomic controls
        """
        merged = firm_df.merge(macro_df, 
                              left_on=[country_col, year_col],
                              right_on=["country", "year"],
                              how="left")
        return merged

# ============================================================================
# Example Workflow
# ============================================================================

def example_workflow():
    """
    Example: Collect data for top 10 tech companies
    """
    log_message("Starting data collection workflow")
    
    # 1. Define sample
    companies = [
        {"name": "Apple Inc", "ticker": "AAPL"},
        {"name": "Microsoft Corporation", "ticker": "MSFT"},
        {"name": "Alphabet Inc", "ticker": "GOOGL"}
    ]
    
    # 2. Collect patent data
    patent_collector = USPTOPatentCollector()
    patent_data = []
    
    for company in companies:
        patents = patent_collector.get_patents_by_assignee(
            company["name"], 
            start_date="2020-01-01", 
            end_date="2023-12-31"
        )
        metrics = patent_collector.calculate_patent_metrics(patents)
        metrics["company_name"] = company["name"]
        patent_data.append(metrics)
    
    patent_df = pd.DataFrame(patent_data)
    
    # 3. Collect macroeconomic data
    wb_collector = WorldBankCollector()
    gdp_data = wb_collector.get_indicator("USA", "NY.GDP.MKTP.CD", 2020, 2023)
    
    # 4. Save data
    patent_df.to_csv("data/patent_data.csv", index=False)
    gdp_data.to_csv("data/macro_data.csv", index=False)
    
    log_message("Data collection complete")
    print("\n✅ Data saved to data/ directory")
    print(f"✅ Patent data: {len(patent_df)} companies")
    print(f"✅ Macro data: {len(gdp_data)} years")

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution function
    """
    print("=" * 70)
    print("Strategic & Organizational Research Data Collection")
    print("=" * 70)
    
    # Create output directory
    import os
    os.makedirs(CONFIG["output_dir"], exist_ok=True)
    
    # Run example workflow
    example_workflow()
    
    print("\n" + "=" * 70)
    print("Next steps:")
    print("1. Review collected data in data/ directory")
    print("2. Clean and merge data using panel_data_analysis.py")
    print("3. Run regression analysis")
    print("=" * 70)

if __name__ == "__main__":
    main()