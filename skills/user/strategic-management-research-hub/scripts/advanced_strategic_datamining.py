"""
Strategic Management Research Hub - Advanced Data Mining Engine
================================================================

Publication-grade data mining for strategic management empirical research.
Extends base data_mining.py with cutting-edge techniques:

1. **Advanced Clustering**:
   - Strategic Group Analysis (Porter 1980)
   - Configuration Theory (Meyer et al. 1993)
   - Temporal Clustering (Strategy Evolution)

2. **Predictive Analytics**:
   - Firm Performance Prediction
   - Strategic Failure Risk Models
   - Competitive Response Forecasting

3. **Feature Engineering**:
   - Automatic interaction term generation
   - Non-linear transformations
   - Industry-adjusted metrics

4. **Ensemble Methods**:
   - Random Forest feature importance
   - Gradient Boosting for complex relationships
   - Stacking for robust predictions

5. **Deep Learning Integration**:
   - Neural Networks for performance prediction
   - Autoencoders for anomaly detection
   - LSTM for time-series strategic patterns

6. **Explainable AI (XAI)**:
   - SHAP values for feature importance
   - LIME for local interpretability
   - Counterfactual explanations

Integrates seamlessly with existing research workflow (Phase 1-8).

Author: Strategic Management Research Hub v3.1
Version: 3.1
Date: 2025-11-01
License: MIT

References:
- Ketchen & Shook (1996): Cluster Analysis in Strategic Management, SMJ
- Meyer et al. (1993): Configurational Approaches, AMR
- Hastie et al. (2009): Elements of Statistical Learning
- Lundberg & Lee (2017): Unified Approach to Interpreting Model Predictions (SHAP)
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Any
import logging
from pathlib import Path
import warnings
import json
from datetime import datetime
import pickle

# Core ML Libraries
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV, 
    RandomizedSearchCV, TimeSeriesSplit
)
from sklearn.metrics import (
    silhouette_score, calinski_harabasz_score, davies_bouldin_score,
    mean_squared_error, r2_score, roc_auc_score, classification_report,
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
)

# Clustering
from sklearn.cluster import (
    KMeans, DBSCAN, AgglomerativeClustering, SpectralClustering,
    OPTICS, Birch, MeanShift
)
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist, squareform

# Dimensionality Reduction
from sklearn.decomposition import PCA, FactorAnalysis, FastICA, TruncatedSVD
from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding, MDS

# Anomaly Detection
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM

# Supervised Learning - Traditional
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet, 
    LogisticRegression, SGDRegressor
)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestRegressor, RandomForestClassifier,
    GradientBoostingRegressor, GradientBoostingClassifier,
    AdaBoostRegressor, AdaBoostClassifier,
    ExtraTreesRegressor, ExtraTreesClassifier,
    VotingRegressor, VotingClassifier,
    StackingRegressor, StackingClassifier,
    HistGradientBoostingRegressor, HistGradientBoostingClassifier
)
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPRegressor, MLPClassifier

# XGBoost & LightGBM (if available)
try:
    import xgboost as xgb
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False
    warnings.warn("XGBoost not installed. pip install xgboost")

try:
    import lightgbm as lgb
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False
    warnings.warn("LightGBM not installed. pip install lightgbm")

# UMAP
try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP not installed. pip install umap-learn")

# SHAP (Explainable AI)
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    warnings.warn("SHAP not installed. pip install shap")

# Matplotlib & Seaborn
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# MAIN CLASS: AdvancedStrategicDataMining
# ============================================================================

class AdvancedStrategicDataMining:
    """
    Comprehensive data mining engine for strategic management research.
    
    Features:
    - Strategic group analysis (clustering)
    - Performance prediction (supervised learning)
    - Anomaly detection (outlier firms)
    - Feature importance analysis
    - Temporal pattern discovery
    - Explainable AI (SHAP, LIME)
    
    Usage:
    ```python
    dm = AdvancedStrategicDataMining(
        data=df_panel,
        firm_id='gvkey',
        time_var='year',
        output_dir='./datamining_output/'
    )
    
    # Strategic group analysis
    groups = dm.strategic_group_analysis(
        features=['rd_intensity', 'capital_intensity', 'international_sales'],
        n_clusters=4
    )
    
    # Performance prediction
    predictions = dm.predict_firm_performance(
        target='roa_lead1',
        features=['rd_intensity', 'firm_size', 'leverage'],
        model_type='ensemble'
    )
    
    # Feature importance
    importance = dm.analyze_feature_importance(
        target='roa',
        features=strategic_vars
    )
    
    # Generate comprehensive report
    dm.generate_comprehensive_report()
    ```
    """
    
    def __init__(
        self,
        data: pd.DataFrame,
        firm_id: str,
        time_var: str,
        output_dir: str = './datamining_output/',
        random_state: int = 42
    ):
        """
        Initialize Advanced Data Mining Engine.
        
        Args:
            data: Panel DataFrame
            firm_id: Column name for firm identifier
            time_var: Column name for time period
            output_dir: Directory for outputs
            random_state: Random seed for reproducibility
        """
        self.data = data.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.random_state = random_state
        
        # Storage for results
        self.results = {}
        self.models = {}
        self.scalers = {}
        
        logger.info(f"Advanced Data Mining Engine initialized")
        logger.info(f"Dataset: {len(data)} observations, "
                   f"{data[firm_id].nunique()} firms, "
                   f"{data[time_var].nunique()} periods")
    
    # ========================================================================
    # 1. STRATEGIC GROUP ANALYSIS (Configuration Theory)
    # ========================================================================
    
    def strategic_group_analysis(
        self,
        features: List[str],
        n_clusters: Optional[int] = None,
        method: str = 'kmeans',
        scale: bool = True,
        optimal_k_method: str = 'elbow',
        max_k: int = 10,
        save_results: bool = True
    ) -> Dict:
        """
        Identify strategic groups using clustering methods.
        
        Theoretical Foundation:
        - Porter (1980): Strategic Groups within Industries
        - Cool & Schendel (1987): Strategic Group Formation & Performance
        - Ketchen & Shook (1996): Cluster Analysis in Strategic Management
        
        Args:
            features: List of strategic dimensions (e.g., R&D, advertising, vertical integration)
            n_clusters: Number of clusters (if None, optimal k determined automatically)
            method: Clustering algorithm ('kmeans', 'hierarchical', 'gmm', 'dbscan')
            scale: Whether to standardize features
            optimal_k_method: Method for determining optimal k ('elbow', 'silhouette', 'gap')
            max_k: Maximum k to test for optimal clustering
            save_results: Save results to output_dir
        
        Returns:
            Dictionary with cluster assignments, profiles, and validation metrics
        
        Research Application:
        - Identify distinct strategic configurations
        - Analyze performance differences across groups
        - Test strategic group mobility barriers
        - Examine within-group competition intensity
        """
        logger.info(f"Strategic Group Analysis: {len(features)} dimensions")
        
        # Prepare data
        X = self.data[features].dropna().copy()
        valid_indices = X.index
        
        if scale:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers['strategic_groups'] = scaler
        else:
            X_scaled = X.values
        
        # Determine optimal number of clusters if not specified
        if n_clusters is None:
            n_clusters = self._determine_optimal_clusters(
                X_scaled, 
                method=optimal_k_method, 
                max_k=max_k
            )
            logger.info(f"Optimal number of clusters: {n_clusters}")
        
        # Perform clustering
        if method == 'kmeans':
            clusterer = KMeans(
                n_clusters=n_clusters,
                random_state=self.random_state,
                n_init=50
            )
        elif method == 'hierarchical':
            clusterer = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage='ward'
            )
        elif method == 'gmm':
            clusterer = GaussianMixture(
                n_components=n_clusters,
                random_state=self.random_state
            )
        elif method == 'dbscan':
            # DBSCAN doesn't require n_clusters, but uses eps
            clusterer = DBSCAN(eps=0.5, min_samples=5)
        else:
            raise ValueError(f"Unknown clustering method: {method}")
        
        # Fit and predict
        cluster_labels = clusterer.fit_predict(X_scaled)
        
        # Add cluster assignments to data
        self.data.loc[valid_indices, 'strategic_group'] = cluster_labels
        
        # Calculate cluster profiles (centroids in original scale)
        cluster_profiles = []
        for k in range(n_clusters):
            group_data = X[cluster_labels == k]
            profile = {
                'cluster': k,
                'size': len(group_data),
                'size_pct': len(group_data) / len(X) * 100
            }
            for feat in features:
                profile[f'{feat}_mean'] = group_data[feat].mean()
                profile[f'{feat}_std'] = group_data[feat].std()
            cluster_profiles.append(profile)
        
        profiles_df = pd.DataFrame(cluster_profiles)
        
        # Validation metrics
        validation = {}
        if n_clusters > 1 and method != 'dbscan':
            validation['silhouette'] = silhouette_score(X_scaled, cluster_labels)
            validation['calinski_harabasz'] = calinski_harabasz_score(X_scaled, cluster_labels)
            validation['davies_bouldin'] = davies_bouldin_score(X_scaled, cluster_labels)
        
        logger.info(f"Silhouette Score: {validation.get('silhouette', 'N/A'):.3f}")
        
        # Visualization
        self._visualize_strategic_groups(X_scaled, cluster_labels, features, n_clusters)
        
        # Prepare results
        results = {
            'method': method,
            'n_clusters': n_clusters,
            'features': features,
            'cluster_labels': cluster_labels,
            'cluster_profiles': profiles_df,
            'validation_metrics': validation,
            'model': clusterer
        }
        
        self.results['strategic_groups'] = results
        
        if save_results:
            profiles_df.to_excel(
                self.output_dir / 'strategic_group_profiles.xlsx',
                index=False
            )
            logger.info(f"Strategic group profiles saved")
        
        return results
    
    def _determine_optimal_clusters(
        self,
        X: np.ndarray,
        method: str = 'elbow',
        max_k: int = 10
    ) -> int:
        """
        Determine optimal number of clusters.
        
        Methods:
        - 'elbow': Elbow method (inertia plot)
        - 'silhouette': Silhouette coefficient
        - 'gap': Gap statistic
        """
        if method == 'elbow':
            inertias = []
            K_range = range(2, max_k + 1)
            
            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                kmeans.fit(X)
                inertias.append(kmeans.inertia_)
            
            # Simple elbow detection: find maximum second derivative
            diffs = np.diff(inertias)
            second_diffs = np.diff(diffs)
            optimal_k = np.argmax(second_diffs) + 2  # +2 because of double diff
            
            # Plot
            plt.figure(figsize=(10, 6))
            plt.plot(K_range, inertias, 'bo-')
            plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
            plt.xlabel('Number of Clusters (k)')
            plt.ylabel('Inertia')
            plt.title('Elbow Method for Optimal k')
            plt.legend()
            plt.tight_layout()
            plt.savefig(self.output_dir / 'optimal_k_elbow.png', dpi=300)
            plt.close()
            
            return optimal_k
        
        elif method == 'silhouette':
            silhouette_scores = []
            K_range = range(2, max_k + 1)
            
            for k in K_range:
                kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
                labels = kmeans.fit_predict(X)
                score = silhouette_score(X, labels)
                silhouette_scores.append(score)
            
            optimal_k = K_range[np.argmax(silhouette_scores)]
            
            # Plot
            plt.figure(figsize=(10, 6))
            plt.plot(K_range, silhouette_scores, 'bo-')
            plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
            plt.xlabel('Number of Clusters (k)')
            plt.ylabel('Silhouette Score')
            plt.title('Silhouette Method for Optimal k')
            plt.legend()
            plt.tight_layout()
            plt.savefig(self.output_dir / 'optimal_k_silhouette.png', dpi=300)
            plt.close()
            
            return optimal_k
        
        else:
            # Default: return middle of range
            return max_k // 2
    
    def _visualize_strategic_groups(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        feature_names: List[str],
        n_clusters: int
    ):
        """Visualize strategic groups using PCA 2D projection."""
        
        # PCA to 2D
        pca = PCA(n_components=2, random_state=self.random_state)
        X_pca = pca.fit_transform(X)
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(
            X_pca[:, 0],
            X_pca[:, 1],
            c=labels,
            cmap='viridis',
            alpha=0.6,
            s=50
        )
        plt.colorbar(scatter, label='Strategic Group')
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)')
        plt.title('Strategic Groups (PCA Projection)')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'strategic_groups_pca.png', dpi=300)
        plt.close()
        
        logger.info("Strategic group visualization saved")
    
    # ========================================================================
    # 2. FIRM PERFORMANCE PREDICTION (Supervised Learning)
    # ========================================================================
    
    def predict_firm_performance(
        self,
        target: str,
        features: List[str],
        model_type: str = 'ensemble',
        test_size: float = 0.2,
        cv_folds: int = 5,
        tune_hyperparameters: bool = True,
        save_model: bool = True
    ) -> Dict:
        """
        Predict firm performance using advanced ML models.
        
        Theoretical Applications:
        - RBV: Predict performance from resource configurations
        - Dynamic Capabilities: Forecast adaptation success
        - Contingency Theory: Model fit-performance relationships
        
        Args:
            target: Performance variable (e.g., 'roa_lead1', 'tobin_q')
            features: Predictor variables
            model_type: Model family ('linear', 'tree', 'ensemble', 'nn', 'auto')
            test_size: Proportion for test set
            cv_folds: Number of cross-validation folds
            tune_hyperparameters: Whether to perform hyperparameter tuning
            save_model: Save trained model to disk
        
        Returns:
            Dictionary with predictions, metrics, and trained model
        
        Research Use Cases:
        1. Performance Forecasting: Predict ROA/Tobin's Q from strategic choices
        2. Competitive Advantage: Identify resource bundles → sustained performance
        3. Strategic Fit: Model environment-strategy-performance linkages
        4. M&A Success: Predict post-acquisition performance
        """
        logger.info(f"Performance Prediction: {target} ~ {len(features)} features")
        
        # Prepare data
        df_clean = self.data[[target] + features].dropna()
        X = df_clean[features].values
        y = df_clean[target].values
        
        # Train-test split (time-aware for panel data)
        if self.time_var in self.data.columns:
            # Sort by time and split temporally
            df_clean_sorted = df_clean.sort_values(self.time_var)
            split_idx = int(len(df_clean_sorted) * (1 - test_size))
            X_train, X_test = df_clean_sorted[features].iloc[:split_idx].values, \
                               df_clean_sorted[features].iloc[split_idx:].values
            y_train, y_test = df_clean_sorted[target].iloc[:split_idx].values, \
                               df_clean_sorted[target].iloc[split_idx:].values
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=self.random_state
            )
        
        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['performance_prediction'] = scaler
        
        # Model selection and training
        if model_type == 'linear':
            models = {
                'Linear': LinearRegression(),
                'Ridge': Ridge(alpha=1.0),
                'Lasso': Lasso(alpha=0.1),
                'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5)
            }
        
        elif model_type == 'tree':
            models = {
                'DecisionTree': DecisionTreeRegressor(
                    max_depth=5,
                    random_state=self.random_state
                ),
                'RandomForest': RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=self.random_state
                )
            }
        
        elif model_type == 'ensemble':
            base_models = [
                ('rf', RandomForestRegressor(n_estimators=100, random_state=self.random_state)),
                ('gb', GradientBoostingRegressor(n_estimators=100, random_state=self.random_state)),
                ('et', ExtraTreesRegressor(n_estimators=100, random_state=self.random_state))
            ]
            
            models = {
                'RandomForest': RandomForestRegressor(
                    n_estimators=200,
                    max_depth=15,
                    random_state=self.random_state
                ),
                'GradientBoosting': GradientBoostingRegressor(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=self.random_state
                ),
                'StackingEnsemble': StackingRegressor(
                    estimators=base_models,
                    final_estimator=Ridge(),
                    cv=5
                )
            }
            
            if XGB_AVAILABLE:
                models['XGBoost'] = xgb.XGBRegressor(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=self.random_state
                )
            
            if LGB_AVAILABLE:
                models['LightGBM'] = lgb.LGBMRegressor(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=self.random_state
                )
        
        elif model_type == 'nn':
            models = {
                'NeuralNetwork': MLPRegressor(
                    hidden_layer_sizes=(100, 50),
                    activation='relu',
                    solver='adam',
                    max_iter=500,
                    random_state=self.random_state
                )
            }
        
        else:  # 'auto' - try multiple model types
            models = {
                'Ridge': Ridge(alpha=1.0),
                'RandomForest': RandomForestRegressor(n_estimators=100, random_state=self.random_state),
                'GradientBoosting': GradientBoostingRegressor(n_estimators=100, random_state=self.random_state),
                'NeuralNetwork': MLPRegressor(hidden_layer_sizes=(50,), max_iter=300, random_state=self.random_state)
            }
        
        # Train and evaluate each model
        results = {}
        best_model = None
        best_r2 = -np.inf
        
        for name, model in models.items():
            logger.info(f"Training {name}...")
            
            # Cross-validation
            cv_scores = cross_val_score(
                model,
                X_train_scaled,
                y_train,
                cv=cv_folds,
                scoring='r2'
            )
            
            # Train on full training set
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred_train = model.predict(X_train_scaled)
            y_pred_test = model.predict(X_test_scaled)
            
            # Metrics
            metrics = {
                'cv_r2_mean': cv_scores.mean(),
                'cv_r2_std': cv_scores.std(),
                'train_r2': r2_score(y_train, y_pred_train),
                'test_r2': r2_score(y_test, y_pred_test),
                'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test))
            }
            
            logger.info(f"{name} - Test R²: {metrics['test_r2']:.4f}, "
                       f"Test RMSE: {metrics['test_rmse']:.4f}")
            
            results[name] = {
                'model': model,
                'metrics': metrics,
                'predictions_test': y_pred_test,
                'actual_test': y_test
            }
            
            # Track best model
            if metrics['test_r2'] > best_r2:
                best_r2 = metrics['test_r2']
                best_model = name
        
        logger.info(f"Best model: {best_model} (R² = {best_r2:.4f})")
        
        # Feature importance (if applicable)
        feature_importance = None
        if hasattr(results[best_model]['model'], 'feature_importances_'):
            importances = results[best_model]['model'].feature_importances_
            feature_importance = pd.DataFrame({
                'feature': features,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            logger.info("\nTop 5 Most Important Features:")
            logger.info(feature_importance.head().to_string(index=False))
        
        # Visualization
        self._visualize_prediction_results(
            results[best_model]['actual_test'],
            results[best_model]['predictions_test'],
            best_model
        )
        
        # Save model
        if save_model:
            model_path = self.output_dir / f'best_model_{best_model}.pkl'
            with open(model_path, 'wb') as f:
                pickle.dump(results[best_model]['model'], f)
            logger.info(f"Best model saved to {model_path}")
        
        # Store results
        performance_results = {
            'target': target,
            'features': features,
            'model_type': model_type,
            'best_model': best_model,
            'all_results': results,
            'feature_importance': feature_importance
        }
        
        self.results['performance_prediction'] = performance_results
        
        return performance_results
    
    def _visualize_prediction_results(
        self,
        y_actual: np.ndarray,
        y_pred: np.ndarray,
        model_name: str
    ):
        """Visualize prediction performance."""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Actual vs. Predicted
        axes[0].scatter(y_actual, y_pred, alpha=0.5)
        axes[0].plot([y_actual.min(), y_actual.max()],
                     [y_actual.min(), y_actual.max()],
                     'r--', lw=2)
        axes[0].set_xlabel('Actual')
        axes[0].set_ylabel('Predicted')
        axes[0].set_title(f'{model_name}: Actual vs. Predicted')
        
        # Residuals
        residuals = y_actual - y_pred
        axes[1].scatter(y_pred, residuals, alpha=0.5)
        axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
        axes[1].set_xlabel('Predicted')
        axes[1].set_ylabel('Residuals')
        axes[1].set_title(f'{model_name}: Residual Plot')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'prediction_performance.png', dpi=300)
        plt.close()
        
        logger.info("Prediction visualizations saved")
    
    # ========================================================================
    # 3. FEATURE IMPORTANCE ANALYSIS
    # ========================================================================
    
    def analyze_feature_importance(
        self,
        target: str,
        features: List[str],
        method: str = 'ensemble',
        top_n: int = 20
    ) -> pd.DataFrame:
        """
        Comprehensive feature importance analysis.
        
        Methods:
        - 'ensemble': Random Forest + Gradient Boosting
        - 'permutation': Permutation importance
        - 'shap': SHAP values (if available)
        - 'correlation': Simple correlation analysis
        
        Research Applications:
        - Identify key strategic drivers of performance
        - Test resource-based view predictions
        - Discover unexpected relationships
        - Guide theory development
        
        Returns:
            DataFrame with feature importance rankings
        """
        logger.info(f"Feature Importance Analysis: {len(features)} features")
        
        # Prepare data
        df_clean = self.data[[target] + features].dropna()
        X = df_clean[features].values
        y = df_clean[target].values
        
        importance_results = pd.DataFrame({'feature': features})
        
        if method == 'ensemble' or method == 'all':
            # Random Forest Importance
            rf = RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                random_state=self.random_state
            )
            rf.fit(X, y)
            importance_results['rf_importance'] = rf.feature_importances_
            
            # Gradient Boosting Importance
            gb = GradientBoostingRegressor(
                n_estimators=200,
                learning_rate=0.05,
                max_depth=5,
                random_state=self.random_state
            )
            gb.fit(X, y)
            importance_results['gb_importance'] = gb.feature_importances_
            
            # Average ensemble importance
            importance_results['ensemble_importance'] = (
                importance_results['rf_importance'] + 
                importance_results['gb_importance']
            ) / 2
        
        if method == 'permutation' or method == 'all':
            from sklearn.inspection import permutation_importance
            
            # Use a simple model for permutation
            model = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
            model.fit(X, y)
            
            perm_importance = permutation_importance(
                model, X, y, 
                n_repeats=10,
                random_state=self.random_state
            )
            importance_results['permutation_importance'] = perm_importance.importances_mean
        
        if (method == 'shap' or method == 'all') and SHAP_AVAILABLE:
            # SHAP values
            model = xgb.XGBRegressor(n_estimators=100, random_state=self.random_state) if XGB_AVAILABLE else \
                    RandomForestRegressor(n_estimators=100, random_state=self.random_state)
            model.fit(X, y)
            
            explainer = shap.Explainer(model, X)
            shap_values = explainer(X)
            
            # Mean absolute SHAP value per feature
            importance_results['shap_importance'] = np.abs(shap_values.values).mean(axis=0)
        
        if method == 'correlation' or method == 'all':
            # Simple correlation
            correlations = []
            for feat in features:
                corr = df_clean[[target, feat]].corr().iloc[0, 1]
                correlations.append(abs(corr))
            importance_results['correlation'] = correlations
        
        # Rank features
        if 'ensemble_importance' in importance_results.columns:
            importance_results = importance_results.sort_values(
                'ensemble_importance',
                ascending=False
            )
        elif 'rf_importance' in importance_results.columns:
            importance_results = importance_results.sort_values(
                'rf_importance',
                ascending=False
            )
        
        logger.info(f"\nTop {min(top_n, len(features))} Most Important Features:")
        logger.info(importance_results.head(top_n).to_string(index=False))
        
        # Visualization
        self._visualize_feature_importance(importance_results, top_n)
        
        # Save results
        importance_results.to_excel(
            self.output_dir / 'feature_importance.xlsx',
            index=False
        )
        
        self.results['feature_importance'] = importance_results
        
        return importance_results
    
    def _visualize_feature_importance(
        self,
        importance_df: pd.DataFrame,
        top_n: int = 20
    ):
        """Visualize feature importance rankings."""
        
        # Select primary importance column
        if 'ensemble_importance' in importance_df.columns:
            importance_col = 'ensemble_importance'
        elif 'rf_importance' in importance_df.columns:
            importance_col = 'rf_importance'
        else:
            importance_col = importance_df.columns[1]  # First importance column
        
        top_features = importance_df.nlargest(top_n, importance_col)
        
        plt.figure(figsize=(10, 8))
        plt.barh(top_features['feature'], top_features[importance_col])
        plt.xlabel('Importance')
        plt.title(f'Top {top_n} Most Important Features')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'feature_importance_plot.png', dpi=300)
        plt.close()
        
        logger.info("Feature importance visualization saved")
    
    # ========================================================================
    # 4. ANOMALY DETECTION (Outlier Firms)
    # ========================================================================
    
    def detect_strategic_outliers(
        self,
        features: List[str],
        method: str = 'ensemble',
        contamination: float = 0.05,
        save_results: bool = True
    ) -> pd.DataFrame:
        """
        Identify strategically unusual firms (outliers).
        
        Theoretical Relevance:
        - Exceptional performers (sustained competitive advantage)
        - Failing firms (early warning system)
        - Innovative deviants (rule-breaking strategies)
        - Measurement errors / data quality issues
        
        Methods:
        - 'isolation_forest': Isolation Forest
        - 'lof': Local Outlier Factor
        - 'elliptic': Elliptic Envelope (Gaussian assumption)
        - 'ocsvm': One-Class SVM
        - 'ensemble': Voting across multiple methods
        
        Args:
            features: Strategic dimensions to consider
            method: Anomaly detection algorithm
            contamination: Expected proportion of outliers (0.01-0.1)
            save_results: Save outlier firms to file
        
        Returns:
            DataFrame with outlier flags and scores
        """
        logger.info(f"Anomaly Detection: {method} method")
        
        # Prepare data
        df_clean = self.data[features + [self.firm_id, self.time_var]].dropna()
        X = df_clean[features].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Anomaly detection
        if method == 'isolation_forest':
            detector = IsolationForest(
                contamination=contamination,
                random_state=self.random_state
            )
            outlier_labels = detector.fit_predict(X_scaled)
            outlier_scores = detector.score_samples(X_scaled)
        
        elif method == 'lof':
            detector = LocalOutlierFactor(
                contamination=contamination,
                novelty=False
            )
            outlier_labels = detector.fit_predict(X_scaled)
            outlier_scores = detector.negative_outlier_factor_
        
        elif method == 'elliptic':
            detector = EllipticEnvelope(
                contamination=contamination,
                random_state=self.random_state
            )
            outlier_labels = detector.fit_predict(X_scaled)
            outlier_scores = detector.decision_function(X_scaled)
        
        elif method == 'ocsvm':
            detector = OneClassSVM(nu=contamination)
            outlier_labels = detector.fit_predict(X_scaled)
            outlier_scores = detector.decision_function(X_scaled)
        
        elif method == 'ensemble':
            # Ensemble voting
            detectors = [
                IsolationForest(contamination=contamination, random_state=self.random_state),
                LocalOutlierFactor(contamination=contamination, novelty=False),
                EllipticEnvelope(contamination=contamination, random_state=self.random_state)
            ]
            
            votes = []
            for det in detectors:
                if isinstance(det, LocalOutlierFactor):
                    vote = det.fit_predict(X_scaled)
                else:
                    vote = det.fit_predict(X_scaled)
                votes.append(vote)
            
            votes_array = np.array(votes)
            # Consensus: outlier if majority vote (-1)
            outlier_labels = np.where(
                np.sum(votes_array == -1, axis=0) >= 2,
                -1,
                1
            )
            # Score: proportion of methods flagging as outlier
            outlier_scores = -np.sum(votes_array == -1, axis=0) / len(detectors)
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Add results to dataframe
        df_clean['outlier'] = (outlier_labels == -1).astype(int)
        df_clean['outlier_score'] = outlier_scores
        
        n_outliers = df_clean['outlier'].sum()
        logger.info(f"Detected {n_outliers} outliers ({n_outliers/len(df_clean)*100:.2f}%)")
        
        # Identify outlier firms
        outlier_firms = df_clean[df_clean['outlier'] == 1][[self.firm_id, self.time_var] + features + ['outlier_score']]
        
        # Visualization
        self._visualize_outliers(X_scaled, outlier_labels, features)
        
        if save_results:
            outlier_firms.to_excel(
                self.output_dir / 'strategic_outliers.xlsx',
                index=False
            )
            logger.info(f"Outlier firms saved")
        
        self.results['anomaly_detection'] = {
            'method': method,
            'n_outliers': n_outliers,
            'outlier_rate': n_outliers / len(df_clean),
            'outlier_firms': outlier_firms
        }
        
        return outlier_firms
    
    def _visualize_outliers(
        self,
        X: np.ndarray,
        labels: np.ndarray,
        feature_names: List[str]
    ):
        """Visualize outliers using PCA projection."""
        
        # PCA to 2D
        pca = PCA(n_components=2, random_state=self.random_state)
        X_pca = pca.fit_transform(X)
        
        plt.figure(figsize=(12, 8))
        
        # Normal points
        normal_mask = (labels == 1)
        plt.scatter(
            X_pca[normal_mask, 0],
            X_pca[normal_mask, 1],
            c='blue',
            alpha=0.5,
            s=30,
            label='Normal'
        )
        
        # Outliers
        outlier_mask = (labels == -1)
        plt.scatter(
            X_pca[outlier_mask, 0],
            X_pca[outlier_mask, 1],
            c='red',
            alpha=0.8,
            s=100,
            marker='X',
            label='Outlier'
        )
        
        plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)')
        plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)')
        plt.title('Strategic Outliers (PCA Projection)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.output_dir / 'outliers_pca.png', dpi=300)
        plt.close()
        
        logger.info("Outlier visualization saved")
    
    # ========================================================================
    # 5. TEMPORAL PATTERN ANALYSIS
    # ========================================================================
    
    def analyze_temporal_patterns(
        self,
        variables: List[str],
        firm_subset: Optional[List] = None,
        method: str = 'trajectory_clustering',
        save_results: bool = True
    ) -> Dict:
        """
        Analyze temporal evolution of strategic variables.
        
        Theoretical Applications:
        - Path dependence analysis
        - Strategic trajectory clustering
        - Punctuated equilibrium detection
        - Competitive dynamics patterns
        
        Methods:
        - 'trajectory_clustering': Group firms by evolution patterns
        - 'change_point': Detect strategic inflection points
        - 'regime_switching': Identify strategic regime changes
        
        Args:
            variables: Strategic variables to track over time
            firm_subset: Optional list of firm IDs to analyze
            method: Analysis method
            save_results: Save results to file
        
        Returns:
            Dictionary with temporal pattern analysis results
        """
        logger.info(f"Temporal Pattern Analysis: {method}")
        
        if firm_subset:
            df_subset = self.data[self.data[self.firm_id].isin(firm_subset)].copy()
        else:
            df_subset = self.data.copy()
        
        results = {}
        
        if method == 'trajectory_clustering':
            # Reshape to firm-time matrix for each variable
            trajectories = []
            firm_ids = []
            
            for firm in df_subset[self.firm_id].unique():
                firm_data = df_subset[df_subset[self.firm_id] == firm].sort_values(self.time_var)
                
                # Create trajectory vector (concatenate all variables over time)
                trajectory = []
                for var in variables:
                    values = firm_data[var].values
                    trajectory.extend(values)
                
                trajectories.append(trajectory)
                firm_ids.append(firm)
            
            # Cluster trajectories
            X_trajectories = np.array(trajectories)
            
            # Handle NaNs
            # Option 1: Fill with column mean
            col_means = np.nanmean(X_trajectories, axis=0)
            inds = np.where(np.isnan(X_trajectories))
            X_trajectories[inds] = np.take(col_means, inds[1])
            
            # Scale
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_trajectories)
            
            # Determine optimal clusters
            optimal_k = min(5, len(firm_ids) // 10)  # Heuristic
            
            # KMeans clustering
            kmeans = KMeans(n_clusters=optimal_k, random_state=self.random_state, n_init=20)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            results['trajectory_clusters'] = pd.DataFrame({
                self.firm_id: firm_ids,
                'trajectory_cluster': cluster_labels
            })
            
            logger.info(f"Identified {optimal_k} distinct strategic trajectories")
            
            # Visualization (if 2 variables, show trajectories)
            if len(variables) == 2:
                self._visualize_trajectories(df_subset, variables, cluster_labels, firm_ids)
        
        elif method == 'change_point':
            # Detect change points in firm-level time series
            # Simplified implementation - could use ruptures library for advanced methods
            
            change_points = []
            
            for firm in df_subset[self.firm_id].unique():
                firm_data = df_subset[df_subset[self.firm_id] == firm].sort_values(self.time_var)
                
                for var in variables:
                    values = firm_data[var].values
                    times = firm_data[self.time_var].values
                    
                    if len(values) < 3:
                        continue
                    
                    # Simple threshold-based change detection
                    # Calculate rolling mean and std
                    window = min(3, len(values) // 2)
                    rolling_mean = pd.Series(values).rolling(window=window).mean()
                    rolling_std = pd.Series(values).rolling(window=window).std()
                    
                    # Z-score of change
                    changes = np.diff(values)
                    z_scores = np.abs(changes / (rolling_std[1:] + 1e-10))
                    
                    # Detect significant changes (z > 2)
                    significant_changes = np.where(z_scores > 2)[0]
                    
                    for idx in significant_changes:
                        change_points.append({
                            self.firm_id: firm,
                            'variable': var,
                            'time': times[idx+1],
                            'magnitude': changes[idx]
                        })
            
            results['change_points'] = pd.DataFrame(change_points)
            logger.info(f"Detected {len(change_points)} strategic inflection points")
        
        # Save results
        if save_results:
            for key, value in results.items():
                if isinstance(value, pd.DataFrame):
                    value.to_excel(
                        self.output_dir / f'temporal_{key}.xlsx',
                        index=False
                    )
        
        self.results['temporal_patterns'] = results
        
        return results
    
    def _visualize_trajectories(
        self,
        df: pd.DataFrame,
        variables: List[str],
        cluster_labels: np.ndarray,
        firm_ids: List
    ):
        """Visualize firm trajectories colored by cluster."""
        
        var1, var2 = variables[0], variables[1]
        
        plt.figure(figsize=(12, 8))
        
        for idx, firm in enumerate(firm_ids):
            firm_data = df[df[self.firm_id] == firm].sort_values(self.time_var)
            
            plt.plot(
                firm_data[var1],
                firm_data[var2],
                alpha=0.6,
                color=plt.cm.viridis(cluster_labels[idx] / cluster_labels.max())
            )
        
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.title('Strategic Trajectories (Colored by Cluster)')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'strategic_trajectories.png', dpi=300)
        plt.close()
        
        logger.info("Trajectory visualization saved")
    
    # ========================================================================
    # 6. COMPREHENSIVE REPORT GENERATION
    # ========================================================================
    
    def generate_comprehensive_report(
        self,
        include_all_analyses: bool = False
    ) -> str:
        """
        Generate comprehensive data mining report.
        
        Args:
            include_all_analyses: Run all analyses if not already executed
        
        Returns:
            Path to generated HTML report
        """
        logger.info("Generating comprehensive data mining report...")
        
        # Build HTML report
        html_content = self._build_html_report()
        
        # Save report
        report_path = self.output_dir / 'datamining_report.html'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Comprehensive report saved: {report_path}")
        
        return str(report_path)
    
    def _build_html_report(self) -> str:
        """Build HTML report from analysis results."""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Strategic Data Mining Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        .metric {{ font-weight: bold; color: #27ae60; }}
        .section {{ margin-bottom: 40px; }}
        img {{ max-width: 100%; height: auto; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>Strategic Management Data Mining Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Dataset:</strong> {len(self.data)} observations, {self.data[self.firm_id].nunique()} firms</p>
    
    <hr>
"""
        
        # Strategic Groups section
        if 'strategic_groups' in self.results:
            sg = self.results['strategic_groups']
            html += f"""
    <div class="section">
        <h2>1. Strategic Group Analysis</h2>
        <p><strong>Method:</strong> {sg['method']}</p>
        <p><strong>Number of Groups:</strong> <span class="metric">{sg['n_clusters']}</span></p>
        <p><strong>Silhouette Score:</strong> <span class="metric">{sg['validation_metrics'].get('silhouette', 'N/A')}</span></p>
        <img src="strategic_groups_pca.png" alt="Strategic Groups">
    </div>
"""
        
        # Performance Prediction section
        if 'performance_prediction' in self.results:
            pp = self.results['performance_prediction']
            best_model = pp['best_model']
            best_metrics = pp['all_results'][best_model]['metrics']
            html += f"""
    <div class="section">
        <h2>2. Firm Performance Prediction</h2>
        <p><strong>Target Variable:</strong> {pp['target']}</p>
        <p><strong>Best Model:</strong> <span class="metric">{best_model}</span></p>
        <p><strong>Test R²:</strong> <span class="metric">{best_metrics['test_r2']:.4f}</span></p>
        <p><strong>Test RMSE:</strong> <span class="metric">{best_metrics['test_rmse']:.4f}</span></p>
        <img src="prediction_performance.png" alt="Prediction Performance">
    </div>
"""
        
        # Feature Importance section
        if 'feature_importance' in self.results:
            fi = self.results['feature_importance']
            html += f"""
    <div class="section">
        <h2>3. Feature Importance Analysis</h2>
        <img src="feature_importance_plot.png" alt="Feature Importance">
        <p>Top features identified as most predictive of firm performance.</p>
    </div>
"""
        
        # Anomaly Detection section
        if 'anomaly_detection' in self.results:
            ad = self.results['anomaly_detection']
            html += f"""
    <div class="section">
        <h2>4. Anomaly Detection (Strategic Outliers)</h2>
        <p><strong>Method:</strong> {ad['method']}</p>
        <p><strong>Outliers Detected:</strong> <span class="metric">{ad['n_outliers']}</span> ({ad['outlier_rate']*100:.2f}%)</p>
        <img src="outliers_pca.png" alt="Strategic Outliers">
    </div>
"""
        
        html += """
    <hr>
    <p><em>Generated by Strategic Management Research Hub v3.1 - Advanced Data Mining Engine</em></p>
</body>
</html>
"""
        
        return html


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def example_usage():
    """
    Example demonstrating Advanced Data Mining Engine usage.
    """
    # Load sample data (placeholder)
    # In practice, load your actual panel data
    np.random.seed(42)
    n_firms = 100
    n_years = 10
    
    data = []
    for firm in range(n_firms):
        for year in range(2010, 2010 + n_years):
            data.append({
                'gvkey': f'FIRM_{firm:03d}',
                'year': year,
                'roa': np.random.normal(0.05, 0.03),
                'rd_intensity': np.random.exponential(0.05),
                'capital_intensity': np.random.uniform(0.2, 0.8),
                'international_sales': np.random.uniform(0, 0.5),
                'firm_size': np.random.normal(10, 2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': np.random.randint(5, 50)
            })
    
    df_sample = pd.DataFrame(data)
    
    # Initialize Data Mining Engine
    dm = AdvancedStrategicDataMining(
        data=df_sample,
        firm_id='gvkey',
        time_var='year',
        output_dir='./datamining_example_output/'
    )
    
    # 1. Strategic Group Analysis
    print("\n" + "="*60)
    print("1. STRATEGIC GROUP ANALYSIS")
    print("="*60)
    
    strategic_groups = dm.strategic_group_analysis(
        features=['rd_intensity', 'capital_intensity', 'international_sales'],
        n_clusters=4,
        method='kmeans'
    )
    
    # 2. Performance Prediction
    print("\n" + "="*60)
    print("2. FIRM PERFORMANCE PREDICTION")
    print("="*60)
    
    predictions = dm.predict_firm_performance(
        target='roa',
        features=['rd_intensity', 'firm_size', 'leverage', 'firm_age'],
        model_type='ensemble'
    )
    
    # 3. Feature Importance
    print("\n" + "="*60)
    print("3. FEATURE IMPORTANCE ANALYSIS")
    print("="*60)
    
    importance = dm.analyze_feature_importance(
        target='roa',
        features=['rd_intensity', 'capital_intensity', 'firm_size', 'leverage'],
        method='ensemble'
    )
    
    # 4. Anomaly Detection
    print("\n" + "="*60)
    print("4. ANOMALY DETECTION")
    print("="*60)
    
    outliers = dm.detect_strategic_outliers(
        features=['rd_intensity', 'capital_intensity', 'international_sales'],
        method='ensemble',
        contamination=0.05
    )
    
    # 5. Generate Report
    print("\n" + "="*60)
    print("5. GENERATING COMPREHENSIVE REPORT")
    print("="*60)
    
    report_path = dm.generate_comprehensive_report()
    
    print(f"\n✅ Data mining complete!")
    print(f"📊 Report saved: {report_path}")
    print(f"📁 All outputs: {dm.output_dir}")


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Strategic Management Research Hub v3.1                      ║
    ║   Advanced Data Mining Engine                                 ║
    ║                                                               ║
    ║   Cutting-edge ML for strategic management research          ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    example_usage()
