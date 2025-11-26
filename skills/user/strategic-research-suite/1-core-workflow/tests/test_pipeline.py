"""
test_pipeline.py

Unit tests for research_pipeline.py

Tests each phase of the pipeline and the full pipeline execution.

Usage:
    pytest test_pipeline.py -v
    python -m pytest test_pipeline.py
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))
from research_pipeline import StrategicResearchPipeline


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after test
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_dataframe():
    """Create sample panel data for testing"""
    np.random.seed(42)
    n_firms = 50
    years = range(2015, 2024)
    
    data = []
    for firm_id in range(1, n_firms + 1):
        for year in years:
            data.append({
                'firm_id': firm_id,
                'year': year,
                'roa': np.random.normal(0.05, 0.02),
                'sales': np.random.lognormal(15, 1.5),
                'rd_intensity': np.random.uniform(0, 0.15),
                'firm_age': year - 2000 + np.random.randint(-3, 3),
                'leverage': np.random.uniform(0.2, 0.6),
                'industry': np.random.choice(['Tech', 'Manufacturing', 'Finance'])
            })
    
    return pd.DataFrame(data)


@pytest.fixture
def pipeline(temp_output_dir):
    """Create pipeline instance for testing"""
    return StrategicResearchPipeline(
        research_question="Test research question: Does R&D affect performance?",
        output_dir=temp_output_dir
    )


# ==================== Phase 1 Tests ====================

def test_phase_1_research_design(pipeline, temp_output_dir):
    """Test Phase 1: Research Design"""
    result = pipeline.run_phase_1_research_design()
    
    # Check result structure
    assert 'research_question' in result
    assert 'hypotheses' in result
    assert 'variables' in result
    assert isinstance(result['hypotheses'], list)
    
    # Check file output
    design_file = Path(temp_output_dir) / 'phase1_research_design.json'
    assert design_file.exists()


# ==================== Phase 2 Tests ====================

def test_phase_2_data_sources(pipeline, temp_output_dir):
    """Test Phase 2: Data Source Discovery"""
    result = pipeline.run_phase_2_data_sources()
    
    # Check result structure
    assert 'primary_sources' in result
    assert 'supplementary_sources' in result
    assert isinstance(result['primary_sources'], list)
    
    # Check file output
    sources_file = Path(temp_output_dir) / 'phase2_data_sources.json'
    assert sources_file.exists()


# ==================== Phase 3 Tests ====================

def test_phase_3_sample_construction(pipeline, sample_dataframe, temp_output_dir):
    """Test Phase 3: Sample Construction"""
    result = pipeline.run_phase_3_sample_construction(sample_dataframe)
    
    # Check result is DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check sample was filtered
    assert len(result) > 0
    assert len(result) <= len(sample_dataframe)
    
    # Check required columns exist
    assert 'firm_id' in result.columns
    assert 'year' in result.columns
    
    # Check file outputs
    sample_file = Path(temp_output_dir) / 'phase3_sample.csv'
    stats_file = Path(temp_output_dir) / 'phase3_sample_stats.json'
    assert sample_file.exists()
    assert stats_file.exists()


# ==================== Phase 4 Tests ====================

def test_phase_4_data_collection(pipeline, temp_output_dir):
    """Test Phase 4: Data Collection"""
    result = pipeline.run_phase_4_data_collection()
    
    # Check result is DataFrame
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    
    # Check file output
    raw_file = Path(temp_output_dir) / 'phase4_raw_data.csv'
    assert raw_file.exists()


# ==================== Phase 5 Tests ====================

def test_phase_5_data_cleaning(pipeline, sample_dataframe, temp_output_dir):
    """Test Phase 5: Data Cleaning"""
    # Add some missing values to test cleaning
    df_with_missing = sample_dataframe.copy()
    df_with_missing.loc[0:5, 'rd_intensity'] = np.nan
    
    result = pipeline.run_phase_5_data_cleaning(df_with_missing)
    
    # Check result is DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check cleaning worked
    assert len(result) > 0
    
    # Check file outputs
    clean_file = Path(temp_output_dir) / 'phase5_cleaned_data.csv'
    report_file = Path(temp_output_dir) / 'phase5_quality_report.txt'
    assert clean_file.exists()
    assert report_file.exists()


# ==================== Phase 6 Tests ====================

def test_phase_6_variable_construction(pipeline, sample_dataframe, temp_output_dir):
    """Test Phase 6: Variable Construction"""
    result = pipeline.run_phase_6_variable_construction(sample_dataframe)
    
    # Check result is DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Check new variables were created
    assert 'log_sales' in result.columns
    assert 'leverage_squared' in result.columns
    
    # Check file outputs
    vars_file = Path(temp_output_dir) / 'phase6_variables.csv'
    defs_file = Path(temp_output_dir) / 'phase6_variable_definitions.json'
    assert vars_file.exists()
    assert defs_file.exists()


# ==================== Phase 7 Tests ====================

def test_phase_7_statistical_analysis(pipeline, sample_dataframe, temp_output_dir):
    """Test Phase 7: Statistical Analysis"""
    # First construct variables
    df_vars = pipeline.run_phase_6_variable_construction(sample_dataframe)
    
    result = pipeline.run_phase_7_statistical_analysis(df_vars)
    
    # Check result structure
    assert 'descriptive' in result
    assert 'correlation' in result
    assert 'regression' in result
    
    # Check file outputs
    desc_file = Path(temp_output_dir) / 'phase7_descriptive_stats.csv'
    corr_file = Path(temp_output_dir) / 'phase7_correlation_matrix.csv'
    reg_file = Path(temp_output_dir) / 'phase7_regression_results.json'
    assert desc_file.exists()
    assert corr_file.exists()
    assert reg_file.exists()


# ==================== Phase 8 Tests ====================

def test_phase_8_reporting(pipeline, temp_output_dir):
    """Test Phase 8: Reporting"""
    # Run some phases first to have results
    pipeline.run_phase_1_research_design()
    
    result = pipeline.run_phase_8_reporting()
    
    # Check result is file path
    assert isinstance(result, str)
    
    # Check file exists
    report_file = Path(result)
    assert report_file.exists()
    
    # Check file has content
    with open(report_file, 'r') as f:
        content = f.read()
    assert len(content) > 0
    assert 'Research Question' in content


# ==================== Full Pipeline Tests ====================

def test_full_pipeline_execution(pipeline, temp_output_dir):
    """Test full pipeline execution (Phase 1-8)"""
    result = pipeline.run_full_pipeline()
    
    # Check status
    assert result['status'] == 'success'
    assert 'duration_seconds' in result
    assert 'final_report' in result
    
    # Check all phase results exist
    assert 'phase_1' in pipeline.results
    assert 'phase_2' in pipeline.results
    assert 'phase_3' in pipeline.results
    assert 'phase_4' in pipeline.results
    assert 'phase_5' in pipeline.results
    assert 'phase_6' in pipeline.results
    assert 'phase_7' in pipeline.results
    assert 'phase_8' in pipeline.results
    
    # Check final report file exists
    assert Path(result['final_report']).exists()


def test_full_pipeline_with_custom_data(pipeline, sample_dataframe, temp_output_dir):
    """Test full pipeline with custom input data"""
    result = pipeline.run_full_pipeline(input_data=sample_dataframe)
    
    # Check status
    assert result['status'] == 'success'
    
    # Check results contain data
    assert 'data' in pipeline.results['phase_3']
    assert isinstance(pipeline.results['phase_3']['data'], pd.DataFrame)


def test_specific_phase_execution(pipeline):
    """Test running a specific phase independently"""
    # Test Phase 1
    result = pipeline.run_specific_phase(1)
    assert 'research_question' in result
    
    # Test Phase 2
    result = pipeline.run_specific_phase(2)
    assert 'primary_sources' in result


def test_invalid_phase_number(pipeline):
    """Test error handling for invalid phase number"""
    with pytest.raises(ValueError):
        pipeline.run_specific_phase(9)  # Invalid phase number


# ==================== Configuration Tests ====================

def test_custom_config(temp_output_dir):
    """Test pipeline with custom configuration"""
    custom_config = {
        'sample_criteria': {
            'start_year': 2018,
            'end_year': 2023,
            'min_observations': 5
        }
    }
    
    pipeline = StrategicResearchPipeline(
        research_question="Test question",
        output_dir=temp_output_dir
    )
    
    # Manually set config
    pipeline.config.update(custom_config)
    
    # Test sample construction uses custom config
    df = pipeline._generate_placeholder_data()
    result = pipeline.run_phase_3_sample_construction(df)
    
    # Check year range matches config
    assert result['year'].min() >= 2018
    assert result['year'].max() <= 2023


# ==================== Error Handling Tests ====================

def test_empty_dataframe_handling(pipeline):
    """Test handling of empty DataFrame"""
    empty_df = pd.DataFrame()
    
    # Phase 3 should handle empty DataFrame gracefully
    result = pipeline.run_phase_3_sample_construction(empty_df)
    assert isinstance(result, pd.DataFrame)


def test_missing_columns_handling(pipeline):
    """Test handling of DataFrame with missing columns"""
    df = pd.DataFrame({
        'firm_id': [1, 2, 3],
        'year': [2020, 2021, 2022]
        # Missing other required columns
    })
    
    # Should not crash, but may produce warnings
    try:
        result = pipeline.run_phase_5_data_cleaning(df)
        assert isinstance(result, pd.DataFrame)
    except KeyError:
        # Expected if required columns are missing
        pass


# ==================== Integration Tests ====================

def test_phase_continuity(pipeline, sample_dataframe):
    """Test that phases can be chained together"""
    # Execute phases sequentially
    pipeline.run_phase_1_research_design()
    pipeline.run_phase_2_data_sources()
    df_sample = pipeline.run_phase_3_sample_construction(sample_dataframe)
    df_clean = pipeline.run_phase_5_data_cleaning(df_sample)
    df_vars = pipeline.run_phase_6_variable_construction(df_clean)
    analysis = pipeline.run_phase_7_statistical_analysis(df_vars)
    
    # Check final analysis has expected structure
    assert 'descriptive' in analysis
    assert 'regression' in analysis


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, '-v'])
