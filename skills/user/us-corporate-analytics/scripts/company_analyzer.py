"""
US Corporate Analytics - 企業分析統合スクリプト

このスクリプトは企業の財務・ガバナンス・マクロ経済データを統合分析します。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import sys
import os

# パスの設定
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sec_client import SECEdgarClient
from utils.worldbank_client import WorldBankClient
from utils.financial_ratios import FinancialRatioCalculator


class CompanyAnalyzer:
    """企業総合分析クラス"""
    
    def __init__(self, ticker: str, config: Dict):
        """
        初期化
        
        Parameters:
            ticker: 企業のティッカーシンボル
            config: 設定辞書
        """
        self.ticker = ticker
        self.config = config
        
        # クライアント初期化
        self.sec_client = SECEdgarClient(
            api_key=config['sec_edgar']['api_key'],
            user_agent=config['sec_edgar']['user_agent']
        )
        self.wb_client = WorldBankClient()
        
        # データ保存用
        self.cik = None
        self.company_name = None
        self.financial_data = pd.DataFrame()
        self.macro_data = pd.DataFrame()
        self.financial_ratios = pd.DataFrame()
        self.governance_data = {}
        
    def fetch_all_data(self, years: int = 5) -> None:
        """
        すべてのデータを取得
        
        Parameters:
            years: 取得する年数
        """
        print(f"Fetching data for {self.ticker}...")
        
        # CIK取得
        self.cik = self.sec_client.get_company_cik(self.ticker)
        if not self.cik:
            raise ValueError(f"CIK not found for {self.ticker}")
        print(f"CIK: {self.cik}")
        
        # 財務データ取得
        print("Fetching financial data...")
        self.fetch_financial_data(years)
        
        # マクロ経済データ取得
        print("Fetching macroeconomic data...")
        self.fetch_macro_data(years)
        
        # 財務比率計算
        print("Calculating financial ratios...")
        self.calculate_ratios()
        
        print("Data fetching complete!")
    
    def fetch_financial_data(self, years: int = 5) -> pd.DataFrame:
        """
        財務データを取得
        
        Parameters:
            years: 取得する年数
            
        Returns:
            財務データのDataFrame
        """
        # XBRLデータを取得
        raw_data = self.sec_client.extract_financial_data(self.cik)
        
        # 最近のN年分にフィルタ
        if not raw_data.empty:
            recent_years = sorted(raw_data['fiscal_year'].dropna().unique())[-years:]
            raw_data = raw_data[raw_data['fiscal_year'].isin(recent_years)]
        
        # ピボットして整形
        financial_data = self._pivot_financial_data(raw_data)
        
        self.financial_data = financial_data
        return financial_data
    
    def _pivot_financial_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """
        生データをピボットして使いやすい形式に変換
        
        Parameters:
            raw_data: 生の財務データ
            
        Returns:
            整形された財務データ
        """
        if raw_data.empty:
            return pd.DataFrame()
        
        # 年次データのみ抽出
        annual_data = raw_data[raw_data['form'] == '10-K'].copy()
        
        # タグ名の標準化マッピング
        tag_mapping = {
            'Revenues': 'revenue',
            'RevenueFromContractWithCustomerExcludingAssessedTax': 'revenue',
            'CostOfRevenue': 'cost_of_revenue',
            'GrossProfit': 'gross_profit',
            'OperatingIncomeLoss': 'operating_income',
            'NetIncomeLoss': 'net_income',
            'Assets': 'total_assets',
            'AssetsCurrent': 'current_assets',
            'Liabilities': 'total_liabilities',
            'LiabilitiesCurrent': 'current_liabilities',
            'StockholdersEquity': 'stockholders_equity',
            'CashAndCashEquivalentsAtCarryingValue': 'cash_and_equivalents',
            'PropertyPlantAndEquipmentNet': 'property_plant_equipment'
        }
        
        # ピボット
        pivot_data = annual_data.pivot_table(
            index='fiscal_year',
            columns='tag',
            values='value',
            aggfunc='last'
        )
        
        # カラム名を標準化
        pivot_data.rename(columns=tag_mapping, inplace=True)
        
        # 基本的な計算項目を追加
        if 'revenue' in pivot_data.columns and 'cost_of_revenue' in pivot_data.columns:
            if 'gross_profit' not in pivot_data.columns:
                pivot_data['gross_profit'] = (pivot_data['revenue'] - 
                                             pivot_data['cost_of_revenue'])
        
        return pivot_data
    
    def fetch_macro_data(self, years: int = 5) -> pd.DataFrame:
        """
        マクロ経済データを取得
        
        Parameters:
            years: 取得する年数
            
        Returns:
            マクロ経済データのDataFrame
        """
        from datetime import datetime
        current_year = datetime.now().year
        start_year = current_year - years
        
        # GDPデータ
        gdp_data = self.wb_client.get_gdp_data("USA", start_year, current_year)
        
        # ビジネス環境データ
        biz_data = self.wb_client.get_business_environment("USA", start_year, current_year)
        
        # 労働市場データ
        labor_data = self.wb_client.get_labor_market("USA", start_year, current_year)
        
        # 統合
        macro_data = gdp_data
        if not biz_data.empty:
            macro_data = macro_data.merge(biz_data, on='year', how='outer')
        if not labor_data.empty:
            macro_data = macro_data.merge(labor_data, on='year', how='outer')
        
        self.macro_data = macro_data
        return macro_data
    
    def calculate_ratios(self) -> pd.DataFrame:
        """
        財務比率を計算
        
        Returns:
            財務比率のDataFrame
        """
        if self.financial_data.empty:
            raise ValueError("Financial data not available. Run fetch_financial_data first.")
        
        calculator = FinancialRatioCalculator(self.financial_data)
        self.financial_ratios = calculator.calculate_all_ratios()
        
        return self.financial_ratios
    
    def analyze_performance(self) -> Dict:
        """
        企業パフォーマンスを分析
        
        Returns:
            分析結果の辞書
        """
        if self.financial_ratios.empty:
            self.calculate_ratios()
        
        # 最新年度のデータ
        latest_year = self.financial_ratios.index[-1]
        latest_ratios = self.financial_ratios.loc[latest_year]
        
        # 平均値
        avg_ratios = self.financial_ratios.mean()
        
        # トレンド（線形回帰の傾き）
        trends = {}
        for col in self.financial_ratios.columns:
            if self.financial_ratios[col].notna().sum() >= 2:
                x = np.arange(len(self.financial_ratios))
                y = self.financial_ratios[col].values
                # 欠損値を除外
                mask = ~np.isnan(y)
                if mask.sum() >= 2:
                    slope = np.polyfit(x[mask], y[mask], 1)[0]
                    trends[col] = slope
        
        analysis = {
            'ticker': self.ticker,
            'latest_year': int(latest_year),
            'latest_ratios': latest_ratios.to_dict(),
            'average_ratios': avg_ratios.to_dict(),
            'trends': trends,
            'performance_rating': self._rate_performance(latest_ratios)
        }
        
        return analysis
    
    def _rate_performance(self, ratios: pd.Series) -> str:
        """
        パフォーマンスを評価
        
        Parameters:
            ratios: 財務比率のSeries
            
        Returns:
            評価（AAA, AA, A, BBB, BB, B, CCC等）
        """
        score = 0
        
        # ROA
        if 'ROA' in ratios:
            if ratios['ROA'] > 15:
                score += 3
            elif ratios['ROA'] > 10:
                score += 2
            elif ratios['ROA'] > 5:
                score += 1
        
        # ROE
        if 'ROE' in ratios:
            if ratios['ROE'] > 20:
                score += 3
            elif ratios['ROE'] > 15:
                score += 2
            elif ratios['ROE'] > 10:
                score += 1
        
        # Current Ratio
        if 'current_ratio' in ratios:
            if ratios['current_ratio'] > 2:
                score += 2
            elif ratios['current_ratio'] > 1.5:
                score += 1
        
        # Debt Ratio
        if 'debt_ratio' in ratios:
            if ratios['debt_ratio'] < 0.3:
                score += 2
            elif ratios['debt_ratio'] < 0.5:
                score += 1
        
        # 評価変換
        if score >= 9:
            return "AAA"
        elif score >= 7:
            return "AA"
        elif score >= 5:
            return "A"
        elif score >= 3:
            return "BBB"
        elif score >= 2:
            return "BB"
        else:
            return "B"
    
    def generate_summary_report(self) -> str:
        """
        サマリーレポートを生成
        
        Returns:
            レポート文字列
        """
        analysis = self.analyze_performance()
        
        report = f"""
{'='*70}
企業財務分析レポート
{'='*70}

企業情報
--------
ティッカー: {self.ticker}
CIK: {self.cik}
分析年度: {analysis['latest_year']}

財務パフォーマンス評価: {analysis['performance_rating']}

主要財務比率（最新年度）
------------------------
"""
        
        # 主要比率を表示
        key_ratios = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
        for ratio in key_ratios:
            if ratio in analysis['latest_ratios']:
                value = analysis['latest_ratios'][ratio]
                avg = analysis['average_ratios'][ratio]
                trend = analysis['trends'].get(ratio, 0)
                
                trend_str = "↑" if trend > 0 else "↓" if trend < 0 else "→"
                
                report += f"{ratio}: {value:.2f} "
                report += f"(平均: {avg:.2f}, トレンド: {trend_str})\n"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    def export_data(self, output_dir: str) -> None:
        """
        データをエクスポート
        
        Parameters:
            output_dir: 出力ディレクトリ
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 財務データ
        if not self.financial_data.empty:
            self.financial_data.to_csv(
                f"{output_dir}/{self.ticker}_financial_data.csv"
            )
        
        # 財務比率
        if not self.financial_ratios.empty:
            self.financial_ratios.to_csv(
                f"{output_dir}/{self.ticker}_financial_ratios.csv"
            )
        
        # マクロ経済データ
        if not self.macro_data.empty:
            self.macro_data.to_csv(
                f"{output_dir}/{self.ticker}_macro_data.csv"
            )
        
        # サマリーレポート
        report = self.generate_summary_report()
        with open(f"{output_dir}/{self.ticker}_summary_report.txt", 'w') as f:
            f.write(report)
        
        print(f"Data exported to {output_dir}")


def main():
    """メイン実行関数"""
    import yaml
    
    # 設定読み込み
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # 分析実行例
    ticker = "AAPL"
    print(f"Analyzing {ticker}...")
    
    analyzer = CompanyAnalyzer(ticker, config)
    analyzer.fetch_all_data(years=5)
    
    # レポート表示
    report = analyzer.generate_summary_report()
    print(report)
    
    # データエクスポート
    output_dir = "../data/processed"
    analyzer.export_data(output_dir)


if __name__ == "__main__":
    main()
