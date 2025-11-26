"""
centrality_calculator.py

Network Centrality Metrics Calculator

This module provides comprehensive calculation of network centrality metrics
for strategic management research, enabling analysis of firm positions,
power, and influence in various organizational networks.

Key Features:
- Multiple centrality measures (degree, betweenness, closeness, eigenvector)
- Weighted and unweighted networks
- Directed and undirected networks
- Temporal centrality evolution
- Industry-adjusted centrality scores

Common Applications in Strategic Research:
- Identifying central/powerful firms in industry networks
- Analyzing competitive positioning through network structure
- Knowledge broker identification
- Innovation diffusion patterns
- Resource access and control

Usage:
    from centrality_calculator import CentralityCalculator
    
    # Initialize calculator
    calc = CentralityCalculator(network)
    
    # Calculate all centrality metrics
    centrality_df = calc.calculate_all_centralities()
    
    # Identify top central firms
    top_firms = calc.get_top_central_firms(n=10, metric='betweenness')
    
    # Compare centralities across time
    evolution = calc.track_centrality_evolution(temporal_networks)

References:
- Freeman, L. C. (1978). "Centrality in social networks: Conceptual clarification."
  Social Networks, 1(3), 215-239.
- Bonacich, P. (1987). "Power and centrality: A family of measures."
  American Journal of Sociology, 92(5), 1170-1182.
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CentralityCalculator:
    """
    Calculate and analyze network centrality metrics
    
    Attributes:
        network: NetworkX graph object
        centralities: Dictionary of calculated centrality metrics
        is_directed: Whether network is directed
        is_weighted: Whether network has edge weights
    """
    
    def __init__(self, network: nx.Graph):
        """
        Initialize centrality calculator
        
        Args:
            network: NetworkX graph object
        """
        self.network = network
        self.centralities = {}
        self.is_directed = isinstance(network, nx.DiGraph)
        self.is_weighted = 'weight' in next(iter(network.edges(data=True)), [None, None, {}])[2]
        
        logger.info(f"CentralityCalculator initialized")
        logger.info(f"  Network type: {'Directed' if self.is_directed else 'Undirected'}")
        logger.info(f"  Weighted: {self.is_weighted}")
        logger.info(f"  Nodes: {network.number_of_nodes()}")
        logger.info(f"  Edges: {network.number_of_edges()}")
    
    # =========================================================================
    # Core Centrality Metrics
    # =========================================================================
    
    def calculate_degree_centrality(self, normalized: bool = True) -> Dict[str, float]:
        """
        Calculate degree centrality
        
        Degree centrality: Number of direct connections
        
        Args:
            normalized: Whether to normalize by (n-1)
        
        Returns:
            Dictionary mapping node to degree centrality
        """
        logger.info("Calculating degree centrality...")
        
        if self.is_directed:
            # For directed networks, calculate both in-degree and out-degree
            in_degree = dict(self.network.in_degree())
            out_degree = dict(self.network.out_degree())
            
            if normalized:
                n = self.network.number_of_nodes()
                in_degree = {k: v/(n-1) for k, v in in_degree.items()}
                out_degree = {k: v/(n-1) for k, v in out_degree.items()}
            
            self.centralities['in_degree_centrality'] = in_degree
            self.centralities['out_degree_centrality'] = out_degree
            
            # Total degree
            degree = {k: in_degree[k] + out_degree[k] for k in in_degree.keys()}
        else:
            degree = nx.degree_centrality(self.network) if normalized else dict(self.network.degree())
        
        self.centralities['degree_centrality'] = degree
        
        logger.info(f"  Mean: {np.mean(list(degree.values())):.4f}")
        logger.info(f"  Max: {max(degree.values()):.4f} ({max(degree, key=degree.get)})")
        
        return degree
    
    def calculate_betweenness_centrality(self, 
                                        normalized: bool = True,
                                        weight: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate betweenness centrality
        
        Betweenness centrality: Frequency of node appearing on shortest paths
        
        Args:
            normalized: Whether to normalize
            weight: Edge weight attribute (None for unweighted)
        
        Returns:
            Dictionary mapping node to betweenness centrality
        """
        logger.info("Calculating betweenness centrality...")
        
        betweenness = nx.betweenness_centrality(
            self.network,
            normalized=normalized,
            weight=weight
        )
        
        self.centralities['betweenness_centrality'] = betweenness
        
        logger.info(f"  Mean: {np.mean(list(betweenness.values())):.4f}")
        logger.info(f"  Max: {max(betweenness.values()):.4f} ({max(betweenness, key=betweenness.get)})")
        
        return betweenness
    
    def calculate_closeness_centrality(self, 
                                      weight: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate closeness centrality
        
        Closeness centrality: Inverse of average distance to all other nodes
        
        Args:
            weight: Edge weight attribute
        
        Returns:
            Dictionary mapping node to closeness centrality
        """
        logger.info("Calculating closeness centrality...")
        
        if nx.is_connected(self.network) or self.is_directed:
            closeness = nx.closeness_centrality(self.network, distance=weight)
        else:
            # For disconnected undirected graphs, use harmonic centrality
            logger.warning("  Network not connected, using harmonic centrality")
            closeness = nx.harmonic_centrality(self.network, distance=weight)
        
        self.centralities['closeness_centrality'] = closeness
        
        logger.info(f"  Mean: {np.mean(list(closeness.values())):.4f}")
        logger.info(f"  Max: {max(closeness.values()):.4f} ({max(closeness, key=closeness.get)})")
        
        return closeness
    
    def calculate_eigenvector_centrality(self, 
                                        max_iter: int = 1000,
                                        weight: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate eigenvector centrality
        
        Eigenvector centrality: Importance based on connections to important nodes
        
        Args:
            max_iter: Maximum iterations for convergence
            weight: Edge weight attribute
        
        Returns:
            Dictionary mapping node to eigenvector centrality
        """
        logger.info("Calculating eigenvector centrality...")
        
        try:
            eigenvector = nx.eigenvector_centrality(
                self.network,
                max_iter=max_iter,
                weight=weight
            )
            
            self.centralities['eigenvector_centrality'] = eigenvector
            
            logger.info(f"  Mean: {np.mean(list(eigenvector.values())):.4f}")
            logger.info(f"  Max: {max(eigenvector.values()):.4f} ({max(eigenvector, key=eigenvector.get)})")
            
            return eigenvector
        
        except nx.PowerIterationFailedConvergence:
            logger.error("  Eigenvector centrality failed to converge")
            return {}
    
    def calculate_pagerank(self, 
                          alpha: float = 0.85,
                          weight: Optional[str] = None) -> Dict[str, float]:
        """
        Calculate PageRank centrality
        
        PageRank: Google's algorithm, weighted eigenvector centrality
        
        Args:
            alpha: Damping parameter (default: 0.85)
            weight: Edge weight attribute
        
        Returns:
            Dictionary mapping node to PageRank score
        """
        logger.info("Calculating PageRank...")
        
        pagerank = nx.pagerank(self.network, alpha=alpha, weight=weight)
        
        self.centralities['pagerank'] = pagerank
        
        logger.info(f"  Mean: {np.mean(list(pagerank.values())):.4f}")
        logger.info(f"  Max: {max(pagerank.values()):.4f} ({max(pagerank, key=pagerank.get)})")
        
        return pagerank
    
    # =========================================================================
    # Comprehensive Analysis
    # =========================================================================
    
    def calculate_all_centralities(self, 
                                   include_pagerank: bool = True,
                                   weight: Optional[str] = None) -> pd.DataFrame:
        """
        Calculate all centrality metrics at once
        
        Args:
            include_pagerank: Whether to include PageRank
            weight: Edge weight attribute
        
        Returns:
            DataFrame with all centrality metrics
        """
        logger.info("Calculating all centrality metrics...")
        
        # Calculate each metric
        degree = self.calculate_degree_centrality()
        betweenness = self.calculate_betweenness_centrality(weight=weight)
        closeness = self.calculate_closeness_centrality(weight=weight)
        eigenvector = self.calculate_eigenvector_centrality(weight=weight)
        
        # Combine into DataFrame
        df = pd.DataFrame({
            'node': list(degree.keys()),
            'degree_centrality': list(degree.values()),
            'betweenness_centrality': list(betweenness.values()),
            'closeness_centrality': list(closeness.values())
        })
        
        if eigenvector:
            df['eigenvector_centrality'] = df['node'].map(eigenvector)
        
        if include_pagerank:
            pagerank = self.calculate_pagerank(weight=weight)
            df['pagerank'] = df['node'].map(pagerank)
        
        # Add directed network metrics
        if self.is_directed:
            df['in_degree_centrality'] = df['node'].map(self.centralities['in_degree_centrality'])
            df['out_degree_centrality'] = df['node'].map(self.centralities['out_degree_centrality'])
        
        logger.info(f"✓ All centralities calculated for {len(df)} nodes")
        
        return df
    
    def get_top_central_firms(self, 
                             n: int = 10,
                             metric: str = 'degree_centrality') -> pd.DataFrame:
        """
        Get top N central firms by specified metric
        
        Args:
            n: Number of top firms to return
            metric: Centrality metric to use for ranking
        
        Returns:
            DataFrame with top N firms
        """
        if metric not in self.centralities:
            raise ValueError(f"Metric '{metric}' not calculated. Run calculate_all_centralities() first.")
        
        centrality_dict = self.centralities[metric]
        
        # Sort and get top N
        sorted_firms = sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:n]
        
        df = pd.DataFrame(sorted_firms, columns=['firm_id', metric])
        df['rank'] = range(1, len(df) + 1)
        
        logger.info(f"Top {n} firms by {metric}:")
        for idx, row in df.head(5).iterrows():
            logger.info(f"  {row['rank']}. {row['firm_id']}: {row[metric]:.4f}")
        
        return df
    
    def compare_centralities(self) -> pd.DataFrame:
        """
        Compare correlations between different centrality metrics
        
        Returns:
            Correlation matrix of centrality metrics
        """
        logger.info("Comparing centrality metrics...")
        
        if not self.centralities:
            raise ValueError("No centralities calculated. Run calculate_all_centralities() first.")
        
        # Create DataFrame
        df = pd.DataFrame(self.centralities)
        
        # Calculate correlations
        corr = df.corr()
        
        logger.info("Centrality correlations:")
        logger.info(f"\n{corr.round(3)}")
        
        return corr
    
    # =========================================================================
    # Temporal Analysis
    # =========================================================================
    
    def track_centrality_evolution(self,
                                   temporal_networks: Dict[int, nx.Graph],
                                   metric: str = 'degree_centrality') -> pd.DataFrame:
        """
        Track how centrality evolves over time
        
        Args:
            temporal_networks: Dictionary mapping time period to network
            metric: Centrality metric to track
        
        Returns:
            DataFrame with centrality evolution
        """
        logger.info(f"Tracking {metric} evolution over time...")
        
        evolution_data = []
        
        for period, G in sorted(temporal_networks.items()):
            calc = CentralityCalculator(G)
            
            if metric == 'degree_centrality':
                centrality = calc.calculate_degree_centrality()
            elif metric == 'betweenness_centrality':
                centrality = calc.calculate_betweenness_centrality()
            elif metric == 'closeness_centrality':
                centrality = calc.calculate_closeness_centrality()
            elif metric == 'eigenvector_centrality':
                centrality = calc.calculate_eigenvector_centrality()
            else:
                raise ValueError(f"Unknown metric: {metric}")
            
            for node, value in centrality.items():
                evolution_data.append({
                    'period': period,
                    'node': node,
                    metric: value
                })
        
        df = pd.DataFrame(evolution_data)
        
        logger.info(f"✓ Tracked {len(df['node'].unique())} nodes over {len(temporal_networks)} periods")
        
        return df
    
    # =========================================================================
    # Industry-Adjusted Centrality
    # =========================================================================
    
    def calculate_industry_adjusted_centrality(self,
                                              node_industries: Dict[str, str],
                                              metric: str = 'degree_centrality') -> pd.DataFrame:
        """
        Calculate industry-adjusted centrality scores
        
        Args:
            node_industries: Dictionary mapping node to industry
            metric: Centrality metric to adjust
        
        Returns:
            DataFrame with adjusted centrality scores
        """
        logger.info(f"Calculating industry-adjusted {metric}...")
        
        if metric not in self.centralities:
            raise ValueError(f"Metric '{metric}' not calculated.")
        
        centrality = self.centralities[metric]
        
        # Create DataFrame
        df = pd.DataFrame({
            'node': list(centrality.keys()),
            metric: list(centrality.values())
        })
        
        df['industry'] = df['node'].map(node_industries)
        
        # Calculate industry mean and std
        industry_stats = df.groupby('industry')[metric].agg(['mean', 'std'])
        
        # Adjust centrality
        df['industry_mean'] = df['industry'].map(industry_stats['mean'])
        df['industry_std'] = df['industry'].map(industry_stats['std'])
        
        df[f'{metric}_adjusted'] = (df[metric] - df['industry_mean']) / df['industry_std']
        
        logger.info(f"✓ Adjusted centrality calculated for {len(df)} nodes")
        
        return df
    
    # =========================================================================
    # Visualization
    # =========================================================================
    
    def plot_centrality_distribution(self, 
                                    metric: str = 'degree_centrality',
                                    save_path: Optional[Path] = None) -> plt.Figure:
        """
        Plot distribution of centrality metric
        
        Args:
            metric: Centrality metric to plot
            save_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        if metric not in self.centralities:
            raise ValueError(f"Metric '{metric}' not calculated.")
        
        centrality = self.centralities[metric]
        values = list(centrality.values())
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Histogram
        axes[0].hist(values, bins=30, edgecolor='black', alpha=0.7)
        axes[0].axvline(np.mean(values), color='red', linestyle='--', 
                       label=f'Mean: {np.mean(values):.3f}')
        axes[0].set_xlabel(metric.replace('_', ' ').title())
        axes[0].set_ylabel('Frequency')
        axes[0].set_title(f'Distribution of {metric.replace("_", " ").title()}')
        axes[0].legend()
        
        # Box plot
        axes[1].boxplot(values, vert=True)
        axes[1].set_ylabel(metric.replace('_', ' ').title())
        axes[1].set_title('Distribution Summary')
        axes[1].set_xticks([])
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  Figure saved: {save_path}")
        
        return fig
    
    def plot_centrality_comparison(self, 
                                  metrics: List[str] = None,
                                  save_path: Optional[Path] = None) -> plt.Figure:
        """
        Plot comparison of multiple centrality metrics
        
        Args:
            metrics: List of metrics to compare (None for all)
            save_path: Optional path to save figure
        
        Returns:
            Matplotlib figure
        """
        if metrics is None:
            metrics = list(self.centralities.keys())
        
        # Create DataFrame
        df = pd.DataFrame(self.centralities)
        
        # Normalize each metric to [0, 1] for comparison
        df_norm = (df - df.min()) / (df.max() - df.min())
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for metric in metrics:
            if metric in df_norm.columns:
                df_norm[metric].hist(bins=30, alpha=0.5, label=metric.replace('_', ' ').title())
        
        ax.set_xlabel('Normalized Centrality')
        ax.set_ylabel('Frequency')
        ax.set_title('Comparison of Centrality Metrics')
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  Figure saved: {save_path}")
        
        return fig
    
    # =========================================================================
    # Export
    # =========================================================================
    
    def export_centralities(self, filepath: Path):
        """
        Export all centrality metrics to CSV
        
        Args:
            filepath: Output file path
        """
        df = self.calculate_all_centralities()
        df.to_csv(filepath, index=False)
        logger.info(f"✓ Centralities exported: {filepath}")


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CENTRALITY CALCULATOR EXAMPLE")
    print("=" * 80)
    
    # Generate sample network
    np.random.seed(42)
    
    # Create network with different structures
    G = nx.Graph()
    
    # Add 50 nodes
    nodes = [f'FIRM{i:03d}' for i in range(1, 51)]
    G.add_nodes_from(nodes)
    
    # Add edges with different patterns
    # Core firms with high connectivity
    core_firms = nodes[:5]
    for i, firm1 in enumerate(core_firms):
        for firm2 in core_firms[i+1:]:
            G.add_edge(firm1, firm2)
    
    # Peripheral firms
    for firm in nodes[5:]:
        # Connect to random core firm
        core = np.random.choice(core_firms)
        G.add_edge(firm, core)
        
        # Occasional connections to other peripheral firms
        if np.random.random() < 0.2:
            other = np.random.choice([f for f in nodes[5:] if f != firm])
            G.add_edge(firm, other)
    
    print(f"\nNetwork: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Initialize calculator
    calc = CentralityCalculator(G)
    
    # Calculate all centralities
    centralities = calc.calculate_all_centralities()
    
    print("\n" + "=" * 80)
    print("TOP 10 FIRMS BY DEGREE CENTRALITY")
    print("=" * 80)
    top_degree = calc.get_top_central_firms(n=10, metric='degree_centrality')
    print(top_degree.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("TOP 10 FIRMS BY BETWEENNESS CENTRALITY")
    print("=" * 80)
    top_betweenness = calc.get_top_central_firms(n=10, metric='betweenness_centrality')
    print(top_betweenness.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("CENTRALITY CORRELATIONS")
    print("=" * 80)
    corr = calc.compare_centralities()
    print(corr.round(3))
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)
