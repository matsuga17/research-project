"""
US Corporate Analytics - SEC EDGAR APIクライアント

このモジュールはSEC EDGARからデータを取得するための関数を提供します。
"""

import requests
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd


class SECEdgarClient:
    """SEC EDGAR APIクライアント"""
    
    def __init__(self, api_key: str, user_agent: str, rate_limit: int = 10):
        """
        初期化
        
        Parameters:
            api_key: SEC API キー
            user_agent: User-Agentヘッダー（メールアドレス含む）
            rate_limit: リクエスト制限（リクエスト/秒）
        """
        self.api_key = api_key
        self.headers = {
            "User-Agent": user_agent,
            "Accept": "application/json"
        }
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.base_url = "https://data.sec.gov"
        
    def _rate_limit_wait(self):
        """レート制限を守るための待機"""
        elapsed = time.time() - self.last_request_time
        wait_time = 1.0 / self.rate_limit - elapsed
        if wait_time > 0:
            time.sleep(wait_time)
        self.last_request_time = time.time()
        
    def get_company_cik(self, ticker: str) -> Optional[str]:
        """
        ティッカーシンボルからCIKコードを取得
        
        Parameters:
            ticker: 企業のティッカーシンボル（例: "AAPL"）
            
        Returns:
            CIKコード（10桁、ゼロパディング済み）
        """
        self._rate_limit_wait()
        
        # ティッカーマッピングを取得
        url = f"{self.base_url}/files/company_tickers.json"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            for item in data.values():
                if item['ticker'].upper() == ticker.upper():
                    cik = str(item['cik_str']).zfill(10)
                    return cik
        return None
    
    def get_company_facts(self, cik: str) -> Dict[str, Any]:
        """
        企業の財務データ（Company Facts）を取得
        
        Parameters:
            cik: CIKコード（10桁）
            
        Returns:
            財務データ辞書
        """
        self._rate_limit_wait()
        
        url = f"{self.base_url}/api/xbrl/companyfacts/CIK{cik}.json"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch company facts: {response.status_code}")
    
    def get_submissions(self, cik: str) -> Dict[str, Any]:
        """
        企業の提出書類リストを取得
        
        Parameters:
            cik: CIKコード（10桁）
            
        Returns:
            提出書類情報の辞書
        """
        self._rate_limit_wait()
        
        url = f"{self.base_url}/submissions/CIK{cik}.json"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch submissions: {response.status_code}")
    
    def get_filing_urls(self, cik: str, form_type: str, 
                       start_date: Optional[str] = None,
                       end_date: Optional[str] = None) -> List[Dict[str, str]]:
        """
        特定の書類タイプのファイリングURLを取得
        
        Parameters:
            cik: CIKコード（10桁）
            form_type: 書類タイプ（"10-K", "10-Q", "8-K", "DEF 14A"等）
            start_date: 開始日（"YYYY-MM-DD"形式、オプション）
            end_date: 終了日（"YYYY-MM-DD"形式、オプション）
            
        Returns:
            ファイリング情報のリスト
        """
        submissions = self.get_submissions(cik)
        filings = submissions['filings']['recent']
        
        result = []
        for i in range(len(filings['form'])):
            if filings['form'][i] == form_type:
                filing_date = filings['filingDate'][i]
                
                # 日付フィルタリング
                if start_date and filing_date < start_date:
                    continue
                if end_date and filing_date > end_date:
                    continue
                
                accession = filings['accessionNumber'][i].replace('-', '')
                primary_doc = filings['primaryDocument'][i]
                
                url = f"{self.base_url}/Archives/edgar/data/{cik}/{accession}/{primary_doc}"
                
                result.append({
                    'filing_date': filing_date,
                    'accession_number': filings['accessionNumber'][i],
                    'url': url,
                    'primary_document': primary_doc
                })
        
        return result
    
    def extract_financial_data(self, cik: str, 
                              tags: Optional[List[str]] = None) -> pd.DataFrame:
        """
        XBRLから財務データを抽出してDataFrameに変換
        
        Parameters:
            cik: CIKコード（10桁）
            tags: 取得するXBRLタグのリスト（Noneの場合は主要タグを取得）
            
        Returns:
            財務データのDataFrame
        """
        facts = self.get_company_facts(cik)
        
        # デフォルトの重要タグ
        if tags is None:
            tags = [
                'Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax',
                'CostOfRevenue', 'GrossProfit',
                'OperatingIncomeLoss', 'NetIncomeLoss',
                'Assets', 'AssetsCurrent', 'Liabilities', 'LiabilitiesCurrent',
                'StockholdersEquity', 'RetainedEarningsAccumulatedDeficit',
                'CashAndCashEquivalentsAtCarryingValue',
                'PropertyPlantAndEquipmentNet',
                'OperatingCashFlow', 'InvestingCashFlow', 'FinancingCashFlow'
            ]
        
        data_list = []
        
        # US-GAAPデータを抽出
        if 'us-gaap' in facts['facts']:
            for tag in tags:
                if tag in facts['facts']['us-gaap']:
                    units = facts['facts']['us-gaap'][tag]['units']
                    
                    # USD単位のデータを取得
                    if 'USD' in units:
                        for item in units['USD']:
                            if item.get('form') in ['10-K', '10-Q']:
                                data_list.append({
                                    'tag': tag,
                                    'value': item['val'],
                                    'end_date': item['end'],
                                    'filed_date': item['filed'],
                                    'form': item['form'],
                                    'fiscal_year': item.get('fy'),
                                    'fiscal_period': item.get('fp')
                                })
        
        df = pd.DataFrame(data_list)
        
        if not df.empty:
            # 日付型に変換
            df['end_date'] = pd.to_datetime(df['end_date'])
            df['filed_date'] = pd.to_datetime(df['filed_date'])
            
            # ソート
            df = df.sort_values(['fiscal_year', 'fiscal_period', 'end_date'])
        
        return df
    
    def get_10k_data(self, ticker: str, year: int) -> Dict[str, Any]:
        """
        特定年度の10-Kデータを取得
        
        Parameters:
            ticker: ティッカーシンボル
            year: 会計年度
            
        Returns:
            10-Kデータの辞書
        """
        cik = self.get_company_cik(ticker)
        if not cik:
            raise ValueError(f"CIK not found for ticker: {ticker}")
        
        # 10-K URLを取得
        start_date = f"{year}-01-01"
        end_date = f"{year+1}-12-31"
        
        filings = self.get_filing_urls(cik, "10-K", start_date, end_date)
        
        if not filings:
            raise ValueError(f"No 10-K found for {ticker} in year {year}")
        
        # 最新のファイリングを使用
        filing = filings[0]
        
        # 財務データを取得
        df = self.extract_financial_data(cik)
        
        # 該当年度のデータをフィルタ
        year_data = df[df['fiscal_year'] == year].copy()
        
        return {
            'ticker': ticker,
            'cik': cik,
            'fiscal_year': year,
            'filing_date': filing['filing_date'],
            'url': filing['url'],
            'financial_data': year_data
        }


def test_sec_client():
    """テスト関数"""
    # 設定を読み込み
    import yaml
    with open('../config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # クライアント初期化
    client = SECEdgarClient(
        api_key=config['sec_edgar']['api_key'],
        user_agent=config['sec_edgar']['user_agent']
    )
    
    # Appleのデータを取得してテスト
    print("Testing SEC EDGAR Client...")
    print("Getting CIK for AAPL...")
    cik = client.get_company_cik("AAPL")
    print(f"CIK: {cik}")
    
    print("\nGetting 10-K data for 2023...")
    data = client.get_10k_data("AAPL", 2023)
    print(f"Filing Date: {data['filing_date']}")
    print(f"Data points: {len(data['financial_data'])}")
    print("\nSample financial data:")
    print(data['financial_data'].head())


if __name__ == "__main__":
    test_sec_client()
