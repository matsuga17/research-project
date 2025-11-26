"""
US Corporate Analytics - 業界比較分析スクリプト

このスクリプトは複数企業の財務データを比較分析します。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.company_analyzer import CompanyAnalyzer


class IndustryComparison:
    """業界比較分析クラス"""
    
    def __init__(self, tickers: List[str], config: Dict):
        """
        初期化
        
        Parameters:
            tickers: ティッカーシンボルのリスト
            config: 設定辞書
        """
        self.tickers = tickers
        self.config = config
        self.analyzers = {}
        self.comparison_data = pd.DataFrame()
        
    def fetch_all_companies(self, years: int = 5) -> None:
        """
        すべての企業のデータを取得
        
        Parameters:
            years: 取得する年数
        """
        for ticker in self.tickers:
            print(f"\nFetching data for {ticker}...")
            try:
                analyzer = CompanyAnalyzer(ticker, self.config)
                analyzer.fetch_all_data(years)
                self.analyzers[ticker] = analyzer
                print(f"✓ {ticker} data fetched successfully")
            except Exception as e:
                print(f"✗ Error fetching {ticker}: {e}")
    
    def compare_ratios(self, ratio_names: List[str]) -> pd.DataFrame:
        """
        指定された比率を比較
        
        Parameters:
            ratio_names: 比較する比率名のリスト
            
        Returns:
            比較結果のDataFrame
        """
        comparison = {}
        
        for ticker, analyzer in self.analyzers.items():
            ratios = analyzer.financial_ratios
            if not ratios.empty:
                # 最新年度のデータ
                latest = ratios.iloc[-1]
                comparison[ticker] = {
                    ratio: latest.get(ratio, np.nan) 
                    for ratio in ratio_names
                }
        
        self.comparison_data = pd.DataFrame(comparison).T
        return self.comparison_data
    
    def generate_ranking(self, metric: str, 
                        ascending: bool = False) -> pd.DataFrame:
        """
        指定メトリックでランキングを生成
        
        Parameters:
            metric: ランキングの基準となるメトリック
            ascending: 昇順か（デフォルトは降順）
            
        Returns:
            ランキングのDataFrame
        """
        if self.comparison_data.empty:
            raise ValueError("Comparison data not available. Run compare_ratios first.")
        
        if metric not in self.comparison_data.columns:
            raise ValueError(f"Metric {metric} not found in comparison data")
        
        ranking = self.comparison_data[[metric]].copy()
        ranking = ranking.sort_values(metric, ascending=ascending)
        ranking['rank'] = range(1, len(ranking) + 1)
        
        return ranking
    
    def calculate_industry_statistics(self, ratio_names: List[str]) -> pd.DataFrame:
        """
        業界統計を計算
        
        Parameters:
            ratio_names: 統計を計算する比率名のリスト
            
        Returns:
            統計データのDataFrame
        """
        if self.comparison_data.empty:
            self.compare_ratios(ratio_names)
        
        stats = pd.DataFrame({
            'mean': self.comparison_data[ratio_names].mean(),
            'median': self.comparison_data[ratio_names].median(),
            'std': self.comparison_data[ratio_names].std(),
            'min': self.comparison_data[ratio_names].min(),
            'max': self.comparison_data[ratio_names].max()
        })
        
        return stats
    
    def visualize_comparison(self, ratio_names: List[str],
                           output_path: Optional[str] = None) -> None:
        """
        比較結果を可視化
        
        Parameters:
            ratio_names: 可視化する比率名のリスト
            output_path: 出力ファイルパス（Noneの場合は表示のみ）
        """
        if self.comparison_data.empty:
            self.compare_ratios(ratio_names)
        
        # サブプロット数を計算
        n_ratios = len(ratio_names)
        n_cols = 2
        n_rows = (n_ratios + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        axes = axes.flatten() if n_ratios > 1 else [axes]
        
        for i, ratio in enumerate(ratio_names):
            if ratio in self.comparison_data.columns:
                data = self.comparison_data[ratio].dropna()
                
                # 棒グラフ
                data.plot(kind='bar', ax=axes[i], color='steelblue')
                axes[i].set_title(f'{ratio} Comparison', fontsize=12, fontweight='bold')
                axes[i].set_xlabel('Company', fontsize=10)
                axes[i].set_ylabel(ratio, fontsize=10)
                axes[i].grid(axis='y', alpha=0.3)
                
                # 業界平均線を追加
                avg = data.mean()
                axes[i].axhline(y=avg, color='red', linestyle='--', 
                              label=f'Industry Avg: {avg:.2f}')
                axes[i].legend()
        
        # 未使用のサブプロットを非表示
        for i in range(n_ratios, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {output_path}")
        else:
            plt.show()
    
    def generate_heatmap(self, ratio_names: List[str],
                        output_path: Optional[str] = None) -> None:
        """
        ヒートマップを生成
        
        Parameters:
            ratio_names: ヒートマップに含める比率名のリスト
            output_path: 出力ファイルパス
        """
        if self.comparison_data.empty:
            self.compare_ratios(ratio_names)
        
        # データを標準化（Z-score）
        data = self.comparison_data[ratio_names]
        data_normalized = (data - data.mean()) / data.std()
        
        # ヒートマップ作成
        plt.figure(figsize=(12, 8))
        sns.heatmap(data_normalized.T, annot=True, fmt='.2f', 
                   cmap='RdYlGn', center=0, 
                   cbar_kws={'label': 'Standard Deviations from Mean'})
        
        plt.title('Financial Ratios Heatmap (Standardized)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Company', fontsize=12)
        plt.ylabel('Financial Ratio', fontsize=12)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Heatmap saved to {output_path}")
        else:
            plt.show()
    
    def generate_comparison_report(self) -> str:
        """
        比較レポートを生成
        
        Returns:
            レポート文字列
        """
        if self.comparison_data.empty:
            raise ValueError("No comparison data available")
        
        report = f"""
{'='*70}
業界比較分析レポート
{'='*70}

対象企業: {', '.join(self.tickers)}
分析企業数: {len(self.analyzers)}

主要財務比率の比較
------------------

"""
        
        # 主要比率
        key_ratios = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
        
        for ratio in key_ratios:
            if ratio in self.comparison_data.columns:
                report += f"\n{ratio}:\n"
                
                # ランキング
                ranking = self.generate_ranking(ratio)
                for idx, row in ranking.iterrows():
                    report += f"  {int(row['rank'])}. {idx}: {row[ratio]:.2f}\n"
                
                # 統計
                stats = self.comparison_data[ratio].describe()
                report += f"  平均: {stats['mean']:.2f}\n"
                report += f"  中央値: {stats['50%']:.2f}\n"
                report += f"  標準偏差: {stats['std']:.2f}\n"
        
        report += f"\n{'='*70}\n"
        
        return report
    
    def export_comparison(self, output_dir: str) -> None:
        """
        比較データをエクスポート
        
        Parameters:
            output_dir: 出力ディレクトリ
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # 比較データ
        if not self.comparison_data.empty:
            self.comparison_data.to_csv(
                f"{output_dir}/industry_comparison.csv"
            )
        
        # 業界統計
        ratio_names = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
        stats = self.calculate_industry_statistics(ratio_names)
        stats.to_csv(f"{output_dir}/industry_statistics.csv")
        
        # レポート
        report = self.generate_comparison_report()
        with open(f"{output_dir}/comparison_report.txt", 'w') as f:
            f.write(report)
        
        # 可視化
        self.visualize_comparison(
            ratio_names,
            output_path=f"{output_dir}/comparison_chart.png"
        )
        
        self.generate_heatmap(
            ratio_names,
            output_path=f"{output_dir}/comparison_heatmap.png"
        )
        
        print(f"Comparison data exported to {output_dir}")


def main():
    """メイン実行関数"""
    import yaml
    
    # 設定読み込み
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # テクノロジー企業の比較例
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    
    print("Industry Comparison Analysis")
    print(f"Companies: {', '.join(tickers)}\n")
    
    comparison = IndustryComparison(tickers, config)
    comparison.fetch_all_companies(years=5)
    
    # 比率比較
    ratio_names = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
    comparison.compare_ratios(ratio_names)
    
    # レポート表示
    report = comparison.generate_comparison_report()
    print(report)
    
    # エクスポート
    output_dir = "../data/comparison"
    comparison.export_comparison(output_dir)


if __name__ == "__main__":
    main()
