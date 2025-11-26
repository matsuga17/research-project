"""
test_edinet_collector.py

Unit Tests for EDINET Data Collector

Tests cover:
- Initialization
- Document list retrieval
- Panel data collection
- Error handling
- Rate limiting

Run with:
    pytest test_edinet_collector.py -v
    pytest test_edinet_collector.py::TestEDINETCollector::test_initialization -v
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

from edinet_collector import EDINETCollector


class TestEDINETCollector:
    """Test suite for EDINETCollector class"""
    
    def test_initialization(self):
        """Test collector initialization"""
        collector = EDINETCollector(api_key="test_key", rate_limit_delay=0.5)
        
        assert collector.api_key == "test_key"
        assert collector.rate_limit_delay == 0.5
        assert collector.base_url == "https://disclosure.edinet-fsa.go.jp/api/v1"
    
    def test_initialization_without_api_key(self):
        """Test initialization without API key"""
        collector = EDINETCollector()
        
        # API key should be None or from environment
        assert isinstance(collector, EDINETCollector)
        assert collector.base_url == "https://disclosure.edinet-fsa.go.jp/api/v1"
    
    @patch('requests.get')
    def test_get_document_list_success(self, mock_get):
        """Test successful document list retrieval"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {
                    'docID': 'S100TEST',
                    'edinetCode': 'E00001',
                    'filerName': 'Test Corporation',
                    'docTypeCode': '120',
                    'periodEnd': '2024-03-31',
                    'submitDateTime': '2024-06-30 15:00'
                },
                {
                    'docID': 'S100TEST2',
                    'edinetCode': 'E00002',
                    'filerName': 'Sample Inc.',
                    'docTypeCode': '120',
                    'periodEnd': '2024-03-31',
                    'submitDateTime': '2024-06-30 16:00'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Test
        collector = EDINETCollector()
        df = collector.get_document_list('2024-06-30')
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'docID' in df.columns
        assert 'edinetCode' in df.columns
        assert 'retrieval_date' in df.columns
        assert df['retrieval_date'].iloc[0] == '2024-06-30'
    
    @patch('requests.get')
    def test_get_document_list_empty(self, mock_get):
        """Test document list retrieval with no results"""
        # Mock empty response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response
        
        # Test
        collector = EDINETCollector()
        df = collector.get_document_list('2024-01-01')
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    @patch('requests.get')
    def test_get_document_list_with_type_filter(self, mock_get):
        """Test document list retrieval with type filter"""
        # Mock response with mixed document types
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'docID': 'S100TEST1', 'docTypeCode': '120', 'filerName': 'Corp A'},
                {'docID': 'S100TEST2', 'docTypeCode': '140', 'filerName': 'Corp B'},
                {'docID': 'S100TEST3', 'docTypeCode': '120', 'filerName': 'Corp C'}
            ]
        }
        mock_get.return_value = mock_response
        
        # Test with type filter
        collector = EDINETCollector()
        df = collector.get_document_list('2024-06-30', doc_type='120')
        
        # Assertions
        assert len(df) == 2  # Only type '120' documents
        assert all(df['docTypeCode'] == '120')
    
    @patch('requests.get')
    def test_get_document_list_api_error(self, mock_get):
        """Test handling of API errors"""
        # Mock API error
        mock_get.side_effect = Exception("API Error")
        
        # Test
        collector = EDINETCollector()
        
        with pytest.raises(Exception):
            collector.get_document_list('2024-06-30')
    
    @patch('requests.get')
    def test_get_document_list_timeout(self, mock_get):
        """Test handling of timeout errors"""
        import requests
        
        # Mock timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        # Test
        collector = EDINETCollector()
        
        with pytest.raises(requests.exceptions.Timeout):
            collector.get_document_list('2024-06-30')
    
    @patch('requests.get')
    def test_collect_sample_success(self, mock_get):
        """Test sample collection over date range"""
        # Mock successful responses
        def mock_response(*args, **kwargs):
            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                'results': [
                    {'docID': f'S100TEST{i}', 'docTypeCode': '120', 'filerName': f'Corp {i}'}
                    for i in range(3)
                ]
            }
            return response
        
        mock_get.side_effect = mock_response
        
        # Test
        collector = EDINETCollector(rate_limit_delay=0.01)  # Short delay for testing
        df = collector.collect_sample('2024-06-01', '2024-06-03', delay=0.01)
        
        # Assertions
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'docID' in df.columns
    
    @patch('requests.get')
    def test_rate_limiting(self, mock_get):
        """Test that rate limiting is applied"""
        import time
        
        # Mock responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': [{'docID': 'TEST'}]}
        mock_get.return_value = mock_response
        
        # Test with rate limiting
        collector = EDINETCollector(rate_limit_delay=0.1)
        
        start_time = time.time()
        collector.get_document_list('2024-06-30')
        collector.get_document_list('2024-07-01')
        elapsed = time.time() - start_time
        
        # Should have some delay between calls
        assert elapsed >= 0.1
    
    @patch('requests.get')
    def test_date_format_conversion(self, mock_get):
        """Test date format conversion (YYYY-MM-DD to YYYYMMDD)"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response
        
        # Test
        collector = EDINETCollector()
        collector.get_document_list('2024-06-30')
        
        # Check that API was called with correct date format
        call_args = mock_get.call_args
        assert call_args[1]['params']['date'] == '20240630'


class TestEDINETCollectorIntegration:
    """Integration tests (require actual API access)"""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="Requires actual EDINET API access")
    def test_real_api_call(self):
        """Test with real API (skip by default)"""
        collector = EDINETCollector()
        
        # Use a recent date
        date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        df = collector.get_document_list(date)
        
        # Basic validation
        assert isinstance(df, pd.DataFrame)
        if len(df) > 0:
            assert 'docID' in df.columns
            assert 'edinetCode' in df.columns


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_edinet_response():
    """Sample EDINET API response for testing"""
    return {
        'results': [
            {
                'docID': 'S100TEST001',
                'edinetCode': 'E00001',
                'secCode': '1234',
                'JCN': '1234567890123',
                'filerName': 'Test Corporation',
                'fundCode': None,
                'ordinanceCode': '010',
                'formCode': '030000',
                'docTypeCode': '120',
                'periodStart': '2023-04-01',
                'periodEnd': '2024-03-31',
                'submitDateTime': '2024-06-30 15:00',
                'docDescription': '有価証券報告書',
                'issuerEdinetCode': None,
                'subjectEdinetCode': None,
                'subsidiaryEdinetCode': None,
                'currentReportReason': None,
                'parentDocID': None,
                'opeDateTime': None,
                'withdrawalStatus': '0',
                'docInfoEditStatus': '0',
                'disclosureStatus': '0',
                'xbrlFlag': '1',
                'pdfFlag': '1',
                'attachDocFlag': '0',
                'englishDocFlag': '0'
            }
        ]
    }


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
