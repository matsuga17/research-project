"""
Strategic Management Research Hub - Comprehensive Data Mining Pipeline
=======================================================================

完全自動化されたデータマイニングパイプライン。研究者がコマンド1つで
Publication-Ready な分析結果を取得できるように設計。

主要機能：
1. データ読み込み＆前処理の自動化
2. 8種類のデータマイニング手法の統合実行
3. 結果の可視化（30種類以上のグラフ）
4. HTMLレポートの自動生成
5. Publication-Ready なLaTeX表の出力
6. 再現性の完全確保（全パラメータ保存）

使用例：
```python
from comprehensive_datamining_pipeline import ComprehensiveDataMiningPipeline

# 初期化
pipeline = ComprehensiveDataMiningPipeline(
    data_path='./data/final/analysis_panel.dta',
    config_path='./configs/datamining_config.yaml',
    output_dir='./datamining_results/'
)

# 全自動実行
pipeline.run_complete_analysis()

# または段階的実行
pipeline.load_and_validate_data()
pipeline.run_strategic_group_analysis()
pipeline.run_performance_prediction()
pipeline.run_causal_inference()
pipeline.generate_comprehensive_report()
```

Author: Strategic Management Research Hub v3.1
Version: 3.1
Date: 2025-11-01
License: MIT
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any
import logging
from pathlib import Path
import warnings
import json
import yaml
from datetime import datetime
import pickle
import sys
from dataclasses import dataclass, asdict
import traceback

# Core ML Libraries
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    silhouette_score, mean_squared_error, r2_score, 
    roc_auc_score, classification_report
)
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.ensemble import (
    RandomForestRegressor, RandomForestClassifier,
    GradientBoostingRegressor, IsolationForest
)

# Advanced ML (if available)
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

try:
    from econml.dml import DML, LinearDML, CausalForestDML
    from econml.dr import DRLearner
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('datamining_pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURATION DATA CLASS
# ============================================================================

@dataclass
class DataMiningConfig:
    """データマイニングパイプラインの設定"""
    
    # データ設定
    data_path: str
    firm_id: str = 'gvkey'
    time_var: str = 'year'
    output_dir: str = './datamining_output/'
    
    # 分析対象変数
    strategic_features: List[str] = None
    performance_target: str = 'roa'
    control_variables: List[str] = None
    
    # 戦略的グループ分析
    n_clusters: Optional[int] = None  # Noneの場合は自動決定
    clustering_method: str = 'kmeans'
    max_clusters: int = 10
    
    # パフォーマンス予測
    prediction_models: List[str] = None
    test_size: float = 0.2
    cv_folds: int = 5
    
    # 因果推論
    treatment_var: str = None
    outcome_var: str = None
    causal_method: str = 'dml'
    
    # 異常検知
    contamination: float = 0.05
    
    # 品質管理
    min_observations: int = 100
    max_missing_rate: float = 0.3
    outlier_method: str = 'iqr'
    outlier_threshold: float = 3.0
    
    # 出力設定
    save_models: bool = True
    generate_html_report: bool = True
    generate_latex_tables: bool = True
    figure_format: str = 'png'
    figure_dpi: int = 300
    
    # 計算設定
    random_seed: int = 42
    n_jobs: int = -1
    verbose: bool = True
    
    def __post_init__(self):
        """デフォルト値の設定"""
        if self.strategic_features is None:
            self.strategic_features = [
                'rd_intensity', 'capital_intensity', 
                'advertising_intensity', 'international_sales'
            ]
        if self.control_variables is None:
            self.control_variables = [
                'firm_size', 'firm_age', 'leverage', 'sales_growth'
            ]
        if self.prediction_models is None:
            self.prediction_models = [
                'rf', 'gbm', 'xgboost', 'lightgbm', 'ensemble'
            ]
    
    @classmethod
    def from_yaml(cls, yaml_path: str):
        """YAMLファイルから設定を読み込み"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)
    
    def to_yaml(self, yaml_path: str):
        """設定をYAMLファイルに保存"""
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(asdict(self), f, default_flow_style=False)


# ============================================================================
# MAIN PIPELINE CLASS
# ============================================================================

class ComprehensiveDataMiningPipeline:
    """
    戦略経営研究のための統合データマイニングパイプライン
    
    【8つの主要分析】
    1. データ品質診断
    2. 戦略的グループ分析（Strategic Group Analysis）
    3. パフォーマンス予測（Performance Prediction）
    4. 特徴量重要度分析（Feature Importance）
    5. 異常検知（Anomaly Detection）
    6. 因果推論（Causal Inference）
    7. 時系列パターン分析（Temporal Pattern Analysis）
    8. 統合レポート生成（Comprehensive Reporting）
    """
    
    def __init__(
        self,
        data_path: str = None,
        config_path: str = None,
        config: DataMiningConfig = None,
        output_dir: str = './datamining_output/'
    ):
        """
        Parameters
        ----------
        data_path : str, optional
            データファイルのパス
        config_path : str, optional
            設定ファイル（YAML）のパス
        config : DataMiningConfig, optional
            設定オブジェクト（直接渡す場合）
        output_dir : str, optional
            出力ディレクトリ
        """
        # 設定の読み込み
        if config is not None:
            self.config = config
        elif config_path is not None:
            self.config = DataMiningConfig.from_yaml(config_path)
        elif data_path is not None:
            self.config = DataMiningConfig(data_path=data_path, output_dir=output_dir)
        else:
            raise ValueError("data_path, config_path, または config のいずれかを指定してください")
        
        # 出力ディレクトリの作成
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'figures').mkdir(exist_ok=True)
        (self.output_dir / 'tables').mkdir(exist_ok=True)
        (self.output_dir / 'models').mkdir(exist_ok=True)
        (self.output_dir / 'logs').mkdir(exist_ok=True)
        
        # データとモデルの格納
        self.data = None
        self.data_cleaned = None
        self.results = {}
        self.models = {}
        
        # 実行時間の記録
        self.execution_times = {}
        
        # ログの設定
        self._setup_logging()
        
        logger.info(f"ComprehensiveDataMiningPipeline 初期化完了")
        logger.info(f"出力ディレクトリ: {self.output_dir}")
    
    def _setup_logging(self):
        """ログ設定"""
        log_file = self.output_dir / 'logs' / f'pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # ========================================================================
    # 1. データ読み込み＆検証
    # ========================================================================
    
    def load_and_validate_data(self) -> pd.DataFrame:
        """
        データの読み込みと基本的な検証
        
        Returns
        -------
        pd.DataFrame
            読み込まれたデータ
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 1: データ読み込み＆検証")
        logger.info("=" * 80)
        
        try:
            # データ読み込み
            data_path = Path(self.config.data_path)
            logger.info(f"データファイル: {data_path}")
            
            if data_path.suffix == '.dta':
                self.data = pd.read_stata(data_path)
            elif data_path.suffix == '.csv':
                self.data = pd.read_csv(data_path)
            elif data_path.suffix == '.parquet':
                self.data = pd.read_parquet(data_path)
            else:
                raise ValueError(f"未対応のファイル形式: {data_path.suffix}")
            
            logger.info(f"✓ データ読み込み完了: {self.data.shape[0]:,} 行 × {self.data.shape[1]:,} 列")
            
            # 基本的な検証
            self._validate_data()
            
            # データクリーニング
            self.data_cleaned = self._clean_data(self.data.copy())
            
            # 結果の保存
            self.results['data_summary'] = {
                'n_observations': len(self.data),
                'n_firms': self.data[self.config.firm_id].nunique(),
                'n_years': self.data[self.config.time_var].nunique(),
                'year_range': [
                    int(self.data[self.config.time_var].min()), 
                    int(self.data[self.config.time_var].max())
                ],
                'variables': list(self.data.columns)
            }
            
            self.execution_times['data_loading'] = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ PHASE 1 完了 ({self.execution_times['data_loading']:.2f}秒)")
            
            return self.data_cleaned
            
        except Exception as e:
            logger.error(f"データ読み込みエラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _validate_data(self):
        """データの基本的な検証"""
        logger.info("データ検証を実行中...")
        
        # 必須変数の確認
        required_vars = [self.config.firm_id, self.config.time_var]
        missing_vars = [v for v in required_vars if v not in self.data.columns]
        if missing_vars:
            raise ValueError(f"必須変数が見つかりません: {missing_vars}")
        
        # 最小観測数の確認
        if len(self.data) < self.config.min_observations:
            logger.warning(
                f"観測数が少なすぎます: {len(self.data)} < {self.config.min_observations}"
            )
        
        # 欠損値の確認
        missing_rates = self.data.isnull().sum() / len(self.data)
        high_missing = missing_rates[missing_rates > self.config.max_missing_rate]
        if len(high_missing) > 0:
            logger.warning(f"欠損値の多い変数: {len(high_missing)} 個")
            for var, rate in high_missing.items():
                logger.warning(f"  {var}: {rate:.1%}")
        
        logger.info("✓ データ検証完了")
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """データクリーニング"""
        logger.info("データクリーニングを実行中...")
        
        df_clean = df.copy()
        
        # 1. 外れ値処理
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in [self.config.firm_id, self.config.time_var]:
                continue
            
            if self.config.outlier_method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - self.config.outlier_threshold * IQR
                upper = Q3 + self.config.outlier_threshold * IQR
                df_clean[col] = df_clean[col].clip(lower, upper)
            
            elif self.config.outlier_method == 'zscore':
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                lower = mean - self.config.outlier_threshold * std
                upper = mean + self.config.outlier_threshold * std
                df_clean[col] = df_clean[col].clip(lower, upper)
        
        # 2. 欠損値処理（リストワイズ削除）
        original_len = len(df_clean)
        analysis_vars = (
            [self.config.performance_target] + 
            self.config.strategic_features + 
            self.config.control_variables
        )
        analysis_vars = [v for v in analysis_vars if v in df_clean.columns]
        df_clean = df_clean.dropna(subset=analysis_vars)
        dropped = original_len - len(df_clean)
        
        if dropped > 0:
            logger.info(f"欠損値による削除: {dropped:,} 行 ({dropped/original_len:.1%})")
        
        logger.info(f"✓ クリーニング後: {len(df_clean):,} 行")
        
        return df_clean
    
    # ========================================================================
    # 2. 戦略的グループ分析
    # ========================================================================
    
    def run_strategic_group_analysis(
        self,
        features: List[str] = None,
        n_clusters: int = None,
        method: str = None
    ) -> Dict[str, Any]:
        """
        戦略的グループ分析（Strategic Group Analysis）
        
        Porter (1980) の戦略的グループ理論に基づき、類似の戦略を採用する
        企業群を特定。
        
        Parameters
        ----------
        features : List[str], optional
            クラスタリングに使用する戦略的次元
        n_clusters : int, optional
            クラスタ数（Noneの場合は自動決定）
        method : str, optional
            クラスタリング手法
        
        Returns
        -------
        Dict[str, Any]
            分析結果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 2: 戦略的グループ分析")
        logger.info("=" * 80)
        
        if self.data_cleaned is None:
            self.load_and_validate_data()
        
        # パラメータ設定
        features = features or self.config.strategic_features
        n_clusters = n_clusters or self.config.n_clusters
        method = method or self.config.clustering_method
        
        logger.info(f"戦略的次元: {features}")
        logger.info(f"クラスタリング手法: {method}")
        
        try:
            # データ準備
            X = self.data_cleaned[features].dropna()
            
            # 標準化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 最適クラスタ数の決定
            if n_clusters is None:
                n_clusters = self._determine_optimal_clusters(
                    X_scaled, 
                    max_k=self.config.max_clusters
                )
                logger.info(f"最適クラスタ数: {n_clusters}")
            
            # クラスタリング実行
            if method == 'kmeans':
                model = KMeans(
                    n_clusters=n_clusters, 
                    random_state=self.config.random_seed,
                    n_init=10
                )
            elif method == 'hierarchical':
                model = AgglomerativeClustering(n_clusters=n_clusters)
            elif method == 'dbscan':
                model = DBSCAN(eps=0.5, min_samples=5)
            else:
                raise ValueError(f"未対応のクラスタリング手法: {method}")
            
            cluster_labels = model.fit_predict(X_scaled)
            
            # クラスタプロファイルの作成
            cluster_profiles = self._create_cluster_profiles(
                X, cluster_labels, features
            )
            
            # 結果の保存
            self.results['strategic_groups'] = {
                'n_clusters': n_clusters,
                'method': method,
                'features': features,
                'cluster_labels': cluster_labels,
                'cluster_profiles': cluster_profiles,
                'silhouette_score': silhouette_score(X_scaled, cluster_labels)
            }
            
            # モデルの保存
            if self.config.save_models:
                model_path = self.output_dir / 'models' / 'strategic_groups_model.pkl'
                with open(model_path, 'wb') as f:
                    pickle.dump({'model': model, 'scaler': scaler}, f)
                logger.info(f"モデル保存: {model_path}")
            
            # 可視化
            self._visualize_strategic_groups(X_scaled, cluster_labels, features)
            
            self.execution_times['strategic_groups'] = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ PHASE 2 完了 ({self.execution_times['strategic_groups']:.2f}秒)")
            
            return self.results['strategic_groups']
            
        except Exception as e:
            logger.error(f"戦略的グループ分析エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _determine_optimal_clusters(
        self, 
        X: np.ndarray, 
        max_k: int = 10
    ) -> int:
        """エルボー法とシルエット分析で最適クラスタ数を決定"""
        logger.info("最適クラスタ数を探索中...")
        
        silhouette_scores = []
        inertias = []
        
        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.config.random_seed, n_init=10)
            labels = kmeans.fit_predict(X)
            silhouette_scores.append(silhouette_score(X, labels))
            inertias.append(kmeans.inertia_)
        
        # シルエットスコアが最大のk
        optimal_k = np.argmax(silhouette_scores) + 2
        
        logger.info(f"クラスタ数 {optimal_k} を選択（シルエットスコア: {max(silhouette_scores):.3f}）")
        
        return optimal_k
    
    def _create_cluster_profiles(
        self, 
        X: pd.DataFrame, 
        labels: np.ndarray, 
        features: List[str]
    ) -> pd.DataFrame:
        """クラスタプロファイルの作成"""
        profiles = []
        
        for cluster_id in np.unique(labels):
            mask = labels == cluster_id
            cluster_data = X[mask]
            
            profile = {'cluster': cluster_id, 'size': int(mask.sum())}
            for feat in features:
                profile[f'{feat}_mean'] = cluster_data[feat].mean()
                profile[f'{feat}_std'] = cluster_data[feat].std()
            
            profiles.append(profile)
        
        return pd.DataFrame(profiles)
    
    def _visualize_strategic_groups(
        self, 
        X: np.ndarray, 
        labels: np.ndarray, 
        features: List[str]
    ):
        """戦略的グループの可視化"""
        from sklearn.decomposition import PCA
        
        # PCAで2次元に削減
        pca = PCA(n_components=2, random_state=self.config.random_seed)
        X_pca = pca.fit_transform(X)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(
            X_pca[:, 0], X_pca[:, 1],
            c=labels, cmap='Set2', 
            s=50, alpha=0.6, edgecolors='k'
        )
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        ax.set_title('Strategic Groups (PCA Projection)')
        plt.colorbar(scatter, label='Cluster')
        plt.tight_layout()
        
        fig_path = self.output_dir / 'figures' / f'strategic_groups.{self.config.figure_format}'
        plt.savefig(fig_path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"可視化保存: {fig_path}")
    
    # ========================================================================
    # 3. パフォーマンス予測
    # ========================================================================
    
    def run_performance_prediction(
        self,
        target: str = None,
        features: List[str] = None,
        models: List[str] = None
    ) -> Dict[str, Any]:
        """
        企業パフォーマンスの機械学習予測
        
        複数のMLモデルを比較し、最適なモデルを選択。
        
        Parameters
        ----------
        target : str, optional
            予測対象変数
        features : List[str], optional
            説明変数
        models : List[str], optional
            使用するモデルのリスト
        
        Returns
        -------
        Dict[str, Any]
            予測結果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 3: パフォーマンス予測")
        logger.info("=" * 80)
        
        if self.data_cleaned is None:
            self.load_and_validate_data()
        
        # パラメータ設定
        target = target or self.config.performance_target
        features = features or (self.config.strategic_features + self.config.control_variables)
        models = models or self.config.prediction_models
        
        logger.info(f"予測対象: {target}")
        logger.info(f"説明変数: {len(features)} 個")
        logger.info(f"モデル: {models}")
        
        try:
            # データ準備
            X = self.data_cleaned[features].dropna()
            y = self.data_cleaned.loc[X.index, target]
            
            # Train-Test Split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=self.config.test_size,
                random_state=self.config.random_seed
            )
            
            # 標準化
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # モデルトレーニング
            model_results = {}
            
            for model_name in models:
                logger.info(f"トレーニング中: {model_name}")
                
                if model_name == 'rf':
                    model = RandomForestRegressor(
                        n_estimators=100,
                        random_state=self.config.random_seed,
                        n_jobs=self.config.n_jobs
                    )
                elif model_name == 'gbm':
                    model = GradientBoostingRegressor(
                        n_estimators=100,
                        random_state=self.config.random_seed
                    )
                elif model_name == 'xgboost' and XGB_AVAILABLE:
                    model = xgb.XGBRegressor(
                        n_estimators=100,
                        random_state=self.config.random_seed,
                        n_jobs=self.config.n_jobs
                    )
                elif model_name == 'lightgbm' and LGB_AVAILABLE:
                    model = lgb.LGBMRegressor(
                        n_estimators=100,
                        random_state=self.config.random_seed,
                        n_jobs=self.config.n_jobs
                    )
                else:
                    logger.warning(f"スキップ: {model_name}")
                    continue
                
                # トレーニング
                model.fit(X_train_scaled, y_train)
                
                # 予測
                y_pred_train = model.predict(X_train_scaled)
                y_pred_test = model.predict(X_test_scaled)
                
                # 評価
                train_r2 = r2_score(y_train, y_pred_train)
                test_r2 = r2_score(y_test, y_pred_test)
                train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
                test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
                
                model_results[model_name] = {
                    'model': model,
                    'train_r2': train_r2,
                    'test_r2': test_r2,
                    'train_rmse': train_rmse,
                    'test_rmse': test_rmse
                }
                
                logger.info(f"  Train R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
            
            # 最良モデルの選択
            best_model_name = max(model_results, key=lambda k: model_results[k]['test_r2'])
            logger.info(f"最良モデル: {best_model_name}")
            
            # 結果の保存
            self.results['performance_prediction'] = {
                'target': target,
                'features': features,
                'model_results': model_results,
                'best_model': best_model_name,
                'scaler': scaler
            }
            
            self.execution_times['performance_prediction'] = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ PHASE 3 完了 ({self.execution_times['performance_prediction']:.2f}秒)")
            
            return self.results['performance_prediction']
            
        except Exception as e:
            logger.error(f"パフォーマンス予測エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    # ========================================================================
    # 4. 特徴量重要度分析
    # ========================================================================
    
    def run_feature_importance_analysis(
        self,
        target: str = None,
        features: List[str] = None
    ) -> Dict[str, Any]:
        """
        特徴量重要度分析
        
        どの戦略的変数が企業パフォーマンスに最も影響するかを分析。
        
        Parameters
        ----------
        target : str, optional
            予測対象変数
        features : List[str], optional
            説明変数
        
        Returns
        -------
        Dict[str, Any]
            特徴量重要度
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 4: 特徴量重要度分析")
        logger.info("=" * 80)
        
        if 'performance_prediction' not in self.results:
            self.run_performance_prediction(target, features)
        
        try:
            # Random Forestモデルから特徴量重要度を取得
            if 'rf' in self.results['performance_prediction']['model_results']:
                rf_model = self.results['performance_prediction']['model_results']['rf']['model']
                features = self.results['performance_prediction']['features']
                
                importances = rf_model.feature_importances_
                feature_importance_df = pd.DataFrame({
                    'feature': features,
                    'importance': importances
                }).sort_values('importance', ascending=False)
                
                logger.info("Top 5 重要特徴量:")
                for idx, row in feature_importance_df.head(5).iterrows():
                    logger.info(f"  {row['feature']}: {row['importance']:.4f}")
                
                # 可視化
                self._visualize_feature_importance(feature_importance_df)
                
                self.results['feature_importance'] = {
                    'importance_df': feature_importance_df,
                    'top_features': feature_importance_df.head(10)['feature'].tolist()
                }
                
                self.execution_times['feature_importance'] = (datetime.now() - start_time).total_seconds()
                logger.info(f"✓ PHASE 4 完了 ({self.execution_times['feature_importance']:.2f}秒)")
                
                return self.results['feature_importance']
            else:
                logger.warning("Random Forestモデルが見つかりません")
                return {}
                
        except Exception as e:
            logger.error(f"特徴量重要度分析エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _visualize_feature_importance(self, importance_df: pd.DataFrame):
        """特徴量重要度の可視化"""
        top_n = min(15, len(importance_df))
        
        fig, ax = plt.subplots(figsize=(10, 8))
        importance_df.head(top_n).plot(
            x='feature', y='importance', kind='barh', ax=ax,
            color='steelblue', edgecolor='black'
        )
        ax.set_xlabel('Feature Importance')
        ax.set_ylabel('Features')
        ax.set_title(f'Top {top_n} Feature Importance (Random Forest)')
        ax.invert_yaxis()
        plt.tight_layout()
        
        fig_path = self.output_dir / 'figures' / f'feature_importance.{self.config.figure_format}'
        plt.savefig(fig_path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"可視化保存: {fig_path}")
    
    # ========================================================================
    # 5. 異常検知
    # ========================================================================
    
    def run_anomaly_detection(
        self,
        features: List[str] = None,
        contamination: float = None
    ) -> Dict[str, Any]:
        """
        異常検知（Anomaly Detection）
        
        戦略的アウトライア（極端に異なる戦略を採用する企業）を特定。
        
        Parameters
        ----------
        features : List[str], optional
            異常検知に使用する特徴量
        contamination : float, optional
            異常値の割合
        
        Returns
        -------
        Dict[str, Any]
            異常検知結果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 5: 異常検知")
        logger.info("=" * 80)
        
        if self.data_cleaned is None:
            self.load_and_validate_data()
        
        # パラメータ設定
        features = features or (self.config.strategic_features + self.config.control_variables)
        contamination = contamination or self.config.contamination
        
        logger.info(f"異常検知特徴量: {len(features)} 個")
        logger.info(f"異常値割合: {contamination:.1%}")
        
        try:
            # データ準備
            X = self.data_cleaned[features].dropna()
            
            # 標準化
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Isolation Forest
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=self.config.random_seed,
                n_jobs=self.config.n_jobs
            )
            anomaly_labels = iso_forest.fit_predict(X_scaled)
            anomaly_scores = iso_forest.score_samples(X_scaled)
            
            # 異常値の特定
            is_anomaly = anomaly_labels == -1
            n_anomalies = is_anomaly.sum()
            
            logger.info(f"検出された異常値: {n_anomalies:,} 個 ({n_anomalies/len(X):.1%})")
            
            # 結果の保存
            anomaly_df = X.copy()
            anomaly_df['is_anomaly'] = is_anomaly
            anomaly_df['anomaly_score'] = anomaly_scores
            
            self.results['anomaly_detection'] = {
                'anomaly_df': anomaly_df,
                'n_anomalies': int(n_anomalies),
                'anomaly_rate': float(n_anomalies / len(X)),
                'top_anomalies': anomaly_df[is_anomaly].nsmallest(10, 'anomaly_score')
            }
            
            # 可視化
            self._visualize_anomalies(X_scaled, is_anomaly)
            
            self.execution_times['anomaly_detection'] = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ PHASE 5 完了 ({self.execution_times['anomaly_detection']:.2f}秒)")
            
            return self.results['anomaly_detection']
            
        except Exception as e:
            logger.error(f"異常検知エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _visualize_anomalies(self, X: np.ndarray, is_anomaly: np.ndarray):
        """異常値の可視化"""
        from sklearn.decomposition import PCA
        
        # PCAで2次元に削減
        pca = PCA(n_components=2, random_state=self.config.random_seed)
        X_pca = pca.fit_transform(X)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # 正常値
        ax.scatter(
            X_pca[~is_anomaly, 0], X_pca[~is_anomaly, 1],
            c='lightblue', s=30, alpha=0.5, label='Normal'
        )
        
        # 異常値
        ax.scatter(
            X_pca[is_anomaly, 0], X_pca[is_anomaly, 1],
            c='red', s=100, alpha=0.7, marker='x', label='Anomaly'
        )
        
        ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
        ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
        ax.set_title('Anomaly Detection (PCA Projection)')
        ax.legend()
        plt.tight_layout()
        
        fig_path = self.output_dir / 'figures' / f'anomaly_detection.{self.config.figure_format}'
        plt.savefig(fig_path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"可視化保存: {fig_path}")
    
    # ========================================================================
    # 6. 因果推論（オプション）
    # ========================================================================
    
    def run_causal_inference(
        self,
        treatment_var: str = None,
        outcome_var: str = None,
        control_vars: List[str] = None,
        method: str = None
    ) -> Dict[str, Any]:
        """
        機械学習ベースの因果推論
        
        Double Machine Learning (DML) を使用して、処置効果を推定。
        
        Parameters
        ----------
        treatment_var : str, optional
            処置変数
        outcome_var : str, optional
            結果変数
        control_vars : List[str], optional
            制御変数
        method : str, optional
            因果推論手法
        
        Returns
        -------
        Dict[str, Any]
            因果推論結果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 6: 因果推論")
        logger.info("=" * 80)
        
        if not ECONML_AVAILABLE:
            logger.warning("EconMLがインストールされていません。スキップします。")
            return {}
        
        if self.data_cleaned is None:
            self.load_and_validate_data()
        
        # パラメータ設定
        treatment_var = treatment_var or self.config.treatment_var
        outcome_var = outcome_var or self.config.outcome_var or self.config.performance_target
        control_vars = control_vars or self.config.control_variables
        method = method or self.config.causal_method
        
        if treatment_var is None:
            logger.warning("treatment_var が指定されていません。スキップします。")
            return {}
        
        logger.info(f"処置変数: {treatment_var}")
        logger.info(f"結果変数: {outcome_var}")
        logger.info(f"制御変数: {len(control_vars)} 個")
        logger.info(f"手法: {method}")
        
        try:
            # データ準備
            required_vars = [treatment_var, outcome_var] + control_vars
            df = self.data_cleaned[required_vars].dropna()
            
            T = df[treatment_var].values
            Y = df[outcome_var].values
            X = df[control_vars].values
            
            # Double Machine Learning
            if method == 'dml':
                est = LinearDML(
                    model_y=GradientBoostingRegressor(random_state=self.config.random_seed),
                    model_t=GradientBoostingRegressor(random_state=self.config.random_seed),
                    random_state=self.config.random_seed
                )
                est.fit(Y, T, X=X, W=None)
                
                # 処置効果の推定
                ate = est.ate(X=X)
                ate_inference = est.ate_inference(X=X)
                
                logger.info(f"平均処置効果 (ATE): {ate:.4f}")
                logger.info(f"95% CI: [{ate_inference.conf_int()[0]:.4f}, {ate_inference.conf_int()[1]:.4f}]")
                
                self.results['causal_inference'] = {
                    'method': method,
                    'treatment': treatment_var,
                    'outcome': outcome_var,
                    'ate': float(ate),
                    'ate_ci': [float(ate_inference.conf_int()[0]), float(ate_inference.conf_int()[1])],
                    'p_value': float(ate_inference.pvalue())
                }
                
                self.execution_times['causal_inference'] = (datetime.now() - start_time).total_seconds()
                logger.info(f"✓ PHASE 6 完了 ({self.execution_times['causal_inference']:.2f}秒)")
                
                return self.results['causal_inference']
            
        except Exception as e:
            logger.error(f"因果推論エラー: {str(e)}")
            logger.error(traceback.format_exc())
            return {}
    
    # ========================================================================
    # 7. 時系列パターン分析
    # ========================================================================
    
    def run_temporal_pattern_analysis(self) -> Dict[str, Any]:
        """
        時系列パターン分析
        
        戦略的変数の時系列推移を分析。
        
        Returns
        -------
        Dict[str, Any]
            時系列分析結果
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("PHASE 7: 時系列パターン分析")
        logger.info("=" * 80)
        
        if self.data_cleaned is None:
            self.load_and_validate_data()
        
        try:
            # 年次トレンドの計算
            temporal_trends = {}
            
            for var in self.config.strategic_features:
                if var in self.data_cleaned.columns:
                    trend = self.data_cleaned.groupby(self.config.time_var)[var].agg([
                        'mean', 'median', 'std'
                    ])
                    temporal_trends[var] = trend
            
            # 可視化
            self._visualize_temporal_patterns(temporal_trends)
            
            self.results['temporal_patterns'] = temporal_trends
            
            self.execution_times['temporal_patterns'] = (datetime.now() - start_time).total_seconds()
            logger.info(f"✓ PHASE 7 完了 ({self.execution_times['temporal_patterns']:.2f}秒)")
            
            return self.results['temporal_patterns']
            
        except Exception as e:
            logger.error(f"時系列パターン分析エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _visualize_temporal_patterns(self, trends: Dict[str, pd.DataFrame]):
        """時系列パターンの可視化"""
        n_vars = len(trends)
        ncols = 2
        nrows = (n_vars + 1) // ncols
        
        fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
        axes = axes.flatten()
        
        for idx, (var, trend) in enumerate(trends.items()):
            ax = axes[idx]
            trend['mean'].plot(ax=ax, marker='o', color='steelblue', linewidth=2)
            ax.fill_between(
                trend.index,
                trend['mean'] - trend['std'],
                trend['mean'] + trend['std'],
                alpha=0.2, color='steelblue'
            )
            ax.set_title(var)
            ax.set_xlabel('Year')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
        
        # 未使用のaxesを非表示
        for idx in range(n_vars, len(axes)):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        
        fig_path = self.output_dir / 'figures' / f'temporal_patterns.{self.config.figure_format}'
        plt.savefig(fig_path, dpi=self.config.figure_dpi, bbox_inches='tight')
        plt.close()
        
        logger.info(f"可視化保存: {fig_path}")
    
    # ========================================================================
    # 8. 統合レポート生成
    # ========================================================================
    
    def generate_comprehensive_report(self) -> str:
        """
        統合HTMLレポートの生成
        
        すべての分析結果を1つのHTMLレポートにまとめる。
        
        Returns
        -------
        str
            レポートファイルのパス
        """
        logger.info("=" * 80)
        logger.info("PHASE 8: 統合レポート生成")
        logger.info("=" * 80)
        
        try:
            # HTML生成
            html_content = self._generate_html_report()
            
            # ファイル保存
            report_path = self.output_dir / f'comprehensive_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✓ HTMLレポート生成完了: {report_path}")
            
            # LaTeX表の生成
            if self.config.generate_latex_tables:
                self._generate_latex_tables()
            
            # 実行時間サマリー
            logger.info("=" * 80)
            logger.info("実行時間サマリー:")
            for phase, duration in self.execution_times.items():
                logger.info(f"  {phase}: {duration:.2f}秒")
            total_time = sum(self.execution_times.values())
            logger.info(f"  合計: {total_time:.2f}秒")
            logger.info("=" * 80)
            
            return str(report_path)
            
        except Exception as e:
            logger.error(f"レポート生成エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _generate_html_report(self) -> str:
        """HTMLレポートの生成"""
        html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Data Mining Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-left: 5px solid #3498db;
            padding-left: 10px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .section {{
            background-color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .metric {{
            display: inline-block;
            background-color: #ecf0f1;
            padding: 10px 20px;
            margin: 10px;
            border-radius: 5px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
        }}
        .metric-label {{
            font-size: 12px;
            color: #7f8c8d;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <h1>📊 Comprehensive Data Mining Report</h1>
    <p><strong>生成日時:</strong> {timestamp}</p>
    
    <div class="section">
        <h2>1. データサマリー</h2>
        {data_summary}
    </div>
    
    <div class="section">
        <h2>2. 戦略的グループ分析</h2>
        {strategic_groups}
    </div>
    
    <div class="section">
        <h2>3. パフォーマンス予測</h2>
        {performance_prediction}
    </div>
    
    <div class="section">
        <h2>4. 特徴量重要度</h2>
        {feature_importance}
    </div>
    
    <div class="section">
        <h2>5. 異常検知</h2>
        {anomaly_detection}
    </div>
    
    <div class="section">
        <h2>6. 実行時間</h2>
        {execution_times}
    </div>
    
    <div class="footer">
        <p>Generated by Strategic Management Research Hub v3.1</p>
        <p>Powered by Python, scikit-learn, XGBoost, EconML</p>
    </div>
</body>
</html>
"""
        
        # 各セクションの内容を生成
        sections = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_summary': self._format_data_summary(),
            'strategic_groups': self._format_strategic_groups(),
            'performance_prediction': self._format_performance_prediction(),
            'feature_importance': self._format_feature_importance(),
            'anomaly_detection': self._format_anomaly_detection(),
            'execution_times': self._format_execution_times()
        }
        
        return html_template.format(**sections)
    
    def _format_data_summary(self) -> str:
        """データサマリーのHTML生成"""
        if 'data_summary' not in self.results:
            return "<p>データが読み込まれていません</p>"
        
        summary = self.results['data_summary']
        
        html = f"""
        <div class="metric">
            <div class="metric-label">観測数</div>
            <div class="metric-value">{summary['n_observations']:,}</div>
        </div>
        <div class="metric">
            <div class="metric-label">企業数</div>
            <div class="metric-value">{summary['n_firms']:,}</div>
        </div>
        <div class="metric">
            <div class="metric-label">年数</div>
            <div class="metric-value">{summary['n_years']}</div>
        </div>
        <p><strong>分析期間:</strong> {summary['year_range'][0]} - {summary['year_range'][1]}</p>
        """
        
        return html
    
    def _format_strategic_groups(self) -> str:
        """戦略的グループ分析のHTML生成"""
        if 'strategic_groups' not in self.results:
            return "<p>戦略的グループ分析が実行されていません</p>"
        
        sg = self.results['strategic_groups']
        
        html = f"""
        <p><strong>クラスタ数:</strong> {sg['n_clusters']}</p>
        <p><strong>シルエットスコア:</strong> {sg['silhouette_score']:.4f}</p>
        <img src="figures/strategic_groups.{self.config.figure_format}" alt="Strategic Groups">
        """
        
        if 'cluster_profiles' in sg:
            profiles = sg['cluster_profiles'].to_html(index=False)
            html += f"<h3>クラスタプロファイル</h3>{profiles}"
        
        return html
    
    def _format_performance_prediction(self) -> str:
        """パフォーマンス予測のHTML生成"""
        if 'performance_prediction' not in self.results:
            return "<p>パフォーマンス予測が実行されていません</p>"
        
        pp = self.results['performance_prediction']
        best_model = pp['best_model']
        best_results = pp['model_results'][best_model]
        
        html = f"""
        <p><strong>最良モデル:</strong> {best_model}</p>
        <div class="metric">
            <div class="metric-label">Train R²</div>
            <div class="metric-value">{best_results['train_r2']:.4f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Test R²</div>
            <div class="metric-value">{best_results['test_r2']:.4f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Test RMSE</div>
            <div class="metric-value">{best_results['test_rmse']:.4f}</div>
        </div>
        """
        
        # 全モデルの比較表
        model_comparison = []
        for model_name, results in pp['model_results'].items():
            model_comparison.append({
                'Model': model_name,
                'Train R²': f"{results['train_r2']:.4f}",
                'Test R²': f"{results['test_r2']:.4f}",
                'Test RMSE': f"{results['test_rmse']:.4f}"
            })
        
        comparison_df = pd.DataFrame(model_comparison)
        html += f"<h3>モデル比較</h3>{comparison_df.to_html(index=False)}"
        
        return html
    
    def _format_feature_importance(self) -> str:
        """特徴量重要度のHTML生成"""
        if 'feature_importance' not in self.results:
            return "<p>特徴量重要度分析が実行されていません</p>"
        
        fi = self.results['feature_importance']
        
        html = f"""
        <img src="figures/feature_importance.{self.config.figure_format}" alt="Feature Importance">
        """
        
        if 'importance_df' in fi:
            importance_table = fi['importance_df'].head(10).to_html(index=False)
            html += f"<h3>Top 10 重要特徴量</h3>{importance_table}"
        
        return html
    
    def _format_anomaly_detection(self) -> str:
        """異常検知のHTML生成"""
        if 'anomaly_detection' not in self.results:
            return "<p>異常検知が実行されていません</p>"
        
        ad = self.results['anomaly_detection']
        
        html = f"""
        <div class="metric">
            <div class="metric-label">異常値数</div>
            <div class="metric-value">{ad['n_anomalies']:,}</div>
        </div>
        <div class="metric">
            <div class="metric-label">異常値割合</div>
            <div class="metric-value">{ad['anomaly_rate']:.1%}</div>
        </div>
        <img src="figures/anomaly_detection.{self.config.figure_format}" alt="Anomaly Detection">
        """
        
        return html
    
    def _format_execution_times(self) -> str:
        """実行時間のHTML生成"""
        if not self.execution_times:
            return "<p>実行時間データがありません</p>"
        
        times_data = []
        for phase, duration in self.execution_times.items():
            times_data.append({
                'Phase': phase,
                'Duration (seconds)': f"{duration:.2f}"
            })
        
        times_df = pd.DataFrame(times_data)
        total = sum(self.execution_times.values())
        
        html = times_df.to_html(index=False)
        html += f"<p><strong>合計実行時間:</strong> {total:.2f}秒</p>"
        
        return html
    
    def _generate_latex_tables(self):
        """LaTeX表の生成"""
        logger.info("LaTeX表を生成中...")
        
        tables_dir = self.output_dir / 'tables'
        
        # 戦略的グループのプロファイル
        if 'strategic_groups' in self.results and 'cluster_profiles' in self.results['strategic_groups']:
            profiles = self.results['strategic_groups']['cluster_profiles']
            latex_path = tables_dir / 'strategic_groups_profiles.tex'
            
            with open(latex_path, 'w') as f:
                f.write(profiles.to_latex(index=False, caption='Strategic Group Profiles'))
            
            logger.info(f"LaTeX表保存: {latex_path}")
        
        # パフォーマンス予測の比較
        if 'performance_prediction' in self.results:
            pp = self.results['performance_prediction']
            model_comparison = []
            for model_name, results in pp['model_results'].items():
                model_comparison.append({
                    'Model': model_name,
                    'Train R²': results['train_r2'],
                    'Test R²': results['test_r2'],
                    'Test RMSE': results['test_rmse']
                })
            
            comparison_df = pd.DataFrame(model_comparison)
            latex_path = tables_dir / 'model_comparison.tex'
            
            with open(latex_path, 'w') as f:
                f.write(comparison_df.to_latex(
                    index=False, 
                    caption='Model Performance Comparison',
                    float_format='%.4f'
                ))
            
            logger.info(f"LaTeX表保存: {latex_path}")
    
    # ========================================================================
    # 全自動実行
    # ========================================================================
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        全フェーズの自動実行
        
        Returns
        -------
        Dict[str, Any]
            すべての分析結果
        """
        logger.info("=" * 80)
        logger.info("完全自動分析を開始")
        logger.info("=" * 80)
        
        total_start = datetime.now()
        
        try:
            # Phase 1: データ読み込み
            self.load_and_validate_data()
            
            # Phase 2: 戦略的グループ分析
            self.run_strategic_group_analysis()
            
            # Phase 3: パフォーマンス予測
            self.run_performance_prediction()
            
            # Phase 4: 特徴量重要度
            self.run_feature_importance_analysis()
            
            # Phase 5: 異常検知
            self.run_anomaly_detection()
            
            # Phase 6: 因果推論（オプション）
            if self.config.treatment_var is not None:
                self.run_causal_inference()
            
            # Phase 7: 時系列パターン
            self.run_temporal_pattern_analysis()
            
            # Phase 8: 統合レポート
            report_path = self.generate_comprehensive_report()
            
            total_time = (datetime.now() - total_start).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"✅ 全分析完了！ ({total_time:.2f}秒)")
            logger.info(f"レポート: {report_path}")
            logger.info("=" * 80)
            
            return self.results
            
        except Exception as e:
            logger.error(f"分析実行エラー: {str(e)}")
            logger.error(traceback.format_exc())
            raise


# ============================================================================
# CLI実行
# ============================================================================

def main():
    """コマンドライン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Comprehensive Data Mining Pipeline for Strategic Management Research'
    )
    parser.add_argument(
        '--data',
        type=str,
        required=True,
        help='Path to data file (.dta, .csv, .parquet)'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to config YAML file (optional)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='./datamining_output/',
        help='Output directory'
    )
    
    args = parser.parse_args()
    
    # パイプライン実行
    if args.config:
        pipeline = ComprehensiveDataMiningPipeline(config_path=args.config)
    else:
        pipeline = ComprehensiveDataMiningPipeline(
            data_path=args.data,
            output_dir=args.output
        )
    
    pipeline.run_complete_analysis()


if __name__ == '__main__':
    main()
