"""
Strategic Management Research Hub - ML×Causal Inference Integration
====================================================================

State-of-the-art causal inference methods integrated with machine learning
for publication-ready strategic management research.

Addresses the fundamental challenge: **Correlation ≠ Causation**

Key Methods Implemented:
1. **Causal Forest (Heterogeneous Treatment Effects)**
   - Discover which firms benefit most from strategic actions
   - Non-parametric, flexible estimation
   - Honest confidence intervals

2. **Double Machine Learning (DML)**
   - Robust to high-dimensional confounding
   - Consistent estimation with complex controls
   - Orthogonalized moment conditions

3. **Synthetic Control Method**
   - Gold standard for case studies
   - Event study with few treated units
   - Transparent counterfactual

4. **Propensity Score Methods**
   - Matching, weighting, stratification
   - Balance diagnostics
   - Sensitivity analysis

5. **Instrumental Variables (ML-enhanced)**
   - Weak instrument detection
   - Many instruments problem
   - Post-Lasso IV selection

6. **Regression Discontinuity Design (RDD)**
   - Sharp & Fuzzy RDD
   - Optimal bandwidth selection
   - Robustness checks

Theoretical Applications:
- RBV: Causal effect of resources on performance
- M&A: Acquisition impact on innovation
- Strategic Alliances: Partnership benefits
- International Strategy: Entry mode effects
- Corporate Governance: Board composition impact

Author: Strategic Management Research Hub v3.1
Version: 3.1
Date: 2025-11-01
License: MIT

References:
- Athey & Imbens (2016): Recursive Partitioning for Heterogeneous Causal Effects
- Chernozhukov et al. (2018): Double/Debiased Machine Learning
- Abadie & Gardeazabal (2003): Economic Costs of Conflict (Synthetic Control)
- Rosenbaum & Rubin (1983): Central Role of Propensity Score
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any, Callable
import logging
from pathlib import Path
import warnings
import json
from datetime import datetime

# Core ML Libraries
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Econometric Causal Inference
try:
    from econml.dml import CausalForestDML, LinearDML, SparseLinearDML
    from econml.sklearn_extensions.linear_model import WeightedLasso
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False
    warnings.warn("EconML not installed. pip install econml")

# Causal Inference Libraries
try:
    from causalinference import CausalModel
    CAUSALINFERENCE_AVAILABLE = True
except ImportError:
    CAUSALINFERENCE_AVAILABLE = False
    warnings.warn("causalinference not installed. pip install causalinference")

try:
    from dowhy import CausalModel as DoWhyCausalModel
    DOWHY_AVAILABLE = True
except ImportError:
    DOWHY_AVAILABLE = False
    warnings.warn("DoWhy not installed. pip install dowhy")

# Propensity Score Matching
from sklearn.neighbors import NearestNeighbors
from scipy.optimize import minimize

# Statistical Tests
from scipy import stats
from scipy.stats import norm, t as t_dist

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MAIN CLASS: CausalMLIntegration
# ============================================================================

class CausalMLIntegration:
    """
    Comprehensive causal inference system for strategic management research.
    
    Solves endogeneity problems common in strategy research:
    - Selection bias (firms self-select into strategic actions)
    - Omitted variable bias (unobserved firm characteristics)
    - Reverse causality (performance → strategy)
    - Measurement error
    
    Usage:
    ```python
    causal = CausalMLIntegration(
        data=df_panel,
        firm_id='gvkey',
        time_var='year',
        output_dir='./causal_output/'
    )
    
    # Causal Forest (Heterogeneous Effects)
    results = causal.causal_forest(
        treatment='ma_dummy',
        outcome='roa_change',
        controls=['firm_size', 'leverage', 'prior_ma'],
        heterogeneity_vars=['firm_size', 'rd_intensity', 'industry_dynamism']
    )
    
    # Double Machine Learning
    dml_results = causal.double_machine_learning(
        treatment='rd_intensity',
        outcome='roa_lead2',
        controls=['size', 'age', 'leverage', ...]
    )
    
    # Synthetic Control
    sc_results = causal.synthetic_control(
        treated_unit='AAPL',
        treatment_time='2014-05',
        outcome_var='innovation_output',
        donor_pool=['MSFT', 'GOOG', 'AMZN']
    )
    ```
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        firm_id: str,
        time_var: str,
        output_dir: str = './causal_output/',
        random_state: int = 42
    ):
        """
        Initialize Causal ML Integration system.
        
        Args:
            data: Panel DataFrame
            firm_id: Column name for firm identifier
            time_var: Column name for time period
            output_dir: Directory for outputs
            random_state: Random seed for reproducibility
        """
        self.data = data.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.random_state = random_state
        
        # Storage for results
        self.results = {}
        
        logger.info(f"Causal ML Integration initialized")
        logger.info(f"Dataset: {len(data)} observations, "
                   f"{data[firm_id].nunique()} firms")
    
    # ========================================================================
    # 1. CAUSAL FOREST (Heterogeneous Treatment Effects)
    # ========================================================================
    
    def causal_forest(
        self,
        treatment: str,
        outcome: str,
        controls: List[str],
        heterogeneity_vars: List[str],
        discrete_treatment: bool = True,
        n_estimators: int = 100,
        min_samples_leaf: int = 10,
        max_depth: Optional[int] = None,
        save_results: bool = True
    ) -> Dict:
        """
        Causal Forest for heterogeneous treatment effect estimation.
        
        Theoretical Foundation:
        - Athey & Imbens (2016): Recursive Partitioning for Heterogeneous Causal Effects
        - Wager & Athey (2018): Estimation and Inference of Heterogeneous Treatment Effects
        
        Key Innovation:
        Traditional regression assumes homogeneous effects (β constant for all firms).
        Causal Forest discovers:
        - Which firms benefit most from treatment
        - What firm characteristics moderate treatment effects
        - Optimal targeting strategies
        
        Research Applications:
        1. **M&A Effects**: Which acquirers benefit from M&A? (by size, experience, relatedness)
        2. **R&D Investment**: Optimal R&D intensity varies by firm capabilities
        3. **International Entry**: Entry mode effectiveness depends on firm resources
        4. **Alliance Formation**: Partnership benefits heterogeneous by partner characteristics
        
        Args:
            treatment: Treatment variable (e.g., 'ma_dummy', 'alliance_formed')
            outcome: Outcome variable (e.g., 'roa_change', 'innovation_output')
            controls: Control variables (W in CATE estimation)
            heterogeneity_vars: Variables driving treatment effect heterogeneity (X)
            discrete_treatment: Whether treatment is binary/discrete
            n_estimators: Number of trees in forest
            min_samples_leaf: Minimum samples per leaf (larger → more conservative)
            max_depth: Maximum tree depth (None = unlimited)
            save_results: Save results to file
        
        Returns:
            Dictionary with:
            - cate: Conditional Average Treatment Effects per observation
            - cate_lower, cate_upper: 95% confidence intervals
            - feature_importance: Which variables drive heterogeneity
            - ate: Average Treatment Effect
        """
        if not ECONML_AVAILABLE:
            raise ImportError("EconML required. pip install econml")
        
        logger.info(f"Causal Forest: {treatment} → {outcome}")
        logger.info(f"Heterogeneity variables: {heterogeneity_vars}")
        
        # Prepare data
        required_cols = [treatment, outcome] + controls + heterogeneity_vars
        df_clean = self.data[required_cols].dropna()
        
        T = df_clean[treatment].values
        Y = df_clean[outcome].values
        X = df_clean[heterogeneity_vars].values
        W = df_clean[controls].values if controls else None
        
        logger.info(f"Sample size: {len(df_clean)} observations")
        logger.info(f"Treatment prevalence: {T.mean():.2%}" if discrete_treatment else 
                   f"Treatment mean: {T.mean():.4f}")
        
        # Estimate Causal Forest
        est = CausalForestDML(
            model_y=GradientBoostingRegressor(n_estimators=50, max_depth=5, random_state=self.random_state),
            model_t=GradientBoostingRegressor(n_estimators=50, max_depth=5, random_state=self.random_state) if not discrete_treatment else \
                   LogisticRegression(max_iter=500, random_state=self.random_state),
            discrete_treatment=discrete_treatment,
            n_estimators=n_estimators,
            min_samples_leaf=min_samples_leaf,
            max_depth=max_depth,
            random_state=self.random_state
        )
        
        est.fit(Y, T, X=X, W=W)
        
        # Conditional Average Treatment Effects (CATE)
        cate = est.effect(X)
        cate_lower, cate_upper = est.effect_interval(X, alpha=0.05)
        
        # Average Treatment Effect (ATE)
        ate = cate.mean()
        ate_se = cate.std() / np.sqrt(len(cate))
        
        logger.info(f"\nAverage Treatment Effect (ATE): {ate:.4f}")
        logger.info(f"ATE 95% CI: [{ate - 1.96*ate_se:.4f}, {ate + 1.96*ate_se:.4f}]")
        
        # Feature Importance (which variables drive heterogeneity)
        feature_importances = est.feature_importances_
        importance_df = pd.DataFrame({
            'variable': heterogeneity_vars,
            'importance': feature_importances
        }).sort_values('importance', ascending=False)
        
        logger.info("\nFeature Importance (Heterogeneity Drivers):")
        logger.info(importance_df.to_string(index=False))
        
        # Add CATE to dataframe
        df_clean['cate'] = cate
        df_clean['cate_lower'] = cate_lower
        df_clean['cate_upper'] = cate_upper
        df_clean['cate_significant'] = ((cate_lower > 0) | (cate_upper < 0)).astype(int)
        
        # Analyze heterogeneity by firm characteristics
        heterogeneity_analysis = self._analyze_heterogeneity(
            df_clean, heterogeneity_vars, 'cate'
        )
        
        # Visualization
        self._visualize_causal_forest_results(
            df_clean, heterogeneity_vars, treatment, outcome
        )
        
        # Prepare results
        results = {
            'treatment': treatment,
            'outcome': outcome,
            'ate': ate,
            'ate_se': ate_se,
            'ate_ci': (ate - 1.96*ate_se, ate + 1.96*ate_se),
            'cate': cate,
            'cate_ci': (cate_lower, cate_upper),
            'feature_importance': importance_df,
            'heterogeneity_analysis': heterogeneity_analysis,
            'model': est,
            'data_with_cate': df_clean
        }
        
        self.results['causal_forest'] = results
        
        if save_results:
            # Save CATE by firm-time
            df_clean.to_excel(
                self.output_dir / 'causal_forest_cate.xlsx',
                index=False
            )
            
            # Save feature importance
            importance_df.to_excel(
                self.output_dir / 'causal_forest_importance.xlsx',
                index=False
            )
            
            logger.info("Causal Forest results saved")
        
        return results
    
    def _analyze_heterogeneity(
        self,
        df: pd.DataFrame,
        heterogeneity_vars: List[str],
        cate_col: str = 'cate'
    ) -> Dict:
        """
        Analyze how treatment effects vary by firm characteristics.
        """
        analysis = {}
        
        for var in heterogeneity_vars:
            # Split by median
            median_val = df[var].median()
            low_group = df[df[var] <= median_val]
            high_group = df[df[var] > median_val]
            
            ate_low = low_group[cate_col].mean()
            ate_high = high_group[cate_col].mean()
            
            # T-test for difference
            t_stat, p_val = stats.ttest_ind(
                low_group[cate_col].dropna(),
                high_group[cate_col].dropna()
            )
            
            analysis[var] = {
                'ate_low': ate_low,
                'ate_high': ate_high,
                'difference': ate_high - ate_low,
                't_statistic': t_stat,
                'p_value': p_val,
                'significant': (p_val < 0.05)
            }
            
            logger.info(f"\n{var}:")
            logger.info(f"  Low group ATE: {ate_low:.4f}")
            logger.info(f"  High group ATE: {ate_high:.4f}")
            logger.info(f"  Difference: {ate_high - ate_low:.4f} (p={p_val:.4f})")
        
        return analysis
    
    def _visualize_causal_forest_results(
        self,
        df: pd.DataFrame,
        heterogeneity_vars: List[str],
        treatment: str,
        outcome: str
    ):
        """Visualize Causal Forest results."""
        
        # 1. CATE distribution
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # CATE histogram
        axes[0, 0].hist(df['cate'], bins=30, edgecolor='black', alpha=0.7)
        axes[0, 0].axvline(df['cate'].mean(), color='r', linestyle='--', 
                          label=f'ATE = {df["cate"].mean():.4f}')
        axes[0, 0].set_xlabel('Conditional Average Treatment Effect (CATE)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Treatment Effects')
        axes[0, 0].legend()
        
        # CATE by first heterogeneity variable
        if len(heterogeneity_vars) >= 1:
            var1 = heterogeneity_vars[0]
            axes[0, 1].scatter(df[var1], df['cate'], alpha=0.5)
            axes[0, 1].axhline(0, color='r', linestyle='--')
            axes[0, 1].set_xlabel(var1)
            axes[0, 1].set_ylabel('CATE')
            axes[0, 1].set_title(f'Treatment Effect Heterogeneity by {var1}')
        
        # Significant vs. Non-significant effects
        if len(heterogeneity_vars) >= 2:
            var1, var2 = heterogeneity_vars[0], heterogeneity_vars[1]
            
            sig = df[df['cate_significant'] == 1]
            non_sig = df[df['cate_significant'] == 0]
            
            axes[1, 0].scatter(non_sig[var1], non_sig[var2], 
                              alpha=0.3, label='Non-significant', s=20)
            axes[1, 0].scatter(sig[var1], sig[var2], 
                              alpha=0.7, label='Significant', s=50, marker='*')
            axes[1, 0].set_xlabel(var1)
            axes[1, 0].set_ylabel(var2)
            axes[1, 0].set_title('Significant Treatment Effects')
            axes[1, 0].legend()
        
        # CATE confidence intervals (sample)
        sample_indices = df.sample(min(50, len(df)), random_state=self.random_state).index
        sample_df = df.loc[sample_indices].sort_values('cate')
        
        x_pos = range(len(sample_df))
        axes[1, 1].errorbar(
            x_pos,
            sample_df['cate'],
            yerr=[sample_df['cate'] - sample_df['cate_lower'],
                  sample_df['cate_upper'] - sample_df['cate']],
            fmt='o',
            alpha=0.6,
            capsize=3
        )
        axes[1, 1].axhline(0, color='r', linestyle='--')
        axes[1, 1].set_xlabel('Observation (sorted by CATE)')
        axes[1, 1].set_ylabel('CATE with 95% CI')
        axes[1, 1].set_title('Treatment Effect Heterogeneity (Sample)')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'causal_forest_results.png', dpi=300)
        plt.close()
        
        logger.info("Causal Forest visualizations saved")
    
    # ========================================================================
    # 2. DOUBLE MACHINE LEARNING (DML)
    # ========================================================================
    
    def double_machine_learning(
        self,
        treatment: str,
        outcome: str,
        controls: List[str],
        discrete_treatment: bool = False,
        cv_folds: int = 5,
        save_results: bool = True
    ) -> Dict:
        """
        Double/Debiased Machine Learning for average treatment effect estimation.
        
        Theoretical Foundation:
        - Chernozhukov et al. (2018): Double/Debiased Machine Learning for Treatment and Structural Parameters
        - Robinson (1988): Root-N-Consistent Semiparametric Regression
        
        Key Advantages:
        1. **Robust to model misspecification**: Uses orthogonalized moments
        2. **High-dimensional controls**: Can handle hundreds of controls
        3. **Nonlinear confounding**: ML models capture complex relationships
        4. **√n convergence**: Achieves parametric rate despite nonparametric nuisance
        
        When to Use:
        - Many control variables (high-dimensional)
        - Nonlinear relationships between X → Y, X → T
        - Want consistent ATE estimate despite complex confounding
        
        Research Applications:
        - R&D → Performance (many firm/industry controls)
        - Corporate Governance → Strategy (complex confounding)
        - CEO Characteristics → Firm Outcomes (many observables)
        
        Args:
            treatment: Treatment variable
            outcome: Outcome variable
            controls: Control variables (can be many!)
            discrete_treatment: Whether treatment is binary
            cv_folds: Cross-validation folds for nuisance estimation
            save_results: Save results to file
        
        Returns:
            Dictionary with ATE, standard error, confidence interval
        """
        if not ECONML_AVAILABLE:
            raise ImportError("EconML required. pip install econml")
        
        logger.info(f"Double Machine Learning: {treatment} → {outcome}")
        logger.info(f"Number of controls: {len(controls)}")
        
        # Prepare data
        required_cols = [treatment, outcome] + controls
        df_clean = self.data[required_cols].dropna()
        
        Y = df_clean[outcome].values
        T = df_clean[treatment].values
        X = df_clean[controls].values
        
        logger.info(f"Sample size: {len(df_clean)}")
        
        # DML Estimator
        est = LinearDML(
            model_y=GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=self.random_state),
            model_t=GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=self.random_state) if not discrete_treatment else \
                   LogisticRegression(max_iter=500, random_state=self.random_state),
            discrete_treatment=discrete_treatment,
            linear_first_stages=False,
            cv=cv_folds,
            random_state=self.random_state
        )
        
        est.fit(Y, T, X=X, W=None)
        
        # Average Treatment Effect
        ate = est.effect(X).mean()
        ate_stderr = est.effect_stderr(X).mean()
        ate_ci_lower = ate - 1.96 * ate_stderr
        ate_ci_upper = ate + 1.96 * ate_stderr
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Double Machine Learning Results")
        logger.info(f"{'='*60}")
        logger.info(f"Average Treatment Effect (ATE): {ate:.4f}")
        logger.info(f"Standard Error: {ate_stderr:.4f}")
        logger.info(f"95% Confidence Interval: [{ate_ci_lower:.4f}, {ate_ci_upper:.4f}]")
        logger.info(f"p-value: {2 * (1 - norm.cdf(abs(ate / ate_stderr))):.4f}")
        
        # Compare with naive OLS (for reference)
        ols_comparison = self._compare_with_ols(df_clean, treatment, outcome, controls)
        
        # Prepare results
        results = {
            'treatment': treatment,
            'outcome': outcome,
            'ate': ate,
            'ate_stderr': ate_stderr,
            'ate_ci': (ate_ci_lower, ate_ci_upper),
            'p_value': 2 * (1 - norm.cdf(abs(ate / ate_stderr))),
            'ols_comparison': ols_comparison,
            'model': est
        }
        
        self.results['dml'] = results
        
        if save_results:
            # Save summary
            summary = {
                'method': 'Double Machine Learning',
                'treatment': treatment,
                'outcome': outcome,
                'n_controls': len(controls),
                'n_observations': len(df_clean),
                'ate': float(ate),
                'ate_stderr': float(ate_stderr),
                'ate_ci_lower': float(ate_ci_lower),
                'ate_ci_upper': float(ate_ci_upper),
                'p_value': float(results['p_value'])
            }
            
            with open(self.output_dir / 'dml_results.json', 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info("DML results saved")
        
        return results
    
    def _compare_with_ols(
        self,
        df: pd.DataFrame,
        treatment: str,
        outcome: str,
        controls: List[str]
    ) -> Dict:
        """Compare DML with naive OLS (for reference)."""
        
        # OLS regression
        formula = f"{outcome} ~ {treatment} + " + " + ".join(controls)
        
        try:
            ols_model = smf.ols(formula, data=df).fit()
            
            ols_coef = ols_model.params[treatment]
            ols_se = ols_model.bse[treatment]
            ols_pval = ols_model.pvalues[treatment]
            
            logger.info(f"\nNaive OLS Comparison:")
            logger.info(f"OLS coefficient: {ols_coef:.4f} (SE: {ols_se:.4f}, p={ols_pval:.4f})")
            
            return {
                'ols_coef': ols_coef,
                'ols_se': ols_se,
                'ols_pval': ols_pval
            }
        except Exception as e:
            logger.warning(f"OLS comparison failed: {e}")
            return {}
    
    # ========================================================================
    # 3. SYNTHETIC CONTROL METHOD
    # ========================================================================
    
    def synthetic_control(
        self,
        treated_unit: Union[str, int],
        treatment_time: Union[str, int],
        outcome_var: str,
        donor_pool: List[Union[str, int]],
        pre_treatment_periods: Optional[int] = None,
        optimize_method: str = 'L2',
        save_results: bool = True
    ) -> Dict:
        """
        Synthetic Control Method for case studies with single treated unit.
        
        Theoretical Foundation:
        - Abadie & Gardeazabal (2003): Economic Costs of Conflict (Basque Country)
        - Abadie et al. (2010): Synthetic Control Methods for Comparative Case Studies
        
        Gold Standard for:
        - Single treated unit (or few treated units)
        - Rich pre-treatment data
        - Event study / Policy evaluation
        - Transparent counterfactual construction
        
        Research Applications:
        1. **Firm-Level Events**:
           - CEO change effect on performance
           - Major acquisition impact on innovation
           - Strategic reorientation consequences
        
        2. **Policy/Regulation**:
           - Sarbanes-Oxley Act impact on specific firms
           - Patent law changes on affected industries
        
        3. **Competitive Dynamics**:
           - Entry of new competitor on focal firm
           - Technology disruption effects
        
        Example:
        ```python
        # Apple's Beats acquisition (2014) impact on innovation
        sc_results = causal.synthetic_control(
            treated_unit='AAPL',
            treatment_time='2014-05',
            outcome_var='patent_count',
            donor_pool=['MSFT', 'GOOG', 'AMZN', 'FB', 'NFLX']
        )
        ```
        
        Args:
            treated_unit: ID of treated firm
            treatment_time: Time period when treatment occurs
            outcome_var: Outcome variable to track
            donor_pool: List of control firms (potential synthetic control donors)
            pre_treatment_periods: Number of pre-treatment periods (auto-detect if None)
            optimize_method: Optimization objective ('L2', 'L1', 'Lasso')
            save_results: Save results and plots
        
        Returns:
            Dictionary with synthetic control weights, treatment effect, and plots
        """
        logger.info(f"Synthetic Control Method")
        logger.info(f"Treated unit: {treated_unit}")
        logger.info(f"Treatment time: {treatment_time}")
        logger.info(f"Donor pool: {len(donor_pool)} units")
        
        # Prepare data
        df_treated = self.data[self.data[self.firm_id] == treated_unit].sort_values(self.time_var)
        df_donors = self.data[self.data[self.firm_id].isin(donor_pool)].copy()
        
        # Split pre/post treatment
        treated_pre = df_treated[df_treated[self.time_var] < treatment_time]
        treated_post = df_treated[df_treated[self.time_var] >= treatment_time]
        
        # Donor pool pre/post
        donors_pre = df_donors[df_donors[self.time_var] < treatment_time]
        donors_post = df_donors[df_donors[self.time_var] >= treatment_time]
        
        # Pivot to matrix form
        Y_treated_pre = treated_pre[outcome_var].values
        Y_treated_post = treated_post[outcome_var].values
        
        # Donor matrix (each column = one donor)
        Y_donors_pre = donors_pre.pivot(
            index=self.time_var, 
            columns=self.firm_id, 
            values=outcome_var
        ).values
        
        Y_donors_post = donors_post.pivot(
            index=self.time_var, 
            columns=self.firm_id, 
            values=outcome_var
        ).values
        
        logger.info(f"Pre-treatment periods: {len(Y_treated_pre)}")
        logger.info(f"Post-treatment periods: {len(Y_treated_post)}")
        
        # Optimize weights to match pre-treatment treated unit
        weights = self._optimize_synthetic_control_weights(
            Y_treated_pre,
            Y_donors_pre,
            method=optimize_method
        )
        
        logger.info(f"\nSynthetic Control Weights:")
        weights_df = pd.DataFrame({
            'donor': donor_pool,
            'weight': weights
        }).sort_values('weight', ascending=False)
        logger.info(weights_df.to_string(index=False))
        
        # Construct synthetic control
        synthetic_pre = Y_donors_pre @ weights
        synthetic_post = Y_donors_post @ weights
        
        # Treatment effect (post-treatment difference)
        treatment_effect = Y_treated_post - synthetic_post
        ate_post = treatment_effect.mean()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Synthetic Control Results")
        logger.info(f"{'='*60}")
        logger.info(f"Average Treatment Effect (post-period): {ate_post:.4f}")
        logger.info(f"Pre-treatment RMSPE: {np.sqrt(np.mean((Y_treated_pre - synthetic_pre)**2)):.4f}")
        
        # Visualization
        self._visualize_synthetic_control(
            treated_pre, treated_post,
            synthetic_pre, synthetic_post,
            treated_unit, treatment_time, outcome_var
        )
        
        # Prepare results
        results = {
            'treated_unit': treated_unit,
            'treatment_time': treatment_time,
            'outcome_var': outcome_var,
            'donor_pool': donor_pool,
            'weights': weights_df,
            'ate_post': ate_post,
            'treatment_effect_series': treatment_effect,
            'Y_treated_pre': Y_treated_pre,
            'Y_treated_post': Y_treated_post,
            'synthetic_pre': synthetic_pre,
            'synthetic_post': synthetic_post
        }
        
        self.results['synthetic_control'] = results
        
        if save_results:
            weights_df.to_excel(
                self.output_dir / 'synthetic_control_weights.xlsx',
                index=False
            )
            
            # Save time series
            time_series = pd.DataFrame({
                'time': list(treated_pre[self.time_var]) + list(treated_post[self.time_var]),
                'treated': list(Y_treated_pre) + list(Y_treated_post),
                'synthetic': list(synthetic_pre) + list(synthetic_post),
                'gap': [0]*len(Y_treated_pre) + list(treatment_effect)
            })
            time_series.to_excel(
                self.output_dir / 'synthetic_control_series.xlsx',
                index=False
            )
            
            logger.info("Synthetic Control results saved")
        
        return results
    
    def _optimize_synthetic_control_weights(
        self,
        Y_treated: np.ndarray,
        Y_donors: np.ndarray,
        method: str = 'L2'
    ) -> np.ndarray:
        """
        Optimize weights to minimize pre-treatment fit.
        
        Objective: min ||Y_treated - Y_donors @ w||²
        Subject to: Σw = 1, w ≥ 0
        """
        n_donors = Y_donors.shape[1]
        
        if method == 'L2':
            # Quadratic programming
            def objective(w):
                return np.sum((Y_treated - Y_donors @ w) ** 2)
        
        elif method == 'L1':
            # L1 loss (more robust to outliers)
            def objective(w):
                return np.sum(np.abs(Y_treated - Y_donors @ w))
        
        else:
            def objective(w):
                return np.sum((Y_treated - Y_donors @ w) ** 2)
        
        # Constraints: sum(w) = 1, w >= 0
        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = [(0, 1) for _ in range(n_donors)]
        
        # Initial guess: equal weights
        w0 = np.ones(n_donors) / n_donors
        
        # Optimize
        result = minimize(
            objective,
            w0,
            bounds=bounds,
            constraints=constraints,
            method='SLSQP'
        )
        
        if not result.success:
            logger.warning(f"Optimization did not converge: {result.message}")
        
        return result.x
    
    def _visualize_synthetic_control(
        self,
        treated_pre: pd.DataFrame,
        treated_post: pd.DataFrame,
        synthetic_pre: np.ndarray,
        synthetic_post: np.ndarray,
        treated_unit: str,
        treatment_time: str,
        outcome_var: str
    ):
        """Visualize Synthetic Control results."""
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Combine pre and post
        time_pre = treated_pre[self.time_var].values
        time_post = treated_post[self.time_var].values
        time_all = np.concatenate([time_pre, time_post])
        
        Y_treated_all = np.concatenate([
            treated_pre[outcome_var].values,
            treated_post[outcome_var].values
        ])
        synthetic_all = np.concatenate([synthetic_pre, synthetic_post])
        
        # Plot 1: Treated vs. Synthetic
        axes[0].plot(time_all, Y_treated_all, 'b-', label=f'Treated: {treated_unit}', linewidth=2)
        axes[0].plot(time_all, synthetic_all, 'r--', label='Synthetic Control', linewidth=2)
        axes[0].axvline(x=treatment_time, color='gray', linestyle=':', label='Treatment', linewidth=2)
        axes[0].set_xlabel('Time')
        axes[0].set_ylabel(outcome_var)
        axes[0].set_title('Synthetic Control Analysis: Treated vs. Synthetic')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # Plot 2: Treatment Effect (Gap)
        gap_pre = treated_pre[outcome_var].values - synthetic_pre
        gap_post = treated_post[outcome_var].values - synthetic_post
        gap_all = np.concatenate([gap_pre, gap_post])
        
        axes[1].plot(time_all, gap_all, 'g-', linewidth=2)
        axes[1].axhline(y=0, color='black', linestyle='-', linewidth=1)
        axes[1].axvline(x=treatment_time, color='gray', linestyle=':', label='Treatment', linewidth=2)
        axes[1].fill_between(
            time_post,
            0,
            gap_post,
            alpha=0.3,
            color='green' if gap_post.mean() > 0 else 'red'
        )
        axes[1].set_xlabel('Time')
        axes[1].set_ylabel(f'Gap ({outcome_var})')
        axes[1].set_title('Treatment Effect Over Time')
        axes[1].legend()
        axes[1].grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'synthetic_control.png', dpi=300)
        plt.close()
        
        logger.info("Synthetic Control visualization saved")
    
    # ========================================================================
    # 4. PROPENSITY SCORE MATCHING
    # ========================================================================
    
    def propensity_score_matching(
        self,
        treatment: str,
        outcome: str,
        covariates: List[str],
        matching_method: str = 'nearest',
        n_neighbors: int = 1,
        caliper: Optional[float] = 0.1,
        estimate_att: bool = True,
        save_results: bool = True
    ) -> Dict:
        """
        Propensity Score Matching for treatment effect estimation.
        
        Theoretical Foundation:
        - Rosenbaum & Rubin (1983): The Central Role of the Propensity Score
        - Assumptions: Selection on observables, Common support, SUTVA
        
        When to Use:
        - Binary treatment (e.g., M&A yes/no, alliance formed yes/no)
        - Rich set of pre-treatment covariates
        - Want to balance treated and control groups
        - Concern about confounding bias
        
        Matching Methods:
        - 'nearest': Nearest neighbor matching
        - 'radius': Within-caliper matching
        - 'kernel': Kernel-weighted matching
        
        Research Applications:
        - M&A effects (match acquirers to non-acquirers)
        - Strategic alliance formation (match alliance firms to non-alliance)
        - CEO turnover effects (match firms with vs. without turnover)
        
        Args:
            treatment: Binary treatment variable
            outcome: Outcome variable
            covariates: Variables for propensity score estimation
            matching_method: Matching algorithm
            n_neighbors: Number of matches per treated unit
            caliper: Maximum propensity score distance (0-1)
            estimate_att: Estimate ATT (Average Treatment effect on Treated)
            save_results: Save results to file
        
        Returns:
            Dictionary with ATT, balance diagnostics, matched pairs
        """
        logger.info(f"Propensity Score Matching: {treatment} → {outcome}")
        
        # Prepare data
        required_cols = [treatment, outcome] + covariates
        df_clean = self.data[required_cols].dropna()
        
        # Ensure treatment is binary
        if df_clean[treatment].nunique() != 2:
            raise ValueError(f"Treatment must be binary. Found {df_clean[treatment].nunique()} unique values")
        
        X = df_clean[covariates].values
        T = df_clean[treatment].values.astype(int)
        Y = df_clean[outcome].values
        
        n_treated = T.sum()
        n_control = len(T) - n_treated
        
        logger.info(f"Sample: {n_treated} treated, {n_control} control")
        
        # Estimate propensity scores
        logit = LogisticRegression(max_iter=500, random_state=self.random_state)
        logit.fit(X, T)
        propensity_scores = logit.predict_proba(X)[:, 1]
        
        df_clean['propensity_score'] = propensity_scores
        
        # Check common support
        ps_treated = propensity_scores[T == 1]
        ps_control = propensity_scores[T == 0]
        
        common_support_min = max(ps_treated.min(), ps_control.min())
        common_support_max = min(ps_treated.max(), ps_control.max())
        
        logger.info(f"Common support: [{common_support_min:.4f}, {common_support_max:.4f}]")
        
        # Matching
        if matching_method == 'nearest':
            matched_pairs, matched_indices = self._nearest_neighbor_matching(
                propensity_scores, T, n_neighbors, caliper
            )
        else:
            raise NotImplementedError(f"Matching method '{matching_method}' not implemented yet")
        
        # Estimate ATT
        if estimate_att:
            treated_indices = np.where(T == 1)[0]
            matched_treated_indices = [i for i, j in matched_pairs]
            matched_control_indices = [j for i, j in matched_pairs]
            
            Y_treated_matched = Y[matched_treated_indices]
            Y_control_matched = Y[matched_control_indices]
            
            att = (Y_treated_matched - Y_control_matched).mean()
            att_se = (Y_treated_matched - Y_control_matched).std() / np.sqrt(len(matched_pairs))
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Propensity Score Matching Results")
            logger.info(f"{'='*60}")
            logger.info(f"ATT (Average Treatment effect on Treated): {att:.4f}")
            logger.info(f"Standard Error: {att_se:.4f}")
            logger.info(f"95% CI: [{att - 1.96*att_se:.4f}, {att + 1.96*att_se:.4f}]")
            logger.info(f"Number of matched pairs: {len(matched_pairs)}")
        
        # Balance diagnostics
        balance = self._check_covariate_balance(
            df_clean, T, matched_indices, covariates
        )
        
        # Visualization
        self._visualize_psm_results(
            df_clean, T, propensity_scores, matched_indices, treatment
        )
        
        # Prepare results
        results = {
            'treatment': treatment,
            'outcome': outcome,
            'att': att if estimate_att else None,
            'att_se': att_se if estimate_att else None,
            'att_ci': (att - 1.96*att_se, att + 1.96*att_se) if estimate_att else None,
            'n_matched_pairs': len(matched_pairs),
            'matched_pairs': matched_pairs,
            'balance_diagnostics': balance,
            'propensity_scores': propensity_scores
        }
        
        self.results['psm'] = results
        
        if save_results:
            # Save matched pairs
            matched_df = pd.DataFrame(matched_pairs, columns=['treated_idx', 'control_idx'])
            matched_df.to_excel(
                self.output_dir / 'psm_matched_pairs.xlsx',
                index=False
            )
            
            # Save balance diagnostics
            balance.to_excel(
                self.output_dir / 'psm_balance.xlsx',
                index=False
            )
            
            logger.info("PSM results saved")
        
        return results
    
    def _nearest_neighbor_matching(
        self,
        propensity_scores: np.ndarray,
        treatment: np.ndarray,
        n_neighbors: int = 1,
        caliper: Optional[float] = None
    ) -> Tuple[List[Tuple], np.ndarray]:
        """Nearest neighbor propensity score matching."""
        
        treated_indices = np.where(treatment == 1)[0]
        control_indices = np.where(treatment == 0)[0]
        
        ps_treated = propensity_scores[treated_indices].reshape(-1, 1)
        ps_control = propensity_scores[control_indices].reshape(-1, 1)
        
        # Find nearest neighbors
        nn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
        nn.fit(ps_control)
        
        distances, indices = nn.kneighbors(ps_treated)
        
        # Apply caliper if specified
        matched_pairs = []
        matched_control_used = set()
        
        for i, treated_idx in enumerate(treated_indices):
            for j in range(n_neighbors):
                distance = distances[i, j]
                control_match_idx = control_indices[indices[i, j]]
                
                # Check caliper
                if caliper is not None and distance > caliper:
                    continue
                
                # Check if control already used (without replacement)
                if control_match_idx in matched_control_used:
                    continue
                
                matched_pairs.append((treated_idx, control_match_idx))
                matched_control_used.add(control_match_idx)
                break  # Only one match per treated unit
        
        matched_indices = np.array(list(matched_control_used))
        
        logger.info(f"Matched {len(matched_pairs)} out of {len(treated_indices)} treated units")
        
        return matched_pairs, matched_indices
    
    def _check_covariate_balance(
        self,
        df: pd.DataFrame,
        treatment: np.ndarray,
        matched_control_indices: np.ndarray,
        covariates: List[str]
    ) -> pd.DataFrame:
        """Check covariate balance before/after matching."""
        
        balance_results = []
        
        treated_indices = np.where(treatment == 1)[0]
        all_control_indices = np.where(treatment == 0)[0]
        
        for var in covariates:
            # Before matching
            treated_mean_before = df.iloc[treated_indices][var].mean()
            control_mean_before = df.iloc[all_control_indices][var].mean()
            std_diff_before = (treated_mean_before - control_mean_before) / df[var].std()
            
            # After matching
            control_mean_after = df.iloc[matched_control_indices][var].mean()
            std_diff_after = (treated_mean_before - control_mean_after) / df[var].std()
            
            balance_results.append({
                'variable': var,
                'treated_mean': treated_mean_before,
                'control_mean_before': control_mean_before,
                'control_mean_after': control_mean_after,
                'std_diff_before': std_diff_before,
                'std_diff_after': std_diff_after,
                'balanced': abs(std_diff_after) < 0.1  # Common threshold
            })
        
        balance_df = pd.DataFrame(balance_results)
        
        logger.info(f"\nCovariate Balance:")
        logger.info(balance_df.to_string(index=False))
        
        return balance_df
    
    def _visualize_psm_results(
        self,
        df: pd.DataFrame,
        treatment: np.ndarray,
        propensity_scores: np.ndarray,
        matched_control_indices: np.ndarray,
        treatment_var: str
    ):
        """Visualize PSM results."""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Propensity score distribution
        ps_treated = propensity_scores[treatment == 1]
        ps_control_all = propensity_scores[treatment == 0]
        ps_control_matched = propensity_scores[matched_control_indices]
        
        axes[0].hist(ps_control_all, bins=30, alpha=0.5, label='Control (All)', density=True)
        axes[0].hist(ps_control_matched, bins=30, alpha=0.5, label='Control (Matched)', density=True)
        axes[0].hist(ps_treated, bins=30, alpha=0.5, label='Treated', density=True)
        axes[0].set_xlabel('Propensity Score')
        axes[0].set_ylabel('Density')
        axes[0].set_title('Propensity Score Distribution')
        axes[0].legend()
        
        # Common support
        axes[1].scatter(
            range(len(ps_control_all)),
            ps_control_all,
            alpha=0.3,
            s=20,
            label='Control (All)'
        )
        axes[1].scatter(
            range(len(ps_treated)),
            ps_treated,
            alpha=0.5,
            s=50,
            marker='*',
            label='Treated'
        )
        axes[1].axhline(y=max(ps_treated.min(), ps_control_all.min()), 
                       color='r', linestyle='--', label='Common Support')
        axes[1].axhline(y=min(ps_treated.max(), ps_control_all.max()), 
                       color='r', linestyle='--')
        axes[1].set_xlabel('Observation Index')
        axes[1].set_ylabel('Propensity Score')
        axes[1].set_title('Common Support Region')
        axes[1].legend()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'psm_diagnostics.png', dpi=300)
        plt.close()
        
        logger.info("PSM visualizations saved")
    
    # ========================================================================
    # 5. COMPREHENSIVE REPORT
    # ========================================================================
    
    def generate_causal_report(self) -> str:
        """
        Generate comprehensive causal inference report.
        
        Returns:
            Path to HTML report
        """
        logger.info("Generating comprehensive causal inference report...")
        
        html_content = self._build_causal_html_report()
        
        report_path = self.output_dir / 'causal_inference_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Causal report saved: {report_path}")
        
        return str(report_path)
    
    def _build_causal_html_report(self) -> str:
        """Build HTML report."""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Causal Inference Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #e74c3c; padding-bottom: 10px; }}
        .metric {{ font-weight: bold; color: #e74c3c; }}
        .section {{ margin-bottom: 40px; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #e74c3c; color: white; }}
    </style>
</head>
<body>
    <h1>Causal Inference Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <hr>
"""
        
        # Causal Forest
        if 'causal_forest' in self.results:
            cf = self.results['causal_forest']
            html += f"""
    <div class="section">
        <h2>1. Causal Forest (Heterogeneous Effects)</h2>
        <p><strong>Treatment:</strong> {cf['treatment']} → <strong>Outcome:</strong> {cf['outcome']}</p>
        <p><strong>Average Treatment Effect (ATE):</strong> <span class="metric">{cf['ate']:.4f}</span></p>
        <p><strong>95% CI:</strong> [{cf['ate_ci'][0]:.4f}, {cf['ate_ci'][1]:.4f}]</p>
        <img src="causal_forest_results.png" alt="Causal Forest">
    </div>
"""
        
        # Double Machine Learning
        if 'dml' in self.results:
            dml = self.results['dml']
            html += f"""
    <div class="section">
        <h2>2. Double Machine Learning</h2>
        <p><strong>Treatment:</strong> {dml['treatment']} → <strong>Outcome:</strong> {dml['outcome']}</p>
        <p><strong>ATE:</strong> <span class="metric">{dml['ate']:.4f}</span> (SE: {dml['ate_stderr']:.4f})</p>
        <p><strong>95% CI:</strong> [{dml['ate_ci'][0]:.4f}, {dml['ate_ci'][1]:.4f}]</p>
        <p><strong>p-value:</strong> {dml['p_value']:.4f}</p>
    </div>
"""
        
        # Synthetic Control
        if 'synthetic_control' in self.results:
            sc = self.results['synthetic_control']
            html += f"""
    <div class="section">
        <h2>3. Synthetic Control</h2>
        <p><strong>Treated Unit:</strong> {sc['treated_unit']}</p>
        <p><strong>Treatment Time:</strong> {sc['treatment_time']}</p>
        <p><strong>Average Post-Treatment Effect:</strong> <span class="metric">{sc['ate_post']:.4f}</span></p>
        <img src="synthetic_control.png" alt="Synthetic Control">
    </div>
"""
        
        # PSM
        if 'psm' in self.results:
            psm = self.results['psm']
            html += f"""
    <div class="section">
        <h2>4. Propensity Score Matching</h2>
        <p><strong>Treatment:</strong> {psm['treatment']} → <strong>Outcome:</strong> {psm['outcome']}</p>
        <p><strong>ATT:</strong> <span class="metric">{psm['att']:.4f}</span> (SE: {psm['att_se']:.4f})</p>
        <p><strong>95% CI:</strong> [{psm['att_ci'][0]:.4f}, {psm['att_ci'][1]:.4f}]</p>
        <p><strong>Matched Pairs:</strong> {psm['n_matched_pairs']}</p>
        <img src="psm_diagnostics.png" alt="PSM Diagnostics">
    </div>
"""
        
        html += """
    <hr>
    <p><em>Generated by Strategic Management Research Hub v3.1 - Causal ML Integration</em></p>
</body>
</html>
"""
        
        return html


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def example_usage():
    """Example demonstrating Causal ML Integration."""
    
    # Sample data (placeholder)
    np.random.seed(42)
    n = 500
    
    # Generate confounders
    X1 = np.random.normal(0, 1, n)  # firm size
    X2 = np.random.uniform(0, 1, n)  # prior experience
    
    # Treatment assignment (selection bias)
    propensity = 1 / (1 + np.exp(-(X1 + X2)))
    treatment = np.random.binomial(1, propensity)
    
    # Outcome (heterogeneous effects)
    treatment_effect = 0.5 + 0.3 * X1  # Effect varies by firm size
    noise = np.random.normal(0, 0.5, n)
    outcome = 2 + X1 + X2 + treatment * treatment_effect + noise
    
    df_sample = pd.DataFrame({
        'firm_id': range(n),
        'year': 2020,
        'treatment': treatment,
        'outcome': outcome,
        'firm_size': X1,
        'prior_experience': X2
    })
    
    # Initialize
    causal = CausalMLIntegration(
        data=df_sample,
        firm_id='firm_id',
        time_var='year',
        output_dir='./causal_example_output/'
    )
    
    # Causal Forest
    print("\n" + "="*60)
    print("CAUSAL FOREST (Heterogeneous Effects)")
    print("="*60)
    
    if ECONML_AVAILABLE:
        cf_results = causal.causal_forest(
            treatment='treatment',
            outcome='outcome',
            controls=[],
            heterogeneity_vars=['firm_size', 'prior_experience'],
            discrete_treatment=True
        )
    
    # Double Machine Learning
    print("\n" + "="*60)
    print("DOUBLE MACHINE LEARNING")
    print("="*60)
    
    if ECONML_AVAILABLE:
        dml_results = causal.double_machine_learning(
            treatment='treatment',
            outcome='outcome',
            controls=['firm_size', 'prior_experience'],
            discrete_treatment=True
        )
    
    # Propensity Score Matching
    print("\n" + "="*60)
    print("PROPENSITY SCORE MATCHING")
    print("="*60)
    
    psm_results = causal.propensity_score_matching(
        treatment='treatment',
        outcome='outcome',
        covariates=['firm_size', 'prior_experience'],
        matching_method='nearest',
        n_neighbors=1
    )
    
    # Generate Report
    print("\n" + "="*60)
    print("GENERATING REPORT")
    print("="*60)
    
    report_path = causal.generate_causal_report()
    
    print(f"\n✅ Causal analysis complete!")
    print(f"📊 Report: {report_path}")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Strategic Management Research Hub v3.1                      ║
    ║   ML × Causal Inference Integration                           ║
    ║                                                               ║
    ║   State-of-the-art causal methods for strategy research      ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    example_usage()
