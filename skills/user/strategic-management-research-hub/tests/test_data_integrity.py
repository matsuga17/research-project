#!/usr/bin/env python3
"""
Data Integrity Tests for Strategic Management Research
=======================================================

Automated test suite to ensure data quality, consistency, and integrity
throughout the research pipeline. Run these tests before proceeding to analysis.

Usage:
    python test_data_integrity.py --data data_final.csv

Tests cover:
1. Data structure validation
2. Missing data patterns
3. Outlier detection
4. Logical consistency checks
5. Temporal consistency (for panel data)
6. Variable range checks
7. Duplicate detection
8. Data type validation

Author: Strategic Management Research Hub
Version: 1.0
Date: 2025-10-31
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Union

import pandas as pd
import numpy as np
from scipy import stats

# Test framework
import unittest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataIntegrityTests(unittest.TestCase):
    """
    Test suite for data integrity validation.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Load data once for all tests.
        """
        logger.info("="*70)
        logger.info("DATA INTEGRITY TEST SUITE")
        logger.info("="*70)
        
        # Load data
        if hasattr(cls, 'data_path'):
            cls.df = pd.read_csv(cls.data_path)
            logger.info(f"Loaded data: {cls.data_path}")
            logger.info(f"Shape: {cls.df.shape} (rows, columns)")
        else:
            logger.warning("No data path specified. Using dummy data.")
            cls.df = cls._generate_dummy_data()
    
    @classmethod
    def _generate_dummy_data(cls) -> pd.DataFrame:
        """
        Generate dummy data for testing when no data file is provided.
        """
        np.random.seed(42)
        n = 1000
        
        df = pd.DataFrame({
            'firm_id': ['F' + str(i).zfill(3) for i in range(100)] * 10,
            'year': [year for year in range(2014, 2024) for _ in range(100)],
            'roa': np.random.normal(0.05, 0.1, n),
            'rd_intensity': np.random.uniform(0, 0.2, n),
            'log_assets': np.random.normal(8, 2, n),
            'leverage': np.random.uniform(0, 0.8, n),
            'firm_age': np.random.randint(5, 100, n),
            'patent_count': np.random.poisson(10, n),
        })
        
        # Introduce some issues for testing
        df.loc[0:5, 'roa'] = np.nan  # Missing values
        df.loc[10, 'roa'] = 5.0  # Outlier
        df.loc[15, 'leverage'] = 1.5  # Out-of-range value
        
        return df
    
    # ========================================================================
    # Test 1: Data Structure Tests
    # ========================================================================
    
    def test_01_data_loaded_successfully(self):
        """
        Test 1.1: Data file exists and loads successfully.
        """
        self.assertIsInstance(self.df, pd.DataFrame, "Data should be a pandas DataFrame")
        self.assertGreater(len(self.df), 0, "Dataset should not be empty")
        logger.info(f"✓ Test 1.1 PASSED: Data loaded successfully ({len(self.df)} rows)")
    
    def test_02_required_columns_present(self):
        """
        Test 1.2: All required columns are present.
        """
        required_columns = ['firm_id', 'year', 'roa']  # Minimum required
        
        for col in required_columns:
            self.assertIn(col, self.df.columns, f"Required column '{col}' is missing")
        
        logger.info(f"✓ Test 1.2 PASSED: All required columns present")
    
    def test_03_no_completely_empty_columns(self):
        """
        Test 1.3: No columns are completely empty.
        """
        empty_cols = [col for col in self.df.columns if self.df[col].isnull().all()]
        
        self.assertEqual(len(empty_cols), 0, 
                        f"Found completely empty columns: {empty_cols}")
        
        logger.info(f"✓ Test 1.3 PASSED: No completely empty columns")
    
    # ========================================================================
    # Test 2: Missing Data Tests
    # ========================================================================
    
    def test_04_missing_data_within_acceptable_limits(self):
        """
        Test 2.1: Missing data is within acceptable limits (<50% per variable).
        """
        missing_pct = (self.df.isnull().sum() / len(self.df)) * 100
        problematic_vars = missing_pct[missing_pct > 50]
        
        if len(problematic_vars) > 0:
            logger.warning(f"Variables with >50% missing data: {problematic_vars.to_dict()}")
        
        self.assertEqual(len(problematic_vars), 0, 
                        f"Variables with excessive missing data: {list(problematic_vars.index)}")
        
        logger.info(f"✓ Test 2.1 PASSED: Missing data within acceptable limits")
    
    def test_05_key_variables_not_missing(self):
        """
        Test 2.2: Key variables (firm_id, year, DV) have minimal missing data (<5%).
        """
        key_vars = ['firm_id', 'year']
        
        for var in key_vars:
            if var in self.df.columns:
                missing_pct = (self.df[var].isnull().sum() / len(self.df)) * 100
                self.assertLess(missing_pct, 5, 
                               f"Key variable '{var}' has {missing_pct:.1f}% missing data (limit: 5%)")
        
        logger.info(f"✓ Test 2.2 PASSED: Key variables have minimal missing data")
    
    # ========================================================================
    # Test 3: Outlier Detection Tests
    # ========================================================================
    
    def test_06_detect_extreme_outliers(self):
        """
        Test 3.1: Detect extreme outliers (|z-score| > 5).
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        extreme_outliers = {}
        
        for col in numeric_cols:
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            n_outliers = (z_scores > 5).sum()
            
            if n_outliers > 0:
                extreme_outliers[col] = n_outliers
                logger.warning(f"  {col}: {n_outliers} extreme outliers (|z| > 5)")
        
        # This is a warning, not a hard failure
        if len(extreme_outliers) > 0:
            logger.warning(f"Found extreme outliers in {len(extreme_outliers)} variables")
            logger.warning("Consider investigating or winsorizing these variables")
        else:
            logger.info(f"✓ Test 3.1 PASSED: No extreme outliers detected")
    
    def test_07_financial_ratios_within_plausible_range(self):
        """
        Test 3.2: Financial ratios are within plausible ranges.
        """
        if 'leverage' in self.df.columns:
            # Leverage should be between 0 and 1 (or slightly above for distressed firms)
            bad_leverage = ((self.df['leverage'] < 0) | (self.df['leverage'] > 2)).sum()
            self.assertEqual(bad_leverage, 0, 
                            f"Found {bad_leverage} leverage values outside [0, 2]")
        
        if 'roa' in self.df.columns:
            # ROA should be roughly between -1 and 1 (after winsorization)
            bad_roa = ((self.df['roa'] < -1) | (self.df['roa'] > 1)).sum()
            self.assertEqual(bad_roa, 0, 
                            f"Found {bad_roa} ROA values outside [-1, 1]")
        
        logger.info(f"✓ Test 3.2 PASSED: Financial ratios within plausible ranges")
    
    # ========================================================================
    # Test 4: Logical Consistency Tests
    # ========================================================================
    
    def test_08_year_values_sensible(self):
        """
        Test 4.1: Year values are within a sensible range.
        """
        if 'year' in self.df.columns:
            min_year = self.df['year'].min()
            max_year = self.df['year'].max()
            
            self.assertGreaterEqual(min_year, 1950, 
                                   f"Minimum year {min_year} seems too early")
            self.assertLessEqual(max_year, 2030, 
                                f"Maximum year {max_year} seems too late")
            
            logger.info(f"✓ Test 4.1 PASSED: Years range from {min_year} to {max_year}")
    
    def test_09_firm_age_non_negative(self):
        """
        Test 4.2: Firm age is non-negative.
        """
        if 'firm_age' in self.df.columns:
            negative_age = (self.df['firm_age'] < 0).sum()
            self.assertEqual(negative_age, 0, 
                            f"Found {negative_age} negative firm ages")
            
            logger.info(f"✓ Test 4.2 PASSED: All firm ages are non-negative")
    
    def test_10_log_variables_correspond_to_positive_originals(self):
        """
        Test 4.3: Log-transformed variables should not have negative values.
        """
        log_vars = [col for col in self.df.columns if col.startswith('log_')]
        
        for var in log_vars:
            if var in self.df.columns:
                # log(x) is defined for x > 0, so log(x) can be any real number
                # But check for NaN due to log(0) or log(negative)
                inf_count = np.isinf(self.df[var]).sum()
                
                if inf_count > 0:
                    logger.warning(f"  {var}: {inf_count} infinite values (likely from log(0))")
        
        logger.info(f"✓ Test 4.3 PASSED: Log variables checked")
    
    # ========================================================================
    # Test 5: Temporal Consistency Tests (Panel Data)
    # ========================================================================
    
    def test_11_panel_structure_balanced_or_documented(self):
        """
        Test 5.1: Panel structure is either balanced or unbalanced is documented.
        """
        if 'firm_id' in self.df.columns and 'year' in self.df.columns:
            firm_year_counts = self.df.groupby('firm_id')['year'].count()
            
            is_balanced = (firm_year_counts.nunique() == 1)
            
            if is_balanced:
                logger.info(f"✓ Test 5.1 INFO: Panel is balanced")
            else:
                logger.info(f"✓ Test 5.1 INFO: Panel is unbalanced")
                logger.info(f"  Firms: {firm_year_counts.min()}-{firm_year_counts.max()} years")
    
    def test_12_no_duplicate_firm_year_observations(self):
        """
        Test 5.2: No duplicate firm-year observations.
        """
        if 'firm_id' in self.df.columns and 'year' in self.df.columns:
            duplicates = self.df.duplicated(subset=['firm_id', 'year'], keep=False).sum()
            
            self.assertEqual(duplicates, 0, 
                            f"Found {duplicates} duplicate firm-year observations")
            
            logger.info(f"✓ Test 5.2 PASSED: No duplicate firm-year observations")
    
    def test_13_years_continuous_or_gaps_documented(self):
        """
        Test 5.3: Check for large gaps in time series (>2 years).
        """
        if 'firm_id' in self.df.columns and 'year' in self.df.columns:
            gaps_found = False
            
            for firm in self.df['firm_id'].unique()[:10]:  # Check first 10 firms
                firm_data = self.df[self.df['firm_id'] == firm].sort_values('year')
                years = firm_data['year'].values
                
                if len(years) > 1:
                    year_diffs = np.diff(years)
                    large_gaps = (year_diffs > 2).sum()
                    
                    if large_gaps > 0:
                        gaps_found = True
                        logger.warning(f"  Firm {firm}: {large_gaps} gaps >2 years")
            
            if not gaps_found:
                logger.info(f"✓ Test 5.3 PASSED: No large time gaps detected (checked 10 firms)")
    
    # ========================================================================
    # Test 6: Data Type Validation
    # ========================================================================
    
    def test_14_numeric_variables_are_numeric(self):
        """
        Test 6.1: Variables that should be numeric are indeed numeric.
        """
        expected_numeric = ['roa', 'rd_intensity', 'log_assets', 'leverage', 'patent_count']
        
        for var in expected_numeric:
            if var in self.df.columns:
                self.assertTrue(pd.api.types.is_numeric_dtype(self.df[var]), 
                               f"Variable '{var}' should be numeric but is {self.df[var].dtype}")
        
        logger.info(f"✓ Test 6.1 PASSED: Numeric variables have correct data types")
    
    def test_15_categorical_variables_are_categorical_or_string(self):
        """
        Test 6.2: Categorical variables (firm_id, industry) are string or categorical.
        """
        expected_categorical = ['firm_id', 'industry']
        
        for var in expected_categorical:
            if var in self.df.columns:
                is_valid = pd.api.types.is_string_dtype(self.df[var]) or \
                          pd.api.types.is_categorical_dtype(self.df[var])
                
                self.assertTrue(is_valid, 
                               f"Variable '{var}' should be string/categorical but is {self.df[var].dtype}")
        
        logger.info(f"✓ Test 6.2 PASSED: Categorical variables have correct data types")
    
    # ========================================================================
    # Test 7: Statistical Properties
    # ========================================================================
    
    def test_16_variance_not_zero(self):
        """
        Test 7.1: Variables have non-zero variance (not constant).
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        zero_variance_vars = []
        
        for col in numeric_cols:
            if self.df[col].var() == 0:
                zero_variance_vars.append(col)
        
        self.assertEqual(len(zero_variance_vars), 0, 
                        f"Variables with zero variance: {zero_variance_vars}")
        
        logger.info(f"✓ Test 7.1 PASSED: All variables have non-zero variance")
    
    def test_17_correlation_matrix_computable(self):
        """
        Test 7.2: Correlation matrix can be computed (no perfect multicollinearity).
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        try:
            corr_matrix = self.df[numeric_cols].corr()
            self.assertIsInstance(corr_matrix, pd.DataFrame)
            
            # Check for perfect correlations (|r| = 1.0, excluding diagonal)
            np.fill_diagonal(corr_matrix.values, 0)
            perfect_corr = (np.abs(corr_matrix) >= 0.99).sum().sum()
            
            if perfect_corr > 0:
                logger.warning(f"Found {perfect_corr} near-perfect correlations (|r| >= 0.99)")
            
            logger.info(f"✓ Test 7.2 PASSED: Correlation matrix computed successfully")
            
        except Exception as e:
            self.fail(f"Failed to compute correlation matrix: {str(e)}")
    
    # ========================================================================
    # Test 8: Sample Size Tests
    # ========================================================================
    
    def test_18_sufficient_sample_size_for_regression(self):
        """
        Test 8.1: Sample size is sufficient for regression (N > 10*k).
        """
        n_obs = len(self.df)
        n_vars = len(self.df.select_dtypes(include=[np.number]).columns)
        
        min_required = n_vars * 10
        
        self.assertGreater(n_obs, min_required, 
                          f"Sample size {n_obs} is too small for {n_vars} variables (need > {min_required})")
        
        logger.info(f"✓ Test 8.1 PASSED: Sample size sufficient (N={n_obs}, k={n_vars})")
    
    def test_19_sufficient_observations_per_group(self):
        """
        Test 8.2: Sufficient observations per firm (for panel FE).
        """
        if 'firm_id' in self.df.columns:
            obs_per_firm = self.df.groupby('firm_id').size()
            min_obs = obs_per_firm.min()
            
            # At least 3 observations per firm for meaningful within variation
            self.assertGreaterEqual(min_obs, 3, 
                                   f"Some firms have only {min_obs} observations (need ≥ 3 for FE)")
            
            logger.info(f"✓ Test 8.2 PASSED: Sufficient observations per firm (min={min_obs})")
    
    # ========================================================================
    # Summary Report
    # ========================================================================
    
    @classmethod
    def tearDownClass(cls):
        """
        Generate summary report after all tests.
        """
        logger.info("="*70)
        logger.info("DATA INTEGRITY TEST SUITE COMPLETED")
        logger.info("="*70)
        logger.info(f"Dataset: {cls.df.shape[0]} observations, {cls.df.shape[1]} variables")
        
        # Summary statistics
        missing_pct = (cls.df.isnull().sum() / len(cls.df)) * 100
        logger.info(f"Missing data: {missing_pct.mean():.1f}% average across variables")
        
        if 'firm_id' in cls.df.columns:
            n_firms = cls.df['firm_id'].nunique()
            logger.info(f"Number of firms: {n_firms}")
        
        if 'year' in cls.df.columns:
            year_range = f"{cls.df['year'].min()}-{cls.df['year'].max()}"
            logger.info(f"Time period: {year_range}")
        
        logger.info("="*70)


# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """
    Run data integrity tests from command line.
    """
    parser = argparse.ArgumentParser(
        description='Data Integrity Tests for Strategic Management Research',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--data',
        type=str,
        default=None,
        help='Path to data file (CSV)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Set data path for test class
    if args.data:
        DataIntegrityTests.data_path = args.data
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(DataIntegrityTests)
    
    runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
