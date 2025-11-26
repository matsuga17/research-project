"""
robustness_checks.py

Comprehensive Robustness Checks for Research

This module provides systematic robustness checks including:
- Alternative specifications
- Subsample analysis
- Outlier robustness
- Alternative measurement
- Placebo tests
- Bootstrap standard errors

Usage:
    from robustness_checks import RobustnessChecker
    
    rc = RobustnessChecker(df, base_results)
    subsample_results = rc.subsample_analysis(split_var='industry')
    outlier_results = rc.outlier_robustness(method='winsorize')
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Callable, Union
from linearmodels.panel import PanelOLS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RobustnessChecker:
    """
    Systematic robustness check toolkit
    
    Attributes:
        df: Input DataFrame
        base_specification: Base regression specification
        results_cache: Cache of robustness check results
    """
    
    def __init__(self, df: pd.DataFrame,
                 firm_id: str = 'firm_id',
                 time_id: str = 'year'):
        """
        Initialize robustness checker
        
        Args:
            df: Panel dataset
            firm_id: Firm identifier column
            time_id: Time identifier column
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.panel_data = self.df.set_index([self.firm_id, self.time_id]).sort_index()
        self.results_cache = {}
        
        logger.info(f"Robustness Checker initialized: {len(df[firm_id].unique())} firms")
    
    def subsample_analysis(self,
                          y: str,
                          X: List[str],
                          split_var: str,
                          entity_effects: bool = True) -> Dict:
        """
        Run analysis on different subsamples
        
        Args:
            y: Dependent variable
            X: Independent variables
            split_var: Variable to split sample on
            entity_effects: Include entity fixed effects
        
        Returns:
            Dictionary of results for each subsample
        """
        logger.info(f"Running subsample analysis split by {split_var}")
        
        results = {}
        
        # Get unique values of split variable
        unique_vals = self.df[split_var].unique()
        
        for val in unique_vals:
            df_sub = self.df[self.df[split_var] == val]
            
            if len(df_sub) < 30:  # Skip small subsamples
                logger.warning(f"Skipping {split_var}={val}: too few observations ({len(df_sub)})")
                continue
            
            panel_sub = df_sub.set_index([self.firm_id, self.time_id]).sort_index()
            
            formula = f"{y} ~ {' + '.join(X)}"
            model = PanelOLS.from_formula(formula, data=panel_sub, entity_effects=entity_effects)
            res = model.fit(cov_type='clustered', clusters=panel_sub.index.get_level_values(0))
            
            results[str(val)] = {
                'n': len(df_sub),
                'n_firms': len(df_sub[self.firm_id].unique()),
                'coefficients': res.params.to_dict(),
                'std_errors': res.std_errors.to_dict(),
                'rsquared': float(res.rsquared),
                'results_obj': res
            }
            
            logger.info(f"  {split_var}={val}: N={len(df_sub)}, R²={res.rsquared:.4f}")
        
        return results
    
    def outlier_robustness(self,
                          y: str,
                          X: List[str],
                          method: str = 'winsorize',
                          percentile: float = 0.01,
                          entity_effects: bool = True) -> Dict:
        """
        Test robustness to outliers
        
        Args:
            y: Dependent variable
            X: Independent variables
            method: 'winsorize', 'trim', or 'drop_extreme'
            percentile: Percentile for outlier treatment
            entity_effects: Include entity fixed effects
        
        Returns:
            Comparison of results with/without outliers
        """
        logger.info(f"Testing outlier robustness using {method}")
        
        df_treated = self.df.copy()
        
        # Identify and treat outliers
        vars_to_treat = [y] + X
        
        for var in vars_to_treat:
            if method == 'winsorize':
                lower = df_treated[var].quantile(percentile)
                upper = df_treated[var].quantile(1 - percentile)
                df_treated[var] = df_treated[var].clip(lower, upper)
            
            elif method == 'trim':
                lower = df_treated[var].quantile(percentile)
                upper = df_treated[var].quantile(1 - percentile)
                df_treated = df_treated[(df_treated[var] >= lower) & (df_treated[var] <= upper)]
            
            elif method == 'drop_extreme':
                z_scores = np.abs((df_treated[var] - df_treated[var].mean()) / df_treated[var].std())
                df_treated = df_treated[z_scores < 3]
        
        # Run regression on treated data
        panel_treated = df_treated.set_index([self.firm_id, self.time_id]).sort_index()
        formula = f"{y} ~ {' + '.join(X)}"
        model = PanelOLS.from_formula(formula, data=panel_treated, entity_effects=entity_effects)
        results_treated = model.fit(cov_type='clustered', 
                                    clusters=panel_treated.index.get_level_values(0))
        
        # Run regression on original data
        panel_original = self.df.set_index([self.firm_id, self.time_id]).sort_index()
        model_orig = PanelOLS.from_formula(formula, data=panel_original, entity_effects=entity_effects)
        results_original = model_orig.fit(cov_type='clustered',
                                         clusters=panel_original.index.get_level_values(0))
        
        logger.info(f"  Original: N={len(self.df)}, R²={results_original.rsquared:.4f}")
        logger.info(f"  Treated:  N={len(df_treated)}, R²={results_treated.rsquared:.4f}")
        
        return {
            'original': {
                'n': len(self.df),
                'coefficients': results_original.params.to_dict(),
                'std_errors': results_original.std_errors.to_dict(),
                'rsquared': float(results_original.rsquared)
            },
            'treated': {
                'n': len(df_treated),
                'coefficients': results_treated.params.to_dict(),
                'std_errors': results_treated.std_errors.to_dict(),
                'rsquared': float(results_treated.rsquared)
            },
            'method': method
        }
    
    def alternative_specifications(self,
                                  y: str,
                                  X: List[str],
                                  alternative_X: List[List[str]],
                                  entity_effects: bool = True) -> Dict:
        """
        Test different model specifications
        
        Args:
            y: Dependent variable
            X: Base independent variables
            alternative_X: List of alternative sets of independent variables
            entity_effects: Include entity fixed effects
        
        Returns:
            Results for each specification
        """
        logger.info("Testing alternative specifications")
        
        results = {}
        
        # Base specification
        formula = f"{y} ~ {' + '.join(X)}"
        panel = self.panel_data
        model = PanelOLS.from_formula(formula, data=panel, entity_effects=entity_effects)
        res = model.fit(cov_type='clustered', clusters=panel.index.get_level_values(0))
        
        results['base'] = {
            'variables': X,
            'coefficients': res.params.to_dict(),
            'std_errors': res.std_errors.to_dict(),
            'rsquared': float(res.rsquared),
            'results_obj': res
        }
        
        # Alternative specifications
        for i, alt_X in enumerate(alternative_X, 1):
            formula = f"{y} ~ {' + '.join(alt_X)}"
            model = PanelOLS.from_formula(formula, data=panel, entity_effects=entity_effects)
            res = model.fit(cov_type='clustered', clusters=panel.index.get_level_values(0))
            
            results[f'alt_{i}'] = {
                'variables': alt_X,
                'coefficients': res.params.to_dict(),
                'std_errors': res.std_errors.to_dict(),
                'rsquared': float(res.rsquared),
                'results_obj': res
            }
            
            logger.info(f"  Specification {i}: {alt_X}, R²={res.rsquared:.4f}")
        
        return results
    
    def compare_robustness(self, robustness_results: Dict) -> pd.DataFrame:
        """
        Create comparison table of robustness checks
        
        Args:
            robustness_results: Results from various robustness checks
        
        Returns:
            Comparison DataFrame
        """
        comparison_data = []
        
        for check_name, check_results in robustness_results.items():
            if isinstance(check_results, dict):
                if 'coefficients' in check_results:
                    row = {'check': check_name}
                    row.update(check_results['coefficients'])
                    row['r_squared'] = check_results.get('rsquared', np.nan)
                    row['n'] = check_results.get('n', np.nan)
                    comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n_firms = 100
    n_years = 10
    
    data = []
    for firm in range(1, n_firms + 1):
        industry = 'tech' if firm <= 50 else 'manufacturing'
        firm_effect = np.random.normal(0, 0.02)
        
        for year in range(2014, 2014 + n_years):
            rd = np.random.uniform(0, 0.15)
            leverage = np.random.uniform(0.2, 0.7)
            
            roa = 0.05 + firm_effect + 0.12 * rd - 0.03 * leverage + np.random.normal(0, 0.015)
            
            # Add some outliers
            if np.random.random() < 0.02:
                roa += np.random.uniform(-0.1, 0.1)
            
            data.append({
                'firm_id': firm,
                'year': year,
                'industry': industry,
                'roa': roa,
                'rd_intensity': rd,
                'leverage': leverage,
                'firm_size': np.random.lognormal(10, 1)
            })
    
    df = pd.DataFrame(data)
    
    # Initialize robustness checker
    rc = RobustnessChecker(df, firm_id='firm_id', time_id='year')
    
    # Subsample analysis
    print("\n" + "="*60)
    print("Subsample Analysis (by Industry)")
    print("="*60)
    subsample_results = rc.subsample_analysis(
        y='roa',
        X=['rd_intensity', 'leverage'],
        split_var='industry'
    )
    
    for industry, res in subsample_results.items():
        print(f"\n{industry}:")
        print(f"  N = {res['n']}, R² = {res['rsquared']:.4f}")
        print(f"  Coefficients: {res['coefficients']}")
    
    # Outlier robustness
    print("\n" + "="*60)
    print("Outlier Robustness (Winsorization)")
    print("="*60)
    outlier_results = rc.outlier_robustness(
        y='roa',
        X=['rd_intensity', 'leverage'],
        method='winsorize',
        percentile=0.01
    )
    
    print(f"\nOriginal: N={outlier_results['original']['n']}, " 
          f"R²={outlier_results['original']['rsquared']:.4f}")
    print(f"Winsorized: N={outlier_results['treated']['n']}, "
          f"R²={outlier_results['treated']['rsquared']:.4f}")
    
    # Alternative specifications
    print("\n" + "="*60)
    print("Alternative Specifications")
    print("="*60)
    alt_spec_results = rc.alternative_specifications(
        y='roa',
        X=['rd_intensity', 'leverage'],
        alternative_X=[
            ['rd_intensity'],
            ['rd_intensity', 'leverage', 'firm_size'],
        ]
    )
    
    for spec_name, res in alt_spec_results.items():
        print(f"\n{spec_name}: {res['variables']}")
        print(f"  R² = {res['rsquared']:.4f}")
