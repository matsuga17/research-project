"""
アジア企業無料データ収集ツールキット（v2.0 - エラーハンドリング強化版）
=========================================================================
予算制約のある研究者向けの包括的データ収集スクリプト集

対応地域: 日本、韓国、中国、台湾、ASEAN諸国
費用: 完全無料（インターネット接続のみ必要）

Version 2.0の主要改善点:
- リトライロジックの実装
- 構造化ロギング
- 具体的な例外処理
- レート制限の自動管理

Author: Corporate Research Data Hub
Version: 2.0
Date: 2025-10-31
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# ロギング設定
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# ユーティリティ関数
# ============================================================================

def create_retry_session(retries: int = 3, backoff_factor: float = 1.0,
                        status_forcelist: tuple = (429, 500, 502, 503, 504)) -> requests.Session:
    """
    リトライ機能付きセッションを作成
    
    Parameters:
    -----------
    retries : int
        最大リトライ回数
    backoff_factor : float
        リトライ間隔の増加率（1.0 = 1秒、2秒、4秒...）
    status_forcelist : tuple
        リトライ対象のHTTPステータスコード
    
    Returns:
    --------
    session : requests.Session
        設定済みセッション
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        status_forcelist=status_forcelist,
        allowed_methods=["GET", "POST"],
        backoff_factor=backoff_factor
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# ============================================================================
# 1. 日本データ収集
# ============================================================================

class JapanDataCollector:
    """日本の無料データソース収集クラス（v2.0 - エラーハンドリング強化版）"""
    
    def __init__(self):
        self.edinet_base_url = "https://disclosure.edinet-fsa.go.jp/api/v1"
        self.jpx_base_url = "https://www.jpx.co.jp"
        self.session = create_retry_session()
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_edinet_documents(self, date: str, doc_type: str = "2") -> Optional[pd.DataFrame]:
        """
        EDINET APIから書類一覧を取得（エラーハンドリング強化版）
        
        Parameters:
        -----------
        date : str
            取得日付 (YYYY-MM-DD形式)
        doc_type : str
            書類タイプ ("2": 有価証券報告書等)
        
        Returns:
        --------
        df : DataFrame or None
            書類一覧。失敗時はNone
        
        Raises:
        -------
        ValueError : 日付形式が不正
        requests.exceptions.RequestException : API接続エラー
        """
        # 入力検証
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError as e:
            self.logger.error(f"Invalid date format: {date}. Expected YYYY-MM-DD")
            raise ValueError(f"Date must be in YYYY-MM-DD format, got: {date}") from e
        
        url = f"{self.edinet_base_url}/documents.json"
        params = {
            'date': date.replace('-', ''),
            'type': doc_type
        }
        
        try:
            self.logger.info(f"Requesting EDINET documents for {date}, type={doc_type}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # APIレスポンス検証
            if 'metadata' not in data:
                self.logger.error(f"Unexpected API response structure: {data}")
                raise ValueError("Invalid API response: missing 'metadata' field")
            
            if data['metadata']['status'] == '200':
                results = data.get('results', [])
                if not results:
                    self.logger.warning(f"No documents found for {date}")
                    return pd.DataFrame()
                
                df = pd.DataFrame(results)
                self.logger.info(f"Successfully retrieved {len(df)} documents")
                return df
            else:
                error_msg = data['metadata'].get('message', 'Unknown error')
                self.logger.error(f"EDINET API error: {error_msg}")
                raise ValueError(f"EDINET API returned error: {error_msg}")
        
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Request timeout for {url}: {e}")
            raise
        
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                self.logger.error("Rate limit exceeded. Wait before retrying.")
            self.logger.error(f"HTTP error {e.response.status_code}: {e}")
            raise
        
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error to EDINET API: {e}")
            raise
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Unexpected request error: {e}")
            raise
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response from API: {e}")
            self.logger.debug(f"Response content: {response.text[:500]}")
            raise ValueError("API returned invalid JSON") from e
    
    def download_edinet_xbrl(self, doc_id: str, save_path: str) -> bool:
        """
        EDINET書類（XBRL）のダウンロード
        
        Parameters:
        -----------
        doc_id : str
            書類管理番号
        save_path : str
            保存先パス
        
        Returns:
        --------
        success : bool
            成功したかどうか
        """
        url = f"{self.edinet_base_url}/documents/{doc_id}"
        params = {'type': '1'}  # 1: 提出本文書及び監査報告書
        
        try:
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            print(f"ダウンロード成功: {doc_id} -> {save_path}")
            return True
            
        except Exception as e:
            print(f"ダウンロードエラー: {e}")
            return False
    
    def get_jpx_stock_prices(self, year: int, month: int) -> pd.DataFrame:
        """
        JPXから株価データを取得（デモ版）
        
        注意: 実際にはJPXのウェブサイトから手動でダウンロードが必要
        このメソッドはデータ構造のサンプルを返します
        
        Parameters:
        -----------
        year : int
            年
        month : int
            月
        
        Returns:
        --------
        df : DataFrame
            株価データのサンプル構造
        """
        print("注意: JPXデータは以下のURLから手動ダウンロードしてください:")
        print("https://www.jpx.co.jp/markets/statistics-equities/misc/01.html")
        
        # サンプルデータ構造
        sample_data = {
            'Date': [],
            'Code': [],
            'Name': [],
            'Open': [],
            'High': [],
            'Low': [],
            'Close': [],
            'Volume': []
        }
        
        return pd.DataFrame(sample_data)


# ============================================================================
# 2. 韓国データ収集
# ============================================================================

class KoreaDataCollector:
    """韓国の無料データソース収集クラス"""
    
    def __init__(self, api_key: str):
        """
        Parameters:
        -----------
        api_key : str
            Open DART APIキー (https://opendart.fss.or.kr/ で取得)
        """
        self.api_key = api_key
        self.base_url = "https://opendart.fss.or.kr/api"
        
    def get_company_info(self, corp_code: str) -> Dict:
        """
        企業基本情報取得
        
        Parameters:
        -----------
        corp_code : str
            기업 고유번호 (8자리)
        
        Returns:
        --------
        info : dict
            企業情報
        """
        url = f"{self.base_url}/company.json"
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '000':
                print(f"取得成功: {data.get('corp_name')}")
                return data
            else:
                print(f"エラー: {data['message']}")
                return {}
                
        except Exception as e:
            print(f"取得エラー: {e}")
            return {}
    
    def get_financial_statements(self, corp_code: str, bsns_year: str, 
                                 reprt_code: str = '11011') -> pd.DataFrame:
        """
        재무제표 취득 (財務諸表取得)
        
        Parameters:
        -----------
        corp_code : str
            기업 고유번호
        bsns_year : str
            사업연도 (YYYY)
        reprt_code : str
            보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서 등)
        
        Returns:
        --------
        df : DataFrame
            財務諸表データ
        """
        url = f"{self.base_url}/fnlttSinglAcntAll.json"
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': bsns_year,
            'reprt_code': reprt_code,
            'fs_div': 'CFS'  # CFS: 연결재무제표, OFS: 재무제표
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '000':
                df = pd.DataFrame(data['list'])
                print(f"取得成功: {len(df)} 項目")
                return df
            else:
                print(f"エラー: {data['message']}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()
    
    def get_major_shareholders(self, corp_code: str, bsns_year: str) -> pd.DataFrame:
        """
        주요주주 현황 취득 (大株主情報取得)
        
        Parameters:
        -----------
        corp_code : str
            기업 고유번호
        bsns_year : str
            사업연도 (YYYY)
        
        Returns:
        --------
        df : DataFrame
            大株主情報
        """
        url = f"{self.base_url}/hyslrSttus.json"
        params = {
            'crtfc_key': self.api_key,
            'corp_code': corp_code,
            'bsns_year': bsns_year,
            'reprt_code': '11011'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '000':
                df = pd.DataFrame(data['list'])
                print(f"取得成功: {len(df)} 株主")
                return df
            else:
                print(f"エラー: {data['message']}")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()


# ============================================================================
# 3. 中国データ収集
# ============================================================================

class ChinaDataCollector:
    """中国の無料データソース収集クラス"""
    
    def __init__(self, tushare_token: Optional[str] = None):
        """
        Parameters:
        -----------
        tushare_token : str, optional
            Tushare APIトークン (https://tushare.pro/register で取得)
        """
        self.tushare_token = tushare_token
        
        if tushare_token:
            try:
                import tushare as ts
                ts.set_token(tushare_token)
                self.pro = ts.pro_api()
                print("Tushare API初期化成功")
            except ImportError:
                print("警告: tushareがインストールされていません")
                print("インストール: pip install tushare")
                self.pro = None
        else:
            self.pro = None
    
    def get_stock_daily(self, ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        A株日次データ取得（Tushare使用）
        
        Parameters:
        -----------
        ts_code : str
            股票代码 (例: '600519.SH' - 貴州茅台)
        start_date : str
            开始日期 (YYYYMMDD)
        end_date : str
            结束日期 (YYYYMMDD)
        
        Returns:
        --------
        df : DataFrame
            株価データ
        """
        if not self.pro:
            print("エラー: Tushare APIが初期化されていません")
            return pd.DataFrame()
        
        try:
            df = self.pro.daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            print(f"取得成功: {len(df)} 日分のデータ")
            return df
            
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()
    
    def get_stock_basic_info(self, exchange: str = '') -> pd.DataFrame:
        """
        上場企業基本情報取得
        
        Parameters:
        -----------
        exchange : str
            取引所 ('SSE': 上海, 'SZSE': 深圳, '': 全部)
        
        Returns:
        --------
        df : DataFrame
            企業基本情報
        """
        if not self.pro:
            print("エラー: Tushare APIが初期化されていません")
            return pd.DataFrame()
        
        try:
            df = self.pro.stock_basic(exchange=exchange, list_status='L')
            print(f"取得成功: {len(df)} 社")
            return df
            
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()
    
    def get_income_statement(self, ts_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        利润表（損益計算書）取得
        
        Parameters:
        -----------
        ts_code : str
            股票代码
        start_date : str
            开始日期 (YYYYMMDD)
        end_date : str
            结束日期 (YYYYMMDD)
        
        Returns:
        --------
        df : DataFrame
            損益計算書データ
        """
        if not self.pro:
            print("エラー: Tushare APIが初期化されていません")
            return pd.DataFrame()
        
        try:
            df = self.pro.income(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            print(f"取得成功: {len(df)} 期分のデータ")
            return df
            
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()


# ============================================================================
# 4. 台湾データ収集
# ============================================================================

class TaiwanDataCollector:
    """台湾の無料データソース収集クラス"""
    
    def __init__(self):
        self.twse_base_url = "https://www.twse.com.tw"
    
    def get_stock_daily(self, date: str) -> pd.DataFrame:
        """
        TWSE日次株価データ取得
        
        Parameters:
        -----------
        date : str
            日期 (YYYYMMDD形式)
        
        Returns:
        --------
        df : DataFrame
            全銘柄の日次データ
        """
        url = f"{self.twse_base_url}/exchangeReport/MI_INDEX"
        params = {
            'response': 'json',
            'date': date,
            'type': 'ALL'
        }
        
        try:
            # TWS推奨: User-Agentを設定
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['stat'] == 'OK':
                df = pd.DataFrame(data['data9'])
                print(f"取得成功: {len(df)} 銘柄")
                return df
            else:
                print(f"エラー: データなし")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"取得エラー: {e}")
            print("注意: TWS E APIには1日の取得制限があります")
            return pd.DataFrame()
    
    def get_listed_companies(self) -> pd.DataFrame:
        """
        上場企業一覧取得
        
        Returns:
        --------
        df : DataFrame
            上場企業情報
        """
        url = f"{self.twse_base_url}/exchangeReport/STOCK_DAY_ALL"
        params = {
            'response': 'json'
        }
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data['data'])
            print(f"取得成功: {len(df)} 社")
            return df
            
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()


# ============================================================================
# 5. グローバル・マクロデータ収集
# ============================================================================

class GlobalDataCollector:
    """国際機関データ収集クラス"""
    
    def __init__(self):
        self.wb_base_url = "https://api.worldbank.org/v2"
        self.fred_base_url = "https://api.stlouisfed.org/fred"
    
    def get_world_bank_data(self, indicator: str, countries: List[str], 
                           start_year: int, end_year: int) -> pd.DataFrame:
        """
        World Bank データ取得
        
        Parameters:
        -----------
        indicator : str
            指標コード (例: 'NY.GDP.PCAP.CD' - GDP per capita)
        countries : list
            国コードリスト (例: ['JPN', 'KOR', 'CHN'])
        start_year : int
            開始年
        end_year : int
            終了年
        
        Returns:
        --------
        df : DataFrame
            マクロデータ
        """
        all_data = []
        
        for country in countries:
            url = f"{self.wb_base_url}/country/{country}/indicator/{indicator}"
            params = {
                'date': f'{start_year}:{end_year}',
                'format': 'json',
                'per_page': 1000
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if len(data) > 1 and data[1]:
                    country_data = pd.DataFrame(data[1])
                    all_data.append(country_data)
                    time.sleep(0.5)  # API制限対策
                    
            except Exception as e:
                print(f"取得エラー ({country}): {e}")
                continue
        
        if all_data:
            df = pd.concat(all_data, ignore_index=True)
            print(f"取得成功: {len(df)} データポイント")
            return df
        else:
            return pd.DataFrame()
    
    def get_fred_exchange_rates(self, api_key: str, series_id: str, 
                                start_date: str, end_date: str) -> pd.DataFrame:
        """
        FRED為替レートデータ取得
        
        Parameters:
        -----------
        api_key : str
            FRED API key (https://fred.stlouisfed.org/docs/api/api_key.html)
        series_id : str
            系列ID (例: 'DEXJPUS' - JPY/USD)
        start_date : str
            開始日 (YYYY-MM-DD)
        end_date : str
            終了日 (YYYY-MM-DD)
        
        Returns:
        --------
        df : DataFrame
            為替レートデータ
        """
        url = f"{self.fred_base_url}/series/observations"
        params = {
            'series_id': series_id,
            'api_key': api_key,
            'file_type': 'json',
            'observation_start': start_date,
            'observation_end': end_date
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            print(f"取得成功: {len(df)} データポイント")
            return df
            
        except Exception as e:
            print(f"取得エラー: {e}")
            return pd.DataFrame()


# ============================================================================
# 6. ユーティリティ関数
# ============================================================================

def batch_download_with_retry(download_func, items: List, 
                               max_retries: int = 3, delay: int = 2):
    """
    リトライ機能付きバッチダウンロード
    
    Parameters:
    -----------
    download_func : callable
        ダウンロード関数
    items : list
        ダウンロード対象リスト
    max_retries : int
        最大リトライ回数
    delay : int
        リトライ間隔（秒）
    
    Returns:
    --------
    results : list
        ダウンロード結果
    """
    results = []
    failed = []
    
    for i, item in enumerate(items):
        print(f"\n進捗: {i+1}/{len(items)}")
        
        for attempt in range(max_retries):
            try:
                result = download_func(item)
                results.append(result)
                time.sleep(delay)  # API制限対策
                break
            except Exception as e:
                print(f"エラー (試行 {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay * (attempt + 1))
                else:
                    failed.append(item)
    
    print(f"\n完了: {len(results)}件成功, {len(failed)}件失敗")
    
    return results, failed


def create_master_crosswalk(japan_codes: List[str], korea_codes: List[str],
                           china_codes: List[str], taiwan_codes: List[str]) -> pd.DataFrame:
    """
    クロスカントリー企業識別子マスターテーブル作成
    
    Parameters:
    -----------
    japan_codes : list
        日本企業の証券コードリスト
    korea_codes : list
        韓国企業の기업코드리スト
    china_codes : list
        中国企業の股票代码リスト
    taiwan_codes : list
        台湾企業の股票代號リスト
    
    Returns:
    --------
    df : DataFrame
        マスタークロスウォーク
    """
    # サンプル構造
    crosswalk = pd.DataFrame({
        'unified_id': range(1, 101),
        'company_name': [''] * 100,
        'country': [''] * 100,
        'japan_code': [''] * 100,
        'korea_code': [''] * 100,
        'china_code': [''] * 100,
        'taiwan_code': [''] * 100,
        'lei_code': [''] * 100  # Legal Entity Identifier
    })
    
    return crosswalk


def standardize_financial_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    財務データの標準化（各国会計基準を考慮）
    
    Parameters:
    -----------
    df : DataFrame
        生の財務データ
    country : str
        国名 ('japan', 'korea', 'china', 'taiwan')
    
    Returns:
    --------
    df : DataFrame
        標準化された財務データ
    """
    # 基本的な財務比率の作成
    if 'total_assets' in df.columns and 'net_income' in df.columns:
        df['roa'] = df['net_income'] / df['total_assets']
    
    if 'total_assets' in df.columns and 'total_debt' in df.columns:
        df['leverage'] = df['total_debt'] / df['total_assets']
    
    # 国別の調整（必要に応じて）
    if country == 'japan':
        # 日本会計基準特有の調整
        pass
    elif country == 'korea':
        # 韓国会計基準特有の調整
        pass
    
    return df


# ============================================================================
# 7. サンプル使用例
# ============================================================================

def example_japan_data_collection():
    """日本データ収集の実例"""
    
    print("=" * 70)
    print("日本データ収集サンプル")
    print("=" * 70)
    
    collector = JapanDataCollector()
    
    # 1. EDINET書類一覧取得
    today = datetime.now().strftime('%Y-%m-%d')
    documents = collector.get_edinet_documents(today)
    
    if not documents.empty:
        print("\n取得した書類:")
        print(documents[['docID', 'filerName', 'docDescription']].head())
        
        # 2. 最初の書類をダウンロード（サンプル）
        if len(documents) > 0:
            first_doc = documents.iloc[0]
            doc_id = first_doc['docID']
            save_path = f"edinet_{doc_id}.zip"
            collector.download_edinet_xbrl(doc_id, save_path)


def example_korea_data_collection(api_key: str):
    """韓国データ収集の実例"""
    
    print("=" * 70)
    print("韓国データ収集サンプル")
    print("=" * 70)
    
    collector = KoreaDataCollector(api_key)
    
    # 1. サムスン電子の企業情報
    samsung_code = "00126380"
    info = collector.get_company_info(samsung_code)
    
    if info:
        print(f"\n企業名: {info.get('corp_name')}")
        print(f"CEO: {info.get('ceo_nm')}")
        print(f"設立日: {info.get('est_dt')}")
    
    # 2. 財務諸表取得
    df_financial = collector.get_financial_statements(
        corp_code=samsung_code,
        bsns_year="2023",
        reprt_code="11011"
    )
    
    if not df_financial.empty:
        print("\n財務データサンプル:")
        print(df_financial[['account_nm', 'thstrm_amount']].head(10))


def example_cross_country_analysis():
    """クロスカントリー分析の実例"""
    
    print("=" * 70)
    print("クロスカントリー分析サンプル")
    print("=" * 70)
    
    # 1. World Bankデータ取得
    collector = GlobalDataCollector()
    
    gdp_data = collector.get_world_bank_data(
        indicator='NY.GDP.PCAP.CD',
        countries=['JPN', 'KOR', 'CHN', 'TWN'],
        start_year=2010,
        end_year=2023
    )
    
    if not gdp_data.empty:
        print("\nGDP per capita データ:")
        pivot = gdp_data.pivot_table(
            values='value',
            index='date',
            columns='country',
            aggfunc='first'
        )
        print(pivot.head())
    
    print("\n注意: クロスカントリー分析では以下を考慮してください:")
    print("- 為替レートの調整")
    print("- 会計基準の違い")
    print("- データ取得タイミングの調整")
    print("- 業種分類の統一")


# ============================================================================
# メイン実行
# ============================================================================

if __name__ == "__main__":
    """
    使用例:
    
    # 日本データ収集
    example_japan_data_collection()
    
    # 韓国データ収集（APIキー必要）
    korea_api_key = "your_dart_api_key"
    example_korea_data_collection(korea_api_key)
    
    # クロスカントリー分析
    example_cross_country_analysis()
    """
    
    print("=" * 70)
    print("アジア企業無料データ収集ツールキット")
    print("=" * 70)
    print("\nこのスクリプトは以下の機能を提供します:")
    print("1. 日本: EDINET API、JPXデータ")
    print("2. 韓国: Open DART API")
    print("3. 中国: Tushare API")
    print("4. 台湾: TWSE API")
    print("5. グローバル: World Bank、FRED API")
    print("\n詳細は各関数のドキュメントを参照してください。")
    print("\n使用開始:")
    print(">>> from asian_data_collectors import JapanDataCollector")
    print(">>> collector = JapanDataCollector()")
    print(">>> data = collector.get_edinet_documents('2024-10-31')")
    print("=" * 70)