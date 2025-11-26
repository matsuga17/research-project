"""
anomaly_detection.py

Anomaly Detection for Strategic Management Research

This module implements anomaly detection algorithms to identify unusual firms
or observations that deviate significantly from normal patterns.

Common applications:
- Fraud/accounting irregularity detection
- Outlier firm identification
- Strategic deviation detection
- Risk assessment

Usage:
    from anomaly_detection import AnomalyDetector
    
    detector = AnomalyDetector(df, features=features)
    anomalies = detector.detect_isolation_forest()
    scores = detector.anomaly_scores()
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Anomaly detection for firm-level data
    
    Attributes:
        df: Input DataFrame
        features: Feature variables for anomaly detection
        anomaly_labels: Anomaly labels (-1: anomaly, 1: normal)
        anomaly_scores: Anomaly scores (higher = more anomalous)
    """
    
    def __init__(self, df: pd.DataFrame,
                 features: List[str] = None,
                 firm_id: str = 'firm_id'):
        """
        Initialize anomaly detector
        
        Args:
            df: DataFrame with features
            features: List of feature names (if None, use all numeric)
            firm_id: Firm identifier column
        """
        self.df = df.copy()
        self.firm_id = firm_id
        
        if features is None:
            self.features = [col for col in df.select_dtypes(include=[np.number]).columns
                           if col != firm_id]
        else:
            self.features = features
        
        self.anomaly_labels = None
        self.anomaly_scores = None
        
        logger.info(f"AnomalyDetector initialized:")
        logger.info(f"  Features: {len(self.features)}")
        logger.info(f"  Observations: {len(df)}")
    
    def detect_isolation_forest(self, contamination: float = 0.1,
                                n_estimators: int = 100,
                                random_state: int = 42) -> pd.DataFrame:
        """
        Detect anomalies using Isolation Forest
        
        Args:
            contamination: Expected proportion of anomalies
            n_estimators: Number of trees
            random_state: Random seed
        
        Returns:
            DataFrame with anomaly labels and scores
        """
        from sklearn.ensemble import IsolationForest
        
        logger.info(f"\nDetecting anomalies using Isolation Forest...")
        logger.info(f"  Expected contamination: {contamination*100:.1f}%")
        
        # Prepare data
        df_clean = self.df[self.features].dropna()
        
        # Fit model
        model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1
        )
        
        # Predict
        self.anomaly_labels = model.fit_predict(df_clean)
        self.anomaly_scores = model.score_samples(df_clean)
        
        # Create results DataFrame
        results = df_clean.copy()
        results['anomaly_label'] = self.anomaly_labels
        results['anomaly_score'] = self.anomaly_scores
        
        n_anomalies = (self.anomaly_labels == -1).sum()
        pct_anomalies = n_anomalies / len(self.anomaly_labels) * 100
        
        logger.info(f"  ✓ Detection completed")
        logger.info(f"  Anomalies detected: {n_anomalies} ({pct_anomalies:.1f}%)")
        
        return results
    
    def detect_local_outlier_factor(self, contamination: float = 0.1,
                                   n_neighbors: int = 20) -> pd.DataFrame:
        """
        Detect anomalies using Local Outlier Factor (LOF)
        
        Args:
            contamination: Expected proportion of anomalies
            n_neighbors: Number of neighbors for LOF calculation
        
        Returns:
            DataFrame with anomaly labels and scores
        """
        from sklearn.neighbors import LocalOutlierFactor
        
        logger.info(f"\nDetecting anomalies using Local Outlier Factor...")
        logger.info(f"  Neighbors: {n_neighbors}")
        logger.info(f"  Expected contamination: {contamination*100:.1f}%")
        
        # Prepare data
        df_clean = self.df[self.features].dropna()
        
        # Fit model
        model = LocalOutlierFactor(
            contamination=contamination,
            n_neighbors=n_neighbors,
            n_jobs=-1
        )
        
        # Predict
        self.anomaly_labels = model.fit_predict(df_clean)
        self.anomaly_scores = model.negative_outlier_factor_
        
        # Create results DataFrame
        results = df_clean.copy()
        results['anomaly_label'] = self.anomaly_labels
        results['anomaly_score'] = self.anomaly_scores
        
        n_anomalies = (self.anomaly_labels == -1).sum()
        pct_anomalies = n_anomalies / len(self.anomaly_labels) * 100
        
        logger.info(f"  ✓ Detection completed")
        logger.info(f"  Anomalies detected: {n_anomalies} ({pct_anomalies:.1f}%)")
        
        return results
    
    def detect_statistical(self, method: str = 'zscore',
                         threshold: float = 3.0) -> pd.DataFrame:
        """
        Detect anomalies using statistical methods
        
        Args:
            method: Method to use ('zscore', 'iqr', 'mahalanobis')
            threshold: Threshold for anomaly detection
        
        Returns:
            DataFrame with anomaly labels
        """
        logger.info(f"\nDetecting anomalies using {method} method...")
        logger.info(f"  Threshold: {threshold}")
        
        # Prepare data
        df_clean = self.df[self.features].dropna()
        
        if method == 'zscore':
            # Z-score method
            z_scores = np.abs((df_clean - df_clean.mean()) / df_clean.std())
            self.anomaly_labels = (z_scores > threshold).any(axis=1).astype(int)
            self.anomaly_labels = np.where(self.anomaly_labels == 1, -1, 1)
            
        elif method == 'iqr':
            # IQR method
            Q1 = df_clean.quantile(0.25)
            Q3 = df_clean.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = ((df_clean < lower_bound) | (df_clean > upper_bound)).any(axis=1)
            self.anomaly_labels = np.where(outliers, -1, 1)
            
        elif method == 'mahalanobis':
            # Mahalanobis distance
            from scipy.spatial.distance import mahalanobis
            
            mean = df_clean.mean().values
            cov = df_clean.cov().values
            
            try:
                inv_cov = np.linalg.inv(cov)
                distances = df_clean.apply(
                    lambda row: mahalanobis(row, mean, inv_cov),
                    axis=1
                )
                
                self.anomaly_scores = distances.values
                self.anomaly_labels = np.where(distances > threshold, -1, 1)
            except np.linalg.LinAlgError:
                logger.error("Covariance matrix is singular. Using Z-score instead.")
                return self.detect_statistical(method='zscore', threshold=threshold)
        else:
            logger.error(f"Unknown method: {method}")
            return None
        
        # Create results DataFrame
        results = df_clean.copy()
        results['anomaly_label'] = self.anomaly_labels
        if self.anomaly_scores is not None:
            results['anomaly_score'] = self.anomaly_scores
        
        n_anomalies = (self.anomaly_labels == -1).sum()
        pct_anomalies = n_anomalies / len(self.anomaly_labels) * 100
        
        logger.info(f"  ✓ Detection completed")
        logger.info(f"  Anomalies detected: {n_anomalies} ({pct_anomalies:.1f}%)")
        
        return results
    
    def get_anomalies(self, results: pd.DataFrame = None,
                     top_n: int = None) -> pd.DataFrame:
        """
        Get anomalous observations
        
        Args:
            results: Results DataFrame from detection method
            top_n: Number of top anomalies to return (by score)
        
        Returns:
            DataFrame with anomalies
        """
        if results is None:
            logger.error("No results available. Run a detection method first.")
            return None
        
        anomalies = results[results['anomaly_label'] == -1].copy()
        
        if top_n is not None and 'anomaly_score' in anomalies.columns:
            # Sort by anomaly score (ascending for Isolation Forest, descending for LOF)
            if anomalies['anomaly_score'].mean() < 0:
                # LOF scores are negative
                anomalies = anomalies.nsmallest(top_n, 'anomaly_score')
            else:
                # Isolation Forest or Mahalanobis scores
                anomalies = anomalies.nlargest(top_n, 'anomaly_score')
        
        return anomalies
    
    def visualize_anomalies(self, results: pd.DataFrame,
                          features_to_plot: List[str] = None,
                          save_path: str = None) -> 'matplotlib.figure.Figure':
        """
        Visualize anomalies using scatter plot
        
        Args:
            results: Results DataFrame from detection method
            features_to_plot: Two features for scatter plot (default: first two)
            save_path: Path to save figure
        
        Returns:
            matplotlib Figure
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logger.error("matplotlib not installed")
            return None
        
        if features_to_plot is None:
            features_to_plot = self.features[:2]
        
        if len(features_to_plot) < 2:
            logger.error("Need at least 2 features for visualization")
            return None
        
        logger.info(f"\nVisualizing anomalies using {features_to_plot[0]} and {features_to_plot[1]}...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot normal points
        normal = results[results['anomaly_label'] == 1]
        ax.scatter(normal[features_to_plot[0]], normal[features_to_plot[1]],
                  c='blue', alpha=0.5, s=30, label='Normal')
        
        # Plot anomalies
        anomalies = results[results['anomaly_label'] == -1]
        ax.scatter(anomalies[features_to_plot[0]], anomalies[features_to_plot[1]],
                  c='red', alpha=0.8, s=60, marker='x', label='Anomaly')
        
        ax.set_xlabel(features_to_plot[0].replace('_', ' ').title())
        ax.set_ylabel(features_to_plot[1].replace('_', ' ').title())
        ax.set_title('Anomaly Detection Results')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Visualization saved: {save_path}")
        
        return fig
    
    def compare_methods(self) -> pd.DataFrame:
        """
        Compare multiple detection methods
        
        Returns:
            DataFrame comparing methods
        """
        logger.info("\nComparing detection methods...")
        
        methods = []
        
        # Isolation Forest
        logger.info("\n1. Isolation Forest")
        results_if = self.detect_isolation_forest(contamination=0.1)
        methods.append({
            'method': 'Isolation Forest',
            'n_anomalies': (results_if['anomaly_label'] == -1).sum(),
            'pct_anomalies': (results_if['anomaly_label'] == -1).sum() / len(results_if) * 100
        })
        
        # LOF
        logger.info("\n2. Local Outlier Factor")
        results_lof = self.detect_local_outlier_factor(contamination=0.1)
        methods.append({
            'method': 'Local Outlier Factor',
            'n_anomalies': (results_lof['anomaly_label'] == -1).sum(),
            'pct_anomalies': (results_lof['anomaly_label'] == -1).sum() / len(results_lof) * 100
        })
        
        # Z-score
        logger.info("\n3. Z-score")
        results_z = self.detect_statistical(method='zscore', threshold=3.0)
        methods.append({
            'method': 'Z-score (threshold=3)',
            'n_anomalies': (results_z['anomaly_label'] == -1).sum(),
            'pct_anomalies': (results_z['anomaly_label'] == -1).sum() / len(results_z) * 100
        })
        
        comparison_df = pd.DataFrame(methods)
        
        logger.info("\n" + "="*60)
        logger.info("Method Comparison")
        logger.info("="*60)
        logger.info(comparison_df.to_string(index=False))
        
        return comparison_df


# Example usage
if __name__ == "__main__":
    # Generate sample data with some anomalies
    np.random.seed(42)
    n = 1000
    
    # Normal firms
    normal_roa = np.random.normal(0.05, 0.02, int(n*0.9))
    normal_leverage = np.random.normal(0.5, 0.15, int(n*0.9))
    normal_growth = np.random.normal(0.10, 0.10, int(n*0.9))
    
    # Anomalous firms (extreme values)
    anomaly_roa = np.random.choice([-0.2, 0.3], int(n*0.1))
    anomaly_leverage = np.random.choice([0.1, 0.95], int(n*0.1))
    anomaly_growth = np.random.choice([-0.5, 0.8], int(n*0.1))
    
    # Combine
    roa = np.concatenate([normal_roa, anomaly_roa])
    leverage = np.concatenate([normal_leverage, anomaly_leverage])
    growth = np.concatenate([normal_growth, anomaly_growth])
    
    df = pd.DataFrame({
        'firm_id': range(n),
        'roa': roa,
        'leverage': leverage,
        'sales_growth': growth
    })
    
    logger.info("="*60)
    logger.info("Anomaly Detection Example")
    logger.info("="*60)
    
    # Create detector
    detector = AnomalyDetector(df, features=['roa', 'leverage', 'sales_growth'])
    
    # Detect using Isolation Forest
    results = detector.detect_isolation_forest(contamination=0.1)
    
    # Get top anomalies
    anomalies = detector.get_anomalies(results, top_n=10)
    logger.info("\nTop 10 Anomalies:")
    print(anomalies[['firm_id', 'roa', 'leverage', 'sales_growth', 'anomaly_score']])
    
    # Visualize
    fig = detector.visualize_anomalies(results, features_to_plot=['roa', 'leverage'])
    if fig:
        import matplotlib.pyplot as plt
        plt.show()
    
    # Compare methods
    comparison = detector.compare_methods()
    
    logger.info("\n" + "="*60)
    logger.info("Anomaly detection completed!")
    logger.info("="*60)
