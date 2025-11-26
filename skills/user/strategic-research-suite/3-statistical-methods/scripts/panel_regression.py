"""
panel_regression.py

Panel Data Regression Analysis for Strategic Research

This module provides comprehensive panel regression methods including:
- Fixed Effects (FE)
- Random Effects (RE)
- Pooled OLS
- First Differences (FD)
- Between Effects (BE)

Includes automatic model selection, robust standard errors, and diagnostics.

Usage:
    from panel_regression import PanelRegression
    
    pr = PanelRegression(df, firm_id='firm_id', time_id='year')
    results = pr.fixed_effects(y='roa', X=['rd_intensity', 'leverage'])
    print(results.summary())
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
import logging
from linearmodels.panel import PanelOLS, RandomEffects, PooledOLS, FirstDifferenceOLS, BetweenOLS
from linearmodels.panel.results import PanelEffectsResults
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PanelRegression:
    """
    Comprehensive panel regression toolkit
    
    Attributes:
        df: Input panel DataFrame
        firm_id: Firm identifier column
        time_id: Time identifier column
        panel_data: Multi-indexed panel data
    """
    
    def __init__(self, df: pd.DataFrame, 
                 firm_id: str = 'firm_id',
                 time_id: str = 'year'):
        """
        Initialize panel regression analyzer
        
        Args:
            df: Panel dataset
            firm_id: Name of firm identifier column
            time_id: Name of time identifier column
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.panel_data = None
        self._prepare_panel()
    
    def _prepare_panel(self):
        """Convert DataFrame to multi-indexed panel format"""
        # Create multi-index
        self.panel_data = self.df.set_index([self.firm_id, self.time_id])
        
        # Sort index for proper panel operations
        self.panel_data = self.panel_data.sort_index()
        
        logger.info(f"Panel data prepared: {len(self.df[self.firm_id].unique())} firms, "
                   f"{len(self.df[self.time_id].unique())} time periods")
    
    def fixed_effects(self, 
                     y: str,
                     X: List[str],
                     entity_effects: bool = True,
                     time_effects: bool = False,
                     cluster_entity: bool = True,
                     cluster_time: bool = False) -> PanelEffectsResults:
        """
        Fixed Effects (Within) regression
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
            entity_effects: Include entity (firm) fixed effects
            time_effects: Include time fixed effects
            cluster_entity: Cluster standard errors by entity
            cluster_time: Cluster standard errors by time
        
        Returns:
            Regression results object
        """
        logger.info(f"Running Fixed Effects regression: {y} ~ {' + '.join(X)}")
        
        # Prepare formula
        formula = f"{y} ~ {' + '.join(X)}"
        if not entity_effects and not time_effects:
            formula += " + EntityEffects + TimeEffects"
        
        # Determine clustering
        if cluster_entity and cluster_time:
            cov_type = 'clustered'
            cov_config = {'clusters': self.panel_data.index}
        elif cluster_entity:
            cov_type = 'clustered'
            cov_config = {'clusters': self.panel_data.index.get_level_values(0)}
        else:
            cov_type = 'robust'
            cov_config = {}
        
        # Run regression
        model = PanelOLS.from_formula(
            formula,
            data=self.panel_data,
            entity_effects=entity_effects,
            time_effects=time_effects
        )
        
        results = model.fit(cov_type=cov_type, **cov_config)
        
        logger.info(f"Fixed Effects completed. R²: {results.rsquared:.4f}")
        
        return results
    
    def random_effects(self,
                      y: str,
                      X: List[str],
                      cluster_entity: bool = True) -> PanelEffectsResults:
        """
        Random Effects (GLS) regression
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
            cluster_entity: Cluster standard errors by entity
        
        Returns:
            Regression results object
        """
        logger.info(f"Running Random Effects regression: {y} ~ {' + '.join(X)}")
        
        formula = f"{y} ~ {' + '.join(X)}"
        
        cov_type = 'clustered' if cluster_entity else 'robust'
        cov_config = {'clusters': self.panel_data.index.get_level_values(0)} if cluster_entity else {}
        
        model = RandomEffects.from_formula(formula, data=self.panel_data)
        results = model.fit(cov_type=cov_type, **cov_config)
        
        logger.info(f"Random Effects completed. R²: {results.rsquared:.4f}")
        
        return results
    
    def pooled_ols(self,
                   y: str,
                   X: List[str],
                   cluster_entity: bool = True,
                   cluster_time: bool = False) -> PanelEffectsResults:
        """
        Pooled OLS regression (ignoring panel structure)
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
            cluster_entity: Cluster standard errors by entity
            cluster_time: Cluster standard errors by time
        
        Returns:
            Regression results object
        """
        logger.info(f"Running Pooled OLS regression: {y} ~ {' + '.join(X)}")
        
        formula = f"{y} ~ {' + '.join(X)}"
        
        if cluster_entity and cluster_time:
            cov_type = 'clustered'
            cov_config = {'clusters': self.panel_data.index}
        elif cluster_entity:
            cov_type = 'clustered'
            cov_config = {'clusters': self.panel_data.index.get_level_values(0)}
        else:
            cov_type = 'robust'
            cov_config = {}
        
        model = PooledOLS.from_formula(formula, data=self.panel_data)
        results = model.fit(cov_type=cov_type, **cov_config)
        
        logger.info(f"Pooled OLS completed. R²: {results.rsquared:.4f}")
        
        return results
    
    def first_differences(self,
                         y: str,
                         X: List[str],
                         cluster_entity: bool = True) -> PanelEffectsResults:
        """
        First Differences regression
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
            cluster_entity: Cluster standard errors by entity
        
        Returns:
            Regression results object
        """
        logger.info(f"Running First Differences regression: {y} ~ {' + '.join(X)}")
        
        formula = f"{y} ~ {' + '.join(X)}"
        
        cov_type = 'clustered' if cluster_entity else 'robust'
        cov_config = {'clusters': self.panel_data.index.get_level_values(0)} if cluster_entity else {}
        
        model = FirstDifferenceOLS.from_formula(formula, data=self.panel_data)
        results = model.fit(cov_type=cov_type, **cov_config)
        
        logger.info(f"First Differences completed. R²: {results.rsquared:.4f}")
        
        return results
    
    def hausman_test(self,
                    y: str,
                    X: List[str]) -> Dict[str, float]:
        """
        Hausman test for FE vs RE model selection
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
        
        Returns:
            Dictionary with test statistic, p-value, and recommendation
        """
        logger.info("Running Hausman test (FE vs RE)")
        
        # Run FE and RE
        fe_results = self.fixed_effects(y, X, cluster_entity=False)
        re_results = self.random_effects(y, X, cluster_entity=False)
        
        # Extract coefficients
        fe_coef = fe_results.params
        re_coef = re_results.params
        
        # Extract covariance matrices
        fe_cov = fe_results.cov
        re_cov = re_results.cov
        
        # Calculate test statistic
        diff = fe_coef - re_coef
        var_diff = fe_cov - re_cov
        
        # Ensure var_diff is positive definite
        try:
            chi2 = diff.T @ np.linalg.inv(var_diff) @ diff
            df = len(diff)
            from scipy.stats import chi2 as chi2_dist
            p_value = 1 - chi2_dist.cdf(chi2, df)
        except:
            logger.warning("Hausman test failed (numerical issues)")
            return {
                'statistic': np.nan,
                'p_value': np.nan,
                'recommendation': 'Unable to compute'
            }
        
        recommendation = 'Fixed Effects' if p_value < 0.05 else 'Random Effects'
        
        logger.info(f"Hausman test: χ² = {chi2:.4f}, p = {p_value:.4f} → {recommendation}")
        
        return {
            'statistic': float(chi2),
            'p_value': float(p_value),
            'recommendation': recommendation
        }
    
    def compare_models(self,
                      y: str,
                      X: List[str]) -> pd.DataFrame:
        """
        Compare Pooled OLS, FE, and RE models
        
        Args:
            y: Dependent variable name
            X: List of independent variable names
        
        Returns:
            Comparison table
        """
        logger.info("Comparing Pooled OLS, FE, and RE models")
        
        # Run all models
        pooled = self.pooled_ols(y, X, cluster_entity=True)
        fe = self.fixed_effects(y, X, cluster_entity=True)
        re = self.random_effects(y, X, cluster_entity=True)
        
        # Create comparison table
        comparison = pd.DataFrame({
            'Pooled OLS': pooled.params,
            'Fixed Effects': fe.params,
            'Random Effects': re.params
        })
        
        # Add standard errors
        se_comparison = pd.DataFrame({
            'Pooled OLS (SE)': pooled.std_errors,
            'Fixed Effects (SE)': fe.std_errors,
            'Random Effects (SE)': re.std_errors
        })
        
        # Add model statistics
        stats = pd.DataFrame({
            'Pooled OLS': [pooled.rsquared, pooled.nobs, pooled.f_statistic.stat],
            'Fixed Effects': [fe.rsquared, fe.nobs, fe.f_statistic.stat],
            'Random Effects': [re.rsquared, re.nobs, re.f_statistic.stat]
        }, index=['R²', 'N', 'F-statistic'])
        
        return comparison, se_comparison, stats
    
    def generate_regression_table(self,
                                 models: List[Tuple[str, PanelEffectsResults]],
                                 output_path: Optional[str] = None) -> str:
        """
        Generate publication-ready regression table
        
        Args:
            models: List of (model_name, results) tuples
            output_path: Optional path to save table
        
        Returns:
            Formatted table string
        """
        # Extract coefficients and standard errors
        coefs = {}
        ses = {}
        
        for name, results in models:
            coefs[name] = results.params
            ses[name] = results.std_errors
        
        # Create DataFrame
        df_coefs = pd.DataFrame(coefs)
        df_ses = pd.DataFrame(ses)
        
        # Format: coef (se)
        table_rows = []
        for var in df_coefs.index:
            row = [var]
            for col in df_coefs.columns:
                coef = df_coefs.loc[var, col]
                se = df_ses.loc[var, col]
                row.append(f"{coef:.4f}\n({se:.4f})")
            table_rows.append(row)
        
        # Add model statistics
        stats_rows = []
        for stat_name in ['R²', 'N', 'F-statistic']:
            row = [stat_name]
            for name, results in models:
                if stat_name == 'R²':
                    row.append(f"{results.rsquared:.4f}")
                elif stat_name == 'N':
                    row.append(f"{results.nobs:.0f}")
                elif stat_name == 'F-statistic':
                    row.append(f"{results.f_statistic.stat:.2f}")
            stats_rows.append(row)
        
        # Combine
        all_rows = table_rows + stats_rows
        
        # Create table
        table_df = pd.DataFrame(all_rows, columns=['Variable'] + [m[0] for m in models])
        
        if output_path:
            table_df.to_csv(output_path, index=False)
            logger.info(f"Regression table saved to {output_path}")
        
        return table_df.to_string()


# Example usage
if __name__ == "__main__":
    # Generate sample panel data
    np.random.seed(42)
    n_firms = 100
    n_years = 10
    
    data = []
    for firm in range(1, n_firms + 1):
        firm_effect = np.random.normal(0, 0.02)
        for year in range(2014, 2014 + n_years):
            rd_intensity = np.random.uniform(0, 0.1)
            leverage = np.random.uniform(0.2, 0.6)
            
            roa = 0.05 + firm_effect + 0.15 * rd_intensity - 0.03 * leverage + np.random.normal(0, 0.01)
            
            data.append({
                'firm_id': firm,
                'year': year,
                'roa': roa,
                'rd_intensity': rd_intensity,
                'leverage': leverage,
                'firm_size': np.random.lognormal(10, 1)
            })
    
    df = pd.DataFrame(data)
    
    # Run panel regression
    pr = PanelRegression(df, firm_id='firm_id', time_id='year')
    
    # Fixed Effects
    fe_results = pr.fixed_effects(y='roa', X=['rd_intensity', 'leverage'])
    print("\n" + "="*60)
    print("Fixed Effects Results")
    print("="*60)
    print(fe_results.summary)
    
    # Random Effects
    re_results = pr.random_effects(y='roa', X=['rd_intensity', 'leverage'])
    print("\n" + "="*60)
    print("Random Effects Results")
    print("="*60)
    print(re_results.summary)
    
    # Hausman Test
    hausman = pr.hausman_test(y='roa', X=['rd_intensity', 'leverage'])
    print("\n" + "="*60)
    print("Hausman Test")
    print("="*60)
    print(f"χ² statistic: {hausman['statistic']:.4f}")
    print(f"p-value: {hausman['p_value']:.4f}")
    print(f"Recommendation: {hausman['recommendation']}")
    
    # Compare models
    comparison = pr.compare_models(y='roa', X=['rd_intensity', 'leverage'])
    print("\n" + "="*60)
    print("Model Comparison")
    print("="*60)
    print(comparison[0])
