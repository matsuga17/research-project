"""
US Corporate Analytics - 可視化スクリプト

財務データの高度な可視化機能を提供します。
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class FinancialVisualizer:
    """財務データ可視化クラス"""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        初期化
        
        Parameters:
            style: matplotlibスタイル
        """
        plt.style.use('default')
        sns.set_palette("husl")
        self.figsize = (12, 6)
        
    def plot_trend(self, data: pd.DataFrame, 
                   columns: List[str],
                   title: str = "Financial Trend",
                   ylabel: str = "Value",
                   save_path: Optional[str] = None) -> None:
        """
        時系列トレンドプロット
        
        Parameters:
            data: データFrame
            columns: プロットする列名のリスト
            title: グラフタイトル
            ylabel: Y軸ラベル
            save_path: 保存パス
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for col in columns:
            if col in data.columns:
                ax.plot(data.index, data[col], 
                       marker='o', linewidth=2.5, 
                       markersize=8, label=col)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend(loc='best', fontsize=10, frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_comparison_bars(self, data: pd.DataFrame,
                            metric: str,
                            title: str = "Company Comparison",
                            save_path: Optional[str] = None) -> None:
        """
        企業比較棒グラフ
        
        Parameters:
            data: データFrame（index=会社名, columns=指標）
            metric: 比較する指標
            title: グラフタイトル
            save_path: 保存パス
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if metric in data.columns:
            data[metric].plot(kind='bar', ax=ax, color='steelblue', 
                            edgecolor='black', linewidth=1.5)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Company', fontsize=12)
            ax.set_ylabel(metric, fontsize=12)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # 値ラベルを追加
            for i, v in enumerate(data[metric]):
                ax.text(i, v, f'{v:.2f}', 
                       ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_radar_chart(self, data: pd.DataFrame,
                        metrics: List[str],
                        title: str = "Performance Radar",
                        save_path: Optional[str] = None) -> None:
        """
        レーダーチャート（複数企業比較）
        
        Parameters:
            data: データFrame（index=会社名, columns=指標）
            metrics: プロットする指標のリスト
            title: グラフタイトル
            save_path: 保存パス
        """
        # データの正規化（0-100スケール）
        normalized_data = data[metrics].copy()
        for col in metrics:
            min_val = normalized_data[col].min()
            max_val = normalized_data[col].max()
            if max_val > min_val:
                normalized_data[col] = ((normalized_data[col] - min_val) / 
                                       (max_val - min_val)) * 100
        
        # レーダーチャート作成
        num_vars = len(metrics)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # 閉じる
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        for idx, company in enumerate(normalized_data.index):
            values = normalized_data.loc[company].tolist()
            values += values[:1]  # 閉じる
            
            ax.plot(angles, values, 'o-', linewidth=2, 
                   label=company, markersize=8)
            ax.fill(angles, values, alpha=0.15)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, size=10)
        ax.set_ylim(0, 100)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=10)
        ax.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_heatmap(self, data: pd.DataFrame,
                    title: str = "Correlation Heatmap",
                    annot: bool = True,
                    save_path: Optional[str] = None) -> None:
        """
        相関ヒートマップ
        
        Parameters:
            data: データFrame
            title: グラフタイトル
            annot: 相関係数を表示するか
            save_path: 保存パス
        """
        # 数値列のみ抽出
        numeric_data = data.select_dtypes(include=[np.number])
        
        # 相関行列を計算
        corr_matrix = numeric_data.corr()
        
        # ヒートマップ作成
        fig, ax = plt.subplots(figsize=(12, 10))
        
        sns.heatmap(corr_matrix, annot=annot, fmt='.2f', 
                   cmap='coolwarm', center=0,
                   square=True, linewidths=1, 
                   cbar_kws={"shrink": 0.8},
                   ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_scatter_with_regression(self, data: pd.DataFrame,
                                    x_col: str, y_col: str,
                                    title: str = "Scatter Plot",
                                    hue: Optional[str] = None,
                                    save_path: Optional[str] = None) -> None:
        """
        回帰線付き散布図
        
        Parameters:
            data: データFrame
            x_col: X軸の列名
            y_col: Y軸の列名
            title: グラフタイトル
            hue: カテゴリ分け列名
            save_path: 保存パス
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if hue:
            sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue,
                          s=100, alpha=0.7, ax=ax)
        else:
            sns.scatterplot(data=data, x=x_col, y=y_col,
                          s=100, alpha=0.7, ax=ax)
        
        # 回帰線を追加
        sns.regplot(data=data, x=x_col, y=y_col,
                   scatter=False, color='red', ax=ax)
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_distribution(self, data: pd.DataFrame,
                         column: str,
                         title: str = "Distribution",
                         bins: int = 30,
                         save_path: Optional[str] = None) -> None:
        """
        分布図（ヒストグラム + KDE）
        
        Parameters:
            data: データFrame
            column: 列名
            title: グラフタイトル
            bins: ビン数
            save_path: 保存パス
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if column in data.columns:
            sns.histplot(data=data, x=column, bins=bins, 
                        kde=True, ax=ax, color='steelblue')
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel(column, fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ グラフを保存: {save_path}")
        
        plt.show()
    
    def plot_dashboard(self, data: pd.DataFrame,
                      metrics: Dict[str, str],
                      save_path: Optional[str] = None) -> None:
        """
        ダッシュボード（複数指標の統合可視化）
        
        Parameters:
            data: データFrame
            metrics: {metric_name: column_name} の辞書
            save_path: 保存パス
        """
        num_metrics = len(metrics)
        rows = (num_metrics + 1) // 2
        cols = 2
        
        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
        axes = axes.flatten() if num_metrics > 1 else [axes]
        
        for i, (metric_name, col_name) in enumerate(metrics.items()):
            if col_name in data.columns:
                axes[i].plot(data.index, data[col_name], 
                           marker='o', linewidth=2.5, markersize=8)
                axes[i].set_title(metric_name, fontsize=14, fontweight='bold')
                axes[i].set_xlabel('Year', fontsize=10)
                axes[i].set_ylabel(metric_name, fontsize=10)
                axes[i].grid(True, alpha=0.3, linestyle='--')
        
        # 余ったサブプロットを非表示
        for j in range(i + 1, len(axes)):
            axes[j].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ ダッシュボードを保存: {save_path}")
        
        plt.show()


def demo():
    """デモ実行"""
    # サンプルデータ作成
    years = pd.Index([2019, 2020, 2021, 2022, 2023], name='year')
    
    data = pd.DataFrame({
        'ROA': [15.2, 16.1, 17.3, 18.5, 19.2],
        'ROE': [45.3, 48.2, 52.1, 55.8, 58.3],
        'net_margin': [21.5, 22.3, 23.8, 25.1, 26.2],
        'current_ratio': [1.5, 1.6, 1.7, 1.8, 1.9],
        'debt_ratio': [0.65, 0.62, 0.58, 0.55, 0.52]
    }, index=years)
    
    # 可視化器の初期化
    visualizer = FinancialVisualizer()
    
    print("=== 財務データ可視化デモ ===\n")
    
    # トレンドプロット
    print("1. トレンドプロット")
    visualizer.plot_trend(data, ['ROA', 'ROE'], 
                         title="Profitability Trend",
                         ylabel="Ratio (%)")
    
    # ダッシュボード
    print("\n2. ダッシュボード")
    metrics = {
        'ROA (%)': 'ROA',
        'ROE (%)': 'ROE',
        'Net Margin (%)': 'net_margin',
        'Current Ratio': 'current_ratio'
    }
    visualizer.plot_dashboard(data, metrics)


if __name__ == "__main__":
    demo()
