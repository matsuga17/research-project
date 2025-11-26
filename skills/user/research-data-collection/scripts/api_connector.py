"""
API Connector Utilities for Research Data Collection
====================================================
Helper functions for connecting to various data source APIs.
Includes authentication, rate limiting, error handling, and retry logic.

Author: Research Data Collection Skill
Version: 1.0
Last Updated: 2025-10-31
"""

import requests
import time
import json
import os
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIConnector:
    """Base class for API connections with common functionality."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None,
                 rate_limit: int = 60, retry_attempts: int = 3):
        """
        Initialize API connector.
        
        Args:
            base_url: Base URL for the API
            api_key: API authentication key (optional)
            rate_limit: Max requests per minute
            retry_attempts: Number of retry attempts for failed requests
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.retry_attempts = retry_attempts
        self.request_timestamps = []
        
    def _check_rate_limit(self):
        """Enforce rate limiting."""
        now = time.time()
        # Remove timestamps older than 1 minute
        self.request_timestamps = [ts for ts in self.request_timestamps 
                                   if now - ts < 60]
        
        if len(self.request_timestamps) >= self.rate_limit:
            sleep_time = 60 - (now - self.request_timestamps[0])
            logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.request_timestamps.append(now)
    
    def _make_request(self, endpoint: str, params: Dict = None,
                     method: str = 'GET', data: Dict = None) -> Dict:
        """
        Make API request with retry logic.
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Query parameters
            method: HTTP method (GET, POST, etc.)
            data: Request body for POST requests
            
        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {}
        
        if self.api_key:
            headers['Authorization'] = f"Bearer {self.api_key}"
        
        for attempt in range(self.retry_attempts):
            try:
                self._check_rate_limit()
                
                if method.upper() == 'GET':
                    response = requests.get(url, params=params, headers=headers)
                elif method.upper() == 'POST':
                    response = requests.post(url, params=params, 
                                           json=data, headers=headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1}/{self.retry_attempts} failed: {e}")
                
                if attempt < self.retry_attempts - 1:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"All retry attempts failed for {url}")
                    raise
    
    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """Convenience method for GET requests."""
        return self._make_request(endpoint, params=params, method='GET')
    
    def post(self, endpoint: str, data: Dict, params: Dict = None) -> Dict:
        """Convenience method for POST requests."""
        return self._make_request(endpoint, params=params, method='POST', data=data)


class WorldBankAPI(APIConnector):
    """World Bank Open Data API connector."""
    
    def __init__(self):
        super().__init__(base_url="https://api.worldbank.org/v2")
    
    def get_indicators(self, country_codes: List[str], indicator: str,
                      start_year: int, end_year: int) -> List[Dict]:
        """
        Fetch indicator data for specified countries and time range.
        
        Args:
            country_codes: List of ISO country codes (e.g., ['USA', 'JPN'])
            indicator: Indicator code (e.g., 'NY.GDP.MKTP.CD')
            start_year: Start year
            end_year: End year
            
        Returns:
            List of data points
        """
        countries = ';'.join(country_codes)
        endpoint = f"country/{countries}/indicator/{indicator}"
        params = {
            'date': f"{start_year}:{end_year}",
            'format': 'json',
            'per_page': 1000
        }
        
        response = self.get(endpoint, params=params)
        
        # World Bank API returns [metadata, data]
        if isinstance(response, list) and len(response) > 1:
            return response[1]
        return []


class OECDAPI(APIConnector):
    """OECD Data API connector."""
    
    def __init__(self):
        super().__init__(base_url="https://stats.oecd.org/sdmx-json/data")
    
    def get_dataset(self, dataset_id: str, filters: Dict = None) -> Dict:
        """
        Fetch OECD dataset.
        
        Args:
            dataset_id: OECD dataset identifier
            filters: Filter parameters (country, time period, etc.)
            
        Returns:
            Dataset in JSON format
        """
        endpoint = dataset_id
        return self.get(endpoint, params=filters)


class PubMedAPI(APIConnector):
    """PubMed E-utilities API connector."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
            api_key=api_key,
            rate_limit=3 if not api_key else 10  # 3/sec without key, 10/sec with key
        )
    
    def search(self, query: str, max_results: int = 100,
              start_date: Optional[str] = None,
              end_date: Optional[str] = None) -> List[str]:
        """
        Search PubMed for articles.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            start_date: Start date (YYYY/MM/DD format)
            end_date: End date (YYYY/MM/DD format)
            
        Returns:
            List of PubMed IDs (PMIDs)
        """
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        
        if start_date:
            params['mindate'] = start_date
        if end_date:
            params['maxdate'] = end_date
        
        if self.api_key:
            params['api_key'] = self.api_key
        
        response = self.get('esearch.fcgi', params=params)
        
        if 'esearchresult' in response and 'idlist' in response['esearchresult']:
            return response['esearchresult']['idlist']
        return []
    
    def fetch_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for PubMed articles.
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            List of article details
        """
        if not pmids:
            return []
        
        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'json',
            'rettype': 'abstract'
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
        
        response = self.get('esummary.fcgi', params=params)
        
        if 'result' in response:
            # Extract article information
            articles = []
            for pmid in pmids:
                if pmid in response['result']:
                    articles.append(response['result'][pmid])
            return articles
        return []


class ClinicalTrialsAPI(APIConnector):
    """ClinicalTrials.gov API connector."""
    
    def __init__(self):
        super().__init__(base_url="https://clinicaltrials.gov/api/v2")
    
    def search_studies(self, condition: str, intervention: Optional[str] = None,
                      status: Optional[List[str]] = None,
                      start_date: Optional[str] = None,
                      max_results: int = 100) -> List[Dict]:
        """
        Search clinical trials.
        
        Args:
            condition: Medical condition
            intervention: Intervention type (optional)
            status: List of study statuses (optional)
            start_date: Minimum start date (YYYY-MM-DD)
            max_results: Maximum number of results
            
        Returns:
            List of clinical trials
        """
        params = {
            'query.cond': condition,
            'pageSize': min(max_results, 100),
            'format': 'json'
        }
        
        if intervention:
            params['query.intr'] = intervention
        
        if status:
            params['filter.overallStatus'] = ','.join(status)
        
        if start_date:
            params['filter.studyFirstPostDate'] = f"{start_date}:MAX"
        
        response = self.get('studies', params=params)
        
        if 'studies' in response:
            return response['studies']
        return []


def load_api_key(service_name: str) -> Optional[str]:
    """
    Load API key from environment variable or .env file.
    
    Args:
        service_name: Name of the service (e.g., 'PUBMED', 'WORLD_BANK')
        
    Returns:
        API key if found, None otherwise
    """
    env_var = f"{service_name.upper()}_API_KEY"
    
    # Check environment variable
    api_key = os.getenv(env_var)
    if api_key:
        return api_key
    
    # Check .env file
    env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith(env_var):
                    return line.split('=', 1)[1].strip()
    
    logger.warning(f"API key for {service_name} not found")
    return None


# Example usage
if __name__ == "__main__":
    # Example 1: World Bank API
    print("Testing World Bank API...")
    wb = WorldBankAPI()
    gdp_data = wb.get_indicators(
        country_codes=['USA', 'JPN'],
        indicator='NY.GDP.MKTP.CD',
        start_year=2020,
        end_year=2023
    )
    print(f"Retrieved {len(gdp_data)} GDP data points")
    
    # Example 2: PubMed API
    print("\nTesting PubMed API...")
    pubmed_key = load_api_key('PUBMED')
    pubmed = PubMedAPI(api_key=pubmed_key)
    pmids = pubmed.search("diabetes treatment", max_results=5)
    print(f"Found {len(pmids)} articles")
    
    if pmids:
        articles = pubmed.fetch_details(pmids[:3])
        print(f"Retrieved details for {len(articles)} articles")
    
    # Example 3: Clinical Trials API
    print("\nTesting ClinicalTrials.gov API...")
    ct = ClinicalTrialsAPI()
    trials = ct.search_studies(
        condition="diabetes",
        status=["RECRUITING", "ACTIVE_NOT_RECRUITING"],
        max_results=5
    )
    print(f"Found {len(trials)} active trials")
