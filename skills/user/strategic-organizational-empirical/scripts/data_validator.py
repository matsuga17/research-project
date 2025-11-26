#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Validator: Multi-Layered Data Quality Assessment System

Philosophical/Theoretical Foundation:
    Data validation is not merely a technical procedure but an epistemological
    necessity. Following Popper's (1959) falsificationist logic, empirical research
    requires data that can genuinely test theoretical propositions. Invalid or
    unreliable data undermines the entire inferential chain from theory to evidence.
    
    This validator implements a three-tier validation framework:
    1. Data Integrity Layer: Technical completeness and consistency
    2. Theoretical Consistency Layer: Alignment with theoretical expectations
    3. Statistical Assumptions Layer: Preconditions for valid inference
    
    Drawing on measurement theory (Stevens, 1946; Messick, 1989) and statistical
    philosophy (Fisher, 1935; Neyman, 1950), this tool ensures that data meet
    the minimum quality standards for rigorous empirical research.

Validation Levels:
    Level 1 - CRITICAL: Data cannot be analyzed without fixing these issues
    Level 2 - WARNING: Analysis possible but results may be compromised
    Level 3 - ADVISORY: Best practices for optimal analysis quality

Usage:
    python data_validator.py --data dataset.csv --config framework_config.yaml
    python data_validator.py --data dataset.csv --quick-check

Author: Strategic Research Lab
License: MIT
Version: 1.0.0
Date: 2025-11-08
"""

import pandas as pd
import numpy as np
import yaml
import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

# Statistical tests
from scipy import stats
from scipy.stats import shapiro, levene, jarque_bera, normaltest
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan


class ValidationLevel(Enum):
    """Validation severity levels"""
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    ADVISORY = "ADVISORY"
    INFO = "INFO"


@dataclass
class ValidationIssue:
    """Represents a single validation issue"""
    level: ValidationLevel
    category: str
    variable: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    recommendation: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'level': self.level.value,
            'category': self.category,
            'variable': self.variable,
            'message': self.message,
            'details': self.details,
            'recommendation': self.recommendation
        }


@dataclass
class ValidationReport:
    """Complete validation report"""
    timestamp: str
    dataset_info: Dict[str, Any]
    validation_summary: Dict[str, int]
    issues: List[ValidationIssue] = field(default_factory=list)
    passed_checks: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp,
            'dataset_info': self.dataset_info,
            'validation_summary': self.validation_summary,
            'issues': [issue.to_dict() for issue in self.issues],
            'passed_checks': self.passed_checks,
            'recommendations': self.recommendations
        }
    
    def get_issues_by_level(self, level: ValidationLevel) -> List[ValidationIssue]:
        """Get issues filtered by level"""
        return [issue for issue in self.issues if issue.level == level]


class DataValidator:
    """
    Multi-Layered Data Validation System
    
    Implements comprehensive validation across three epistemological layers:
    1. Data Integrity (completeness, consistency, range)
    2. Theoretical Consistency (construct validity, expected patterns)
    3. Statistical Assumptions (normality, homoscedasticity, multicollinearity)
    """
    
    def __init__(self, data: pd.DataFrame, config: Optional[Dict[str, Any]] = None):
        """
        Initialize validator
        
        Args:
            data: DataFrame to validate
            config: Optional theoretical framework configuration
        """
        self.data = data.copy()
        self.config = config
        self.report = ValidationReport(
            timestamp=datetime.now().isoformat(),
            dataset_info=self._get_dataset_info(),
            validation_summary={'CRITICAL': 0, 'WARNING': 0, 'ADVISORY': 0, 'INFO': 0}
        )
    
    def _get_dataset_info(self) -> Dict[str, Any]:
        """Get basic dataset information"""
        return {
            'n_observations': len(self.data),
            'n_variables': len(self.data.columns),
            'variables': list(self.data.columns),
            'memory_usage_mb': self.data.memory_usage(deep=True).sum() / 1024**2,
            'dtypes': self.data.dtypes.astype(str).to_dict()
        }
    
    def _add_issue(self, level: ValidationLevel, category: str, variable: Optional[str],
                   message: str, details: Dict[str, Any] = None, recommendation: str = None):
        """Add validation issue to report"""
        issue = ValidationIssue(
            level=level,
            category=category,
            variable=variable,
            message=message,
            details=details or {},
            recommendation=recommendation
        )
        self.report.issues.append(issue)
        self.report.validation_summary[level.value] += 1
    
    def _add_passed_check(self, check: str):
        """Add passed validation check"""
        self.report.passed_checks.append(check)
    
    # ========================================================================
    # LAYER 1: DATA INTEGRITY VALIDATION
    # ========================================================================
    
    def validate_missing_data(self) -> None:
        """
        Validate missing data patterns
        
        Philosophical note: Missing data is not merely a technical inconvenience
        but potentially a substantive phenomenon (Little & Rubin, 2002). The
        pattern of missingness may be informative about underlying processes.
        """
        missing_counts = self.data.isnull().sum()
        missing_pct = (missing_counts / len(self.data)) * 100
        
        for var in self.data.columns:
            if missing_counts[var] == 0:
                continue
            
            pct = missing_pct[var]
            
            if pct > 50:
                self._add_issue(
                    level=ValidationLevel.CRITICAL,
                    category="Missing Data",
                    variable=var,
                    message=f"Excessive missing data: {pct:.1f}%",
                    details={'missing_count': int(missing_counts[var]), 'missing_pct': float(pct)},
                    recommendation="Consider excluding this variable or using multiple imputation if theoretically justified"
                )
            elif pct > 20:
                self._add_issue(
                    level=ValidationLevel.WARNING,
                    category="Missing Data",
                    variable=var,
                    message=f"Substantial missing data: {pct:.1f}%",
                    details={'missing_count': int(missing_counts[var]), 'missing_pct': float(pct)},
                    recommendation="Investigate missingness mechanism (MCAR, MAR, MNAR) and consider imputation"
                )
            elif pct > 5:
                self._add_issue(
                    level=ValidationLevel.ADVISORY,
                    category="Missing Data",
                    variable=var,
                    message=f"Notable missing data: {pct:.1f}%",
                    details={'missing_count': int(missing_counts[var]), 'missing_pct': float(pct)},
                    recommendation="Document handling strategy (listwise deletion, imputation)"
                )
        
        if missing_counts.sum() == 0:
            self._add_passed_check("Missing data: No missing values detected")
    
    def validate_duplicates(self) -> None:
        """Validate duplicate observations"""
        duplicates = self.data.duplicated().sum()
        
        if duplicates > 0:
            pct = (duplicates / len(self.data)) * 100
            self._add_issue(
                level=ValidationLevel.WARNING,
                category="Data Integrity",
                variable=None,
                message=f"Duplicate observations detected: {duplicates} ({pct:.2f}%)",
                details={'duplicate_count': int(duplicates), 'duplicate_pct': float(pct)},
                recommendation="Investigate source of duplicates and remove if appropriate"
            )
        else:
            self._add_passed_check("Duplicates: No duplicate observations found")
    
    def validate_variable_types(self) -> None:
        """
        Validate variable types and scales of measurement
        
        Following Stevens (1946), we recognize four scales of measurement:
        nominal, ordinal, interval, and ratio. Inappropriate statistical
        operations on wrong scale types lead to meaningless results.
        """
        for var in self.data.columns:
            dtype = self.data[var].dtype
            unique_vals = self.data[var].nunique()
            n_obs = len(self.data[var].dropna())
            
            # Check for suspicious categorical variables stored as numeric
            if np.issubdtype(dtype, np.number):
                if unique_vals < 10 and n_obs > 100:
                    self._add_issue(
                        level=ValidationLevel.ADVISORY,
                        category="Variable Types",
                        variable=var,
                        message=f"Numeric variable with few unique values ({unique_vals})",
                        details={'unique_values': int(unique_vals), 'dtype': str(dtype)},
                        recommendation="Verify if this should be categorical/ordinal"
                    )
            
            # Check for constant variables
            if unique_vals == 1:
                self._add_issue(
                    level=ValidationLevel.WARNING,
                    category="Variable Types",
                    variable=var,
                    message="Constant variable (no variance)",
                    details={'unique_values': 1},
                    recommendation="Consider removing - provides no information"
                )
            
            # Check for near-zero variance
            if np.issubdtype(dtype, np.number):
                variance = self.data[var].var()
                if variance < 1e-10 and variance > 0:
                    self._add_issue(
                        level=ValidationLevel.ADVISORY,
                        category="Variable Types",
                        variable=var,
                        message="Near-zero variance detected",
                        details={'variance': float(variance)},
                        recommendation="May cause numerical instability in analysis"
                    )
    
    def validate_outliers(self, threshold: float = 3.5) -> None:
        """
        Detect outliers using modified Z-score (Iglewicz & Hoaglin, 1993)
        
        Philosophical note: Outliers are not necessarily "errors" but may represent
        genuine extreme values or different populations. Their treatment should
        be theoretically justified.
        
        Args:
            threshold: Modified Z-score threshold (default: 3.5)
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for var in numeric_cols:
            data = self.data[var].dropna()
            if len(data) < 10:
                continue
            
            # Modified Z-score using median absolute deviation
            median = data.median()
            mad = np.median(np.abs(data - median))
            
            if mad == 0:
                continue
            
            modified_z = 0.6745 * (data - median) / mad
            outliers = (np.abs(modified_z) > threshold).sum()
            
            if outliers > 0:
                pct = (outliers / len(data)) * 100
                
                if pct > 5:
                    level = ValidationLevel.WARNING
                elif pct > 1:
                    level = ValidationLevel.ADVISORY
                else:
                    level = ValidationLevel.INFO
                
                self._add_issue(
                    level=level,
                    category="Outliers",
                    variable=var,
                    message=f"Outliers detected: {outliers} ({pct:.2f}%)",
                    details={
                        'outlier_count': int(outliers),
                        'outlier_pct': float(pct),
                        'median': float(median),
                        'mad': float(mad)
                    },
                    recommendation="Investigate outliers - winsorize, transform, or exclude with justification"
                )
    
    def validate_value_ranges(self) -> None:
        """Validate that values are within expected ranges"""
        if not self.config or 'constructs' not in self.config:
            return
        
        for construct in self.config['constructs']:
            var_name = construct.get('name')
            if var_name not in self.data.columns:
                continue
            
            # Check for impossible values (e.g., negative values for inherently positive constructs)
            if construct.get('role') in ['performance', 'size', 'age']:
                negative_count = (self.data[var_name] < 0).sum()
                if negative_count > 0:
                    self._add_issue(
                        level=ValidationLevel.CRITICAL,
                        category="Value Range",
                        variable=var_name,
                        message=f"Negative values in inherently positive variable: {negative_count}",
                        details={'negative_count': int(negative_count)},
                        recommendation="Check data collection/coding errors"
                    )
            
            # Check for Likert-scale range violations
            if construct.get('measurement_type') == 'reflective':
                items = construct.get('items', [])
                # Assume 7-point Likert if items are specified
                if items:
                    min_val = self.data[var_name].min()
                    max_val = self.data[var_name].max()
                    
                    if min_val < 1 or max_val > 7:
                        self._add_issue(
                            level=ValidationLevel.WARNING,
                            category="Value Range",
                            variable=var_name,
                            message=f"Values outside expected Likert range [1-7]: [{min_val}, {max_val}]",
                            details={'min': float(min_val), 'max': float(max_val)},
                            recommendation="Verify scale coding and data entry"
                        )
    
    # ========================================================================
    # LAYER 2: THEORETICAL CONSISTENCY VALIDATION
    # ========================================================================
    
    def validate_construct_presence(self) -> None:
        """Validate that all configured constructs are present in data"""
        if not self.config or 'constructs' not in self.config:
            return
        
        missing_constructs = []
        for construct in self.config['constructs']:
            var_name = construct.get('name')
            if var_name not in self.data.columns:
                missing_constructs.append(var_name)
                self._add_issue(
                    level=ValidationLevel.CRITICAL,
                    category="Theoretical Consistency",
                    variable=var_name,
                    message=f"Configured construct '{var_name}' not found in dataset",
                    details={'construct_role': construct.get('role')},
                    recommendation="Check variable naming or data import process"
                )
        
        if not missing_constructs:
            self._add_passed_check(f"Construct presence: All {len(self.config['constructs'])} constructs found")
    
    def validate_measurement_items(self) -> None:
        """Validate presence of measurement items for multi-item constructs"""
        if not self.config or 'constructs' not in self.config:
            return
        
        for construct in self.config['constructs']:
            items = construct.get('items', [])
            if not items or len(items) <= 1:
                continue
            
            missing_items = [item for item in items if item not in self.data.columns]
            
            if missing_items:
                self._add_issue(
                    level=ValidationLevel.CRITICAL,
                    category="Measurement Items",
                    variable=construct.get('name'),
                    message=f"Missing measurement items: {', '.join(missing_items)}",
                    details={'missing_items': missing_items, 'total_items': len(items)},
                    recommendation="Multi-item constructs require all items for validity assessment"
                )
    
    def validate_expected_correlations(self) -> None:
        """
        Validate theoretically expected correlation patterns
        
        Theoretical note: Constructs within the same theoretical domain
        should exhibit moderate positive correlations. Absence of expected
        correlations may indicate measurement invalidity.
        """
        if not self.config or 'constructs' not in self.config:
            return
        
        # Get independent and dependent variables
        iv_vars = [c['name'] for c in self.config['constructs'] if c.get('role') == 'independent']
        dv_vars = [c['name'] for c in self.config['constructs'] if c.get('role') == 'dependent']
        
        if len(iv_vars) >= 2 and len(dv_vars) >= 1:
            # Check if independent variables show some correlation (not too high, not too low)
            iv_data = self.data[iv_vars].dropna()
            if len(iv_data) > 30:
                corr_matrix = iv_data.corr()
                
                # Check for very low correlations among IVs (might indicate distinct constructs)
                for i in range(len(iv_vars)):
                    for j in range(i+1, len(iv_vars)):
                        corr = abs(corr_matrix.iloc[i, j])
                        
                        if corr < 0.05:
                            self._add_issue(
                                level=ValidationLevel.INFO,
                                category="Theoretical Consistency",
                                variable=f"{iv_vars[i]} - {iv_vars[j]}",
                                message=f"Very low correlation: r = {corr:.3f}",
                                details={'correlation': float(corr)},
                                recommendation="Verify if these are truly independent constructs"
                            )
    
    # ========================================================================
    # LAYER 3: STATISTICAL ASSUMPTIONS VALIDATION
    # ========================================================================
    
    def validate_normality(self, alpha: float = 0.05) -> None:
        """
        Test normality assumption using Shapiro-Wilk and Jarque-Bera tests
        
        Philosophical note: Many parametric tests assume normality, but this
        assumption can be relaxed with large samples (Central Limit Theorem).
        Non-normality may also suggest need for transformation or alternative
        methods.
        
        Args:
            alpha: Significance level for tests
        """
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for var in numeric_cols:
            data = self.data[var].dropna()
            
            if len(data) < 20:
                continue
            
            # Shapiro-Wilk test (better for small samples)
            if len(data) <= 5000:
                stat, p_value = shapiro(data)
                test_name = "Shapiro-Wilk"
            else:
                # Jarque-Bera for large samples
                stat, p_value = jarque_bera(data)
                test_name = "Jarque-Bera"
            
            if p_value < alpha:
                # Calculate skewness and kurtosis for diagnostic
                skewness = stats.skew(data)
                kurtosis_val = stats.kurtosis(data)
                
                # Determine severity based on departure from normality
                if abs(skewness) > 2 or abs(kurtosis_val) > 7:
                    level = ValidationLevel.WARNING
                else:
                    level = ValidationLevel.ADVISORY
                
                self._add_issue(
                    level=level,
                    category="Normality",
                    variable=var,
                    message=f"Significant departure from normality ({test_name}, p={p_value:.4f})",
                    details={
                        'test': test_name,
                        'statistic': float(stat),
                        'p_value': float(p_value),
                        'skewness': float(skewness),
                        'kurtosis': float(kurtosis_val)
                    },
                    recommendation="Consider transformation (log, square root) or robust methods"
                )
    
    def validate_homoscedasticity(self) -> None:
        """
        Test homoscedasticity (equal variance) assumption
        
        Important for: t-tests, ANOVA, regression
        """
        if not self.config or 'constructs' not in self.config:
            return
        
        # Test variance equality across categorical groups if available
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for cat_var in categorical_cols:
            groups = self.data[cat_var].value_counts()
            
            # Only test if 2-5 groups with sufficient observations
            if 2 <= len(groups) <= 5 and groups.min() >= 30:
                for num_var in numeric_cols:
                    group_data = [self.data[self.data[cat_var] == group][num_var].dropna() 
                                 for group in groups.index]
                    
                    if all(len(g) >= 30 for g in group_data):
                        stat, p_value = levene(*group_data)
                        
                        if p_value < 0.05:
                            self._add_issue(
                                level=ValidationLevel.ADVISORY,
                                category="Homoscedasticity",
                                variable=f"{num_var} by {cat_var}",
                                message=f"Unequal variances detected (Levene test, p={p_value:.4f})",
                                details={'statistic': float(stat), 'p_value': float(p_value)},
                                recommendation="Consider robust standard errors or transformation"
                            )
    
    def validate_multicollinearity(self, threshold: float = 10.0) -> None:
        """
        Detect multicollinearity using Variance Inflation Factor (VIF)
        
        VIF > 10 indicates severe multicollinearity
        VIF > 5 indicates moderate multicollinearity
        
        Theoretical note: Multicollinearity doesn't bias coefficients but
        inflates standard errors, making hypothesis tests unreliable.
        
        Args:
            threshold: VIF threshold for concern (default: 10)
        """
        if not self.config or 'constructs' not in self.config:
            return
        
        # Get independent variables
        iv_vars = [c['name'] for c in self.config['constructs'] 
                  if c.get('role') in ['independent', 'control', 'moderator']]
        
        if len(iv_vars) < 2:
            return
        
        # Filter to numeric columns that exist
        iv_vars = [v for v in iv_vars if v in self.data.columns 
                  and np.issubdtype(self.data[v].dtype, np.number)]
        
        if len(iv_vars) < 2:
            return
        
        # Calculate VIF
        data = self.data[iv_vars].dropna()
        
        if len(data) < 30:
            return
        
        vif_data = pd.DataFrame()
        vif_data["Variable"] = iv_vars
        vif_data["VIF"] = [variance_inflation_factor(data.values, i) 
                           for i in range(len(iv_vars))]
        
        for _, row in vif_data.iterrows():
            vif = row['VIF']
            var = row['Variable']
            
            if vif > threshold:
                self._add_issue(
                    level=ValidationLevel.WARNING,
                    category="Multicollinearity",
                    variable=var,
                    message=f"Severe multicollinearity detected: VIF = {vif:.2f}",
                    details={'vif': float(vif)},
                    recommendation="Consider removing variable, combining with correlated variable, or using ridge regression"
                )
            elif vif > 5:
                self._add_issue(
                    level=ValidationLevel.ADVISORY,
                    category="Multicollinearity",
                    variable=var,
                    message=f"Moderate multicollinearity detected: VIF = {vif:.2f}",
                    details={'vif': float(vif)},
                    recommendation="Monitor collinearity but may not require action"
                )
    
    def validate_sample_size(self) -> None:
        """
        Validate adequate sample size for planned analyses
        
        Rules of thumb (Tabachnick & Fidell, 2013):
        - Multiple regression: N > 50 + 8k (k = number of predictors)
        - Factor analysis: N > 300 or 10 observations per variable
        - SEM: N > 200, preferably > 400
        """
        n = len(self.data)
        
        if not self.config or 'constructs' not in self.config:
            # General guidelines
            if n < 30:
                self._add_issue(
                    level=ValidationLevel.CRITICAL,
                    category="Sample Size",
                    variable=None,
                    message=f"Very small sample size: N = {n}",
                    details={'n': n},
                    recommendation="Results may be unreliable - consider collecting more data"
                )
            elif n < 100:
                self._add_issue(
                    level=ValidationLevel.WARNING,
                    category="Sample Size",
                    variable=None,
                    message=f"Small sample size: N = {n}",
                    details={'n': n},
                    recommendation="Limited statistical power - interpret results cautiously"
                )
            return
        
        # Theory-specific guidelines
        n_predictors = len([c for c in self.config['constructs'] 
                           if c.get('role') in ['independent', 'control', 'moderator']])
        
        # Regression rule: N > 50 + 8k
        required_n = 50 + 8 * n_predictors
        
        if n < required_n:
            self._add_issue(
                level=ValidationLevel.WARNING,
                category="Sample Size",
                variable=None,
                message=f"Sample size may be insufficient for regression: N = {n}, required ≈ {required_n}",
                details={'n': n, 'n_predictors': n_predictors, 'required_n': required_n},
                recommendation="Consider reducing number of predictors or collecting more data"
            )
        else:
            self._add_passed_check(f"Sample size adequate for regression: N = {n}")
        
        # SEM rule (if multiple constructs with multiple items)
        multi_item_constructs = [c for c in self.config['constructs'] 
                                if len(c.get('items', [])) > 1]
        if len(multi_item_constructs) >= 3 and n < 200:
            self._add_issue(
                level=ValidationLevel.WARNING,
                category="Sample Size",
                variable=None,
                message=f"Sample size may be insufficient for SEM: N = {n}, recommended > 200",
                details={'n': n},
                recommendation="SEM with small samples requires cautious interpretation"
            )
    
    # ========================================================================
    # VALIDATION EXECUTION AND REPORTING
    # ========================================================================
    
    def run_all_validations(self, quick_check: bool = False) -> ValidationReport:
        """
        Run all validation checks
        
        Args:
            quick_check: If True, skip time-consuming checks
            
        Returns:
            Complete validation report
        """
        print("Running data validation...")
        print(f"Dataset: {len(self.data)} observations × {len(self.data.columns)} variables")
        print()
        
        # Layer 1: Data Integrity
        print("[1/3] Data Integrity Layer")
        self.validate_missing_data()
        self.validate_duplicates()
        self.validate_variable_types()
        self.validate_outliers()
        self.validate_value_ranges()
        
        # Layer 2: Theoretical Consistency
        print("[2/3] Theoretical Consistency Layer")
        self.validate_construct_presence()
        self.validate_measurement_items()
        if not quick_check:
            self.validate_expected_correlations()
        
        # Layer 3: Statistical Assumptions
        print("[3/3] Statistical Assumptions Layer")
        if not quick_check:
            self.validate_normality()
            self.validate_homoscedasticity()
        self.validate_multicollinearity()
        self.validate_sample_size()
        
        print("\nValidation complete.")
        return self.report
    
    def print_summary(self) -> None:
        """Print validation summary to console"""
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        
        print(f"\nDataset: {self.report.dataset_info['n_observations']} observations × "
              f"{self.report.dataset_info['n_variables']} variables")
        
        print(f"\nValidation Results:")
        for level in ['CRITICAL', 'WARNING', 'ADVISORY', 'INFO']:
            count = self.report.validation_summary[level]
            if count > 0:
                symbol = "✗" if level in ['CRITICAL', 'WARNING'] else "⚠"
                print(f"  {symbol} {level}: {count} issue(s)")
        
        if self.report.validation_summary['CRITICAL'] == 0 and \
           self.report.validation_summary['WARNING'] == 0:
            print("  ✓ No critical issues detected")
        
        print(f"\nPassed Checks: {len(self.report.passed_checks)}")
        
        # Show critical and warning issues
        critical_issues = self.report.get_issues_by_level(ValidationLevel.CRITICAL)
        warning_issues = self.report.get_issues_by_level(ValidationLevel.WARNING)
        
        if critical_issues:
            print("\n" + "-"*80)
            print("CRITICAL ISSUES (must be addressed)")
            print("-"*80)
            for issue in critical_issues:
                var_str = f" [{issue.variable}]" if issue.variable else ""
                print(f"\n✗ {issue.category}{var_str}")
                print(f"  {issue.message}")
                if issue.recommendation:
                    print(f"  → {issue.recommendation}")
        
        if warning_issues:
            print("\n" + "-"*80)
            print("WARNINGS (should be addressed)")
            print("-"*80)
            for issue in warning_issues:
                var_str = f" [{issue.variable}]" if issue.variable else ""
                print(f"\n⚠ {issue.category}{var_str}")
                print(f"  {issue.message}")
                if issue.recommendation:
                    print(f"  → {issue.recommendation}")
        
        print("\n" + "="*80)
    
    def save_report(self, output_path: str) -> None:
        """
        Save validation report to JSON file
        
        Args:
            output_path: Output file path
        """
        report_dict = self.report.to_dict()
        
        output_file = Path(output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Detailed report saved to: {output_file.absolute()}")


def load_config(config_path: str) -> Optional[Dict[str, Any]]:
    """Load theoretical framework configuration"""
    if not config_path:
        return None
    
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Warning: Configuration file not found: {config_path}")
        return None
    
    with open(config_file, 'r', encoding='utf-8') as f:
        if config_file.suffix == '.yaml' or config_file.suffix == '.yml':
            return yaml.safe_load(f)
        elif config_file.suffix == '.json':
            return json.load(f)
        else:
            print(f"Warning: Unsupported config format: {config_file.suffix}")
            return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Multi-Layered Data Validation System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic validation without theoretical framework
    python data_validator.py --data dataset.csv
    
    # Validation with theoretical framework
    python data_validator.py --data dataset.csv --config framework_config.yaml
    
    # Quick check (skip time-consuming tests)
    python data_validator.py --data dataset.csv --quick-check
    
    # Save detailed report
    python data_validator.py --data dataset.csv --output validation_report.json

Validation Layers:
    1. Data Integrity: Completeness, consistency, outliers, ranges
    2. Theoretical Consistency: Construct presence, expected patterns
    3. Statistical Assumptions: Normality, homoscedasticity, multicollinearity
        """
    )
    
    parser.add_argument('--data', type=str, required=True,
                       help='Path to dataset (CSV format)')
    parser.add_argument('--config', type=str,
                       help='Path to theoretical framework configuration (YAML/JSON)')
    parser.add_argument('--quick-check', action='store_true',
                       help='Skip time-consuming validation checks')
    parser.add_argument('--output', type=str, default='validation_report.json',
                       help='Output report file path (default: validation_report.json)')
    
    args = parser.parse_args()
    
    try:
        # Load data
        print(f"Loading dataset: {args.data}")
        data = pd.read_csv(args.data)
        print(f"✓ Loaded: {len(data)} observations × {len(data.columns)} variables")
        
        # Load configuration if provided
        config = load_config(args.config) if args.config else None
        if config:
            print(f"✓ Loaded theoretical framework: {config['theoretical_framework']['name']}")
        
        # Create validator and run
        validator = DataValidator(data, config)
        report = validator.run_all_validations(quick_check=args.quick_check)
        
        # Print summary
        validator.print_summary()
        
        # Save report
        validator.save_report(args.output)
        
        # Exit with error code if critical issues found
        if report.validation_summary['CRITICAL'] > 0:
            print("\n✗ Critical issues detected. Data cannot be analyzed without addressing these issues.")
            sys.exit(1)
        elif report.validation_summary['WARNING'] > 0:
            print("\n⚠ Warnings detected. Proceed with caution.")
            sys.exit(0)
        else:
            print("\n✓ Validation passed. Data is ready for analysis.")
            sys.exit(0)
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
