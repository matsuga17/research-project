"""
clustering.py

Enterprise Clustering for Strategic Group Analysis

This module provides comprehensive clustering functionality for strategic
management research, including:
- K-means clustering
- Hierarchical clustering
- DBSCAN
- Cluster evaluation metrics
- Visualization tools

Usage:
    from clustering import FirmClusterer
    
    clusterer = FirmClusterer(df, features=['roa', 'rd_intensity', 'leverage'])
    clusterer.preprocess()
    labels = clusterer.kmeans(n_clusters=3)
    stats = clusterer.describe_clusters(labels)
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirmClusterer:
    """
    Comprehensive clustering tool for firm-level strategic analysis
    
    Attributes:
        df: Input DataFrame
        features: List of feature column names
        X: Preprocessed feature matrix
        scaler: StandardScaler instance
        labels_: Most recent clustering labels
    """
    
    def __init__(self, df: pd.DataFrame, features: List[str]):
        """
        Initialize clusterer
        
        Args:
            df: DataFrame with firm data
            features: List of feature column names to use for clustering
        """
        self.df = df.copy()
        self.features = features
        self.X = None
        self.X_scaled = None
        self.scaler = StandardScaler()
        self.labels_ = None
        self.df_clean = None
        
        logger.info(f"FirmClusterer initialized with {len(features)} features")
        logger.info(f"Features: {', '.join(features)}")
    
    def preprocess(self, handle_missing: str = 'drop') -> np.ndarray:
        """
        Preprocess data: handle missing values and standardize
        
        Args:
            handle_missing: How to handle missing values ('drop', 'mean', 'median')
        
        Returns:
            Standardized feature matrix
        """
        logger.info("Preprocessing data...")
        
        # Extract features
        self.df_clean = self.df[self.features].copy()
        
        # Handle missing values
        if handle_missing == 'drop':
            self.df_clean = self.df_clean.dropna()
            logger.info(f"Dropped rows with missing values: {len(self.df)} → {len(self.df_clean)}")
        elif handle_missing == 'mean':
            self.df_clean = self.df_clean.fillna(self.df_clean.mean())
        elif handle_missing == 'median':
            self.df_clean = self.df_clean.fillna(self.df_clean.median())
        
        # Convert to numpy array
        self.X = self.df_clean.values
        
        # Standardize
        self.X_scaled = self.scaler.fit_transform(self.X)
        
        logger.info(f"Preprocessing complete: {self.X_scaled.shape[0]} samples, {self.X_scaled.shape[1]} features")
        
        return self.X_scaled
    
    def kmeans(self, n_clusters: int = 3, **kwargs) -> np.ndarray:
        """
        K-means clustering
        
        Args:
            n_clusters: Number of clusters
            **kwargs: Additional arguments for KMeans
        
        Returns:
            Cluster labels
        """
        logger.info(f"Running K-means with k={n_clusters}")
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, **kwargs)
        labels = kmeans.fit_predict(self.X_scaled)
        
        # Evaluate
        silhouette = silhouette_score(self.X_scaled, labels)
        davies_bouldin = davies_bouldin_score(self.X_scaled, labels)
        calinski = calinski_harabasz_score(self.X_scaled, labels)
        
        logger.info(f"K-means results:")
        logger.info(f"  Silhouette Score: {silhouette:.3f}")
        logger.info(f"  Davies-Bouldin Index: {davies_bouldin:.3f}")
        logger.info(f"  Calinski-Harabasz Score: {calinski:.1f}")
        
        self.labels_ = labels
        return labels
    
    def hierarchical(self, n_clusters: int = 3, linkage: str = 'ward', **kwargs) -> np.ndarray:
        """
        Hierarchical clustering
        
        Args:
            n_clusters: Number of clusters
            linkage: Linkage criterion ('ward', 'complete', 'average', 'single')
            **kwargs: Additional arguments for AgglomerativeClustering
        
        Returns:
            Cluster labels
        """
        logger.info(f"Running Hierarchical clustering (k={n_clusters}, linkage={linkage})")
        
        hc = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage, **kwargs)
        labels = hc.fit_predict(self.X_scaled)
        
        # Evaluate
        silhouette = silhouette_score(self.X_scaled, labels)
        davies_bouldin = davies_bouldin_score(self.X_scaled, labels)
        
        logger.info(f"Hierarchical clustering results:")
        logger.info(f"  Silhouette Score: {silhouette:.3f}")
        logger.info(f"  Davies-Bouldin Index: {davies_bouldin:.3f}")
        
        self.labels_ = labels
        return labels
    
    def dbscan(self, eps: float = 0.5, min_samples: int = 5, **kwargs) -> np.ndarray:
        """
        DBSCAN clustering
        
        Args:
            eps: Maximum distance between two samples
            min_samples: Minimum samples in a neighborhood
            **kwargs: Additional arguments for DBSCAN
        
        Returns:
            Cluster labels (-1 indicates noise points)
        """
        logger.info(f"Running DBSCAN (eps={eps}, min_samples={min_samples})")
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples, **kwargs)
        labels = dbscan.fit_predict(self.X_scaled)
        
        # Count clusters and noise
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = (labels == -1).sum()
        
        logger.info(f"DBSCAN results:")
        logger.info(f"  Clusters: {n_clusters}")
        logger.info(f"  Noise points: {n_noise} ({n_noise/len(labels)*100:.1f}%)")
        
        if n_clusters > 1:
            # Only calculate silhouette if there are multiple clusters
            mask = labels != -1
            if mask.sum() > 0:
                silhouette = silhouette_score(self.X_scaled[mask], labels[mask])
                logger.info(f"  Silhouette Score: {silhouette:.3f}")
        
        self.labels_ = labels
        return labels
    
    def find_optimal_k(self, max_k: int = 10, method: str = 'elbow') -> Tuple[int, plt.Figure]:
        """
        Find optimal number of clusters
        
        Args:
            max_k: Maximum number of clusters to try
            method: Method to use ('elbow', 'silhouette', 'both')
        
        Returns:
            Tuple of (optimal_k, figure)
        """
        logger.info(f"Finding optimal k (max_k={max_k}, method={method})")
        
        inertias = []
        silhouettes = []
        davies_bouldins = []
        
        for k in range(2, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.X_scaled)
            
            inertias.append(kmeans.inertia_)
            silhouettes.append(silhouette_score(self.X_scaled, labels))
            davies_bouldins.append(davies_bouldin_score(self.X_scaled, labels))
        
        # Create plots
        if method in ['elbow', 'both']:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            # Elbow plot
            axes[0].plot(range(2, max_k + 1), inertias, 'bo-', linewidth=2, markersize=8)
            axes[0].set_xlabel('Number of Clusters (k)', fontsize=12)
            axes[0].set_ylabel('Inertia (Within-cluster sum of squares)', fontsize=12)
            axes[0].set_title('Elbow Method', fontsize=14, fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            
            # Silhouette plot
            axes[1].plot(range(2, max_k + 1), silhouettes, 'ro-', linewidth=2, markersize=8)
            axes[1].set_xlabel('Number of Clusters (k)', fontsize=12)
            axes[1].set_ylabel('Silhouette Score', fontsize=12)
            axes[1].set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
            axes[1].grid(True, alpha=0.3)
            axes[1].axhline(y=0.5, color='g', linestyle='--', label='Good threshold (0.5)')
            axes[1].legend()
            
            plt.tight_layout()
            
        elif method == 'silhouette':
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(range(2, max_k + 1), silhouettes, 'ro-', linewidth=2, markersize=8)
            ax.set_xlabel('Number of Clusters (k)', fontsize=12)
            ax.set_ylabel('Silhouette Score', fontsize=12)
            ax.set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0.5, color='g', linestyle='--', label='Good threshold (0.5)')
            ax.legend()
        
        # Determine optimal k
        optimal_k_silhouette = silhouettes.index(max(silhouettes)) + 2
        
        logger.info(f"Optimal k by Silhouette Score: {optimal_k_silhouette}")
        
        return optimal_k_silhouette, fig
    
    def describe_clusters(self, labels: np.ndarray) -> pd.DataFrame:
        """
        Describe cluster characteristics
        
        Args:
            labels: Cluster labels
        
        Returns:
            DataFrame with cluster statistics
        """
        logger.info("Describing cluster characteristics...")
        
        # Add labels to dataframe
        self.df_clean['cluster'] = labels
        
        # Calculate statistics for each cluster
        cluster_stats = self.df_clean.groupby('cluster')[self.features].agg([
            'count', 'mean', 'std', 'min', 'max'
        ])
        
        logger.info(f"\nCluster sizes:")
        for cluster_id in sorted(set(labels)):
            count = (labels == cluster_id).sum()
            pct = count / len(labels) * 100
            logger.info(f"  Cluster {cluster_id}: {count} firms ({pct:.1f}%)")
        
        return cluster_stats
    
    def visualize_clusters(self, labels: np.ndarray, 
                          method: str = 'pca',
                          figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Visualize clusters in 2D
        
        Args:
            labels: Cluster labels
            method: Dimensionality reduction method ('pca' or 'tsne')
            figsize: Figure size
        
        Returns:
            Matplotlib figure
        """
        logger.info(f"Creating cluster visualization using {method.upper()}...")
        
        # Dimensionality reduction
        if method == 'pca':
            reducer = PCA(n_components=2, random_state=42)
            X_2d = reducer.fit_transform(self.X_scaled)
            var_explained = reducer.explained_variance_ratio_
            xlabel = f'PC1 ({var_explained[0]:.1%} variance)'
            ylabel = f'PC2 ({var_explained[1]:.1%} variance)'
        elif method == 'tsne':
            reducer = TSNE(n_components=2, random_state=42, perplexity=30)
            X_2d = reducer.fit_transform(self.X_scaled)
            xlabel = 't-SNE Component 1'
            ylabel = 't-SNE Component 2'
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot clusters
        unique_labels = sorted(set(labels))
        colors = plt.cm.viridis(np.linspace(0, 1, len(unique_labels)))
        
        for i, cluster_id in enumerate(unique_labels):
            mask = labels == cluster_id
            label_text = f'Noise' if cluster_id == -1 else f'Cluster {cluster_id}'
            
            ax.scatter(
                X_2d[mask, 0], 
                X_2d[mask, 1],
                c=[colors[i]],
                label=label_text,
                s=100,
                alpha=0.6,
                edgecolors='k',
                linewidth=0.5
            )
        
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(f'Firm Clusters ({method.upper()} visualization)', 
                    fontsize=14, fontweight='bold')
        ax.legend(title='Strategic Groups', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        return fig
    
    def get_cluster_profiles(self, labels: np.ndarray) -> Dict:
        """
        Get detailed profiles for each cluster
        
        Args:
            labels: Cluster labels
        
        Returns:
            Dictionary with cluster profiles
        """
        self.df_clean['cluster'] = labels
        
        profiles = {}
        for cluster_id in sorted(set(labels)):
            cluster_data = self.df_clean[self.df_clean['cluster'] == cluster_id]
            
            profiles[cluster_id] = {
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(self.df_clean) * 100,
                'means': cluster_data[self.features].mean().to_dict(),
                'stds': cluster_data[self.features].std().to_dict()
            }
        
        return profiles


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    n_firms = 300
    
    # Simulate 3 strategic groups
    df_firms = pd.DataFrame({
        'firm_id': range(n_firms),
        'firm_name': [f'Company_{i:03d}' for i in range(n_firms)],
        'roa': np.concatenate([
            np.random.normal(0.10, 0.02, 100),  # High profitability
            np.random.normal(0.05, 0.02, 100),  # Medium profitability
            np.random.normal(0.02, 0.02, 100)   # Low profitability
        ]),
        'rd_intensity': np.concatenate([
            np.random.uniform(0.05, 0.15, 100),  # High R&D
            np.random.uniform(0.01, 0.05, 100),  # Medium R&D
            np.random.uniform(0, 0.02, 100)      # Low R&D
        ]),
        'leverage': np.concatenate([
            np.random.uniform(0.2, 0.4, 100),   # Low leverage
            np.random.uniform(0.4, 0.6, 100),   # Medium leverage
            np.random.uniform(0.6, 0.8, 100)    # High leverage
        ])
    })
    
    print("=" * 80)
    print("FIRM CLUSTERING EXAMPLE")
    print("=" * 80)
    print()
    
    # Initialize clusterer
    features = ['roa', 'rd_intensity', 'leverage']
    clusterer = FirmClusterer(df_firms, features=features)
    
    # Preprocess
    clusterer.preprocess()
    
    # Find optimal k
    print("Finding optimal number of clusters...")
    optimal_k, fig_elbow = clusterer.find_optimal_k(max_k=8)
    
    # Run K-means
    print(f"\nRunning K-means with k={optimal_k}...")
    labels = clusterer.kmeans(n_clusters=optimal_k)
    
    # Describe clusters
    print("\nCluster characteristics:")
    cluster_stats = clusterer.describe_clusters(labels)
    print(cluster_stats['mean'])
    
    # Visualize
    fig_clusters = clusterer.visualize_clusters(labels, method='pca')
    
    print("\n" + "=" * 80)
    print("Clustering completed! Check the generated plots.")
    print("=" * 80)
    
    plt.show()
