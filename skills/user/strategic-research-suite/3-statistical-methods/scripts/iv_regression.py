"""
iv_regression.py

Instrumental Variables (IV) Regression - 2SLS & GMM

This module provides IV estimation methods for handling endogeneity:
- Two-Stage Least Squares (2SLS)
- Generalized Method of Moments (GMM)
- Weak instrument tests
- Overidentification tests
- Endogeneity tests

Usage:
    from iv_regression import IVRegression
    
    iv = IVRegression(df)
    results = iv.two_stage_least_squares(y='roa', X=['rd_intensity'], 
                                        Z=['lagged_rd'], endogenous=['rd_intensity'])
    print(results.summary())
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from linearmodels.iv import IV2SLS, IVGMM
from linearmodels.iv.results import IVResults
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IVRegression:
    """
    Instrumental Variables regression toolkit
    
    Handles endogeneity using IV/2SLS methods with comprehensive diagnostics
    
    Attributes:
        df: Input DataFrame
        panel_structure: Whether data has panel structure
    """
    
    def __init__(self, df: pd.DataFrame,
                 firm_id: Optional[str] = None,
                 time_id: Optional[str] = None):
        """
        Initialize IV regression analyzer
        
        Args:
            df: Dataset
            firm_id: Optional firm identifier for panel data
            time_id: Optional time identifier for panel data
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_id = time_id
        self.panel_structure = (firm_id is not None) and (time_id is not None)
        
        if self.panel_structure:
            self.panel_data = self.df.set_index([self.firm_id, self.time_id]).sort_index()
            logger.info(f"Panel IV initialized: {len(df[firm_id].unique())} firms, "
                       f"{len(df[time_id].unique())} periods")
        else:
            logger.info(f"Cross-sectional IV initialized: {len(df)} observations")
    
    def two_stage_least_squares(self,
                                y: str,
                                X: List[str],
                                Z: List[str],
                                endogenous: List[str],
                                controls: Optional[List[str]] = None,
                                cluster: Optional[str] = None) -> Tuple[IVResults, Dict]:
        """
        Two-Stage Least Squares (2SLS) estimation
        
        Args:
            y: Dependent variable name
            X: List of all independent variables (exogenous + endogenous)
            Z: List of instruments
            endogenous: List of endogenous variables (subset of X)
            controls: Additional exogenous controls
            cluster: Variable to cluster standard errors on
        
        Returns:
            Tuple of (regression results, diagnostics)
        """
        logger.info(f"Running 2SLS: {y} ~ {X} | Instruments: {Z}")
        
        # Prepare exogenous variables (all X except endogenous, plus controls)
        exogenous = [x for x in X if x not in endogenous]
        if controls:
            exogenous.extend(controls)
        
        # Create formula
        dependent = self.df[y]
        exog = self.df[exogenous]
        endog = self.df[endogenous]
        instruments = self.df[Z]
        
        # Run 2SLS
        model = IV2SLS(dependent=dependent, exog=exog, endog=endog, instruments=instruments)
        
        # Determine covariance type
        if cluster:
            results = model.fit(cov_type='clustered', clusters=self.df[cluster])
        else:
            results = model.fit(cov_type='robust')
        
        logger.info(f"2SLS completed. R²: {results.rsquared:.4f}")
        
        # Run diagnostics
        diagnostics = self._run_diagnostics(results, y, X, Z, endogenous)
        
        return results, diagnostics
    
    def _run_diagnostics(self,
                        results: IVResults,
                        y: str,
                        X: List[str],
                        Z: List[str],
                        endogenous: List[str]) -> Dict:
        """Run IV diagnostics"""
        diagnostics = {}
        
        # F-statistic from first stage
        if hasattr(results, 'first_stage'):
            diagnostics['first_stage_fstat'] = {
                var: float(results.first_stage.diagnostics.loc['f.stat', var])
                for var in endogenous
            }
            
            # Weak instrument test (F < 10 is weak)
            diagnostics['weak_instruments'] = {
                var: results.first_stage.diagnostics.loc['f.stat', var] < 10
                for var in endogenous
            }
        
        # Sargan-Hansen J statistic (overidentification test)
        if hasattr(results, 'sargan'):
            diagnostics['sargan_pvalue'] = float(results.sargan.pval)
            diagnostics['overidentified'] = results.sargan.pval > 0.05
        
        # Wu-Hausman endogeneity test
        if hasattr(results, 'wu_hausman'):
            diagnostics['wu_hausman_pvalue'] = float(results.wu_hausman.pval)
            diagnostics['endogeneity_detected'] = results.wu_hausman.pval < 0.05
        
        return diagnostics
    
    def print_diagnostics(self, diagnostics: Dict):
        """Print IV diagnostics in readable format"""
        print("\n" + "="*60)
        print("IV Regression Diagnostics")
        print("="*60)
        
        if 'first_stage_fstat' in diagnostics:
            print("\n[First Stage F-statistics]")
            for var, fstat in diagnostics['first_stage_fstat'].items():
                weak = "⚠️ WEAK" if diagnostics['weak_instruments'][var] else "✓ Strong"
                print(f"  {var}: F = {fstat:.2f} {weak}")
        
        if 'sargan_pvalue' in diagnostics:
            print(f"\n[Overidentification Test (Sargan-Hansen J)]")
            print(f"  p-value: {diagnostics['sargan_pvalue']:.4f}")
            status = "✓ Valid instruments" if diagnostics['overidentified'] else "⚠️ Overidentified"
            print(f"  Status: {status}")
        
        if 'wu_hausman_pvalue' in diagnostics:
            print(f"\n[Endogeneity Test (Wu-Hausman)]")
            print(f"  p-value: {diagnostics['wu_hausman_pvalue']:.4f}")
            status = "⚠️ Endogeneity detected (use IV)" if diagnostics['endogeneity_detected'] else "OLS sufficient"
            print(f"  Status: {status}")
        
        print("="*60)
    
    def gmm_estimation(self,
                      y: str,
                      X: List[str],
                      Z: List[str],
                      endogenous: List[str],
                      controls: Optional[List[str]] = None,
                      cluster: Optional[str] = None) -> IVResults:
        """
        GMM estimation (more efficient with heteroskedasticity)
        
        Args:
            y: Dependent variable name
            X: List of all independent variables
            Z: List of instruments
            endogenous: List of endogenous variables
            controls: Additional exogenous controls
            cluster: Variable to cluster standard errors on
        
        Returns:
            GMM regression results
        """
        logger.info(f"Running GMM: {y} ~ {X} | Instruments: {Z}")
        
        exogenous = [x for x in X if x not in endogenous]
        if controls:
            exogenous.extend(controls)
        
        dependent = self.df[y]
        exog = self.df[exogenous]
        endog = self.df[endogenous]
        instruments = self.df[Z]
        
        model = IVGMM(dependent=dependent, exog=exog, endog=endog, instruments=instruments)
        
        if cluster:
            results = model.fit(cov_type='clustered', clusters=self.df[cluster])
        else:
            results = model.fit(cov_type='robust')
        
        logger.info(f"GMM completed. R²: {results.rsquared:.4f}")
        
        return results


# Example usage
if __name__ == "__main__":
    # Generate sample data with endogeneity
    np.random.seed(42)
    n = 1000
    
    # Unobserved confounder
    u = np.random.normal(0, 1, n)
    
    # Instrument (correlated with X but not with error)
    z1 = np.random.normal(0, 1, n)
    z2 = np.random.normal(0, 1, n)
    
    # Endogenous variable (correlated with error through u)
    x_endo = 2 + 0.5 * z1 + 0.3 * z2 + 0.8 * u + np.random.normal(0, 0.5, n)
    
    # Exogenous variable
    x_exog = np.random.normal(0, 1, n)
    
    # Outcome (endogenous relationship)
    y = 5 + 1.5 * x_endo + 0.8 * x_exog + 0.7 * u + np.random.normal(0, 1, n)
    
    df = pd.DataFrame({
        'y': y,
        'x_endo': x_endo,
        'x_exog': x_exog,
        'z1': z1,
        'z2': z2,
        'firm_id': np.repeat(range(100), 10),
        'year': np.tile(range(2014, 2024), 100)
    })
    
    # Run IV regression
    iv = IVRegression(df)
    
    results, diagnostics = iv.two_stage_least_squares(
        y='y',
        X=['x_endo', 'x_exog'],
        Z=['z1', 'z2'],
        endogenous=['x_endo']
    )
    
    print("\n" + "="*60)
    print("2SLS Results")
    print("="*60)
    print(results.summary)
    
    iv.print_diagnostics(diagnostics)
    
    # Compare with GMM
    gmm_results = iv.gmm_estimation(
        y='y',
        X=['x_endo', 'x_exog'],
        Z=['z1', 'z2'],
        endogenous=['x_endo']
    )
    
    print("\n" + "="*60)
    print("GMM Results")
    print("="*60)
    print(gmm_results.summary)
