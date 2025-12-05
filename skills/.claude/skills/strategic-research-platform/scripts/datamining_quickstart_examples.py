"""
Strategic Management Research Hub - Data Mining Quick Start Examples
=====================================================================

このスクリプトは、データマイニングパイプラインの実行例を提供します。
コピー＆ペーストですぐに使い始められるように設計されています。

実行方法:
  python scripts/datamining_quickstart_examples.py

または、Jupyter Notebookにコピー＆ペーストして実行してください。

Author: Strategic Management Research Hub v3.1
Version: 3.1
Date: 2025-11-01
"""

import sys
from pathlib import Path

# パスの設定
sys.path.insert(0, str(Path(__file__).parent))

from comprehensive_datamining_pipeline import (
    ComprehensiveDataMiningPipeline,
    DataMiningConfig
)
import pandas as pd
import numpy as np


# ============================================================================
# 例1: 最速実行（デフォルト設定）
# ============================================================================

def example_01_quickest_execution():
    """
    最速実行例 - 1コマンドで全分析を実行
    
    実行時間: 2-5分（データサイズによる）
    """
    print("=" * 80)
    print("例1: 最速実行")
    print("=" * 80)
    
    pipeline = ComprehensiveDataMiningPipeline(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./quickstart_output/'
    )
    
    # 全自動実行
    results = pipeline.run_complete_analysis()
    
    print("\n✅ 完了！結果は ./quickstart_output/ に保存されました")
    print(f"HTMLレポート: {pipeline.output_dir / 'comprehensive_report_*.html'}")


# ============================================================================
# 例2: 設定ファイルを使用した実行
# ============================================================================

def example_02_with_config_file():
    """
    設定ファイルを使用した実行
    
    より詳細な設定が可能
    """
    print("=" * 80)
    print("例2: 設定ファイルを使用した実行")
    print("=" * 80)
    
    pipeline = ComprehensiveDataMiningPipeline(
        config_path='./configs/datamining_full_config.yaml'
    )
    
    results = pipeline.run_complete_analysis()
    
    print("\n✅ 完了！")


# ============================================================================
# 例3: 段階的実行（各分析を個別に実行）
# ============================================================================

def example_03_step_by_step():
    """
    段階的実行 - 各分析を個別に実行
    
    より細かい制御が可能
    """
    print("=" * 80)
    print("例3: 段階的実行")
    print("=" * 80)
    
    # 初期化
    pipeline = ComprehensiveDataMiningPipeline(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./step_by_step_output/'
    )
    
    # Phase 1: データ読み込み
    print("\n[Phase 1] データ読み込み...")
    pipeline.load_and_validate_data()
    print(f"✓ {pipeline.results['data_summary']['n_observations']:,} 観測を読み込み")
    
    # Phase 2: 戦略的グループ分析
    print("\n[Phase 2] 戦略的グループ分析...")
    sg_results = pipeline.run_strategic_group_analysis()
    print(f"✓ {sg_results['n_clusters']} グループを特定")
    
    # Phase 3: パフォーマンス予測
    print("\n[Phase 3] パフォーマンス予測...")
    pred_results = pipeline.run_performance_prediction()
    print(f"✓ 最良モデル: {pred_results['best_model']}")
    print(f"  Test R²: {pred_results['model_results'][pred_results['best_model']]['test_r2']:.4f}")
    
    # Phase 4: 特徴量重要度
    print("\n[Phase 4] 特徴量重要度分析...")
    fi_results = pipeline.run_feature_importance_analysis()
    print(f"✓ Top 5 重要特徴量:")
    for feat in fi_results['top_features'][:5]:
        print(f"  - {feat}")
    
    # Phase 5: 異常検知
    print("\n[Phase 5] 異常検知...")
    anomaly_results = pipeline.run_anomaly_detection()
    print(f"✓ {anomaly_results['n_anomalies']} 個の異常値を検出 ({anomaly_results['anomaly_rate']:.1%})")
    
    # Phase 7: 時系列パターン
    print("\n[Phase 7] 時系列パターン分析...")
    temporal_results = pipeline.run_temporal_pattern_analysis()
    print(f"✓ {len(temporal_results)} 変数の時系列パターンを分析")
    
    # Phase 8: 統合レポート
    print("\n[Phase 8] 統合レポート生成...")
    report_path = pipeline.generate_comprehensive_report()
    print(f"✓ レポート: {report_path}")


# ============================================================================
# 例4: カスタム設定での実行
# ============================================================================

def example_04_custom_config():
    """
    カスタム設定での実行
    
    プログラム内で設定を変更
    """
    print("=" * 80)
    print("例4: カスタム設定での実行")
    print("=" * 80)
    
    # カスタム設定の作成
    config = DataMiningConfig(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./custom_output/',
        
        # 独自の戦略的特徴量を指定
        strategic_features=[
            'rd_intensity',
            'patent_intensity',
            'human_capital_intensity',
            'organizational_slack'
        ],
        
        # パフォーマンス指標の変更
        performance_target='tobin_q',
        
        # クラスタ数を固定
        n_clusters=5,
        
        # 予測モデルの選択
        prediction_models=['rf', 'xgboost', 'ensemble'],
        
        # 計算設定
        random_seed=123,
        n_jobs=-1,
        verbose=True
    )
    
    # パイプライン実行
    pipeline = ComprehensiveDataMiningPipeline(config=config)
    results = pipeline.run_complete_analysis()
    
    print("\n✅ カスタム設定での分析完了！")


# ============================================================================
# 例5: 特定の分析のみ実行
# ============================================================================

def example_05_specific_analysis_only():
    """
    特定の分析のみ実行
    
    例: 戦略的グループ分析とパフォーマンス予測のみ
    """
    print("=" * 80)
    print("例5: 特定の分析のみ実行")
    print("=" * 80)
    
    pipeline = ComprehensiveDataMiningPipeline(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./specific_analysis_output/'
    )
    
    # データ読み込み
    pipeline.load_and_validate_data()
    
    # 戦略的グループ分析のみ
    print("\n[戦略的グループ分析]")
    sg_results = pipeline.run_strategic_group_analysis(
        features=['rd_intensity', 'capital_intensity', 'international_sales'],
        n_clusters=4,
        method='kmeans'
    )
    
    print(f"検出されたグループ数: {sg_results['n_clusters']}")
    print(f"シルエットスコア: {sg_results['silhouette_score']:.4f}")
    
    print("\nクラスタプロファイル:")
    print(sg_results['cluster_profiles'])
    
    # パフォーマンス予測のみ
    print("\n[パフォーマンス予測]")
    pred_results = pipeline.run_performance_prediction(
        target='roa',
        features=['rd_intensity', 'firm_size', 'leverage', 'sales_growth'],
        models=['rf', 'xgboost']
    )
    
    print(f"\n最良モデル: {pred_results['best_model']}")
    for model_name, results in pred_results['model_results'].items():
        print(f"  {model_name}:")
        print(f"    Train R²: {results['train_r2']:.4f}")
        print(f"    Test R²: {results['test_r2']:.4f}")


# ============================================================================
# 例6: 因果推論の実行
# ============================================================================

def example_06_causal_inference():
    """
    因果推論の実行
    
    Double Machine Learning を使用した処置効果の推定
    
    注意: EconMLのインストールが必要
      pip install econml
    """
    print("=" * 80)
    print("例6: 因果推論")
    print("=" * 80)
    
    # 設定
    config = DataMiningConfig(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./causal_output/',
        
        # 因果推論の設定
        treatment_var='rd_intensity',  # 処置: R&D投資
        outcome_var='roa_lead1',       # 結果: 翌年のROA
        causal_method='dml',            # Double Machine Learning
        
        control_variables=[
            'firm_size', 'firm_age', 'leverage', 
            'industry_concentration', 'gdp_growth'
        ]
    )
    
    pipeline = ComprehensiveDataMiningPipeline(config=config)
    
    # データ読み込み
    pipeline.load_and_validate_data()
    
    # 因果推論実行
    causal_results = pipeline.run_causal_inference()
    
    if causal_results:
        print(f"\n処置変数: {causal_results['treatment']}")
        print(f"結果変数: {causal_results['outcome']}")
        print(f"平均処置効果 (ATE): {causal_results['ate']:.4f}")
        print(f"95% 信頼区間: [{causal_results['ate_ci'][0]:.4f}, {causal_results['ate_ci'][1]:.4f}]")
        print(f"P値: {causal_results['p_value']:.4f}")
        
        # 解釈
        if causal_results['p_value'] < 0.05:
            print("\n✓ R&D投資は企業パフォーマンスに統計的に有意な因果効果があります")
        else:
            print("\n✗ R&D投資の因果効果は統計的に有意ではありません")


# ============================================================================
# 例7: 異なるクラスタリング手法の比較
# ============================================================================

def example_07_compare_clustering_methods():
    """
    異なるクラスタリング手法の比較
    
    K-Means, 階層的クラスタリング, DBSCANを比較
    """
    print("=" * 80)
    print("例7: クラスタリング手法の比較")
    print("=" * 80)
    
    pipeline = ComprehensiveDataMiningPipeline(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./clustering_comparison/'
    )
    
    # データ読み込み
    pipeline.load_and_validate_data()
    
    # 戦略的特徴量
    features = ['rd_intensity', 'capital_intensity', 'advertising_intensity']
    
    # 各手法で実行
    methods = ['kmeans', 'hierarchical', 'dbscan']
    results_comparison = {}
    
    for method in methods:
        print(f"\n[{method.upper()}]")
        
        try:
            results = pipeline.run_strategic_group_analysis(
                features=features,
                n_clusters=4 if method != 'dbscan' else None,
                method=method
            )
            
            results_comparison[method] = results
            
            if 'silhouette_score' in results:
                print(f"  シルエットスコア: {results['silhouette_score']:.4f}")
            print(f"  検出グループ数: {results['n_clusters']}")
            
        except Exception as e:
            print(f"  エラー: {str(e)}")
    
    # 最良手法の選択
    best_method = max(
        results_comparison.items(),
        key=lambda x: x[1].get('silhouette_score', -1)
    )
    
    print(f"\n✓ 最良の手法: {best_method[0].upper()}")
    print(f"  シルエットスコア: {best_method[1]['silhouette_score']:.4f}")


# ============================================================================
# 例8: 複数のパフォーマンス指標の予測
# ============================================================================

def example_08_multiple_performance_metrics():
    """
    複数のパフォーマンス指標の予測
    
    ROA, ROE, Tobin's Q, Sales Growth を同時に予測
    """
    print("=" * 80)
    print("例8: 複数のパフォーマンス指標の予測")
    print("=" * 80)
    
    pipeline = ComprehensiveDataMiningPipeline(
        data_path='./data/final/analysis_panel.dta',
        output_dir='./multi_metric_output/'
    )
    
    # データ読み込み
    pipeline.load_and_validate_data()
    
    # 各指標で予測
    targets = ['roa', 'roe', 'tobin_q', 'sales_growth']
    features = ['rd_intensity', 'capital_intensity', 'firm_size', 'leverage']
    
    all_results = {}
    
    for target in targets:
        print(f"\n[{target.upper()}]")
        
        if target not in pipeline.data_cleaned.columns:
            print(f"  ✗ {target} が見つかりません。スキップします。")
            continue
        
        results = pipeline.run_performance_prediction(
            target=target,
            features=features,
            models=['rf', 'xgboost']
        )
        
        all_results[target] = results
        
        best_model = results['best_model']
        best_r2 = results['model_results'][best_model]['test_r2']
        
        print(f"  最良モデル: {best_model}")
        print(f"  Test R²: {best_r2:.4f}")
    
    # 結果の比較
    print("\n" + "=" * 80)
    print("パフォーマンス指標別の予測精度:")
    print("=" * 80)
    
    for target, results in all_results.items():
        best_model = results['best_model']
        best_r2 = results['model_results'][best_model]['test_r2']
        print(f"{target:15s}: R² = {best_r2:.4f} ({best_model})")


# ============================================================================
# 例9: 産業別の戦略的グループ分析
# ============================================================================

def example_09_industry_specific_analysis():
    """
    産業別の戦略的グループ分析
    
    各産業で個別にグループ分析を実行
    """
    print("=" * 80)
    print("例9: 産業別の戦略的グループ分析")
    print("=" * 80)
    
    # データ読み込み
    df = pd.read_stata('./data/final/analysis_panel.dta')
    
    # 産業の特定（SIC 2-digit）
    df['industry'] = (df['sic'] // 100).astype(int) if 'sic' in df.columns else 1
    
    industries = df['industry'].unique()[:3]  # 最初の3産業
    
    for ind in industries:
        print(f"\n[産業 {ind}]")
        
        # 産業別データの保存
        ind_data = df[df['industry'] == ind]
        ind_path = f'./temp/industry_{ind}_data.csv'
        ind_data.to_csv(ind_path, index=False)
        
        # 分析実行
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=ind_path,
            output_dir=f'./industry_{ind}_output/'
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_strategic_group_analysis()
        
        print(f"  企業数: {len(ind_data)}")
        print(f"  検出グループ数: {results['n_clusters']}")
        print(f"  シルエットスコア: {results['silhouette_score']:.4f}")


# ============================================================================
# 例10: バッチ処理（複数のデータセットを自動処理）
# ============================================================================

def example_10_batch_processing():
    """
    バッチ処理
    
    複数のデータセットを自動的に処理
    """
    print("=" * 80)
    print("例10: バッチ処理")
    print("=" * 80)
    
    # 処理するデータセットのリスト
    datasets = [
        './data/final/manufacturing_firms.dta',
        './data/final/service_firms.dta',
        './data/final/tech_firms.dta'
    ]
    
    all_results = {}
    
    for data_path in datasets:
        dataset_name = Path(data_path).stem
        print(f"\n[{dataset_name}]")
        
        if not Path(data_path).exists():
            print(f"  ✗ ファイルが見つかりません: {data_path}")
            continue
        
        try:
            pipeline = ComprehensiveDataMiningPipeline(
                data_path=data_path,
                output_dir=f'./batch_output/{dataset_name}/'
            )
            
            results = pipeline.run_complete_analysis()
            all_results[dataset_name] = results
            
            print(f"  ✓ 完了！")
            
        except Exception as e:
            print(f"  ✗ エラー: {str(e)}")
    
    print(f"\n✅ バッチ処理完了！ {len(all_results)} データセットを処理しました")


# ============================================================================
# メイン実行
# ============================================================================

def main():
    """
    例を選択して実行
    """
    print("=" * 80)
    print("Strategic Management Research Hub - Data Mining Examples")
    print("=" * 80)
    print("\n実行可能な例:")
    print("  1. 最速実行")
    print("  2. 設定ファイルを使用した実行")
    print("  3. 段階的実行")
    print("  4. カスタム設定での実行")
    print("  5. 特定の分析のみ実行")
    print("  6. 因果推論の実行")
    print("  7. クラスタリング手法の比較")
    print("  8. 複数のパフォーマンス指標の予測")
    print("  9. 産業別の分析")
    print(" 10. バッチ処理")
    
    choice = input("\n実行する例の番号を入力してください (1-10): ")
    
    examples = {
        '1': example_01_quickest_execution,
        '2': example_02_with_config_file,
        '3': example_03_step_by_step,
        '4': example_04_custom_config,
        '5': example_05_specific_analysis_only,
        '6': example_06_causal_inference,
        '7': example_07_compare_clustering_methods,
        '8': example_08_multiple_performance_metrics,
        '9': example_09_industry_specific_analysis,
        '10': example_10_batch_processing
    }
    
    if choice in examples:
        examples[choice]()
    else:
        print("無効な選択です")


if __name__ == '__main__':
    # すべての例を順次実行する場合
    # main()
    
    # または特定の例を直接実行
    # example_01_quickest_execution()
    # example_03_step_by_step()
    # example_05_specific_analysis_only()
    
    print(__doc__)
    print("\nこのスクリプトの関数を個別に実行するか、")
    print("Jupyter Notebookにコピー＆ペーストしてください。")
