"""
01_data_collection.py

Data Collection Script Template

This script collects raw data from specified sources according to
sample criteria defined in config.yaml.

Usage:
    python scripts/01_data_collection.py
"""

import yaml
import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('output/logs/01_data_collection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yaml') -> dict:
    """Load configuration from YAML file"""
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def collect_financial_data(config: dict) -> pd.DataFrame:
    """
    Collect financial statement data
    
    Args:
        config: Configuration dictionary
    
    Returns:
        DataFrame with financial data
    """
    logger.info("Starting financial data collection...")
    
    # Extract sample criteria
    country = config['sample']['country']
    start_year = config['sample']['start_year']
    end_year = config['sample']['end_year']
    
    logger.info(f"Sample: {country}, {start_year}-{end_year}")
    
    # TODO: Implement actual data collection
    # Example for EDINET (Japan):
    # from data_sources import EDINETCollector
    # collector = EDINETCollector()
    # df = collector.collect_sample(start_year, end_year)
    
    # Placeholder: Return empty DataFrame with expected structure
    df = pd.DataFrame(columns=[
        'firm_id', 'year', 'sales', 'operating_income',
        'net_income', 'total_assets', 'total_equity'
    ])
    
    logger.info(f"Collected {len(df)} firm-year observations")
    return df
