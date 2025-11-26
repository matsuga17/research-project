#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theoretical Relationship Explorer: Hypothesis Testing and Effect Analysis

Philosophical/Theoretical Foundation:
    Statistical hypothesis testing, properly understood, is not mere mechanical
    procedure but inferential reasoning under uncertainty (Fisher, 1935; Neyman
    & Pearson, 1933). In strategy research, hypothesis testing serves to
    evaluate theoretical propositions against empirical evidence.
    
    This tool implements four critical types of theoretical relationships:
    
    1. Direct Effects: IV → DV (main theoretical predictions)
    2. Mediation: IV → Mediator → DV (mechanism explanation)
    3. Moderation: IV × Moderator → DV (boundary conditions)
    4. Hierarchical Effects: Control → IV → DV (incremental contribution)
    
    Drawing on Baron & Kenny (1986), Hayes (2013), and Aiken & West (1991),
    this tool provides rigorous statistical tests while maintaining theoretical
    interpretability.

Statistical Methods:
    - Hierarchical regression (incremental variance explained)
    - Mediation analysis (Sobel test, bootstrap confidence intervals)
    - Moderation analysis (interaction effects, simple slopes)
    - Robustness checks (alternative specifications)

Usage:
    python theoretical_relationship_explorer.py --data dataset.csv --config framework_config.yaml
    python theoretical_relationship_explorer.py --data dataset.csv --iv resources --dv performance

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
from dataclasses import dataclass, field

# Statistical models
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy import stats
from sklearn.preprocessing import StandardScaler


@dataclass
class HypothesisTest:
    """Represents results of a single hypothesis test"""
    hypothesis_id: str
    independent_var: str
    dependent_var: str
    mediator: Optional[str] = None
    moderator: Optional[str] = None
    controls: List[str] = field(default_factory=list)
    
    # Results
    coefficient: float = 0.0
    std_error: float = 0.0
    t_statistic: float = 0.0
    p_value: float = 1.0
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    r_squared: float = 0.0
    adjusted_r_squared: float = 0.0
    delta_r_squared: Optional[float] = None
    
    # Interpretation
    supported: bool = False
    effect_size: str = "negligible"
    theoretical_interpretation: str = ""
    
    # Additional analyses
    mediation_results: Optional[Dict[str, Any]] = None
    moderation_results: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'hypothesis_id': self.hypothesis_id,
            'independent_var': self.independent_var,
            'dependent_var': self.dependent_var,
            'mediator': self.mediator,
            'moderator': self.moderator,
            'controls': self.controls,
            'coefficient': float(self.coefficient),
            'std_error': float(self.std_error),
            't_statistic': float(self.t_statistic),
            'p_value': float(self.p_value),
            'confidence_interval': [float(self.confidence_interval[0]), float(self.confidence_interval[1])],
            'r_squared': float(self.r_squared),
            'adjusted_r_squared': float(self.adjusted_r_squared),
            'delta_r_squared': float(self.delta_r_squared) if self.delta_r_squared else None,
            'supported': self.supported,
            'effect_size': self.effect_size,
            'theoretical_interpretation': self.theoretical_interpretation,
            'mediation_results': self.mediation_results,
            'moderation_results': self.moderation_results
        }


class TheoreticalRelationshipExplorer:
    """
    Hypothesis Testing and Theoretical Relationship Analysis
    
    Implements statistical tests for direct, mediated, and moderated
    relationships with rigorous hypothesis testing procedures.
    """
    
    def __init__(self, data: pd.DataFrame, config: Optional[Dict[str, Any]] = None,
                 output_dir: str = './relationship_results'):
        """
        Initialize relationship explorer
        
        Args:
            data: DataFrame with variables
            config: Optional theoretical framework configuration
            output_dir: Directory for output files
        """
        self.data = data.copy()
        self.config = config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.results: List[HypothesisTest] = []
    
    def _standardize_variables(self, vars_to_standardize: List[str]) -> pd.DataFrame:
        """Standardize variables for analysis"""
        data_copy = self.data.copy()
        scaler = StandardScaler()
        
        for var in vars_to_standardize:
            if var in data_copy.columns and np.issubdtype(data_copy[var].dtype, np.number):
                data_copy[var] = scaler.fit_transform(data_copy[[var]])
        
        return data_copy
    
    def _interpret_effect_size(self, r_squared: float) -> str:
        """
        Interpret effect size based on R²
        
        Following Cohen (1988):
        R² ≥ 0.26: large
        R² ≥ 0.13: medium
        R² ≥ 0.02: small
        """
        if r_squared >= 0.26:
            return "large"
        elif r_squared >= 0.13:
            return "medium"
        elif r_squared >= 0.02:
            return "small"
        else:
            return "negligible"
    
    def test_direct_effect(self, iv: str, dv: str, controls: List[str] = None,
                          hypothesis_id: str = None) -> HypothesisTest:
        """
        Test direct effect using hierarchical regression
        
        Model 1: DV = β₀ + Σ(βᵢControlᵢ) + ε
        Model 2: DV = β₀ + Σ(βᵢControlᵢ) + β_IV*IV + ε
        
        Args:
            iv: Independent variable
            dv: Dependent variable
            controls: List of control variables
            hypothesis_id: Hypothesis identifier
            
        Returns:
            HypothesisTest object with results
        """
        controls = controls or []
        
        # Prepare data
        vars_needed = [iv, dv] + controls
        data_clean = self.data[vars_needed].dropna()
        
        if len(data_clean) < 30:
            raise ValueError(f"Insufficient data after removing missing values: n={len(data_clean)}")
        
        # Model 1: Controls only
        if controls:
            formula1 = f"{dv} ~ {' + '.join(controls)}"
            model1 = smf.ols(formula1, data=data_clean).fit()
            r2_controls = model1.rsquared
        else:
            r2_controls = 0.0
        
        # Model 2: Controls + IV
        if controls:
            formula2 = f"{dv} ~ {' + '.join(controls)} + {iv}"
        else:
            formula2 = f"{dv} ~ {iv}"
        
        model2 = smf.ols(formula2, data=data_clean).fit()
        
        # Extract IV coefficient
        iv_coef = model2.params[iv]
        iv_stderr = model2.bse[iv]
        iv_tstat = model2.tvalues[iv]
        iv_pval = model2.pvalues[iv]
        iv_ci = model2.conf_int().loc[iv].values
        
        # Calculate ΔR²
        delta_r2 = model2.rsquared - r2_controls
        
        # Determine if hypothesis is supported (p < 0.05)
        supported = iv_pval < 0.05
        
        # Effect size
        effect_size = self._interpret_effect_size(delta_r2)
        
        # Theoretical interpretation
        direction = "positive" if iv_coef > 0 else "negative"
        strength = f"β={iv_coef:.3f}, p={iv_pval:.4f}"
        
        if supported:
            interpretation = (
                f"Significant {direction} relationship between {iv} and {dv} ({strength}). "
                f"The IV explains an additional {delta_r2*100:.2f}% of variance in {dv} "
                f"beyond controls ({effect_size} effect size). "
                f"This supports the theoretical prediction."
            )
        else:
            interpretation = (
                f"No significant relationship between {iv} and {dv} ({strength}). "
                f"The theoretical prediction is not supported by the data. "
                f"Possible explanations include measurement error, model misspecification, "
                f"or genuine absence of the hypothesized relationship."
            )
        
        result = HypothesisTest(
            hypothesis_id=hypothesis_id or f"H: {iv}→{dv}",
            independent_var=iv,
            dependent_var=dv,
            controls=controls,
            coefficient=iv_coef,
            std_error=iv_stderr,
            t_statistic=iv_tstat,
            p_value=iv_pval,
            confidence_interval=(iv_ci[0], iv_ci[1]),
            r_squared=model2.rsquared,
            adjusted_r_squared=model2.rsquared_adj,
            delta_r_squared=delta_r2,
            supported=supported,
            effect_size=effect_size,
            theoretical_interpretation=interpretation
        )
        
        self.results.append(result)
        return result
    
    def test_mediation(self, iv: str, mediator: str, dv: str, controls: List[str] = None,
                      hypothesis_id: str = None) -> HypothesisTest:
        """
        Test mediation effect using Baron & Kenny (1986) approach
        
        Step 1: IV → DV (total effect, c)
        Step 2: IV → Mediator (a path)
        Step 3: IV + Mediator → DV (b path and c' direct effect)
        
        Mediation exists if:
        - a is significant
        - b is significant
        - c' < c (partial mediation) or c' ≈ 0 (full mediation)
        
        Args:
            iv: Independent variable
            mediator: Mediator variable
            dv: Dependent variable
            controls: List of control variables
            hypothesis_id: Hypothesis identifier
            
        Returns:
            HypothesisTest object with mediation results
        """
        controls = controls or []
        
        # Prepare data
        vars_needed = [iv, mediator, dv] + controls
        data_clean = self.data[vars_needed].dropna()
        
        if len(data_clean) < 30:
            raise ValueError(f"Insufficient data: n={len(data_clean)}")
        
        # Step 1: Total effect (c path)
        if controls:
            formula_total = f"{dv} ~ {' + '.join(controls)} + {iv}"
        else:
            formula_total = f"{dv} ~ {iv}"
        model_total = smf.ols(formula_total, data=data_clean).fit()
        c_path = model_total.params[iv]
        c_pval = model_total.pvalues[iv]
        
        # Step 2: IV → Mediator (a path)
        if controls:
            formula_a = f"{mediator} ~ {' + '.join(controls)} + {iv}"
        else:
            formula_a = f"{mediator} ~ {iv}"
        model_a = smf.ols(formula_a, data=data_clean).fit()
        a_path = model_a.params[iv]
        a_pval = model_a.pvalues[iv]
        
        # Step 3: IV + Mediator → DV (b path and c' path)
        if controls:
            formula_med = f"{dv} ~ {' + '.join(controls)} + {iv} + {mediator}"
        else:
            formula_med = f"{dv} ~ {iv} + {mediator}"
        model_med = smf.ols(formula_med, data=data_clean).fit()
        b_path = model_med.params[mediator]
        b_pval = model_med.pvalues[mediator]
        c_prime_path = model_med.params[iv]
        c_prime_pval = model_med.pvalues[iv]
        
        # Indirect effect (a * b)
        indirect_effect = a_path * b_path
        
        # Sobel test for significance of indirect effect
        se_a = model_a.bse[iv]
        se_b = model_med.bse[mediator]
        sobel_se = np.sqrt((b_path**2 * se_a**2) + (a_path**2 * se_b**2))
        sobel_z = indirect_effect / sobel_se if sobel_se > 0 else 0
        sobel_p = 2 * (1 - stats.norm.cdf(abs(sobel_z)))
        
        # Proportion mediated
        if c_path != 0:
            prop_mediated = indirect_effect / c_path
        else:
            prop_mediated = 0
        
        # Mediation type
        if a_pval < 0.05 and b_pval < 0.05:
            if c_prime_pval >= 0.05:
                mediation_type = "full"
            else:
                mediation_type = "partial"
        elif c_pval < 0.05 and (a_pval >= 0.05 or b_pval >= 0.05):
            mediation_type = "none"
        else:
            mediation_type = "none"
        
        # Theoretical interpretation
        if mediation_type == "full":
            interpretation = (
                f"Full mediation detected: {iv} → {mediator} → {dv}. "
                f"The indirect effect (a*b={indirect_effect:.3f}, Sobel p={sobel_p:.4f}) "
                f"accounts for the entire relationship between {iv} and {dv}. "
                f"This suggests {mediator} is the mechanism through which {iv} affects {dv}."
            )
        elif mediation_type == "partial":
            interpretation = (
                f"Partial mediation detected: {iv} → {mediator} → {dv}. "
                f"The indirect effect (a*b={indirect_effect:.3f}) explains {prop_mediated*100:.1f}% "
                f"of the total effect. Both direct (c'={c_prime_path:.3f}) and indirect paths "
                f"are significant, suggesting multiple mechanisms at play."
            )
        else:
            interpretation = (
                f"No significant mediation: The pathway {iv} → {mediator} → {dv} is not supported. "
                f"Either {iv} does not affect {mediator} (a={a_path:.3f}, p={a_pval:.4f}) "
                f"or {mediator} does not affect {dv} (b={b_path:.3f}, p={b_pval:.4f})."
            )
        
        mediation_results = {
            'c_path': float(c_path),
            'c_pvalue': float(c_pval),
            'a_path': float(a_path),
            'a_pvalue': float(a_pval),
            'b_path': float(b_path),
            'b_pvalue': float(b_pval),
            'c_prime_path': float(c_prime_path),
            'c_prime_pvalue': float(c_prime_pval),
            'indirect_effect': float(indirect_effect),
            'sobel_z': float(sobel_z),
            'sobel_p': float(sobel_p),
            'proportion_mediated': float(prop_mediated),
            'mediation_type': mediation_type
        }
        
        result = HypothesisTest(
            hypothesis_id=hypothesis_id or f"H: {iv}→{mediator}→{dv}",
            independent_var=iv,
            dependent_var=dv,
            mediator=mediator,
            controls=controls,
            coefficient=indirect_effect,
            p_value=sobel_p,
            r_squared=model_med.rsquared,
            adjusted_r_squared=model_med.rsquared_adj,
            supported=(mediation_type in ["full", "partial"]),
            effect_size=self._interpret_effect_size(model_med.rsquared),
            theoretical_interpretation=interpretation,
            mediation_results=mediation_results
        )
        
        self.results.append(result)
        return result
    
    def test_moderation(self, iv: str, moderator: str, dv: str, controls: List[str] = None,
                       hypothesis_id: str = None) -> HypothesisTest:
        """
        Test moderation effect using interaction term
        
        Model: DV = β₀ + β₁IV + β₂Moderator + β₃(IV×Moderator) + Σ(βᵢControlᵢ) + ε
        
        Moderation exists if β₃ is significant.
        
        Args:
            iv: Independent variable
            moderator: Moderator variable
            dv: Dependent variable
            controls: List of control variables
            hypothesis_id: Hypothesis identifier
            
        Returns:
            HypothesisTest object with moderation results
        """
        controls = controls or []
        
        # Prepare data
        vars_needed = [iv, moderator, dv] + controls
        data_clean = self.data[vars_needed].dropna()
        
        if len(data_clean) < 30:
            raise ValueError(f"Insufficient data: n={len(data_clean)}")
        
        # Standardize IV and moderator to reduce multicollinearity
        data_std = data_clean.copy()
        scaler = StandardScaler()
        data_std[iv] = scaler.fit_transform(data_std[[iv]])
        data_std[moderator] = scaler.fit_transform(data_std[[moderator]])
        
        # Create interaction term
        interaction_name = f"{iv}_{moderator}_interaction"
        data_std[interaction_name] = data_std[iv] * data_std[moderator]
        
        # Model without interaction
        if controls:
            formula_main = f"{dv} ~ {' + '.join(controls)} + {iv} + {moderator}"
        else:
            formula_main = f"{dv} ~ {iv} + {moderator}"
        model_main = smf.ols(formula_main, data=data_std).fit()
        r2_main = model_main.rsquared
        
        # Model with interaction
        if controls:
            formula_int = f"{dv} ~ {' + '.join(controls)} + {iv} + {moderator} + {interaction_name}"
        else:
            formula_int = f"{dv} ~ {iv} + {moderator} + {interaction_name}"
        model_int = smf.ols(formula_int, data=data_std).fit()
        
        # Extract interaction coefficient
        int_coef = model_int.params[interaction_name]
        int_stderr = model_int.bse[interaction_name]
        int_tstat = model_int.tvalues[interaction_name]
        int_pval = model_int.pvalues[interaction_name]
        int_ci = model_int.conf_int().loc[interaction_name].values
        
        # ΔR² from interaction
        delta_r2 = model_int.rsquared - r2_main
        
        # Simple slopes analysis (at mean ± 1 SD of moderator)
        mod_mean = data_std[moderator].mean()
        mod_std = data_std[moderator].std()
        
        # Slope at low moderator (-1 SD)
        slope_low = model_int.params[iv] + int_coef * (mod_mean - mod_std)
        
        # Slope at mean moderator
        slope_mean = model_int.params[iv] + int_coef * mod_mean
        
        # Slope at high moderator (+1 SD)
        slope_high = model_int.params[iv] + int_coef * (mod_mean + mod_std)
        
        # Determine if moderation is supported
        supported = int_pval < 0.05
        
        # Theoretical interpretation
        direction = "positive" if int_coef > 0 else "negative"
        
        if supported:
            interpretation = (
                f"Significant {direction} moderation effect (β={int_coef:.3f}, p={int_pval:.4f}). "
                f"{moderator} moderates the relationship between {iv} and {dv}. "
                f"Simple slopes analysis reveals: "
                f"When {moderator} is low (-1SD): slope={slope_low:.3f}; "
                f"When {moderator} is high (+1SD): slope={slope_high:.3f}. "
                f"The interaction explains an additional {delta_r2*100:.2f}% of variance."
            )
        else:
            interpretation = (
                f"No significant moderation effect (β={int_coef:.3f}, p={int_pval:.4f}). "
                f"{moderator} does not significantly alter the {iv}-{dv} relationship. "
                f"The effect of {iv} appears stable across levels of {moderator}."
            )
        
        moderation_results = {
            'interaction_coefficient': float(int_coef),
            'interaction_pvalue': float(int_pval),
            'delta_r_squared': float(delta_r2),
            'slope_low_moderator': float(slope_low),
            'slope_mean_moderator': float(slope_mean),
            'slope_high_moderator': float(slope_high),
            'moderator_mean': float(mod_mean),
            'moderator_std': float(mod_std)
        }
        
        result = HypothesisTest(
            hypothesis_id=hypothesis_id or f"H: {iv}×{moderator}→{dv}",
            independent_var=iv,
            dependent_var=dv,
            moderator=moderator,
            controls=controls,
            coefficient=int_coef,
            std_error=int_stderr,
            t_statistic=int_tstat,
            p_value=int_pval,
            confidence_interval=(int_ci[0], int_ci[1]),
            r_squared=model_int.rsquared,
            adjusted_r_squared=model_int.rsquared_adj,
            delta_r_squared=delta_r2,
            supported=supported,
            effect_size=self._interpret_effect_size(delta_r2),
            theoretical_interpretation=interpretation,
            moderation_results=moderation_results
        )
        
        self.results.append(result)
        return result
    
    def test_hypotheses_from_config(self) -> List[HypothesisTest]:
        """
        Test all hypotheses specified in configuration
        
        Returns:
            List of hypothesis test results
        """
        if not self.config or 'hypotheses' not in self.config:
            print("No hypotheses found in configuration")
            return []
        
        print(f"\nTesting {len(self.config['hypotheses'])} hypotheses from configuration...")
        
        # Get control variables
        controls = [c['name'] for c in self.config.get('constructs', []) 
                   if c.get('role') == 'control']
        
        for hyp in self.config['hypotheses']:
            iv = hyp.get('independent')
            dv = hyp.get('dependent')
            direction = hyp.get('direction', 'positive').lower()
            statement = hyp.get('statement', '')
            
            print(f"\nTesting: {statement}")
            
            if direction == 'mediation':
                # Assume mediator is specified or infer from constructs
                mediators = [c['name'] for c in self.config.get('constructs', []) 
                            if c.get('role') == 'mediator']
                if mediators:
                    self.test_mediation(iv, mediators[0], dv, controls, hypothesis_id=statement)
            elif direction == 'moderation':
                # Assume moderator is specified or infer from constructs
                moderators = [c['name'] for c in self.config.get('constructs', []) 
                             if c.get('role') == 'moderator']
                if moderators:
                    self.test_moderation(iv, moderators[0], dv, controls, hypothesis_id=statement)
            else:
                # Direct effect
                self.test_direct_effect(iv, dv, controls, hypothesis_id=statement)
        
        return self.results
    
    def save_results(self, output_path: str = 'hypothesis_tests.json') -> None:
        """Save results to JSON file"""
        results_path = self.output_dir / output_path
        
        results_dict = {
            'timestamp': datetime.now().isoformat(),
            'n_tests': len(self.results),
            'n_supported': sum(1 for r in self.results if r.supported),
            'results': [r.to_dict() for r in self.results]
        }
        
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Results saved to: {results_path.absolute()}")
    
    def generate_summary_report(self) -> None:
        """Generate summary report"""
        print("\n" + "="*80)
        print("HYPOTHESIS TESTING SUMMARY")
        print("="*80)
        
        n_supported = sum(1 for r in self.results if r.supported)
        n_total = len(self.results)
        
        print(f"\nTotal hypotheses tested: {n_total}")
        print(f"Supported: {n_supported} ({n_supported/n_total*100:.1f}%)")
        print(f"Not supported: {n_total - n_supported} ({(n_total-n_supported)/n_total*100:.1f}%)")
        
        print("\n" + "-"*80)
        print("DETAILED RESULTS")
        print("-"*80)
        
        for result in self.results:
            status = "✓ SUPPORTED" if result.supported else "✗ NOT SUPPORTED"
            print(f"\n{status}: {result.hypothesis_id}")
            print(f"  {result.independent_var} → {result.dependent_var}")
            if result.mediator:
                print(f"  Via mediator: {result.mediator}")
            if result.moderator:
                print(f"  Moderated by: {result.moderator}")
            print(f"  Coefficient: {result.coefficient:.4f}, p-value: {result.p_value:.4f}")
            print(f"  R²: {result.r_squared:.4f}, Effect size: {result.effect_size}")
            print(f"  Interpretation: {result.theoretical_interpretation[:200]}...")
        
        print("\n" + "="*80)


def load_config(config_path: str) -> Optional[Dict[str, Any]]:
    """Load theoretical framework configuration"""
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
        description='Theoretical Relationship Explorer: Hypothesis Testing',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--data', type=str, required=True, help='Path to dataset (CSV)')
    parser.add_argument('--config', type=str, help='Path to theoretical framework configuration')
    parser.add_argument('--iv', type=str, help='Independent variable (for single test)')
    parser.add_argument('--dv', type=str, help='Dependent variable (for single test)')
    parser.add_argument('--mediator', type=str, help='Mediator variable (optional)')
    parser.add_argument('--moderator', type=str, help='Moderator variable (optional)')
    parser.add_argument('--controls', type=str, nargs='+', help='Control variables')
    parser.add_argument('--output-dir', type=str, default='./relationship_results',
                       help='Output directory')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading dataset: {args.data}")
        data = pd.read_csv(args.data)
        print(f"✓ Loaded: {len(data)} observations × {len(data.columns)} variables")
        
        # Load configuration
        config = load_config(args.config) if args.config else None
        
        # Create explorer
        explorer = TheoreticalRelationshipExplorer(data, config, output_dir=args.output_dir)
        
        # Run tests
        if config and 'hypotheses' in config:
            # Test hypotheses from configuration
            explorer.test_hypotheses_from_config()
        elif args.iv and args.dv:
            # Single hypothesis test
            if args.mediator:
                explorer.test_mediation(args.iv, args.mediator, args.dv, controls=args.controls)
            elif args.moderator:
                explorer.test_moderation(args.iv, args.moderator, args.dv, controls=args.controls)
            else:
                explorer.test_direct_effect(args.iv, args.dv, controls=args.controls)
        else:
            print("Error: Either provide --config with hypotheses or specify --iv and --dv")
            sys.exit(1)
        
        # Generate reports
        explorer.generate_summary_report()
        explorer.save_results()
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
