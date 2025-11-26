"""
psm_analysis.py

Propensity Score Matching (PSM) Analysis

This module implements Propensity Score Matching for causal inference
in strategic management research, particularly for treatment effect estimation
when randomization is not possible.

Common applications:
- M&A impact analysis
- Policy intervention effects
- Strategic choice consequences
- Alliance formation outcomes

Usage:
    from psm_analysis import PSMAnalyzer
    
    psm = PSMAnalyzer(df, treatment='merged', outcome='roa')
    matched_df = psm.match(method='nearest', caliper=0.1)
    ate = psm.estimate_ate()
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PSMAnalyzer:
    """
    Propensity Score Matching Analyzer
    
    Implements various matching methods to estimate treatment effects
    while controlling for selection bias.
    
    Attributes:
        df: Input DataFrame
        treatment: Treatment variable (binary: 0/1)
        outcome: Outcome variable
        covariates: List of covariate variables
        propensity_scores: Estimated propensity scores
        matched_data: Matched dataset
    """
    
    def __init__(self, df: pd.DataFrame,
                 treatment: str,
                 outcome: str,
                 covariates: List[str] = None):
        """
        Initialize PSM analyzer
        
        Args:
            df: DataFrame with treatment, outcome, and covariates
            treatment: Name of treatment variable (must be binary 0/1)
            outcome: Name of outcome variable
            covariates: List of covariate names (if None, use all numeric columns)
        """
        self.df = df.copy()
        self.treatment = treatment
        self.outcome = outcome
        
        # Validate treatment variable
        if not set(self.df[treatment].dropna().unique()).issubset({0, 1}):
            raise ValueError(f"Treatment variable '{treatment}' must be binary (0/1)")
        
        # Set covariates
        if covariates is None:
            self.covariates = [col for col in df.select_dtypes(include=[np.number]).columns
                             if col not in [treatment, outcome]]
        else:
            self.covariates = covariates
        
        self.propensity_scores = None
        self.matched_data = None
        
        logger.info(f"PSM Analyzer initialized:")
        logger.info(f"  Treatment: {treatment}")
        logger.info(f"  Outcome: {outcome}")
        logger.info(f"  Covariates: {len(self.covariates)} variables")
    
    def estimate_propensity_scores(self, method: str = 'logit') -> np.ndarray:
        """
        Estimate propensity scores using logistic regression
        
        Args:
            method: Estimation method ('logit' or 'probit')
        
        Returns:
            Array of propensity scores
        """
        logger.info("Estimating propensity scores...")
        
        # Prepare data
        analysis_vars = [self.treatment] + self.covariates
        df_clean = self.df[analysis_vars].dropna()
        
        X = df_clean[self.covariates]
        y = df_clean[self.treatment]
        
        try:
            import statsmodels.api as sm
            
            # Add constant
            X = sm.add_constant(X)
            
            # Fit logistic regression
            if method == 'logit':
                model = sm.Logit(y, X)
            elif method == 'probit':
                model = sm.Probit(y, X)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            result = model.fit(disp=False)
            
            # Get propensity scores
            self.propensity_scores = result.predict(X)
            
            # Add to dataframe
            df_clean['propensity_score'] = self.propensity_scores
            self.df = self.df.merge(
                df_clean[[self.treatment, 'propensity_score']],
                left_index=True, right_index=True,
                how='left',
                suffixes=('', '_ps')
            )
            
            logger.info(f"  ✓ Propensity scores estimated (method: {method})")
            logger.info(f"  Mean propensity score: {self.propensity_scores.mean():.3f}")
            
            return self.propensity_scores
            
        except ImportError:
            logger.error("statsmodels not installed. Cannot estimate propensity scores.")
            return None
    
    def match(self, method: str = 'nearest', 
             caliper: float = None,
             replacement: bool = False,
             n_neighbors: int = 1) -> pd.DataFrame:
        """
        Perform matching based on propensity scores
        
        Args:
            method: Matching method ('nearest', 'radius', 'kernel')
            caliper: Maximum distance for matching (default: 0.25 * std of propensity scores)
            replacement: Whether to match with replacement
            n_neighbors: Number of control units to match (for nearest neighbor)
        
        Returns:
            Matched DataFrame
        """
        if self.propensity_scores is None:
            self.estimate_propensity_scores()
        
        logger.info(f"Performing {method} neighbor matching...")
        
        # Prepare data
        df_treated = self.df[self.df[self.treatment] == 1].copy()
        df_control = self.df[self.df[self.treatment] == 0].copy()
        
        logger.info(f"  Treated units: {len(df_treated)}")
        logger.info(f"  Control units: {len(df_control)}")
        
        if method == 'nearest':
            matched_data = self._nearest_neighbor_matching(
                df_treated, df_control, 
                caliper=caliper,
                replacement=replacement,
                n_neighbors=n_neighbors
            )
        else:
            logger.warning(f"Method '{method}' not yet implemented. Using nearest neighbor.")
            matched_data = self._nearest_neighbor_matching(
                df_treated, df_control,
                caliper=caliper,
                replacement=replacement,
                n_neighbors=n_neighbors
            )
        
        self.matched_data = matched_data
        logger.info(f"  ✓ Matching completed: {len(matched_data)} matched pairs")
        
        return matched_data
    
    def _nearest_neighbor_matching(self, df_treated: pd.DataFrame,
                                   df_control: pd.DataFrame,
                                   caliper: float = None,
                                   replacement: bool = False,
                                   n_neighbors: int = 1) -> pd.DataFrame:
        """
        Nearest neighbor matching implementation
        
        Args:
            df_treated: Treated units DataFrame
            df_control: Control units DataFrame
            caliper: Maximum distance for matching
            replacement: Whether to allow replacement
            n_neighbors: Number of neighbors to match
        
        Returns:
            Matched DataFrame
        """
        if caliper is None:
            caliper = 0.25 * self.propensity_scores.std()
        
        logger.info(f"  Caliper: {caliper:.4f}")
        
        matched_pairs = []
        used_controls = set()
        
        for idx, treated_row in df_treated.iterrows():
            treated_ps = treated_row['propensity_score']
            
            # Calculate distances to all control units
            if replacement:
                available_controls = df_control
            else:
                available_controls = df_control[~df_control.index.isin(used_controls)]
            
            if len(available_controls) == 0:
                continue
            
            distances = np.abs(
                available_controls['propensity_score'] - treated_ps
            )
            
            # Find nearest neighbors within caliper
            valid_matches = distances[distances <= caliper].nsmallest(n_neighbors)
            
            if len(valid_matches) > 0:
                for control_idx in valid_matches.index:
                    matched_pairs.append({
                        'treated_id': idx,
                        'control_id': control_idx,
                        'distance': distances[control_idx]
                    })
                    if not replacement:
                        used_controls.add(control_idx)
        
        logger.info(f"  Matched pairs: {len(matched_pairs)}")
        
        # Create matched dataset
        matched_treated = []
        matched_control = []
        
        for pair in matched_pairs:
            matched_treated.append(df_treated.loc[pair['treated_id']])
            matched_control.append(df_control.loc[pair['control_id']])
        
        matched_df = pd.concat([
            pd.DataFrame(matched_treated),
            pd.DataFrame(matched_control)
        ], ignore_index=True)
        
        return matched_df
    
    def estimate_ate(self) -> Dict:
        """
        Estimate Average Treatment Effect (ATE)
        
        Returns:
            Dictionary with ATE estimates and statistics
        """
        if self.matched_data is None:
            logger.error("No matched data available. Run match() first.")
            return None
        
        logger.info("Estimating Average Treatment Effect (ATE)...")
        
        # Calculate outcomes by treatment group
        treated_outcomes = self.matched_data[
            self.matched_data[self.treatment] == 1
        ][self.outcome]
        
        control_outcomes = self.matched_data[
            self.matched_data[self.treatment] == 0
        ][self.outcome]
        
        # Calculate ATE
        ate = treated_outcomes.mean() - control_outcomes.mean()
        
        # Standard error (simplified - use bootstrap for more accurate estimate)
        n_treated = len(treated_outcomes)
        n_control = len(control_outcomes)
        
        pooled_var = (
            (n_treated - 1) * treated_outcomes.var() +
            (n_control - 1) * control_outcomes.var()
        ) / (n_treated + n_control - 2)
        
        se = np.sqrt(pooled_var * (1/n_treated + 1/n_control))
        
        # T-statistic
        t_stat = ate / se if se > 0 else np.nan
        
        results = {
            'ate': ate,
            'se': se,
            't_stat': t_stat,
            'treated_mean': treated_outcomes.mean(),
            'control_mean': control_outcomes.mean(),
            'n_treated': n_treated,
            'n_control': n_control
        }
        
        logger.info(f"\nAverage Treatment Effect (ATE):")
        logger.info(f"  ATE: {ate:.4f}")
        logger.info(f"  SE: {se:.4f}")
        logger.info(f"  t-statistic: {t_stat:.4f}")
        logger.info(f"  Treated mean: {treated_outcomes.mean():.4f}")
        logger.info(f"  Control mean: {control_outcomes.mean():.4f}")
        
        return results
    
    def check_balance(self) -> pd.DataFrame:
        """
        Check covariate balance before and after matching
        
        Returns:
            DataFrame with balance statistics
        """
        if self.matched_data is None:
            logger.error("No matched data available. Run match() first.")
            return None
        
        logger.info("Checking covariate balance...")
        
        balance_stats = []
        
        for covar in self.covariates:
            # Before matching
            treated_before = self.df[self.df[self.treatment] == 1][covar].mean()
            control_before = self.df[self.df[self.treatment] == 0][covar].mean()
            std_diff_before = (treated_before - control_before) / self.df[covar].std()
            
            # After matching
            treated_after = self.matched_data[self.matched_data[self.treatment] == 1][covar].mean()
            control_after = self.matched_data[self.matched_data[self.treatment] == 0][covar].mean()
            std_diff_after = (treated_after - control_after) / self.matched_data[covar].std()
            
            balance_stats.append({
                'covariate': covar,
                'std_diff_before': std_diff_before,
                'std_diff_after': std_diff_after,
                'improvement': abs(std_diff_before) - abs(std_diff_after)
            })
        
        balance_df = pd.DataFrame(balance_stats)
        
        logger.info("\nCovariate Balance:")
        logger.info(balance_df.to_string(index=False))
        
        return balance_df


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n = 1000
    
    # Covariates
    firm_size = np.random.normal(10, 2, n)
    industry = np.random.choice([0, 1, 2], n)
    age = np.random.normal(15, 5, n)
    
    # Treatment assignment (influenced by covariates)
    propensity = 1 / (1 + np.exp(-(
        -2 + 0.5*firm_size + 0.3*industry + 0.2*age + np.random.normal(0, 1, n)
    )))
    treatment = (np.random.random(n) < propensity).astype(int)
    
    # Outcome (influenced by treatment and covariates)
    outcome = (
        0.05 +
        0.1 * treatment +  # Treatment effect
        0.02 * firm_size +
        0.01 * age +
        np.random.normal(0, 0.02, n)
    )
    
    df = pd.DataFrame({
        'firm_id': range(n),
        'treatment': treatment,
        'outcome': outcome,
        'firm_size': firm_size,
        'industry': industry,
        'age': age
    })
    
    # Run PSM
    psm = PSMAnalyzer(df, treatment='treatment', outcome='outcome')
    psm.estimate_propensity_scores()
    matched_df = psm.match(caliper=0.1, n_neighbors=1)
    ate_results = psm.estimate_ate()
    balance = psm.check_balance()
    
    print("\n" + "="*60)
    print("PSM Analysis completed!")
    print("="*60)
