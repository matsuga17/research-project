"""
Strategic Management Research Hub - Data Mining Module
=======================================================

Advanced data mining and machine learning for strategic management research:
- Clustering Analysis (Firm Segmentation)
- Dimensionality Reduction (PCA, t-SNE, UMAP)
- Anomaly Detection (Outlier Firms)
- Feature Importance Analysis
- Predictive Modeling (Performance, Failure Prediction)
- Association Rule Mining
- Time Series Pattern Discovery

Integrates with existing modules for comprehensive research workflow.

Author: Strategic Management Research Hub
Version: 3.0
License: MIT

References:
- Ketchen & Shook (1996): Cluster Analysis in Strategic Management. SMJ
- Hair et al. (2014): Multivariate Data Analysis
- Hastie et al. (2009): The Elements of Statistical Learning
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union, Set
import logging
from pathlib import Path
import warnings
import json

# Clustering
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform

# Dimensionality Reduction
from sklearn.decomposition import PCA, FactorAnalysis
from sklearn.manifold import TSNE

try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False
    warnings.warn("UMAP not installed. Install with: pip install umap-learn")

# Anomaly Detection
from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor

# Predictive Modeling
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, r2_score, mean_absolute_error
)

# Preprocessing
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FirmClusterAnalyzer:
    """
    Cluster analysis for firm segmentation and strategic group identification.
    
    Strategic groups are clusters of firms pursuing similar strategies.
    
    Usage:
    ```python
    analyzer = FirmClusterAnalyzer()
    
    # Prepare data
    features = df[['rd_intensity', 'advertising_intensity', 'log_assets', 'leverage']]
    
    # Determine optimal clusters
    analyzer.plot_elbow_curve(features, max_clusters=10)
    
    # Perform clustering
    clusters = analyzer.kmeans_clustering(features, n_clusters=4)
    
    # Analyze cluster characteristics
    profiles = analyzer.cluster_profiles(df, clusters, features.columns)
    
    # Visualize (2D projection)
    analyzer.visualize_clusters(features, clusters, method='pca')
    ```
    
    References:
    - Ketchen & Shook (1996): The Application of Cluster Analysis. SMJ
    - Short et al. (2008): Strategic Groups. SMJ
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.clusters = None
        self.cluster_centers = None
        
    def kmeans_clustering(
        self,
        X: pd.DataFrame,
        n_clusters: int = 3,
        random_state: int = 42,
        scale: bool = True
    ) -> np.ndarray:
        """
        Perform K-means clustering.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix (firms × variables)
        n_clusters : int
            Number of clusters (strategic groups)
        random_state : int
            Random seed for reproducibility
        scale : bool
            Whether to standardize features
            
        Returns:
        --------
        clusters : ndarray
            Cluster assignments for each firm
        """
        logger.info(f"Performing K-means clustering with {n_clusters} clusters...")
        
        # Scale features
        if scale:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X.values
            
        # K-means
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)
        
        self.clusters = clusters
        self.cluster_centers = kmeans.cluster_centers_
        
        logger.info(f"Clustering complete. Cluster sizes: {np.bincount(clusters)}")
        
        return clusters
        
    def hierarchical_clustering(
        self,
        X: pd.DataFrame,
        n_clusters: int = 3,
        linkage_method: str = 'ward',
        scale: bool = True
    ) -> np.ndarray:
        """
        Perform hierarchical clustering.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        n_clusters : int
            Number of clusters
        linkage_method : str
            Linkage method: 'ward', 'complete', 'average', 'single'
        scale : bool
            Whether to standardize features
            
        Returns:
        --------
        clusters : ndarray
            Cluster assignments
        """
        logger.info(f"Performing hierarchical clustering ({linkage_method} linkage)...")
        
        if scale:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X.values
            
        clustering = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage_method
        )
        clusters = clustering.fit_predict(X_scaled)
        
        self.clusters = clusters
        
        logger.info(f"Clustering complete. Cluster sizes: {np.bincount(clusters)}")
        
        return clusters
        
    def plot_elbow_curve(
        self,
        X: pd.DataFrame,
        max_clusters: int = 10,
        output_path: Optional[str] = None
    ):
        """
        Plot elbow curve to determine optimal number of clusters.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        max_clusters : int
            Maximum number of clusters to test
        output_path : str, optional
            Path to save figure
        """
        logger.info("Computing elbow curve...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        inertias = []
        silhouettes = []
        K_range = range(2, max_clusters + 1)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            
            # Silhouette score
            from sklearn.metrics import silhouette_score
            score = silhouette_score(X_scaled, kmeans.labels_)
            silhouettes.append(score)
            
        # Plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Elbow curve
        axes[0].plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
        axes[0].set_xlabel('Number of Clusters', fontsize=12)
        axes[0].set_ylabel('Within-Cluster Sum of Squares', fontsize=12)
        axes[0].set_title('Elbow Curve', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # Silhouette scores
        axes[1].plot(K_range, silhouettes, 'ro-', linewidth=2, markersize=8)
        axes[1].set_xlabel('Number of Clusters', fontsize=12)
        axes[1].set_ylabel('Silhouette Score', fontsize=12)
        axes[1].set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0.5, color='green', linestyle='--', alpha=0.5, label='Good (>0.5)')
        axes[1].legend()
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Elbow curve saved to {output_path}")
        else:
            plt.show()
            
        plt.close()
        
    def cluster_profiles(
        self,
        df: pd.DataFrame,
        clusters: np.ndarray,
        feature_cols: List[str]
    ) -> pd.DataFrame:
        """
        Generate cluster profiles (strategic group characteristics).
        
        Parameters:
        -----------
        df : DataFrame
            Full dataset
        clusters : ndarray
            Cluster assignments
        feature_cols : list
            Feature column names
            
        Returns:
        --------
        profiles : DataFrame
            Mean values for each cluster
        """
        logger.info("Generating cluster profiles...")
        
        df_temp = df.copy()
        df_temp['cluster'] = clusters
        
        # Compute means by cluster
        profiles = df_temp.groupby('cluster')[feature_cols].mean()
        
        # Add cluster sizes
        profiles['cluster_size'] = df_temp['cluster'].value_counts().sort_index()
        
        # Add percentage
        profiles['percentage'] = (profiles['cluster_size'] / len(df_temp)) * 100
        
        logger.info("\nCluster Profiles:")
        logger.info("\n" + str(profiles))
        
        return profiles
        
    def visualize_clusters(
        self,
        X: pd.DataFrame,
        clusters: np.ndarray,
        method: str = 'pca',
        output_path: Optional[str] = None
    ):
        """
        Visualize clusters in 2D using dimensionality reduction.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        clusters : ndarray
            Cluster assignments
        method : str
            Reduction method: 'pca', 'tsne', 'umap'
        output_path : str, optional
            Path to save figure
        """
        logger.info(f"Visualizing clusters using {method.upper()}...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        # Dimensionality reduction
        if method == 'pca':
            reducer = PCA(n_components=2, random_state=42)
            X_2d = reducer.fit_transform(X_scaled)
            explained_var = reducer.explained_variance_ratio_
            title = f'Cluster Visualization (PCA: {explained_var[0]:.1%} + {explained_var[1]:.1%} variance)'
        elif method == 'tsne':
            reducer = TSNE(n_components=2, random_state=42)
            X_2d = reducer.fit_transform(X_scaled)
            title = 'Cluster Visualization (t-SNE)'
        elif method == 'umap':
            if not UMAP_AVAILABLE:
                logger.warning("UMAP not available. Using PCA instead.")
                method = 'pca'
                reducer = PCA(n_components=2, random_state=42)
                X_2d = reducer.fit_transform(X_scaled)
                title = 'Cluster Visualization (PCA)'
            else:
                reducer = umap.UMAP(n_components=2, random_state=42)
                X_2d = reducer.fit_transform(X_scaled)
                title = 'Cluster Visualization (UMAP)'
        else:
            raise ValueError(f"Unknown method: {method}")
            
        # Plot
        plt.figure(figsize=(12, 8))
        
        n_clusters = len(np.unique(clusters))
        colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
        
        for i in range(n_clusters):
            mask = clusters == i
            plt.scatter(
                X_2d[mask, 0],
                X_2d[mask, 1],
                c=[colors[i]],
                label=f'Cluster {i+1} (n={mask.sum()})',
                s=100,
                alpha=0.7,
                edgecolors='black',
                linewidth=0.5
            )
            
        plt.xlabel('Component 1', fontsize=12)
        plt.ylabel('Component 2', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Cluster visualization saved to {output_path}")
        else:
            plt.show()
            
        plt.close()


class AnomalyDetector:
    """
    Detect anomalous firms (outliers) in the dataset.
    
    Useful for:
    - Identifying exceptional performers
    - Detecting data quality issues
    - Finding rare strategic configurations
    
    Usage:
    ```python
    detector = AnomalyDetector()
    
    # Detect anomalies
    anomalies = detector.isolation_forest(df, features)
    
    # Analyze anomalous firms
    anomalous_firms = df[anomalies == -1]
    print(anomalous_firms)
    ```
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        
    def isolation_forest(
        self,
        X: pd.DataFrame,
        contamination: float = 0.05,
        random_state: int = 42
    ) -> np.ndarray:
        """
        Detect anomalies using Isolation Forest.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        contamination : float
            Expected proportion of outliers (0.01-0.10)
        random_state : int
            Random seed
            
        Returns:
        --------
        predictions : ndarray
            1 for normal, -1 for anomaly
        """
        logger.info(f"Detecting anomalies (contamination={contamination})...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        predictions = iso_forest.fit_predict(X_scaled)
        
        n_anomalies = (predictions == -1).sum()
        logger.info(f"Detected {n_anomalies} anomalies ({n_anomalies/len(X):.1%})")
        
        return predictions
        
    def local_outlier_factor(
        self,
        X: pd.DataFrame,
        n_neighbors: int = 20,
        contamination: float = 0.05
    ) -> np.ndarray:
        """
        Detect anomalies using Local Outlier Factor.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        n_neighbors : int
            Number of neighbors for density estimation
        contamination : float
            Expected proportion of outliers
            
        Returns:
        --------
        predictions : ndarray
            1 for normal, -1 for anomaly
        """
        logger.info("Detecting anomalies using LOF...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        lof = LocalOutlierFactor(
            n_neighbors=n_neighbors,
            contamination=contamination
        )
        predictions = lof.fit_predict(X_scaled)
        
        n_anomalies = (predictions == -1).sum()
        logger.info(f"Detected {n_anomalies} anomalies ({n_anomalies/len(X):.1%})")
        
        return predictions


class FeatureImportanceAnalyzer:
    """
    Analyze feature importance for understanding key drivers of performance.
    
    Usage:
    ```python
    analyzer = FeatureImportanceAnalyzer()
    
    # Train model and get importance
    importance = analyzer.random_forest_importance(
        X_train, y_train,
        feature_names=X.columns
    )
    
    # Visualize
    analyzer.plot_importance(importance)
    ```
    """
    
    def __init__(self):
        self.model = None
        
    def random_forest_importance(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        feature_names: List[str],
        task: str = 'regression',
        n_estimators: int = 100,
        random_state: int = 42
    ) -> pd.DataFrame:
        """
        Compute feature importance using Random Forest.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
        y : Series
            Target variable
        feature_names : list
            Feature column names
        task : str
            'regression' or 'classification'
        n_estimators : int
            Number of trees
        random_state : int
            Random seed
            
        Returns:
        --------
        importance_df : DataFrame
            Features ranked by importance
        """
        logger.info("Computing feature importance...")
        
        if task == 'regression':
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                random_state=random_state,
                max_depth=10
            )
        else:
            model = RandomForestClassifier(
                n_estimators=n_estimators,
                random_state=random_state,
                max_depth=10
            )
            
        model.fit(X, y)
        self.model = model
        
        # Extract importance
        importances = model.feature_importances_
        std = np.std([tree.feature_importances_ for tree in model.estimators_], axis=0)
        
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': importances,
            'std': std
        }).sort_values('importance', ascending=False)
        
        logger.info("\nTop 10 Important Features:")
        logger.info("\n" + str(importance_df.head(10)))
        
        return importance_df
        
    def plot_importance(
        self,
        importance_df: pd.DataFrame,
        top_n: int = 15,
        output_path: Optional[str] = None
    ):
        """
        Plot feature importance.
        
        Parameters:
        -----------
        importance_df : DataFrame
            Feature importance from random_forest_importance()
        top_n : int
            Number of top features to display
        output_path : str, optional
            Path to save figure
        """
        plt.figure(figsize=(10, 8))
        
        top_features = importance_df.head(top_n)
        
        plt.barh(
            range(len(top_features)),
            top_features['importance'],
            xerr=top_features['std'],
            align='center',
            alpha=0.8,
            color='steelblue',
            edgecolor='black'
        )
        
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.title(f'Top {top_n} Feature Importance', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Importance plot saved to {output_path}")
        else:
            plt.show()
            
        plt.close()


class PerformancePredictor:
    """
    Predict firm performance using machine learning.
    
    Usage:
    ```python
    predictor = PerformancePredictor()
    
    # Train model
    results = predictor.train_regression_model(
        X_train, y_train, X_test, y_test,
        model_type='random_forest'
    )
    
    # Predict new cases
    predictions = predictor.predict(X_new)
    ```
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def train_regression_model(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_test: pd.DataFrame,
        y_test: pd.Series,
        model_type: str = 'random_forest',
        cv_folds: int = 5
    ) -> Dict:
        """
        Train and evaluate regression model.
        
        Parameters:
        -----------
        X_train, y_train : DataFrame, Series
            Training data
        X_test, y_test : DataFrame, Series
            Test data
        model_type : str
            'random_forest' or 'gradient_boosting'
        cv_folds : int
            Cross-validation folds
            
        Returns:
        --------
        results : dict
            Model performance metrics
        """
        logger.info(f"Training {model_type} regression model...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Select model
        if model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
            
        # Train
        model.fit(X_train_scaled, y_train)
        self.model = model
        self.feature_names = X_train.columns.tolist()
        
        # Predictions
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)
        
        # Evaluate
        results = {
            'train_r2': r2_score(y_train, y_train_pred),
            'test_r2': r2_score(y_test, y_test_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_test_pred)),
            'train_mae': mean_absolute_error(y_train, y_train_pred),
            'test_mae': mean_absolute_error(y_test, y_test_pred)
        }
        
        # Cross-validation
        cv_scores = cross_val_score(
            model, X_train_scaled, y_train,
            cv=cv_folds, scoring='r2'
        )
        results['cv_r2_mean'] = cv_scores.mean()
        results['cv_r2_std'] = cv_scores.std()
        
        logger.info("\nModel Performance:")
        logger.info(f"  Train R²: {results['train_r2']:.4f}")
        logger.info(f"  Test R²: {results['test_r2']:.4f}")
        logger.info(f"  Test RMSE: {results['test_rmse']:.4f}")
        logger.info(f"  CV R² (mean±std): {results['cv_r2_mean']:.4f}±{results['cv_r2_std']:.4f}")
        
        return results
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Make predictions on new data.
        
        Parameters:
        -----------
        X : DataFrame
            Feature matrix
            
        Returns:
        --------
        predictions : ndarray
            Predicted values
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_regression_model() first.")
            
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("Data Mining Module - Example Usage")
    print("=" * 80)
    
    # Generate sample data
    np.random.seed(42)
    n_firms = 200
    
    data = pd.DataFrame({
        'firm_id': range(1, n_firms + 1),
        'rd_intensity': np.random.beta(2, 5, n_firms) * 0.3,
        'advertising_intensity': np.random.beta(3, 5, n_firms) * 0.2,
        'log_assets': np.random.normal(10, 1.5, n_firms),
        'leverage': np.random.beta(2, 3, n_firms) * 0.8,
        'roa': np.random.normal(0.05, 0.02, n_firms)
    })
    
    # Add some anomalies
    data.loc[:5, 'roa'] = 0.15  # Exceptional performers
    
    print("\nExample 1: Cluster Analysis (Strategic Groups)")
    print("-" * 80)
    
    features = ['rd_intensity', 'advertising_intensity', 'log_assets', 'leverage']
    X = data[features]
    
    analyzer = FirmClusterAnalyzer()
    
    # Determine optimal clusters
    analyzer.plot_elbow_curve(X, max_clusters=8)
    
    # Perform clustering
    clusters = analyzer.kmeans_clustering(X, n_clusters=3)
    
    # Cluster profiles
    profiles = analyzer.cluster_profiles(data, clusters, features)
    print("\nCluster Profiles:")
    print(profiles)
    
    # Visualize
    analyzer.visualize_clusters(X, clusters, method='pca')
    
    print("\n\nExample 2: Anomaly Detection")
    print("-" * 80)
    
    detector = AnomalyDetector()
    anomalies = detector.isolation_forest(X, contamination=0.05)
    
    print(f"\nAnomalous firms:")
    print(data[anomalies == -1][['firm_id', 'roa', 'rd_intensity', 'log_assets']])
    
    print("\n\nExample 3: Feature Importance")
    print("-" * 80)
    
    importance_analyzer = FeatureImportanceAnalyzer()
    importance = importance_analyzer.random_forest_importance(
        X, data['roa'],
        feature_names=features,
        task='regression'
    )
    
    importance_analyzer.plot_importance(importance)
    
    print("\n" + "=" * 80)
    print("Data mining module ready for use!")
    print("=" * 80)
