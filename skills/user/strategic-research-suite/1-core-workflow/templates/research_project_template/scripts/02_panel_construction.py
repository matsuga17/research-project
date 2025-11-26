"""
02_panel_construction.py

Panel Dataset Construction Script

This script constructs a balanced or unbalanced panel dataset from raw data.

Features:
- Firm-year panel structure creation
- Missing period interpolation
- Panel balance checking
- Time-invariant variable handling

Usage:
    python 02_panel_construction.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from scripts.data_quality_checker import DataQualityChecker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PanelConstructor:
    """
    Construct panel datasets from raw data
    
    Attributes:
        df: Input DataFrame
        firm_id: Firm identifier column
        time_id: Time identifier column
        panel_type: 'balanced' or 'unbalanced'
    """
    
    def __init__(self, df: pd.DataFrame, 
                 firm_id: str = 'firm_id',
                 time_id: str = 'year',
                 panel_type: str = 'unbalanced'):
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.panel_type = panel_type
        
    def create_panel_structure(self) -> pd.DataFrame:
        """
        Create panel structure with all firm-year combinations
        
        Returns:
            DataFrame with complete panel structure
        """
        logger.info(f"Creating {self.panel_type} panel structure...")
        
        firms = self.df[self.firm_id].unique()
        years = self.df[self.time_id].unique()
        
        # Create all combinations
        from itertools import product
        all_combinations = pd.DataFrame(
            list(product(firms, years)),
            columns=[self.firm_id, self.time_id]
        )
        
        # Merge with original data
        panel_df = all_combinations.merge(
            self.df,
            on=[self.firm_id, self.time_id],
            how='left'
        )
        
        logger.info(f"Panel structure created: {len(panel_df)} observations")
        logger.info(f"Original data: {len(self.df)} observations")
        logger.info(f"Missing observations: {len(panel_df) - len(self.df)}")
        
        return panel_df
    
    def balance_panel(self, min_periods: int = None) -> pd.DataFrame:
        """
        Create balanced panel by removing firms with incomplete periods
        
        Args:
            min_periods: Minimum number of periods required (default: all periods)
        
        Returns:
            Balanced panel DataFrame
        """
        logger.info("Creating balanced panel...")
        
        # Count periods per firm
        period_counts = self.df.groupby(self.firm_id)[self.time_id].nunique()
        max_periods = period_counts.max()
        
        if min_periods is None:
            min_periods = max_periods
        
        # Keep only firms with sufficient periods
        valid_firms = period_counts[period_counts >= min_periods].index
        balanced_df = self.df[self.df[self.firm_id].isin(valid_firms)]
        
        logger.info(f"Balanced panel created:")
        logger.info(f"  Firms: {len(valid_firms)} (removed {len(period_counts) - len(valid_firms)})")
        logger.info(f"  Observations: {len(balanced_df)} (removed {len(self.df) - len(balanced_df)})")
        
        return balanced_df
    
    def interpolate_missing(self, columns: list = None, 
                          method: str = 'linear') -> pd.DataFrame:
        """
        Interpolate missing values within firm time series
        
        Args:
            columns: Columns to interpolate (default: all numeric columns)
            method: Interpolation method ('linear', 'ffill', 'bfill')
        
        Returns:
            DataFrame with interpolated values
        """
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            columns = [c for c in columns if c not in [self.firm_id, self.time_id]]
        
        logger.info(f"Interpolating {len(columns)} columns using {method} method...")
        
        df_interpolated = self.df.copy()
        
        for col in columns:
            # Interpolate within each firm's time series
            df_interpolated[col] = df_interpolated.groupby(self.firm_id)[col].transform(
                lambda x: x.interpolate(method=method) if method == 'linear' else x.fillna(method=method)
            )
        
        missing_before = self.df[columns].isnull().sum().sum()
        missing_after = df_interpolated[columns].isnull().sum().sum()
        
        logger.info(f"Missing values: {missing_before} → {missing_after} "
                   f"(filled {missing_before - missing_after})")
        
        return df_interpolated
    
    def add_time_invariant_vars(self, time_invariant_df: pd.DataFrame) -> pd.DataFrame:
        """
        Add time-invariant firm characteristics
        
        Args:
            time_invariant_df: DataFrame with firm-level characteristics
        
        Returns:
            Panel DataFrame with time-invariant variables added
        """
        logger.info("Adding time-invariant variables...")
        
        df_with_invariant = self.df.merge(
            time_invariant_df,
            on=self.firm_id,
            how='left'
        )
        
        added_cols = [c for c in time_invariant_df.columns if c != self.firm_id]
        logger.info(f"Added {len(added_cols)} time-invariant variables: {added_cols}")
        
        return df_with_invariant
    
    def check_panel_properties(self) -> dict:
        """
        Check panel dataset properties
        
        Returns:
            Dictionary with panel properties
        """
        props = {}
        
        # Basic dimensions
        props['n_firms'] = self.df[self.firm_id].nunique()
        props['n_periods'] = self.df[self.time_id].nunique()
        props['n_observations'] = len(self.df)
        
        # Balance check
        period_counts = self.df.groupby(self.firm_id)[self.time_id].count()
        props['balanced'] = (period_counts.std() == 0)
        props['min_periods'] = period_counts.min()
        props['max_periods'] = period_counts.max()
        props['mean_periods'] = period_counts.mean()
        
        # Time range
        props['start_year'] = self.df[self.time_id].min()
        props['end_year'] = self.df[self.time_id].max()
        
        return props


def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("Panel Construction Pipeline")
    logger.info("=" * 60)
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    raw_data_dir = base_dir / 'data' / 'raw'
    processed_data_dir = base_dir / 'data' / 'processed'
    
    # Create directories if they don't exist
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load raw data
    logger.info("\n[Step 1] Loading raw data...")
    raw_file = raw_data_dir / 'firm_data_raw.csv'
    
    if not raw_file.exists():
        logger.warning(f"Raw data file not found: {raw_file}")
        logger.info("Creating sample data for demonstration...")
        
        # Create sample data
        np.random.seed(42)
        n_firms = 50
        n_years = 10
        
        data = []
        for firm in range(1, n_firms + 1):
            # Randomly drop some years to create unbalanced panel
            available_years = np.random.choice(
                range(2013, 2013 + n_years),
                size=np.random.randint(5, n_years + 1),
                replace=False
            )
            
            for year in available_years:
                data.append({
                    'firm_id': firm,
                    'year': year,
                    'sales': np.random.lognormal(10, 2),
                    'employees': np.random.lognormal(6, 1.5),
                    'rd_expenditure': np.random.lognormal(7, 2),
                    'net_income': np.random.normal(100, 50)
                })
        
        df = pd.DataFrame(data)
        df.to_csv(raw_file, index=False)
        logger.info(f"Sample data created: {raw_file}")
    else:
        df = pd.read_csv(raw_file)
    
    logger.info(f"Loaded {len(df)} observations")
    
    # Step 2: Check initial data quality
    logger.info("\n[Step 2] Initial data quality check...")
    checker = DataQualityChecker(df)
    initial_report = checker.check_all()
    
    # Step 3: Construct panel
    logger.info("\n[Step 3] Constructing panel dataset...")
    constructor = PanelConstructor(df, firm_id='firm_id', time_id='year')
    
    # Check panel properties
    props = constructor.check_panel_properties()
    logger.info(f"\nPanel properties:")
    for key, value in props.items():
        logger.info(f"  {key}: {value}")
    
    # Step 4: Create balanced panel (optional)
    logger.info("\n[Step 4] Creating balanced panel...")
    df_balanced = constructor.balance_panel(min_periods=8)
    
    # Step 5: Interpolate missing values
    logger.info("\n[Step 5] Interpolating missing values...")
    df_interpolated = constructor.interpolate_missing(method='linear')
    
    # Step 6: Final quality check
    logger.info("\n[Step 6] Final data quality check...")
    constructor.df = df_interpolated
    props_final = constructor.check_panel_properties()
    
    logger.info(f"\nFinal panel properties:")
    for key, value in props_final.items():
        logger.info(f"  {key}: {value}")
    
    # Step 7: Save processed data
    logger.info("\n[Step 7] Saving processed data...")
    
    # Save unbalanced panel
    output_file_unbalanced = processed_data_dir / 'panel_unbalanced.csv'
    df_interpolated.to_csv(output_file_unbalanced, index=False)
    logger.info(f"Saved unbalanced panel: {output_file_unbalanced}")
    
    # Save balanced panel
    output_file_balanced = processed_data_dir / 'panel_balanced.csv'
    df_balanced.to_csv(output_file_balanced, index=False)
    logger.info(f"Saved balanced panel: {output_file_balanced}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Panel construction completed successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
