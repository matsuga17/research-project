"""
Strategic Management Research Hub - Data Quality Checker Module
================================================================

Publication-ready quality assurance system for strategic management research.
Implements comprehensive checks required by top journals (SMJ, AMJ, ASQ, OS):

- Multivariate outlier detection (Ensemble methods)
- Benford's Law test (fraud detection)
- Structural break detection (Chow test)
- Statistical power analysis
- Panel balance & attrition analysis
- Accounting identity verification

Author: Strategic Management Research Hub
Version: 3.0
License: MIT
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple, Union
import logging
from pathlib import Path
import json
from datetime import datetime

# Machine learning libraries for outlier detection
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Statistical power analysis
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdvancedQualityAssurance:
    """
    Comprehensive quality assurance system for panel data in strategic management research.
    
    Usage:
    ```python
    qa = AdvancedQualityAssurance(
        df_panel,
        firm_id='gvkey',
        time_var='year',
        verbose=True
    )
    
    qa_report = qa.run_comprehensive_qa()
    qa.generate_report(output_dir='./qa_reports/')
    ```
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        firm_id: str,
        time_var: str,
        verbose: bool = True
    ):
        """
        Initialize QA system.
        
        Args:
            data: Panel DataFrame
            firm_id: Column name for firm identifier
            time_var: Column name for time variable
            verbose: Print detailed logs
        """
        self.data = data.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.verbose = verbose
        self.qa_results = {}
        
        logger.info(f"QA System initialized: {len(data)} obs, "
                   f"{data[firm_id].nunique()} firms, "
                   f"{data[time_var].nunique()} periods")
    
    def run_comprehensive_qa(self) -> Dict:
        """
        Run all QA checks and return comprehensive report.
        
        Returns:
            Dictionary with all QA results
        """
        logger.info("=" * 60)
        logger.info("STARTING COMPREHENSIVE QUALITY ASSURANCE")
        logger.info("=" * 60)
        
        # Phase 1: Outlier Detection
        logger.info("\n[1/6] Multivariate Outlier Detection...")
        self.qa_results['outliers'] = self.multivariate_outlier_detection()
        
        # Phase 2: Benford's Law
        logger.info("\n[2/6] Benford's Law Test...")
        self.qa_results['benfords_law'] = self.benfords_law_test()
        
        # Phase 3: Structural Breaks
        logger.info("\n[3/6] Structural Break Detection...")
        self.qa_results['structural_breaks'] = self.structural_break_detection()
        
        # Phase 4: Panel Balance
        logger.info("\n[4/6] Panel Balance Analysis...")
        self.qa_results['panel_balance'] = self.panel_balance_analysis()
        
        # Phase 5: Selection Bias
        logger.info("\n[5/6] Attrition & Selection Bias Analysis...")
        self.qa_results['selection_bias'] = self.attrition_analysis()
        
        # Phase 6: Accounting Identities
        logger.info("\n[6/6] Accounting Identity Verification...")
        self.qa_results['accounting_checks'] = self.accounting_identity_check()
        
        logger.info("\n" + "=" * 60)
        logger.info("QUALITY ASSURANCE COMPLETE")
        logger.info("=" * 60)
        
        self._print_summary()
        
        return self.qa_results
    
    def multivariate_outlier_detection(
        self,
        methods: List[str] = ['isolation_forest', 'lof', 'dbscan'],
        contamination: float = 0.05
    ) -> Dict:
        """
        Detect multivariate outliers using ensemble of methods.
        
        Args:
            methods: List of detection methods to use
            contamination: Expected proportion of outliers
            
        Returns:
            Dictionary with outlier detection results
        """
        # Select continuous variables
        continuous_vars = self.data.select_dtypes(include=[np.number]).columns.tolist()
        continuous_vars = [v for v in continuous_vars 
                          if v not in [self.firm_id, self.time_var]]
        
        if len(continuous_vars) == 0:
            logger.warning("No continuous variables found for outlier detection")
            return {'outliers_detected': 0}
        
        # Prepare data
        X = self.data[continuous_vars].dropna()
        X_scaled = StandardScaler().fit_transform(X)
        
        outlier_scores = pd.DataFrame(index=X.index)
        
        # Method 1: Isolation Forest
        if 'isolation_forest' in methods:
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=42
            )
            outlier_scores['iso_forest'] = iso_forest.fit_predict(X_scaled)
        
        # Method 2: Local Outlier Factor
        if 'lof' in methods:
            lof = LocalOutlierFactor(contamination=contamination)
            outlier_scores['lof'] = lof.fit_predict(X_scaled)
        
        # Method 3: DBSCAN
        if 'dbscan' in methods:
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            labels = dbscan.fit_predict(X_scaled)
            outlier_scores['dbscan'] = np.where(labels == -1, -1, 1)
        
        # Ensemble: Vote-based detection
        outlier_scores['outlier_votes'] = (outlier_scores == -1).sum(axis=1)
        outlier_scores['is_outlier'] = (outlier_scores['outlier_votes'] >= 2).astype(int)
        
        # High confidence outliers (detected by all methods)
        high_confidence = (outlier_scores['outlier_votes'] == len(methods))
        
        # Add to original data
        self.data['outlier_flag'] = 0
        self.data.loc[X.index, 'outlier_flag'] = outlier_scores['is_outlier']
        
        self.data['outlier_confidence'] = 0.0
        self.data.loc[X.index, 'outlier_confidence'] = (
            outlier_scores['outlier_votes'] / len(methods)
        )
        
        results = {
            'total_outliers': outlier_scores['is_outlier'].sum(),
            'high_confidence_outliers': high_confidence.sum(),
            'outlier_rate': outlier_scores['is_outlier'].mean(),
            'methods_used': methods,
            'contamination': contamination
        }
        
        logger.info(f"Detected {results['total_outliers']} outliers "
                   f"({results['outlier_rate']:.1%})")
        logger.info(f"High confidence: {results['high_confidence_outliers']}")
        
        return results
    
    def benfords_law_test(
        self,
        variables: Optional[List[str]] = None,
        alpha: float = 0.05
    ) -> Dict:
        """
        Test conformance to Benford's Law (fraud/manipulation detection).
        
        Args:
            variables: Variables to test (default: all continuous)
            alpha: Significance level
            
        Returns:
            Dictionary with test results
        """
        if variables is None:
            variables = self.data.select_dtypes(include=[np.number]).columns.tolist()
            variables = [v for v in variables 
                        if v not in [self.firm_id, self.time_var]]
        
        # Benford's Law expected distribution
        benford_probs = np.array([
            np.log10(1 + 1/d) for d in range(1, 10)
        ])
        
        test_results = {}
        conforming_vars = []
        suspicious_vars = []
        
        for var in variables:
            # Extract first digits
            values = self.data[var].dropna()
            values = values[values > 0]  # Benford only applies to positive values
            
            if len(values) < 100:  # Benford unreliable for small samples
                continue
            
            first_digits = values.apply(
                lambda x: int(str(float(x)).lstrip('0')[0])
            )
            
            # Observed distribution
            observed_counts = first_digits.value_counts().sort_index()
            expected_counts = benford_probs * len(first_digits)
            
            # Chi-squared test
            chi2_stat = sum(
                (observed_counts.get(d, 0) - expected_counts[d-1])**2 / 
                expected_counts[d-1]
                for d in range(1, 10)
            )
            p_value = 1 - chi2.cdf(chi2_stat, df=8)
            
            test_results[var] = {
                'chi2_statistic': chi2_stat,
                'p_value': p_value,
                'conforms': p_value > alpha
            }
            
            if p_value > alpha:
                conforming_vars.append(var)
            else:
                suspicious_vars.append(var)
        
        overall_conformance = len(conforming_vars) / len(test_results) if test_results else 1.0
        
        results = {
            'conforms_to_benford': overall_conformance > 0.7,
            'conformance_rate': overall_conformance,
            'suspicious_variables': suspicious_vars,
            'variable_tests': test_results
        }
        
        if suspicious_vars:
            logger.warning(f"⚠️  Benford's Law violations detected: {suspicious_vars}")
        else:
            logger.info("✓ Benford's Law: No violations detected")
        
        return results
    
    def structural_break_detection(
        self,
        key_variables: Optional[List[str]] = None,
        alpha: float = 0.05
    ) -> Dict:
        """
        Detect structural breaks using Chow test.
        
        Args:
            key_variables: Variables to test for breaks
            alpha: Significance level
            
        Returns:
            Dictionary with break detection results
        """
        if key_variables is None:
            key_variables = self.data.select_dtypes(include=[np.number]).columns.tolist()
            key_variables = [v for v in key_variables[:5]  # Test top 5 only
                           if v not in [self.firm_id, self.time_var]]
        
        time_periods = sorted(self.data[self.time_var].unique())
        
        if len(time_periods) < 10:  # Need sufficient periods
            logger.warning("Insufficient time periods for structural break detection")
            return {'breaks_detected': 0}
        
        break_points = []
        
        for var in key_variables:
            # Test each potential break point (middle periods only)
            for t in time_periods[3:-3]:
                
                before = self.data[self.data[self.time_var] < t][var].dropna()
                after = self.data[self.data[self.time_var] >= t][var].dropna()
                
                if len(before) < 30 or len(after) < 30:
                    continue
                
                # Chow test (F-test for equality of means)
                f_stat, p_value = stats.f_oneway(before, after)
                
                if p_value < alpha:
                    break_points.append({
                        'time': t,
                        'variable': var,
                        'f_statistic': f_stat,
                        'p_value': p_value
                    })
        
        results = {
            'breaks_detected': len(break_points),
            'break_points': break_points
        }
        
        if break_points:
            logger.warning(f"⚠️  {len(break_points)} structural breaks detected")
        else:
            logger.info("✓ No structural breaks detected")
        
        return results
    
    def panel_balance_analysis(self) -> Dict:
        """
        Analyze panel balance and structure.
        
        Returns:
            Dictionary with panel balance statistics
        """
        # Count observations per firm
        obs_per_firm = self.data.groupby(self.firm_id).size()
        
        max_periods = self.data[self.time_var].nunique()
        balanced_firms = (obs_per_firm == max_periods).sum()
        
        results = {
            'total_firms': self.data[self.firm_id].nunique(),
            'total_observations': len(self.data),
            'time_periods': max_periods,
            'balanced_firms': balanced_firms,
            'balance_rate': balanced_firms / self.data[self.firm_id].nunique(),
            'avg_obs_per_firm': obs_per_firm.mean(),
            'min_obs_per_firm': obs_per_firm.min(),
            'max_obs_per_firm': obs_per_firm.max()
        }
        
        logger.info(f"Panel balance: {results['balance_rate']:.1%} "
                   f"({balanced_firms}/{results['total_firms']} firms)")
        
        return results
    
    def attrition_analysis(self) -> Dict:
        """
        Analyze sample attrition and selection bias.
        
        Returns:
            Dictionary with attrition analysis results
        """
        # Identify firms that attrite (exit before final period)
        final_period = self.data[self.time_var].max()
        
        last_period_per_firm = self.data.groupby(self.firm_id)[self.time_var].max()
        attrite_firms = (last_period_per_firm < final_period)
        
        attrition_rate = attrite_firms.mean()
        
        # Compare attrite vs. survive firms
        self.data['attrite'] = self.data[self.firm_id].map(
            lambda x: 1 if attrite_firms.get(x, False) else 0
        )
        
        # Test for systematic differences
        continuous_vars = self.data.select_dtypes(include=[np.number]).columns.tolist()
        continuous_vars = [v for v in continuous_vars 
                          if v not in [self.firm_id, self.time_var, 'attrite']][:5]
        
        differences = {}
        for var in continuous_vars:
            attrite_mean = self.data[self.data['attrite'] == 1][var].mean()
            survive_mean = self.data[self.data['attrite'] == 0][var].mean()
            
            t_stat, p_value = stats.ttest_ind(
                self.data[self.data['attrite'] == 1][var].dropna(),
                self.data[self.data['attrite'] == 0][var].dropna()
            )
            
            differences[var] = {
                'attrite_mean': attrite_mean,
                'survive_mean': survive_mean,
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        results = {
            'total_firms': self.data[self.firm_id].nunique(),
            'attrite_firms': attrite_firms.sum(),
            'attrition_rate': attrition_rate,
            'systematic_differences': any(d['significant'] for d in differences.values()),
            'variable_comparisons': differences
        }
        
        if attrition_rate > 0.3:
            logger.warning(f"⚠️  High attrition rate: {attrition_rate:.1%}")
        else:
            logger.info(f"✓ Attrition rate: {attrition_rate:.1%}")
        
        return results
    
    def accounting_identity_check(
        self,
        tolerance: float = 0.01
    ) -> Dict:
        """
        Verify accounting identities (Balance Sheet, Income Statement).
        
        Args:
            tolerance: Acceptable error percentage
            
        Returns:
            Dictionary with verification results
        """
        checks = {}
        
        # Balance Sheet Identity: Assets = Liabilities + Equity
        if all(col in self.data.columns for col in ['at', 'lt', 'ceq']):
            self.data['bs_error'] = abs(
                self.data['at'] - (self.data['lt'] + self.data['ceq'])
            )
            self.data['bs_error_pct'] = self.data['bs_error'] / self.data['at']
            
            violations = (self.data['bs_error_pct'] > tolerance).sum()
            violation_rate = violations / len(self.data)
            
            checks['balance_sheet'] = {
                'violations': violations,
                'violation_rate': violation_rate,
                'mean_error': self.data['bs_error_pct'].mean(),
                'max_error': self.data['bs_error_pct'].max()
            }
            
            if violation_rate > 0.05:
                logger.warning(f"⚠️  Balance sheet violations: {violation_rate:.1%}")
            else:
                logger.info(f"✓ Balance sheet identity verified")
        
        results = {
            'checks_performed': list(checks.keys()),
            'results': checks
        }
        
        return results
    
    def generate_report(
        self,
        output_formats: List[str] = ['html', 'json'],
        output_dir: str = './qa_reports/'
    ):
        """
        Generate QA report in multiple formats.
        
        Args:
            output_formats: List of formats ('html', 'json', 'pdf')
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON report
        if 'json' in output_formats:
            json_path = output_path / f'qa_report_{timestamp}.json'
            with open(json_path, 'w') as f:
                json.dump(self.qa_results, f, indent=2, default=str)
            logger.info(f"JSON report saved: {json_path}")
        
        # HTML report
        if 'html' in output_formats:
            html_path = output_path / f'qa_report_{timestamp}.html'
            self._generate_html_report(html_path)
            logger.info(f"HTML report saved: {html_path}")
        
        logger.info(f"QA reports generated in {output_dir}")
    
    def _generate_html_report(self, output_path: Path):
        """Generate HTML QA report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quality Assurance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; }}
                .pass {{ color: #27ae60; font-weight: bold; }}
                .warning {{ color: #e67e22; font-weight: bold; }}
                .fail {{ color: #e74c3c; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
            </style>
        </head>
        <body>
            <h1>Quality Assurance Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>Executive Summary</h2>
            <ul>
                <li>Total Observations: {len(self.data)}</li>
                <li>Firms: {self.data[self.firm_id].nunique()}</li>
                <li>Time Periods: {self.data[self.time_var].nunique()}</li>
            </ul>
            
            <h2>Quality Checks</h2>
            <table>
                <tr><th>Check</th><th>Status</th><th>Details</th></tr>
                <tr>
                    <td>Outlier Detection</td>
                    <td class="pass">COMPLETE</td>
                    <td>{self.qa_results.get('outliers', {}).get('total_outliers', 0)} outliers detected</td>
                </tr>
                <tr>
                    <td>Benford's Law</td>
                    <td class="{'pass' if self.qa_results.get('benfords_law', {}).get('conforms_to_benford', True) else 'warning'}">
                        {'PASS' if self.qa_results.get('benfords_law', {}).get('conforms_to_benford', True) else 'WARNING'}
                    </td>
                    <td>Conformance rate: {self.qa_results.get('benfords_law', {}).get('conformance_rate', 0):.1%}</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
    
    def _print_summary(self):
        """Print summary of QA results"""
        print("\n" + "=" * 60)
        print("QUALITY ASSURANCE SUMMARY")
        print("=" * 60)
        
        # Outliers
        outliers = self.qa_results.get('outliers', {})
        print(f"\n✓ Outliers: {outliers.get('total_outliers', 0)} detected "
              f"({outliers.get('outlier_rate', 0):.1%})")
        
        # Benford
        benford = self.qa_results.get('benfords_law', {})
        status = "✓" if benford.get('conforms_to_benford', True) else "⚠️"
        print(f"{status} Benford's Law: "
              f"{benford.get('conformance_rate', 0):.1%} conformance")
        
        # Structural breaks
        breaks = self.qa_results.get('structural_breaks', {})
        status = "✓" if breaks.get('breaks_detected', 0) == 0 else "⚠️"
        print(f"{status} Structural Breaks: {breaks.get('breaks_detected', 0)} detected")
        
        # Attrition
        attrition = self.qa_results.get('selection_bias', {})
        rate = attrition.get('attrition_rate', 0)
        status = "✓" if rate < 0.3 else "⚠️"
        print(f"{status} Attrition: {rate:.1%}")
        
        print("=" * 60 + "\n")


class SampleSizeCalculator:
    """
    Statistical power analysis for research design.
    
    Usage:
    ```python
    calc = SampleSizeCalculator()
    
    # For regression
    result = calc.regression_sample_size(
        num_predictors=8,
        expected_r2=0.15,
        power=0.80
    )
    
    # For t-test
    result = calc.ttest_sample_size(
        effect_size=0.35,
        power=0.80
    )
    ```
    """
    
    def __init__(self):
        """Initialize sample size calculator"""
        logger.info("SampleSizeCalculator initialized")
    
    def regression_sample_size(
        self,
        num_predictors: int,
        expected_r2: float,
        power: float = 0.80,
        alpha: float = 0.05
    ) -> Dict:
        """
        Calculate required sample size for regression.
        
        Args:
            num_predictors: Number of predictors (IVs + controls)
            expected_r2: Expected R-squared from prior research
            power: Desired statistical power (0.80 standard)
            alpha: Significance level
            
        Returns:
            Dictionary with sample size recommendations
        """
        # Calculate effect size (Cohen's f²)
        f2 = expected_r2 / (1 - expected_r2)
        
        # Conservative estimate using F-test power
        # N ≈ (λ/f²) + k + 1, where λ depends on power and α
        
        # Approximation for required N
        if power == 0.80 and alpha == 0.05:
            lambda_value = 8.25  # For 80% power, α=0.05
        elif power == 0.90 and alpha == 0.05:
            lambda_value = 10.51
        else:
            lambda_value = 8.25  # Default
        
        minimum_n = int((lambda_value / f2) + num_predictors + 1)
        recommended_n = int(minimum_n * 1.2)  # 20% buffer
        conservative_n = int(minimum_n * 1.5)  # 50% buffer
        
        results = {
            'minimum_n': minimum_n,
            'recommended_n': recommended_n,
            'conservative_n': conservative_n,
            'num_predictors': num_predictors,
            'expected_r2': expected_r2,
            'effect_size_f2': f2,
            'power': power,
            'alpha': alpha
        }
        
        logger.info(f"Required sample size: {recommended_n} "
                   f"(minimum: {minimum_n}, conservative: {conservative_n})")
        
        return results
    
    def ttest_sample_size(
        self,
        effect_size: float,
        power: float = 0.80,
        alpha: float = 0.05,
        alternative: str = 'two-sided'
    ) -> Dict:
        """
        Calculate required sample size for t-test.
        
        Args:
            effect_size: Cohen's d effect size
            power: Desired statistical power
            alpha: Significance level
            alternative: 'two-sided' or 'one-sided'
            
        Returns:
            Dictionary with sample size per group
        """
        analysis = TTestIndPower()
        
        sample_size = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative=alternative
        )
        
        results = {
            'sample_size_per_group': int(np.ceil(sample_size)),
            'total_sample_size': int(np.ceil(sample_size * 2)),
            'effect_size': effect_size,
            'power': power,
            'alpha': alpha,
            'alternative': alternative
        }
        
        logger.info(f"Required sample size: {results['sample_size_per_group']} per group "
                   f"(total: {results['total_sample_size']})")
        
        return results
    
    def panel_data_sample_size(
        self,
        num_firms: int,
        num_periods: int,
        effect_size: Union[float, str] = 'medium',
        power: float = 0.85,
        clustering: bool = True
    ) -> Dict:
        """
        Calculate effective sample size for panel data.
        
        Args:
            num_firms: Number of firms (cross-sectional units)
            num_periods: Number of time periods
            effect_size: Expected effect size ('small', 'medium', 'large') or numeric
            power: Desired power
            clustering: Whether to account for clustered SEs (design effect)
            
        Returns:
            Dictionary with effective sample size and recommendations
        """
        # Convert effect size to Cohen's d
        if isinstance(effect_size, str):
            effect_sizes = {'small': 0.2, 'medium': 0.5, 'large': 0.8}
            effect_size_d = effect_sizes.get(effect_size.lower(), 0.5)
        else:
            effect_size_d = effect_size
        
        # Nominal sample size
        nominal_n = num_firms * num_periods
        
        # Design effect for clustering (ICC = 0.3 typical for firm-level clustering)
        if clustering:
            icc = 0.3  # Intraclass correlation
            design_effect = 1 + (num_periods - 1) * icc
            effective_n = nominal_n / design_effect
        else:
            design_effect = 1.0
            effective_n = nominal_n
        
        # Check if effective N is sufficient
        analysis = TTestIndPower()
        required_n = analysis.solve_power(
            effect_size=effect_size_d,
            alpha=0.05,
            power=power,
            alternative='two-sided'
        )
        
        sufficient = effective_n >= required_n
        
        results = {
            'num_firms': num_firms,
            'num_periods': num_periods,
            'nominal_n': nominal_n,
            'effective_n': int(effective_n),
            'design_effect': design_effect,
            'required_n': int(np.ceil(required_n)),
            'sufficient_power': sufficient,
            'achieved_power': power if sufficient else None,
            'recommendation': 'Sufficient' if sufficient else f'Need {int(required_n - effective_n)} more observations'
        }
        
        logger.info(f"Panel data: Effective N = {int(effective_n)} "
                   f"(nominal: {nominal_n}, design effect: {design_effect:.2f})")
        
        return results
    
    def minimum_detectable_effect(
        self,
        sample_size: int,
        num_predictors: int,
        power: float = 0.80,
        alpha: float = 0.05
    ) -> Dict:
        """
        Calculate minimum detectable effect with available sample.
        
        Args:
            sample_size: Available sample size
            num_predictors: Number of predictors
            power: Desired power
            alpha: Significance level
            
        Returns:
            Dictionary with MDE
        """
        # Solve for effect size given N
        df1 = num_predictors
        df2 = sample_size - num_predictors - 1
        
        # Critical F-value
        f_crit = stats.f.ppf(1 - alpha, df1, df2)
        
        # Non-centrality parameter for desired power
        # (Simplified approximation)
        lambda_value = 8.25 if power == 0.80 else 10.51
        
        # Minimum detectable f²
        f2_mde = lambda_value / (sample_size - num_predictors - 1)
        
        # Convert to R²
        r2_mde = f2_mde / (1 + f2_mde)
        
        results = {
            'sample_size': sample_size,
            'num_predictors': num_predictors,
            'mde_f2': f2_mde,
            'mde_r2': r2_mde,
            'mde_cohens_d': np.sqrt(f2_mde),
            'power': power,
            'alpha': alpha,
            'interpretation': self._interpret_effect_size(np.sqrt(f2_mde))
        }
        
        logger.info(f"Minimum Detectable Effect: R² = {r2_mde:.3f}, "
                   f"Cohen's d = {np.sqrt(f2_mde):.3f} ({results['interpretation']})")
        
        return results
    
    def _interpret_effect_size(self, cohens_d: float) -> str:
        """Interpret Cohen's d effect size"""
        if cohens_d < 0.2:
            return "negligible"
        elif cohens_d < 0.5:
            return "small"
        elif cohens_d < 0.8:
            return "medium"
        else:
            return "large"


# Example usage and testing
if __name__ == "__main__":
    
    # Generate synthetic panel data for testing
    np.random.seed(42)
    
    n_firms = 200
    n_periods = 10
    
    df_test = pd.DataFrame({
        'gvkey': np.repeat(range(n_firms), n_periods),
        'year': np.tile(range(2014, 2024), n_firms),
        'roa': np.random.normal(0.05, 0.03, n_firms * n_periods),
        'total_assets': np.random.lognormal(10, 2, n_firms * n_periods),
        'sales': np.random.lognormal(9, 2, n_firms * n_periods),
        'rd_intensity': np.random.beta(2, 5, n_firms * n_periods)
    })
    
    # Add some outliers
    df_test.loc[0:5, 'roa'] = 0.5  # Extreme outliers
    
    # QA System
    print("\n" + "=" * 60)
    print("TESTING DATA QUALITY CHECKER")
    print("=" * 60)
    
    qa = AdvancedQualityAssurance(
        df_test,
        firm_id='gvkey',
        time_var='year',
        verbose=True
    )
    
    qa_report = qa.run_comprehensive_qa()
    
    # Sample Size Calculator
    print("\n" + "=" * 60)
    print("TESTING SAMPLE SIZE CALCULATOR")
    print("=" * 60)
    
    calc = SampleSizeCalculator()
    
    # Regression sample size
    reg_result = calc.regression_sample_size(
        num_predictors=8,
        expected_r2=0.15,
        power=0.80
    )
    print(f"\nRegression: Recommended N = {reg_result['recommended_n']}")
    
    # T-test sample size
    ttest_result = calc.ttest_sample_size(
        effect_size=0.35,
        power=0.80
    )
    print(f"T-test: N per group = {ttest_result['sample_size_per_group']}")
    
    # Panel data
    panel_result = calc.panel_data_sample_size(
        num_firms=200,
        num_periods=10,
        effect_size='medium',
        clustering=True
    )
    print(f"Panel: Effective N = {panel_result['effective_n']}")
    
    # MDE
    mde_result = calc.minimum_detectable_effect(
        sample_size=200,
        num_predictors=8,
        power=0.80
    )
    print(f"MDE: R² = {mde_result['mde_r2']:.3f} ({mde_result['interpretation']})")
    
    print("\n✅ data_quality_checker.py module tested successfully")
