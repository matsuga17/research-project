"""
compustat_collector.py

Compustat Data Collector via WRDS

This module collects financial statement data from Compustat (North America and Global)
through the WRDS (Wharton Research Data Services) platform.

Key Features:
- Compustat North America (Fundamentals Annual/Quarterly)
- Compustat Global (Fundamentals Annual/Quarterly)
- Automatic variable selection and filtering
- Panel dataset construction
- Industry classification (SIC, NAICS)
- Connection pooling and error handling

Prerequisites:
- WRDS account with Compustat access
- WRDS library installed: pip install wrds
- WRDS credentials configured

Usage:
    from compustat_collector import CompustatCollector
    
    # Initialize with WRDS credentials
    collector = CompustatCollector(username='your_wrds_username')
    
    # Collect North America annual data
    df_funda = collector.collect_fundamentals_annual(
        start_year=2010,
        end_year=2023,
        variables=['at', 'sale', 'ni', 'ceq']
    )
    
    # Collect Global data
    df_global = collector.collect_global_fundamentals(
        start_year=2010,
        end_year=2023,
        countries=['JPN', 'CHN', 'KOR']
    )
    
    # Build panel with industry classifications
    panel = collector.build_panel(
        df_funda,
        include_industry=True,
        lag_variables=['sale', 'ni']
    )

References:
- WRDS Compustat documentation: https://wrds-www.wharton.upenn.edu/pages/get-data/compustat/
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from pathlib import Path
import warnings

# WRDS library (optional)
try:
    import wrds
    WRDS_AVAILABLE = True
except ImportError:
    WRDS_AVAILABLE = False
    warnings.warn(
        "WRDS library not available. Install with: pip install wrds\n"
        "WRDS account required for access."
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompustatCollector:
    """
    Collect financial data from Compustat via WRDS
    
    Attributes:
        username: WRDS username
        db: WRDS database connection
        data_cache: Dictionary for caching retrieved data
    """
    
    def __init__(self, username: Optional[str] = None):
        """
        Initialize Compustat collector
        
        Args:
            username: WRDS username (optional if configured in .pgpass)
        """
        if not WRDS_AVAILABLE:
            raise ImportError(
                "WRDS library required for Compustat access. "
                "Install with: pip install wrds"
            )
        
        self.username = username
        self.db = None
        self.data_cache = {}
        
        logger.info("CompustatCollector initialized")
        logger.info("Note: WRDS connection will be established on first data request")
    
    def connect(self):
        """Establish connection to WRDS"""
        if self.db is None:
            logger.info("Connecting to WRDS...")
            try:
                if self.username:
                    self.db = wrds.Connection(wrds_username=self.username)
                else:
                    self.db = wrds.Connection()
                logger.info("✓ Connected to WRDS successfully")
            except Exception as e:
                logger.error(f"Failed to connect to WRDS: {e}")
                raise
    
    def disconnect(self):
        """Close WRDS connection"""
        if self.db is not None:
            self.db.close()
            self.db = None
            logger.info("WRDS connection closed")
    
    def collect_fundamentals_annual(self,
                                   start_year: int,
                                   end_year: int,
                                   variables: Optional[List[str]] = None,
                                   filters: Optional[Dict] = None) -> pd.DataFrame:
        """
        Collect Compustat North America Fundamentals Annual
        
        Args:
            start_year: Start fiscal year
            end_year: End fiscal year
            variables: List of Compustat variables (default: common research vars)
            filters: Additional SQL filters (e.g., {'indfmt': 'INDL', 'datafmt': 'STD'})
        
        Returns:
            DataFrame with annual fundamentals
        
        Example Variables:
            - at: Total Assets
            - sale: Sales/Revenue
            - ni: Net Income
            - ceq: Common Equity
            - lt: Total Liabilities
            - capx: Capital Expenditures
            - xrd: R&D Expense
            - xsga: SG&A Expense
        """
        self.connect()
        
        logger.info(f"Collecting Fundamentals Annual ({start_year}-{end_year})...")
        
        # Default research variables
        if variables is None:
            variables = [
                'gvkey', 'datadate', 'fyear', 'sich', 'naicsh',  # Identifiers
                'at', 'sale', 'ni', 'ceq', 'lt',  # Core financials
                'capx', 'xrd', 'xsga',  # Investment & expenses
                'ib', 'oibdp', 'dp',  # Profitability
                'act', 'lct', 'ch', 'che',  # Working capital
                'dltt', 'dlc', 'dvc'  # Debt & dividends
            ]
        
        # Build SQL query
        var_str = ', '.join(variables)
        
        sql_query = f"""
        SELECT {var_str}
        FROM comp.funda
        WHERE fyear >= {start_year}
          AND fyear <= {end_year}
        """
        
        # Add filters
        if filters is None:
            filters = {
                'indfmt': 'INDL',  # Industrial format
                'datafmt': 'STD',  # Standardized format
                'popsrc': 'D',     # Domestic (US/Canada)
                'consol': 'C'      # Consolidated
            }
        
        for key, value in filters.items():
            if isinstance(value, str):
                sql_query += f"\n  AND {key} = '{value}'"
            else:
                sql_query += f"\n  AND {key} = {value}"
        
        sql_query += "\nORDER BY gvkey, fyear"
        
        logger.info(f"Executing SQL query...")
        df = self.db.raw_sql(sql_query)
        
        logger.info(f"✓ Retrieved {len(df):,} firm-year observations")
        logger.info(f"  Unique firms: {df['gvkey'].nunique():,}")
        logger.info(f"  Years: {df['fyear'].min()}-{df['fyear'].max()}")
        
        return df
    
    def collect_fundamentals_quarterly(self,
                                      start_year: int,
                                      end_year: int,
                                      variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Collect Compustat North America Fundamentals Quarterly
        
        Args:
            start_year: Start fiscal year
            end_year: End fiscal year
            variables: List of Compustat variables
        
        Returns:
            DataFrame with quarterly fundamentals
        """
        self.connect()
        
        logger.info(f"Collecting Fundamentals Quarterly ({start_year}-{end_year})...")
        
        if variables is None:
            variables = [
                'gvkey', 'datadate', 'fyearq', 'fqtr',
                'atq', 'saleq', 'niq', 'ceqq',
                'ibq', 'oibdpq', 'dpq'
            ]
        
        var_str = ', '.join(variables)
        
        sql_query = f"""
        SELECT {var_str}
        FROM comp.fundq
        WHERE fyearq >= {start_year}
          AND fyearq <= {end_year}
          AND indfmt = 'INDL'
          AND datafmt = 'STD'
          AND popsrc = 'D'
          AND consol = 'C'
        ORDER BY gvkey, datadate
        """
        
        df = self.db.raw_sql(sql_query)
        
        logger.info(f"✓ Retrieved {len(df):,} firm-quarter observations")
        
        return df
    
    def collect_global_fundamentals(self,
                                   start_year: int,
                                   end_year: int,
                                   countries: Optional[List[str]] = None,
                                   variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Collect Compustat Global Fundamentals Annual
        
        Args:
            start_year: Start fiscal year
            end_year: End fiscal year
            countries: List of country codes (e.g., ['JPN', 'CHN', 'KOR'])
            variables: List of Compustat Global variables
        
        Returns:
            DataFrame with global fundamentals
        """
        self.connect()
        
        logger.info(f"Collecting Global Fundamentals ({start_year}-{end_year})...")
        
        if variables is None:
            variables = [
                'gvkey', 'datadate', 'fyear', 'loc', 'curcd',
                'at', 'sale', 'ni', 'ceq', 'lt',
                'capx', 'xrd', 'ib', 'oibdp'
            ]
        
        var_str = ', '.join(variables)
        
        sql_query = f"""
        SELECT {var_str}
        FROM comp.g_funda
        WHERE fyear >= {start_year}
          AND fyear <= {end_year}
          AND indfmt = 'INDL'
          AND datafmt = 'STD'
          AND consol = 'C'
        """
        
        # Filter by countries if specified
        if countries:
            country_str = "', '".join(countries)
            sql_query += f"\n  AND loc IN ('{country_str}')"
        
        sql_query += "\nORDER BY gvkey, fyear"
        
        df = self.db.raw_sql(sql_query)
        
        logger.info(f"✓ Retrieved {len(df):,} firm-year observations")
        if countries:
            logger.info(f"  Countries: {', '.join(countries)}")
        
        return df
    
    def get_industry_classifications(self, gvkeys: List[str]) -> pd.DataFrame:
        """
        Get industry classifications (SIC, NAICS) for firms
        
        Args:
            gvkeys: List of GVKEYs
        
        Returns:
            DataFrame with industry codes
        """
        self.connect()
        
        gvkey_str = "', '".join([str(g) for g in gvkeys])
        
        sql_query = f"""
        SELECT DISTINCT gvkey, sich, naicsh
        FROM comp.funda
        WHERE gvkey IN ('{gvkey_str}')
          AND sich IS NOT NULL
        ORDER BY gvkey
        """
        
        df = self.db.raw_sql(sql_query)
        
        logger.info(f"✓ Retrieved industry classifications for {len(df)} firms")
        
        return df
    
    def build_panel(self,
                   df: pd.DataFrame,
                   firm_id: str = 'gvkey',
                   time_id: str = 'fyear',
                   include_industry: bool = True,
                   lag_variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Build research-ready panel dataset
        
        Args:
            df: Raw Compustat data
            firm_id: Firm identifier column
            time_id: Time identifier column
            include_industry: Add industry classifications
            lag_variables: Variables to create lagged versions
        
        Returns:
            Panel DataFrame with transformations
        """
        logger.info("Building panel dataset...")
        
        panel = df.copy()
        
        # Sort panel
        panel = panel.sort_values([firm_id, time_id])
        
        # Create lagged variables
        if lag_variables:
            logger.info(f"Creating lagged variables: {', '.join(lag_variables)}")
            
            for var in lag_variables:
                if var in panel.columns:
                    panel[f'{var}_lag1'] = panel.groupby(firm_id)[var].shift(1)
        
        # Calculate growth rates
        if 'sale' in panel.columns:
            panel['sale_growth'] = (
                panel.groupby(firm_id)['sale'].pct_change()
            )
        
        # Calculate financial ratios
        if 'ni' in panel.columns and 'at' in panel.columns:
            panel['roa'] = panel['ni'] / panel['at']
        
        if 'ni' in panel.columns and 'ceq' in panel.columns:
            panel['roe'] = panel['ni'] / panel['ceq']
        
        if 'lt' in panel.columns and 'at' in panel.columns:
            panel['leverage'] = panel['lt'] / panel['at']
        
        logger.info(f"✓ Panel dataset built:")
        logger.info(f"  Firms: {panel[firm_id].nunique():,}")
        logger.info(f"  Time periods: {panel[time_id].nunique()}")
        logger.info(f"  Observations: {len(panel):,}")
        logger.info(f"  Variables: {len(panel.columns)}")
        
        return panel
    
    def calculate_winsorized_variables(self,
                                      df: pd.DataFrame,
                                      variables: List[str],
                                      percentiles: Tuple[float, float] = (0.01, 0.99)) -> pd.DataFrame:
        """
        Winsorize variables to handle outliers
        
        Args:
            df: Input DataFrame
            variables: Variables to winsorize
            percentiles: Lower and upper percentiles
        
        Returns:
            DataFrame with winsorized variables
        """
        logger.info(f"Winsorizing {len(variables)} variables at {percentiles}...")
        
        df_wins = df.copy()
        
        for var in variables:
            if var in df.columns:
                lower = df[var].quantile(percentiles[0])
                upper = df[var].quantile(percentiles[1])
                
                df_wins[f'{var}_wins'] = df[var].clip(lower=lower, upper=upper)
        
        return df_wins
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == '__main__':
    # Example 1: Collect annual fundamentals
    print("=" * 80)
    print("Example 1: Collecting Compustat North America Annual Data")
    print("=" * 80)
    
    try:
        with CompustatCollector() as collector:
            df_annual = collector.collect_fundamentals_annual(
                start_year=2015,
                end_year=2023
            )
            
            print(f"\nSample data:")
            print(df_annual.head())
            
            # Build panel
            panel = collector.build_panel(
                df_annual,
                lag_variables=['sale', 'at']
            )
            
            print(f"\nPanel summary:")
            print(panel[['gvkey', 'fyear', 'sale', 'roa', 'leverage']].head())
    
    except ImportError:
        print("\nWRDS library not available.")
        print("Install with: pip install wrds")
        print("Requires WRDS account with Compustat access.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have:")
        print("  1. WRDS account with Compustat access")
        print("  2. WRDS credentials configured")
