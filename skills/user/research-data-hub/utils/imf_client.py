"""
US Corporate Analytics - IMF APIクライアント

このモジュールはIMF（国際通貨基金）からデータを取得します。
"""

import requests
import pandas as pd
from typing import List, Optional, Dict, Any
import time


class IMFClient:
    """IMF API クライアント"""
    
    def __init__(self, base_url: str = "https://www.imf.org/external/datamapper/api/v1"):
        """
        初期化
        
        Parameters:
            base_url: APIのベースURL
        """
        self.base_url = base_url
        
    def get_indicator(self, indicator: str,
                     countries: Optional[List[str]] = None,
                     start_year: Optional[int] = None,
                     end_year: Optional[int] = None) -> pd.DataFrame:
        """
        特定の指標データを取得
        
        Parameters:
            indicator: 指標コード（例: "NGDP_RPCH"）
            countries: 国コードのリスト（例: ["USA", "CHN"]）
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            指標データのDataFrame
        """
        # デフォルト設定
        if countries is None:
            countries = ["USA"]
        
        # URLを構築
        country_str = "+".join(countries)
        url = f"{self.base_url}/{indicator}/{country_str}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # データを抽出
            records = []
            for country_code, country_data in data['values'][indicator].items():
                for year, value in country_data.items():
                    try:
                        year_int = int(year)
                        # 年でフィルタ
                        if start_year and year_int < start_year:
                            continue
                        if end_year and year_int > end_year:
                            continue
                        
                        records.append({
                            'indicator': indicator,
                            'country_code': country_code,
                            'year': year_int,
                            'value': value
                        })
                    except (ValueError, TypeError):
                        continue
            
            df = pd.DataFrame(records)
            if not df.empty:
                df = df.sort_values(['country_code', 'year'])
            
            return df
            
        except requests.RequestException as e:
            print(f"Error fetching IMF data: {e}")
            return pd.DataFrame()
    
    def get_gdp_indicators(self, countries: List[str] = None,
                          start_year: Optional[int] = None,
                          end_year: Optional[int] = None) -> pd.DataFrame:
        """
        GDP関連指標を取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            GDP関連データのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicators = {
            'NGDP_RPCH': 'real_gdp_growth',      # 実質GDP成長率
            'NGDPD': 'gdp_current_prices',       # 名目GDP（10億ドル）
            'NGDPRPPPPC': 'gdp_per_capita_ppp',  # 一人当たりGDP（PPP）
            'PPPPC': 'gdp_per_capita'            # 一人当たりGDP
        }
        
        dfs = []
        for indicator_code, indicator_name in indicators.items():
            df = self.get_indicator(indicator_code, countries, start_year, end_year)
            if not df.empty:
                df = df.rename(columns={'value': indicator_name})
                df = df[['country_code', 'year', indicator_name]]
                dfs.append(df)
            time.sleep(0.1)  # API負荷軽減
        
        # 統合
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        return result
    
    def get_inflation_data(self, countries: List[str] = None,
                          start_year: Optional[int] = None,
                          end_year: Optional[int] = None) -> pd.DataFrame:
        """
        インフレ関連データを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            インフレデータのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicators = {
            'PCPIPCH': 'inflation_rate',         # 消費者物価指数（年率%）
            'PCPIEPCH': 'inflation_rate_eop',    # 期末インフレ率
        }
        
        dfs = []
        for indicator_code, indicator_name in indicators.items():
            df = self.get_indicator(indicator_code, countries, start_year, end_year)
            if not df.empty:
                df = df.rename(columns={'value': indicator_name})
                df = df[['country_code', 'year', indicator_name]]
                dfs.append(df)
            time.sleep(0.1)
        
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        return result
    
    def get_exchange_rates(self, countries: List[str] = None,
                          start_year: Optional[int] = None,
                          end_year: Optional[int] = None) -> pd.DataFrame:
        """
        為替レートデータを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            為替レートデータのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicators = {
            'ENDA_XDC_USD_RATE': 'exchange_rate',        # 対米ドル為替レート
            'EREER_IX': 'real_effective_exchange_rate',  # 実効為替レート
        }
        
        dfs = []
        for indicator_code, indicator_name in indicators.items():
            df = self.get_indicator(indicator_code, countries, start_year, end_year)
            if not df.empty:
                df = df.rename(columns={'value': indicator_name})
                df = df[['country_code', 'year', indicator_name]]
                dfs.append(df)
            time.sleep(0.1)
        
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        return result
    
    def get_unemployment_data(self, countries: List[str] = None,
                             start_year: Optional[int] = None,
                             end_year: Optional[int] = None) -> pd.DataFrame:
        """
        失業率データを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            失業率データのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicator = 'LUR'  # 失業率
        
        df = self.get_indicator(indicator, countries, start_year, end_year)
        if not df.empty:
            df = df.rename(columns={'value': 'unemployment_rate'})
        
        return df
    
    def get_fiscal_data(self, countries: List[str] = None,
                       start_year: Optional[int] = None,
                       end_year: Optional[int] = None) -> pd.DataFrame:
        """
        財政データを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            財政データのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicators = {
            'GGXWDG_NGDP': 'gross_debt_gdp',           # 政府総債務（対GDP比）
            'GGR_NGDP': 'government_revenue_gdp',      # 政府歳入（対GDP比）
            'GGX_NGDP': 'government_expenditure_gdp',  # 政府歳出（対GDP比）
        }
        
        dfs = []
        for indicator_code, indicator_name in indicators.items():
            df = self.get_indicator(indicator_code, countries, start_year, end_year)
            if not df.empty:
                df = df.rename(columns={'value': indicator_name})
                df = df[['country_code', 'year', indicator_name]]
                dfs.append(df)
            time.sleep(0.1)
        
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        return result
    
    def get_current_account(self, countries: List[str] = None,
                           start_year: Optional[int] = None,
                           end_year: Optional[int] = None) -> pd.DataFrame:
        """
        経常収支データを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            経常収支データのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        indicators = {
            'BCA_NGDPD': 'current_account_gdp',  # 経常収支（対GDP比）
            'BCA': 'current_account_usd',        # 経常収支（10億ドル）
        }
        
        dfs = []
        for indicator_code, indicator_name in indicators.items():
            df = self.get_indicator(indicator_code, countries, start_year, end_year)
            if not df.empty:
                df = df.rename(columns={'value': indicator_name})
                df = df[['country_code', 'year', indicator_name]]
                dfs.append(df)
            time.sleep(0.1)
        
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        return result
    
    def get_comprehensive_data(self, countries: List[str] = None,
                              start_year: Optional[int] = None,
                              end_year: Optional[int] = None) -> pd.DataFrame:
        """
        包括的な経済データを取得
        
        Parameters:
            countries: 国コードのリスト
            start_year: 開始年
            end_year: 終了年
            
        Returns:
            包括的データのDataFrame
        """
        if countries is None:
            countries = ["USA"]
        
        print("Fetching comprehensive IMF data...")
        
        # 各カテゴリーのデータを取得
        gdp = self.get_gdp_indicators(countries, start_year, end_year)
        inflation = self.get_inflation_data(countries, start_year, end_year)
        unemployment = self.get_unemployment_data(countries, start_year, end_year)
        fiscal = self.get_fiscal_data(countries, start_year, end_year)
        current_account = self.get_current_account(countries, start_year, end_year)
        
        # 統合
        dfs = [gdp, inflation, unemployment, fiscal, current_account]
        dfs = [df for df in dfs if not df.empty]
        
        if not dfs:
            return pd.DataFrame()
        
        result = dfs[0]
        for df in dfs[1:]:
            result = result.merge(df, on=['country_code', 'year'], how='outer')
        
        result = result.sort_values(['country_code', 'year'])
        
        return result


def test_imf_client():
    """テスト関数"""
    print("Testing IMF Client...")
    
    client = IMFClient()
    
    # GDP データを取得
    print("\nGetting GDP data for USA (2010-2023)...")
    gdp_data = client.get_gdp_indicators(["USA"], 2010, 2023)
    print(gdp_data.head())
    
    # インフレデータを取得
    print("\nGetting inflation data...")
    inflation_data = client.get_inflation_data(["USA"], 2010, 2023)
    print(inflation_data.head())
    
    # 包括的データを取得
    print("\nGetting comprehensive data...")
    comprehensive = client.get_comprehensive_data(["USA"], 2015, 2023)
    print(comprehensive.head())
    print(f"\nTotal columns: {len(comprehensive.columns)}")
    print(f"Columns: {comprehensive.columns.tolist()}")


if __name__ == "__main__":
    test_imf_client()
