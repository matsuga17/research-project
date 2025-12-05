"""
US Corporate Analytics - World Bank APIクライアント

このモジュールはWorld Bank Open Dataからマクロ経済データを取得します。
"""

import requests
import pandas as pd
from typing import List, Optional, Dict, Any
import time
from datetime import datetime


class WorldBankClient:
    """World Bank API クライアント"""
    
    def __init__(self, base_url: str = "https://api.worldbank.org/v2",
                 format: str = "json", per_page: int = 1000):
        """
        初期化
        
        Parameters:
            base_url: APIのベースURL
            format: レスポンス形式
            per_page: 1ページあたりのデータ数
        """
        self.base_url = base_url
        self.format = format
        self.per_page = per_page
        
    def get_indicator(self, indicator: str, 
                     country: str = "USA",
                     start_year: Optional[int] = None,
                     end_year: Optional[int] = None) -> pd.DataFrame:
        """
        特定の指標データを取得
        
        Parameters:
            indicator: 指標コード（例: "NY.GDP.MKTP.KD.ZG"）
            country: 国コード（例: "USA", "CHN"）
            start_year: 開始年（オプション）
            end_year: 終了年（オプション）
            
        Returns:
            指標データのDataFrame
        """
        # 日付範囲の設定
        date_range = ""
        if start_year and end_year:
            date_range = f"{start_year}:{end_year}"
        elif start_year:
            date_range = f"{start_year}:{datetime.now().year}"
        
        # APIリクエスト
        url = f"{self.base_url}/country/{country}/indicator/{indicator}"
        params = {
            "format": self.format,
            "per_page": self.per_page
        }
        if date_range:
            params["date"] = date_range
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
        
        data = response.json()
        
        if len(data) < 2 or not data[1]:
            return pd.DataFrame()
        
        # DataFrameに変換
        records = []
        for item in data[1]:
            records.append({
                'indicator_id': item['indicator']['id'],
                'indicator_name': item['indicator']['value'],
                'country': item['country']['value'],
                'country_code': item['countryiso3code'],
                'year': item['date'],
                'value': item['value']
            })
        
        df = pd.DataFrame(records)
        df['year'] = pd.to_numeric(df['year'])
        df = df.sort_values('year')
        
        return df
    
    def get_multiple_indicators(self, indicators: List[str],
                                country: str = "USA",
                                start_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> pd.DataFrame:
        """
        複数の指標を一度に取得
        
        Parameters:
            indicators: 指標コードのリスト
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            統合されたDataFrame
        """
        dfs = []
        
        for indicator in indicators:
            try:
                df = self.get_indicator(indicator, country, start_year, end_year)
                if not df.empty:
                    dfs.append(df)
                time.sleep(0.1)  # API負荷軽減
            except Exception as e:
                print(f"Warning: Failed to fetch {indicator}: {e}")
        
        if not dfs:
            return pd.DataFrame()
        
        # 統合
        result = dfs[0][['year', 'country', 'country_code']].copy()
        
        for df in dfs:
            indicator_name = df['indicator_id'].iloc[0]
            result[indicator_name] = df.set_index('year')['value']
        
        return result
    
    def get_gdp_data(self, country: str = "USA",
                    start_year: Optional[int] = None,
                    end_year: Optional[int] = None) -> pd.DataFrame:
        """
        GDP関連データを取得
        
        Parameters:
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            GDP関連データのDataFrame
        """
        indicators = [
            "NY.GDP.MKTP.CD",      # GDP（名目、米ドル）
            "NY.GDP.MKTP.KD.ZG",   # GDP成長率（実質）
            "NY.GDP.PCAP.CD",      # 一人当たりGDP
            "NY.GDP.PCAP.KD.ZG"    # 一人当たりGDP成長率
        ]
        
        return self.get_multiple_indicators(indicators, country, 
                                           start_year, end_year)
    
    def get_business_environment(self, country: str = "USA",
                                start_year: Optional[int] = None,
                                end_year: Optional[int] = None) -> pd.DataFrame:
        """
        ビジネス環境指標を取得
        
        Parameters:
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            ビジネス環境データのDataFrame
        """
        indicators = [
            "IC.BUS.EASE.XQ",     # Doing Business Index
            "IC.REG.DURS",        # 起業にかかる日数
            "IC.FRM.TIME",        # 契約執行にかかる日数
            "IC.TAX.TOTL.CP.ZS"   # 総税率（利益の%）
        ]
        
        return self.get_multiple_indicators(indicators, country,
                                           start_year, end_year)
    
    def get_institutional_quality(self, country: str = "USA",
                                 start_year: Optional[int] = None,
                                 end_year: Optional[int] = None) -> pd.DataFrame:
        """
        制度的環境の質を取得
        
        Parameters:
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            制度的環境データのDataFrame
        """
        indicators = [
            "CC.EST",  # 汚職統制指標
            "RL.EST",  # 法の支配指標
            "RQ.EST",  # 規制品質指標
            "GE.EST",  # 政府効率性
            "PV.EST",  # 政治的安定性
            "VA.EST"   # 説明責任と発言権
        ]
        
        return self.get_multiple_indicators(indicators, country,
                                           start_year, end_year)
    
    def get_labor_market(self, country: str = "USA",
                        start_year: Optional[int] = None,
                        end_year: Optional[int] = None) -> pd.DataFrame:
        """
        労働市場データを取得
        
        Parameters:
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            労働市場データのDataFrame
        """
        indicators = [
            "SL.UEM.TOTL.ZS",      # 失業率
            "SL.TLF.CACT.ZS",      # 労働参加率
            "SL.EMP.WORK.ZS",      # 雇用率
            "SE.TER.CUAT.BA.ZS"    # 大学進学率
        ]
        
        return self.get_multiple_indicators(indicators, country,
                                           start_year, end_year)
    
    def get_innovation_indicators(self, country: str = "USA",
                                 start_year: Optional[int] = None,
                                 end_year: Optional[int] = None) -> pd.DataFrame:
        """
        イノベーション指標を取得
        
        Parameters:
            country: 国コード
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            イノベーションデータのDataFrame
        """
        indicators = [
            "GB.XPD.RSDV.GD.ZS",   # R&D支出（対GDP比）
            "IP.PAT.RESD",         # 特許出願件数（居住者）
            "IP.PAT.NRES",         # 特許出願件数（非居住者）
            "IT.NET.USER.ZS"       # インターネット利用率
        ]
        
        return self.get_multiple_indicators(indicators, country,
                                           start_year, end_year)


def test_world_bank_client():
    """テスト関数"""
    print("Testing World Bank Client...")
    
    client = WorldBankClient()
    
    # GDP データを取得
    print("\nGetting GDP data for USA (2010-2023)...")
    gdp_data = client.get_gdp_data("USA", 2010, 2023)
    print(gdp_data.head())
    
    # ビジネス環境データを取得
    print("\nGetting business environment data...")
    biz_data = client.get_business_environment("USA", 2010, 2023)
    print(biz_data.head())
    
    # 制度的環境データを取得
    print("\nGetting institutional quality data...")
    inst_data = client.get_institutional_quality("USA", 2010, 2023)
    print(inst_data.head())


if __name__ == "__main__":
    test_world_bank_client()
