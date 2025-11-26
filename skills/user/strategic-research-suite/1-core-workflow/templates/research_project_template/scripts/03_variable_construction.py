"""
03_variable_construction.py

Variable Construction for Strategic Management Research

This script constructs common variables used in strategic management research:
- Financial ratios (ROA, ROE, leverage, etc.)
- Growth measures
- Lag and lead variables
- Industry-adjusted variables
- Interaction terms

Usage:
    python 03_variable_construction.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VariableConstructor:
    """
    Construct variables for strategic management research
    
    Attributes:
        df: Input panel DataFrame
        firm_id: Firm identifier column
        time_id: Time identifier column
    """
    
    def __init__(self, df: pd.DataFrame,
                 firm_id: str = 'firm_id',
                 time_id: str = 'year'):
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        
    def calculate_financial_ratios(self) -> pd.DataFrame:
        """
        Calculate standard financial ratios
        
        Requires columns:
            - sales, total_assets, total_equity, net_income, rd_expenditure
        
        Creates:
            - roa: Return on Assets
            - roe: Return on Equity
            - leverage: Debt to Assets
            - rd_intensity: R&D to Sales
            - asset_turnover: Sales to Assets
        """
        logger.info("Calculating financial ratios...")
        
        # ROA = Net Income / Total Assets
        if 'net_income' in self.df.columns and 'total_assets' in self.df.columns:
            self.df['roa'] = self.df['net_income'] / self.df['total_assets']
            logger.info("  ✓ ROA calculated")
        
        # ROE = Net Income / Total Equity
        if 'net_income' in self.df.columns and 'total_equity' in self.df.columns:
            self.df['roe'] = self.df['net_income'] / self.df['total_equity']
            logger.info("  ✓ ROE calculated")
        
        # Leverage = (Total Assets - Total Equity) / Total Assets
        if 'total_assets' in self.df.columns and 'total_equity' in self.df.columns:
            self.df['leverage'] = (self.df['total_assets'] - self.df['total_equity']) / self.df['total_assets']
            logger.info("  ✓ Leverage calculated")
        
        # R&D Intensity = R&D Expenditure / Sales
        if 'rd_expenditure' in self.df.columns and 'sales' in self.df.columns:
            self.df['rd_intensity'] = self.df['rd_expenditure'] / self.df['sales']
            logger.info("  ✓ R&D Intensity calculated")
        
        # Asset Turnover = Sales / Total Assets
        if 'sales' in self.df.columns and 'total_assets' in self.df.columns:
            self.df['asset_turnover'] = self.df['sales'] / self.df['total_assets']
            logger.info("  ✓ Asset Turnover calculated")
        
        return self.df
    
    def calculate_growth_measures(self, variables: list = None) -> pd.DataFrame:
        """
        Calculate growth rates for specified variables
        
        Args:
            variables: List of variables to calculate growth (default: sales)
        
        Creates:
            - {var}_growth: Year-over-year growth rate
        """
        if variables is None:
            variables = ['sales']
        
        logger.info(f"Calculating growth measures for {len(variables)} variables...")
        
        for var in variables:
            if var in self.df.columns:
                # Sort by firm and time
                self.df = self.df.sort_values([self.firm_id, self.time_id])
                
                # Calculate growth within each firm
                self.df[f'{var}_growth'] = self.df.groupby(self.firm_id)[var].pct_change()
                
                logger.info(f"  ✓ {var}_growth calculated")
        
        return self.df
    
    def create_lags(self, variables: list, lags: int = 1) -> pd.DataFrame:
        """
        Create lagged variables
        
        Args:
            variables: List of variables to lag
            lags: Number of lags (default: 1)
        
        Creates:
            - {var}_lag{n}: Lagged variable
        """
        logger.info(f"Creating {lags} lag(s) for {len(variables)} variables...")
        
        # Sort by firm and time
        self.df = self.df.sort_values([self.firm_id, self.time_id])
        
        for var in variables:
            if var in self.df.columns:
                for lag in range(1, lags + 1):
                    self.df[f'{var}_lag{lag}'] = self.df.groupby(self.firm_id)[var].shift(lag)
                
                logger.info(f"  ✓ {var} lagged")
        
        return self.df
    
    def create_leads(self, variables: list, leads: int = 1) -> pd.DataFrame:
        """
        Create lead variables (future values)
        
        Args:
            variables: List of variables to lead
            leads: Number of leads (default: 1)
        
        Creates:
            - {var}_lead{n}: Lead variable
        """
        logger.info(f"Creating {leads} lead(s) for {len(variables)} variables...")
        
        # Sort by firm and time
        self.df = self.df.sort_values([self.firm_id, self.time_id])
        
        for var in variables:
            if var in self.df.columns:
                for lead in range(1, leads + 1):
                    self.df[f'{var}_lead{lead}'] = self.df.groupby(self.firm_id)[var].shift(-lead)
                
                logger.info(f"  ✓ {var} lead created")
        
        return self.df
    
    def create_industry_adjusted(self, variables: list, 
                                industry_var: str = 'industry') -> pd.DataFrame:
        """
        Create industry-adjusted variables
        
        Args:
            variables: List of variables to adjust
            industry_var: Industry classification variable
        
        Creates:
            - {var}_ind_adj: Industry-adjusted variable (firm value - industry mean)
        """
        if industry_var not in self.df.columns:
            logger.warning(f"Industry variable '{industry_var}' not found. Skipping.")
            return self.df
        
        logger.info(f"Creating industry-adjusted variables for {len(variables)} variables...")
        
        for var in variables:
            if var in self.df.columns:
                # Calculate industry-year means
                industry_means = self.df.groupby([industry_var, self.time_id])[var].transform('mean')
                
                # Subtract industry mean
                self.df[f'{var}_ind_adj'] = self.df[var] - industry_means
                
                logger.info(f"  ✓ {var}_ind_adj created")
        
        return self.df
    
    def create_interactions(self, var1: str, var2: str, 
                          name: str = None) -> pd.DataFrame:
        """
        Create interaction term
        
        Args:
            var1: First variable
            var2: Second variable
            name: Name for interaction term (default: var1_x_var2)
        
        Creates:
            - Interaction term
        """
        if var1 not in self.df.columns or var2 not in self.df.columns:
            logger.warning(f"Variables '{var1}' or '{var2}' not found. Skipping.")
            return self.df
        
        if name is None:
            name = f'{var1}_x_{var2}'
        
        self.df[name] = self.df[var1] * self.df[var2]
        logger.info(f"Created interaction term: {name}")
        
        return self.df
    
    def winsorize(self, variables: list, lower: float = 0.01, 
                 upper: float = 0.99) -> pd.DataFrame:
        """
        Winsorize variables to handle outliers
        
        Args:
            variables: List of variables to winsorize
            lower: Lower percentile (default: 1%)
            upper: Upper percentile (default: 99%)
        
        Creates:
            - {var}_wins: Winsorized variable
        """
        logger.info(f"Winsorizing {len(variables)} variables at {lower*100}% and {upper*100}%...")
        
        for var in variables:
            if var in self.df.columns:
                lower_bound = self.df[var].quantile(lower)
                upper_bound = self.df[var].quantile(upper)
                
                self.df[f'{var}_wins'] = self.df[var].clip(lower=lower_bound, upper=upper_bound)
                
                logger.info(f"  ✓ {var}_wins created")
        
        return self.df
    
    def standardize(self, variables: list) -> pd.DataFrame:
        """
        Standardize variables (mean=0, std=1)
        
        Args:
            variables: List of variables to standardize
        
        Creates:
            - {var}_std: Standardized variable
        """
        logger.info(f"Standardizing {len(variables)} variables...")
        
        for var in variables:
            if var in self.df.columns:
                self.df[f'{var}_std'] = (self.df[var] - self.df[var].mean()) / self.df[var].std()
                logger.info(f"  ✓ {var}_std created")
        
        return self.df


def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("Variable Construction Pipeline")
    logger.info("=" * 60)
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    processed_data_dir = base_dir / 'data' / 'processed'
    final_data_dir = base_dir / 'data' / 'final'
    
    # Create directories
    final_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load processed data
    logger.info("\n[Step 1] Loading processed panel data...")
    panel_file = processed_data_dir / 'panel_unbalanced.csv'
    
    if not panel_file.exists():
        logger.error(f"Panel data not found: {panel_file}")
        logger.error("Please run 02_panel_construction.py first")
        return
    
    df = pd.read_csv(panel_file)
    logger.info(f"Loaded {len(df)} observations")
    
    # Step 2: Initialize constructor
    constructor = VariableConstructor(df)
    
    # Step 3: Calculate financial ratios
    logger.info("\n[Step 2] Calculating financial ratios...")
    constructor.calculate_financial_ratios()
    
    # Step 4: Calculate growth measures
    logger.info("\n[Step 3] Calculating growth measures...")
    constructor.calculate_growth_measures(variables=['sales', 'employees'])
    
    # Step 5: Create lagged variables
    logger.info("\n[Step 4] Creating lagged variables...")
    constructor.create_lags(variables=['sales', 'rd_expenditure'], lags=1)
    
    # Step 6: Winsorize key variables
    logger.info("\n[Step 5] Winsorizing key variables...")
    if 'roa' in constructor.df.columns:
        constructor.winsorize(variables=['roa'], lower=0.01, upper=0.99)
    
    # Step 7: Save final dataset
    logger.info("\n[Step 6] Saving final dataset...")
    output_file = final_data_dir / 'analysis_dataset.csv'
    constructor.df.to_csv(output_file, index=False)
    logger.info(f"Saved final dataset: {output_file}")
    
    # Display summary
    logger.info("\n" + "=" * 60)
    logger.info("Variable Construction Summary")
    logger.info("=" * 60)
    logger.info(f"Total variables: {len(constructor.df.columns)}")
    logger.info(f"Total observations: {len(constructor.df)}")
    logger.info("\nNew variables created:")
    
    original_vars = set(df.columns)
    new_vars = set(constructor.df.columns) - original_vars
    for var in sorted(new_vars):
        logger.info(f"  - {var}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Variable construction completed successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
