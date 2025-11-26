"""
Strategic Management Research Hub - Data Mining Test Suite
===========================================================

データマイニングパイプラインの品質保証のための包括的テストスイート

実行方法:
  pytest tests/test_datamining_pipeline.py -v
  
  または
  
  python tests/test_datamining_pipeline.py

依存関係:
  pip install pytest pytest-cov pytest-mock

Author: Strategic Management Research Hub v3.1
Version: 3.1
Date: 2025-11-01
"""

import unittest
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import shutil
import sys

# パスの設定
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from comprehensive_datamining_pipeline import (
    ComprehensiveDataMiningPipeline,
    DataMiningConfig
)


# ============================================================================
# テストデータ生成
# ============================================================================

@pytest.fixture
def sample_data():
    """
    テスト用のサンプルデータを生成
    
    パネルデータ（企業 × 年次）を模擬
    """
    np.random.seed(42)
    
    n_firms = 100
    n_years = 5
    
    data = []
    for firm_id in range(1, n_firms + 1):
        for year in range(2015, 2015 + n_years):
            row = {
                'gvkey': firm_id,
                'year': year,
                'roa': np.random.normal(0.05, 0.03),
                'roe': np.random.normal(0.10, 0.05),
                'rd_intensity': np.random.uniform(0, 0.2),
                'capital_intensity': np.random.uniform(0.1, 0.5),
                'advertising_intensity': np.random.uniform(0, 0.1),
                'international_sales': np.random.uniform(0, 0.8),
                'firm_size': np.random.normal(10, 2),
                'firm_age': np.random.randint(5, 50),
                'leverage': np.random.uniform(0, 0.8),
                'sales_growth': np.random.normal(0.05, 0.10)
            }
            data.append(row)
    
    return pd.DataFrame(data)


@pytest.fixture
def temp_data_file(sample_data):
    """
    一時データファイルを作成
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        sample_data.to_csv(f.name, index=False)
        return f.name


@pytest.fixture
def temp_output_dir():
    """
    一時出力ディレクトリを作成
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


# ============================================================================
# 設定クラスのテスト
# ============================================================================

class TestDataMiningConfig(unittest.TestCase):
    """DataMiningConfig クラスのテスト"""
    
    def test_config_initialization(self):
        """設定の初期化テスト"""
        config = DataMiningConfig(data_path='./test_data.csv')
        
        self.assertEqual(config.firm_id, 'gvkey')
        self.assertEqual(config.time_var, 'year')
        self.assertEqual(config.performance_target, 'roa')
        self.assertIsNotNone(config.strategic_features)
    
    def test_config_from_dict(self):
        """辞書からの設定作成テスト"""
        config_dict = {
            'data_path': './test.csv',
            'n_clusters': 5,
            'random_seed': 123
        }
        
        config = DataMiningConfig(**config_dict)
        
        self.assertEqual(config.data_path, './test.csv')
        self.assertEqual(config.n_clusters, 5)
        self.assertEqual(config.random_seed, 123)
    
    def test_config_to_yaml(self):
        """YAML保存テスト"""
        config = DataMiningConfig(data_path='./test.csv')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config.to_yaml(f.name)
            
            # 読み込みテスト
            config_loaded = DataMiningConfig.from_yaml(f.name)
            self.assertEqual(config_loaded.data_path, config.data_path)


# ============================================================================
# パイプライン初期化のテスト
# ============================================================================

class TestPipelineInitialization(unittest.TestCase):
    """パイプラインの初期化テスト"""
    
    def test_initialization_with_data_path(self):
        """データパスでの初期化"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path='./test_data.csv',
            output_dir='./test_output/'
        )
        
        self.assertIsNotNone(pipeline.config)
        self.assertEqual(pipeline.config.data_path, './test_data.csv')
    
    def test_initialization_with_config(self):
        """設定オブジェクトでの初期化"""
        config = DataMiningConfig(data_path='./test_data.csv')
        pipeline = ComprehensiveDataMiningPipeline(config=config)
        
        self.assertEqual(pipeline.config, config)
    
    def test_output_directory_creation(self):
        """出力ディレクトリの作成テスト"""
        with tempfile.TemporaryDirectory() as temp_dir:
            pipeline = ComprehensiveDataMiningPipeline(
                data_path='./test_data.csv',
                output_dir=temp_dir
            )
            
            self.assertTrue(Path(temp_dir).exists())
            self.assertTrue((Path(temp_dir) / 'figures').exists())
            self.assertTrue((Path(temp_dir) / 'tables').exists())
            self.assertTrue((Path(temp_dir) / 'models').exists())


# ============================================================================
# データ読み込みのテスト
# ============================================================================

class TestDataLoading:
    """データ読み込み機能のテスト"""
    
    def test_load_csv(self, temp_data_file, temp_output_dir):
        """CSVファイルの読み込みテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        data = pipeline.load_and_validate_data()
        
        assert data is not None
        assert len(data) > 0
        assert 'gvkey' in data.columns
        assert 'year' in data.columns
    
    def test_data_validation(self, temp_data_file, temp_output_dir):
        """データ検証テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        data = pipeline.load_and_validate_data()
        
        # 必須変数の存在確認
        assert 'gvkey' in data.columns
        assert 'year' in data.columns
        
        # データサマリーの確認
        assert 'data_summary' in pipeline.results
        assert pipeline.results['data_summary']['n_observations'] > 0
    
    def test_data_cleaning(self, temp_data_file, temp_output_dir):
        """データクリーニングテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        data = pipeline.load_and_validate_data()
        
        # クリーニング後のデータが存在
        assert pipeline.data_cleaned is not None
        
        # 外れ値処理の確認（極端な値が除去されているはず）
        for col in data.select_dtypes(include=[np.number]).columns:
            if col not in ['gvkey', 'year']:
                # 標準偏差が合理的な範囲内
                assert data[col].std() < 1000


# ============================================================================
# 戦略的グループ分析のテスト
# ============================================================================

class TestStrategicGroupAnalysis:
    """戦略的グループ分析のテスト"""
    
    def test_clustering_execution(self, temp_data_file, temp_output_dir):
        """クラスタリングの実行テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_strategic_group_analysis(
            features=['rd_intensity', 'capital_intensity'],
            n_clusters=3
        )
        
        assert results is not None
        assert 'n_clusters' in results
        assert results['n_clusters'] == 3
        assert 'silhouette_score' in results
    
    def test_optimal_clusters_detection(self, temp_data_file, temp_output_dir):
        """最適クラスタ数の自動決定テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_strategic_group_analysis(
            features=['rd_intensity', 'capital_intensity', 'advertising_intensity'],
            n_clusters=None  # 自動決定
        )
        
        assert results['n_clusters'] >= 2
        assert results['n_clusters'] <= 10
    
    def test_cluster_profiles(self, temp_data_file, temp_output_dir):
        """クラスタプロファイルの生成テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_strategic_group_analysis(
            features=['rd_intensity', 'capital_intensity'],
            n_clusters=3
        )
        
        assert 'cluster_profiles' in results
        profiles = results['cluster_profiles']
        
        assert len(profiles) == 3
        assert 'cluster' in profiles.columns
        assert 'size' in profiles.columns


# ============================================================================
# パフォーマンス予測のテスト
# ============================================================================

class TestPerformancePrediction:
    """パフォーマンス予測のテスト"""
    
    def test_prediction_execution(self, temp_data_file, temp_output_dir):
        """予測モデルの実行テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_performance_prediction(
            target='roa',
            features=['rd_intensity', 'firm_size', 'leverage'],
            models=['rf']
        )
        
        assert results is not None
        assert 'model_results' in results
        assert 'best_model' in results
        assert 'rf' in results['model_results']
    
    def test_model_performance_metrics(self, temp_data_file, temp_output_dir):
        """モデル性能指標のテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_performance_prediction(
            target='roa',
            features=['rd_intensity', 'firm_size'],
            models=['rf']
        )
        
        rf_results = results['model_results']['rf']
        
        assert 'train_r2' in rf_results
        assert 'test_r2' in rf_results
        assert 'train_rmse' in rf_results
        assert 'test_rmse' in rf_results
        
        # R²は-1から1の範囲
        assert -1 <= rf_results['test_r2'] <= 1
    
    def test_multiple_models(self, temp_data_file, temp_output_dir):
        """複数モデルの比較テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_performance_prediction(
            target='roa',
            features=['rd_intensity', 'firm_size'],
            models=['rf', 'gbm']
        )
        
        assert len(results['model_results']) >= 2
        assert 'rf' in results['model_results']
        assert 'gbm' in results['model_results']


# ============================================================================
# 特徴量重要度のテスト
# ============================================================================

class TestFeatureImportance:
    """特徴量重要度分析のテスト"""
    
    def test_importance_calculation(self, temp_data_file, temp_output_dir):
        """重要度計算のテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        pipeline.run_performance_prediction(
            target='roa',
            features=['rd_intensity', 'capital_intensity', 'firm_size'],
            models=['rf']
        )
        
        results = pipeline.run_feature_importance_analysis()
        
        assert results is not None
        assert 'importance_df' in results
        assert len(results['importance_df']) > 0
    
    def test_importance_ranking(self, temp_data_file, temp_output_dir):
        """重要度ランキングのテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        pipeline.run_performance_prediction(models=['rf'])
        results = pipeline.run_feature_importance_analysis()
        
        importance_df = results['importance_df']
        
        # 重要度が降順にソート
        importances = importance_df['importance'].values
        assert all(importances[i] >= importances[i+1] for i in range(len(importances)-1))


# ============================================================================
# 異常検知のテスト
# ============================================================================

class TestAnomalyDetection:
    """異常検知のテスト"""
    
    def test_anomaly_detection_execution(self, temp_data_file, temp_output_dir):
        """異常検知の実行テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_anomaly_detection(
            features=['rd_intensity', 'capital_intensity'],
            contamination=0.1
        )
        
        assert results is not None
        assert 'n_anomalies' in results
        assert 'anomaly_rate' in results
        assert results['n_anomalies'] > 0
    
    def test_anomaly_identification(self, temp_data_file, temp_output_dir):
        """異常値の特定テスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_anomaly_detection(contamination=0.05)
        
        # 異常値割合が設定値付近
        assert 0 < results['anomaly_rate'] < 0.2
        
        # 異常値DataFrameが存在
        assert 'anomaly_df' in results


# ============================================================================
# 時系列パターン分析のテスト
# ============================================================================

class TestTemporalPatternAnalysis:
    """時系列パターン分析のテスト"""
    
    def test_temporal_trends(self, temp_data_file, temp_output_dir):
        """時系列トレンドのテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        results = pipeline.run_temporal_pattern_analysis()
        
        assert results is not None
        assert len(results) > 0
        
        # 各変数のトレンドが存在
        for var in pipeline.config.strategic_features:
            if var in results:
                trend = results[var]
                assert 'mean' in trend.columns
                assert 'std' in trend.columns


# ============================================================================
# 統合レポート生成のテスト
# ============================================================================

class TestReportGeneration:
    """統合レポート生成のテスト"""
    
    def test_html_report_generation(self, temp_data_file, temp_output_dir):
        """HTMLレポート生成のテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.load_and_validate_data()
        pipeline.run_strategic_group_analysis()
        pipeline.run_performance_prediction()
        
        report_path = pipeline.generate_comprehensive_report()
        
        assert Path(report_path).exists()
        assert Path(report_path).suffix == '.html'
        
        # ファイルサイズが0より大きい
        assert Path(report_path).stat().st_size > 0


# ============================================================================
# 完全パイプラインのテスト
# ============================================================================

class TestCompletePipeline:
    """完全パイプラインのテスト"""
    
    def test_complete_analysis(self, temp_data_file, temp_output_dir):
        """全自動分析のテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        results = pipeline.run_complete_analysis()
        
        assert results is not None
        assert 'data_summary' in results
        assert 'strategic_groups' in results
        assert 'performance_prediction' in results
        
        # HTMLレポートが生成されている
        report_files = list(Path(temp_output_dir).glob('comprehensive_report_*.html'))
        assert len(report_files) > 0
    
    def test_execution_time_tracking(self, temp_data_file, temp_output_dir):
        """実行時間追跡のテスト"""
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=temp_data_file,
            output_dir=temp_output_dir
        )
        
        pipeline.run_complete_analysis()
        
        assert len(pipeline.execution_times) > 0
        
        # 各フェーズの実行時間が記録されている
        for phase, duration in pipeline.execution_times.items():
            assert duration >= 0


# ============================================================================
# エラーハンドリングのテスト
# ============================================================================

class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングのテスト"""
    
    def test_invalid_data_path(self):
        """無効なデータパスのテスト"""
        with self.assertRaises(Exception):
            pipeline = ComprehensiveDataMiningPipeline(
                data_path='./nonexistent_file.csv'
            )
            pipeline.load_and_validate_data()
    
    def test_missing_required_variables(self, sample_data, temp_output_dir):
        """必須変数欠損のテスト"""
        # firm_idを削除
        data = sample_data.drop(columns=['gvkey'])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            data.to_csv(f.name, index=False)
            
            with self.assertRaises(ValueError):
                pipeline = ComprehensiveDataMiningPipeline(
                    data_path=f.name,
                    output_dir=temp_output_dir
                )
                pipeline.load_and_validate_data()


# ============================================================================
# パフォーマンステスト
# ============================================================================

class TestPerformance:
    """パフォーマンステスト"""
    
    def test_large_dataset_handling(self, temp_output_dir):
        """大規模データセットの処理テスト"""
        # 大規模データの生成
        np.random.seed(42)
        n_observations = 10000
        
        data = pd.DataFrame({
            'gvkey': np.repeat(range(1, 2001), 5),
            'year': np.tile(range(2015, 2020), 2000),
            'roa': np.random.normal(0.05, 0.03, n_observations),
            'rd_intensity': np.random.uniform(0, 0.2, n_observations),
            'capital_intensity': np.random.uniform(0.1, 0.5, n_observations),
            'firm_size': np.random.normal(10, 2, n_observations),
            'leverage': np.random.uniform(0, 0.8, n_observations)
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            data.to_csv(f.name, index=False)
            
            import time
            start_time = time.time()
            
            pipeline = ComprehensiveDataMiningPipeline(
                data_path=f.name,
                output_dir=temp_output_dir
            )
            
            pipeline.load_and_validate_data()
            pipeline.run_strategic_group_analysis()
            
            elapsed_time = time.time() - start_time
            
            # 10,000観測の処理が2分以内
            assert elapsed_time < 120


# ============================================================================
# メイン実行
# ============================================================================

if __name__ == '__main__':
    # pytest実行
    pytest.main([__file__, '-v', '--tb=short'])
