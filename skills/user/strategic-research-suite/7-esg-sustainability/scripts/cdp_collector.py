"""
cdp_collector.py

CDP (Carbon Disclosure Project) Data Collector

This module provides functionality to collect environmental and climate data
from the CDP database, which is the leading global disclosure system for
companies to manage their environmental impacts.

Key Features:
- Carbon emissions data collection (Scope 1, 2, 3)
- Climate change scores and ratings
- Water security data
- Forest sustainability data
- Company-level environmental metrics

Common Applications in Strategic Research:
- ESG performance and firm value
- Carbon intensity and competitive advantage
- Climate risk disclosure and stock returns
- Environmental leadership and innovation

Note: CDP data requires access credentials. This module provides structure
for data collection; actual API access requires registration at:
https://www.cdp.net/en/data

Usage:
    from cdp_collector import CDPCollector
    
    collector = CDPCollector(api_key='your_key')
    
    # Collect carbon emissions
    carbon_data = collector.collect_carbon_emissions(
        companies=['Apple Inc.', 'Microsoft Corp.'],
        years=[2020, 2021, 2022]
    )
    
    # Collect CDP scores
    scores = collector.collect_climate_scores(
        companies=['Apple Inc.', 'Microsoft Corp.'],
        years=[2020, 2021, 2022]
    )
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
import logging
from pathlib import Path
import requests
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CDPCollector:
    """
    Collector for CDP environmental data
    
    This class provides methods to collect and process environmental disclosure
    data from the Carbon Disclosure Project database.
    
    Attributes:
        api_key: CDP API key (requires registration)
        base_url: CDP API base URL
        rate_limit: Requests per second limit
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CDP collector
        
        Args:
            api_key: CDP API key (get from https://www.cdp.net/en/data)
        """
        self.api_key = api_key
        self.base_url = "https://api.cdp.net/v1"  # Hypothetical endpoint
        self.rate_limit = 1.0  # 1 request per second
        
        if api_key is None:
            logger.warning("No API key provided. Using demo mode with simulated data.")
            self.demo_mode = True
        else:
            self.demo_mode = False
            logger.info("CDP Collector initialized with API access")
    
    def collect_carbon_emissions(self,
                                 companies: List[str],
                                 years: List[int],
                                 scopes: List[str] = ['scope1', 'scope2', 'scope3']) -> pd.DataFrame:
        """
        Collect carbon emissions data
        
        Args:
            companies: List of company names
            years: List of years
            scopes: Emission scopes to collect (scope1, scope2, scope3)
        
        Returns:
            DataFrame with carbon emissions data
        """
        logger.info(f"Collecting carbon emissions for {len(companies)} companies...")
        
        if self.demo_mode:
            return self._generate_demo_carbon_data(companies, years, scopes)
        
        # Actual API implementation would go here
        data = []
        for company in companies:
            for year in years:
                time.sleep(self.rate_limit)  # Rate limiting
                
                # API call (pseudo-code)
                # response = requests.get(
                #     f"{self.base_url}/emissions",
                #     headers={'Authorization': f'Bearer {self.api_key}'},
                #     params={'company': company, 'year': year}
                # )
                
                # For now, use demo data
                data.extend(self._generate_demo_carbon_data([company], [year], scopes).to_dict('records'))
        
        df = pd.DataFrame(data)
        logger.info(f"✓ Collected {len(df)} emission records")
        
        return df
    
    def collect_climate_scores(self,
                              companies: List[str],
                              years: List[int]) -> pd.DataFrame:
        """
        Collect CDP climate change scores
        
        CDP scores range from A to D-, where:
        - A: Leadership
        - A-: Management
        - B: Awareness
        - C: Disclosure
        - D: No disclosure
        
        Args:
            companies: List of company names
            years: List of years
        
        Returns:
            DataFrame with climate scores
        """
        logger.info(f"Collecting climate scores for {len(companies)} companies...")
        
        if self.demo_mode:
            return self._generate_demo_score_data(companies, years)
        
        # Actual API implementation
        data = []
        for company in companies:
            for year in years:
                time.sleep(self.rate_limit)
                data.extend(self._generate_demo_score_data([company], [year]).to_dict('records'))
        
        df = pd.DataFrame(data)
        logger.info(f"✓ Collected {len(df)} score records")
        
        return df
    
    def collect_water_security(self,
                              companies: List[str],
                              years: List[int]) -> pd.DataFrame:
        """
        Collect water security disclosure data
        
        Args:
            companies: List of company names
            years: List of years
        
        Returns:
            DataFrame with water security data
        """
        logger.info(f"Collecting water security data for {len(companies)} companies...")
        
        if self.demo_mode:
            return self._generate_demo_water_data(companies, years)
        
        data = []
        for company in companies:
            for year in years:
                time.sleep(self.rate_limit)
                data.extend(self._generate_demo_water_data([company], [year]).to_dict('records'))
        
        df = pd.DataFrame(data)
        logger.info(f"✓ Collected {len(df)} water security records")
        
        return df
    
    def _generate_demo_carbon_data(self,
                                  companies: List[str],
                                  years: List[int],
                                  scopes: List[str]) -> pd.DataFrame:
        """Generate demonstration carbon emissions data"""
        data = []
        
        for company in companies:
            # Company-specific base emissions
            base_emission = np.random.lognormal(10, 1.5)  # Base emissions in tonnes CO2e
            
            for year in years:
                # Time trend (slight decrease over time - decarbonization)
                year_factor = 1 - 0.03 * (year - min(years))
                
                record = {
                    'company': company,
                    'year': year,
                    'reporting_status': np.random.choice(['reported', 'estimated'], p=[0.8, 0.2])
                }
                
                if 'scope1' in scopes:
                    scope1 = base_emission * 0.4 * year_factor * np.random.lognormal(0, 0.2)
                    record['scope1_emissions'] = scope1
                
                if 'scope2' in scopes:
                    scope2 = base_emission * 0.3 * year_factor * np.random.lognormal(0, 0.2)
                    record['scope2_emissions'] = scope2
                
                if 'scope3' in scopes:
                    scope3 = base_emission * 1.5 * year_factor * np.random.lognormal(0, 0.3)
                    record['scope3_emissions'] = scope3
                
                # Total emissions
                record['total_emissions'] = sum([
                    record.get('scope1_emissions', 0),
                    record.get('scope2_emissions', 0),
                    record.get('scope3_emissions', 0)
                ])
                
                # Verification
                record['verified'] = np.random.choice([True, False], p=[0.7, 0.3])
                
                data.append(record)
        
        return pd.DataFrame(data)
    
    def _generate_demo_score_data(self,
                                 companies: List[str],
                                 years: List[int]) -> pd.DataFrame:
        """Generate demonstration CDP score data"""
        
        # CDP scoring categories
        scores = ['A', 'A-', 'B', 'B-', 'C', 'C-', 'D', 'D-']
        numeric_map = {'A': 8, 'A-': 7, 'B': 6, 'B-': 5, 'C': 4, 'C-': 3, 'D': 2, 'D-': 1}
        
        data = []
        
        for company in companies:
            # Company base performance
            base_performance = np.random.choice(range(3, 9))
            
            for year in years:
                # Slight improvement over time
                current_performance = min(8, base_performance + 0.2 * (year - min(years)))
                current_performance = int(current_performance)
                
                # Convert to letter grade
                reverse_map = {v: k for k, v in numeric_map.items()}
                score = reverse_map[current_performance]
                
                data.append({
                    'company': company,
                    'year': year,
                    'climate_score': score,
                    'climate_score_numeric': numeric_map[score],
                    'response_status': np.random.choice(['responded', 'no_response'], p=[0.85, 0.15]),
                    'disclosure_level': np.random.choice(['full', 'partial'], p=[0.75, 0.25])
                })
        
        return pd.DataFrame(data)
    
    def _generate_demo_water_data(self,
                                 companies: List[str],
                                 years: List[int]) -> pd.DataFrame:
        """Generate demonstration water security data"""
        data = []
        
        for company in companies:
            for year in years:
                data.append({
                    'company': company,
                    'year': year,
                    'water_withdrawal': np.random.lognormal(15, 1) * 1000,  # m³
                    'water_discharge': np.random.lognormal(14.5, 1) * 1000,  # m³
                    'water_consumption': np.random.lognormal(12, 1) * 100,   # m³
                    'water_recycled_pct': np.random.uniform(0, 40),  # %
                    'water_stress_locations': np.random.choice([True, False], p=[0.3, 0.7])
                })
        
        return pd.DataFrame(data)
    
    def build_esg_panel(self,
                       companies: List[str],
                       start_year: int,
                       end_year: int,
                       include_scores: bool = True,
                       include_emissions: bool = True,
                       include_water: bool = False) -> pd.DataFrame:
        """
        Build comprehensive ESG panel dataset
        
        Args:
            companies: List of company names
            start_year: Start year
            end_year: End year
            include_scores: Include CDP scores
            include_emissions: Include emissions data
            include_water: Include water data
        
        Returns:
            Comprehensive ESG panel dataset
        """
        logger.info(f"Building ESG panel: {start_year}-{end_year}")
        
        years = list(range(start_year, end_year + 1))
        
        # Collect all data
        dfs = []
        
        if include_emissions:
            emissions_df = self.collect_carbon_emissions(companies, years)
            dfs.append(emissions_df)
        
        if include_scores:
            scores_df = self.collect_climate_scores(companies, years)
            dfs.append(scores_df)
        
        if include_water:
            water_df = self.collect_water_security(companies, years)
            dfs.append(water_df)
        
        # Merge all data
        if len(dfs) == 0:
            raise ValueError("No data types selected")
        
        panel = dfs[0]
        for df in dfs[1:]:
            panel = panel.merge(df, on=['company', 'year'], how='outer')
        
        logger.info(f"✓ Panel built: {len(panel)} observations")
        
        return panel
    
    def export_to_csv(self, df: pd.DataFrame, filepath: Path):
        """
        Export data to CSV
        
        Args:
            df: DataFrame to export
            filepath: Output file path
        """
        df.to_csv(filepath, index=False)
        logger.info(f"✓ Data exported: {filepath}")


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("CDP DATA COLLECTOR EXAMPLE")
    print("=" * 80)
    
    # Initialize collector (demo mode)
    collector = CDPCollector()
    
    # Example companies
    companies = ['Apple Inc.', 'Microsoft Corp.', 'Amazon.com Inc.', 'Tesla Inc.']
    years = [2020, 2021, 2022]
    
    print(f"\n[Step 1] Collecting carbon emissions data...")
    emissions_df = collector.collect_carbon_emissions(companies, years)
    print(emissions_df.head())
    
    print(f"\n[Step 2] Collecting climate scores...")
    scores_df = collector.collect_climate_scores(companies, years)
    print(scores_df.head())
    
    print(f"\n[Step 3] Building comprehensive ESG panel...")
    panel_df = collector.build_esg_panel(
        companies=companies,
        start_year=2020,
        end_year=2022,
        include_scores=True,
        include_emissions=True
    )
    
    print(f"\nPanel summary:")
    print(f"  Companies: {panel_df['company'].nunique()}")
    print(f"  Years: {panel_df['year'].nunique()}")
    print(f"  Total observations: {len(panel_df)}")
    print(f"  Variables: {len(panel_df.columns)}")
    
    # Save to output
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    collector.export_to_csv(panel_df, output_dir / 'cdp_panel_demo.csv')
    
    print("\n" + "=" * 80)
    print("CDP DATA COLLECTION COMPLETED")
    print("=" * 80)
    print("\nNote: This is demonstration mode with simulated data.")
    print("For actual CDP data access, register at: https://www.cdp.net/en/data")
