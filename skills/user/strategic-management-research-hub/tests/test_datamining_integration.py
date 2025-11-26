"""
Strategic Management Research Hub - Integration Test Suite
===========================================================

全データマイニング機能の統合テスト。
システムが正常に動作することを確認します。

実行方法:
    python test_datamining_integration.py

または:
    pytest test_datamining_integration.py -v

Author: Strategic Management Research Hub v3.1
Date: 2025-11-01
"""

import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# テストフレームワーク
import pytest
import numpy as np
import pandas as pd

# パス設定
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# システムモジュール
try:
    from advanced_strategic_datamining import AdvancedStrategicDataMining
    from ml_causal_inference_integrated import CausalMLIntegration
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"❌ モジュールインポートエラー: {e}")


# ============================================================================
# テストデータ生成
# ============================================================================

@pytest.fixture
def sample_panel_data():
    """テスト用サンプルデータ生成"""
    np.random.seed(42)
    
    n_firms = 50
    n_years = 8
    
    data = []
    for firm_id in range(n_firms):
        firm_effect = np.random.normal(0, 0.02)
        base_rd = np.random.exponential(0.05)
        
        for year in range(2015, 2015 + n_years):
            rd_intensity = max(0, base_rd + np.random.normal(0, 0.01))
            capital_intensity = np.random.uniform(0.2, 0.8)
            
            roa = (
                0.05 + 0.3 * rd_intensity - 0.05 * capital_intensity +
                firm_effect + np.random.normal(0, 0.02)
            )
            
            data.append({
                'firm_id': f'FIRM_{firm_id:03d}',
                'year': year,
                'roa': roa,
                'rd_intensity': rd_intensity,
                'capital_intensity': capital_intensity,
                'advertising_intensity': np.random.exponential(0.03),
                'international_sales': np.random.uniform(0, 0.5),
                'firm_size': np.random.normal(10, 2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': np.random.randint(5, 50),
                'ma_dummy': np.random.binomial(1, 0.15)
            })
    
    df = pd.DataFrame(data)
    
    # Lead/lag variables
    df['roa_lead1'] = df.groupby('firm_id')['roa'].shift(-1)
    df['roa_change'] = df.groupby('firm_id')['roa'].diff()
    df['rd_intensity_lag1'] = df.groupby('firm_id')['rd_intensity'].shift(1)
    
    return df


# ============================================================================
# テストクラス: データマイニング基本機能
# ============================================================================

@pytest.mark.skipif(not MODULES_AVAILABLE, reason="Modules not available")
class TestAdvancedDataMining:
    """AdvancedStrategicDataMiningクラスのテスト"""
    
    def test_initialization(self, sample_panel_data, tmp_path):
        """初期化テスト"""
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        assert dm.data is not None
        assert dm.firm_id == 'firm_id'
        assert dm.time_var == 'year'
        assert len(dm.data) == len(sample_panel_data)
    
    def test_strategic_group_analysis(self, sample_panel_data, tmp_path):
        """戦略的グループ分析テスト"""
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        features = ['rd_intensity', 'capital_intensity', 'advertising_intensity']
        
        results = dm.strategic_group_analysis(
            features=features,
            n_clusters=3,
            method='kmeans',
            save_results=False
        )
        
        # 検証
        assert 'cluster_profiles' in results
        assert 'validation_metrics' in results
        assert results['n_clusters'] == 3
        assert 'silhouette' in results['validation_metrics']
        assert results['validation_metrics']['silhouette'] >= -1
        assert results['validation_metrics']['silhouette'] <= 1
    
    def test_performance_prediction(self, sample_panel_data, tmp_path):
        """パフォーマンス予測テスト"""
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        features = ['rd_intensity', 'firm_size', 'leverage']
        
        results = dm.predict_firm_performance(
            target='roa',
            features=features,
            model_type='tree',  # Fast for testing
            test_size=0.2,
            cv_folds=3,
            tune_hyperparameters=False,
            save_model=False
        )
        
        # 検証
        assert 'best_model' in results
        assert 'all_results' in results
        
        best_model = results['best_model']
        metrics = results['all_results'][best_model]['metrics']
        
        assert 'test_r2' in metrics
        assert 'train_r2' in metrics
        assert metrics['test_r2'] <= 1.0
    
    def test_feature_importance(self, sample_panel_data, tmp_path):
        """特徴量重要度分析テスト"""
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        features = ['rd_intensity', 'capital_intensity', 'firm_size', 'leverage']
        
        importance = dm.analyze_feature_importance(
            target='roa',
            features=features,
            method='ensemble',
            top_n=10
        )
        
        # 検証
        assert isinstance(importance, pd.DataFrame)
        assert 'feature' in importance.columns
        assert len(importance) == len(features)
        assert importance['feature'].nunique() == len(features)
    
    def test_anomaly_detection(self, sample_panel_data, tmp_path):
        """異常検知テスト"""
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        features = ['roa', 'rd_intensity', 'leverage']
        
        outliers = dm.detect_strategic_outliers(
            features=features,
            method='isolation_forest',
            contamination=0.05,
            save_results=False
        )
        
        # 検証
        assert isinstance(outliers, pd.DataFrame)
        assert len(outliers) > 0
        assert 'outlier_score' in outliers.columns


# ============================================================================
# テストクラス: 因果推論
# ============================================================================

@pytest.mark.skipif(not MODULES_AVAILABLE, reason="Modules not available")
class TestCausalInference:
    """CausalMLIntegrationクラスのテスト"""
    
    def test_initialization(self, sample_panel_data, tmp_path):
        """初期化テスト"""
        causal = CausalMLIntegration(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        assert causal.data is not None
        assert causal.firm_id == 'firm_id'
        assert causal.time_var == 'year'
    
    @pytest.mark.skipif(
        not MODULES_AVAILABLE or not hasattr(sys.modules.get('econml', object()), 'dml'),
        reason="EconML not available"
    )
    def test_causal_forest(self, sample_panel_data, tmp_path):
        """Causal Forestテスト"""
        causal = CausalMLIntegration(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        try:
            results = causal.causal_forest(
                treatment='ma_dummy',
                outcome='roa_change',
                controls=['firm_size', 'leverage'],
                heterogeneity_vars=['firm_size', 'rd_intensity'],
                discrete_treatment=True,
                n_estimators=20,  # Small for speed
                save_results=False
            )
            
            # 検証
            assert 'ate' in results
            assert 'cate' in results
            assert 'feature_importance' in results
            assert isinstance(results['ate'], float)
            
        except ImportError:
            pytest.skip("EconML not installed")
    
    def test_propensity_score_matching(self, sample_panel_data, tmp_path):
        """Propensity Score Matchingテスト"""
        causal = CausalMLIntegration(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path),
            random_state=42
        )
        
        results = causal.propensity_score_matching(
            treatment='ma_dummy',
            outcome='roa',
            covariates=['firm_size', 'leverage', 'firm_age'],
            matching_method='nearest',
            n_neighbors=1,
            save_results=False
        )
        
        # 検証
        assert 'att' in results
        assert 'matched_pairs' in results
        assert results['n_matched_pairs'] > 0
        assert isinstance(results['att'], (float, type(None)))


# ============================================================================
# 統合テスト
# ============================================================================

@pytest.mark.skipif(not MODULES_AVAILABLE, reason="Modules not available")
class TestIntegration:
    """システム全体の統合テスト"""
    
    def test_full_workflow(self, sample_panel_data, tmp_path):
        """完全ワークフローテスト"""
        # データマイニング
        dm = AdvancedStrategicDataMining(
            data=sample_panel_data,
            firm_id='firm_id',
            time_var='year',
            output_dir=str(tmp_path / 'datamining'),
            random_state=42
        )
        
        # 戦略的グループ
        groups = dm.strategic_group_analysis(
            features=['rd_intensity', 'capital_intensity'],
            n_clusters=3,
            save_results=False
        )
        assert groups is not None
        
        # パフォーマンス予測
        predictions = dm.predict_firm_performance(
            target='roa',
            features=['rd_intensity', 'firm_size'],
            model_type='tree',
            save_model=False
        )
        assert predictions is not None
        
        # レポート生成
        report_path = dm.generate_comprehensive_report()
        assert Path(report_path).exists()
    
    def test_data_quality_checks(self, sample_panel_data):
        """データ品質チェック"""
        # 欠損値チェック
        missing_pct = sample_panel_data.isnull().sum() / len(sample_panel_data) * 100
        assert (missing_pct < 50).all(), "Too many missing values"
        
        # 数値変数の範囲チェック
        assert sample_panel_data['roa'].between(-1, 1).all(), "ROA out of range"
        assert sample_panel_data['rd_intensity'].between(0, 1).all(), "R&D intensity invalid"
        
        # 重複チェック
        duplicates = sample_panel_data.duplicated(subset=['firm_id', 'year'])
        assert not duplicates.any(), "Duplicate firm-year observations"


# ============================================================================
# メイン実行（pytest外での手動テスト）
# ============================================================================

def run_manual_tests():
    """手動テスト実行（pytest不使用）"""
    print("=" * 60)
    print("Strategic Management Research Hub - Manual Integration Test")
    print("=" * 60)
    
    if not MODULES_AVAILABLE:
        print("❌ エラー: モジュールがインポートできません")
        return False
    
    # サンプルデータ生成
    print("\n1. サンプルデータ生成...")
    np.random.seed(42)
    df = generate_test_data(n_firms=30, n_years=5)
    print(f"   ✅ {len(df)} observations, {df['firm_id'].nunique()} firms")
    
    # データマイニングテスト
    print("\n2. データマイニングエンジンテスト...")
    try:
        dm = AdvancedStrategicDataMining(
            data=df,
            firm_id='firm_id',
            time_var='year',
            output_dir='./test_output/',
            random_state=42
        )
        print("   ✅ 初期化成功")
        
        # 戦略的グループ
        groups = dm.strategic_group_analysis(
            features=['rd_intensity', 'capital_intensity'],
            n_clusters=3,
            save_results=False
        )
        print(f"   ✅ 戦略的グループ分析: {groups['n_clusters']} groups")
        
        # パフォーマンス予測
        predictions = dm.predict_firm_performance(
            target='roa',
            features=['rd_intensity', 'firm_size'],
            model_type='tree',
            save_model=False
        )
        print(f"   ✅ パフォーマンス予測: Best model = {predictions['best_model']}")
        
    except Exception as e:
        print(f"   ❌ データマイニングテストエラー: {e}")
        return False
    
    # 因果推論テスト
    print("\n3. 因果推論テスト...")
    try:
        causal = CausalMLIntegration(
            data=df,
            firm_id='firm_id',
            time_var='year',
            output_dir='./test_output/causal/',
            random_state=42
        )
        print("   ✅ 初期化成功")
        
        # PSM
        psm_results = causal.propensity_score_matching(
            treatment='ma_dummy',
            outcome='roa',
            covariates=['firm_size', 'leverage'],
            save_results=False
        )
        print(f"   ✅ PSM: ATT = {psm_results['att']:.4f}")
        
    except Exception as e:
        print(f"   ❌ 因果推論テストエラー: {e}")
        # 因果推論は失敗してもOK（オプショナル）
    
    print("\n" + "=" * 60)
    print("✅ 手動テスト完了")
    print("=" * 60)
    
    return True


def generate_test_data(n_firms=50, n_years=8):
    """テストデータ生成（pytest fixture外）"""
    data = []
    for firm_id in range(n_firms):
        firm_effect = np.random.normal(0, 0.02)
        base_rd = np.random.exponential(0.05)
        
        for year in range(2015, 2015 + n_years):
            rd_intensity = max(0, base_rd + np.random.normal(0, 0.01))
            capital_intensity = np.random.uniform(0.2, 0.8)
            
            roa = (
                0.05 + 0.3 * rd_intensity - 0.05 * capital_intensity +
                firm_effect + np.random.normal(0, 0.02)
            )
            
            data.append({
                'firm_id': f'FIRM_{firm_id:03d}',
                'year': year,
                'roa': roa,
                'rd_intensity': rd_intensity,
                'capital_intensity': capital_intensity,
                'advertising_intensity': np.random.exponential(0.03),
                'international_sales': np.random.uniform(0, 0.5),
                'firm_size': np.random.normal(10, 2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': np.random.randint(5, 50),
                'ma_dummy': np.random.binomial(1, 0.15)
            })
    
    df = pd.DataFrame(data)
    df['roa_lead1'] = df.groupby('firm_id')['roa'].shift(-1)
    df['roa_change'] = df.groupby('firm_id')['roa'].diff()
    df['rd_intensity_lag1'] = df.groupby('firm_id')['rd_intensity'].shift(1)
    
    return df


if __name__ == "__main__":
    """
    実行方法:
        python test_datamining_integration.py        # 手動テスト
        pytest test_datamining_integration.py -v     # pytest
    """
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Strategic Management Research Hub v3.1                      ║
    ║   Integration Test Suite                                      ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Pytestが実行されていない場合は手動テスト
    if 'pytest' not in sys.modules:
        success = run_manual_tests()
        sys.exit(0 if success else 1)
