"""
dimensionality_reduction.py

Dimensionality Reduction for Strategic Management Research

This module implements techniques to reduce high-dimensional data while
preserving important patterns and structures.

Common applications:
- Financial indicator summarization (PCA)
- Strategy space visualization (t-SNE, UMAP)
- Multicollinearity reduction
- Feature engineering for modeling

Usage:
    from dimensionality_reduction import DimensionalityReducer
    
    reducer = DimensionalityReducer(df, features=features)
    X_reduced = reducer.apply_pca(n_components=3)
    reducer.visualize_2d()
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DimensionalityReducer:
    """
    Dimensionality reduction for high-dimensional firm data
    
    Attributes:
        df: Input DataFrame
        features: Feature variables
        X: Feature matrix
        X_reduced: Reduced feature matrix
        reducer: Fitted reduction model
    """
    
    def __init__(self, df: pd.DataFrame,
                 features: List[str] = None):
        """
        Initialize dimensionality reducer
        
        Args:
            df: DataFrame with features
            features: List of feature names (if None, use all numeric)
        """
        self.df = df.copy()
        
        if features is None:
            self.features = df.select_dtypes(include=[np.number]).columns.tolist()
        else:
            self.features = features
        
        # Remove missing values
        self.df = self.df[self.features].dropna()
        self.X = self.df[self.features].values
        
        self.X_reduced = None
        self.reducer = None
        
        logger.info(f"DimensionalityReducer initialized:")
        logger.info(f"  Features: {len(self.features)}")
        logger.info(f"  Observations: {len(self.df)}")
    
    def apply_pca(self, n_components: int = 2,
                 standardize: bool = True) -> np.ndarray:
        """
        Apply Principal Component Analysis (PCA)
        
        Args:
            n_components: Number of components to keep
            standardize: Whether to standardize features first
        
        Returns:
            Reduced feature matrix
        """
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        logger.info(f"\nApplying PCA...")
        logger.info(f"  Components: {n_components}")
        logger.info(f"  Standardize: {standardize}")
        
        # Standardize if requested
        if standardize:
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(self.X)
        else:
            X_scaled = self.X
        
        # Fit PCA
        self.reducer = PCA(n_components=n_components, random_state=42)
        self.X_reduced = self.reducer.fit_transform(X_scaled)
        
        # Log explained variance
        explained_var = self.reducer.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        logger.info(f"\n  Explained variance by component:")
        for i, (var, cum_var) in enumerate(zip(explained_var, cumulative_var)):
            logger.info(f"    PC{i+1}: {var*100:.1f}% (cumulative: {cum_var*100:.1f}%)")
        
        logger.info(f"  ✓ PCA completed")
        
        return self.X_reduced
    
    def get_loadings(self) -> pd.DataFrame:
        """
        Get PCA loadings (component-feature relationships)
        
        Returns:
            DataFrame with loadings
        """
        if self.reducer is None or not hasattr(self.reducer, 'components_'):
            logger.error("PCA not fitted. Run apply_pca() first.")
            return None
        
        loadings = pd.DataFrame(
            self.reducer.components_.T,
            columns=[f'PC{i+1}' for i in range(self.reducer.n_components_)],
            index=self.features
        )
        
        logger.info("\nPCA Loadings:")
        logger.info(loadings)
        
        return loadings
    
    def apply_tsne(self, n_components: int = 2,
                  perplexity: float = 30.0,
                  n_iter: int = 1000) -> np.ndarray:
        """
        Apply t-SNE for visualization
        
        Args:
            n_components: Number of dimensions (usually 2 or 3)
            perplexity: Perplexity parameter (5-50)
            n_iter: Number of iterations
        
        Returns:
            Reduced feature matrix
        """
        from sklearn.manifold import TSNE
        from sklearn.preprocessing import StandardScaler
        
        logger.info(f"\nApplying t-SNE...")
        logger.info(f"  Components: {n_components}")
        logger.info(f"  Perplexity: {perplexity}")
        logger.info(f"  Iterations: {n_iter}")
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X)
        
        # Fit t-SNE
        self.reducer = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            n_iter=n_iter,
            random_state=42
        )
        
        self.X_reduced = self.reducer.fit_transform(X_scaled)
        
        logger.info(f"  ✓ t-SNE completed")
        
        return self.X_reduced
    
    def apply_umap(self, n_components: int = 2,
                  n_neighbors: int = 15,
                  min_dist: float = 0.1) -> np.ndarray:
        """
        Apply UMAP for visualization
        
        Args:
            n_components: Number of dimensions
            n_neighbors: Number of neighbors
            min_dist: Minimum distance between points
        
        Returns:
            Reduced feature matrix
        """
        try:
            import umap
        except ImportError:
            logger.error("umap-learn not installed. Install: pip install umap-learn")
            return None
        
        from sklearn.preprocessing import StandardScaler
        
        logger.info(f"\nApplying UMAP...")
        logger.info(f"  Components: {n_components}")
        logger.info(f"  Neighbors: {n_neighbors}")
        logger.info(f"  Min distance: {min_dist}")
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X)
        
        # Fit UMAP
        self.reducer = umap.UMAP(
            n_components=n_components,
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            random_state=42
        )
        
        self.X_reduced = self.reducer.fit_transform(X_scaled)
        
        logger.info(f"  ✓ UMAP completed")
        
        return self.X_reduced
    
    def visualize_2d(self, labels: Optional[np.ndarray] = None,
                    title: str = 'Dimensionality Reduction',
                    save_path: str = None) -> 'matplotlib.figure.Figure':
        """
        Visualize 2D reduced space
        
        Args:
            labels: Optional labels for coloring points
            title: Plot title
            save_path: Path to save figure
        
        Returns:
            matplotlib Figure
        """
        if self.X_reduced is None:
            logger.error("No reduced data available. Run a reduction method first.")
            return None
        
        if self.X_reduced.shape[1] < 2:
            logger.error("Need at least 2 dimensions for visualization")
            return None
        
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.error("matplotlib not installed")
            return None
        
        logger.info(f"\nCreating 2D visualization...")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if labels is not None:
            # Color by labels
            scatter = ax.scatter(
                self.X_reduced[:, 0],
                self.X_reduced[:, 1],
                c=labels,
                cmap='viridis',
                alpha=0.6,
                s=30
            )
            plt.colorbar(scatter, ax=ax, label='Label')
        else:
            # No labels
            ax.scatter(
                self.X_reduced[:, 0],
                self.X_reduced[:, 1],
                alpha=0.6,
                s=30,
                color='steelblue'
            )
        
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Visualization saved: {save_path}")
        
        return fig
    
    def visualize_3d(self, labels: Optional[np.ndarray] = None,
                    title: str = 'Dimensionality Reduction (3D)',
                    save_path: str = None) -> 'matplotlib.figure.Figure':
        """
        Visualize 3D reduced space
        
        Args:
            labels: Optional labels for coloring points
            title: Plot title
            save_path: Path to save figure
        
        Returns:
            matplotlib Figure
        """
        if self.X_reduced is None:
            logger.error("No reduced data available. Run a reduction method first.")
            return None
        
        if self.X_reduced.shape[1] < 3:
            logger.error("Need at least 3 dimensions for 3D visualization")
            return None
        
        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
        except ImportError:
            logger.error("matplotlib not installed")
            return None
        
        logger.info(f"\nCreating 3D visualization...")
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        if labels is not None:
            scatter = ax.scatter(
                self.X_reduced[:, 0],
                self.X_reduced[:, 1],
                self.X_reduced[:, 2],
                c=labels,
                cmap='viridis',
                alpha=0.6,
                s=30
            )
            fig.colorbar(scatter, ax=ax, label='Label', pad=0.1)
        else:
            ax.scatter(
                self.X_reduced[:, 0],
                self.X_reduced[:, 1],
                self.X_reduced[:, 2],
                alpha=0.6,
                s=30,
                color='steelblue'
            )
        
        ax.set_xlabel('Component 1')
        ax.set_ylabel('Component 2')
        ax.set_zlabel('Component 3')
        ax.set_title(title)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Visualization saved: {save_path}")
        
        return fig
    
    def scree_plot(self, max_components: int = 10) -> 'matplotlib.figure.Figure':
        """
        Create scree plot for PCA
        
        Args:
            max_components: Maximum number of components to test
        
        Returns:
            matplotlib Figure
        """
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.error("matplotlib not installed")
            return None
        
        logger.info(f"\nCreating scree plot (max components: {max_components})...")
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(self.X)
        
        # Fit PCA with all components
        pca = PCA(n_components=min(max_components, len(self.features)))
        pca.fit(X_scaled)
        
        explained_var = pca.explained_variance_ratio_
        cumulative_var = np.cumsum(explained_var)
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scree plot
        ax1.plot(range(1, len(explained_var) + 1), explained_var, 'bo-')
        ax1.set_xlabel('Principal Component')
        ax1.set_ylabel('Explained Variance Ratio')
        ax1.set_title('Scree Plot')
        ax1.grid(True, alpha=0.3)
        
        # Cumulative variance
        ax2.plot(range(1, len(cumulative_var) + 1), cumulative_var, 'ro-')
        ax2.axhline(y=0.8, color='g', linestyle='--', label='80% threshold')
        ax2.axhline(y=0.9, color='b', linestyle='--', label='90% threshold')
        ax2.set_xlabel('Number of Components')
        ax2.set_ylabel('Cumulative Explained Variance')
        ax2.set_title('Cumulative Variance Explained')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        logger.info(f"  ✓ Scree plot created")
        
        return fig


# Example usage
if __name__ == "__main__":
    # Generate sample data with high-dimensional features
    np.random.seed(42)
    n = 500
    
    # Create correlated financial features
    base_performance = np.random.normal(0, 1, n)
    
    features_dict = {
        'roa': base_performance * 0.05 + np.random.normal(0, 0.01, n),
        'roe': base_performance * 0.08 + np.random.normal(0, 0.02, n),
        'profit_margin': base_performance * 0.10 + np.random.normal(0, 0.03, n),
        'asset_turnover': base_performance * 0.5 + np.random.normal(1, 0.2, n),
        'current_ratio': -base_performance * 0.3 + np.random.normal(1.5, 0.5, n),
        'quick_ratio': -base_performance * 0.2 + np.random.normal(1.2, 0.4, n),
        'leverage': -base_performance * 0.1 + np.random.normal(0.5, 0.15, n),
        'interest_coverage': base_performance * 2 + np.random.normal(5, 2, n),
    }
    
    df = pd.DataFrame(features_dict)
    df['firm_id'] = range(n)
    
    logger.info("="*60)
    logger.info("Dimensionality Reduction Example")
    logger.info("="*60)
    
    # Create reducer
    reducer = DimensionalityReducer(df, features=list(features_dict.keys()))
    
    # PCA
    X_pca = reducer.apply_pca(n_components=3)
    loadings = reducer.get_loadings()
    
    # Scree plot
    fig_scree = reducer.scree_plot(max_components=8)
    
    # Visualize 2D
    fig_2d = reducer.visualize_2d(title='PCA Visualization')
    
    # t-SNE
    X_tsne = reducer.apply_tsne(n_components=2, perplexity=30)
    fig_tsne = reducer.visualize_2d(title='t-SNE Visualization')
    
    if fig_2d and fig_tsne:
        import matplotlib.pyplot as plt
        plt.show()
    
    logger.info("\n" + "="*60)
    logger.info("Dimensionality reduction completed!")
    logger.info("="*60)
