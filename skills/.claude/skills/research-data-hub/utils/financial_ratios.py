"""
US Corporate Analytics - 財務比率計算モジュール

このモジュールは企業の財務データから各種比率を計算します。
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List


class FinancialRatioCalculator:
    """財務比率計算クラス"""
    
    def __init__(self, financial_data: pd.DataFrame):
        """
        初期化
        
        Parameters:
            financial_data: 財務データのDataFrame
                必須カラム: 各種財務項目（revenue, net_income, assets等）
        """
        self.data = financial_data.copy()
        self.ratios = pd.DataFrame()
        
    def calculate_all_ratios(self) -> pd.DataFrame:
        """
        すべての財務比率を計算
        
        Returns:
            財務比率のDataFrame
        """
        # 各カテゴリーの比率を計算
        profitability = self.calculate_profitability_ratios()
        liquidity = self.calculate_liquidity_ratios()
        leverage = self.calculate_leverage_ratios()
        efficiency = self.calculate_efficiency_ratios()
        growth = self.calculate_growth_ratios()
        
        # 統合
        self.ratios = pd.concat([
            profitability,
            liquidity,
            leverage,
            efficiency,
            growth
        ], axis=1)
        
        return self.ratios
    
    def calculate_profitability_ratios(self) -> pd.DataFrame:
        """
        収益性指標を計算
        
        Returns:
            収益性指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # ROA (Return on Assets)
        if 'net_income' in df.columns and 'total_assets' in df.columns:
            ratios['ROA'] = (df['net_income'] / df['total_assets']) * 100
        
        # ROE (Return on Equity)
        if 'net_income' in df.columns and 'stockholders_equity' in df.columns:
            ratios['ROE'] = (df['net_income'] / df['stockholders_equity']) * 100
        
        # Gross Margin（売上総利益率）
        if 'gross_profit' in df.columns and 'revenue' in df.columns:
            ratios['gross_margin'] = (df['gross_profit'] / df['revenue']) * 100
        
        # Operating Margin（営業利益率）
        if 'operating_income' in df.columns and 'revenue' in df.columns:
            ratios['operating_margin'] = (df['operating_income'] / df['revenue']) * 100
        
        # Net Margin（純利益率）
        if 'net_income' in df.columns and 'revenue' in df.columns:
            ratios['net_margin'] = (df['net_income'] / df['revenue']) * 100
        
        # ROIC (Return on Invested Capital)
        if all(col in df.columns for col in ['operating_income', 'total_assets', 
                                              'current_liabilities']):
            invested_capital = df['total_assets'] - df['current_liabilities']
            ratios['ROIC'] = (df['operating_income'] / invested_capital) * 100
        
        return ratios
    
    def calculate_liquidity_ratios(self) -> pd.DataFrame:
        """
        流動性指標を計算
        
        Returns:
            流動性指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # Current Ratio（流動比率）
        if 'current_assets' in df.columns and 'current_liabilities' in df.columns:
            ratios['current_ratio'] = df['current_assets'] / df['current_liabilities']
        
        # Quick Ratio（当座比率）
        if all(col in df.columns for col in ['current_assets', 'inventory', 
                                              'current_liabilities']):
            quick_assets = df['current_assets'] - df['inventory']
            ratios['quick_ratio'] = quick_assets / df['current_liabilities']
        
        # Cash Ratio（現金比率）
        if 'cash_and_equivalents' in df.columns and 'current_liabilities' in df.columns:
            ratios['cash_ratio'] = df['cash_and_equivalents'] / df['current_liabilities']
        
        # Working Capital Ratio
        if all(col in df.columns for col in ['current_assets', 'current_liabilities', 
                                              'total_assets']):
            working_capital = df['current_assets'] - df['current_liabilities']
            ratios['working_capital_ratio'] = working_capital / df['total_assets']
        
        return ratios
    
    def calculate_leverage_ratios(self) -> pd.DataFrame:
        """
        レバレッジ指標を計算
        
        Returns:
            レバレッジ指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # Debt Ratio（負債比率）
        if 'total_liabilities' in df.columns and 'total_assets' in df.columns:
            ratios['debt_ratio'] = df['total_liabilities'] / df['total_assets']
        
        # Debt-to-Equity Ratio（D/E比率）
        if 'total_liabilities' in df.columns and 'stockholders_equity' in df.columns:
            ratios['debt_to_equity'] = df['total_liabilities'] / df['stockholders_equity']
        
        # Equity Multiplier（エクイティ乗数）
        if 'total_assets' in df.columns and 'stockholders_equity' in df.columns:
            ratios['equity_multiplier'] = df['total_assets'] / df['stockholders_equity']
        
        # Interest Coverage Ratio（インタレストカバレッジ）
        if 'operating_income' in df.columns and 'interest_expense' in df.columns:
            ratios['interest_coverage'] = df['operating_income'] / df['interest_expense']
        
        # Debt Service Coverage Ratio
        if all(col in df.columns for col in ['operating_income', 'interest_expense', 
                                              'principal_repayment']):
            debt_service = df['interest_expense'] + df['principal_repayment']
            ratios['debt_service_coverage'] = df['operating_income'] / debt_service
        
        return ratios
    
    def calculate_efficiency_ratios(self) -> pd.DataFrame:
        """
        効率性指標を計算
        
        Returns:
            効率性指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # Asset Turnover（総資産回転率）
        if 'revenue' in df.columns and 'total_assets' in df.columns:
            ratios['asset_turnover'] = df['revenue'] / df['total_assets']
        
        # Inventory Turnover（棚卸資産回転率）
        if 'cost_of_revenue' in df.columns and 'inventory' in df.columns:
            ratios['inventory_turnover'] = df['cost_of_revenue'] / df['inventory']
        
        # Receivables Turnover（売上債権回転率）
        if 'revenue' in df.columns and 'accounts_receivable' in df.columns:
            ratios['receivables_turnover'] = df['revenue'] / df['accounts_receivable']
        
        # Payables Turnover（買入債務回転率）
        if 'cost_of_revenue' in df.columns and 'accounts_payable' in df.columns:
            ratios['payables_turnover'] = df['cost_of_revenue'] / df['accounts_payable']
        
        # Fixed Asset Turnover（固定資産回転率）
        if 'revenue' in df.columns and 'property_plant_equipment' in df.columns:
            ratios['fixed_asset_turnover'] = df['revenue'] / df['property_plant_equipment']
        
        return ratios
    
    def calculate_growth_ratios(self) -> pd.DataFrame:
        """
        成長性指標を計算
        
        Returns:
            成長性指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # Revenue Growth Rate（売上成長率）
        if 'revenue' in df.columns:
            ratios['revenue_growth'] = df['revenue'].pct_change() * 100
        
        # Earnings Growth Rate（利益成長率）
        if 'net_income' in df.columns:
            ratios['earnings_growth'] = df['net_income'].pct_change() * 100
        
        # Asset Growth Rate（資産成長率）
        if 'total_assets' in df.columns:
            ratios['asset_growth'] = df['total_assets'].pct_change() * 100
        
        # Equity Growth Rate（株主資本成長率）
        if 'stockholders_equity' in df.columns:
            ratios['equity_growth'] = df['stockholders_equity'].pct_change() * 100
        
        return ratios
    
    def calculate_market_value_ratios(self, stock_price: pd.Series,
                                     shares_outstanding: pd.Series) -> pd.DataFrame:
        """
        市場価値指標を計算
        
        Parameters:
            stock_price: 株価のSeries
            shares_outstanding: 発行済株式数のSeries
            
        Returns:
            市場価値指標のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        # Market Cap（時価総額）
        market_cap = stock_price * shares_outstanding
        ratios['market_cap'] = market_cap
        
        # EPS (Earnings Per Share)
        if 'net_income' in df.columns:
            ratios['EPS'] = df['net_income'] / shares_outstanding
        
        # P/E Ratio
        if 'net_income' in df.columns:
            eps = df['net_income'] / shares_outstanding
            ratios['PER'] = stock_price / eps
        
        # P/B Ratio
        if 'stockholders_equity' in df.columns:
            book_value_per_share = df['stockholders_equity'] / shares_outstanding
            ratios['PBR'] = stock_price / book_value_per_share
        
        # Dividend Yield
        if 'dividends_paid' in df.columns:
            dividend_per_share = df['dividends_paid'] / shares_outstanding
            ratios['dividend_yield'] = (dividend_per_share / stock_price) * 100
        
        return ratios
    
    def calculate_dupont_analysis(self) -> pd.DataFrame:
        """
        デュポン分析を実施
        
        ROE = Net Margin × Asset Turnover × Equity Multiplier
        
        Returns:
            デュポン分析のDataFrame
        """
        df = self.data
        ratios = pd.DataFrame(index=df.index)
        
        if all(col in df.columns for col in ['net_income', 'revenue', 
                                              'total_assets', 'stockholders_equity']):
            # 3要素
            net_margin = df['net_income'] / df['revenue']
            asset_turnover = df['revenue'] / df['total_assets']
            equity_multiplier = df['total_assets'] / df['stockholders_equity']
            
            ratios['dupont_net_margin'] = net_margin * 100
            ratios['dupont_asset_turnover'] = asset_turnover
            ratios['dupont_equity_multiplier'] = equity_multiplier
            ratios['dupont_roe'] = (net_margin * asset_turnover * equity_multiplier) * 100
        
        return ratios
    
    def generate_summary_statistics(self) -> pd.DataFrame:
        """
        財務比率のサマリー統計を生成
        
        Returns:
            サマリー統計のDataFrame
        """
        if self.ratios.empty:
            self.calculate_all_ratios()
        
        summary = self.ratios.describe()
        
        # 追加統計量
        summary.loc['median'] = self.ratios.median()
        summary.loc['skewness'] = self.ratios.skew()
        summary.loc['kurtosis'] = self.ratios.kurtosis()
        
        return summary
    
    def compare_with_benchmark(self, benchmark_data: pd.DataFrame,
                               ratio_name: str) -> pd.DataFrame:
        """
        ベンチマーク（業界平均等）と比較
        
        Parameters:
            benchmark_data: ベンチマークデータ
            ratio_name: 比較する比率名
            
        Returns:
            比較結果のDataFrame
        """
        if self.ratios.empty:
            self.calculate_all_ratios()
        
        comparison = pd.DataFrame()
        comparison['company'] = self.ratios[ratio_name]
        comparison['benchmark'] = benchmark_data[ratio_name]
        comparison['difference'] = comparison['company'] - comparison['benchmark']
        comparison['relative_performance'] = (comparison['difference'] / 
                                             comparison['benchmark']) * 100
        
        return comparison


def test_calculator():
    """テスト関数"""
    # サンプルデータ作成
    data = pd.DataFrame({
        'year': [2020, 2021, 2022, 2023],
        'revenue': [1000000, 1100000, 1200000, 1300000],
        'net_income': [100000, 110000, 125000, 140000],
        'total_assets': [500000, 550000, 600000, 650000],
        'stockholders_equity': [300000, 330000, 360000, 400000],
        'current_assets': [200000, 220000, 240000, 260000],
        'current_liabilities': [100000, 110000, 120000, 130000],
        'total_liabilities': [200000, 220000, 240000, 250000],
        'operating_income': [150000, 165000, 180000, 195000],
        'gross_profit': [400000, 440000, 480000, 520000]
    })
    
    data.set_index('year', inplace=True)
    
    print("Testing Financial Ratio Calculator...")
    calculator = FinancialRatioCalculator(data)
    
    # すべての比率を計算
    ratios = calculator.calculate_all_ratios()
    print("\nCalculated Ratios:")
    print(ratios)
    
    # サマリー統計
    summary = calculator.generate_summary_statistics()
    print("\nSummary Statistics:")
    print(summary)


if __name__ == "__main__":
    test_calculator()
