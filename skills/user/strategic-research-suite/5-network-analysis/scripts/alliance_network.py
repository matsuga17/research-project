"""
alliance_network.py

Strategic Alliance Network Analysis

This module builds and analyzes strategic alliance networks, enabling
research on interfirm collaboration, knowledge transfer, and competitive dynamics.

Key Features:
- Alliance network construction from multiple data sources
- Partner selection and matching analysis
- Network evolution over time
- Alliance portfolio analysis
- Knowledge flow and spillover effects

Common Applications in Strategic Research:
- Alliance formation and partner selection
- Knowledge transfer through alliances
- Network position and firm performance
- Competitive dynamics in alliance networks
- Technology sourcing strategies

Usage:
    from alliance_network import AllianceNetworkBuilder
    
    # Initialize builder
    builder = AllianceNetworkBuilder()
    
    # Build network from SDC Platinum data
    network = builder.build_from_sdc(df_alliances)
    
    # Analyze network properties
    stats = builder.calculate_network_statistics(network)
    
    # Identify strategic positions
    positions = builder.identify_strategic_positions(network)

References:
- Ahuja, G. (2000). "Collaboration networks, structural holes, and innovation."
  Administrative Science Quarterly, 45(3), 425-455.
- Gulati, R. (1995). "Social structure and alliance formation patterns."
  Administrative Science Quarterly, 40(4), 619-652.
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import List, Dict, Optional, Tuple, Any
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AllianceNetworkBuilder:
    """
    Build and analyze strategic alliance networks
    
    Attributes:
        network: NetworkX graph object
        alliances: DataFrame of alliance data
        firms: Set of firm identifiers
    """
    
    def __init__(self):
        """Initialize alliance network builder"""
        self.network = None
        self.alliances = None
        self.firms = set()
        
        logger.info("AllianceNetworkBuilder initialized")
    
    # =========================================================================
    # Network Construction
    # =========================================================================
    
    def build_from_dataframe(self, 
                            df: pd.DataFrame,
                            firm1_col: str = 'firm1',
                            firm2_col: str = 'firm2',
                            date_col: str = 'announcement_date',
                            attributes: Optional[List[str]] = None) -> nx.Graph:
        """
        Build alliance network from DataFrame
        
        Args:
            df: DataFrame with alliance data
            firm1_col: Column name for first firm
            firm2_col: Column name for second firm
            date_col: Column name for announcement date
            attributes: Additional edge attributes to include
        
        Returns:
            NetworkX Graph object
        """
        logger.info(f"Building alliance network from {len(df)} alliances...")
        
        self.alliances = df.copy()
        
        # Create undirected graph
        G = nx.Graph()
        
        # Add edges (alliances)
        for idx, row in df.iterrows():
            firm1 = row[firm1_col]
            firm2 = row[firm2_col]
            
            # Add firms as nodes
            if firm1 not in G:
                G.add_node(firm1, firm_id=firm1)
            if firm2 not in G:
                G.add_node(firm2, firm_id=firm2)
            
            # Edge attributes
            edge_attrs = {'date': row[date_col]}
            
            if attributes:
                for attr in attributes:
                    if attr in row:
                        edge_attrs[attr] = row[attr]
            
            # Add alliance as edge
            G.add_edge(firm1, firm2, **edge_attrs)
            
            self.firms.add(firm1)
            self.firms.add(firm2)
        
        self.network = G
        
        logger.info(f"✓ Network built:")
        logger.info(f"  Nodes (firms): {G.number_of_nodes()}")
        logger.info(f"  Edges (alliances): {G.number_of_edges()}")
        logger.info(f"  Density: {nx.density(G):.4f}")
        
        return G
    
    def build_temporal_networks(self,
                               df: pd.DataFrame,
                               time_col: str = 'year',
                               window_size: int = 3) -> Dict[int, nx.Graph]:
        """
        Build time-varying alliance networks
        
        Args:
            df: DataFrame with alliance data
            time_col: Column name for time period
            window_size: Rolling window size in years
        
        Returns:
            Dictionary mapping time period to network
        """
        logger.info("Building temporal alliance networks...")
        
        years = sorted(df[time_col].unique())
        temporal_networks = {}
        
        for year in years:
            # Get alliances in window
            window_start = year - window_size + 1
            df_window = df[(df[time_col] >= window_start) & (df[time_col] <= year)]
            
            # Build network for this period
            G = self.build_from_dataframe(df_window)
            temporal_networks[year] = G
            
            logger.info(f"  {year}: {G.number_of_nodes()} firms, {G.number_of_edges()} alliances")
        
        logger.info(f"✓ Built {len(temporal_networks)} temporal networks")
        
        return temporal_networks
    
    # =========================================================================
    # Network Analysis
    # =========================================================================
    
    def calculate_network_statistics(self, G: Optional[nx.Graph] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive network statistics
        
        Args:
            G: NetworkX graph (uses self.network if None)
        
        Returns:
            Dictionary of network statistics
        """
        if G is None:
            G = self.network
        
        if G is None:
            raise ValueError("No network available. Build network first.")
        
        logger.info("Calculating network statistics...")
        
        stats = {
            # Basic properties
            'n_firms': G.number_of_nodes(),
            'n_alliances': G.number_of_edges(),
            'density': nx.density(G),
            
            # Connectivity
            'is_connected': nx.is_connected(G),
            'n_components': nx.number_connected_components(G),
            'largest_component_size': len(max(nx.connected_components(G), key=len)),
            
            # Average properties
            'avg_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
            'avg_clustering': nx.average_clustering(G),
            
            # Path lengths (on largest component)
            'avg_path_length': None,
            'diameter': None
        }
        
        # Path length metrics (only for connected graphs)
        if nx.is_connected(G):
            stats['avg_path_length'] = nx.average_shortest_path_length(G)
            stats['diameter'] = nx.diameter(G)
        else:
            # Calculate for largest component
            largest_cc = max(nx.connected_components(G), key=len)
            G_lcc = G.subgraph(largest_cc)
            stats['avg_path_length'] = nx.average_shortest_path_length(G_lcc)
            stats['diameter'] = nx.diameter(G_lcc)
        
        logger.info("✓ Network statistics calculated")
        
        return stats
    
    def calculate_firm_metrics(self, G: Optional[nx.Graph] = None) -> pd.DataFrame:
        """
        Calculate firm-level network metrics
        
        Args:
            G: NetworkX graph
        
        Returns:
            DataFrame with firm-level metrics
        """
        if G is None:
            G = self.network
        
        logger.info("Calculating firm-level network metrics...")
        
        metrics = []
        
        for firm in G.nodes():
            # Degree centrality
            degree = G.degree(firm)
            degree_centrality = nx.degree_centrality(G)[firm]
            
            # Betweenness centrality
            betweenness = nx.betweenness_centrality(G)[firm]
            
            # Closeness centrality
            if nx.is_connected(G):
                closeness = nx.closeness_centrality(G)[firm]
            else:
                # Use harmonic centrality for disconnected graphs
                closeness = nx.harmonic_centrality(G)[firm]
            
            # Eigenvector centrality
            try:
                eigenvector = nx.eigenvector_centrality(G, max_iter=1000)[firm]
            except:
                eigenvector = np.nan
            
            # Clustering coefficient
            clustering = nx.clustering(G, firm)
            
            # Structural holes (constraint)
            try:
                constraint = nx.constraint(G, firm)
            except:
                constraint = np.nan
            
            metrics.append({
                'firm_id': firm,
                'degree': degree,
                'degree_centrality': degree_centrality,
                'betweenness_centrality': betweenness,
                'closeness_centrality': closeness,
                'eigenvector_centrality': eigenvector,
                'clustering_coefficient': clustering,
                'constraint': constraint
            })
        
        df_metrics = pd.DataFrame(metrics)
        
        logger.info(f"✓ Calculated metrics for {len(df_metrics)} firms")
        
        return df_metrics
    
    def identify_strategic_positions(self, G: Optional[nx.Graph] = None) -> Dict[str, List[str]]:
        """
        Identify firms in strategic network positions
        
        Args:
            G: NetworkX graph
        
        Returns:
            Dictionary of strategic position categories
        """
        if G is None:
            G = self.network
        
        logger.info("Identifying strategic network positions...")
        
        # Calculate centrality metrics
        degree_cent = nx.degree_centrality(G)
        betweenness_cent = nx.betweenness_centrality(G)
        
        # Define thresholds (top 10%)
        degree_threshold = np.percentile(list(degree_cent.values()), 90)
        betweenness_threshold = np.percentile(list(betweenness_cent.values()), 90)
        
        positions = {
            'hubs': [],           # High degree
            'brokers': [],        # High betweenness
            'central_players': [], # High both
            'peripheral': []       # Low both
        }
        
        for firm in G.nodes():
            degree = degree_cent[firm]
            betweenness = betweenness_cent[firm]
            
            if degree >= degree_threshold and betweenness >= betweenness_threshold:
                positions['central_players'].append(firm)
            elif degree >= degree_threshold:
                positions['hubs'].append(firm)
            elif betweenness >= betweenness_threshold:
                positions['brokers'].append(firm)
            elif degree < np.percentile(list(degree_cent.values()), 10):
                positions['peripheral'].append(firm)
        
        logger.info("✓ Strategic positions identified:")
        for pos_type, firms in positions.items():
            logger.info(f"  {pos_type}: {len(firms)} firms")
        
        return positions
    
    # =========================================================================
    # Alliance Portfolio Analysis
    # =========================================================================
    
    def analyze_alliance_portfolio(self, firm_id: str, G: Optional[nx.Graph] = None) -> Dict[str, Any]:
        """
        Analyze a firm's alliance portfolio
        
        Args:
            firm_id: Firm identifier
            G: NetworkX graph
        
        Returns:
            Dictionary with portfolio statistics
        """
        if G is None:
            G = self.network
        
        if firm_id not in G:
            raise ValueError(f"Firm {firm_id} not in network")
        
        logger.info(f"Analyzing alliance portfolio for {firm_id}...")
        
        # Get partners
        partners = list(G.neighbors(firm_id))
        
        # Portfolio size
        portfolio_size = len(partners)
        
        # Partner diversity (using degree as proxy for partner type)
        partner_degrees = [G.degree(p) for p in partners]
        partner_diversity = np.std(partner_degrees) if len(partner_degrees) > 1 else 0
        
        # Network reach (second-order connections)
        second_order = set()
        for partner in partners:
            second_order.update(G.neighbors(partner))
        second_order.discard(firm_id)  # Remove focal firm
        second_order.difference_update(partners)  # Remove direct partners
        network_reach = len(second_order)
        
        # Redundancy (clustering among partners)
        partner_subgraph = G.subgraph(partners)
        redundancy = nx.density(partner_subgraph) if portfolio_size > 1 else 0
        
        portfolio = {
            'firm_id': firm_id,
            'portfolio_size': portfolio_size,
            'partners': partners,
            'partner_diversity': partner_diversity,
            'network_reach': network_reach,
            'redundancy': redundancy,
            'avg_partner_degree': np.mean(partner_degrees) if partner_degrees else 0
        }
        
        logger.info(f"✓ Portfolio analysis completed:")
        logger.info(f"  Partners: {portfolio_size}")
        logger.info(f"  Network reach: {network_reach}")
        logger.info(f"  Redundancy: {redundancy:.3f}")
        
        return portfolio
    
    # =========================================================================
    # Export and Visualization
    # =========================================================================
    
    def export_network(self, filepath: Path, format: str = 'graphml'):
        """
        Export network to file
        
        Args:
            filepath: Output file path
            format: File format ('graphml', 'gexf', 'gml', 'edgelist')
        """
        if self.network is None:
            raise ValueError("No network to export")
        
        filepath = Path(filepath)
        
        if format == 'graphml':
            nx.write_graphml(self.network, filepath)
        elif format == 'gexf':
            nx.write_gexf(self.network, filepath)
        elif format == 'gml':
            nx.write_gml(self.network, filepath)
        elif format == 'edgelist':
            nx.write_edgelist(self.network, filepath)
        else:
            raise ValueError(f"Unknown format: {format}")
        
        logger.info(f"✓ Network exported: {filepath}")
    
    def export_firm_metrics(self, filepath: Path):
        """
        Export firm-level metrics to CSV
        
        Args:
            filepath: Output file path
        """
        metrics = self.calculate_firm_metrics()
        metrics.to_csv(filepath, index=False)
        logger.info(f"✓ Firm metrics exported: {filepath}")


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("ALLIANCE NETWORK ANALYSIS EXAMPLE")
    print("=" * 80)
    
    # Generate sample alliance data
    np.random.seed(42)
    
    firms = [f'FIRM{i:03d}' for i in range(1, 51)]  # 50 firms
    
    alliances = []
    for _ in range(100):  # 100 alliances
        firm1, firm2 = np.random.choice(firms, 2, replace=False)
        year = np.random.randint(2015, 2023)
        alliance_type = np.random.choice(['R&D', 'Marketing', 'Manufacturing'])
        
        alliances.append({
            'firm1': firm1,
            'firm2': firm2,
            'year': year,
            'alliance_type': alliance_type,
            'announcement_date': f'{year}-01-01'
        })
    
    df_alliances = pd.DataFrame(alliances)
    
    print(f"\nSample data: {len(df_alliances)} alliances among {len(firms)} firms")
    
    # Build network
    builder = AllianceNetworkBuilder()
    network = builder.build_from_dataframe(df_alliances)
    
    # Calculate statistics
    stats = builder.calculate_network_statistics()
    print("\n" + "=" * 80)
    print("NETWORK STATISTICS")
    print("=" * 80)
    for key, value in stats.items():
        if value is not None:
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")
    
    # Identify strategic positions
    positions = builder.identify_strategic_positions()
    print("\n" + "=" * 80)
    print("STRATEGIC POSITIONS")
    print("=" * 80)
    for pos_type, firm_list in positions.items():
        print(f"{pos_type}: {len(firm_list)} firms")
        if len(firm_list) > 0:
            print(f"  Examples: {firm_list[:3]}")
    
    # Analyze portfolio for a central firm
    if len(positions['central_players']) > 0:
        focal_firm = positions['central_players'][0]
        portfolio = builder.analyze_alliance_portfolio(focal_firm)
        
        print("\n" + "=" * 80)
        print(f"ALLIANCE PORTFOLIO: {focal_firm}")
        print("=" * 80)
        print(f"Portfolio size: {portfolio['portfolio_size']}")
        print(f"Network reach: {portfolio['network_reach']}")
        print(f"Redundancy: {portfolio['redundancy']:.3f}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)
