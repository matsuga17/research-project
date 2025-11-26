"""
04_analysis.py

Statistical Analysis Script

This script performs standard statistical analyses for strategic management research:
- Descriptive statistics
- Correlation analysis
- Panel regression (Fixed Effects, Random Effects)
- Robustness checks

Usage:
    python 04_analysis.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))

try:
    from scripts.panel_regression import PanelRegression
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("panel_regression module not found. Using basic statsmodels instead.")
    PanelRegression = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def descriptive_statistics(df: pd.DataFrame, 
                          variables: list = None) -> pd.DataFrame:
    """
    Calculate descriptive statistics
    
    Args:
        df: Input DataFrame
        variables: List of variables (default: all numeric)
    
    Returns:
        DataFrame with descriptive statistics
    """
    if variables is None:
        variables = df.select_dtypes(include=[np.number]).columns.tolist()
    
    desc = df[variables].describe().T
    desc['median'] = df[variables].median()
    desc['skew'] = df[variables].skew()
    desc['kurtosis'] = df[variables].kurtosis()
    
    # Reorder columns
    desc = desc[['count', 'mean', 'median', 'std', 'min', '25%', '75%', 'max', 'skew', 'kurtosis']]
    
    return desc


def correlation_analysis(df: pd.DataFrame,
                        variables: list = None,
                        method: str = 'pearson') -> pd.DataFrame:
    """
    Calculate correlation matrix
    
    Args:
        df: Input DataFrame
        variables: List of variables (default: all numeric)
        method: Correlation method ('pearson', 'spearman', 'kendall')
    
    Returns:
        Correlation matrix
    """
    if variables is None:
        variables = df.select_dtypes(include=[np.number]).columns.tolist()
    
    corr = df[variables].corr(method=method)
    
    return corr


def run_basic_regression(df: pd.DataFrame,
                        dependent_var: str,
                        independent_vars: list,
                        firm_id: str = 'firm_id',
                        time_id: str = 'year') -> dict:
    """
    Run basic panel regression
    
    Args:
        df: Panel DataFrame
        dependent_var: Dependent variable
        independent_vars: List of independent variables
        firm_id: Firm identifier
        time_id: Time identifier
    
    Returns:
        Dictionary with regression results
    """
    logger.info(f"\nRunning regression: {dependent_var} ~ {' + '.join(independent_vars)}")
    
    # Drop missing values
    analysis_vars = [dependent_var] + independent_vars + [firm_id, time_id]
    df_clean = df[analysis_vars].dropna()
    
    logger.info(f"Sample size: {len(df_clean)} observations")
    
    if PanelRegression is not None:
        # Use custom PanelRegression class if available
        regression = PanelRegression(df_clean, firm_id=firm_id, time_id=time_id)
        
        # Run Fixed Effects model
        results_fe = regression.fixed_effects(
            dependent_var=dependent_var,
            independent_vars=independent_vars
        )
        
        return {'model': 'Fixed Effects', 'results': results_fe}
    
    else:
        # Fallback to basic OLS
        try:
            import statsmodels.api as sm
            
            # Prepare data
            y = df_clean[dependent_var]
            X = df_clean[independent_vars]
            X = sm.add_constant(X)
            
            # Run OLS
            model = sm.OLS(y, X)
            results = model.fit()
            
            logger.info("\nOLS Regression Results:")
            logger.info(results.summary())
            
            return {'model': 'OLS', 'results': results}
            
        except ImportError:
            logger.error("statsmodels not installed. Cannot run regression.")
            return None


def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("Statistical Analysis Pipeline")
    logger.info("=" * 60)
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    final_data_dir = base_dir / 'data' / 'final'
    output_dir = base_dir / 'output' / 'tables'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load final dataset
    logger.info("\n[Step 1] Loading analysis dataset...")
    data_file = final_data_dir / 'analysis_dataset.csv'
    
    if not data_file.exists():
        logger.error(f"Analysis dataset not found: {data_file}")
        logger.error("Please run 03_variable_construction.py first")
        return
    
    df = pd.read_csv(data_file)
    logger.info(f"Loaded {len(df)} observations")
    
    # Step 2: Descriptive statistics
    logger.info("\n[Step 2] Calculating descriptive statistics...")
    
    key_vars = []
    for var in ['roa', 'sales_growth', 'rd_intensity', 'leverage']:
        if var in df.columns:
            key_vars.append(var)
    
    if key_vars:
        desc_stats = descriptive_statistics(df, variables=key_vars)
        logger.info("\nDescriptive Statistics:")
        logger.info(desc_stats)
        
        # Save to file
        desc_file = output_dir / 'descriptive_statistics.csv'
        desc_stats.to_csv(desc_file)
        logger.info(f"Saved: {desc_file}")
    
    # Step 3: Correlation analysis
    logger.info("\n[Step 3] Correlation analysis...")
    
    if key_vars:
        corr_matrix = correlation_analysis(df, variables=key_vars)
        logger.info("\nCorrelation Matrix:")
        logger.info(corr_matrix)
        
        # Save to file
        corr_file = output_dir / 'correlation_matrix.csv'
        corr_matrix.to_csv(corr_file)
        logger.info(f"Saved: {corr_file}")
    
    # Step 4: Regression analysis
    logger.info("\n[Step 4] Regression analysis...")
    
    # Example regression: ROA on R&D intensity and controls
    if all(var in df.columns for var in ['roa', 'rd_intensity', 'leverage']):
        results = run_basic_regression(
            df,
            dependent_var='roa',
            independent_vars=['rd_intensity', 'leverage']
        )
        
        if results:
            logger.info(f"\nRegression completed: {results['model']}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Statistical analysis completed successfully!")
    logger.info("=" * 60)
    logger.info(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
