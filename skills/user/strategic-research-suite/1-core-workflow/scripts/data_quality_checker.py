"""
data_quality_checker.py

Comprehensive data quality checker for panel datasets

This module provides automated quality assurance checks for strategic
management research datasets, including:
- Missing value detection
- Outlier detection
- Panel balance checks
- Duplicate detection
- Data type validation

Usage:
    from data_quality_checker import DataQualityChecker
    
    checker = DataQualityChecker(df, firm_id='firm_id', time_id='year')
    report = checker.check_all()
    print(checker.generate_report())
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataQualityChecker:
    """
    Automated quality checker for panel datasets
    
    Attributes:
        df: Input DataFrame
        firm_id: Column name for firm identifier
        time_id: Column name for time identifier
        report: Dictionary storing check results
    """
    
    def __init__(self, df: pd.DataFrame, 
                 firm_id: str = 'firm_id',
                 time_id: str = 'year'):
        """
        Initialize the quality checker
        
        Args:
            df: Panel dataset to check
            firm_id: Name of firm identifier column
            time_id: Name of time identifier column
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.report = {}
        
        logger.info(f"Initialized DataQualityChecker: {len(df)} rows, {len(df.columns)} columns")
    
    def check_all(self) -> Dict:
        """
        Run all quality checks
        
        Returns:
            Dictionary containing all check results
        """
        logger.info("Running comprehensive quality checks...")
        
        self.report['missing'] = self.check_missing()
        self.report['outliers'] = self.check_outliers()
        self.report['dtypes'] = self.check_dtypes()
        self.report['balance'] = self.check_panel_balance()
        self.report['duplicates'] = self.check_duplicates()
        
        logger.info("Quality checks completed")
        return self.report
    
    def check_missing(self) -> Dict:
        """
        Check for missing values
        
        Returns:
            Dictionary with missing value counts and percentages
        """
        logger.info("Checking for missing values...")
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        result = {
            'missing_counts': missing[missing > 0].to_dict(),
            'missing_percentage': missing_pct[missing_pct > 0].to_dict(),
            'total_missing': int(missing.sum()),
            'columns_with_missing': int((missing > 0).sum())
        }
        
        if result['total_missing'] > 0:
            logger.warning(f"Found {result['total_missing']} missing values "
                          f"across {result['columns_with_missing']} columns")
        else:
            logger.info("No missing values found")
        
        return result
    
    def check_outliers(self, threshold: float = 3.0) -> Dict:
        """
        Detect outliers using Z-score method
        
        Args:
            threshold: Z-score threshold (default: 3.0)
        
        Returns:
            Dictionary with outlier counts per column
        """
        logger.info(f"Checking for outliers (threshold: {threshold})...")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            if col in [self.firm_id, self.time_id]:
                continue
                
            values = self.df[col].dropna()
            if len(values) == 0:
                continue
                
            z_scores = np.abs((values - values.mean()) / values.std())
            outlier_count = (z_scores > threshold).sum()
            
            if outlier_count > 0:
                outliers[col] = {
                    'count': int(outlier_count),
                    'percentage': float(outlier_count / len(values) * 100),
                    'min_value': float(values.min()),
                    'max_value': float(values.max())
                }
        
        if outliers:
            logger.warning(f"Found outliers in {len(outliers)} columns")
        else:
            logger.info("No outliers detected")
        
        return outliers
    
    def check_panel_balance(self) -> Dict:
        """
        Check panel dataset balance
        
        Returns:
            Dictionary with panel balance statistics
        """
        logger.info("Checking panel balance...")
        
        if self.firm_id not in self.df.columns or self.time_id not in self.df.columns:
            logger.error(f"Required columns not found: {self.firm_id}, {self.time_id}")
            return {}
        
        counts = self.df.groupby(self.firm_id)[self.time_id].count()
        
        result = {
            'total_firms': int(len(counts)),
            'total_observations': int(len(self.df)),
            'max_years': int(counts.max()),
            'min_years': int(counts.min()),
            'mean_years': float(counts.mean()),
            'median_years': float(counts.median()),
            'balanced': bool(counts.max() == counts.min())
        }
        
        if result['balanced']:
            logger.info(f"Panel is balanced: {result['total_firms']} firms × "
                       f"{result['max_years']} years = {result['total_observations']} obs")
        else:
            logger.warning(f"Panel is unbalanced: {result['min_years']}-{result['max_years']} "
                          f"years per firm (mean: {result['mean_years']:.1f})")
        
        return result
    
    def check_duplicates(self) -> Dict:
        """
        Check for duplicate rows
        
        Returns:
            Dictionary with duplicate statistics
        """
        logger.info("Checking for duplicates...")
        
        # Check full duplicates
        full_duplicates = self.df.duplicated().sum()
        
        # Check key duplicates (firm_id, time_id)
        if self.firm_id in self.df.columns and self.time_id in self.df.columns:
            key_duplicates = self.df.duplicated(subset=[self.firm_id, self.time_id]).sum()
        else:
            key_duplicates = 0
        
        result = {
            'full_duplicates': int(full_duplicates),
            'key_duplicates': int(key_duplicates),
            'full_duplicate_percentage': float(full_duplicates / len(self.df) * 100),
            'key_duplicate_percentage': float(key_duplicates / len(self.df) * 100)
        }
        
        if key_duplicates > 0:
            logger.warning(f"Found {key_duplicates} duplicate (firm_id, time_id) pairs")
        else:
            logger.info("No duplicate keys found")
        
        return result
    
    def check_dtypes(self) -> Dict:
        """
        Check data types of all columns
        
        Returns:
            Dictionary mapping column names to data types
        """
        logger.info("Checking data types...")
        
        return {col: str(dtype) for col, dtype in self.df.dtypes.items()}
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate human-readable quality report
        
        Args:
            output_path: Optional path to save report
        
        Returns:
            Formatted report string
        """
        logger.info("Generating quality report...")
        
        report_text = f"""
{'='*80}
DATA QUALITY REPORT
{'='*80}

Dataset Overview
----------------
- Total rows: {len(self.df):,}
- Total columns: {len(self.df.columns)}
- Firm ID column: {self.firm_id}
- Time ID column: {self.time_id}


Missing Values
--------------
{self._format_section(self.report.get('missing', {}))}

Outliers (Z-score > 3.0)
-------------------------
{self._format_section(self.report.get('outliers', {}))}

Panel Balance
-------------
{self._format_section(self.report.get('balance', {}))}

Duplicates
----------
{self._format_section(self.report.get('duplicates', {}))}

Data Types
----------
{self._format_dtypes(self.report.get('dtypes', {}))}

{'='*80}
"""
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            logger.info(f"Report saved to: {output_path}")
        
        return report_text
    
    @staticmethod
    def _format_section(data: Dict, indent: int = 0) -> str:
        """Format dictionary as indented text"""
        if not data:
            return "  (No issues found)"
        
        lines = []
        for k, v in data.items():
            if isinstance(v, dict):
                lines.append(f"{'  ' * indent}{k}:")
                lines.append(DataQualityChecker._format_section(v, indent + 1))
            else:
                if isinstance(v, float):
                    lines.append(f"{'  ' * indent}{k}: {v:.3f}")
                else:
                    lines.append(f"{'  ' * indent}{k}: {v}")
        return '\n'.join(lines)
    
    @staticmethod
    def _format_dtypes(dtypes: Dict) -> str:
        """Format data types in columnar format"""
        if not dtypes:
            return "  (No data)"
        
        lines = []
        for col, dtype in sorted(dtypes.items()):
            lines.append(f"  {col:30s} {dtype}")
        return '\n'.join(lines)


# Example usage
if __name__ == "__main__":
    # Create sample panel data
    np.random.seed(42)
    
    df = pd.DataFrame({
        'firm_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'year': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
        'roa': [0.05, 0.06, np.nan, 0.08, 0.09, 0.10, 0.03, 0.04, 0.05],
        'sales': [1000, 1100, 1200, 500, np.nan, 600, 2000, 2100, 2200],
        'leverage': [0.3, 0.4, 0.5, 0.6, 0.5, 0.4, 0.2, 0.3, 0.4]
    })
    
    # Run quality checks
    checker = DataQualityChecker(df)
    report = checker.check_all()
    
    # Print report
    print(checker.generate_report())
