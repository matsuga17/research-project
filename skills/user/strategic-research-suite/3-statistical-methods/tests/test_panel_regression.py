"""
test_panel_regression.py

Unit tests for panel regression module

Run with: pytest test_panel_regression.py -v
"""

import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from panel_regression import PanelRegression


@pytest.fixture
def sample_panel_data():
    """Generate sample panel data for testing"""
    np.random.seed(42)
    n_firms = 50
    n_years = 10
    
    data = []
    for firm in range(1, n_firms + 1):
        firm_effect = np.random.normal(0, 0.02)
        for year in range(2014, 2014 + n_years):
            rd = np.random.uniform(0, 0.1)
            leverage = np.random.uniform(0.2, 0.6)
            roa = 0.05 + firm_effect + 0.15 * rd - 0.03 * leverage + np.random.normal(0, 0.01)
            
            data.append({
                'firm_id': firm,
                'year': year,
                'roa': roa,
                'rd_intensity': rd,
                'leverage': leverage
            })
    
    return pd.DataFrame(data)


class TestPanelRegression:
    """Test suite for PanelRegression class"""
    
    def test_initialization(self, sample_panel_data):
        """Test proper initialization"""
        pr = PanelRegression(sample_panel_data, firm_id='firm_id', time_id='year')
        
        assert pr.firm_id == 'firm_id'
        assert pr.time_id == 'year'
        assert pr.panel_data is not None
        assert len(pr.panel_data) == len(sample_panel_data)
    
    def test_fixed_effects(self, sample_panel_data):
        """Test fixed effects regression"""
        pr = PanelRegression(sample_panel_data)
        results = pr.fixed_effects(y='roa', X=['rd_intensity', 'leverage'])
        
        # Check results exist
        assert results is not None
        
        # Check coefficients exist
        assert 'rd_intensity' in results.params
        assert 'leverage' in results.params
        
        # Check R² is reasonable
        assert 0 <= results.rsquared <= 1
        
        # Check expected signs (rd_intensity positive, leverage negative)
        assert results.params['rd_intensity'] > 0
        assert results.params['leverage'] < 0
    
    def test_random_effects(self, sample_panel_data):
        """Test random effects regression"""
        pr = PanelRegression(sample_panel_data)
        results = pr.random_effects(y='roa', X=['rd_intensity', 'leverage'])
        
        assert results is not None
        assert 'rd_intensity' in results.params
        assert 0 <= results.rsquared <= 1
    
    def test_pooled_ols(self, sample_panel_data):
        """Test pooled OLS"""
        pr = PanelRegression(sample_panel_data)
        results = pr.pooled_ols(y='roa', X=['rd_intensity', 'leverage'])
        
        assert results is not None
        assert 'rd_intensity' in results.params
    
    def test_first_differences(self, sample_panel_data):
        """Test first differences regression"""
        pr = PanelRegression(sample_panel_data)
        results = pr.first_differences(y='roa', X=['rd_intensity', 'leverage'])
        
        assert results is not None
        assert 'rd_intensity' in results.params
    
    def test_hausman_test(self, sample_panel_data):
        """Test Hausman test"""
        pr = PanelRegression(sample_panel_data)
        hausman = pr.hausman_test(y='roa', X=['rd_intensity', 'leverage'])
        
        assert 'statistic' in hausman
        assert 'p_value' in hausman
        assert 'recommendation' in hausman
        assert hausman['recommendation'] in ['Fixed Effects', 'Random Effects', 'Unable to compute']
    
    def test_compare_models(self, sample_panel_data):
        """Test model comparison"""
        pr = PanelRegression(sample_panel_data)
        comparison, se_comparison, stats = pr.compare_models(y='roa', X=['rd_intensity', 'leverage'])
        
        assert len(comparison.columns) == 3  # Pooled, FE, RE
        assert 'rd_intensity' in comparison.index
        assert 'leverage' in comparison.index


def test_sample_execution():
    """Test that example code runs without errors"""
    np.random.seed(42)
    n_firms = 30
    n_years = 5
    
    data = []
    for firm in range(1, n_firms + 1):
        for year in range(2019, 2019 + n_years):
            data.append({
                'firm_id': firm,
                'year': year,
                'roa': np.random.normal(0.05, 0.02),
                'rd_intensity': np.random.uniform(0, 0.1),
                'leverage': np.random.uniform(0.2, 0.6)
            })
    
    df = pd.DataFrame(data)
    pr = PanelRegression(df)
    
    # Should run without errors
    fe_results = pr.fixed_effects(y='roa', X=['rd_intensity', 'leverage'])
    assert fe_results is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v', '--tb=short'])
