"""
mediation_moderation.py

Mediation and Moderation Analysis

This module implements mediation and moderation analysis for strategic
management research, particularly for understanding:
- Mechanisms through which X affects Y (mediation)
- Conditions under which X affects Y (moderation)

Common applications:
- How does strategy (X) affect performance (Y) through innovation (M)?
- Under what conditions (moderator W) does strategy (X) affect performance (Y)?

Usage:
    from mediation_moderation import MediationAnalyzer, ModerationAnalyzer
    
    # Mediation
    med = MediationAnalyzer(df, X='strategy', Y='performance', M='innovation')
    results = med.analyze()
    
    # Moderation
    mod = ModerationAnalyzer(df, X='rd_intensity', Y='roa', W='firm_size')
    results = mod.analyze()
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MediationAnalyzer:
    """
    Mediation Analysis (Baron & Kenny, 1986)
    
    Tests whether M mediates the relationship between X and Y
    
    Steps:
    1. Test if X → Y (c path, total effect)
    2. Test if X → M (a path)
    3. Test if M → Y controlling for X (b path)
    4. Test if X → Y controlling for M (c' path, direct effect)
    
    Mediation occurs if:
    - Steps 1-3 are significant
    - Step 4 (c') is smaller than Step 1 (c)
    
    Attributes:
        df: Input DataFrame
        X: Independent variable
        Y: Dependent variable
        M: Mediator variable
        controls: Control variables
    """
    
    def __init__(self, df: pd.DataFrame,
                 X: str,
                 Y: str,
                 M: str,
                 controls: List[str] = None):
        """
        Initialize mediation analyzer
        
        Args:
            df: DataFrame
            X: Independent variable name
            Y: Dependent variable name
            M: Mediator variable name
            controls: List of control variable names
        """
        self.df = df.copy()
        self.X = X
        self.Y = Y
        self.M = M
        self.controls = controls or []
        
        logger.info(f"Mediation Analysis initialized:")
        logger.info(f"  X (Independent): {X}")
        logger.info(f"  Y (Dependent): {Y}")
        logger.info(f"  M (Mediator): {M}")
        if self.controls:
            logger.info(f"  Controls: {len(self.controls)} variables")
    
    def analyze(self) -> Dict:
        """
        Perform complete mediation analysis
        
        Returns:
            Dictionary with all path coefficients and significance tests
        """
        try:
            import statsmodels.api as sm
        except ImportError:
            logger.error("statsmodels not installed")
            return None
        
        logger.info("\nPerforming mediation analysis...")
        
        # Prepare data
        analysis_vars = [self.X, self.Y, self.M] + self.controls
        df_clean = self.df[analysis_vars].dropna()
        
        logger.info(f"Sample size: {len(df_clean)}")
        
        results = {}
        
        # Step 1: Total effect (c path): X → Y
        logger.info("\n[Step 1] Total effect (c path): X → Y")
        X_vars = [self.X] + self.controls
        X_matrix = sm.add_constant(df_clean[X_vars])
        y = df_clean[self.Y]
        
        model_total = sm.OLS(y, X_matrix).fit()
        c_coef = model_total.params[self.X]
        c_pval = model_total.pvalues[self.X]
        
        results['total_effect'] = {
            'coefficient': c_coef,
            'p_value': c_pval,
            'significant': c_pval < 0.05
        }
        
        logger.info(f"  c (total effect): {c_coef:.4f} (p={c_pval:.4f})")
        
        # Step 2: Path a: X → M
        logger.info("\n[Step 2] Path a: X → M")
        y_m = df_clean[self.M]
        
        model_a = sm.OLS(y_m, X_matrix).fit()
        a_coef = model_a.params[self.X]
        a_pval = model_a.pvalues[self.X]
        
        results['path_a'] = {
            'coefficient': a_coef,
            'p_value': a_pval,
            'significant': a_pval < 0.05
        }
        
        logger.info(f"  a (X → M): {a_coef:.4f} (p={a_pval:.4f})")
        
        # Step 3: Path b & c': M and X → Y
        logger.info("\n[Step 3] Paths b and c': M and X → Y")
        X_M_vars = [self.X, self.M] + self.controls
        X_M_matrix = sm.add_constant(df_clean[X_M_vars])
        
        model_mediated = sm.OLS(y, X_M_matrix).fit()
        b_coef = model_mediated.params[self.M]
        b_pval = model_mediated.pvalues[self.M]
        c_prime_coef = model_mediated.params[self.X]
        c_prime_pval = model_mediated.pvalues[self.X]
        
        results['path_b'] = {
            'coefficient': b_coef,
            'p_value': b_pval,
            'significant': b_pval < 0.05
        }
        
        results['direct_effect'] = {
            'coefficient': c_prime_coef,
            'p_value': c_prime_pval,
            'significant': c_prime_pval < 0.05
        }
        
        logger.info(f"  b (M → Y|X): {b_coef:.4f} (p={b_pval:.4f})")
        logger.info(f"  c' (direct effect): {c_prime_coef:.4f} (p={c_prime_pval:.4f})")
        
        # Indirect effect and proportion mediated
        indirect_effect = a_coef * b_coef
        proportion_mediated = indirect_effect / c_coef if c_coef != 0 else np.nan
        
        results['indirect_effect'] = indirect_effect
        results['proportion_mediated'] = proportion_mediated
        
        # Sobel test for indirect effect
        se_indirect = np.sqrt(b_coef**2 * model_a.bse[self.X]**2 + 
                             a_coef**2 * model_mediated.bse[self.M]**2)
        z_score = indirect_effect / se_indirect if se_indirect > 0 else np.nan
        p_value_sobel = 2 * (1 - np.abs(z_score)) if not np.isnan(z_score) else np.nan
        
        results['sobel_test'] = {
            'z_score': z_score,
            'p_value': p_value_sobel,
            'significant': p_value_sobel < 0.05 if not np.isnan(p_value_sobel) else False
        }
        
        # Determine mediation type
        if results['total_effect']['significant'] and results['path_a']['significant'] and results['path_b']['significant']:
            if results['direct_effect']['significant']:
                mediation_type = 'Partial Mediation'
            else:
                mediation_type = 'Full Mediation'
        else:
            mediation_type = 'No Mediation'
        
        results['mediation_type'] = mediation_type
        
        logger.info(f"\n{'='*60}")
        logger.info("Mediation Analysis Results")
        logger.info(f"{'='*60}")
        logger.info(f"Total effect (c): {c_coef:.4f} ***" if c_pval < 0.001 else f"Total effect (c): {c_coef:.4f}")
        logger.info(f"Direct effect (c'): {c_prime_coef:.4f}")
        logger.info(f"Indirect effect (a*b): {indirect_effect:.4f}")
        logger.info(f"Proportion mediated: {proportion_mediated:.2%}" if not np.isnan(proportion_mediated) else "Proportion mediated: N/A")
        logger.info(f"Mediation type: {mediation_type}")
        logger.info(f"{'='*60}")
        
        return results


class ModerationAnalyzer:
    """
    Moderation Analysis
    
    Tests whether W moderates the relationship between X and Y
    
    Model: Y = b0 + b1*X + b2*W + b3*X*W + controls + error
    
    Moderation occurs if b3 (interaction term) is significant
    
    Attributes:
        df: Input DataFrame
        X: Independent variable
        Y: Dependent variable
        W: Moderator variable
        controls: Control variables
    """
    
    def __init__(self, df: pd.DataFrame,
                 X: str,
                 Y: str,
                 W: str,
                 controls: List[str] = None):
        """
        Initialize moderation analyzer
        
        Args:
            df: DataFrame
            X: Independent variable name
            Y: Dependent variable name
            W: Moderator variable name
            controls: List of control variable names
        """
        self.df = df.copy()
        self.X = X
        self.Y = Y
        self.W = W
        self.controls = controls or []
        
        logger.info(f"Moderation Analysis initialized:")
        logger.info(f"  X (Independent): {X}")
        logger.info(f"  Y (Dependent): {Y}")
        logger.info(f"  W (Moderator): {W}")
        if self.controls:
            logger.info(f"  Controls: {len(self.controls)} variables")
    
    def analyze(self, center_vars: bool = True) -> Dict:
        """
        Perform moderation analysis
        
        Args:
            center_vars: Whether to mean-center X and W before creating interaction
        
        Returns:
            Dictionary with regression results and simple slopes analysis
        """
        try:
            import statsmodels.api as sm
        except ImportError:
            logger.error("statsmodels not installed")
            return None
        
        logger.info("\nPerforming moderation analysis...")
        
        # Prepare data
        analysis_vars = [self.X, self.Y, self.W] + self.controls
        df_clean = self.df[analysis_vars].dropna()
        
        logger.info(f"Sample size: {len(df_clean)}")
        
        # Mean-center X and W if requested
        if center_vars:
            logger.info("Mean-centering X and W...")
            df_clean[f'{self.X}_c'] = df_clean[self.X] - df_clean[self.X].mean()
            df_clean[f'{self.W}_c'] = df_clean[self.W] - df_clean[self.W].mean()
            X_use = f'{self.X}_c'
            W_use = f'{self.W}_c'
        else:
            X_use = self.X
            W_use = self.W
        
        # Create interaction term
        df_clean['interaction'] = df_clean[X_use] * df_clean[W_use]
        
        # Build regression model
        predictors = [X_use, W_use, 'interaction'] + self.controls
        X_matrix = sm.add_constant(df_clean[predictors])
        y = df_clean[self.Y]
        
        model = sm.OLS(y, X_matrix).fit()
        
        # Extract results
        interaction_coef = model.params['interaction']
        interaction_pval = model.pvalues['interaction']
        
        results = {
            'main_effect_X': {
                'coefficient': model.params[X_use],
                'p_value': model.pvalues[X_use]
            },
            'main_effect_W': {
                'coefficient': model.params[W_use],
                'p_value': model.pvalues[W_use]
            },
            'interaction': {
                'coefficient': interaction_coef,
                'p_value': interaction_pval,
                'significant': interaction_pval < 0.05
            },
            'model': {
                'r_squared': model.rsquared,
                'adj_r_squared': model.rsquared_adj,
                'f_statistic': model.fvalue,
                'f_pvalue': model.f_pvalue
            }
        }
        
        # Simple slopes analysis
        if interaction_pval < 0.10:  # Analyze if marginally significant
            logger.info("\nPerforming simple slopes analysis...")
            simple_slopes = self._simple_slopes_analysis(df_clean, X_use, W_use, model)
            results['simple_slopes'] = simple_slopes
        
        logger.info(f"\n{'='*60}")
        logger.info("Moderation Analysis Results")
        logger.info(f"{'='*60}")
        logger.info(f"Main effect (X): {results['main_effect_X']['coefficient']:.4f} (p={results['main_effect_X']['p_value']:.4f})")
        logger.info(f"Main effect (W): {results['main_effect_W']['coefficient']:.4f} (p={results['main_effect_W']['p_value']:.4f})")
        logger.info(f"Interaction (X*W): {interaction_coef:.4f} (p={interaction_pval:.4f})")
        
        if results['interaction']['significant']:
            logger.info("\n✓ Significant moderation effect detected!")
        else:
            logger.info("\n✗ No significant moderation effect")
        
        logger.info(f"\nModel fit:")
        logger.info(f"  R²: {model.rsquared:.4f}")
        logger.info(f"  Adj. R²: {model.rsquared_adj:.4f}")
        logger.info(f"{'='*60}")
        
        return results
    
    def _simple_slopes_analysis(self, df: pd.DataFrame, 
                                X_var: str, W_var: str,
                                model) -> Dict:
        """
        Calculate simple slopes at different levels of moderator
        
        Args:
            df: DataFrame with centered variables
            X_var: X variable name (possibly centered)
            W_var: W variable name (possibly centered)
            model: Fitted regression model
        
        Returns:
            Dictionary with simple slopes at low, mean, high W
        """
        try:
            import statsmodels.api as sm
        except ImportError:
            return {}
        
        # Calculate W at mean ± 1 SD
        w_mean = df[W_var].mean()
        w_std = df[W_var].std()
        
        w_levels = {
            'low': w_mean - w_std,
            'mean': w_mean,
            'high': w_mean + w_std
        }
        
        simple_slopes = {}
        
        b1 = model.params[X_var]
        b3 = model.params['interaction']
        
        for level, w_value in w_levels.items():
            # Simple slope = b1 + b3*W
            slope = b1 + b3 * w_value
            
            # Standard error (simplified)
            # For more accurate SE, use delta method
            se = model.bse[X_var]
            t_stat = slope / se if se > 0 else np.nan
            
            simple_slopes[level] = {
                'W_value': w_value,
                'slope': slope,
                'se': se,
                't_statistic': t_stat
            }
            
            logger.info(f"  Simple slope at W={level}: {slope:.4f}")
        
        return simple_slopes


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n = 500
    
    # Mediation example: strategy → innovation → performance
    strategy = np.random.normal(0, 1, n)
    innovation = 0.5 * strategy + np.random.normal(0, 0.5, n)
    performance = 0.3 * strategy + 0.4 * innovation + np.random.normal(0, 0.5, n)
    
    df_mediation = pd.DataFrame({
        'strategy': strategy,
        'innovation': innovation,
        'performance': performance
    })
    
    print("="*60)
    print("MEDIATION ANALYSIS EXAMPLE")
    print("="*60)
    
    med = MediationAnalyzer(
        df_mediation,
        X='strategy',
        Y='performance',
        M='innovation'
    )
    med_results = med.analyze()
    
    # Moderation example: R&D intensity * firm size → ROA
    rd_intensity = np.random.normal(0, 1, n)
    firm_size = np.random.normal(0, 1, n)
    roa = 0.05 + 0.3 * rd_intensity + 0.2 * firm_size + 0.15 * rd_intensity * firm_size + np.random.normal(0, 0.5, n)
    
    df_moderation = pd.DataFrame({
        'rd_intensity': rd_intensity,
        'firm_size': firm_size,
        'roa': roa
    })
    
    print("\n\n")
    print("="*60)
    print("MODERATION ANALYSIS EXAMPLE")
    print("="*60)
    
    mod = ModerationAnalyzer(
        df_moderation,
        X='rd_intensity',
        Y='roa',
        W='firm_size'
    )
    mod_results = mod.analyze(center_vars=True)
