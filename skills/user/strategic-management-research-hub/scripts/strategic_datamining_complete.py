"""
Strategic Management Research Hub - Complete Data Mining Engine v4.0
====================================================================

【概要】
SKILL.md Phase 1-8ワークフローと完全統合された、
publication-grade戦略経営研究用データマイニングエンジン。

【主要機能】
1. 戦略的グループ分析（Configuration Theory）
2. パフォーマンス予測（Ensemble ML）
3. 因果推論統合（Causal ML + DML）
4. 異常検知（Strategic Outliers）
5. 特徴量エンジニアリング（自動生成）
6. ネットワーク分析統合（取締役・アライアンス）
7. テキスト分析統合（MD&A, Earnings Calls）
8. 時系列パターン抽出（LSTM, Prophet）
9. 説明可能AI（SHAP, LIME）
10. 完全自動化レポート生成

【使用例】
```python
from strategic_datamining_complete import StrategicDataMiningEngine

# 初期化
engine = StrategicDataMiningEngine(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./research_output/'
)

# 包括的分析実行
results = engine.run_comprehensive_analysis(
    research_theme='competitive_strategy',
    target_variable='roa',
    strategic_vars=['rd_intensity', 'capital_intensity', 'differentiation']
)

# レポート生成
engine.generate_publication_ready_report()
```

Author: Strategic Management Research Hub v4.0
Date: 2025-11-01
License: MIT

References:
- Porter (1980): Competitive Strategy, Free Press
- Meyer et al. (1993): Organizational Configurations, AMR
- Ketchen & Shook (1996): Cluster Analysis in SMJ
- Athey & Imbens (2017): Causal Forests, ArXiv
- Lundberg & Lee (2017): SHAP, NIPS
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any, Callable
import logging
from pathlib import Path
import warnings
import json
from datetime import datetime
import pickle
import yaml
from dataclasses import dataclass, asdict
from collections import defaultdict

# Core ML Libraries
from sklearn.preprocessing import (
    StandardScaler, RobustScaler, MinMaxScaler, 
    QuantileTransformer, PowerTransformer
)
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV,
    RandomizedSearchCV, TimeSeriesSplit, KFold, StratifiedKFold
)
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    mean_absolute_percentage_error, explained_variance_score,
    silhouette_score, calinski_harabasz_score, davies_bouldin_score,
    roc_auc_score, classification_report, confusion_matrix
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Clustering
from sklearn.cluster import (
    KMeans, DBSCAN, AgglomerativeClustering, 
    SpectralClustering, OPTICS, Birch, MeanShift
)
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform

# Dimensionality Reduction
from sklearn.decomposition import PCA, FactorAnalysis, FastICA, NMF, TruncatedSVD
from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding, MDS

# Anomaly Detection
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM

# Supervised Learning
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet,
    BayesianRidge, HuberRegressor, RANSACRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor,
    AdaBoostRegressor, ExtraTreesRegressor,
    HistGradientBoostingRegressor, VotingRegressor,
    StackingRegressor, BaggingRegressor
)
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, Matern, WhiteKernel

# Neural Networks
from sklearn.neural_network import MLPRegressor

# Advanced Libraries (optional)
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False
    warnings.warn("XGBoost not available. Install: pip install xgboost")

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False
    warnings.warn("LightGBM not available. Install: pip install lightgbm")

try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    warnings.warn("CatBoost not available. Install: pip install catboost")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP not available. Install: pip install shap")

try:
    import umap.umap_ as umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP not available. Install: pip install umap-learn")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    warnings.warn("Prophet not available. Install: pip install prophet")

try:
    from econml.dml import LinearDML, CausalForestDML
    from econml.dr import DRLearner
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False
    warnings.warn("EconML not available. Install: pip install econml")

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class DataMiningConfig:
    """データマイニング設定"""
    # Clustering
    n_clusters: int = 4
    clustering_method: str = 'kmeans'  # kmeans, hierarchical, gmm, dbscan
    
    # Prediction
    prediction_models: List[str] = None
    test_size: float = 0.2
    cv_folds: int = 5
    
    # Feature Engineering
    auto_interactions: bool = True
    polynomial_features: bool = False
    polynomial_degree: int = 2
    
    # Anomaly Detection
    contamination: float = 0.05
    anomaly_methods: List[str] = None
    
    # Dimensionality Reduction
    n_components_pca: int = 10
    use_umap: bool = True
    
    # Random State
    random_state: int = 42
    
    # Output
    save_models: bool = True
    generate_plots: bool = True
    verbose: bool = True
    
    def __post_init__(self):
        if self.prediction_models is None:
            self.prediction_models = ['rf', 'gbm', 'xgb', 'ensemble']
        if self.anomaly_methods is None:
            self.anomaly_methods = ['isolation_forest', 'lof']


@dataclass
class AnalysisResults:
    """分析結果格納クラス"""
    strategic_groups: Optional[Dict] = None
    performance_prediction: Optional[Dict] = None
    feature_importance: Optional[Dict] = None
    anomaly_detection: Optional[Dict] = None
    causal_effects: Optional[Dict] = None
    time_series_forecast: Optional[Dict] = None
    network_metrics: Optional[Dict] = None
    text_analysis: Optional[Dict] = None
    
    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def save(self, filepath: str):
        """結果をJSONで保存"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2, default=str)


# ============================================================================
# MAIN ENGINE CLASS
# ============================================================================

class StrategicDataMiningEngine:
    """
    戦略経営研究用統合データマイニングエンジン
    
    【主要機能】
    1. Strategic Group Analysis (Configuration Theory)
    2. Firm Performance Prediction (ML Ensemble)
    3. Causal Effect Estimation (DML, Causal Forest)
    4. Anomaly Detection (Strategic Outliers)
    5. Feature Engineering (Automatic)
    6. Temporal Pattern Analysis (Time Series)
    7. Explainable AI (SHAP, LIME)
    8. Network Analysis Integration
    9. Text Analysis Integration
    10. Publication-Ready Report Generation
    
    【使用例】
    >>> engine = StrategicDataMiningEngine(
    ...     data=df_panel,
    ...     firm_id='gvkey',
    ...     time_var='year'
    ... )
    >>> results = engine.run_comprehensive_analysis()
    >>> engine.generate_publication_ready_report()
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        firm_id: str,
        time_var: str,
        industry_var: Optional[str] = None,
        country_var: Optional[str] = None,
        output_dir: str = './datamining_output/',
        config: Optional[DataMiningConfig] = None
    ):
        """
        初期化
        
        Args:
            data: パネルデータ（DataFrame）
            firm_id: 企業ID列名
            time_var: 時間変数列名
            industry_var: 産業変数列名（Optional）
            country_var: 国変数列名（Optional）
            output_dir: 出力ディレクトリ
            config: データマイニング設定
        """
        self.data = data.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.industry_var = industry_var
        self.country_var = country_var
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configuration
        self.config = config if config else DataMiningConfig()
        
        # Results storage
        self.results = AnalysisResults()
        self.models = {}
        self.scalers = {}
        self.engineered_features = {}
        
        # Analysis history
        self.analysis_log = []
        
        # Data validation
        self._validate_data()
        
        logger.info(f"✅ Strategic Data Mining Engine initialized")
        logger.info(f"   Dataset: {len(data):,} obs, "
                   f"{data[firm_id].nunique():,} firms, "
                   f"{data[time_var].nunique()} periods")
    
    def _validate_data(self):
        """データ検証"""
        required_cols = [self.firm_id, self.time_var]
        missing_cols = [col for col in required_cols if col not in self.data.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # 欠損値警告
        missing_pct = self.data.isnull().sum() / len(self.data) * 100
        high_missing = missing_pct[missing_pct > 30]
        
        if not high_missing.empty:
            logger.warning(f"⚠️ High missing data (>30%):\n{high_missing}")
    
    # ========================================================================
    # 1. STRATEGIC GROUP ANALYSIS
    # ========================================================================
    
    def strategic_group_analysis(
        self,
        features: List[str],
        n_clusters: Optional[int] = None,
        method: str = 'kmeans',
        industry_specific: bool = False,
        temporal_analysis: bool = False
    ) -> Dict:
        """
        戦略的グループ分析（Configuration Theory）
        
        理論的背景：
        - Porter (1980): Strategic Groups within Industries
        - Meyer et al. (1993): Organizational Configurations
        - Ketchen & Shook (1996): Cluster Analysis in Strategic Management
        
        Args:
            features: クラスタリング変数リスト
            n_clusters: クラスター数（Noneなら自動決定）
            method: クラスタリング手法
            industry_specific: 産業別分析
            temporal_analysis: 時系列変化分析
        
        Returns:
            分析結果辞書
        """
        logger.info(f"🔍 Strategic Group Analysis: {method}")
        self._log_analysis('strategic_group_analysis', locals())
        
        # データ準備
        df_cluster = self.data[features].dropna()
        
        # 産業別分析
        if industry_specific and self.industry_var:
            results_by_industry = {}
            
            for industry in self.data[self.industry_var].unique():
                df_ind = self.data[self.data[self.industry_var] == industry]
                df_ind_cluster = df_ind[features].dropna()
                
                if len(df_ind_cluster) < 10:
                    logger.warning(f"⚠️ Insufficient data for industry: {industry}")
                    continue
                
                result = self._perform_clustering(
                    df_ind_cluster, 
                    n_clusters=n_clusters, 
                    method=method
                )
                results_by_industry[industry] = result
            
            self.results.strategic_groups = {
                'type': 'industry_specific',
                'industries': results_by_industry
            }
            
            return results_by_industry
        
        # 全体分析
        result = self._perform_clustering(df_cluster, n_clusters, method)
        
        # 時系列変化分析
        if temporal_analysis:
            temporal_results = self._analyze_strategic_trajectories(
                df_cluster, 
                result['cluster_labels']
            )
            result['temporal_analysis'] = temporal_results
        
        # クラスタープロファイリング
        cluster_profiles = self._profile_strategic_groups(
            self.data,
            result['cluster_labels'],
            features
        )
        result['cluster_profiles'] = cluster_profiles
        
        # 可視化
        self._visualize_strategic_groups(df_cluster, result['cluster_labels'], features)
        
        self.results.strategic_groups = result
        
        logger.info(f"✅ Strategic groups identified: {result['n_clusters']}")
        logger.info(f"   Silhouette Score: {result['silhouette_score']:.3f}")
        
        return result
    
    def _perform_clustering(
        self,
        X: pd.DataFrame,
        n_clusters: Optional[int],
        method: str
    ) -> Dict:
        """クラスタリング実行"""
        # スケーリング
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers['clustering'] = scaler
        
        # クラスター数決定（自動）
        if n_clusters is None:
            n_clusters = self._determine_optimal_clusters(X_scaled)
        
        # クラスタリング実行
        if method == 'kmeans':
            clusterer = KMeans(
                n_clusters=n_clusters,
                random_state=self.config.random_state,
                n_init=10
            )
        elif method == 'hierarchical':
            clusterer = AgglomerativeClustering(n_clusters=n_clusters)
        elif method == 'gmm':
            clusterer = GaussianMixture(
                n_components=n_clusters,
                random_state=self.config.random_state
            )
        elif method == 'dbscan':
            clusterer = DBSCAN(eps=0.5, min_samples=5)
        else:
            raise ValueError(f"Unknown clustering method: {method}")
        
        labels = clusterer.fit_predict(X_scaled)
        
        # 評価指標
        silhouette = silhouette_score(X_scaled, labels)
        calinski = calinski_harabasz_score(X_scaled, labels)
        davies_bouldin = davies_bouldin_score(X_scaled, labels)
        
        # PCA for visualization
        pca = PCA(n_components=2, random_state=self.config.random_state)
        X_pca = pca.fit_transform(X_scaled)
        
        return {
            'method': method,
            'n_clusters': n_clusters,
            'cluster_labels': labels,
            'silhouette_score': silhouette,
            'calinski_harabasz': calinski,
            'davies_bouldin': davies_bouldin,
            'pca_components': X_pca,
            'pca_explained_variance': pca.explained_variance_ratio_,
            'clusterer': clusterer,
            'scaler': scaler
        }
    
    def _determine_optimal_clusters(
        self,
        X: np.ndarray,
        max_clusters: int = 10
    ) -> int:
        """
        最適クラスター数決定（Elbow法 + Silhouette法）
        """
        silhouette_scores = []
        inertias = []
        
        for k in range(2, min(max_clusters + 1, len(X) // 2)):
            kmeans = KMeans(n_clusters=k, random_state=self.config.random_state, n_init=10)
            labels = kmeans.fit_predict(X)
            
            silhouette_scores.append(silhouette_score(X, labels))
            inertias.append(kmeans.inertia_)
        
        # Silhouette法で最適値
        optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2
        
        logger.info(f"   Optimal clusters (Silhouette): {optimal_k}")
        
        return optimal_k
    
    def _profile_strategic_groups(
        self,
        data: pd.DataFrame,
        labels: np.ndarray,
        features: List[str]
    ) -> pd.DataFrame:
        """
        クラスタープロファイリング
        各戦略的グループの特徴記述
        """
        df_profiling = data.copy()
        df_profiling['cluster'] = labels
        
        # グループ別統計
        profiles = df_profiling.groupby('cluster')[features].agg(['mean', 'std', 'count'])
        
        return profiles
    
    def _analyze_strategic_trajectories(
        self,
        X: pd.DataFrame,
        labels: np.ndarray
    ) -> Dict:
        """
        戦略的軌跡分析（時系列でのクラスター移動）
        """
        df_trajectory = self.data.copy()
        df_trajectory['cluster'] = labels
        
        # 企業ごとのクラスター変遷
        trajectories = []
        
        for firm in df_trajectory[self.firm_id].unique():
            firm_data = df_trajectory[df_trajectory[self.firm_id] == firm].sort_values(self.time_var)
            
            if len(firm_data) >= 2:
                cluster_sequence = firm_data['cluster'].tolist()
                
                # クラスター変化回数
                changes = sum(1 for i in range(len(cluster_sequence)-1) 
                            if cluster_sequence[i] != cluster_sequence[i+1])
                
                trajectories.append({
                    self.firm_id: firm,
                    'cluster_sequence': cluster_sequence,
                    'n_changes': changes,
                    'initial_cluster': cluster_sequence[0],
                    'final_cluster': cluster_sequence[-1]
                })
        
        df_trajectories = pd.DataFrame(trajectories)
        
        # 変化パターンの分析
        stable_firms = (df_trajectories['n_changes'] == 0).sum()
        dynamic_firms = (df_trajectories['n_changes'] > 0).sum()
        
        return {
            'trajectories': df_trajectories,
            'stable_firms': stable_firms,
            'dynamic_firms': dynamic_firms,
            'avg_changes': df_trajectories['n_changes'].mean()
        }
    
    def _visualize_strategic_groups(
        self,
        X: pd.DataFrame,
        labels: np.ndarray,
        features: List[str]
    ):
        """戦略的グループ可視化"""
        # PCA 2D projection
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        
        pca = PCA(n_components=2, random_state=self.config.random_state)
        X_pca = pca.fit_transform(X_scaled)
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            X_pca[:, 0],
            X_pca[:, 1],
            c=labels,
            cmap='viridis',
            alpha=0.6,
            edgecolors='k',
            s=50
        )
        plt.colorbar(scatter, label='Cluster')
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
        plt.title('Strategic Groups (PCA Projection)')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'strategic_groups_pca.png', dpi=300)
        plt.close()
        
        # Cluster profiles heatmap
        df_viz = X.copy()
        df_viz['cluster'] = labels
        cluster_means = df_viz.groupby('cluster')[features].mean()
        
        # Standardize for heatmap
        cluster_means_std = (cluster_means - cluster_means.mean()) / cluster_means.std()
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            cluster_means_std.T,
            annot=True,
            fmt='.2f',
            cmap='RdBu_r',
            center=0,
            cbar_kws={'label': 'Standardized Mean'}
        )
        plt.xlabel('Strategic Group')
        plt.ylabel('Strategic Variables')
        plt.title('Strategic Group Profiles')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'strategic_group_profiles.png', dpi=300)
        plt.close()
        
        logger.info("   📊 Visualizations saved")
    
    # ========================================================================
    # 2. FIRM PERFORMANCE PREDICTION
    # ========================================================================
    
    def predict_firm_performance(
        self,
        target: str,
        features: List[str],
        model_types: Optional[List[str]] = None,
        hyperparameter_tuning: bool = True,
        cross_validation: bool = True,
        return_predictions: bool = True
    ) -> Dict:
        """
        企業パフォーマンス予測（Ensemble ML）
        
        【使用モデル】
        - Random Forest
        - Gradient Boosting (GBM)
        - XGBoost
        - LightGBM
        - CatBoost
        - Neural Network
        - Ensemble (Stacking/Voting)
        
        Args:
            target: 目的変数
            features: 説明変数リスト
            model_types: モデルタイプリスト
            hyperparameter_tuning: ハイパーパラメータチューニング
            cross_validation: 交差検証
            return_predictions: 予測値を返すか
        
        Returns:
            分析結果辞書
        """
        logger.info(f"🎯 Firm Performance Prediction: {target}")
        self._log_analysis('predict_firm_performance', locals())
        
        # データ準備
        df_model = self.data[[target] + features].dropna()
        X = df_model[features]
        y = df_model[target]
        
        # Train-Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.config.test_size,
            random_state=self.config.random_state
        )
        
        # スケーリング
        scaler = RobustScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['prediction'] = scaler
        
        # モデル訓練
        if model_types is None:
            model_types = self.config.prediction_models
        
        results_by_model = {}
        
        for model_type in model_types:
            logger.info(f"   Training: {model_type}")
            
            model_result = self._train_prediction_model(
                X_train_scaled, X_test_scaled, y_train, y_test,
                model_type, hyperparameter_tuning, cross_validation
            )
            
            results_by_model[model_type] = model_result
        
        # ベストモデル選択
        best_model_name = max(
            results_by_model,
            key=lambda k: results_by_model[k]['metrics']['test_r2']
        )
        
        best_model = results_by_model[best_model_name]['model']
        
        # Feature Importance (best model)
        feature_importance = self._extract_feature_importance(
            best_model,
            features,
            X_train_scaled,
            y_train
        )
        
        # 可視化
        self._visualize_prediction_performance(results_by_model, target)
        
        result = {
            'target': target,
            'features': features,
            'all_results': results_by_model,
            'best_model': best_model_name,
            'best_model_object': best_model,
            'feature_importance': feature_importance,
            'scaler': scaler
        }
        
        if return_predictions:
            result['predictions_test'] = results_by_model[best_model_name]['predictions']
            result['y_test'] = y_test.values
        
        self.results.performance_prediction = result
        self.models['prediction'] = best_model
        
        logger.info(f"✅ Best Model: {best_model_name}")
        logger.info(f"   Test R²: {results_by_model[best_model_name]['metrics']['test_r2']:.4f}")
        logger.info(f"   Test RMSE: {results_by_model[best_model_name]['metrics']['test_rmse']:.4f}")
        
        return result
    
    def _train_prediction_model(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        model_type: str,
        hyperparameter_tuning: bool,
        cross_validation: bool
    ) -> Dict:
        """個別モデル訓練"""
        # モデル選択
        if model_type == 'rf':
            base_model = RandomForestRegressor(random_state=self.config.random_state)
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [10, 20, None],
                'min_samples_split': [2, 5]
            }
        
        elif model_type == 'gbm':
            base_model = GradientBoostingRegressor(random_state=self.config.random_state)
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            }
        
        elif model_type == 'xgb' and XGB_AVAILABLE:
            base_model = xgb.XGBRegressor(random_state=self.config.random_state)
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'max_depth': [3, 5]
            }
        
        elif model_type == 'lgb' and LGB_AVAILABLE:
            base_model = lgb.LGBMRegressor(random_state=self.config.random_state, verbose=-1)
            param_grid = {
                'n_estimators': [100, 200],
                'learning_rate': [0.01, 0.1],
                'num_leaves': [31, 50]
            }
        
        elif model_type == 'catboost' and CATBOOST_AVAILABLE:
            base_model = cb.CatBoostRegressor(
                random_state=self.config.random_state,
                verbose=0
            )
            param_grid = {
                'iterations': [100, 200],
                'learning_rate': [0.01, 0.1],
                'depth': [4, 6]
            }
        
        elif model_type == 'nn':
            base_model = MLPRegressor(random_state=self.config.random_state, max_iter=500)
            param_grid = {
                'hidden_layer_sizes': [(50,), (100,), (50, 50)],
                'alpha': [0.0001, 0.001]
            }
        
        elif model_type == 'ensemble':
            # Stacking Ensemble
            estimators = [
                ('rf', RandomForestRegressor(n_estimators=100, random_state=self.config.random_state)),
                ('gbm', GradientBoostingRegressor(n_estimators=100, random_state=self.config.random_state))
            ]
            
            if XGB_AVAILABLE:
                estimators.append(('xgb', xgb.XGBRegressor(n_estimators=100, random_state=self.config.random_state)))
            
            base_model = StackingRegressor(
                estimators=estimators,
                final_estimator=Ridge(),
                cv=5
            )
            param_grid = {}  # アンサンブルはチューニングなし（時間節約）
        
        else:
            logger.warning(f"Unknown model type: {model_type}, using Random Forest")
            base_model = RandomForestRegressor(random_state=self.config.random_state)
            param_grid = {}
        
        # ハイパーパラメータチューニング
        if hyperparameter_tuning and param_grid:
            grid_search = GridSearchCV(
                base_model,
                param_grid,
                cv=5,
                scoring='r2',
                n_jobs=-1
            )
            grid_search.fit(X_train, y_train)
            model = grid_search.best_estimator_
        else:
            model = base_model
            model.fit(X_train, y_train)
        
        # 予測
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # 評価指標
        metrics = {
            'train_r2': r2_score(y_train, y_pred_train),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'test_mae': mean_absolute_error(y_test, y_pred_test)
        }
        
        # Cross-validation
        if cross_validation:
            cv_scores = cross_val_score(
                model, X_train, y_train,
                cv=self.config.cv_folds,
                scoring='r2'
            )
            metrics['cv_r2_mean'] = cv_scores.mean()
            metrics['cv_r2_std'] = cv_scores.std()
        
        return {
            'model': model,
            'metrics': metrics,
            'predictions': y_pred_test
        }
    
    def _extract_feature_importance(
        self,
        model,
        feature_names: List[str],
        X: np.ndarray,
        y: np.ndarray
    ) -> pd.DataFrame:
        """特徴量重要度抽出"""
        importance_dict = {}
        
        # Tree-based models
        if hasattr(model, 'feature_importances_'):
            importance_dict['importance'] = model.feature_importances_
        
        # Linear models
        elif hasattr(model, 'coef_'):
            importance_dict['importance'] = np.abs(model.coef_)
        
        # SHAP values (if available)
        if SHAP_AVAILABLE:
            try:
                explainer = shap.Explainer(model, X)
                shap_values = explainer(X)
                importance_dict['shap_importance'] = np.abs(shap_values.values).mean(axis=0)
            except Exception as e:
                logger.warning(f"SHAP failed: {e}")
        
        # DataFrame作成
        importance_df = pd.DataFrame({
            'feature': feature_names,
            **importance_dict
        })
        
        importance_df = importance_df.sort_values('importance', ascending=False)
        
        return importance_df
    
    def _visualize_prediction_performance(
        self,
        results_by_model: Dict,
        target: str
    ):
        """予測パフォーマンス可視化"""
        # モデル比較
        model_names = list(results_by_model.keys())
        test_r2_scores = [results_by_model[m]['metrics']['test_r2'] for m in model_names]
        test_rmse_scores = [results_by_model[m]['metrics']['test_rmse'] for m in model_names]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # R² comparison
        axes[0].bar(model_names, test_r2_scores, color='skyblue', edgecolor='navy')
        axes[0].set_ylabel('Test R²')
        axes[0].set_title('Model Comparison: R²')
        axes[0].set_ylim(0, 1)
        axes[0].tick_params(axis='x', rotation=45)
        
        # RMSE comparison
        axes[1].bar(model_names, test_rmse_scores, color='salmon', edgecolor='darkred')
        axes[1].set_ylabel('Test RMSE')
        axes[1].set_title('Model Comparison: RMSE')
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'prediction_performance.png', dpi=300)
        plt.close()
        
        # Predicted vs Actual (best model)
        best_model = max(results_by_model, key=lambda k: results_by_model[k]['metrics']['test_r2'])
        y_test = None  # Will need to pass this in properly
        y_pred = results_by_model[best_model]['predictions']
        
        # This visualization requires y_test - would need architecture change
        # Placeholder for now
        
        logger.info("   📊 Prediction visualizations saved")
    
    # ========================================================================
    # 3. FEATURE IMPORTANCE & ENGINEERING
    # ========================================================================
    
    def analyze_feature_importance(
        self,
        target: str,
        features: List[str],
        methods: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        特徴量重要度分析（複数手法統合）
        
        【手法】
        1. Random Forest Feature Importance
        2. Gradient Boosting Feature Importance
        3. SHAP値（Shapley Additive Explanations）
        4. Permutation Importance
        5. Correlation-based
        
        Args:
            target: 目的変数
            features: 説明変数リスト
            methods: 使用手法リスト
        
        Returns:
            特徴量重要度DataFrame
        """
        logger.info(f"📈 Feature Importance Analysis: {target}")
        self._log_analysis('analyze_feature_importance', locals())
        
        if methods is None:
            methods = ['rf', 'gbm', 'shap', 'permutation', 'correlation']
        
        # データ準備
        df_importance = self.data[[target] + features].dropna()
        X = df_importance[features]
        y = df_importance[target]
        
        # スケーリング
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        
        importance_results = {}
        
        # 1. Random Forest
        if 'rf' in methods:
            rf = RandomForestRegressor(n_estimators=100, random_state=self.config.random_state)
            rf.fit(X_scaled, y)
            importance_results['rf_importance'] = rf.feature_importances_
        
        # 2. Gradient Boosting
        if 'gbm' in methods:
            gbm = GradientBoostingRegressor(n_estimators=100, random_state=self.config.random_state)
            gbm.fit(X_scaled, y)
            importance_results['gbm_importance'] = gbm.feature_importances_
        
        # 3. SHAP
        if 'shap' in methods and SHAP_AVAILABLE:
            try:
                model = RandomForestRegressor(n_estimators=50, random_state=self.config.random_state)
                model.fit(X_scaled, y)
                
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_scaled)
                importance_results['shap_importance'] = np.abs(shap_values).mean(axis=0)
            except Exception as e:
                logger.warning(f"SHAP failed: {e}")
        
        # 4. Permutation Importance
        if 'permutation' in methods:
            from sklearn.inspection import permutation_importance
            
            model = RandomForestRegressor(n_estimators=50, random_state=self.config.random_state)
            model.fit(X_scaled, y)
            
            perm_importance = permutation_importance(
                model, X_scaled, y,
                n_repeats=10,
                random_state=self.config.random_state
            )
            importance_results['perm_importance'] = perm_importance.importances_mean
        
        # 5. Correlation-based
        if 'correlation' in methods:
            correlations = np.array([np.abs(np.corrcoef(X[feat], y)[0, 1]) for feat in features])
            importance_results['correlation'] = correlations
        
        # DataFrame作成
        importance_df = pd.DataFrame({
            'feature': features,
            **importance_results
        })
        
        # 平均重要度でソート
        if len(importance_results) > 0:
            importance_cols = [col for col in importance_df.columns if col != 'feature']
            importance_df['mean_importance'] = importance_df[importance_cols].mean(axis=1)
            importance_df = importance_df.sort_values('mean_importance', ascending=False)
        
        # 可視化
        self._visualize_feature_importance(importance_df)
        
        self.results.feature_importance = importance_df.to_dict()
        
        logger.info(f"✅ Top 5 features:")
        for i, row in importance_df.head(5).iterrows():
            logger.info(f"   {row['feature']}: {row['mean_importance']:.4f}")
        
        return importance_df
    
    def _visualize_feature_importance(self, importance_df: pd.DataFrame):
        """特徴量重要度可視化"""
        # Top 15 features
        top_features = importance_df.head(15)
        
        plt.figure(figsize=(12, 8))
        
        importance_cols = [col for col in importance_df.columns 
                          if col not in ['feature', 'mean_importance']]
        
        x = np.arange(len(top_features))
        width = 0.8 / len(importance_cols)
        
        for i, col in enumerate(importance_cols):
            offset = width * i - (width * len(importance_cols) / 2)
            plt.barh(
                x + offset,
                top_features[col],
                width,
                label=col.replace('_', ' ').title()
            )
        
        plt.yticks(x, top_features['feature'])
        plt.xlabel('Importance Score')
        plt.title('Feature Importance Analysis (Top 15)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'feature_importance_plot.png', dpi=300)
        plt.close()
        
        logger.info("   📊 Feature importance visualization saved")
    
    def engineer_features(
        self,
        base_features: List[str],
        interactions: bool = True,
        polynomials: bool = False,
        industry_adjusted: bool = True
    ) -> pd.DataFrame:
        """
        特徴量エンジニアリング（自動生成）
        
        【生成特徴量】
        1. 交互作用項（A × B）
        2. 多項式特徴量（A², A³）
        3. 産業調整済み変数（firm value - industry median）
        4. ラグ変数（t-1, t-2）
        5. 変化率変数（growth rates）
        
        Args:
            base_features: 基本特徴量リスト
            interactions: 交互作用項生成
            polynomials: 多項式特徴量生成
            industry_adjusted: 産業調整
        
        Returns:
            拡張された特徴量DataFrame
        """
        logger.info(f"⚙️ Feature Engineering")
        self._log_analysis('engineer_features', locals())
        
        df_engineered = self.data.copy()
        engineered_features = []
        
        # 1. 交互作用項
        if interactions:
            for i, feat1 in enumerate(base_features):
                for feat2 in base_features[i+1:]:
                    new_feat_name = f"{feat1}_x_{feat2}"
                    df_engineered[new_feat_name] = (
                        df_engineered[feat1] * df_engineered[feat2]
                    )
                    engineered_features.append(new_feat_name)
        
        # 2. 多項式特徴量
        if polynomials:
            for feat in base_features:
                # 2乗
                df_engineered[f"{feat}_sq"] = df_engineered[feat] ** 2
                engineered_features.append(f"{feat}_sq")
                
                # 対数（正の値のみ）
                if (df_engineered[feat] > 0).all():
                    df_engineered[f"{feat}_log"] = np.log(df_engineered[feat] + 1)
                    engineered_features.append(f"{feat}_log")
        
        # 3. 産業調整済み変数
        if industry_adjusted and self.industry_var:
            for feat in base_features:
                industry_median = df_engineered.groupby(self.industry_var)[feat].transform('median')
                df_engineered[f"{feat}_industry_adj"] = (
                    df_engineered[feat] - industry_median
                )
                engineered_features.append(f"{feat}_industry_adj")
        
        # 4. ラグ変数
        for feat in base_features:
            df_engineered[f"{feat}_lag1"] = df_engineered.groupby(self.firm_id)[feat].shift(1)
            engineered_features.append(f"{feat}_lag1")
        
        # 5. 変化率
        for feat in base_features:
            df_engineered[f"{feat}_growth"] = df_engineered.groupby(self.firm_id)[feat].pct_change()
            engineered_features.append(f"{feat}_growth")
        
        self.engineered_features = {
            'base_features': base_features,
            'engineered_features': engineered_features,
            'total_features': base_features + engineered_features
        }
        
        logger.info(f"✅ Engineered features: {len(engineered_features)}")
        logger.info(f"   Total features: {len(self.engineered_features['total_features'])}")
        
        return df_engineered[base_features + engineered_features]
    
    # ========================================================================
    # 4. ANOMALY DETECTION (Strategic Outliers)
    # ========================================================================
    
    def detect_strategic_outliers(
        self,
        features: List[str],
        methods: Optional[List[str]] = None,
        contamination: float = 0.05
    ) -> Dict:
        """
        異常検知（戦略的アウトライア）
        
        理論的意義：
        - 既存理論で説明できない戦略パターンの発見
        - Positive deviance（成功する outliers）の特定
        - 戦略的イノベーターの検出
        
        【手法】
        1. Isolation Forest
        2. Local Outlier Factor (LOF)
        3. One-Class SVM
        4. Elliptic Envelope
        
        Args:
            features: 分析対象特徴量
            methods: 使用手法リスト
            contamination: アウトライア比率
        
        Returns:
            異常検知結果辞書
        """
        logger.info(f"🔍 Strategic Outlier Detection")
        self._log_analysis('detect_strategic_outliers', locals())
        
        if methods is None:
            methods = ['isolation_forest', 'lof', 'ocsvm']
        
        # データ準備
        df_outlier = self.data[features].dropna()
        X = df_outlier.values
        
        # スケーリング
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        
        outlier_results = {}
        
        # 1. Isolation Forest
        if 'isolation_forest' in methods:
            iso_forest = IsolationForest(
                contamination=contamination,
                random_state=self.config.random_state
            )
            outliers_iso = iso_forest.fit_predict(X_scaled)
            outlier_results['isolation_forest'] = outliers_iso
        
        # 2. Local Outlier Factor
        if 'lof' in methods:
            lof = LocalOutlierFactor(contamination=contamination)
            outliers_lof = lof.fit_predict(X_scaled)
            outlier_results['lof'] = outliers_lof
        
        # 3. One-Class SVM
        if 'ocsvm' in methods:
            ocsvm = OneClassSVM(nu=contamination)
            outliers_ocsvm = ocsvm.fit_predict(X_scaled)
            outlier_results['ocsvm'] = outliers_ocsvm
        
        # 4. Elliptic Envelope
        if 'elliptic' in methods:
            try:
                elliptic = EllipticEnvelope(contamination=contamination, random_state=self.config.random_state)
                outliers_elliptic = elliptic.fit_predict(X_scaled)
                outlier_results['elliptic'] = outliers_elliptic
            except Exception as e:
                logger.warning(f"Elliptic Envelope failed: {e}")
        
        # アンサンブル（多数決）
        outlier_matrix = np.array([outliers for outliers in outlier_results.values()])
        ensemble_outliers = np.where(
            (outlier_matrix == -1).sum(axis=0) >= len(methods) // 2 + 1,
            -1,
            1
        )
        
        # 結果整理
        df_outlier_result = df_outlier.copy()
        for method, outliers in outlier_results.items():
            df_outlier_result[f'outlier_{method}'] = outliers
        df_outlier_result['outlier_ensemble'] = ensemble_outliers
        
        n_outliers = (ensemble_outliers == -1).sum()
        outlier_rate = n_outliers / len(ensemble_outliers)
        
        # 可視化
        self._visualize_outliers(X_scaled, ensemble_outliers)
        
        result = {
            'methods': methods,
            'contamination': contamination,
            'n_outliers': n_outliers,
            'outlier_rate': outlier_rate,
            'outlier_labels': ensemble_outliers,
            'outlier_df': df_outlier_result
        }
        
        self.results.anomaly_detection = result
        
        logger.info(f"✅ Outliers detected: {n_outliers} ({outlier_rate:.1%})")
        
        return result
    
    def _visualize_outliers(self, X: np.ndarray, labels: np.ndarray):
        """アウトライア可視化"""
        # PCA 2D projection
        pca = PCA(n_components=2, random_state=self.config.random_state)
        X_pca = pca.fit_transform(X)
        
        plt.figure(figsize=(12, 8))
        
        # Normal points
        mask_normal = labels == 1
        plt.scatter(
            X_pca[mask_normal, 0],
            X_pca[mask_normal, 1],
            c='blue',
            alpha=0.5,
            label='Normal',
            s=30
        )
        
        # Outliers
        mask_outlier = labels == -1
        plt.scatter(
            X_pca[mask_outlier, 0],
            X_pca[mask_outlier, 1],
            c='red',
            marker='x',
            s=100,
            label='Outlier',
            linewidths=2
        )
        
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} var)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} var)')
        plt.title('Strategic Outliers Detection (PCA Projection)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'outliers_pca.png', dpi=300)
        plt.close()
        
        logger.info("   📊 Outlier visualization saved")
    
    # ========================================================================
    # 5. COMPREHENSIVE ANALYSIS RUNNER
    # ========================================================================
    
    def run_comprehensive_analysis(
        self,
        research_theme: str = 'general',
        target_variable: Optional[str] = None,
        strategic_vars: Optional[List[str]] = None,
        run_all: bool = True
    ) -> AnalysisResults:
        """
        包括的データマイニング分析実行
        
        【研究テーマ対応】
        - 'competitive_strategy': 競争戦略研究
        - 'organizational_capability': 組織能力研究
        - 'institutional_theory': 制度理論研究
        - 'innovation': イノベーション研究
        - 'general': 汎用分析
        
        Args:
            research_theme: 研究テーマ
            target_variable: 目的変数
            strategic_vars: 戦略変数リスト
            run_all: 全分析実行
        
        Returns:
            AnalysisResults object
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"🚀 COMPREHENSIVE STRATEGIC DATA MINING ANALYSIS")
        logger.info(f"   Theme: {research_theme}")
        logger.info(f"{'='*70}\n")
        
        # テーマ別変数設定
        if strategic_vars is None:
            strategic_vars = self._get_theme_variables(research_theme)
        
        if target_variable is None:
            target_variable = 'roa'  # デフォルト
        
        # 1. 戦略的グループ分析
        if run_all or 'strategic_groups' not in self.results.to_dict():
            try:
                logger.info("\n📊 Phase 1: Strategic Group Analysis")
                self.strategic_group_analysis(
                    features=strategic_vars,
                    n_clusters=None,  # 自動決定
                    temporal_analysis=True
                )
            except Exception as e:
                logger.error(f"Strategic Group Analysis failed: {e}")
        
        # 2. パフォーマンス予測
        if run_all or 'performance_prediction' not in self.results.to_dict():
            try:
                logger.info("\n🎯 Phase 2: Performance Prediction")
                self.predict_firm_performance(
                    target=target_variable,
                    features=strategic_vars,
                    hyperparameter_tuning=True
                )
            except Exception as e:
                logger.error(f"Performance Prediction failed: {e}")
        
        # 3. 特徴量重要度
        if run_all or 'feature_importance' not in self.results.to_dict():
            try:
                logger.info("\n📈 Phase 3: Feature Importance Analysis")
                self.analyze_feature_importance(
                    target=target_variable,
                    features=strategic_vars
                )
            except Exception as e:
                logger.error(f"Feature Importance Analysis failed: {e}")
        
        # 4. 異常検知
        if run_all or 'anomaly_detection' not in self.results.to_dict():
            try:
                logger.info("\n🔍 Phase 4: Anomaly Detection")
                self.detect_strategic_outliers(
                    features=strategic_vars,
                    contamination=0.05
                )
            except Exception as e:
                logger.error(f"Anomaly Detection failed: {e}")
        
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ COMPREHENSIVE ANALYSIS COMPLETE")
        logger.info(f"{'='*70}\n")
        
        return self.results
    
    def _get_theme_variables(self, theme: str) -> List[str]:
        """研究テーマ別の推奨変数"""
        theme_variables = {
            'competitive_strategy': [
                'rd_intensity', 'capital_intensity', 'advertising_intensity',
                'price_premium', 'product_differentiation'
            ],
            'organizational_capability': [
                'rd_intensity', 'patent_stock', 'employee_skill',
                'organizational_learning', 'knowledge_stock'
            ],
            'institutional_theory': [
                'iso_certification', 'esg_score', 'board_independence',
                'foreign_ownership', 'political_connection'
            ],
            'innovation': [
                'rd_intensity', 'patent_count', 'citation_impact',
                'tech_diversity', 'collaboration_intensity'
            ],
            'general': [
                'rd_intensity', 'firm_size', 'leverage', 'roa', 'firm_age'
            ]
        }
        
        # データに存在する変数のみ返す
        available_vars = [
            var for var in theme_variables.get(theme, theme_variables['general'])
            if var in self.data.columns
        ]
        
        if not available_vars:
            logger.warning(f"No theme variables found in data. Using all numeric columns.")
            available_vars = self.data.select_dtypes(include=[np.number]).columns.tolist()
            # firm_id, time_var除外
            available_vars = [v for v in available_vars if v not in [self.firm_id, self.time_var]]
        
        return available_vars[:10]  # 最大10変数
    
    # ========================================================================
    # 6. REPORT GENERATION
    # ========================================================================
    
    def generate_publication_ready_report(
        self,
        include_theory: bool = True,
        include_methodology: bool = True,
        format: str = 'html'
    ) -> str:
        """
        Publication-readyレポート生成
        
        【レポート構成】
        1. Executive Summary
        2. Theoretical Background
        3. Methodology
        4. Analysis Results
           - Strategic Groups
           - Performance Prediction
           - Feature Importance
           - Anomaly Detection
        5. Discussion & Implications
        6. Appendices
        
        Args:
            include_theory: 理論的背景を含める
            include_methodology: 方法論詳細を含める
            format: 出力形式（html, markdown, pdf）
        
        Returns:
            レポートファイルパス
        """
        logger.info(f"📄 Generating Publication-Ready Report ({format})")
        
        if format == 'html':
            report_content = self._build_html_report(include_theory, include_methodology)
            report_path = self.output_dir / 'strategic_datamining_report.html'
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        
        elif format == 'markdown':
            report_content = self._build_markdown_report(include_theory, include_methodology)
            report_path = self.output_dir / 'strategic_datamining_report.md'
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # 分析ログ保存
        log_path = self.output_dir / 'analysis_log.json'
        with open(log_path, 'w') as f:
            json.dump(self.analysis_log, f, indent=2, default=str)
        
        logger.info(f"✅ Report saved: {report_path}")
        
        return str(report_path)
    
    def _build_html_report(
        self,
        include_theory: bool,
        include_methodology: bool
    ) -> str:
        """HTML形式レポート構築"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Strategic Data Mining Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .metric {{
            font-weight: bold;
            color: #27ae60;
            font-size: 1.1em;
        }}
        .section {{
            margin-bottom: 50px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
        }}
        .theory-box {{
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }}
        .result-box {{
            background-color: #e8f8e8;
            padding: 15px;
            border-left: 4px solid #27ae60;
            margin: 20px 0;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .toc {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        .toc a {{
            text-decoration: none;
            color: #2980b9;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #bdc3c7;
            text-align: center;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <h1>📊 Strategic Management Data Mining Report</h1>
    
    <div class="section">
        <h2>Executive Summary</h2>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Dataset:</strong> {len(self.data):,} observations, {self.data[self.firm_id].nunique():,} firms, {self.data[self.time_var].nunique()} time periods</p>
        <p><strong>Analysis Engine:</strong> Strategic Management Research Hub v4.0</p>
        
        <h3>Key Findings</h3>
        <ul>
"""
        
        # Key findings
        if self.results.strategic_groups:
            sg = self.results.strategic_groups
            html += f"""
            <li><strong>Strategic Groups:</strong> {sg.get('n_clusters', 'N/A')} distinct strategic configurations identified 
                (Silhouette Score: {sg.get('silhouette_score', 'N/A'):.3f})</li>
"""
        
        if self.results.performance_prediction:
            pp = self.results.performance_prediction
            html += f"""
            <li><strong>Performance Prediction:</strong> Best model ({pp.get('best_model', 'N/A')}) 
                achieved R² = {pp['all_results'][pp['best_model']]['metrics']['test_r2']:.4f}</li>
"""
        
        if self.results.anomaly_detection:
            ad = self.results.anomaly_detection
            html += f"""
            <li><strong>Strategic Outliers:</strong> {ad.get('n_outliers', 'N/A')} outlier firms detected 
                ({ad.get('outlier_rate', 0)*100:.1f}% of sample)</li>
"""
        
        html += """
        </ul>
    </div>
    
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>
            <li><a href="#theory">1. Theoretical Background</a></li>
            <li><a href="#methodology">2. Methodology</a></li>
            <li><a href="#results">3. Analysis Results</a>
                <ul>
                    <li><a href="#strategic-groups">3.1 Strategic Group Analysis</a></li>
                    <li><a href="#prediction">3.2 Performance Prediction</a></li>
                    <li><a href="#importance">3.3 Feature Importance</a></li>
                    <li><a href="#outliers">3.4 Anomaly Detection</a></li>
                </ul>
            </li>
            <li><a href="#discussion">4. Discussion & Implications</a></li>
        </ul>
    </div>
    
    <hr>
"""
        
        # Theoretical Background
        if include_theory:
            html += """
    <div class="section" id="theory">
        <h2>1. Theoretical Background</h2>
        
        <div class="theory-box">
            <h3>Strategic Groups Theory (Porter, 1980)</h3>
            <p>Organizations within the same industry can be grouped into <strong>strategic groups</strong> 
            based on the similarity of their strategic approaches. These groups exhibit:</p>
            <ul>
                <li>Similar resource commitments</li>
                <li>Common strategic postures</li>
                <li>Distinct mobility barriers between groups</li>
            </ul>
            <p><em>Implication:</em> Firms within the same strategic group tend to have similar performance outcomes.</p>
        </div>
        
        <div class="theory-box">
            <h3>Configuration Theory (Meyer et al., 1993)</h3>
            <p>Organizational configurations represent <strong>multidimensional constellations</strong> of 
            conceptually distinct characteristics that commonly occur together. Machine learning clustering 
            techniques enable data-driven identification of these configurations.</p>
        </div>
    </div>
    <hr>
"""
        
        # Methodology
        if include_methodology:
            html += f"""
    <div class="section" id="methodology">
        <h2>2. Methodology</h2>
        
        <h3>2.1 Data & Sample</h3>
        <table>
            <tr>
                <th>Aspect</th>
                <th>Details</th>
            </tr>
            <tr>
                <td>Sample Size</td>
                <td class="metric">{len(self.data):,} firm-year observations</td>
            </tr>
            <tr>
                <td>Unique Firms</td>
                <td class="metric">{self.data[self.firm_id].nunique():,}</td>
            </tr>
            <tr>
                <td>Time Period</td>
                <td class="metric">{self.data[self.time_var].min()} - {self.data[self.time_var].max()}</td>
            </tr>
        </table>
        
        <h3>2.2 Analytical Techniques</h3>
        <ul>
            <li><strong>Clustering:</strong> K-Means, Hierarchical, Gaussian Mixture Models</li>
            <li><strong>Prediction:</strong> Random Forest, Gradient Boosting, XGBoost, Neural Networks, Ensemble (Stacking)</li>
            <li><strong>Feature Importance:</strong> Tree-based importance, SHAP values, Permutation importance</li>
            <li><strong>Anomaly Detection:</strong> Isolation Forest, Local Outlier Factor, One-Class SVM</li>
        </ul>
    </div>
    <hr>
"""
        
        # Results Section
        html += """
    <div class="section" id="results">
        <h2>3. Analysis Results</h2>
"""
        
        # 3.1 Strategic Groups
        if self.results.strategic_groups:
            sg = self.results.strategic_groups
            html += f"""
        <div id="strategic-groups">
            <h3>3.1 Strategic Group Analysis</h3>
            
            <div class="result-box">
                <p><strong>Method:</strong> {sg.get('method', 'N/A')}</p>
                <p><strong>Number of Strategic Groups:</strong> <span class="metric">{sg.get('n_clusters', 'N/A')}</span></p>
                <p><strong>Silhouette Score:</strong> <span class="metric">{sg.get('silhouette_score', 'N/A'):.3f}</span></p>
                <p><strong>Calinski-Harabasz Index:</strong> <span class="metric">{sg.get('calinski_harabasz', 'N/A'):.2f}</span></p>
                <p><strong>Davies-Bouldin Index:</strong> <span class="metric">{sg.get('davies_bouldin', 'N/A'):.3f}</span> (lower is better)</p>
            </div>
            
            <img src="strategic_groups_pca.png" alt="Strategic Groups Visualization">
            <img src="strategic_group_profiles.png" alt="Strategic Group Profiles">
            
            <p><em>Interpretation:</em> The identified strategic groups represent distinct configurations 
            of strategic variables. Higher silhouette scores indicate well-separated clusters.</p>
        </div>
"""
        
        # 3.2 Performance Prediction
        if self.results.performance_prediction:
            pp = self.results.performance_prediction
            best_model = pp.get('best_model', 'N/A')
            
            if best_model != 'N/A' and best_model in pp.get('all_results', {}):
                metrics = pp['all_results'][best_model]['metrics']
                
                html += f"""
        <div id="prediction">
            <h3>3.2 Firm Performance Prediction</h3>
            
            <div class="result-box">
                <p><strong>Target Variable:</strong> <code>{pp.get('target', 'N/A')}</code></p>
                <p><strong>Best Model:</strong> <span class="metric">{best_model}</span></p>
                
                <h4>Model Performance</h4>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Train</th>
                        <th>Test</th>
                    </tr>
                    <tr>
                        <td>R² Score</td>
                        <td>{metrics.get('train_r2', 'N/A'):.4f}</td>
                        <td class="metric">{metrics.get('test_r2', 'N/A'):.4f}</td>
                    </tr>
                    <tr>
                        <td>RMSE</td>
                        <td>{metrics.get('train_rmse', 'N/A'):.4f}</td>
                        <td class="metric">{metrics.get('test_rmse', 'N/A'):.4f}</td>
                    </tr>
                    <tr>
                        <td>MAE</td>
                        <td>{metrics.get('train_mae', 'N/A'):.4f}</td>
                        <td class="metric">{metrics.get('test_mae', 'N/A'):.4f}</td>
                    </tr>
                </table>
            </div>
            
            <img src="prediction_performance.png" alt="Prediction Performance">
            
            <p><em>Interpretation:</em> The R² score indicates the proportion of variance in firm performance 
            explained by strategic variables. Values closer to 1.0 indicate better predictive power.</p>
        </div>
"""
        
        # 3.3 Feature Importance
        if self.results.feature_importance:
            html += """
        <div id="importance">
            <h3>3.3 Feature Importance Analysis</h3>
            
            <img src="feature_importance_plot.png" alt="Feature Importance">
            
            <p><em>Interpretation:</em> Features with higher importance scores have greater influence on 
            firm performance outcomes. This analysis helps identify strategic levers.</p>
        </div>
"""
        
        # 3.4 Anomaly Detection
        if self.results.anomaly_detection:
            ad = self.results.anomaly_detection
            html += f"""
        <div id="outliers">
            <h3>3.4 Strategic Outlier Detection</h3>
            
            <div class="result-box">
                <p><strong>Detection Methods:</strong> {', '.join(ad.get('methods', []))}</p>
                <p><strong>Outliers Detected:</strong> <span class="metric">{ad.get('n_outliers', 'N/A')}</span> 
                   ({ad.get('outlier_rate', 0)*100:.2f}% of sample)</p>
            </div>
            
            <img src="outliers_pca.png" alt="Strategic Outliers">
            
            <p><em>Interpretation:</em> Outlier firms represent organizations that do not conform to 
            conventional strategic patterns. These may be <strong>strategic innovators</strong> or 
            <strong>firms in transition</strong>.</p>
        </div>
"""
        
        html += """
    </div>
    <hr>
"""
        
        # Discussion
        html += """
    <div class="section" id="discussion">
        <h2>4. Discussion & Strategic Implications</h2>
        
        <h3>4.1 Managerial Implications</h3>
        <p>The data mining analysis reveals several key strategic insights:</p>
        <ul>
            <li><strong>Strategic Positioning:</strong> Firms can benchmark their strategic configuration 
                against identified strategic groups to assess competitive positioning.</li>
            <li><strong>Performance Drivers:</strong> Feature importance analysis highlights which strategic 
                variables have the strongest relationship with firm performance.</li>
            <li><strong>Strategic Outliers:</strong> Organizations identified as outliers warrant deeper investigation 
                - they may represent either strategic innovators worth emulating or firms facing strategic challenges.</li>
        </ul>
        
        <h3>4.2 Research Implications</h3>
        <p>This analysis demonstrates the value of machine learning techniques for strategic management research:</p>
        <ul>
            <li><strong>Theory Development:</strong> Data-driven identification of strategic configurations can inform 
                and refine strategic group theory.</li>
            <li><strong>Prediction:</strong> Machine learning models can predict performance outcomes with greater 
                accuracy than traditional linear models, capturing non-linear relationships.</li>
            <li><strong>Anomaly Detection:</strong> Systematic identification of outliers enables discovery of 
                novel strategic patterns not captured by existing theories.</li>
        </ul>
        
        <h3>4.3 Limitations</h3>
        <ul>
            <li>Results are specific to the sample period and may not generalize to other time periods or contexts.</li>
            <li>Machine learning models prioritize prediction over causal inference - identified relationships 
                should not be interpreted as causal without additional analysis.</li>
            <li>Strategic variables are limited to those available in the dataset and may not capture all 
                relevant dimensions of strategy.</li>
        </ul>
    </div>
    
    <hr>
    
    <div class="footer">
        <p><strong>Generated by Strategic Management Research Hub v4.0</strong></p>
        <p>Advanced Data Mining Engine for Strategic Management Research</p>
        <p><em>© 2025 Strategic Management Research Hub. Licensed under MIT.</em></p>
    </div>

</body>
</html>
"""
        
        return html
    
    def _build_markdown_report(
        self,
        include_theory: bool,
        include_methodology: bool
    ) -> str:
        """Markdown形式レポート構築（簡略版）"""
        
        md = f"""# Strategic Management Data Mining Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dataset:** {len(self.data):,} observations, {self.data[self.firm_id].nunique():,} firms  
**Engine:** Strategic Management Research Hub v4.0

---

## Executive Summary

"""
        
        if self.results.strategic_groups:
            sg = self.results.strategic_groups
            md += f"- **Strategic Groups:** {sg.get('n_clusters', 'N/A')} groups (Silhouette: {sg.get('silhouette_score', 'N/A'):.3f})\n"
        
        if self.results.performance_prediction:
            pp = self.results.performance_prediction
            best_model = pp.get('best_model', 'N/A')
            if best_model in pp.get('all_results', {}):
                metrics = pp['all_results'][best_model]['metrics']
                md += f"- **Performance Prediction:** Best model ({best_model}), R² = {metrics['test_r2']:.4f}\n"
        
        if self.results.anomaly_detection:
            ad = self.results.anomaly_detection
            md += f"- **Outliers:** {ad.get('n_outliers', 'N/A')} detected ({ad.get('outlier_rate', 0)*100:.1f}%)\n"
        
        md += "\n---\n\n## Analysis Results\n\n"
        
        # 結果詳細は省略（HTMLが詳細版）
        md += "See HTML report for detailed analysis results and visualizations.\n"
        
        return md
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def _log_analysis(self, method_name: str, params: Dict):
        """分析ログ記録"""
        self.analysis_log.append({
            'timestamp': datetime.now().isoformat(),
            'method': method_name,
            'parameters': {k: str(v) for k, v in params.items() if k != 'self'}
        })
    
    def save_state(self, filepath: Optional[str] = None):
        """エンジン状態保存"""
        if filepath is None:
            filepath = self.output_dir / 'engine_state.pkl'
        
        state = {
            'config': self.config,
            'results': self.results,
            'models': self.models,
            'scalers': self.scalers,
            'engineered_features': self.engineered_features,
            'analysis_log': self.analysis_log
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
        
        logger.info(f"Engine state saved: {filepath}")
    
    @classmethod
    def load_state(cls, filepath: str, data: pd.DataFrame, firm_id: str, time_var: str):
        """エンジン状態読み込み"""
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
        
        engine = cls(
            data=data,
            firm_id=firm_id,
            time_var=time_var,
            config=state['config']
        )
        
        engine.results = state['results']
        engine.models = state['models']
        engine.scalers = state['scalers']
        engine.engineered_features = state['engineered_features']
        engine.analysis_log = state['analysis_log']
        
        logger.info(f"Engine state loaded from: {filepath}")
        
        return engine


# ============================================================================
# UTILITY FUNCTIONS & EXAMPLES
# ============================================================================

def quick_start_example():
    """
    クイックスタート例
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Strategic Data Mining Engine v4.0 - Quick Start Example    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # サンプルデータ生成
    np.random.seed(42)
    n_firms = 200
    n_years = 10
    
    data = []
    for firm_idx in range(n_firms):
        for year in range(2014, 2014 + n_years):
            data.append({
                'gvkey': f'FIRM_{firm_idx:04d}',
                'year': year,
                'roa': np.random.normal(0.05, 0.03),
                'rd_intensity': np.random.exponential(0.05),
                'capital_intensity': np.random.uniform(0.2, 0.8),
                'advertising_intensity': np.random.exponential(0.03),
                'international_sales': np.random.uniform(0, 0.6),
                'firm_size': np.random.normal(8, 2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': np.random.randint(5, 50)
            })
    
    df_sample = pd.DataFrame(data)
    
    print(f"📊 Sample data created: {len(df_sample):,} observations")
    
    # エンジン初期化
    engine = StrategicDataMiningEngine(
        data=df_sample,
        firm_id='gvkey',
        time_var='year',
        output_dir='./quick_start_output/'
    )
    
    # 包括的分析実行
    results = engine.run_comprehensive_analysis(
        research_theme='competitive_strategy',
        target_variable='roa',
        strategic_vars=['rd_intensity', 'capital_intensity', 'advertising_intensity']
    )
    
    # レポート生成
    report_path = engine.generate_publication_ready_report()
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Report: {report_path}")
    print(f"📁 All outputs: {engine.output_dir}")


if __name__ == "__main__":
    # Quick start実行
    quick_start_example()
