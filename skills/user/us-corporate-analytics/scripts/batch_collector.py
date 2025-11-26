"""
US Corporate Analytics - バッチデータ収集スクリプト

複数企業のデータを一括で取得します。
"""

import sys
import os
import pandas as pd
from typing import List
import yaml
from datetime import datetime
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sec_client import SECEdgarClient
from utils.worldbank_client import WorldBankClient
from utils.financial_ratios import FinancialRatioCalculator
from scripts.company_analyzer import CompanyAnalyzer


class BatchDataCollector:
    """バッチデータ収集クラス"""
    
    def __init__(self, config: dict):
        """
        初期化
        
        Parameters:
            config: 設定辞書
        """
        self.config = config
        self.sec_client = SECEdgarClient(
            api_key=config['sec_edgar']['api_key'],
            user_agent=config['sec_edgar']['user_agent']
        )
        self.results = []
        
    def collect_multiple_companies(self, tickers: List[str], 
                                   years: int = 5) -> pd.DataFrame:
        """
        複数企業のデータを一括収集
        
        Parameters:
            tickers: ティッカーシンボルのリスト
            years: 取得する年数
            
        Returns:
            統合データのDataFrame
        """
        print(f"\n{'='*60}")
        print(f"バッチデータ収集開始")
        print(f"{'='*60}")
        print(f"対象企業数: {len(tickers)}")
        print(f"取得期間: 過去{years}年\n")
        
        all_data = []
        failed_companies = []
        
        for i, ticker in enumerate(tickers, 1):
            print(f"[{i}/{len(tickers)}] Processing {ticker}...", end=' ')
            
            try:
                # データ取得
                analyzer = CompanyAnalyzer(ticker, self.config)
                analyzer.fetch_all_data(years=years)
                
                # 財務比率を取得
                ratios = analyzer.financial_ratios
                
                if not ratios.empty:
                    # ティッカー情報を追加
                    ratios['ticker'] = ticker
                    ratios['company_cik'] = analyzer.cik
                    all_data.append(ratios)
                    print("✓")
                else:
                    print("✗ (データなし)")
                    failed_companies.append((ticker, "データなし"))
                    
            except Exception as e:
                print(f"✗ (エラー: {e})")
                failed_companies.append((ticker, str(e)))
        
        print(f"\n{'='*60}")
        print(f"収集完了")
        print(f"{'='*60}")
        print(f"成功: {len(all_data)}/{len(tickers)}企業")
        
        if failed_companies:
            print(f"失敗: {len(failed_companies)}企業")
            print("\n失敗した企業:")
            for ticker, reason in failed_companies:
                print(f"  - {ticker}: {reason}")
        
        # 統合
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=False)
            return combined_df
        else:
            return pd.DataFrame()
    
    def collect_by_industry(self, sic_code: str, 
                           max_companies: int = 50,
                           years: int = 5) -> pd.DataFrame:
        """
        業界別データ収集
        
        Parameters:
            sic_code: SIC産業分類コード
            max_companies: 最大企業数
            years: 取得する年数
            
        Returns:
            業界データのDataFrame
        """
        print(f"\n業界別データ収集 (SIC: {sic_code})")
        print(f"最大企業数: {max_companies}")
        
        # 実装: SICコードから企業リストを取得
        # ここではプレースホルダー
        tickers = []  # 実際にはSICコードから企業を抽出
        
        return self.collect_multiple_companies(tickers[:max_companies], years)
    
    def save_results(self, df: pd.DataFrame, output_dir: str,
                    filename: str = None) -> None:
        """
        結果を保存
        
        Parameters:
            df: データFrame
            output_dir: 出力ディレクトリ
            filename: ファイル名（Noneの場合は自動生成）
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_data_{timestamp}.csv"
        
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path)
        
        print(f"\n✓ データを保存しました: {output_path}")
        print(f"  - 行数: {len(df)}")
        print(f"  - 列数: {len(df.columns)}")
        print(f"  - ファイルサイズ: {os.path.getsize(output_path) / 1024:.2f} KB")


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description='複数企業のデータを一括収集'
    )
    parser.add_argument(
        '--tickers',
        type=str,
        required=True,
        help='ティッカーシンボル（カンマ区切り、例: AAPL,MSFT,GOOGL）'
    )
    parser.add_argument(
        '--years',
        type=int,
        default=5,
        help='取得する年数（デフォルト: 5）'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='../data/processed',
        help='出力ディレクトリ'
    )
    parser.add_argument(
        '--filename',
        type=str,
        help='出力ファイル名'
    )
    
    args = parser.parse_args()
    
    # ティッカーリストをパース
    tickers = [t.strip().upper() for t in args.tickers.split(',')]
    
    # 設定読み込み
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'config', 
        'config.yaml'
    )
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # バッチ収集実行
    collector = BatchDataCollector(config)
    data = collector.collect_multiple_companies(tickers, args.years)
    
    # 保存
    if not data.empty:
        collector.save_results(data, args.output_dir, args.filename)
    else:
        print("\n✗ 収集可能なデータがありませんでした")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n処理を中断しました")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nエラーが発生しました: {e}")
        sys.exit(1)
