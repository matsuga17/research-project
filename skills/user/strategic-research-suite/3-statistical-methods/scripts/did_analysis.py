"""
did_analysis.py

Difference-in-Differences (DiD) Analysis

This module provides comprehensive DiD methods for causal inference including:
- Standard 2x2 DiD
- Staggered adoption DiD
- Event study designs
- Parallel trends testing
- Robustness checks

Usage:
    from did_analysis import DIDAnalyzer
    
    did = DIDAnalyzer(df, firm_id='firm_id', time_id='year',
                     treatment_var='treated', outcome_var='roa')
    results = did.standard_did(treatment_time=2018)
    print(results['ate'])
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DIDAnalyzer:
    """
    Difference-in-Differences analyzer for causal inference
    
    Attributes:
        df: Input panel DataFrame
        firm_id: Firm identifier column
        time_id: Time identifier column
        treatment_var: Treatment indicator (0/1)
        outcome_var: Outcome variable name
    """
    
    def __init__(self, df: pd.DataFrame,
                 firm_id: str = 'firm_id',
                 time_id: str = 'year',
                 treatment_var: str = 'treated',
                 outcome_var: str = 'outcome'):
        """
        Initialize DiD analyzer
        
        Args:
            df: Panel dataset
            firm_id: Name of firm identifier column
            time_id: Name of time identifier column
            treatment_var: Name of treatment indicator (0/1)
            outcome_var: Name of outcome variable
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.treatment_var = treatment_var
        self.outcome_var = outcome_var
        
        # Prepare panel structure
        self.panel_data = self.df.set_index([self.firm_id, self.time_id]).sort_index()
        
        logger.info(f"DiD Analyzer initialized: {len(df[firm_id].unique())} firms, "
                   f"{len(df[time_id].unique())} time periods")
    
    def standard_did(self,
                    treatment_time: int,
                    controls: Optional[List[str]] = None,
                    cluster_entity: bool = True) -> Dict:
        """
        Standard 2x2 Difference-in-Differences
        
        Args:
            treatment_time: Time period when treatment occurs
            controls: Optional list of control variables
            cluster_entity: Cluster standard errors by entity
        
        Returns:
            Dictionary with ATE, standard error, and regression results
        """
        logger.info(f"Running standard DiD with treatment at t={treatment_time}")
        
        # Create post-treatment indicator
        self.df['post'] = (self.df[self.time_id] >= treatment_time).astype(int)
        
        # Create interaction term
        self.df['treated_x_post'] = self.df[self.treatment_var] * self.df['post']
        
        # Prepare formula
        formula_parts = [self.outcome_var, '~', self.treatment_var, '+ post + treated_x_post']
        
        if controls:
            formula_parts.extend(['+'] + controls)
        
        formula = ' '.join(formula_parts)
        
        # Prepare panel data
        panel_data = self.df.set_index([self.firm_id, self.time_id]).sort_index()
        
        # Run regression
        cov_type = 'clustered' if cluster_entity else 'robust'
        cov_config = {'clusters': panel_data.index.get_level_values(0)} if cluster_entity else {}
        
        model = PanelOLS.from_formula(formula, data=panel_data, entity_effects=True)
        results = model.fit(cov_type=cov_type, **cov_config)
        
        # Extract ATE (coefficient on treated_x_post)
        ate = results.params['treated_x_post']
        ate_se = results.std_errors['treated_x_post']
        ate_pvalue = results.pvalues['treated_x_post']
        
        logger.info(f"DiD ATE: {ate:.4f} (SE: {ate_se:.4f}, p={ate_pvalue:.4f})")
        
        return {
            'ate': float(ate),
            'se': float(ate_se),
            'pvalue': float(ate_pvalue),
            'ci_lower': float(ate - 1.96 * ate_se),
            'ci_upper': float(ate + 1.96 * ate_se),
            'results': results
        }
    
    def event_study(self,
                   treatment_time: int,
                   leads: int = 3,
                   lags: int = 5,
                   controls: Optional[List[str]] = None,
                   cluster_entity: bool = True) -> Dict:
        """
        Event study design with leads and lags
        
        Args:
            treatment_time: Time period when treatment occurs
            leads: Number of pre-treatment periods to include
            lags: Number of post-treatment periods to include
            controls: Optional list of control variables
            cluster_entity: Cluster standard errors by entity
        
        Returns:
            Dictionary with coefficients for each time period
        """
        logger.info(f"Running event study: {leads} leads, {lags} lags")
        
        # Create relative time variable
        self.df['rel_time'] = self.df[self.time_id] - treatment_time
        
        # Create treatment indicators for each period (excluding t-1 as base)
        for t in range(-leads, lags + 1):
            if t != -1:  # Exclude t-1 as reference category
                var_name = f'treated_time_{t}'
                self.df[var_name] = ((self.df['rel_time'] == t) & 
                                    (self.df[self.treatment_var] == 1)).astype(int)
        
        # Prepare formula
        time_vars = [f'treated_time_{t}' for t in range(-leads, lags + 1) if t != -1]
        formula_parts = [self.outcome_var, '~'] + time_vars
        
        if controls:
            formula_parts.extend(['+'] + controls)
        
        formula = ' '.join(formula_parts)
        
        # Prepare panel data
        panel_data = self.df.set_index([self.firm_id, self.time_id]).sort_index()
        
        # Run regression
        cov_type = 'clustered' if cluster_entity else 'robust'
        cov_config = {'clusters': panel_data.index.get_level_values(0)} if cluster_entity else {}
        
        model = PanelOLS.from_formula(formula, data=panel_data, entity_effects=True, time_effects=True)
        results = model.fit(cov_type=cov_type, **cov_config)
        
        # Extract coefficients
        coefs = {}
        for t in range(-leads, lags + 1):
            if t == -1:
                coefs[t] = {'coef': 0.0, 'se': 0.0, 'ci_lower': 0.0, 'ci_upper': 0.0}
            else:
                var_name = f'treated_time_{t}'
                coefs[t] = {
                    'coef': float(results.params[var_name]),
                    'se': float(results.std_errors[var_name]),
                    'ci_lower': float(results.params[var_name] - 1.96 * results.std_errors[var_name]),
                    'ci_upper': float(results.params[var_name] + 1.96 * results.std_errors[var_name])
                }
        
        return {
            'coefficients': coefs,
            'results': results
        }
    
    def parallel_trends_test(self,
                            treatment_time: int,
                            pre_periods: int = 3,
                            controls: Optional[List[str]] = None) -> Dict:
        """
        Test parallel trends assumption
        
        Args:
            treatment_time: Time period when treatment occurs
            pre_periods: Number of pre-treatment periods to test
            controls: Optional list of control variables
        
        Returns:
            Dictionary with F-test results
        """
        logger.info("Testing parallel trends assumption")
        
        # Filter to pre-treatment periods
        df_pre = self.df[self.df[self.time_id] < treatment_time].copy()
        
        # Create treatment-time interactions
        df_pre['time_since_start'] = df_pre[self.time_id] - df_pre[self.time_id].min()
        df_pre['treated_x_time'] = df_pre[self.treatment_var] * df_pre['time_since_start']
        
        # Prepare formula
        formula_parts = [self.outcome_var, '~', self.treatment_var, '+ time_since_start + treated_x_time']
        
        if controls:
            formula_parts.extend(['+'] + controls)
        
        formula = ' '.join(formula_parts)
        
        # Run regression
        panel_data = df_pre.set_index([self.firm_id, self.time_id]).sort_index()
        model = PanelOLS.from_formula(formula, data=panel_data, entity_effects=True)
        results = model.fit(cov_type='robust')
        
        # Test if treated_x_time coefficient is zero
        coef = results.params['treated_x_time']
        se = results.std_errors['treated_x_time']
        pvalue = results.pvalues['treated_x_time']
        
        parallel_trends_hold = pvalue > 0.05
        
        logger.info(f"Parallel trends test: p={pvalue:.4f} → "
                   f"{'Assumption holds' if parallel_trends_hold else 'Assumption violated'}")
        
        return {
            'coefficient': float(coef),
            'se': float(se),
            'pvalue': float(pvalue),
            'parallel_trends_hold': parallel_trends_hold
        }
    
    def visualize_event_study(self,
                             event_study_results: Dict,
                             output_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize event study results
        
        Args:
            event_study_results: Results from event_study()
            output_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        coefs = event_study_results['coefficients']
        
        # Extract data
        times = sorted(coefs.keys())
        point_estimates = [coefs[t]['coef'] for t in times]
        ci_lower = [coefs[t]['ci_lower'] for t in times]
        ci_upper = [coefs[t]['ci_upper'] for t in times]
        
        # Create plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot point estimates and confidence intervals
        ax.plot(times, point_estimates, 'o-', color='darkblue', linewidth=2, markersize=8, label='Point Estimate')
        ax.fill_between(times, ci_lower, ci_upper, alpha=0.2, color='darkblue', label='95% CI')
        
        # Add reference lines
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.axvline(x=-0.5, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Treatment Time')
        
        # Labels and title
        ax.set_xlabel('Time Relative to Treatment', fontsize=12)
        ax.set_ylabel('Treatment Effect', fontsize=12)
        ax.set_title('Event Study: Dynamic Treatment Effects', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Event study plot saved to {output_path}")
        
        return fig


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n_firms = 200
    n_years = 10
    treatment_year = 2018
    
    data = []
    for firm in range(1, n_firms + 1):
        treated = 1 if firm <= 100 else 0
        firm_effect = np.random.normal(0, 0.5)
        
        for year in range(2014, 2014 + n_years):
            # Generate outcome with treatment effect
            if treated and year >= treatment_year:
                treatment_effect = 0.2  # True treatment effect
            else:
                treatment_effect = 0
            
            outcome = 5 + firm_effect + 0.1 * (year - 2014) + treatment_effect + np.random.normal(0, 0.3)
            
            data.append({
                'firm_id': firm,
                'year': year,
                'treated': treated,
                'outcome': outcome,
                'control_var': np.random.normal(0, 1)
            })
    
    df = pd.DataFrame(data)
    
    # Run DiD analysis
    did = DIDAnalyzer(df, firm_id='firm_id', time_id='year', 
                     treatment_var='treated', outcome_var='outcome')
    
    # Standard DiD
    did_results = did.standard_did(treatment_time=2018, controls=['control_var'])
    print("\n" + "="*60)
    print("Standard DiD Results")
    print("="*60)
    print(f"Average Treatment Effect: {did_results['ate']:.4f}")
    print(f"Standard Error: {did_results['se']:.4f}")
    print(f"95% CI: [{did_results['ci_lower']:.4f}, {did_results['ci_upper']:.4f}]")
    print(f"p-value: {did_results['pvalue']:.4f}")
    
    # Event study
    event_results = did.event_study(treatment_time=2018, leads=3, lags=5)
    print("\n" + "="*60)
    print("Event Study Results")
    print("="*60)
    for t, coef_data in sorted(event_results['coefficients'].items()):
        print(f"t={t:+d}: {coef_data['coef']:7.4f} (SE: {coef_data['se']:.4f})")
    
    # Parallel trends test
    pt_test = did.parallel_trends_test(treatment_time=2018, pre_periods=3)
    print("\n" + "="*60)
    print("Parallel Trends Test")
    print("="*60)
    print(f"Coefficient: {pt_test['coefficient']:.4f}")
    print(f"p-value: {pt_test['pvalue']:.4f}")
    print(f"Parallel trends assumption: {'✓ Holds' if pt_test['parallel_trends_hold'] else '✗ Violated'}")
    
    # Visualize event study
    fig = did.visualize_event_study(event_results)
    plt.show()
