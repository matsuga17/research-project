"""
Strategic Management Research Hub - Data Collectors Module
==========================================================

This module provides automated data collection from major sources for
strategic management research including:
- Compustat (via WRDS)
- USPTO PatentsView
- Japan EDINET
- SEC EDGAR

Author: Strategic Management Research Hub
Version: 3.0
License: MIT
"""

import pandas as pd
import numpy as np
import requests
import time
import logging
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path
import json
from ratelimit import limits, sleep_and_retry
from fuzzywuzzy import fuzz, process
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CompustatCollector:
    """
    Collect financial data from Compustat via WRDS.
    
    Requires WRDS account and wrds library installed:
    ```bash
    pip install wrds
    ```
    
    Usage:
    ```python
    collector = CompustatCollector(wrds_username='your_username')
    df = collector.collect_financial_data(
        start_year=2010,
        end_year=2023,
        sic_range=(2000, 3999)  # Manufacturing
    )
    ```
    """
    
    def __init__(self, wrds_username: Optional[str] = None):
        """
        Initialize Compustat collector.
        
        Args:
            wrds_username: WRDS account username. If None, will prompt.
        """
        self.wrds_username = wrds_username
        self.conn = None
        logger.info("CompustatCollector initialized")
    
    def connect(self):
        """Establish WRDS connection"""
        try:
            import wrds
            self.conn = wrds.Connection(wrds_username=self.wrds_username)
            logger.info("WRDS connection established")
        except ImportError:
            logger.error("wrds library not installed. Install: pip install wrds")
            raise
        except Exception as e:
            logger.error(f"WRDS connection failed: {e}")
            raise
    
    def collect_financial_data(
        self,
        start_year: int,
        end_year: int,
        sic_range: Optional[tuple] = None,
        min_assets: float = 10.0,  # million USD
        save_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Collect annual financial data from Compustat.
        
        Args:
            start_year: Start fiscal year
            end_year: End fiscal year
            sic_range: Tuple of (min_sic, max_sic) for industry filter
            min_assets: Minimum total assets in million USD
            save_path: Optional path to save CSV
            
        Returns:
            DataFrame with financial variables
        """
        if self.conn is None:
            self.connect()
        
        logger.info(f"Collecting Compustat data {start_year}-{end_year}")
        
        # Build SQL query
        query = f"""
        SELECT 
            a.gvkey,
            a.fyear,
            a.datadate,
            a.conm AS firm_name,
            a.fic AS incorporation_country,
            
            -- Performance variables
            a.at AS total_assets,
            a.sale AS sales,
            a.ni AS net_income,
            a.ebitda,
            a.oibdp AS operating_income,
            
            -- Strategy variables
            a.xrd AS rd_expenditure,
            a.xad AS advertising_expense,
            a.capx AS capex,
            a.emp AS employees,
            
            -- Financial controls
            a.ceq AS common_equity,
            a.dltt AS long_term_debt,
            a.dlc AS short_term_debt,
            a.che AS cash,
            a.ppent AS ppe,
            
            -- Industry
            a.sich AS sic_code,
            
            -- Market data
            b.prcc_f AS stock_price_fy,
            b.csho AS shares_outstanding
            
        FROM 
            comp.funda a
        LEFT JOIN 
            comp.funda b ON a.gvkey = b.gvkey AND a.fyear = b.fyear
            
        WHERE 
            a.fyear BETWEEN {start_year} AND {end_year}
            AND a.indfmt = 'INDL'
            AND a.datafmt = 'STD'
            AND a.popsrc = 'D'
            AND a.consol = 'C'
            AND a.at > {min_assets}
        """
        
        if sic_range:
            query += f" AND a.sich BETWEEN {sic_range[0]} AND {sic_range[1]}"
        
        # Execute query
        df = self.conn.raw_sql(query)
        
        logger.info(f"Retrieved {len(df)} observations, "
                   f"{df['gvkey'].nunique()} firms")
        
        # Basic data cleaning
        df = self._clean_financial_data(df)
        
        if save_path:
            df.to_csv(save_path, index=False)
            logger.info(f"Saved to {save_path}")
        
        return df
    
    def _clean_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate financial data"""
        initial_n = len(df)
        
        # Remove negative equity
        df = df[df['common_equity'] > 0]
        
        # Remove extreme leverage
        df['leverage'] = df['long_term_debt'] / df['total_assets']
        df = df[df['leverage'] <= 1.5]
        
        # Convert datadate to datetime
        df['datadate'] = pd.to_datetime(df['datadate'])
        
        logger.info(f"Cleaned: {initial_n} → {len(df)} observations")
        
        return df
    
    def collect_segment_data(
        self,
        gvkeys: List[str],
        start_year: int,
        end_year: int
    ) -> pd.DataFrame:
        """
        Collect segment-level data for diversification analysis.
        
        Args:
            gvkeys: List of GVKEY identifiers
            start_year: Start fiscal year
            end_year: End fiscal year
            
        Returns:
            DataFrame with segment sales and SIC codes
        """
        if self.conn is None:
            self.connect()
        
        logger.info(f"Collecting segment data for {len(gvkeys)} firms")
        
        # Convert list to SQL-compatible format
        gvkeys_str = "', '".join(gvkeys)
        
        query = f"""
        SELECT 
            gvkey,
            fyear,
            stype1,
            sics1 AS segment_sic,
            sales AS segment_sales
        FROM 
            comp.seg_annual
        WHERE 
            fyear BETWEEN {start_year} AND {end_year}
            AND stype1 = 'BUSSEG'
            AND gvkey IN ('{gvkeys_str}')
        """
        
        df = self.conn.raw_sql(query)
        
        logger.info(f"Retrieved segment data: {len(df)} segments")
        
        return df
    
    def link_to_crsp(
        self,
        compustat_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Link Compustat to CRSP using CCM link table.
        
        Args:
            compustat_df: DataFrame with GVKEY and datadate
            
        Returns:
            DataFrame with PERMNO added
        """
        if self.conn is None:
            self.connect()
        
        logger.info("Linking Compustat to CRSP")
        
        # Get CCM link table
        ccm_link = self.conn.raw_sql("""
            SELECT gvkey, lpermno as permno, linkdt, linkenddt
            FROM crsp.ccmxpf_lnkhist
            WHERE linktype IN ('LU', 'LC')
              AND linkprim IN ('P', 'C')
        """)
        
        # Merge with time-variant consideration
        compustat_df = compustat_df.sort_values('datadate')
        ccm_link['linkdt'] = pd.to_datetime(ccm_link['linkdt'])
        ccm_link['linkenddt'] = pd.to_datetime(ccm_link['linkenddt'])
        
        merged = pd.merge_asof(
            compustat_df,
            ccm_link,
            left_on='datadate',
            right_on='linkdt',
            by='gvkey',
            direction='backward'
        )
        
        # Filter to valid link period
        merged = merged[
            (merged['datadate'] >= merged['linkdt']) &
            (merged['datadate'] <= merged['linkenddt'])
        ]
        
        logger.info(f"Linked: {merged['permno'].nunique()} firms with PERMNO")
        
        return merged
    
    def close(self):
        """Close WRDS connection"""
        if self.conn:
            self.conn.close()
            logger.info("WRDS connection closed")


class PatentsViewCollector:
    """
    Collect patent data from USPTO PatentsView API.
    
    API documentation: https://patentsview.org/apis/api-endpoints
    
    Usage:
    ```python
    collector = PatentsViewCollector()
    patents = collector.collect_firm_patents(
        firm_name='Apple Inc',
        start_year=2010,
        end_year=2023
    )
    metrics = collector.calculate_innovation_metrics(patents)
    ```
    """
    
    def __init__(self, rate_limit_calls: int = 45, rate_limit_period: int = 60):
        """
        Initialize PatentsView collector.
        
        Args:
            rate_limit_calls: Max API calls per period
            rate_limit_period: Period in seconds (default: 45 calls/minute)
        """
        self.api_url = "https://api.patentsview.org/patents/query"
        self.rate_limit_calls = rate_limit_calls
        self.rate_limit_period = rate_limit_period
        logger.info("PatentsViewCollector initialized")
    
    @sleep_and_retry
    @limits(calls=45, period=60)  # API limit: 45 requests/minute
    def _make_api_request(self, query: dict) -> dict:
        """Make rate-limited API request"""
        response = requests.post(self.api_url, json=query)
        response.raise_for_status()
        return response.json()
    
    def collect_firm_patents(
        self,
        firm_name: str,
        start_year: int,
        end_year: int,
        save_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Collect patents for a specific firm.
        
        Args:
            firm_name: Company name (will be fuzzy matched)
            start_year: Start grant year
            end_year: End grant year
            save_path: Optional path to save CSV
            
        Returns:
            DataFrame with patent details
        """
        logger.info(f"Collecting patents for '{firm_name}' ({start_year}-{end_year})")
        
        query = {
            "q": {
                "_and": [
                    {"assignee_organization": firm_name},
                    {"_gte": {"patent_date": f"{start_year}-01-01"}},
                    {"_lte": {"patent_date": f"{end_year}-12-31"}}
                ]
            },
            "f": [
                "patent_number",
                "patent_date",
                "patent_title",
                "patent_abstract",
                "cited_patent_number",
                "uspc_mainclass_id",
                "cpc_subgroup_id",
                "assignee_organization"
            ],
            "o": {"per_page": 10000}
        }
        
        try:
            data = self._make_api_request(query)
            patents = data.get('patents', [])
            
            if not patents:
                logger.warning(f"No patents found for '{firm_name}'")
                return pd.DataFrame()
            
            df = pd.DataFrame(patents)
            logger.info(f"Retrieved {len(df)} patents")
            
            if save_path:
                df.to_csv(save_path, index=False)
                logger.info(f"Saved to {save_path}")
            
            return df
            
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return pd.DataFrame()
    
    def calculate_innovation_metrics(
        self,
        patents_df: pd.DataFrame,
        depreciation_rate: float = 0.15,
        max_lag: int = 10
    ) -> Dict[str, float]:
        """
        Calculate innovation metrics from patent data.
        
        Args:
            patents_df: DataFrame from collect_firm_patents
            depreciation_rate: Annual depreciation rate for patent stock
            max_lag: Years to look back for stock calculation
            
        Returns:
            Dictionary with innovation metrics
        """
        if patents_df.empty:
            return {}
        
        metrics = {}
        
        # Patent count
        metrics['patent_count'] = len(patents_df)
        
        # Technology diversity (Entropy index)
        if 'uspc_mainclass_id' in patents_df.columns:
            tech_classes = patents_df['uspc_mainclass_id'].value_counts()
            probs = tech_classes / tech_classes.sum()
            metrics['tech_diversity'] = -sum(probs * np.log(probs + 1e-10))
        
        # Citation impact
        if 'cited_patent_number' in patents_df.columns:
            patents_df['num_citations'] = patents_df['cited_patent_number'].apply(
                lambda x: len(x) if isinstance(x, list) else 0
            )
            metrics['avg_citations'] = patents_df['num_citations'].mean()
            metrics['citation_std'] = patents_df['num_citations'].std()
            metrics['highly_cited_ratio'] = (
                patents_df['num_citations'] > patents_df['num_citations'].quantile(0.9)
            ).mean()
        
        logger.info(f"Calculated innovation metrics: {list(metrics.keys())}")
        
        return metrics
    
    def match_companies_to_compustat(
        self,
        patents_df: pd.DataFrame,
        compustat_df: pd.DataFrame,
        threshold: int = 85
    ) -> pd.DataFrame:
        """
        Match patent assignee names to Compustat firms using fuzzy matching.
        
        Args:
            patents_df: DataFrame with 'assignee_organization'
            compustat_df: DataFrame with 'firm_name' and 'gvkey'
            threshold: Minimum similarity score (0-100)
            
        Returns:
            DataFrame with match results and GVKEY
        """
        logger.info("Matching patent assignees to Compustat firms")
        
        # Clean company names
        def clean_name(name):
            if pd.isna(name):
                return ""
            name = str(name).lower()
            suffixes = ['inc', 'corp', 'corporation', 'company', 'co',
                       'ltd', 'limited', 'llc', 'plc']
            for suffix in suffixes:
                name = re.sub(rf'\b{suffix}\b\.?', '', name)
            name = re.sub(r'[^\w\s]', '', name)
            return re.sub(r'\s+', ' ', name).strip()
        
        patents_df['clean_assignee'] = patents_df['assignee_organization'].apply(clean_name)
        compustat_df['clean_name'] = compustat_df['firm_name'].apply(clean_name)
        
        # Fuzzy matching
        compustat_names = compustat_df['clean_name'].unique()
        matches = []
        
        unique_assignees = patents_df['clean_assignee'].unique()
        
        for assignee in tqdm(unique_assignees, desc="Fuzzy matching"):
            if not assignee:
                continue
                
            best_match, score = process.extractOne(
                assignee,
                compustat_names,
                scorer=fuzz.token_sort_ratio
            )
            
            if score >= threshold:
                gvkey = compustat_df[
                    compustat_df['clean_name'] == best_match
                ]['gvkey'].iloc[0]
                
                matches.append({
                    'assignee_name': assignee,
                    'compustat_name': best_match,
                    'gvkey': gvkey,
                    'match_score': score
                })
        
        matches_df = pd.DataFrame(matches)
        logger.info(f"Matched {len(matches_df)} assignees to Compustat")
        
        # Merge back to patents
        result = patents_df.merge(
            matches_df[['assignee_name', 'gvkey']],
            left_on='clean_assignee',
            right_on='assignee_name',
            how='left'
        )
        
        return result


class EDINETCollector:
    """
    Collect financial data from Japan's EDINET system.
    
    API documentation: https://disclosure2.edinet-fsa.go.jp/
    
    Usage:
    ```python
    collector = EDINETCollector()
    df = collector.collect_sample(
        start_date='2023-01-01',
        end_date='2023-12-31',
        industry_codes=['010']  # Manufacturing
    )
    ```
    """
    
    def __init__(self):
        """Initialize EDINET collector"""
        self.base_url = "https://disclosure2.edinet-fsa.go.jp/api/v2"
        logger.info("EDINETCollector initialized")
    
    @sleep_and_retry
    @limits(calls=10, period=60)  # Conservative rate limit
    def _make_api_request(self, endpoint: str, params: dict) -> dict:
        """Make rate-limited API request"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_document_list(self, date: str, doc_type: int = 2) -> dict:
        """
        Get list of documents submitted on a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            doc_type: 1=Timely, 2=Periodic (Annual Report)
            
        Returns:
            Dictionary with document list
        """
        params = {
            'date': date,
            'type': doc_type
        }
        
        try:
            return self._make_api_request('documents.json', params)
        except Exception as e:
            logger.error(f"Failed to get document list for {date}: {e}")
            return {'results': []}
    
    def collect_sample(
        self,
        start_date: str,
        end_date: str,
        industry_codes: Optional[List[str]] = None,
        save_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Collect sample of Japanese firms' financial data.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            industry_codes: List of industry codes to filter
            save_path: Optional path to save CSV
            
        Returns:
            DataFrame with basic financial information
        """
        logger.info(f"Collecting EDINET data {start_date} to {end_date}")
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        date_range = pd.date_range(start, end, freq='D')
        
        all_docs = []
        
        for date in tqdm(date_range, desc="Collecting documents"):
            date_str = date.strftime('%Y-%m-%d')
            docs = self.get_document_list(date_str)
            
            for doc in docs.get('results', []):
                # Filter by industry if specified
                if industry_codes and doc.get('ordinanceCode') not in industry_codes:
                    continue
                
                all_docs.append({
                    'doc_id': doc.get('docID'),
                    'date': date_str,
                    'company_name': doc.get('filerName'),
                    'securities_code': doc.get('secCode'),
                    'industry_code': doc.get('ordinanceCode'),
                    'document_type': doc.get('docDescription')
                })
            
            time.sleep(0.5)  # Respectful scraping
        
        df = pd.DataFrame(all_docs)
        logger.info(f"Collected {len(df)} documents, "
                   f"{df['securities_code'].nunique()} unique companies")
        
        if save_path:
            df.to_csv(save_path, index=False)
            logger.info(f"Saved to {save_path}")
        
        return df
    
    def extract_financial_data(self, doc_id: str) -> dict:
        """
        Extract financial data from XBRL document.
        
        Note: This is a placeholder. Full XBRL parsing requires
        specialized libraries like xbrl-parser or Arelle.
        
        Args:
            doc_id: Document ID from EDINET
            
        Returns:
            Dictionary with financial data
        """
        logger.warning("XBRL extraction not fully implemented. "
                      "Use xbrl-parser library for production use.")
        
        # Placeholder implementation
        params = {'type': 5}  # XBRL format
        endpoint = f"documents/{doc_id}"
        
        try:
            data = self._make_api_request(endpoint, params)
            # TODO: Implement XBRL parsing
            return data
        except Exception as e:
            logger.error(f"Failed to extract financial data: {e}")
            return {}


class SECTextCollector:
    """
    Collect text data from SEC EDGAR filings.
    
    Usage:
    ```python
    collector = SECTextCollector()
    mda_text = collector.extract_mda_section('0000320193', '10-K', 2023)
    ```
    """
    
    def __init__(self, user_agent: str = "research@university.edu"):
        """
        Initialize SEC collector.
        
        Args:
            user_agent: Contact email for SEC API (required by SEC)
        """
        self.base_url = "https://www.sec.gov"
        self.headers = {'User-Agent': user_agent}
        logger.info("SECTextCollector initialized")
        
        if 'university.edu' in user_agent or 'example.com' in user_agent:
            logger.warning("Using placeholder email. Replace with your actual email!")
    
    @sleep_and_retry
    @limits(calls=10, period=1)  # SEC: 10 requests/second max
    def _make_request(self, url: str) -> requests.Response:
        """Make rate-limited SEC request"""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response
    
    def download_10k_filing(
        self,
        cik: str,
        filing_year: int,
        save_dir: Optional[str] = None
    ) -> Optional[str]:
        """
        Download 10-K filing for a company.
        
        Args:
            cik: Central Index Key (10 digits, zero-padded)
            filing_year: Fiscal year
            save_dir: Optional directory to save HTML
            
        Returns:
            HTML content as string, or None if failed
        """
        # Pad CIK to 10 digits
        cik = str(cik).zfill(10)
        
        logger.info(f"Downloading 10-K for CIK {cik}, FY {filing_year}")
        
        # Search for filing
        search_url = f"{self.base_url}/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'CIK': cik,
            'type': '10-K',
            'dateb': f"{filing_year + 1}0331",  # Search up to 3 months after FY
            'owner': 'exclude',
            'count': '10'
        }
        
        try:
            response = self._make_request(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find document link
            doc_link = soup.find('a', {'id': 'documentsbutton'})
            if not doc_link:
                logger.warning(f"No 10-K found for CIK {cik}, FY {filing_year}")
                return None
            
            doc_url = self.base_url + doc_link['href']
            doc_response = self._make_request(doc_url)
            
            if save_dir:
                save_path = Path(save_dir) / f"{cik}_{filing_year}_10K.html"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(doc_response.text)
                logger.info(f"Saved to {save_path}")
            
            return doc_response.text
            
        except Exception as e:
            logger.error(f"Failed to download 10-K: {e}")
            return None
    
    def extract_mda_section(
        self,
        html_content: str
    ) -> Optional[str]:
        """
        Extract MD&A section from 10-K HTML.
        
        Args:
            html_content: HTML content of 10-K filing
            
        Returns:
            MD&A text, or None if not found
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common patterns for MD&A section
        mda_patterns = [
            r"Item\s*7\.?\s*Management'?s?\s*Discussion",
            r"ITEM\s*7\.?\s*MANAGEMENT'?S?\s*DISCUSSION"
        ]
        
        text = soup.get_text()
        
        for pattern in mda_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                start = match.end()
                # Find Item 8 (end of MD&A)
                end_match = re.search(r"Item\s*8\.?", text[start:], re.IGNORECASE)
                if end_match:
                    end = start + end_match.start()
                    mda_text = text[start:end]
                    logger.info(f"Extracted MD&A: {len(mda_text)} characters")
                    return mda_text.strip()
        
        logger.warning("MD&A section not found")
        return None


# Example usage and testing
if __name__ == "__main__":
    
    # Example 1: Compustat (requires WRDS account)
    # compustat = CompustatCollector(wrds_username='your_username')
    # df_financials = compustat.collect_financial_data(
    #     start_year=2010,
    #     end_year=2023,
    #     sic_range=(2000, 3999),
    #     save_path='./data/compustat_sample.csv'
    # )
    # compustat.close()
    
    # Example 2: PatentsView (free, no login required)
    patents_collector = PatentsViewCollector()
    patents = patents_collector.collect_firm_patents(
        firm_name='Apple Inc',
        start_year=2020,
        end_year=2023
    )
    
    if not patents.empty:
        metrics = patents_collector.calculate_innovation_metrics(patents)
        print("\nInnovation Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.3f}")
    
    # Example 3: EDINET (free, no login required)
    # edinet = EDINETCollector()
    # df_japan = edinet.collect_sample(
    #     start_date='2023-06-01',
    #     end_date='2023-06-30',
    #     industry_codes=['010'],  # Manufacturing
    #     save_path='./data/edinet_sample.csv'
    # )
    
    # Example 4: SEC EDGAR (free, but need to provide email)
    # sec = SECTextCollector(user_agent='your_email@university.edu')
    # html_10k = sec.download_10k_filing(
    #     cik='0000320193',  # Apple
    #     filing_year=2023
    # )
    # if html_10k:
    #     mda = sec.extract_mda_section(html_10k)
    #     if mda:
    #         print(f"\nMD&A excerpt:\n{mda[:500]}...")
    
    print("\n✅ data_collectors.py module loaded successfully")
    print("   See examples in __main__ section for usage")
