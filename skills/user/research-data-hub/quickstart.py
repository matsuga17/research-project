#!/usr/bin/env python3
"""
US Corporate Analytics - クイックスタートガイド

このスクリプトを実行することで、基本的な使い方を学べます。
"""

import os
import sys
import yaml

# パスの設定
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.company_analyzer import CompanyAnalyzer


def print_banner():
    """バナーを表示"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          US Corporate Analytics - Quick Start               ║
║          米国企業財務・ガバナンス分析スキル                   ║
║                                                              ║
║          Version 1.0.0                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def load_config():
    """設定を読み込み"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("✓ 設定ファイル読み込み完了")
        return config
    except FileNotFoundError:
        print("✗ エラー: config/config.yaml が見つかりません")
        sys.exit(1)
    except Exception as e:
        print(f"✗ エラー: 設定ファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def quick_demo(config):
    """クイックデモを実行"""
    print("\n" + "="*70)
    print("クイックデモ: Apple Inc. (AAPL) の財務分析")
    print("="*70 + "\n")
    
    ticker = "AAPL"
    
    try:
        # アナライザー初期化
        print(f"1. {ticker} のデータ取得中...")
        analyzer = CompanyAnalyzer(ticker, config)
        
        # データ取得
        analyzer.fetch_all_data(years=5)
        print(f"   ✓ データ取得完了\n")
        
        # パフォーマンス分析
        print("2. パフォーマンス分析中...")
        analysis = analyzer.analyze_performance()
        print(f"   ✓ 分析完了\n")
        
        # 結果表示
        print("3. 分析結果:")
        print(f"   企業評価: {analysis['performance_rating']}")
        print(f"   最新年度: {analysis['latest_year']}")
        
        print("\n   主要財務比率:")
        key_ratios = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
        for ratio in key_ratios:
            if ratio in analysis['latest_ratios']:
                value = analysis['latest_ratios'][ratio]
                print(f"   - {ratio}: {value:.2f}")
        
        # レポート生成
        print("\n4. サマリーレポート生成中...")
        report = analyzer.generate_summary_report()
        print(report)
        
        # データエクスポート
        print("5. データをエクスポート中...")
        output_dir = "./quick_demo_output"
        analyzer.export_data(output_dir)
        print(f"   ✓ データを {output_dir} に保存しました")
        
        print("\n" + "="*70)
        print("✓ デモ完了！")
        print("="*70)
        
        print("\n次のステップ:")
        print("  1. examples/USAGE_EXAMPLES.md を参照して、より高度な使用例を学ぶ")
        print("  2. scripts/company_analyzer.py をカスタマイズして、独自の分析を実行")
        print("  3. templates/ のExcelテンプレートを使用して、レポートを作成")
        
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        print("\nトラブルシューティング:")
        print("  1. インターネット接続を確認してください")
        print("  2. SEC EDGAR APIキーが正しく設定されているか確認してください")
        print("  3. config/config.yaml の設定を確認してください")
        sys.exit(1)


def interactive_mode(config):
    """対話モード"""
    print("\n" + "="*70)
    print("対話モード")
    print("="*70 + "\n")
    
    while True:
        print("\n何をしますか？")
        print("  1. 企業の財務分析")
        print("  2. 業界比較分析")
        print("  3. ガバナンス分析")
        print("  4. クイックデモを再実行")
        print("  0. 終了")
        
        choice = input("\n選択してください (0-4): ").strip()
        
        if choice == "0":
            print("\nUS Corporate Analyticsを終了します。")
            break
        elif choice == "1":
            ticker = input("ティッカーシンボルを入力してください (例: AAPL): ").strip().upper()
            analyze_company(ticker, config)
        elif choice == "2":
            tickers_str = input("ティッカーシンボルをカンマ区切りで入力してください (例: AAPL,MSFT,GOOGL): ").strip().upper()
            tickers = [t.strip() for t in tickers_str.split(',')]
            compare_companies(tickers, config)
        elif choice == "3":
            ticker = input("ティッカーシンボルを入力してください (例: AAPL): ").strip().upper()
            analyze_governance(ticker, config)
        elif choice == "4":
            quick_demo(config)
        else:
            print("無効な選択です。0-4の数字を入力してください。")


def analyze_company(ticker, config):
    """企業分析"""
    print(f"\n{ticker} を分析中...")
    
    try:
        analyzer = CompanyAnalyzer(ticker, config)
        analyzer.fetch_all_data(years=5)
        
        report = analyzer.generate_summary_report()
        print(report)
        
        save = input("\nレポートを保存しますか？ (y/n): ").strip().lower()
        if save == 'y':
            output_dir = f"./output/{ticker}"
            analyzer.export_data(output_dir)
            print(f"✓ レポートを {output_dir} に保存しました")
            
    except Exception as e:
        print(f"✗ エラー: {e}")


def compare_companies(tickers, config):
    """業界比較"""
    from scripts.industry_comparison import IndustryComparison
    
    print(f"\n{len(tickers)}社を比較中...")
    
    try:
        comparison = IndustryComparison(tickers, config)
        comparison.fetch_all_companies(years=5)
        
        report = comparison.generate_comparison_report()
        print(report)
        
        save = input("\n比較結果を保存しますか？ (y/n): ").strip().lower()
        if save == 'y':
            output_dir = "./output/comparison"
            comparison.export_comparison(output_dir)
            print(f"✓ 比較結果を {output_dir} に保存しました")
            
    except Exception as e:
        print(f"✗ エラー: {e}")


def analyze_governance(ticker, config):
    """ガバナンス分析"""
    from utils.governance_analyzer import GovernanceAnalyzer
    from utils.sec_client import SECEdgarClient
    
    print(f"\n{ticker} のガバナンスを分析中...")
    
    try:
        sec_client = SECEdgarClient(
            api_key=config['sec_edgar']['api_key'],
            user_agent=config['sec_edgar']['user_agent']
        )
        
        analyzer = GovernanceAnalyzer(sec_client)
        cik = sec_client.get_company_cik(ticker)
        
        report = analyzer.generate_governance_report(cik, ticker, 2023)
        print(report)
        
    except Exception as e:
        print(f"✗ エラー: {e}")


def main():
    """メイン関数"""
    print_banner()
    
    # 設定読み込み
    config = load_config()
    
    # モード選択
    print("\nモードを選択してください:")
    print("  1. クイックデモ（推奨）")
    print("  2. 対話モード")
    print("  0. 終了")
    
    mode = input("\n選択してください (0-2): ").strip()
    
    if mode == "0":
        print("\nUS Corporate Analyticsを終了します。")
        sys.exit(0)
    elif mode == "1":
        quick_demo(config)
        
        # デモ後に対話モードに移行するか確認
        continue_choice = input("\n対話モードに移行しますか？ (y/n): ").strip().lower()
        if continue_choice == 'y':
            interactive_mode(config)
    elif mode == "2":
        interactive_mode(config)
    else:
        print("無効な選択です。")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nプログラムを中断しました。")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n予期しないエラーが発生しました: {e}")
        sys.exit(1)
