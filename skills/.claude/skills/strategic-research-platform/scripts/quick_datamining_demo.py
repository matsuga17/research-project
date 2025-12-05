"""
Strategic Management Research Hub - Quick Start Script
======================================================

このスクリプトは、データマイニング分析を最速で開始するための
エントリーポイントです。

使用方法:
    python quick_datamining_demo.py

必要なファイル:
    - データファイル（CSV, Stata, Excel等）
    - datamining_config.yaml（オプション）

出力:
    - ./demo_output/ 以下に全結果が保存されます

Author: Strategic Management Research Hub v3.1
Date: 2025-11-01
"""

import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ロギング設定
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# データ処理ライブラリ
import pandas as pd
import numpy as np

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 本スキルのモジュール
from advanced_strategic_datamining import AdvancedStrategicDataMining
from ml_causal_inference_integrated import CausalMLIntegration


def print_banner():
    """ウェルカムバナー表示"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Strategic Management Research Hub v3.1                      ║
    ║   Quick Start: Data Mining Demo                              ║
    ║                                                               ║
    ║   This demo will run comprehensive data mining analyses      ║
    ║   on your panel data in just a few minutes!                  ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)


def generate_sample_data(n_firms=100, n_years=10):
    """
    サンプルデータ生成（デモ用）
    
    実際の研究では、自分のデータに置き換えてください。
    """
    logger.info("サンプルデータを生成中...")
    
    np.random.seed(42)
    
    data = []
    for firm_id in range(n_firms):
        # 企業固有効果
        firm_effect = np.random.normal(0, 0.02)
        base_rd = np.random.exponential(0.05)
        
        for year in range(2010, 2010 + n_years):
            # 時間トレンド
            time_effect = (year - 2010) * 0.001
            
            # 戦略変数
            rd_intensity = max(0, base_rd + np.random.normal(0, 0.01))
            capital_intensity = np.random.uniform(0.2, 0.8)
            advertising_intensity = np.random.exponential(0.03)
            international_sales = np.random.uniform(0, 0.5)
            
            # パフォーマンス（理論的関係を埋め込み）
            roa = (
                0.05  # ベース
                + 0.3 * rd_intensity  # R&D効果（RBV）
                - 0.05 * capital_intensity  # 資本集約度
                + 0.1 * advertising_intensity  # 差別化
                + firm_effect  # 企業固有
                + time_effect  # 時間トレンド
                + np.random.normal(0, 0.02)  # ノイズ
            )
            
            data.append({
                'firm_id': f'FIRM_{firm_id:03d}',
                'year': year,
                'roa': roa,
                'rd_intensity': rd_intensity,
                'capital_intensity': capital_intensity,
                'advertising_intensity': advertising_intensity,
                'international_sales': international_sales,
                'firm_size': np.random.normal(10, 2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': np.random.randint(5, 50),
                'ma_dummy': np.random.binomial(1, 0.15)  # M&A実施ダミー
            })
    
    df = pd.DataFrame(data)
    
    # 将来パフォーマンス
    df['roa_lead1'] = df.groupby('firm_id')['roa'].shift(-1)
    df['roa_lead2'] = df.groupby('firm_id')['roa'].shift(-2)
    
    # ROA変化
    df['roa_change'] = df.groupby('firm_id')['roa'].diff()
    
    logger.info(f"サンプルデータ生成完了: {len(df)} observations, {df['firm_id'].nunique()} firms")
    
    return df


def run_quick_demo(data_path=None, output_dir='./demo_output/'):
    """
    クイックデモ実行
    
    Args:
        data_path: データファイルパス（Noneならサンプル生成）
        output_dir: 出力ディレクトリ
    """
    print_banner()
    
    # ステップ1: データ読み込み
    logger.info("=" * 60)
    logger.info("STEP 1: データ読み込み")
    logger.info("=" * 60)
    
    if data_path is None:
        # サンプルデータ生成
        df_panel = generate_sample_data(n_firms=100, n_years=10)
        logger.info("→ サンプルデータを使用（デモモード）")
    else:
        # ユーザーデータ読み込み
        if data_path.endswith('.dta'):
            df_panel = pd.read_stata(data_path)
        elif data_path.endswith('.csv'):
            df_panel = pd.read_csv(data_path)
        elif data_path.endswith(('.xls', '.xlsx')):
            df_panel = pd.read_excel(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path}")
        
        logger.info(f"→ データ読み込み完了: {data_path}")
    
    logger.info(f"   {len(df_panel)} observations, {df_panel['firm_id'].nunique()} firms")
    
    # ステップ2: データマイニングエンジン初期化
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: データマイニングエンジン初期化")
    logger.info("=" * 60)
    
    dm = AdvancedStrategicDataMining(
        data=df_panel,
        firm_id='firm_id',
        time_var='year',
        output_dir=output_dir,
        random_state=42
    )
    
    logger.info("→ 初期化完了")
    
    # ステップ3: 戦略的グループ分析
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: 戦略的グループ分析（Strategic Group Analysis）")
    logger.info("=" * 60)
    
    try:
        strategic_features = [
            'rd_intensity',
            'capital_intensity',
            'advertising_intensity',
            'international_sales'
        ]
        
        groups = dm.strategic_group_analysis(
            features=strategic_features,
            n_clusters=4,
            method='kmeans',
            save_results=True
        )
        
        logger.info("→ ✅ 戦略的グループ分析完了")
        logger.info(f"   {groups['n_clusters']} グループを特定")
        logger.info(f"   Silhouette Score: {groups['validation_metrics'].get('silhouette', 'N/A')}")
    
    except Exception as e:
        logger.error(f"→ ❌ 戦略的グループ分析エラー: {e}")
    
    # ステップ4: パフォーマンス予測
    logger.info("\n" + "=" * 60)
    logger.info("STEP 4: パフォーマンス予測（Performance Prediction）")
    logger.info("=" * 60)
    
    try:
        performance_features = [
            'rd_intensity',
            'firm_size',
            'leverage',
            'firm_age'
        ]
        
        predictions = dm.predict_firm_performance(
            target='roa',
            features=performance_features,
            model_type='ensemble',
            test_size=0.2,
            cv_folds=5,
            save_model=True
        )
        
        best_model = predictions['best_model']
        test_r2 = predictions['all_results'][best_model]['metrics']['test_r2']
        
        logger.info("→ ✅ パフォーマンス予測完了")
        logger.info(f"   Best Model: {best_model}")
        logger.info(f"   Test R²: {test_r2:.4f}")
    
    except Exception as e:
        logger.error(f"→ ❌ パフォーマンス予測エラー: {e}")
    
    # ステップ5: 特徴量重要度分析
    logger.info("\n" + "=" * 60)
    logger.info("STEP 5: 特徴量重要度分析（Feature Importance）")
    logger.info("=" * 60)
    
    try:
        importance = dm.analyze_feature_importance(
            target='roa',
            features=performance_features,
            method='ensemble',
            top_n=10
        )
        
        logger.info("→ ✅ 特徴量重要度分析完了")
        logger.info(f"\n   Top 3 Most Important Features:")
        for idx, row in importance.head(3).iterrows():
            logger.info(f"   - {row['feature']}: {row.get('ensemble_importance', row.iloc[1]):.4f}")
    
    except Exception as e:
        logger.error(f"→ ❌ 特徴量重要度分析エラー: {e}")
    
    # ステップ6: 異常検知
    logger.info("\n" + "=" * 60)
    logger.info("STEP 6: 異常検知（Anomaly Detection）")
    logger.info("=" * 60)
    
    try:
        outliers = dm.detect_strategic_outliers(
            features=['roa', 'rd_intensity', 'leverage'],
            method='ensemble',
            contamination=0.05,
            save_results=True
        )
        
        logger.info("→ ✅ 異常検知完了")
        logger.info(f"   {len(outliers)} 社のアウトライア企業を検出")
    
    except Exception as e:
        logger.error(f"→ ❌ 異常検知エラー: {e}")
    
    # ステップ7: 包括的レポート生成
    logger.info("\n" + "=" * 60)
    logger.info("STEP 7: 包括的レポート生成")
    logger.info("=" * 60)
    
    try:
        report_path = dm.generate_comprehensive_report()
        
        logger.info("→ ✅ レポート生成完了")
        logger.info(f"   レポート: {report_path}")
    
    except Exception as e:
        logger.error(f"→ ❌ レポート生成エラー: {e}")
    
    # 完了メッセージ
    logger.info("\n" + "=" * 60)
    logger.info("🎉 データマイニング分析完了！")
    logger.info("=" * 60)
    logger.info(f"\n📁 すべての結果: {output_dir}")
    logger.info(f"📊 HTMLレポート: {output_dir}/datamining_report.html")
    logger.info(f"📈 図表: {output_dir}/*.png")
    logger.info(f"📄 データ: {output_dir}/*.xlsx")
    
    print("\n" + "="*60)
    print("次のステップ:")
    print("1. HTMLレポートをブラウザで開く")
    print("2. 生成された図表を確認")
    print("3. DATAMINING_GUIDE.mdで詳細な使い方を学ぶ")
    print("4. 自分の研究データで分析を実行")
    print("="*60 + "\n")


def run_causal_demo(data_path=None, output_dir='./causal_demo_output/'):
    """
    因果推論デモ実行（オプション）
    
    EconMLがインストールされている場合のみ実行可能
    """
    logger.info("\n" + "=" * 60)
    logger.info("因果推論デモ（Causal Inference Demo）")
    logger.info("=" * 60)
    
    try:
        from econml.dml import CausalForestDML
        
        # データ準備
        if data_path is None:
            df_panel = generate_sample_data(n_firms=150, n_years=10)
        else:
            if data_path.endswith('.dta'):
                df_panel = pd.read_stata(data_path)
            elif data_path.endswith('.csv'):
                df_panel = pd.read_csv(data_path)
        
        # 因果推論システム初期化
        causal = CausalMLIntegration(
            data=df_panel,
            firm_id='firm_id',
            time_var='year',
            output_dir=output_dir
        )
        
        # Causal Forest（異質的処置効果）
        logger.info("\n実行中: Causal Forest...")
        cf_results = causal.causal_forest(
            treatment='ma_dummy',
            outcome='roa_change',
            controls=['firm_size', 'leverage', 'firm_age'],
            heterogeneity_vars=['firm_size', 'rd_intensity'],
            discrete_treatment=True,
            n_estimators=50  # デモ用に少なめ
        )
        
        logger.info("→ ✅ Causal Forest完了")
        logger.info(f"   ATE: {cf_results['ate']:.4f}")
        
        # レポート生成
        causal_report = causal.generate_causal_report()
        logger.info(f"\n📊 因果推論レポート: {causal_report}")
    
    except ImportError:
        logger.warning("❌ EconMLがインストールされていません")
        logger.warning("   因果推論デモをスキップします")
        logger.warning("   インストール: pip install econml")
    
    except Exception as e:
        logger.error(f"❌ 因果推論デモエラー: {e}")


if __name__ == "__main__":
    """
    メイン実行
    
    使用例:
        # サンプルデータでデモ実行
        python quick_datamining_demo.py
        
        # 自分のデータで実行
        python quick_datamining_demo.py --data ./my_data.csv
    """
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Strategic Management Data Mining Quick Start'
    )
    parser.add_argument(
        '--data',
        type=str,
        default=None,
        help='Path to your data file (CSV, Stata, Excel)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./demo_output/',
        help='Output directory for results'
    )
    parser.add_argument(
        '--causal',
        action='store_true',
        help='Run causal inference demo (requires econml)'
    )
    
    args = parser.parse_args()
    
    # メインデモ実行
    run_quick_demo(
        data_path=args.data,
        output_dir=args.output
    )
    
    # 因果推論デモ（オプション）
    if args.causal:
        run_causal_demo(
            data_path=args.data,
            output_dir=os.path.join(args.output, 'causal/')
        )
    
    print("\n✅ All done! Happy researching! 🚀\n")
