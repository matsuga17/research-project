"""
network_visualizer.py

Network Visualization for Strategic Research

This module provides publication-quality network visualization capabilities
for strategic management research, with support for various layout algorithms,
node/edge styling, and interactive visualizations.

Key Features:
- Multiple layout algorithms (spring, circular, hierarchical)
- Node sizing by centrality or attributes
- Edge weighting and coloring
- Community detection visualization
- Temporal network animation
- Interactive HTML visualizations

Common Applications in Strategic Research:
- Visualizing industry structure and competitive dynamics
- Illustrating alliance networks and partnerships
- Showing knowledge flows and spillovers
- Presenting board interlocks
- Demonstrating network evolution over time

Usage:
    from network_visualizer import NetworkVisualizer
    
    # Initialize visualizer
    viz = NetworkVisualizer(network)
    
    # Basic visualization
    viz.plot_network(node_size_by='degree_centrality')
    
    # Community visualization
    viz.plot_communities()
    
    # Save publication-quality figure
    viz.export_figure('network.pdf', dpi=300)

References:
- Borgatti, S. P., Everett, M. G., & Johnson, J. C. (2018). 
  Analyzing Social Networks. SAGE Publications.
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.colors import Normalize
import warnings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkVisualizer:
    """
    Visualize networks for strategic research
    
    Attributes:
        network: NetworkX graph object
        pos: Node positions (layout)
        fig: Current matplotlib figure
        ax: Current matplotlib axes
    """
    
    def __init__(self, network: nx.Graph):
        """
        Initialize network visualizer
        
        Args:
            network: NetworkX graph object
        """
        self.network = network
        self.pos = None
        self.fig = None
        self.ax = None
        
        logger.info(f"NetworkVisualizer initialized")
        logger.info(f"  Nodes: {network.number_of_nodes()}")
        logger.info(f"  Edges: {network.number_of_edges()}")
    
    # =========================================================================
    # Layout Algorithms
    # =========================================================================
    
    def compute_layout(self, 
                      layout: str = 'spring',
                      **kwargs) -> Dict[str, Tuple[float, float]]:
        """
        Compute node positions using specified layout algorithm
        
        Args:
            layout: Layout algorithm ('spring', 'circular', 'kamada_kawai', 
                   'random', 'shell', 'spectral')
            **kwargs: Additional arguments for layout algorithm
        
        Returns:
            Dictionary mapping node to (x, y) position
        """
        logger.info(f"Computing {layout} layout...")
        
        if layout == 'spring':
            self.pos = nx.spring_layout(self.network, **kwargs)
        elif layout == 'circular':
            self.pos = nx.circular_layout(self.network, **kwargs)
        elif layout == 'kamada_kawai':
            self.pos = nx.kamada_kawai_layout(self.network, **kwargs)
        elif layout == 'random':
            self.pos = nx.random_layout(self.network, **kwargs)
        elif layout == 'shell':
            self.pos = nx.shell_layout(self.network, **kwargs)
        elif layout == 'spectral':
            self.pos = nx.spectral_layout(self.network, **kwargs)
        else:
            raise ValueError(f"Unknown layout: {layout}")
        
        logger.info(f"  Layout computed for {len(self.pos)} nodes")
        
        return self.pos
    
    # =========================================================================
    # Basic Visualization
    # =========================================================================
    
    def plot_network(self,
                    layout: str = 'spring',
                    node_size_by: Optional[str] = None,
                    node_color_by: Optional[str] = None,
                    edge_width_by: Optional[str] = None,
                    figsize: Tuple[int, int] = (12, 10),
                    node_size_scale: float = 300,
                    show_labels: bool = True,
                    label_font_size: int = 8,
                    title: Optional[str] = None) -> plt.Figure:
        """
        Create basic network visualization
        
        Args:
            layout: Layout algorithm
            node_size_by: Node attribute for sizing (e.g., 'degree_centrality')
            node_color_by: Node attribute for coloring
            edge_width_by: Edge attribute for width
            figsize: Figure size
            node_size_scale: Scaling factor for node sizes
            show_labels: Whether to show node labels
            label_font_size: Font size for labels
            title: Optional plot title
        
        Returns:
            Matplotlib figure
        """
        logger.info("Creating network visualization...")
        
        # Compute layout if not already done
        if self.pos is None:
            self.compute_layout(layout)
        
        # Create figure
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Node sizes
        if node_size_by:
            node_sizes = self._get_node_attribute(node_size_by)
            # Normalize and scale
            node_sizes = np.array(node_sizes)
            node_sizes = (node_sizes - node_sizes.min()) / (node_sizes.max() - node_sizes.min() + 1e-10)
            node_sizes = node_sizes * node_size_scale + 100  # Min size 100
        else:
            node_sizes = 300
        
        # Node colors
        if node_color_by:
            node_colors = self._get_node_attribute(node_color_by)
            # Check if categorical or numeric
            if isinstance(node_colors[0], str):
                # Categorical
                unique_colors = list(set(node_colors))
                color_map = {c: i for i, c in enumerate(unique_colors)}
                node_colors = [color_map[c] for c in node_colors]
                cmap = plt.cm.tab10
            else:
                # Numeric
                cmap = plt.cm.viridis
        else:
            node_colors = '#1f77b4'  # Default blue
            cmap = None
        
        # Edge widths
        if edge_width_by:
            edge_widths = self._get_edge_attribute(edge_width_by)
            edge_widths = np.array(edge_widths)
            edge_widths = (edge_widths - edge_widths.min()) / (edge_widths.max() - edge_widths.min() + 1e-10)
            edge_widths = edge_widths * 3 + 0.5  # Range [0.5, 3.5]
        else:
            edge_widths = 1.0
        
        # Draw network
        nx.draw_networkx_nodes(
            self.network, self.pos,
            node_size=node_sizes,
            node_color=node_colors,
            cmap=cmap,
            alpha=0.7,
            ax=self.ax
        )
        
        nx.draw_networkx_edges(
            self.network, self.pos,
            width=edge_widths,
            alpha=0.3,
            ax=self.ax
        )
        
        if show_labels:
            nx.draw_networkx_labels(
                self.network, self.pos,
                font_size=label_font_size,
                ax=self.ax
            )
        
        if title:
            self.ax.set_title(title, fontsize=14, fontweight='bold')
        
        self.ax.axis('off')
        plt.tight_layout()
        
        logger.info("✓ Network visualization created")
        
        return self.fig
    
    # =========================================================================
    # Community Detection Visualization
    # =========================================================================
    
    def plot_communities(self,
                        algorithm: str = 'louvain',
                        figsize: Tuple[int, int] = (12, 10),
                        layout: str = 'spring',
                        show_legend: bool = True) -> plt.Figure:
        """
        Visualize network with community detection
        
        Args:
            algorithm: Community detection algorithm ('louvain', 'girvan_newman', 'label_propagation')
            figsize: Figure size
            layout: Layout algorithm
            show_legend: Whether to show legend
        
        Returns:
            Matplotlib figure
        """
        logger.info(f"Detecting communities using {algorithm}...")
        
        # Detect communities
        if algorithm == 'louvain':
            try:
                import community as community_louvain
                communities = community_louvain.best_partition(self.network)
            except ImportError:
                logger.warning("python-louvain not installed, using label propagation")
                communities = nx.algorithms.community.label_propagation_communities(self.network)
                communities = {node: i for i, comm in enumerate(communities) for node in comm}
        elif algorithm == 'girvan_newman':
            from networkx.algorithms.community import girvan_newman
            communities_gen = girvan_newman(self.network)
            top_level = next(communities_gen)
            communities = {node: i for i, comm in enumerate(top_level) for node in comm}
        elif algorithm == 'label_propagation':
            communities_gen = nx.algorithms.community.label_propagation_communities(self.network)
            communities = {node: i for i, comm in enumerate(communities_gen) for node in comm}
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        
        n_communities = len(set(communities.values()))
        logger.info(f"  Found {n_communities} communities")
        
        # Compute layout
        if self.pos is None:
            self.compute_layout(layout)
        
        # Create figure
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Colors for communities
        cmap = plt.cm.tab10 if n_communities <= 10 else plt.cm.tab20
        colors = [cmap(communities[node] % cmap.N) for node in self.network.nodes()]
        
        # Draw network
        nx.draw_networkx_nodes(
            self.network, self.pos,
            node_color=colors,
            node_size=300,
            alpha=0.7,
            ax=self.ax
        )
        
        nx.draw_networkx_edges(
            self.network, self.pos,
            alpha=0.2,
            ax=self.ax
        )
        
        # Legend
        if show_legend:
            legend_elements = [
                mpatches.Patch(color=cmap(i % cmap.N), label=f'Community {i+1}')
                for i in range(n_communities)
            ]
            self.ax.legend(handles=legend_elements, loc='upper left', fontsize=8)
        
        self.ax.set_title(f'Network Communities ({algorithm.replace("_", " ").title()})', 
                         fontsize=14, fontweight='bold')
        self.ax.axis('off')
        plt.tight_layout()
        
        logger.info("✓ Community visualization created")
        
        return self.fig
    
    # =========================================================================
    # Centrality Visualization
    # =========================================================================
    
    def plot_centrality_network(self,
                               centrality: Dict[str, float],
                               centrality_name: str = 'Centrality',
                               figsize: Tuple[int, int] = (12, 10),
                               layout: str = 'spring',
                               colormap: str = 'YlOrRd') -> plt.Figure:
        """
        Visualize network with nodes colored/sized by centrality
        
        Args:
            centrality: Dictionary mapping node to centrality value
            centrality_name: Name of centrality measure
            figsize: Figure size
            layout: Layout algorithm
            colormap: Matplotlib colormap name
        
        Returns:
            Matplotlib figure
        """
        logger.info(f"Creating {centrality_name} visualization...")
        
        # Compute layout
        if self.pos is None:
            self.compute_layout(layout)
        
        # Create figure
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Get centrality values
        nodes = list(self.network.nodes())
        cent_values = [centrality.get(node, 0) for node in nodes]
        
        # Normalize for visualization
        cent_array = np.array(cent_values)
        norm = Normalize(vmin=cent_array.min(), vmax=cent_array.max())
        
        # Node sizes (proportional to centrality)
        node_sizes = (cent_array - cent_array.min()) / (cent_array.max() - cent_array.min() + 1e-10)
        node_sizes = node_sizes * 1000 + 100
        
        # Draw network
        nx.draw_networkx_nodes(
            self.network, self.pos,
            node_size=node_sizes,
            node_color=cent_values,
            cmap=colormap,
            alpha=0.8,
            ax=self.ax
        )
        
        nx.draw_networkx_edges(
            self.network, self.pos,
            alpha=0.2,
            ax=self.ax
        )
        
        # Top 5 nodes labels
        top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        top_labels = {node: node for node, _ in top_nodes}
        
        nx.draw_networkx_labels(
            self.network, self.pos,
            labels=top_labels,
            font_size=10,
            font_weight='bold',
            ax=self.ax
        )
        
        # Colorbar
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=self.ax, fraction=0.046, pad=0.04)
        cbar.set_label(centrality_name, rotation=270, labelpad=15)
        
        self.ax.set_title(f'Network by {centrality_name}', fontsize=14, fontweight='bold')
        self.ax.axis('off')
        plt.tight_layout()
        
        logger.info("✓ Centrality visualization created")
        
        return self.fig
    
    # =========================================================================
    # Temporal Visualization
    # =========================================================================
    
    def plot_temporal_networks(self,
                              temporal_networks: Dict[int, nx.Graph],
                              n_cols: int = 3,
                              figsize: Tuple[int, int] = (15, 12)) -> plt.Figure:
        """
        Visualize network evolution over time
        
        Args:
            temporal_networks: Dictionary mapping time period to network
            n_cols: Number of columns in subplot grid
            figsize: Figure size
        
        Returns:
            Matplotlib figure
        """
        logger.info("Creating temporal network visualization...")
        
        periods = sorted(temporal_networks.keys())
        n_periods = len(periods)
        n_rows = (n_periods + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_periods > 1 else [axes]
        
        # Use consistent layout across time
        # Get union of all nodes
        all_nodes = set()
        for G in temporal_networks.values():
            all_nodes.update(G.nodes())
        
        # Create layout on full node set
        G_union = nx.Graph()
        G_union.add_nodes_from(all_nodes)
        for G in temporal_networks.values():
            G_union.add_edges_from(G.edges())
        
        pos = nx.spring_layout(G_union, seed=42)
        
        # Plot each period
        for i, (period, G) in enumerate(zip(periods, temporal_networks.values())):
            ax = axes[i]
            
            # Only show nodes that exist in this period
            nodes_in_period = list(G.nodes())
            pos_period = {n: pos[n] for n in nodes_in_period if n in pos}
            
            nx.draw_networkx_nodes(
                G, pos_period,
                node_size=200,
                node_color='lightblue',
                alpha=0.7,
                ax=ax
            )
            
            nx.draw_networkx_edges(
                G, pos_period,
                alpha=0.3,
                ax=ax
            )
            
            ax.set_title(f'Period {period}\n({G.number_of_nodes()} nodes, {G.number_of_edges()} edges)',
                        fontsize=10)
            ax.axis('off')
        
        # Hide empty subplots
        for i in range(n_periods, len(axes)):
            axes[i].axis('off')
        
        plt.suptitle('Network Evolution Over Time', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        logger.info(f"✓ Temporal visualization created ({n_periods} periods)")
        
        return fig
    
    # =========================================================================
    # Ego Network Visualization
    # =========================================================================
    
    def plot_ego_network(self,
                        center_node: str,
                        radius: int = 1,
                        figsize: Tuple[int, int] = (10, 10)) -> plt.Figure:
        """
        Visualize ego network (focal node and its neighbors)
        
        Args:
            center_node: Central node
            radius: Number of hops to include
            figsize: Figure size
        
        Returns:
            Matplotlib figure
        """
        logger.info(f"Creating ego network for {center_node}...")
        
        # Extract ego network
        ego = nx.ego_graph(self.network, center_node, radius=radius)
        
        logger.info(f"  Ego network: {ego.number_of_nodes()} nodes, {ego.number_of_edges()} edges")
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Layout
        pos = nx.spring_layout(ego, seed=42)
        
        # Node colors (center vs neighbors)
        node_colors = ['red' if node == center_node else 'lightblue' 
                      for node in ego.nodes()]
        
        # Node sizes
        node_sizes = [1000 if node == center_node else 300 
                     for node in ego.nodes()]
        
        # Draw network
        nx.draw_networkx_nodes(
            ego, pos,
            node_size=node_sizes,
            node_color=node_colors,
            alpha=0.7,
            ax=ax
        )
        
        nx.draw_networkx_edges(
            ego, pos,
            alpha=0.3,
            ax=ax
        )
        
        nx.draw_networkx_labels(
            ego, pos,
            font_size=8,
            ax=ax
        )
        
        ax.set_title(f'Ego Network: {center_node}\n({ego.number_of_nodes()} nodes, radius={radius})',
                    fontsize=12, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        
        logger.info("✓ Ego network visualization created")
        
        return fig
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def _get_node_attribute(self, attribute: str) -> List:
        """Get node attribute values in node order"""
        if attribute in ['degree', 'degree_centrality']:
            return [self.network.degree(node) for node in self.network.nodes()]
        else:
            return [self.network.nodes[node].get(attribute, 0) for node in self.network.nodes()]
    
    def _get_edge_attribute(self, attribute: str) -> List:
        """Get edge attribute values in edge order"""
        return [self.network[u][v].get(attribute, 1) for u, v in self.network.edges()]
    
    # =========================================================================
    # Export
    # =========================================================================
    
    def export_figure(self, 
                     filepath: Path,
                     dpi: int = 300,
                     format: str = 'pdf'):
        """
        Export current figure to file
        
        Args:
            filepath: Output file path
            dpi: Resolution (for raster formats)
            format: File format ('pdf', 'png', 'svg')
        """
        if self.fig is None:
            raise ValueError("No figure to export. Create visualization first.")
        
        filepath = Path(filepath)
        
        self.fig.savefig(filepath, dpi=dpi, format=format, bbox_inches='tight')
        
        logger.info(f"✓ Figure exported: {filepath}")


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("NETWORK VISUALIZER EXAMPLE")
    print("=" * 80)
    
    # Generate sample network
    np.random.seed(42)
    
    # Create scale-free network (common in real-world networks)
    G = nx.barabasi_albert_graph(50, 2, seed=42)
    
    # Add node attributes
    for node in G.nodes():
        G.nodes[node]['degree_centrality'] = nx.degree_centrality(G)[node]
        G.nodes[node]['type'] = 'Core' if G.degree(node) > 4 else 'Peripheral'
    
    print(f"\nNetwork: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Initialize visualizer
    viz = NetworkVisualizer(G)
    
    # Basic visualization
    print("\n[1] Creating basic network visualization...")
    viz.plot_network(
        node_size_by='degree_centrality',
        title='Strategic Alliance Network'
    )
    
    # Community visualization
    print("\n[2] Creating community visualization...")
    viz.plot_communities(algorithm='label_propagation')
    
    # Centrality visualization
    print("\n[3] Creating centrality visualization...")
    degree_cent = nx.degree_centrality(G)
    viz.plot_centrality_network(
        centrality=degree_cent,
        centrality_name='Degree Centrality'
    )
    
    # Ego network
    print("\n[4] Creating ego network...")
    center_node = max(degree_cent, key=degree_cent.get)
    viz.plot_ego_network(center_node, radius=2)
    
    plt.show()
    
    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETED")
    print("=" * 80)
