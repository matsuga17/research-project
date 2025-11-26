"""
test_esg_builder.py

Unit Tests for ESG Variable Builder

Tests cover:
- Initialization and data merging
- Carbon intensity calculation
- ESG score standardization
- Industry-adjusted metrics
- Temporal analysis
- Error handling

Run with:
    pytest test_esg_builder.py -v
    pytest test_esg_builder.py::TestESGVariableBuilder -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

from esg_variable_builder import ESGVariableBuilder


class TestESGVariableBuilder:
    """Test suite for ESGVariableBuilder class"""
    
    def test_initialization_basic(self):
        """Test basic initialization"""
        # Create sample ESG data
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020, 2020, 2020],
            'total_emissions': [1000, 2000, 1500],
            'esg_score': [70, 80, 75]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        assert len(builder.esg_data) == 3
        assert builder.company_id == 'company'
        assert builder.year_id == 'year'
        assert builder.financial_data is None
    
    def test_initialization_with_financial_data(self):
        """Test initialization with financial data"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020, 2020],
            'total_emissions': [1000, 2000]
        })
        
        financial_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020, 2020],
            'revenue': [10000, 20000],
            'assets': [50000, 100000]
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data
        )
        
        assert hasattr(builder, 'merged_data')
        assert len(builder.merged_data) == 2
        assert 'revenue' in builder.merged_data.columns
    
    def test_calculate_carbon_intensity_with_revenue(self):
        """Test carbon intensity calculation with revenue"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'total_emissions': [1000, 2000, 1500]
        })
        
        financial_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'revenue': [10000, 20000, 15000]  # in millions
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data
        )
        
        intensity = builder.calculate_carbon_intensity(
            emission_col='total_emissions',
            revenue_col='revenue'
        )
        
        # Assertions
        assert len(intensity) == 3
        assert all(intensity > 0)
        assert not any(np.isnan(intensity))
        
        # Company A: 1000 / (10000/1000000) = 100
        # Company B: 2000 / (20000/1000000) = 100
        # Intensities should be equal for A and B
        assert intensity.iloc[0] == pytest.approx(intensity.iloc[1], rel=0.01)
    
    def test_calculate_carbon_intensity_without_revenue(self):
        """Test carbon intensity calculation without revenue data"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020] * 2,
            'total_emissions': [1000, 2000]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        intensity = builder.calculate_carbon_intensity(
            emission_col='total_emissions',
            revenue_col=None
        )
        
        # Should return emissions as-is when no revenue
        assert len(intensity) == 2
        assert intensity.iloc[0] == 1000
        assert intensity.iloc[1] == 2000
    
    def test_standardize_esg_scores_zscore(self):
        """Test ESG score standardization using z-score"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C', 'D'],
            'year': [2020] * 4,
            'esg_score': [60, 70, 80, 90],
            'env_score': [55, 65, 75, 85]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        standardized = builder.standardize_esg_scores(
            score_cols=['esg_score', 'env_score'],
            method='zscore'
        )
        
        # Assertions
        assert len(standardized) == 4
        assert 'esg_score' in standardized.columns or 'esg_score_std' in standardized.columns
        
        # Check standardization: mean should be ~0, std should be ~1
        if 'esg_score_std' in standardized.columns:
            std_scores = standardized['esg_score_std']
            assert abs(std_scores.mean()) < 0.01
            assert abs(std_scores.std() - 1.0) < 0.01
    
    def test_standardize_esg_scores_minmax(self):
        """Test ESG score standardization using min-max"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'esg_score': [60, 80, 100]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        standardized = builder.standardize_esg_scores(
            score_cols=['esg_score'],
            method='minmax'
        )
        
        # Check that values are in [0, 1]
        if 'esg_score_std' in standardized.columns:
            scores = standardized['esg_score_std']
            assert scores.min() == pytest.approx(0.0, abs=0.01)
            assert scores.max() == pytest.approx(1.0, abs=0.01)
    
    def test_industry_adjusted_metrics(self):
        """Test industry-adjusted ESG metrics"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C', 'D'],
            'year': [2020] * 4,
            'industry': ['Tech', 'Tech', 'Manufacturing', 'Manufacturing'],
            'esg_score': [70, 80, 60, 70]
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            industry_id='industry'
        )
        
        adjusted = builder.calculate_industry_adjusted_metrics(
            metric_cols=['esg_score']
        )
        
        # Assertions
        assert isinstance(adjusted, pd.DataFrame)
        assert len(adjusted) == 4
        
        # Industry-adjusted scores should have mean ~0 within each industry
        if 'esg_score_adj' in adjusted.columns:
            for industry in ['Tech', 'Manufacturing']:
                ind_scores = adjusted[adjusted['industry'] == industry]['esg_score_adj']
                assert abs(ind_scores.mean()) < 0.1
    
    def test_temporal_change_calculation(self):
        """Test year-over-year change calculation"""
        esg_data = pd.DataFrame({
            'company': ['A', 'A', 'B', 'B'],
            'year': [2019, 2020, 2019, 2020],
            'esg_score': [70, 75, 80, 82]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        changes = builder.calculate_temporal_changes(
            metric_cols=['esg_score']
        )
        
        # Assertions
        assert isinstance(changes, pd.DataFrame)
        
        # Should have change columns
        if 'esg_score_change' in changes.columns:
            # Company A: 75 - 70 = 5
            # Company B: 82 - 80 = 2
            a_change = changes[(changes['company'] == 'A') & (changes['year'] == 2020)]['esg_score_change'].values
            if len(a_change) > 0:
                assert a_change[0] == pytest.approx(5, abs=0.1)
    
    def test_esg_performance_ranking(self):
        """Test ESG performance ranking"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C', 'D'],
            'year': [2020] * 4,
            'esg_score': [90, 70, 80, 60]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        ranked = builder.calculate_performance_rankings(
            metric_col='esg_score'
        )
        
        # Assertions
        assert isinstance(ranked, pd.DataFrame)
        assert 'rank' in ranked.columns or 'esg_score_rank' in ranked.columns
        
        # Company A (90) should rank 1st
        if 'esg_score_rank' in ranked.columns:
            a_rank = ranked[ranked['company'] == 'A']['esg_score_rank'].values[0]
            assert a_rank == 1
    
    def test_build_all_variables(self):
        """Test building all ESG variables at once"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'total_emissions': [1000, 2000, 1500],
            'esg_score': [70, 80, 75]
        })
        
        financial_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'revenue': [10000, 20000, 15000]
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data
        )
        
        variables = builder.build_all_variables()
        
        # Assertions
        assert isinstance(variables, pd.DataFrame)
        assert len(variables) == 3
        
        # Should have multiple variable types
        assert len(variables.columns) > len(esg_data.columns)


class TestESGVariableBuilderEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_emission_data(self):
        """Test handling of missing emission data"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B', 'C'],
            'year': [2020] * 3,
            'total_emissions': [1000, np.nan, 1500]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        # Should handle NaN values gracefully
        intensity = builder.calculate_carbon_intensity(emission_col='total_emissions')
        
        assert len(intensity) == 3
        # NaN should remain NaN or be handled appropriately
        assert np.isnan(intensity.iloc[1]) or intensity.iloc[1] == 0
    
    def test_zero_revenue(self):
        """Test handling of zero revenue (division by zero)"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020] * 2,
            'total_emissions': [1000, 2000]
        })
        
        financial_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020] * 2,
            'revenue': [10000, 0]  # Zero revenue for B
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data
        )
        
        # Should handle division by zero
        try:
            intensity = builder.calculate_carbon_intensity(
                emission_col='total_emissions',
                revenue_col='revenue'
            )
            # If it succeeds, check that infinity/nan is handled
            assert not any(np.isinf(intensity))
        except ZeroDivisionError:
            # If it raises error, that's also acceptable
            pass
    
    def test_mismatched_merge_keys(self):
        """Test handling of mismatched company-year pairs"""
        esg_data = pd.DataFrame({
            'company': ['A', 'B'],
            'year': [2020, 2020],
            'total_emissions': [1000, 2000]
        })
        
        financial_data = pd.DataFrame({
            'company': ['A', 'C'],  # C not in ESG data
            'year': [2020, 2020],
            'revenue': [10000, 30000]
        })
        
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data
        )
        
        # Should handle mismatched data with left join
        assert len(builder.merged_data) == 2  # Only A and B
        assert 'A' in builder.merged_data['company'].values
        assert 'B' in builder.merged_data['company'].values
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrame"""
        esg_data = pd.DataFrame(columns=['company', 'year', 'esg_score'])
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        assert len(builder.esg_data) == 0
        
        # Should handle empty data gracefully
        try:
            standardized = builder.standardize_esg_scores(score_cols=['esg_score'])
            assert len(standardized) == 0
        except (ValueError, IndexError):
            # If it raises error for empty data, that's acceptable
            pass
    
    def test_single_observation(self):
        """Test with single observation"""
        esg_data = pd.DataFrame({
            'company': ['A'],
            'year': [2020],
            'esg_score': [70]
        })
        
        builder = ESGVariableBuilder(esg_data=esg_data)
        
        # Should handle single observation
        try:
            standardized = builder.standardize_esg_scores(
                score_cols=['esg_score'],
                method='zscore'
            )
            # With single observation, std=0, so z-score is undefined
            # Implementation should handle this gracefully
            assert len(standardized) == 1
        except (ValueError, ZeroDivisionError):
            # If it raises error, that's also acceptable
            pass


class TestESGVariableBuilderIntegration:
    """Integration tests with realistic data"""
    
    def test_full_workflow(self):
        """Test complete workflow from raw data to research variables"""
        # Create realistic panel data
        np.random.seed(42)
        n_companies = 10
        n_years = 3
        
        esg_data = pd.DataFrame({
            'company': [f'Firm{i}' for i in range(1, n_companies + 1)] * n_years,
            'year': [y for y in range(2018, 2021) for _ in range(n_companies)],
            'total_emissions': np.random.gamma(2, 500, n_companies * n_years),
            'esg_score': np.random.normal(70, 15, n_companies * n_years),
            'env_score': np.random.normal(65, 12, n_companies * n_years),
            'industry': np.random.choice(['Tech', 'Manufacturing', 'Services'], 
                                        n_companies * n_years)
        })
        
        financial_data = pd.DataFrame({
            'company': [f'Firm{i}' for i in range(1, n_companies + 1)] * n_years,
            'year': [y for y in range(2018, 2021) for _ in range(n_companies)],
            'revenue': np.random.gamma(3, 5000, n_companies * n_years),
            'assets': np.random.gamma(5, 10000, n_companies * n_years)
        })
        
        # Build variables
        builder = ESGVariableBuilder(
            esg_data=esg_data,
            financial_data=financial_data,
            industry_id='industry'
        )
        
        # Calculate various metrics
        carbon_intensity = builder.calculate_carbon_intensity(
            emission_col='total_emissions',
            revenue_col='revenue'
        )
        
        standardized = builder.standardize_esg_scores(
            score_cols=['esg_score', 'env_score'],
            method='zscore'
        )
        
        # Assertions
        assert len(carbon_intensity) == n_companies * n_years
        assert len(standardized) == n_companies * n_years
        assert not all(np.isnan(carbon_intensity))


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_esg_data():
    """Sample ESG data for testing"""
    return pd.DataFrame({
        'company': ['Toyota', 'Honda', 'Nissan'] * 2,
        'year': [2019] * 3 + [2020] * 3,
        'total_emissions': [10000, 8000, 9000, 10500, 7800, 8900],
        'esg_score': [75, 80, 70, 77, 82, 72],
        'env_score': [70, 75, 65, 72, 78, 68],
        'industry': ['Auto', 'Auto', 'Auto', 'Auto', 'Auto', 'Auto']
    })


@pytest.fixture
def sample_financial_data():
    """Sample financial data for testing"""
    return pd.DataFrame({
        'company': ['Toyota', 'Honda', 'Nissan'] * 2,
        'year': [2019] * 3 + [2020] * 3,
        'revenue': [30000, 15000, 11000, 31000, 15500, 11200],
        'assets': [500000, 200000, 150000, 510000, 205000, 152000]
    })


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
