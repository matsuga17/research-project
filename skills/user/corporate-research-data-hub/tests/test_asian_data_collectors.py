"""
テストスイート for Asian Data Collectors
========================================
pytest based test suite for data collection modules

実行方法:
    pytest tests/test_asian_data_collectors.py -v
    pytest tests/test_asian_data_collectors.py -v --cov=scripts --cov-report=html

Author: Corporate Research Data Hub
Version: 2.0
Date: 2025-10-31
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.asian_data_collectors import (
    JapanDataCollector,
    KoreaDataCollector,
    ChinaDataCollector
)


# ============================================================================
# Japan Data Collector Tests
# ============================================================================

class TestJapanDataCollector:
    """日本データコレクターのテスト"""
    
    @pytest.fixture
    def collector(self):
        """テスト用コレクターインスタンス"""
        return JapanDataCollector()
    
    def test_initialization(self, collector):
        """初期化テスト"""
        assert collector.edinet_base_url == "https://disclosure.edinet-fsa.go.jp/api/v1"
        assert hasattr(collector, 'session')
        assert hasattr(collector, 'logger')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_success(self, mock_get, collector):
        """正常系: 書類一覧取得成功"""
        # モックレスポンス
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'metadata': {'status': '200'},
            'results': [
                {'docID': '12345', 'filerName': 'テスト株式会社', 'docDescription': '有価証券報告書'},
                {'docID': '67890', 'filerName': 'サンプル株式会社', 'docDescription': '有価証券報告書'}
            ]
        }
        mock_get.return_value = mock_response
        
        # 実行
        df = collector.get_edinet_documents('2024-10-31')
        
        # 検証
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert 'docID' in df.columns
        assert 'filerName' in df.columns
        assert df.iloc[0]['docID'] == '12345'
        assert df.iloc[1]['filerName'] == 'サンプル株式会社'
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_no_results(self, mock_get, collector):
        """正常系: 書類なし"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'metadata': {'status': '200'},
            'results': []
        }
        mock_get.return_value = mock_response
        
        df = collector.get_edinet_documents('2024-10-31')
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    def test_get_edinet_documents_invalid_date(self, collector):
        """異常系: 不正な日付形式"""
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            collector.get_edinet_documents('2024/10/31')
        
        with pytest.raises(ValueError, match="Date must be in YYYY-MM-DD format"):
            collector.get_edinet_documents('20241031')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_api_error(self, mock_get, collector):
        """異常系: APIエラー"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'metadata': {'status': '400', 'message': '不正なパラメータ'}
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="EDINET API returned error"):
            collector.get_edinet_documents('2024-10-31')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_timeout(self, mock_get, collector):
        """異常系: タイムアウト"""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        
        with pytest.raises(requests.exceptions.Timeout):
            collector.get_edinet_documents('2024-10-31')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_rate_limit(self, mock_get, collector):
        """異常系: レート制限"""
        import requests
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_get.return_value = mock_response
        
        with pytest.raises(requests.exceptions.HTTPError):
            collector.get_edinet_documents('2024-10-31')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_connection_error(self, mock_get, collector):
        """異常系: 接続エラー"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        with pytest.raises(requests.exceptions.ConnectionError):
            collector.get_edinet_documents('2024-10-31')
    
    @patch('scripts.asian_data_collectors.requests.Session.get')
    def test_get_edinet_documents_invalid_json(self, mock_get, collector):
        """異常系: 不正なJSONレスポンス"""
        import json
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError('Invalid', '', 0)
        mock_response.text = 'Invalid JSON response'
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="API returned invalid JSON"):
            collector.get_edinet_documents('2024-10-31')


# ============================================================================
# Korea Data Collector Tests
# ============================================================================

class TestKoreaDataCollector:
    """韓国データコレクターのテスト"""
    
    @pytest.fixture
    def collector(self):
        return KoreaDataCollector(api_key='test_api_key_12345')
    
    def test_initialization(self, collector):
        """初期化テスト"""
        assert collector.api_key == 'test_api_key_12345'
        assert collector.base_url == "https://opendart.fss.or.kr/api"
        assert hasattr(collector, 'logger')
    
    def test_initialization_without_api_key(self):
        """APIキーなしでの初期化"""
        with pytest.raises(ValueError, match="API key is required"):
            KoreaDataCollector(api_key=None)
    
    @patch('scripts.asian_data_collectors.requests.get')
    def test_get_company_info_success(self, mock_get, collector):
        """正常系: 企業情報取得成功"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': '000',
            'corp_code': '00126380',
            'corp_name': 'サムスン電子',
            'ceo_nm': 'テスト代表',
            'corp_cls': 'Y',
            'jurir_no': '1234567890'
        }
        mock_get.return_value = mock_response
        
        info = collector.get_company_info('00126380')
        
        assert info['status'] == '000'
        assert info['corp_name'] == 'サムスン電子'
        assert info['corp_code'] == '00126380'
    
    @patch('scripts.asian_data_collectors.requests.get')
    def test_get_company_info_not_found(self, mock_get, collector):
        """異常系: 企業が見つからない"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': '013',
            'message': '회사를 찾을 수 없습니다'
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="DART API error"):
            collector.get_company_info('99999999')


# ============================================================================
# China Data Collector Tests
# ============================================================================

class TestChinaDataCollector:
    """中国データコレクターのテスト"""
    
    @pytest.fixture
    def collector(self):
        return ChinaDataCollector(tushare_token='test_token_xyz')
    
    def test_initialization(self, collector):
        """初期化テスト"""
        assert collector.tushare_token == 'test_token_xyz'
        assert hasattr(collector, 'logger')
    
    def test_initialization_without_token(self):
        """トークンなしでの初期化"""
        with pytest.raises(ValueError, match="Tushare token is required"):
            ChinaDataCollector(tushare_token=None)
    
    @patch('scripts.asian_data_collectors.tushare.pro_api')
    def test_get_stock_basic_success(self, mock_pro_api, collector):
        """正常系: 株式基本情報取得"""
        # モックAPI
        mock_api = Mock()
        mock_df = pd.DataFrame({
            'ts_code': ['000001.SZ', '600000.SH'],
            'name': ['平安银行', '浦发银行'],
            'industry': ['银行', '银行']
        })
        mock_api.stock_basic.return_value = mock_df
        mock_pro_api.return_value = mock_api
        
        # 実行
        # Note: 実際のテストではtushare APIの初期化をモックする必要がある
        # このテストは構造の例示のみ
        pass


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """統合テスト"""
    
    def test_multi_country_workflow(self):
        """複数国データ収集ワークフロー"""
        # 実際のAPIは呼ばずにモックで検証
        pass


# ============================================================================
# Fixtures and Utilities
# ============================================================================

@pytest.fixture
def sample_dataframe():
    """テスト用サンプルデータフレーム"""
    return pd.DataFrame({
        'firm_id': ['A001', 'A002', 'A003'] * 3,
        'year': [2020, 2020, 2020, 2021, 2021, 2021, 2022, 2022, 2022],
        'total_assets': [1000, 1500, 2000, 1100, 1600, 2100, 1200, 1700, 2200],
        'net_income': [100, 150, 200, 110, 160, 210, 120, 170, 220],
        'sales': [500, 750, 1000, 550, 800, 1050, 600, 850, 1100]
    })


if __name__ == '__main__':
    # Run tests with coverage
    pytest.main([
        __file__,
        '-v',
        '--cov=scripts',
        '--cov-report=html',
        '--cov-report=term-missing'
    ])
