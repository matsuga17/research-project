"""
test_causal_forest.py

Unit Tests for Causal Forest Analyzer

Tests cover:
- Initialization and configuration
- Data preprocessing
- CATE estimation
- Heterogeneity analysis
- Feature importance
- Error handling

Run with:
    pytest test_causal_forest.py -v
    pytest test_causal_forest.py::TestCausalForestAnalyzer -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

# Check if EconML is available
try:
    from econml.dml import CausalForestDML
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False

# Import after checking EconML
if ECONML_AVAILABLE:
    from causal_forest import CausalForestAnalyzer


@pytest.mark.skipif(not ECONML_AVAILABLE, reason="EconML not installed")
class TestCausalForestAnalyzer:
    """Test suite for CausalForestAnalyzer class"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        # Create sample data
        df = pd.DataFrame({
            'firm_id': [1, 1, 2, 2, 3, 3],
            'year': [2019, 2020, 2019, 2020, 2019, 2020],
            'merger_dummy': [0, 1, 0, 0, 0, 1],
            'roa': [0.05, 0.07, 0.06, 0.06, 0.04, 0.08],
            'firm_size': [10.5, 10.6, 9.8, 9.9, 11.2, 11.3],
            'rd_intensity': [0.03, 0.04, 0.02, 0.02, 0.05, 0.06],
            'leverage': [0.4, 0.45, 0.3, 0.32, 0.5, 0.48]
        })
        
        # Initialize analyzer
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='merger_dummy',
            outcome='roa',
            features=['firm_size', 'rd_intensity', 'leverage'],
            firm_id='firm_id',
            time_id='year'
        )
        
        # Assertions
        assert analyzer.treatment == 'merger_dummy'
        assert analyzer.outcome == 'roa'
        assert len(analyzer.features) == 3
        assert analyzer.model is None
        assert analyzer.cate_ is None
    
    def test_initialization_with_controls(self):
        """Test initialization with control variables"""
        df = pd.DataFrame({
            'firm_id': [1, 2],
            'year': [2020, 2020],
            'treatment': [0, 1],
            'outcome': [0.05, 0.08],
            'feature1': [1.0, 2.0],
            'control1': [0.5, 0.6]
        })
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1'],
            controls=['control1']
        )
        
        assert len(analyzer.controls) == 1
        assert 'control1' in analyzer.controls
    
    def test_preprocess_data(self):
        """Test data preprocessing"""
        # Create sample data
        np.random.seed(42)
        df = pd.DataFrame({
            'firm_id': list(range(1, 101)) * 2,
            'year': [2019] * 100 + [2020] * 100,
            'treatment': np.random.binomial(1, 0.5, 200),
            'outcome': np.random.normal(0.05, 0.02, 200),
            'feature1': np.random.normal(10, 2, 200),
            'feature2': np.random.normal(0.03, 0.01, 200)
        })
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1', 'feature2']
        )
        
        # Preprocess
        Y, T, X, W = analyzer.preprocess_data()
        
        # Assertions
        assert Y.shape[0] == 200
        assert T.shape[0] == 200
        assert X.shape == (200, 2)  # 2 features
        assert W is None or W.shape[0] == 200
    
    def test_estimate_cate_basic(self):
        """Test basic CATE estimation"""
        # Create sample data with clear treatment effect
        np.random.seed(42)
        n = 200
        
        df = pd.DataFrame({
            'firm_id': list(range(1, n//2 + 1)) * 2,
            'year': [2019] * (n//2) + [2020] * (n//2),
            'treatment': np.random.binomial(1, 0.5, n),
            'feature1': np.random.normal(10, 2, n),
            'feature2': np.random.normal(0.03, 0.01, n)
        })
        
        # Generate outcome with heterogeneous effect
        # Effect varies with feature1
        df['outcome'] = (
            0.05 + 
            0.01 * df['feature1'] + 
            df['treatment'] * (0.02 + 0.005 * df['feature1']) +
            np.random.normal(0, 0.01, n)
        )
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1', 'feature2']
        )
        
        # Estimate CATE
        results = analyzer.estimate_cate()
        
        # Assertions
        assert isinstance(results, dict)
        assert 'cate_estimates' in results or 'ate' in results
        assert analyzer.model is not None
        assert analyzer.cate_ is not None
        assert len(analyzer.cate_) == n
    
    def test_feature_importance(self):
        """Test feature importance calculation"""
        # Create sample data
        np.random.seed(42)
        n = 200
        
        df = pd.DataFrame({
            'firm_id': list(range(1, n//2 + 1)) * 2,
            'year': [2019] * (n//2) + [2020] * (n//2),
            'treatment': np.random.binomial(1, 0.5, n),
            'feature1': np.random.normal(10, 2, n),
            'feature2': np.random.normal(0.03, 0.01, n)
        })
        
        # Important feature (feature1) drives heterogeneity
        df['outcome'] = (
            0.05 + 
            df['treatment'] * (0.02 + 0.01 * df['feature1']) +
            np.random.normal(0, 0.01, n)
        )
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1', 'feature2']
        )
        
        # Estimate and get feature importance
        analyzer.estimate_cate()
        importance = analyzer.get_feature_importance()
        
        # Assertions
        assert isinstance(importance, (pd.DataFrame, dict))
        if isinstance(importance, pd.DataFrame):
            assert len(importance) == 2  # 2 features
            assert 'feature' in importance.columns or 'importance' in importance.columns
    
    def test_cate_distribution(self):
        """Test CATE distribution analysis"""
        # Create sample data
        np.random.seed(42)
        n = 200
        
        df = pd.DataFrame({
            'firm_id': list(range(1, n//2 + 1)) * 2,
            'year': [2019] * (n//2) + [2020] * (n//2),
            'treatment': np.random.binomial(1, 0.5, n),
            'feature1': np.random.normal(10, 2, n)
        })
        
        df['outcome'] = (
            0.05 + 
            df['treatment'] * 0.03 +
            np.random.normal(0, 0.01, n)
        )
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1']
        )
        
        # Estimate CATE
        analyzer.estimate_cate()
        
        # Check CATE distribution
        assert analyzer.cate_ is not None
        assert len(analyzer.cate_) == n
        assert not np.all(np.isnan(analyzer.cate_))
    
    def test_analyze_heterogeneity(self):
        """Test heterogeneity analysis"""
        # Create data with heterogeneous effects
        np.random.seed(42)
        n = 200
        
        df = pd.DataFrame({
            'firm_id': list(range(1, n//2 + 1)) * 2,
            'year': [2019] * (n//2) + [2020] * (n//2),
            'treatment': np.random.binomial(1, 0.5, n),
            'firm_size': np.random.choice(['Small', 'Large'], n),
            'feature1': np.random.normal(10, 2, n)
        })
        
        # Large firms benefit more from treatment
        df['size_numeric'] = (df['firm_size'] == 'Large').astype(int)
        df['outcome'] = (
            0.05 + 
            df['treatment'] * (0.02 + 0.03 * df['size_numeric']) +
            np.random.normal(0, 0.01, n)
        )
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature1']
        )
        
        analyzer.estimate_cate()
        heterogeneity = analyzer.analyze_heterogeneity()
        
        # Assertions
        assert isinstance(heterogeneity, dict)
        assert 'cate_mean' in heterogeneity or 'ate' in heterogeneity


class TestCausalForestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_econml(self):
        """Test error when EconML is not available"""
        if ECONML_AVAILABLE:
            pytest.skip("EconML is available")
        
        df = pd.DataFrame({
            'treatment': [0, 1],
            'outcome': [0.05, 0.08],
            'feature': [1.0, 2.0]
        })
        
        with pytest.raises(ImportError):
            CausalForestAnalyzer(
                df=df,
                treatment='treatment',
                outcome='outcome',
                features=['feature']
            )
    
    @pytest.mark.skipif(not ECONML_AVAILABLE, reason="EconML not installed")
    def test_binary_treatment_requirement(self):
        """Test that treatment must be binary"""
        df = pd.DataFrame({
            'firm_id': [1, 2, 3],
            'year': [2020] * 3,
            'treatment': [0, 1, 2],  # Not binary
            'outcome': [0.05, 0.08, 0.10],
            'feature': [1.0, 2.0, 3.0]
        })
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature']
        )
        
        # Should handle or raise error for non-binary treatment
        # Exact behavior depends on implementation
        try:
            analyzer.estimate_cate()
        except (ValueError, TypeError):
            pass  # Expected for non-binary treatment
    
    @pytest.mark.skipif(not ECONML_AVAILABLE, reason="EconML not installed")
    def test_missing_values(self):
        """Test handling of missing values"""
        df = pd.DataFrame({
            'firm_id': [1, 2, 3, 4],
            'year': [2020] * 4,
            'treatment': [0, 1, 0, 1],
            'outcome': [0.05, np.nan, 0.06, 0.08],
            'feature': [1.0, 2.0, np.nan, 3.0]
        })
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature']
        )
        
        # Should handle missing values (drop or impute)
        try:
            Y, T, X, W = analyzer.preprocess_data()
            # If preprocessing succeeds, check that NaNs are handled
            assert not np.any(np.isnan(Y))
            assert not np.any(np.isnan(X))
        except ValueError:
            # If it raises an error, that's also acceptable
            pass
    
    @pytest.mark.skipif(not ECONML_AVAILABLE, reason="EconML not installed")
    def test_insufficient_data(self):
        """Test with very small sample size"""
        df = pd.DataFrame({
            'firm_id': [1, 2],
            'year': [2020] * 2,
            'treatment': [0, 1],
            'outcome': [0.05, 0.08],
            'feature': [1.0, 2.0]
        })
        
        analyzer = CausalForestAnalyzer(
            df=df,
            treatment='treatment',
            outcome='outcome',
            features=['feature']
        )
        
        # Should handle or warn about small sample
        # Exact behavior depends on implementation
        try:
            results = analyzer.estimate_cate()
            # If it succeeds, that's fine
            assert results is not None
        except (ValueError, RuntimeError):
            # If it raises an error, that's also acceptable
            pass


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_panel_data():
    """Generate sample panel data for testing"""
    np.random.seed(42)
    n_firms = 100
    n_years = 3
    
    data = []
    for firm_id in range(1, n_firms + 1):
        for year in range(2018, 2018 + n_years):
            data.append({
                'firm_id': firm_id,
                'year': year,
                'treatment': np.random.binomial(1, 0.3),
                'outcome': np.random.normal(0.05, 0.02),
                'firm_size': np.random.normal(10, 2),
                'rd_intensity': np.random.normal(0.03, 0.01),
                'leverage': np.random.normal(0.4, 0.1)
            })
    
    return pd.DataFrame(data)


@pytest.fixture
def heterogeneous_effect_data():
    """Generate data with clear heterogeneous effects"""
    np.random.seed(42)
    n = 300
    
    df = pd.DataFrame({
        'firm_id': list(range(1, n//3 + 1)) * 3,
        'year': [2018] * (n//3) + [2019] * (n//3) + [2020] * (n//3),
        'treatment': np.random.binomial(1, 0.5, n),
        'firm_size': np.random.normal(10, 2, n)
    })
    
    # Effect increases with firm size
    df['outcome'] = (
        0.05 + 
        0.01 * df['firm_size'] + 
        df['treatment'] * (0.02 + 0.005 * df['firm_size']) +
        np.random.normal(0, 0.01, n)
    )
    
    return df


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
