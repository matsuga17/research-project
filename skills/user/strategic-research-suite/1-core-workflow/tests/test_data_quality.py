"""
test_data_quality.py

Unit tests for DataQualityChecker

Usage:
    pytest test_data_quality.py
    # or
    python -m pytest test_data_quality.py -v
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from scripts.data_quality_checker import DataQualityChecker


@pytest.fixture
def sample_panel_data():
    """Create sample panel dataset for testing"""
    return pd.DataFrame({
        'firm_id': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'year': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
        'roa': [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.03, 0.04, 0.05],
        'sales': [1000, 1100, 1200, 500, 550, 600, 2000, 2100, 2200]
    })


@pytest.fixture
def unbalanced_panel_data():
    """Create unbalanced panel dataset for testing"""
    return pd.DataFrame({
        'firm_id': [1, 1, 2, 2, 2, 3],
        'year': [2020, 2021, 2020, 2021, 2022, 2020],
        'roa': [0.05, 0.06, 0.08, 0.09, 0.10, 0.03]
    })


@pytest.fixture
def data_with_missing():
    """Create dataset with missing values"""
    return pd.DataFrame({
        'firm_id': [1, 2, 3],
        'year': [2020, 2021, 2022],
        'roa': [0.05, np.nan, 0.07],
        'sales': [1000, 1100, np.nan]
    })


def test_initialization(sample_panel_data):
    """Test DataQualityChecker initialization"""
    checker = DataQualityChecker(sample_panel_data)
    
    assert checker.firm_id == 'firm_id'
    assert checker.time_id == 'year'
    assert len(checker.df) == 9
    assert isinstance(checker.report, dict)


def test_check_missing_no_missing(sample_panel_data):
    """Test missing value check with no missing values"""
    checker = DataQualityChecker(sample_panel_data)
    result = checker.check_missing()
    
    assert result['total_missing'] == 0
    assert result['columns_with_missing'] == 0
    assert len(result['missing_counts']) == 0


def test_check_missing_with_missing(data_with_missing):
    """Test missing value check with missing values"""
    checker = DataQualityChecker(data_with_missing)
    result = checker.check_missing()
    
    assert result['total_missing'] == 2
    assert result['columns_with_missing'] == 2
    assert 'roa' in result['missing_counts']
    assert 'sales' in result['missing_counts']
    assert result['missing_counts']['roa'] == 1
    assert result['missing_counts']['sales'] == 1


def test_panel_balance_balanced(sample_panel_data):
    """Test panel balance check with balanced panel"""
    checker = DataQualityChecker(sample_panel_data)
    result = checker.check_panel_balance()
    
    assert result['balanced'] == True
    assert result['total_firms'] == 3
    assert result['max_years'] == 3
    assert result['min_years'] == 3
    assert result['mean_years'] == 3.0


def test_panel_balance_unbalanced(unbalanced_panel_data):
    """Test panel balance check with unbalanced panel"""
    checker = DataQualityChecker(unbalanced_panel_data)
    result = checker.check_panel_balance()
    
    assert result['balanced'] == False
    assert result['total_firms'] == 3
    assert result['max_years'] == 3
    assert result['min_years'] == 1
    assert result['mean_years'] == 2.0


def test_check_duplicates_no_duplicates(sample_panel_data):
    """Test duplicate check with no duplicates"""
    checker = DataQualityChecker(sample_panel_data)
    result = checker.check_duplicates()
    
    assert result['full_duplicates'] == 0
    assert result['key_duplicates'] == 0


def test_check_duplicates_with_duplicates():
    """Test duplicate check with duplicates"""
    df = pd.DataFrame({
        'firm_id': [1, 1, 1, 2, 2],
        'year': [2020, 2020, 2021, 2020, 2020],  # Duplicate key
        'roa': [0.05, 0.05, 0.06, 0.08, 0.08]
    })
    
    checker = DataQualityChecker(df)
    result = checker.check_duplicates()
    
    assert result['key_duplicates'] >= 1


def test_check_outliers(sample_panel_data):
    """Test outlier detection"""
    checker = DataQualityChecker(sample_panel_data)
    result = checker.check_outliers(threshold=3.0)
    
    # With normal data, should not detect outliers
    assert len(result) == 0


def test_check_outliers_with_outliers():
    """Test outlier detection with actual outliers"""
    df = pd.DataFrame({
        'firm_id': [1, 2, 3, 4, 5],
        'year': [2020, 2020, 2020, 2020, 2020],
        'roa': [0.05, 0.06, 0.05, 0.07, 100.0]  # 100.0 is outlier
    })
    
    checker = DataQualityChecker(df)
    result = checker.check_outliers(threshold=3.0)
    
    assert 'roa' in result
    assert result['roa']['count'] >= 1


def test_check_all(sample_panel_data):
    """Test running all checks together"""
    checker = DataQualityChecker(sample_panel_data)
    report = checker.check_all()
    
    assert 'missing' in report
    assert 'outliers' in report
    assert 'dtypes' in report
    assert 'balance' in report
    assert 'duplicates' in report


def test_generate_report(sample_panel_data):
    """Test report generation"""
    checker = DataQualityChecker(sample_panel_data)
    checker.check_all()
    
    report_text = checker.generate_report()
    
    assert 'DATA QUALITY REPORT' in report_text
    assert 'Missing Values' in report_text
    assert 'Panel Balance' in report_text
    assert 'Duplicates' in report_text


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v'])
