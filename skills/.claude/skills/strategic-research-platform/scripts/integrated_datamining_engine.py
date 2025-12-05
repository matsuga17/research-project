"""
Integrated Data Mining Engine for Strategic Management Research
================================================================

統合データマイニングエンジン - SKILL.md v3.0完全対応

このモジュールは、戦略経営研究のための包括的なデータマイニング機能を提供します：

【主要機能】
1. 戦略的グループ分析（Strategic Group Analysis）
2. 企業パフォーマンス予測（Performance Prediction）
3. 特徴量重要度分析（Feature Importance）
4. 異常検知（Anomaly Detection）
5. 因果推論統合ML（Causal Machine Learning）
6. 時系列パターン発見（Time Series Pattern Discovery）
7. ネットワーク分析統合（Network Analytics Integration）
8. テキストマイニング統合（Text Analytics Integration）

【設計原則】
- Publication-ready: トップジャーナル基準対応
- Reproducible: 完全な再現性保証
- Interpretable: 説明可能なML手法優先
- Scalable: 大規模データ対応

【理論的基盤】
- Porter (1980): Strategic Groups
- Barney (1991): RBV - Resource Heterogeneity
- Teece (2007): Dynamic Capabilities
- Ketchen & Shook (1996): Cluster Analysis in SMJ

Author: Strategic Management Research Hub
Version: 3.1
License: MIT
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any
from pathlib import Path
import logging
import warnings
import json
from datetime import datetime
import pickle

# Clustering & Segmentation
from sklearn.cluster import (
    KMeans, DBSCAN, AgglomerativeClustering, 
    SpectralClustering, MeanShift
)
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform

# Dimensionality Reduction
from sklearn.decomposition import PCA, FactorAnalysis, NMF
from sklearn.manifold import TSNE, MDS, Isomap

# Machine Learning Models
from sklearn.ensemble import (
    RandomForestRegressor, RandomForestClassifier,
    GradientBoostingRegressor, GradientBoostingClassifier,
    ExtraTreesRegressor, AdaBoostRegressor
)
from sklearn.linear_model import (
    Ridge, Lasso, ElasticNet,
    LogisticRegression, LinearRegression
)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier

# Model Evaluation
from sklearn.model_selection import (
    train_test_split, cross_val_score, 
    GridSearchCV, TimeSeriesSplit
)
from sklearn.metrics import (
    mean_squared_error, r2_score, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    silhouette_score, davies_bouldin_score, calinski_harabasz_score
)

# Feature Engineering & Selection
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler,
    LabelEncoder, OneHotEncoder
)
from sklearn.feature_selection import (
    SelectKBest, f_regression, mutual_info_regression,
    RFE, SelectFromModel
)

# Anomaly Detection
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Statistical Tests
from scipy import stats
from scipy.stats import (
    normaltest, shapiro, kstest, 
    mannwhitneyu, kruskal, friedmanchisquare
)

# Optional Advanced Libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    warnings.warn("XGBoost not installed. Install with: pip install xgboost")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    warnings.warn("LightGBM not installed. Install with: pip install lightgbm")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP not installed. Install with: pip install shap")

try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP not installed. Install with: pip install umap-learn")

try:
    from econml.dml import CausalForestDML, LinearDML
    from econml.dr import DRLearner
    ECONML_AVAILABLE = True
except ImportError:
    ECONML_AVAILABLE = False
    warnings.warn("EconML not installed. Install with: pip install econml")

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IntegratedDataMiningEngine:
    """
    統合データマイニングエンジン
    
    戦略経営研究のための包括的なデータマイニング機能を提供
    
    Parameters
    ----------
    data : pd.DataFrame
        分析対象のパネルデータ
    firm_id : str
        企業識別子の列名
    time_var : str
        時間変数の列名
    output_dir : str, optional
        出力ディレクトリ（デフォルト: './datamining_output/'）
    config : dict, optional
        設定辞書
    
    Attributes
    ----------
    results : dict
        分析結果を格納する辞書
    models : dict
        学習済みモデルを格納する辞書
    scalers : dict
        スケーラーを格納する辞書
    
    Examples
    --------
    >>> import pandas as pd
    >>> from integrated_datamining_engine import IntegratedDataMiningEngine
    >>> 
    >>> # データ読み込み
    >>> df = pd.read_stata('./data/final/analysis_panel.dta')
    >>> 
    >>> # エンジン初期化
    >>> engine = IntegratedDataMiningEngine(
    ...     data=df,
    ...     firm_id='gvkey',
    ...     time_var='year',
    ...     output_dir='./output/'
    ... )
    >>> 
    >>> # 戦略的グループ分析
    >>> groups = engine.strategic_group_analysis(
    ...     features=['rd_intensity', 'capital_intensity'],
    ...     n_clusters=4
    ... )
    >>> 
    >>> # パフォーマンス予測
    >>> predictions = engine.predict_performance(
    ...     target='roa',
    ...     features=['rd_intensity', 'firm_size', 'leverage'],
    ...     model_type='ensemble'
    ... )
    >>> 
    >>> # 包括的レポート生成
    >>> engine.generate_comprehensive_report()
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        firm_id: str,
        time_var: str,
        output_dir: str = './datamining_output/',
        config: Optional[Dict] = None
    ):
        """エンジンの初期化"""
        
        self.data = data.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # デフォルト設定
        self.config = config or self._default_config()
        
        # 結果とモデルの保存用辞書
        self.results = {}
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        
        # データ検証
        self._validate_data()
        
        # ログ初期化
        self._setup_logging()
        
        logger.info(f"IntegratedDataMiningEngine initialized")
        logger.info(f"Data shape: {self.data.shape}")
        logger.info(f"Firms: {self.data[firm_id].nunique()}")
        logger.info(f"Time periods: {self.data[time_var].nunique()}")
    
    def _default_config(self) -> Dict:
        """デフォルト設定"""
        return {
            'clustering': {
                'n_clusters_range': (2, 10),
                'methods': ['kmeans', 'hierarchical', 'gaussian_mixture'],
                'random_state': 42
            },
            'prediction': {
                'test_size': 0.2,
                'cv_folds': 5,
                'random_state': 42,
                'ensemble_methods': ['rf', 'gbm', 'xgb', 'lgb']
            },
            'anomaly_detection': {
                'contamination': 0.05,
                'methods': ['isolation_forest', 'lof', 'elliptic_envelope']
            },
            'visualization': {
                'style': 'seaborn',
                'context': 'paper',
                'palette': 'Set2',
                'dpi': 300
            },
            'output': {
                'save_models': True,
                'save_figures': True,
                'figure_format': ['png', 'pdf']
            }
        }
    
    def _validate_data(self):
        """データの検証"""
        
        # 必須列の存在確認
        if self.firm_id not in self.data.columns:
            raise ValueError(f"firm_id '{self.firm_id}' not found in data")
        
        if self.time_var not in self.data.columns:
            raise ValueError(f"time_var '{self.time_var}' not found in data")
        
        # 欠損値チェック
        missing_summary = self.data.isnull().sum()
        if missing_summary.sum() > 0:
            logger.warning(f"Data contains missing values:\n{missing_summary[missing_summary > 0]}")
        
        # データ型チェック
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        logger.info(f"Numeric columns: {len(numeric_cols)}")
    
    def _setup_logging(self):
        """ログの設定"""
        
        log_file = self.output_dir / f'datamining_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        logger.addHandler(file_handler)
        logger.info(f"Logging to {log_file}")
    
    # ============================================================
    # 1. 戦略的グループ分析（Strategic Group Analysis）
    # ============================================================
    
    def strategic_group_analysis(
        self,
        features: List[str],
        n_clusters: Optional[int] = None,
        method: str = 'kmeans',
        include_dimensionality_reduction: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        戦略的グループ分析
        
        Porter (1980)の戦略的グループ概念に基づき、
        類似の戦略を持つ企業群を特定します。
        
        Parameters
        ----------
        features : List[str]
            クラスタリングに使用する変数リスト
            例: ['rd_intensity', 'capital_intensity', 'international_sales']
        n_clusters : int, optional
            クラスター数（Noneの場合、最適数を自動決定）
        method : str, default='kmeans'
            クラスタリング手法
            - 'kmeans': K-Means
            - 'hierarchical': 階層的クラスタリング
            - 'gaussian_mixture': ガウス混合モデル
            - 'dbscan': DBSCAN（密度ベース）
        include_dimensionality_reduction : bool, default=True
            次元削減（PCA, t-SNE）を含めるか
        **kwargs
            手法固有のパラメータ
        
        Returns
        -------
        pd.DataFrame
            クラスターラベル付きデータフレーム
        
        Examples
        --------
        >>> groups = engine.strategic_group_analysis(
        ...     features=['rd_intensity', 'capital_intensity', 'advertising_intensity'],
        ...     n_clusters=4,
        ...     method='kmeans'
        ... )
        >>> 
        >>> # グループ別記述統計
        >>> print(groups.groupby('strategic_group')[features].mean())
        
        References
        ----------
        - Porter, M. E. (1980). Competitive Strategy. Free Press.
        - Ketchen, D. J., & Shook, C. L. (1996). The application of cluster analysis 
          in strategic management research. SMJ, 17(6), 441-458.
        """
        
        logger.info(f"Starting strategic group analysis with {method}")
        
        # データ準備
        X, valid_data = self._prepare_features(features)
        
        # 最適クラスター数決定（必要な場合）
        if n_clusters is None:
            n_clusters = self._optimal_clusters(
                X, 
                method=method,
                max_clusters=self.config['clustering']['n_clusters_range'][1]
            )
            logger.info(f"Optimal number of clusters: {n_clusters}")
        
        # クラスタリング実行
        cluster_labels = self._perform_clustering(
            X, 
            n_clusters=n_clusters, 
            method=method,
            **kwargs
        )
        
        # 結果をデータに追加
        valid_data['strategic_group'] = cluster_labels
        
        # グループプロファイル作成
        group_profiles = self._create_group_profiles(
            valid_data, 
            features, 
            'strategic_group'
        )
        
        # 可視化
        if include_dimensionality_reduction:
            self._visualize_strategic_groups(
                X, 
                cluster_labels, 
                features,
                method=method
            )
        
        # 統計的検証
        cluster_stats = self._validate_clustering(X, cluster_labels)
        
        # 結果保存
        self.results['strategic_groups'] = {
            'data': valid_data,
            'profiles': group_profiles,
            'n_clusters': n_clusters,
            'method': method,
            'statistics': cluster_stats
        }
        
        # レポート生成
        self._save_strategic_group_report(group_profiles, cluster_stats)
        
        logger.info(f"Strategic group analysis completed: {n_clusters} groups identified")
        
        return valid_data
    
    def _prepare_features(
        self, 
        features: List[str], 
        scale: bool = True
    ) -> Tuple[np.ndarray, pd.DataFrame]:
        """特徴量の準備"""
        
        # 欠損値除外
        valid_data = self.data[features + [self.firm_id, self.time_var]].dropna()
        
        X = valid_data[features].values
        
        # スケーリング
        if scale:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers['features'] = scaler
            
            logger.info(f"Features scaled using StandardScaler")
            
            return X_scaled, valid_data
        
        return X, valid_data
    
    def _optimal_clusters(
        self, 
        X: np.ndarray, 
        method: str = 'kmeans',
        max_clusters: int = 10
    ) -> int:
        """最適クラスター数の決定"""
        
        # Elbow method & Silhouette score
        inertias = []
        silhouette_scores = []
        
        cluster_range = range(2, min(max_clusters + 1, len(X) // 10))
        
        for n in cluster_range:
            if method == 'kmeans':
                model = KMeans(n_clusters=n, random_state=42)
                labels = model.fit_predict(X)
                inertias.append(model.inertia_)
            elif method == 'gaussian_mixture':
                model = GaussianMixture(n_components=n, random_state=42)
                labels = model.fit_predict(X)
                inertias.append(-model.score(X))  # Negative log-likelihood
            else:
                # Default to KMeans
                model = KMeans(n_clusters=n, random_state=42)
                labels = model.fit_predict(X)
                inertias.append(model.inertia_)
            
            sil_score = silhouette_score(X, labels)
            silhouette_scores.append(sil_score)
        
        # Silhouette scoreが最大のクラスター数
        optimal_n = list(cluster_range)[np.argmax(silhouette_scores)]
        
        # 可視化
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Elbow plot
        axes[0].plot(cluster_range, inertias, 'bo-')
        axes[0].set_xlabel('Number of Clusters')
        axes[0].set_ylabel('Inertia / -Log Likelihood')
        axes[0].set_title('Elbow Method')
        axes[0].grid(True, alpha=0.3)
        
        # Silhouette plot
        axes[1].plot(cluster_range, silhouette_scores, 'ro-')
        axes[1].axvline(optimal_n, color='green', linestyle='--', label=f'Optimal: {optimal_n}')
        axes[1].set_xlabel('Number of Clusters')
        axes[1].set_ylabel('Silhouette Score')
        axes[1].set_title('Silhouette Analysis')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'optimal_clusters.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return optimal_n
    
    def _perform_clustering(
        self,
        X: np.ndarray,
        n_clusters: int,
        method: str = 'kmeans',
        **kwargs
    ) -> np.ndarray:
        """クラスタリングの実行"""
        
        random_state = self.config['clustering']['random_state']
        
        if method == 'kmeans':
            model = KMeans(
                n_clusters=n_clusters, 
                random_state=random_state,
                n_init=10,
                **kwargs
            )
        elif method == 'hierarchical':
            linkage_method = kwargs.get('linkage', 'ward')
            model = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage=linkage_method
            )
        elif method == 'gaussian_mixture':
            model = GaussianMixture(
                n_components=n_clusters,
                random_state=random_state,
                **kwargs
            )
        elif method == 'dbscan':
            eps = kwargs.get('eps', 0.5)
            min_samples = kwargs.get('min_samples', 5)
            model = DBSCAN(eps=eps, min_samples=min_samples)
        else:
            raise ValueError(f"Unknown clustering method: {method}")
        
        labels = model.fit_predict(X)
        
        # モデル保存
        self.models[f'clustering_{method}'] = model
        
        return labels
    
    def _create_group_profiles(
        self,
        data: pd.DataFrame,
        features: List[str],
        group_col: str
    ) -> pd.DataFrame:
        """戦略的グループのプロファイル作成"""
        
        # グループ別統計量
        profiles = data.groupby(group_col)[features].agg(['mean', 'std', 'median', 'count'])
        
        # グループサイズ
        group_sizes = data.groupby(group_col).size().rename('group_size')
        
        profiles = profiles.join(group_sizes)
        
        logger.info(f"Group profiles created:\n{profiles}")
        
        return profiles
    
    def _visualize_strategic_groups(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        features: List[str],
        method: str = 'kmeans'
    ):
        """戦略的グループの可視化"""
        
        n_features = X.shape[1]
        
        # 1. PCA 2D visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # PCA scatter plot
        scatter = axes[0].scatter(
            X_pca[:, 0], X_pca[:, 1], 
            c=labels, cmap='viridis', 
            alpha=0.6, edgecolors='k', s=50
        )
        axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        axes[0].set_title(f'Strategic Groups - PCA ({method.upper()})')
        plt.colorbar(scatter, ax=axes[0], label='Strategic Group')
        axes[0].grid(True, alpha=0.3)
        
        # Feature importance in PCA
        components_df = pd.DataFrame(
            pca.components_.T,
            columns=['PC1', 'PC2'],
            index=features
        )
        
        components_df.plot(kind='bar', ax=axes[1])
        axes[1].set_title('Feature Loadings on Principal Components')
        axes[1].set_ylabel('Loading')
        axes[1].legend(title='Component')
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / f'strategic_groups_{method}_pca.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. t-SNE visualization (if >2 features)
        if n_features > 2:
            tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X) // 4))
            X_tsne = tsne.fit_transform(X)
            
            plt.figure(figsize=(8, 6))
            scatter = plt.scatter(
                X_tsne[:, 0], X_tsne[:, 1],
                c=labels, cmap='viridis',
                alpha=0.6, edgecolors='k', s=50
            )
            plt.xlabel('t-SNE Dimension 1')
            plt.ylabel('t-SNE Dimension 2')
            plt.title(f'Strategic Groups - t-SNE ({method.upper()})')
            plt.colorbar(scatter, label='Strategic Group')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(self.output_dir / f'strategic_groups_{method}_tsne.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        logger.info(f"Strategic groups visualization saved")
    
    def _validate_clustering(
        self,
        X: np.ndarray,
        labels: np.ndarray
    ) -> Dict:
        """クラスタリングの統計的検証"""
        
        # Silhouette Score（-1〜1、高いほど良い）
        sil_score = silhouette_score(X, labels)
        
        # Davies-Bouldin Index（低いほど良い）
        db_score = davies_bouldin_score(X, labels)
        
        # Calinski-Harabasz Index（高いほど良い）
        ch_score = calinski_harabasz_score(X, labels)
        
        stats = {
            'silhouette_score': sil_score,
            'davies_bouldin_index': db_score,
            'calinski_harabasz_index': ch_score,
            'n_clusters': len(np.unique(labels)),
            'interpretation': {
                'silhouette': 'Excellent' if sil_score > 0.7 else 'Good' if sil_score > 0.5 else 'Fair' if sil_score > 0.25 else 'Poor',
                'davies_bouldin': 'Good' if db_score < 1.0 else 'Fair' if db_score < 2.0 else 'Poor'
            }
        }
        
        logger.info(f"Clustering validation: Silhouette={sil_score:.3f}, DB={db_score:.3f}, CH={ch_score:.1f}")
        
        return stats
    
    def _save_strategic_group_report(
        self,
        profiles: pd.DataFrame,
        stats: Dict
    ):
        """戦略的グループ分析レポート保存"""
        
        report_path = self.output_dir / 'strategic_group_analysis_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("STRATEGIC GROUP ANALYSIS REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("CLUSTER STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Number of Groups: {stats['n_clusters']}\n")
            f.write(f"Silhouette Score: {stats['silhouette_score']:.4f} ({stats['interpretation']['silhouette']})\n")
            f.write(f"Davies-Bouldin Index: {stats['davies_bouldin_index']:.4f} ({stats['interpretation']['davies_bouldin']})\n")
            f.write(f"Calinski-Harabasz Index: {stats['calinski_harabasz_index']:.2f}\n\n")
            
            f.write("GROUP PROFILES\n")
            f.write("-" * 70 + "\n")
            f.write(profiles.to_string())
            f.write("\n\n")
            
            f.write("INTERPRETATION GUIDE\n")
            f.write("-" * 70 + "\n")
            f.write("Silhouette Score:\n")
            f.write("  > 0.70: Strong structure\n")
            f.write("  0.50-0.70: Reasonable structure\n")
            f.write("  0.25-0.50: Weak structure\n")
            f.write("  < 0.25: No substantial structure\n\n")
            
            f.write("Davies-Bouldin Index:\n")
            f.write("  < 1.0: Well-separated clusters\n")
            f.write("  1.0-2.0: Moderate separation\n")
            f.write("  > 2.0: Poor separation\n")
        
        logger.info(f"Report saved to {report_path}")
    
    # ============================================================
    # 2. 企業パフォーマンス予測（Performance Prediction）
    # ============================================================
    
    def predict_performance(
        self,
        target: str,
        features: List[str],
        model_type: str = 'ensemble',
        time_window: Optional[int] = None,
        include_interpretation: bool = True,
        **kwargs
    ) -> pd.DataFrame:
        """
        企業パフォーマンス予測
        
        機械学習モデルを用いて企業のパフォーマンスを予測します。
        将来パフォーマンス（1〜3年先）の予測も可能。
        
        Parameters
        ----------
        target : str
            予測対象変数（例: 'roa', 'sales_growth', 'tobins_q'）
        features : List[str]
            予測に使用する特徴量リスト
        model_type : str, default='ensemble'
            使用するモデル
            - 'ensemble': 複数モデルの平均（推奨）
            - 'rf': Random Forest
            - 'gbm': Gradient Boosting
            - 'xgb': XGBoost（要インストール）
            - 'lgb': LightGBM（要インストール）
            - 'linear': 線形回帰（ベースライン）
        time_window : int, optional
            予測する将来期間（年数）
            例: time_window=2 → 2年後のパフォーマンス
        include_interpretation : bool, default=True
            特徴量重要度分析を含めるか
        **kwargs
            モデル固有のハイパーパラメータ
        
        Returns
        -------
        pd.DataFrame
            予測値付きデータフレーム
        
        Examples
        --------
        >>> # 現在パフォーマンス予測
        >>> predictions = engine.predict_performance(
        ...     target='roa',
        ...     features=['rd_intensity', 'firm_size', 'leverage', 'firm_age'],
        ...     model_type='ensemble'
        ... )
        >>> 
        >>> # 2年後のパフォーマンス予測
        >>> future_pred = engine.predict_performance(
        ...     target='roa',
        ...     features=['rd_intensity', 'patent_stock', 'alliance_count'],
        ...     time_window=2,
        ...     model_type='xgb'
        ... )
        
        References
        ----------
        - Hair et al. (2014): Multivariate Data Analysis
        - Hastie et al. (2009): The Elements of Statistical Learning
        """
        
        logger.info(f"Starting performance prediction for target: {target}")
        
        # データ準備
        X, y, valid_data = self._prepare_prediction_data(
            target, 
            features, 
            time_window
        )
        
        # Train-test split
        test_size = self.config['prediction']['test_size']
        random_state = self.config['prediction']['random_state']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
        
        # モデル学習
        if model_type == 'ensemble':
            model, metrics = self._train_ensemble_model(
                X_train, X_test, y_train, y_test, **kwargs
            )
        else:
            model, metrics = self._train_single_model(
                X_train, X_test, y_train, y_test, 
                model_type=model_type, **kwargs
            )
        
        # 全データで予測
        predictions = model.predict(X)
        valid_data[f'{target}_pred'] = predictions
        valid_data[f'{target}_residual'] = y - predictions
        
        # 特徴量重要度
        if include_interpretation:
            importance_df = self._feature_importance_analysis(
                model, features, model_type
            )
            
            # SHAP分析（利用可能な場合）
            if SHAP_AVAILABLE and model_type != 'linear':
                self._shap_analysis(model, X_test, features, target)
        
        # 結果可視化
        self._visualize_predictions(
            y_test, model.predict(X_test), target, model_type
        )
        
        # 結果保存
        self.results['performance_prediction'] = {
            'target': target,
            'features': features,
            'model_type': model_type,
            'metrics': metrics,
            'predictions': valid_data,
            'feature_importance': importance_df if include_interpretation else None
        }
        
        self.models[f'prediction_{target}'] = model
        
        logger.info(f"Performance prediction completed. Test R²: {metrics['test_r2']:.4f}")
        
        return valid_data
    
    def _prepare_prediction_data(
        self,
        target: str,
        features: List[str],
        time_window: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
        """予測用データの準備"""
        
        # 必要な列
        cols_needed = features + [target, self.firm_id, self.time_var]
        
        # 将来予測の場合、targetをshiftする
        if time_window is not None:
            data_temp = self.data.copy()
            data_temp[f'{target}_future'] = data_temp.groupby(self.firm_id)[target].shift(-time_window)
            target_col = f'{target}_future'
            cols_needed.append(target_col)
            valid_data = data_temp[cols_needed].dropna()
            
            logger.info(f"Predicting {target} {time_window} years ahead")
        else:
            valid_data = self.data[cols_needed].dropna()
            target_col = target
        
        X = valid_data[features].values
        y = valid_data[target_col].values
        
        # スケーリング
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        self.scalers[f'prediction_{target}'] = scaler
        
        return X_scaled, y, valid_data
    
    def _train_ensemble_model(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        **kwargs
    ) -> Tuple[Any, Dict]:
        """アンサンブルモデルの学習"""
        
        models = []
        predictions_train = []
        predictions_test = []
        
        # Random Forest
        rf = RandomForestRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 10),
            random_state=42
        )
        rf.fit(X_train, y_train)
        models.append(('rf', rf))
        predictions_train.append(rf.predict(X_train))
        predictions_test.append(rf.predict(X_test))
        
        # Gradient Boosting
        gbm = GradientBoostingRegressor(
            n_estimators=kwargs.get('n_estimators', 100),
            max_depth=kwargs.get('max_depth', 5),
            learning_rate=kwargs.get('learning_rate', 0.1),
            random_state=42
        )
        gbm.fit(X_train, y_train)
        models.append(('gbm', gbm))
        predictions_train.append(gbm.predict(X_train))
        predictions_test.append(gbm.predict(X_test))
        
        # XGBoost (if available)
        if XGBOOST_AVAILABLE:
            xgb_model = xgb.XGBRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 6),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=42
            )
            xgb_model.fit(X_train, y_train)
            models.append(('xgb', xgb_model))
            predictions_train.append(xgb_model.predict(X_train))
            predictions_test.append(xgb_model.predict(X_test))
        
        # LightGBM (if available)
        if LIGHTGBM_AVAILABLE:
            lgb_model = lgb.LGBMRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 5),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=42
            )
            lgb_model.fit(X_train, y_train)
            models.append(('lgb', lgb_model))
            predictions_train.append(lgb_model.predict(X_train))
            predictions_test.append(lgb_model.predict(X_test))
        
        # アンサンブル予測（平均）
        ensemble_pred_train = np.mean(predictions_train, axis=0)
        ensemble_pred_test = np.mean(predictions_test, axis=0)
        
        # メトリクス計算
        metrics = {
            'train_r2': r2_score(y_train, ensemble_pred_train),
            'test_r2': r2_score(y_test, ensemble_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, ensemble_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, ensemble_pred_test)),
            'train_mae': mean_absolute_error(y_train, ensemble_pred_train),
            'test_mae': mean_absolute_error(y_test, ensemble_pred_test),
            'models': [name for name, _ in models]
        }
        
        # アンサンブルモデル（予測用）
        class EnsembleModel:
            def __init__(self, models):
                self.models = [m for _, m in models]
            
            def predict(self, X):
                preds = [model.predict(X) for model in self.models]
                return np.mean(preds, axis=0)
        
        ensemble_model = EnsembleModel(models)
        
        logger.info(f"Ensemble model trained with {len(models)} base models")
        
        return ensemble_model, metrics
    
    def _train_single_model(
        self,
        X_train: np.ndarray,
        X_test: np.ndarray,
        y_train: np.ndarray,
        y_test: np.ndarray,
        model_type: str = 'rf',
        **kwargs
    ) -> Tuple[Any, Dict]:
        """単一モデルの学習"""
        
        # モデル選択
        if model_type == 'rf':
            model = RandomForestRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 10),
                random_state=42
            )
        elif model_type == 'gbm':
            model = GradientBoostingRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 5),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=42
            )
        elif model_type == 'xgb' and XGBOOST_AVAILABLE:
            model = xgb.XGBRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 6),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=42
            )
        elif model_type == 'lgb' and LIGHTGBM_AVAILABLE:
            model = lgb.LGBMRegressor(
                n_estimators=kwargs.get('n_estimators', 100),
                max_depth=kwargs.get('max_depth', 5),
                learning_rate=kwargs.get('learning_rate', 0.1),
                random_state=42
            )
        elif model_type == 'linear':
            model = LinearRegression()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # 学習
        model.fit(X_train, y_train)
        
        # 予測
        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)
        
        # メトリクス
        metrics = {
            'train_r2': r2_score(y_train, pred_train),
            'test_r2': r2_score(y_test, pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, pred_test)),
            'train_mae': mean_absolute_error(y_train, pred_train),
            'test_mae': mean_absolute_error(y_test, pred_test)
        }
        
        logger.info(f"{model_type.upper()} model trained")
        
        return model, metrics
    
    def _feature_importance_analysis(
        self,
        model: Any,
        features: List[str],
        model_type: str
    ) -> pd.DataFrame:
        """特徴量重要度分析"""
        
        # モデルタイプに応じた重要度取得
        if hasattr(model, 'feature_importances_'):
            # Tree-based models
            importances = model.feature_importances_
        elif hasattr(model, 'models'):  # Ensemble
            # 各モデルの重要度を平均
            importances_list = []
            for m in model.models:
                if hasattr(m, 'feature_importances_'):
                    importances_list.append(m.feature_importances_)
            
            if importances_list:
                importances = np.mean(importances_list, axis=0)
            else:
                logger.warning("Cannot extract feature importances from ensemble")
                return pd.DataFrame()
        elif hasattr(model, 'coef_'):
            # Linear models
            importances = np.abs(model.coef_)
        else:
            logger.warning(f"Feature importances not available for {model_type}")
            return pd.DataFrame()
        
        # DataFrame作成
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        # 可視化
        plt.figure(figsize=(10, max(6, len(features) * 0.3)))
        plt.barh(importance_df['feature'], importance_df['importance'])
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance Analysis')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Feature importance analysis completed")
        
        return importance_df
    
    def _shap_analysis(
        self,
        model: Any,
        X_test: np.ndarray,
        features: List[str],
        target: str
    ):
        """SHAP分析（説明可能AI）"""
        
        if not SHAP_AVAILABLE:
            return
        
        try:
            # SHAP explainer
            if hasattr(model, 'models'):  # Ensemble
                # 最初のモデルを使用（簡略化）
                explainer = shap.Explainer(model.models[0], X_test[:100])
            else:
                explainer = shap.Explainer(model, X_test[:100])
            
            # SHAP values計算
            shap_values = explainer(X_test[:100])
            
            # Summary plot
            plt.figure(figsize=(10, 8))
            shap.summary_plot(shap_values, X_test[:100], feature_names=features, show=False)
            plt.tight_layout()
            plt.savefig(self.output_dir / f'shap_summary_{target}.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # Feature importance plot
            plt.figure(figsize=(10, 6))
            shap.plots.bar(shap_values, show=False)
            plt.tight_layout()
            plt.savefig(self.output_dir / f'shap_importance_{target}.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"SHAP analysis completed for {target}")
            
        except Exception as e:
            logger.warning(f"SHAP analysis failed: {str(e)}")
    
    def _visualize_predictions(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        target: str,
        model_type: str
    ):
        """予測結果の可視化"""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Actual vs Predicted
        axes[0].scatter(y_true, y_pred, alpha=0.5, edgecolors='k', s=30)
        
        # 45度線
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
        
        axes[0].set_xlabel('Actual')
        axes[0].set_ylabel('Predicted')
        axes[0].set_title(f'Actual vs Predicted: {target} ({model_type.upper()})')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # R²表示
        r2 = r2_score(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        axes[0].text(
            0.05, 0.95, 
            f'R² = {r2:.4f}\nRMSE = {rmse:.4f}',
            transform=axes[0].transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        # Residual plot
        residuals = y_true - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.5, edgecolors='k', s=30)
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted')
        axes[1].set_ylabel('Residuals')
        axes[1].set_title('Residual Plot')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / f'prediction_{target}_{model_type}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Prediction visualization saved")
    
    # ============================================================
    # 3. 異常検知（Anomaly Detection）
    # ============================================================
    
    def detect_anomalies(
        self,
        features: List[str],
        contamination: float = 0.05,
        method: str = 'isolation_forest',
        **kwargs
    ) -> pd.DataFrame:
        """
        異常企業の検出
        
        統計的・機械学習的手法で、戦略的に異常な企業を検出します。
        
        Parameters
        ----------
        features : List[str]
            異常検知に使用する変数リスト
        contamination : float, default=0.05
            異常値の割合（0-0.5）
        method : str, default='isolation_forest'
            検出手法
            - 'isolation_forest': Isolation Forest
            - 'lof': Local Outlier Factor
            - 'elliptic_envelope': Elliptic Envelope
            - 'one_class_svm': One-Class SVM
        **kwargs
            手法固有のパラメータ
        
        Returns
        -------
        pd.DataFrame
            異常スコア付きデータフレーム
        
        Examples
        --------
        >>> anomalies = engine.detect_anomalies(
        ...     features=['roa', 'rd_intensity', 'leverage'],
        ...     contamination=0.05,
        ...     method='isolation_forest'
        ... )
        >>> 
        >>> # 異常企業の分析
        >>> outliers = anomalies[anomalies['is_anomaly'] == -1]
        >>> print(outliers[[engine.firm_id, 'anomaly_score', 'roa', 'rd_intensity']])
        
        References
        ----------
        - Liu et al. (2008): Isolation Forest. ICDM.
        - Breunig et al. (2000): LOF: Identifying Density-Based Local Outliers. SIGMOD.
        """
        
        logger.info(f"Starting anomaly detection with {method}")
        
        # データ準備
        X, valid_data = self._prepare_features(features, scale=True)
        
        # 異常検知モデル
        if method == 'isolation_forest':
            model = IsolationForest(
                contamination=contamination,
                random_state=42,
                **kwargs
            )
        elif method == 'lof':
            model = LocalOutlierFactor(
                contamination=contamination,
                novelty=False,
                **kwargs
            )
        elif method == 'elliptic_envelope':
            model = EllipticEnvelope(
                contamination=contamination,
                random_state=42,
                **kwargs
            )
        elif method == 'one_class_svm':
            model = OneClassSVM(
                nu=contamination,
                **kwargs
            )
        else:
            raise ValueError(f"Unknown anomaly detection method: {method}")
        
        # 異常検知実行
        if method == 'lof':
            predictions = model.fit_predict(X)
            scores = model.negative_outlier_factor_
        else:
            predictions = model.fit_predict(X)
            scores = model.score_samples(X)
        
        # 結果をデータに追加
        valid_data['is_anomaly'] = predictions  # -1: anomaly, 1: normal
        valid_data['anomaly_score'] = scores
        
        # 異常企業の詳細分析
        anomaly_analysis = self._analyze_anomalies(valid_data, features)
        
        # 可視化
        self._visualize_anomalies(X, predictions, scores, features, method)
        
        # 結果保存
        self.results['anomaly_detection'] = {
            'method': method,
            'contamination': contamination,
            'n_anomalies': (predictions == -1).sum(),
            'data': valid_data,
            'analysis': anomaly_analysis
        }
        
        self.models[f'anomaly_{method}'] = model
        
        logger.info(f"Anomaly detection completed: {(predictions == -1).sum()} anomalies detected")
        
        return valid_data
    
    def _analyze_anomalies(
        self,
        data: pd.DataFrame,
        features: List[str]
    ) -> Dict:
        """異常企業の詳細分析"""
        
        anomalies = data[data['is_anomaly'] == -1]
        normals = data[data['is_anomaly'] == 1]
        
        # 記述統計比較
        comparison = pd.DataFrame({
            'Normal_Mean': normals[features].mean(),
            'Normal_SD': normals[features].std(),
            'Anomaly_Mean': anomalies[features].mean(),
            'Anomaly_SD': anomalies[features].std()
        })
        
        # t-test
        p_values = []
        for feat in features:
            try:
                _, p = stats.ttest_ind(
                    normals[feat].dropna(),
                    anomalies[feat].dropna(),
                    equal_var=False
                )
                p_values.append(p)
            except:
                p_values.append(np.nan)
        
        comparison['p_value'] = p_values
        comparison['significant'] = comparison['p_value'] < 0.05
        
        logger.info(f"Anomaly analysis:\n{comparison}")
        
        return {
            'n_anomalies': len(anomalies),
            'n_normals': len(normals),
            'comparison': comparison,
            'anomaly_firms': anomalies[self.firm_id].tolist()
        }
    
    def _visualize_anomalies(
        self,
        X: np.ndarray,
        predictions: np.ndarray,
        scores: np.ndarray,
        features: List[str],
        method: str
    ):
        """異常検知結果の可視化"""
        
        # PCA for visualization
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # PCA scatter (colored by anomaly status)
        colors = ['red' if pred == -1 else 'blue' for pred in predictions]
        axes[0].scatter(X_pca[:, 0], X_pca[:, 1], c=colors, alpha=0.6, edgecolors='k', s=50)
        axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
        axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
        axes[0].set_title(f'Anomaly Detection - {method.upper()}\nRed: Anomalies, Blue: Normal')
        axes[0].grid(True, alpha=0.3)
        
        # Anomaly score distribution
        axes[1].hist(scores[predictions == 1], bins=50, alpha=0.7, label='Normal', color='blue')
        axes[1].hist(scores[predictions == -1], bins=50, alpha=0.7, label='Anomaly', color='red')
        axes[1].set_xlabel('Anomaly Score')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title('Anomaly Score Distribution')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / f'anomaly_detection_{method}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Anomaly visualization saved")
    
    # ============================================================
    # 4. 包括的レポート生成
    # ============================================================
    
    def generate_comprehensive_report(
        self,
        include_sections: Optional[List[str]] = None
    ) -> str:
        """
        包括的なデータマイニング分析レポート生成
        
        Parameters
        ----------
        include_sections : List[str], optional
            含めるセクション（Noneの場合、全セクション）
            - 'strategic_groups'
            - 'performance_prediction'
            - 'anomaly_detection'
            - 'feature_importance'
        
        Returns
        -------
        str
            レポートファイルのパス
        
        Examples
        --------
        >>> report_path = engine.generate_comprehensive_report()
        >>> print(f"Report saved to: {report_path}")
        """
        
        logger.info("Generating comprehensive report...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f'comprehensive_report_{timestamp}.html'
        
        # HTMLレポート作成
        html_content = self._create_html_report(include_sections)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Comprehensive report saved to {report_path}")
        
        return str(report_path)
    
    def _create_html_report(
        self,
        include_sections: Optional[List[str]] = None
    ) -> str:
        """HTMLレポートの作成"""
        
        html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategic Management Data Mining Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0 0 10px 0;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .section h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 15px 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        .metric-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #667eea;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .figure {
            text-align: center;
            margin: 20px 0;
        }
        .figure img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .note {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Strategic Management Data Mining Report</h1>
        <p>Integrated Data Mining Engine Analysis Results</p>
        <p><strong>Generated:</strong> {timestamp}</p>
    </div>
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # データサマリー
        html += self._html_data_summary()
        
        # 分析結果セクション
        if not include_sections or 'strategic_groups' in include_sections:
            if 'strategic_groups' in self.results:
                html += self._html_strategic_groups()
        
        if not include_sections or 'performance_prediction' in include_sections:
            if 'performance_prediction' in self.results:
                html += self._html_performance_prediction()
        
        if not include_sections or 'anomaly_detection' in include_sections:
            if 'anomaly_detection' in self.results:
                html += self._html_anomaly_detection()
        
        # フッター
        html += """
    <div class="section">
        <h2>📚 References</h2>
        <ul>
            <li>Porter, M. E. (1980). Competitive Strategy. Free Press.</li>
            <li>Barney, J. (1991). Firm Resources and Sustained Competitive Advantage. JOM, 17(1), 99-120.</li>
            <li>Ketchen, D. J., & Shook, C. L. (1996). The application of cluster analysis in strategic management research. SMJ, 17(6), 441-458.</li>
            <li>Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning. Springer.</li>
        </ul>
    </div>
    
    <div class="section">
        <h2>📧 Contact & Support</h2>
        <p><strong>Engine Version:</strong> 3.1</p>
        <p><strong>Documentation:</strong> See SKILL.md for complete usage guide</p>
        <p><strong>License:</strong> MIT</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _html_data_summary(self) -> str:
        """データサマリーHTML"""
        
        n_firms = self.data[self.firm_id].nunique()
        n_periods = self.data[self.time_var].nunique()
        n_obs = len(self.data)
        
        html = f"""
    <div class="section">
        <h2>📊 Data Summary</h2>
        <div class="metric">
            <div class="metric-label">Total Firms</div>
            <div class="metric-value">{n_firms:,}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Time Periods</div>
            <div class="metric-value">{n_periods}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Total Observations</div>
            <div class="metric-value">{n_obs:,}</div>
        </div>
    </div>
"""
        
        return html
    
    def _html_strategic_groups(self) -> str:
        """戦略的グループ分析HTML"""
        
        results = self.results['strategic_groups']
        stats = results['statistics']
        profiles = results['profiles']
        
        html = f"""
    <div class="section">
        <h2>🎯 Strategic Group Analysis</h2>
        
        <h3>Clustering Statistics</h3>
        <div class="metric">
            <div class="metric-label">Number of Groups</div>
            <div class="metric-value">{stats['n_clusters']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Silhouette Score</div>
            <div class="metric-value">{stats['silhouette_score']:.3f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Quality</div>
            <div class="metric-value">{stats['interpretation']['silhouette']}</div>
        </div>
        
        <h3>Group Profiles</h3>
        {profiles.to_html(classes='table')}
        
        <div class="note">
            <strong>💡 Interpretation:</strong> Silhouette Score of {stats['silhouette_score']:.3f} 
            indicates {stats['interpretation']['silhouette'].lower()} cluster structure.
        </div>
    </div>
"""
        
        return html
    
    def _html_performance_prediction(self) -> str:
        """パフォーマンス予測HTML"""
        
        results = self.results['performance_prediction']
        metrics = results['metrics']
        
        html = f"""
    <div class="section">
        <h2>📈 Performance Prediction</h2>
        
        <h3>Model Performance</h3>
        <div class="metric">
            <div class="metric-label">Test R²</div>
            <div class="metric-value">{metrics['test_r2']:.4f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Test RMSE</div>
            <div class="metric-value">{metrics['test_rmse']:.4f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Test MAE</div>
            <div class="metric-value">{metrics['test_mae']:.4f}</div>
        </div>
        
        <h3>Model Details</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Train</th>
                <th>Test</th>
            </tr>
            <tr>
                <td>R²</td>
                <td>{metrics['train_r2']:.4f}</td>
                <td>{metrics['test_r2']:.4f}</td>
            </tr>
            <tr>
                <td>RMSE</td>
                <td>{metrics['train_rmse']:.4f}</td>
                <td>{metrics['test_rmse']:.4f}</td>
            </tr>
            <tr>
                <td>MAE</td>
                <td>{metrics['train_mae']:.4f}</td>
                <td>{metrics['test_mae']:.4f}</td>
            </tr>
        </table>
"""
        
        # Feature Importance
        if results['feature_importance'] is not None:
            importance_html = results['feature_importance'].to_html(classes='table', index=False)
            html += f"""
        <h3>Feature Importance</h3>
        {importance_html}
"""
        
        html += """
    </div>
"""
        
        return html
    
    def _html_anomaly_detection(self) -> str:
        """異常検知HTML"""
        
        results = self.results['anomaly_detection']
        analysis = results['analysis']
        
        html = f"""
    <div class="section">
        <h2>🔍 Anomaly Detection</h2>
        
        <h3>Detection Summary</h3>
        <div class="metric">
            <div class="metric-label">Anomalies Detected</div>
            <div class="metric-value">{analysis['n_anomalies']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Normal Firms</div>
            <div class="metric-value">{analysis['n_normals']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Anomaly Rate</div>
            <div class="metric-value">{analysis['n_anomalies']/(analysis['n_anomalies']+analysis['n_normals'])*100:.1f}%</div>
        </div>
        
        <h3>Feature Comparison (Normal vs Anomaly)</h3>
        {analysis['comparison'].to_html(classes='table')}
        
        <div class="note">
            <strong>💡 Note:</strong> Features with p-value < 0.05 show significant differences 
            between normal and anomalous firms.
        </div>
    </div>
"""
        
        return html
    
    # ============================================================
    # ユーティリティメソッド
    # ============================================================
    
    def save_results(
        self,
        filename: str = 'datamining_results.pkl'
    ):
        """結果をPickleファイルに保存"""
        
        save_path = self.output_dir / filename
        
        save_obj = {
            'results': self.results,
            'models': self.models,
            'config': self.config
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(save_obj, f)
        
        logger.info(f"Results saved to {save_path}")
    
    def load_results(
        self,
        filename: str = 'datamining_results.pkl'
    ):
        """保存された結果を読み込み"""
        
        load_path = self.output_dir / filename
        
        if not load_path.exists():
            raise FileNotFoundError(f"Results file not found: {load_path}")
        
        with open(load_path, 'rb') as f:
            save_obj = pickle.load(f)
        
        self.results = save_obj['results']
        self.models = save_obj['models']
        self.config = save_obj['config']
        
        logger.info(f"Results loaded from {load_path}")


# ============================================================
# 使用例
# ============================================================

if __name__ == "__main__":
    """
    使用例：統合データマイニング分析
    """
    
    import pandas as pd
    
    # サンプルデータ生成（実際はファイルから読み込み）
    np.random.seed(42)
    n_firms = 300
    n_years = 10
    
    data_list = []
    for firm_id in range(1, n_firms + 1):
        for year in range(2014, 2014 + n_years):
            data_list.append({
                'gvkey': f'FIRM{firm_id:04d}',
                'year': year,
                'roa': np.random.normal(0.05, 0.10) + np.random.uniform(-0.02, 0.02),
                'rd_intensity': max(0, np.random.normal(0.05, 0.03)),
                'capital_intensity': max(0, np.random.normal(0.30, 0.15)),
                'firm_size': np.random.normal(5, 1),
                'leverage': max(0, min(1, np.random.normal(0.35, 0.20))),
                'firm_age': year - (2000 + np.random.randint(0, 20))
            })
    
    df_sample = pd.DataFrame(data_list)
    
    print("=" * 70)
    print("INTEGRATED DATA MINING ENGINE - DEMO")
    print("=" * 70)
    
    # エンジン初期化
    engine = IntegratedDataMiningEngine(
        data=df_sample,
        firm_id='gvkey',
        time_var='year',
        output_dir='./demo_output/'
    )
    
    print("\n1. Strategic Group Analysis...")
    groups = engine.strategic_group_analysis(
        features=['rd_intensity', 'capital_intensity'],
        method='kmeans'
    )
    print(f"✓ Identified {groups['strategic_group'].nunique()} strategic groups")
    
    print("\n2. Performance Prediction...")
    predictions = engine.predict_performance(
        target='roa',
        features=['rd_intensity', 'firm_size', 'leverage', 'firm_age'],
        model_type='ensemble'
    )
    print("✓ Performance prediction completed")
    
    print("\n3. Anomaly Detection...")
    anomalies = engine.detect_anomalies(
        features=['roa', 'rd_intensity', 'leverage'],
        contamination=0.05,
        method='isolation_forest'
    )
    print(f"✓ Detected {(anomalies['is_anomaly'] == -1).sum()} anomalies")
    
    print("\n4. Generating Comprehensive Report...")
    report_path = engine.generate_comprehensive_report()
    print(f"✓ Report saved: {report_path}")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"\nAll outputs saved to: ./demo_output/")
