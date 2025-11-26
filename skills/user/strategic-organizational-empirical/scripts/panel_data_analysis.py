#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panel Data Analysis: Fixed Effects and Random Effects Models

Philosophical/Theoretical Foundation:
    Panel data analysis addresses the fundamental problem of unobserved
    heterogeneity - firm-specific factors that are correlated with both
    independent and dependent variables (Wooldridge, 2010). In strategy
    research, such factors include organizational culture, managerial quality,
    and historical path dependencies.
    
    Two principal approaches exist:
    
    1. Fixed Effects (FE): Controls for all time-invariant unobserved factors
       by effectively differencing them out. Assumes strict exogeneity.
       Answers: "Within-firm, does X cause Y?"
       
    2. Random Effects (RE): Models unobserved heterogeneity as random variation.
       More efficient but requires uncorrelated individual effects (strong assumption).
       Answers: "Across and within firms, does X cause Y?"
    
    The Hausman test adjudicates between FE and RE by testing whether
    individual effects are correlated with regressors (Hausman, 1978).

Theoretical Applications:
    - RBV: Resource accumulation over time
    - Dynamic Capabilities: Capability evolution and persistence
    - Institutional Theory: Temporal patterns of isomorphism
    - TCE: Governance choice adaptation

Usage:
    python panel_data_analysis.py --data panel_data.csv --entity firm_id --time year --dv performance --iv resources
    python panel_data_analysis.py --data panel_data.csv --config framework_config.yaml

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
Date: 2025-11-08
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Panel data models
from linearmodels import PanelOLS, RandomEffects
from linearmodels.panel import compare
import statsmodels.api as sm
from scipy import stats


@dataclass
class PanelResults:
    """Container for panel analysis results"""
    model_type: str
    dependent_var: str
    independent_vars: List[str]
    n_entities: int
    n_time_periods: int
    n_observations: int
    
    # Model estimates
    coefficients: Dict[str, float]
    std_errors: Dict[str, float]
    t_statistics: Dict[str, float]
    p_values: Dict[str, float]
    
    # Model fit
    r_squared_overall: float
    r_squared_within: float
    r_squared_between: float
    f_statistic: float
    f_pvalue: float
    
    # Additional results
    hausman_test: Optional[Dict[str, Any]] = None
    entity_effects: Optional[Dict[str, float]] = None
    time_effects: Optional[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'model_type': self.model_type,
            'dependent_var': self.dependent_var,
            'independent_vars': self.independent_vars,
            'n_entities': self.n_entities,
            'n_time_periods': self.n_time_periods,
            'n_observations': self.n_observations,
            'coefficients': self.coefficients,
            'std_errors': self.std_errors,
            't_statistics': self.t_statistics,
            'p_values': self.p_values,
            'r_squared_overall': self.r_squared_overall,
            'r_squared_within': self.r_squared_within,
            'r_squared_between': self.r_squared_between,
            'f_statistic': self.f_statistic,
            'f_pvalue': self.f_pvalue,
            'hausman_test': self.hausman_test,
            'entity_effects_summary': self._summarize_effects(self.entity_effects) if self.entity_effects else None,
            'time_effects_summary': self._summarize_effects(self.time_effects) if self.time_effects else None
        }
    
    def _summarize_effects(self, effects: Dict[str, float]) -> Dict[str, Any]:
        """Summarize fixed effects"""
        if not effects:
            return None
        values = list(effects.values())
        return {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values)),
            'n_effects': len(effects)
        }


class PanelDataAnalyzer:
    """
    Panel Data Analysis System
    
    Implements fixed effects, random effects, and related panel data methods
    for longitudinal strategic research.
    """
    
    def __init__(self, data: pd.DataFrame, entity_col: str, time_col: str,
                 output_dir: str = './panel_results'):
        """
        Initialize panel analyzer
        
        Args:
            data: DataFrame with panel structure
            entity_col: Column identifying entities (e.g., firm_id)
            time_col: Column identifying time periods (e.g., year)
            output_dir: Directory for output files
        """
        self.data = data.copy()
        self.entity_col = entity_col
        self.time_col = time_col
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Validate panel structure
        self._validate_panel_structure()
        
        # Set multi-index for panel analysis
        self.data_panel = self.data.set_index([entity_col, time_col])
        
        self.results: Dict[str, PanelResults] = {}
    
    def _validate_panel_structure(self) -> None:
        """Validate that data has proper panel structure"""
        # Check for required columns
        if self.entity_col not in self.data.columns:
            raise ValueError(f"Entity column '{self.entity_col}' not found")
        if self.time_col not in self.data.columns:
            raise ValueError(f"Time column '{self.time_col}' not found")
        
        # Count entities and time periods
        self.n_entities = self.data[self.entity_col].nunique()
        self.n_time_periods = self.data[self.time_col].nunique()
        
        print(f"\nPanel structure:")
        print(f"  Entities: {self.n_entities}")
        print(f"  Time periods: {self.n_time_periods}")
        print(f"  Observations: {len(self.data)}")
        
        # Check balance
        counts = self.data.groupby(self.entity_col)[self.time_col].count()
        if counts.std() == 0:
            print("  Panel: Balanced")
        else:
            print(f"  Panel: Unbalanced (obs per entity: {counts.min()}-{counts.max()})")
    
    def estimate_pooled_ols(self, dv: str, ivs: List[str]) -> PanelResults:
        """
        Estimate pooled OLS (baseline model ignoring panel structure)
        
        This serves as a benchmark to show the bias from ignoring unobserved
        heterogeneity.
        
        Args:
            dv: Dependent variable
            ivs: List of independent variables
            
        Returns:
            PanelResults object
        """
        print(f"\nEstimating Pooled OLS...")
        
        # Prepare data
        vars_needed = [dv] + ivs + [self.entity_col, self.time_col]
        data_clean = self.data[vars_needed].dropna()
        
        # Set panel index
        data_indexed = data_clean.set_index([self.entity_col, self.time_col])
        
        # Estimate model
        exog = sm.add_constant(data_indexed[ivs])
        model = sm.OLS(data_indexed[dv], exog).fit()
        
        # Extract results
        coefficients = {var: float(model.params[var]) for var in ivs}
        std_errors = {var: float(model.bse[var]) for var in ivs}
        t_statistics = {var: float(model.tvalues[var]) for var in ivs}
        p_values = {var: float(model.pvalues[var]) for var in ivs}
        
        results = PanelResults(
            model_type="Pooled OLS",
            dependent_var=dv,
            independent_vars=ivs,
            n_entities=data_clean[self.entity_col].nunique(),
            n_time_periods=data_clean[self.time_col].nunique(),
            n_observations=len(data_clean),
            coefficients=coefficients,
            std_errors=std_errors,
            t_statistics=t_statistics,
            p_values=p_values,
            r_squared_overall=model.rsquared,
            r_squared_within=0.0,
            r_squared_between=0.0,
            f_statistic=model.fvalue,
            f_pvalue=model.f_pvalue
        )
        
        self.results['pooled_ols'] = results
        return results
    
    def estimate_fixed_effects(self, dv: str, ivs: List[str],
                               time_effects: bool = False,
                               cluster_entity: bool = True) -> PanelResults:
        """
        Estimate fixed effects model
        
        FE eliminates time-invariant unobserved heterogeneity by within-
        transformation (demeaning at entity level).
        
        Args:
            dv: Dependent variable
            ivs: List of independent variables
            time_effects: Include time fixed effects
            cluster_entity: Use entity-clustered standard errors
            
        Returns:
            PanelResults object
        """
        print(f"\nEstimating Fixed Effects model...")
        
        # Prepare data
        vars_needed = [dv] + ivs
        data_clean = self.data_panel[vars_needed].dropna()
        
        # Estimate FE model
        exog = data_clean[ivs]
        endog = data_clean[dv]
        
        model = PanelOLS(endog, exog, entity_effects=True, time_effects=time_effects)
        
        if cluster_entity:
            results_fit = model.fit(cov_type='clustered', cluster_entity=True)
        else:
            results_fit = model.fit()
        
        # Extract results
        coefficients = {var: float(results_fit.params[var]) for var in ivs}
        std_errors = {var: float(results_fit.std_errors[var]) for var in ivs}
        t_statistics = {var: float(results_fit.tstats[var]) for var in ivs}
        p_values = {var: float(results_fit.pvalues[var]) for var in ivs}
        
        # Extract entity effects if available
        entity_effects = None
        if hasattr(results_fit, 'estimated_effects'):
            entity_effects = results_fit.estimated_effects.to_dict()
        
        results = PanelResults(
            model_type="Fixed Effects",
            dependent_var=dv,
            independent_vars=ivs,
            n_entities=data_clean.index.get_level_values(0).nunique(),
            n_time_periods=data_clean.index.get_level_values(1).nunique(),
            n_observations=len(data_clean),
            coefficients=coefficients,
            std_errors=std_errors,
            t_statistics=t_statistics,
            p_values=p_values,
            r_squared_overall=results_fit.rsquared_overall,
            r_squared_within=results_fit.rsquared_within,
            r_squared_between=results_fit.rsquared_between,
            f_statistic=results_fit.f_statistic.stat,
            f_pvalue=results_fit.f_statistic.pval,
            entity_effects=entity_effects
        )
        
        self.results['fixed_effects'] = results
        return results
    
    def estimate_random_effects(self, dv: str, ivs: List[str]) -> PanelResults:
        """
        Estimate random effects model
        
        RE models unobserved heterogeneity as random draws from a distribution.
        More efficient than FE but requires strict exogeneity.
        
        Args:
            dv: Dependent variable
            ivs: List of independent variables
            
        Returns:
            PanelResults object
        """
        print(f"\nEstimating Random Effects model...")
        
        # Prepare data
        vars_needed = [dv] + ivs
        data_clean = self.data_panel[vars_needed].dropna()
        
        # Estimate RE model
        exog = data_clean[ivs]
        endog = data_clean[dv]
        
        model = RandomEffects(endog, exog)
        results_fit = model.fit()
        
        # Extract results
        coefficients = {var: float(results_fit.params[var]) for var in ivs}
        std_errors = {var: float(results_fit.std_errors[var]) for var in ivs}
        t_statistics = {var: float(results_fit.tstats[var]) for var in ivs}
        p_values = {var: float(results_fit.pvalues[var]) for var in ivs}
        
        results = PanelResults(
            model_type="Random Effects",
            dependent_var=dv,
            independent_vars=ivs,
            n_entities=data_clean.index.get_level_values(0).nunique(),
            n_time_periods=data_clean.index.get_level_values(1).nunique(),
            n_observations=len(data_clean),
            coefficients=coefficients,
            std_errors=std_errors,
            t_statistics=t_statistics,
            p_values=p_values,
            r_squared_overall=results_fit.rsquared_overall,
            r_squared_within=results_fit.rsquared_within,
            r_squared_between=results_fit.rsquared_between,
            f_statistic=results_fit.f_statistic.stat,
            f_pvalue=results_fit.f_statistic.pval
        )
        
        self.results['random_effects'] = results
        return results
    
    def hausman_test(self) -> Dict[str, Any]:
        """
        Conduct Hausman specification test
        
        H0: RE is consistent and efficient (preferred)
        H1: FE is consistent, RE is inconsistent (use FE)
        
        Returns:
            Dictionary with test results
        """
        if 'fixed_effects' not in self.results or 'random_effects' not in self.results:
            raise ValueError("Must estimate both FE and RE models before Hausman test")
        
        print(f"\nConducting Hausman specification test...")
        
        fe_results = self.results['fixed_effects']
        re_results = self.results['random_effects']
        
        # Extract coefficients
        vars_common = set(fe_results.coefficients.keys()) & set(re_results.coefficients.keys())
        
        b_fe = np.array([fe_results.coefficients[v] for v in vars_common])
        b_re = np.array([re_results.coefficients[v] for v in vars_common])
        
        # Difference in coefficients
        b_diff = b_fe - b_re
        
        # Variance of difference (approximation)
        var_fe = np.array([fe_results.std_errors[v]**2 for v in vars_common])
        var_re = np.array([re_results.std_errors[v]**2 for v in vars_common])
        var_diff = var_fe - var_re
        
        # Handle negative variances (can occur with small samples)
        var_diff = np.abs(var_diff)
        
        # Hausman statistic
        if len(b_diff) > 0 and np.all(var_diff > 0):
            H = np.sum((b_diff**2) / var_diff)
            df = len(b_diff)
            p_value = 1 - stats.chi2.cdf(H, df)
            
            # Interpretation
            if p_value < 0.05:
                recommendation = "Fixed Effects"
                interpretation = (
                    f"Hausman test rejects RE (H={H:.2f}, df={df}, p={p_value:.4f}). "
                    f"Individual effects are correlated with regressors. Use Fixed Effects "
                    f"to avoid inconsistent estimates (Wooldridge, 2010)."
                )
            else:
                recommendation = "Random Effects"
                interpretation = (
                    f"Hausman test fails to reject RE (H={H:.2f}, df={df}, p={p_value:.4f}). "
                    f"Random Effects is consistent and more efficient. Preferred specification "
                    f"under the assumption of uncorrelated individual effects."
                )
        else:
            H, df, p_value = 0, 0, 1
            recommendation = "Fixed Effects (default)"
            interpretation = "Hausman test could not be computed. Default to Fixed Effects for robustness."
        
        hausman_results = {
            'statistic': float(H),
            'df': int(df),
            'p_value': float(p_value),
            'recommendation': recommendation,
            'interpretation': interpretation
        }
        
        # Add to both model results
        if 'fixed_effects' in self.results:
            self.results['fixed_effects'].hausman_test = hausman_results
        if 'random_effects' in self.results:
            self.results['random_effects'].hausman_test = hausman_results
        
        return hausman_results
    
    def compare_models(self) -> None:
        """Generate comparison table of all estimated models"""
        print("\n" + "="*80)
        print("MODEL COMPARISON")
        print("="*80)
        
        if not self.results:
            print("No models estimated yet.")
            return
        
        # Create comparison table
        comparison_data = []
        
        for model_name, result in self.results.items():
            row = {
                'Model': result.model_type,
                'N': result.n_observations,
                'R² (overall)': f"{result.r_squared_overall:.4f}",
                'R² (within)': f"{result.r_squared_within:.4f}",
                'R² (between)': f"{result.r_squared_between:.4f}",
                'F-stat': f"{result.f_statistic:.2f}",
                'p-value': f"{result.f_pvalue:.4f}"
            }
            comparison_data.append(row)
        
        comparison_df = pd.DataFrame(comparison_data)
        print("\n", comparison_df.to_string(index=False))
        
        # Show Hausman test if available
        if 'fixed_effects' in self.results and self.results['fixed_effects'].hausman_test:
            print("\n" + "-"*80)
            print("HAUSMAN TEST")
            print("-"*80)
            hausman = self.results['fixed_effects'].hausman_test
            print(f"Statistic: {hausman['statistic']:.2f}")
            print(f"p-value: {hausman['p_value']:.4f}")
            print(f"Recommendation: {hausman['recommendation']}")
            print(f"\n{hausman['interpretation']}")
    
    def save_results(self, output_path: str = 'panel_results.json') -> None:
        """Save all results to JSON"""
        results_path = self.output_dir / output_path
        
        results_dict = {
            'timestamp': datetime.now().isoformat(),
            'panel_structure': {
                'entity_col': self.entity_col,
                'time_col': self.time_col,
                'n_entities': self.n_entities,
                'n_time_periods': self.n_time_periods
            },
            'models': {name: result.to_dict() for name, result in self.results.items()}
        }
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Results saved to: {results_path.absolute()}")


def load_config(config_path: str) -> Optional[Dict[str, Any]]:
    """Load configuration"""
    if not config_path:
        return None
    
    config_file = Path(config_path)
    if not config_file.exists():
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        if config_file.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(f)
        elif config_file.suffix == '.json':
            return json.load(f)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Panel Data Analysis: Fixed and Random Effects',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data', type=str, required=True, help='Path to panel dataset (CSV)')
    parser.add_argument('--entity', type=str, required=True, help='Entity identifier column (e.g., firm_id)')
    parser.add_argument('--time', type=str, required=True, help='Time identifier column (e.g., year)')
    parser.add_argument('--dv', type=str, required=True, help='Dependent variable')
    parser.add_argument('--iv', type=str, nargs='+', required=True, help='Independent variable(s)')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--time-effects', action='store_true', help='Include time fixed effects')
    parser.add_argument('--output-dir', type=str, default='./panel_results', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading panel dataset: {args.data}")
        data = pd.read_csv(args.data)
        print(f"✓ Loaded: {len(data)} observations")
        
        # Create analyzer
        analyzer = PanelDataAnalyzer(data, entity_col=args.entity, time_col=args.time,
                                     output_dir=args.output_dir)
        
        # Estimate models
        analyzer.estimate_pooled_ols(args.dv, args.iv)
        analyzer.estimate_fixed_effects(args.dv, args.iv, time_effects=args.time_effects)
        analyzer.estimate_random_effects(args.dv, args.iv)
        
        # Hausman test
        hausman_results = analyzer.hausman_test()
        
        # Compare models
        analyzer.compare_models()
        
        # Save results
        analyzer.save_results()
        
        print("\n" + "="*80)
        print("✓ Panel data analysis complete!")
        print("="*80)
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
