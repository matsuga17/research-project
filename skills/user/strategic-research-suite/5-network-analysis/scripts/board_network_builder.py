"""
board_network_builder.py

Board Interlock Network Analysis

This module constructs and analyzes board interlock networks for strategic
management research. Board interlocks occur when a director sits on multiple
company boards, creating ties between firms.

Common applications:
- Information diffusion and practice adoption
- Strategic mimicry and isomorphism
- Corporate governance research
- Elite social capital analysis

Usage:
    from board_network_builder import BoardNetworkBuilder
    
    builder = BoardNetworkBuilder()
    network = builder.build_network_from_data(board_data)
    centrality = builder.calculate_centrality(network)
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Set
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BoardNetworkBuilder:
    """
    Build and analyze board interlock networks
    
    Attributes:
        board_data: DataFrame with firm-director linkages
        network: NetworkX graph object
        firm_id: Column name for firm identifier
        director_id: Column name for director identifier
    """
    
    def __init__(self):
        """Initialize board network builder"""
        self.board_data = None
        self.network = None
        self.firm_id = 'firm_id'
        self.director_id = 'director_id'
        
        logger.info("BoardNetworkBuilder initialized")
    
    def build_network_from_data(self, board_data: pd.DataFrame,
                                firm_id: str = 'firm_id',
                                director_id: str = 'director_id',
                                year: int = None) -> 'networkx.Graph':
        """
        Build board interlock network from data
        
        Args:
            board_data: DataFrame with columns [firm_id, director_id, year, ...]
            firm_id: Name of firm identifier column
            director_id: Name of director identifier column
            year: Specific year to analyze (if None, use all data)
        
        Returns:
            NetworkX graph with firms as nodes, interlocks as edges
        """
        self.board_data = board_data.copy()
        self.firm_id = firm_id
        self.director_id = director_id
        
        # Filter by year if specified
        if year is not None and 'year' in board_data.columns:
            self.board_data = self.board_data[self.board_data['year'] == year]
            logger.info(f"Analyzing board network for year {year}")
        
        logger.info(f"Building network from {len(self.board_data)} director-firm linkages...")
        
        try:
            import networkx as nx
        except ImportError:
            logger.error("networkx not installed. Please install: pip install networkx")
            return None
        
        # Create graph
        self.network = nx.Graph()
        
        # Add all firms as nodes
        firms = self.board_data[firm_id].unique()
        self.network.add_nodes_from(firms)
        logger.info(f"  Added {len(firms)} firms as nodes")
        
        # Create director-to-firms mapping
        director_firms = defaultdict(set)
        for _, row in self.board_data.iterrows():
            director_firms[row[director_id]].add(row[firm_id])
        
        # Add edges for firms sharing directors
        edge_count = 0
        director_count = defaultdict(int)
        
        for director, firm_set in director_firms.items():
            firm_list = list(firm_set)
            
            # Create edges between all pairs of firms sharing this director
            if len(firm_list) > 1:
                for i in range(len(firm_list)):
                    for j in range(i + 1, len(firm_list)):
                        firm_i = firm_list[i]
                        firm_j = firm_list[j]
                        
                        # If edge exists, increment weight; otherwise create edge
                        if self.network.has_edge(firm_i, firm_j):
                            self.network[firm_i][firm_j]['weight'] += 1
                            self.network[firm_i][firm_j]['directors'].add(director)
                        else:
                            self.network.add_edge(firm_i, firm_j, 
                                                weight=1, 
                                                directors={director})
                            edge_count += 1
                        
                        director_count[director] += 1
        
        logger.info(f"  Added {edge_count} edges (interlocks)")
        logger.info(f"  Directors creating interlocks: {len(director_count)}")
        
        # Network statistics
        logger.info(f"\nNetwork Statistics:")
        logger.info(f"  Nodes (firms): {self.network.number_of_nodes()}")
        logger.info(f"  Edges (interlocks): {self.network.number_of_edges()}")
        logger.info(f"  Density: {nx.density(self.network):.4f}")
        logger.info(f"  Connected components: {nx.number_connected_components(self.network)}")
        
        return self.network
    
    def calculate_centrality(self, metrics: List[str] = None) -> pd.DataFrame:
        """
        Calculate centrality measures for all firms
        
        Args:
            metrics: List of centrality metrics to calculate
                    ['degree', 'betweenness', 'closeness', 'eigenvector']
        
        Returns:
            DataFrame with centrality scores
        """
        if self.network is None:
            logger.error("Network not built. Run build_network_from_data() first.")
            return None
        
        try:
            import networkx as nx
        except ImportError:
            logger.error("networkx not installed")
            return None
        
        if metrics is None:
            metrics = ['degree', 'betweenness', 'closeness', 'eigenvector']
        
        logger.info(f"\nCalculating {len(metrics)} centrality metrics...")
        
        centrality_df = pd.DataFrame()
        centrality_df[self.firm_id] = list(self.network.nodes())
        
        # Degree centrality
        if 'degree' in metrics:
            degree_cent = nx.degree_centrality(self.network)
            centrality_df['degree_centrality'] = centrality_df[self.firm_id].map(degree_cent)
            logger.info("  ✓ Degree centrality calculated")
        
        # Betweenness centrality
        if 'betweenness' in metrics:
            betweenness_cent = nx.betweenness_centrality(self.network)
            centrality_df['betweenness_centrality'] = centrality_df[self.firm_id].map(betweenness_cent)
            logger.info("  ✓ Betweenness centrality calculated")
        
        # Closeness centrality
        if 'closeness' in metrics:
            # Only for connected components
            try:
                closeness_cent = nx.closeness_centrality(self.network)
                centrality_df['closeness_centrality'] = centrality_df[self.firm_id].map(closeness_cent)
                logger.info("  ✓ Closeness centrality calculated")
            except Exception as e:
                logger.warning(f"  ✗ Could not calculate closeness centrality: {e}")
        
        # Eigenvector centrality
        if 'eigenvector' in metrics:
            try:
                eigenvector_cent = nx.eigenvector_centrality(self.network, max_iter=1000)
                centrality_df['eigenvector_centrality'] = centrality_df[self.firm_id].map(eigenvector_cent)
                logger.info("  ✓ Eigenvector centrality calculated")
            except Exception as e:
                logger.warning(f"  ✗ Could not calculate eigenvector centrality: {e}")
        
        return centrality_df
    
    def identify_key_directors(self, top_n: int = 10) -> pd.DataFrame:
        """
        Identify most connected directors (those creating most interlocks)
        
        Args:
            top_n: Number of top directors to return
        
        Returns:
            DataFrame with director statistics
        """
        if self.board_data is None:
            logger.error("No board data available")
            return None
        
        logger.info(f"\nIdentifying top {top_n} directors by board seats...")
        
        # Count board seats per director
        director_stats = self.board_data.groupby(self.director_id).agg({
            self.firm_id: ['count', 'nunique']
        }).reset_index()
        
        director_stats.columns = [self.director_id, 'total_seats', 'unique_firms']
        
        # Sort by number of unique firms
        director_stats = director_stats.sort_values('unique_firms', ascending=False)
        
        # Calculate potential interlocks created by each director
        director_stats['potential_interlocks'] = (
            director_stats['unique_firms'] * (director_stats['unique_firms'] - 1) / 2
        )
        
        top_directors = director_stats.head(top_n)
        
        logger.info(f"\nTop {top_n} Directors:")
        for idx, row in top_directors.iterrows():
            logger.info(f"  Director {row[self.director_id]}: "
                       f"{row['unique_firms']} boards, "
                       f"{int(row['potential_interlocks'])} potential ties")
        
        return top_directors
    
    def visualize_network(self, save_path: str = None,
                         node_size_by: str = 'degree',
                         layout: str = 'spring') -> 'matplotlib.figure.Figure':
        """
        Visualize board network
        
        Args:
            save_path: Path to save figure
            node_size_by: Size nodes by centrality measure
            layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
        
        Returns:
            matplotlib Figure object
        """
        if self.network is None:
            logger.error("Network not built. Run build_network_from_data() first.")
            return None
        
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except ImportError:
            logger.error("networkx or matplotlib not installed")
            return None
        
        logger.info(f"\nVisualizing network with {layout} layout...")
        
        # Calculate layout
        if layout == 'spring':
            pos = nx.spring_layout(self.network, k=0.5, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(self.network)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(self.network)
        else:
            pos = nx.spring_layout(self.network)
        
        # Node sizes
        if node_size_by == 'degree':
            node_sizes = [self.network.degree(node) * 100 for node in self.network.nodes()]
        else:
            node_sizes = [300] * self.network.number_of_nodes()
        
        # Edge widths based on weight
        edge_widths = [self.network[u][v].get('weight', 1) * 0.5 
                      for u, v in self.network.edges()]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Draw network
        nx.draw_networkx_nodes(self.network, pos,
                              node_size=node_sizes,
                              node_color='lightblue',
                              alpha=0.7,
                              ax=ax)
        
        nx.draw_networkx_edges(self.network, pos,
                              width=edge_widths,
                              alpha=0.3,
                              ax=ax)
        
        # Draw labels for high-degree nodes
        high_degree_nodes = [node for node in self.network.nodes() 
                           if self.network.degree(node) >= 5]
        high_degree_labels = {node: str(node) for node in high_degree_nodes}
        
        nx.draw_networkx_labels(self.network, pos,
                               labels=high_degree_labels,
                               font_size=8,
                               ax=ax)
        
        ax.set_title(f'Board Interlock Network\n'
                    f'{self.network.number_of_nodes()} firms, '
                    f'{self.network.number_of_edges()} interlocks',
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Visualization saved: {save_path}")
        
        return fig


# Example usage
if __name__ == "__main__":
    # Generate sample board data
    np.random.seed(42)
    
    # Create firms
    n_firms = 50
    firms = [f'Firm_{i}' for i in range(n_firms)]
    
    # Create directors
    n_directors = 200
    directors = [f'Director_{i}' for i in range(n_directors)]
    
    # Assign directors to boards
    # Most directors on 1-2 boards, some on 3-5 boards
    board_data = []
    for director in directors:
        n_boards = np.random.choice([1, 2, 3, 4, 5], p=[0.6, 0.25, 0.10, 0.04, 0.01])
        selected_firms = np.random.choice(firms, size=n_boards, replace=False)
        
        for firm in selected_firms:
            board_data.append({
                'firm_id': firm,
                'director_id': director,
                'year': 2023
            })
    
    df_board = pd.DataFrame(board_data)
    
    logger.info("="*60)
    logger.info("Board Interlock Network Analysis Example")
    logger.info("="*60)
    
    # Build network
    builder = BoardNetworkBuilder()
    network = builder.build_network_from_data(df_board)
    
    # Calculate centrality
    centrality_df = builder.calculate_centrality()
    logger.info("\nTop 5 firms by degree centrality:")
    print(centrality_df.nlargest(5, 'degree_centrality'))
    
    # Identify key directors
    top_directors = builder.identify_key_directors(top_n=10)
    
    # Visualize
    fig = builder.visualize_network()
    if fig:
        import matplotlib.pyplot as plt
        plt.show()
    
    logger.info("\n" + "="*60)
    logger.info("Analysis completed!")
    logger.info("="*60)
