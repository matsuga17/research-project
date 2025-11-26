"""
Strategic Management Research Hub - Network Analyzer Module
============================================================

Advanced network analysis for strategic management research:
- Board Interlocks Analysis
- Strategic Alliance Networks
- Patent Citation Networks
- Supply Chain Networks
- Executive Mobility Networks

Metrics: Centrality, Structural Holes, Clustering, Small-World Properties

Author: Strategic Management Research Hub
Version: 3.0
License: MIT

References:
- Burt (2004): Structural Holes and Good Ideas. AJS
- Uzzi & Spiro (2005): Collaboration and Creativity. AJS
- Stuart (1998): Network Positions and Propensities. ASQ
- Ahuja (2000): Collaboration Networks. SMJ
"""

import pandas as pd
import numpy as np
import networkx as nx
from typing import List, Dict, Optional, Tuple, Union, Set
import logging
from pathlib import Path
import json
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
from itertools import combinations
import warnings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BoardInterlockAnalyzer:
    """
    Analyze board interlock networks and compute board-level metrics.
    
    Board interlocks occur when directors serve on multiple boards,
    creating information channels between firms.
    
    Usage:
    ```python
    analyzer = BoardInterlockAnalyzer()
    
    # Input: DataFrame with columns [company_id, company_name, director_id, director_name, year]
    board_data = pd.read_csv('board_composition.csv')
    
    # Build network
    G = analyzer.build_interlock_network(board_data, year=2020)
    
    # Compute metrics
    metrics = analyzer.compute_network_metrics(G, board_data)
    
    # Visualize
    analyzer.visualize_network(G, output_path='board_network.png')
    ```
    
    Key Metrics:
    - **Degree Centrality**: Number of direct connections (interlocks)
    - **Betweenness Centrality**: Position as bridge between clusters
    - **Eigenvector Centrality**: Connection to well-connected firms
    - **Structural Holes (Burt 1992)**: Access to non-redundant information
    """
    
    def __init__(self):
        self.G = None
        self.metrics_df = None
        
    def build_interlock_network(
        self,
        board_data: pd.DataFrame,
        year: Optional[int] = None,
        min_directors: int = 1
    ) -> nx.Graph:
        """
        Build board interlock network from board composition data.
        
        Parameters:
        -----------
        board_data : DataFrame
            Must contain columns: company_id, director_id, year
        year : int, optional
            Filter to specific year. If None, use all years
        min_directors : int
            Minimum number of shared directors to create edge (default: 1)
            
        Returns:
        --------
        G : networkx.Graph
            Firm interlock network where edge weight = number of shared directors
        """
        logger.info("Building board interlock network...")
        
        # Filter by year if specified
        if year is not None:
            df = board_data[board_data['year'] == year].copy()
            logger.info(f"Filtered to year {year}: {len(df)} records")
        else:
            df = board_data.copy()
            
        # Validate required columns
        required_cols = ['company_id', 'director_id']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
            
        # Create director-company mapping
        director_firms = defaultdict(set)
        for _, row in df.iterrows():
            director_firms[row['director_id']].add(row['company_id'])
            
        # Build network
        G = nx.Graph()
        
        # Add all firms as nodes
        firms = df['company_id'].unique()
        G.add_nodes_from(firms)
        
        # Add company names if available
        if 'company_name' in df.columns:
            name_mapping = df[['company_id', 'company_name']].drop_duplicates()
            name_dict = dict(zip(name_mapping['company_id'], name_mapping['company_name']))
            nx.set_node_attributes(G, name_dict, 'name')
            
        # Create edges based on shared directors
        edge_weights = defaultdict(int)
        for director_id, firm_set in director_firms.items():
            if len(firm_set) > 1:  # Director serves on multiple boards
                for firm1, firm2 in combinations(firm_set, 2):
                    edge_weights[(firm1, firm2)] += 1
                    
        # Add edges with weights
        for (firm1, firm2), weight in edge_weights.items():
            if weight >= min_directors:
                G.add_edge(firm1, firm2, weight=weight)
                
        logger.info(f"Network created: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        self.G = G
        return G
        
    def compute_network_metrics(
        self,
        G: nx.Graph,
        board_data: Optional[pd.DataFrame] = None,
        include_structural_holes: bool = True
    ) -> pd.DataFrame:
        """
        Compute comprehensive network metrics for each firm.
        
        Parameters:
        -----------
        G : networkx.Graph
            Firm interlock network
        board_data : DataFrame, optional
            Original board data for additional metrics
        include_structural_holes : bool
            Whether to compute Burt's structural holes metrics (computationally expensive)
            
        Returns:
        --------
        metrics_df : DataFrame
            Firm-level network metrics
        """
        logger.info("Computing network metrics...")
        
        metrics = []
        
        # Basic metrics
        degree_cent = nx.degree_centrality(G)
        betweenness_cent = nx.betweenness_centrality(G, weight='weight')
        closeness_cent = nx.closeness_centrality(G, distance='weight')
        eigenvector_cent = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
        
        # Clustering coefficient
        clustering = nx.clustering(G, weight='weight')
        
        # PageRank (alternative to eigenvector centrality)
        pagerank = nx.pagerank(G, weight='weight')
        
        for node in G.nodes():
            node_metrics = {
                'company_id': node,
                'degree': G.degree(node),
                'weighted_degree': G.degree(node, weight='weight'),
                'degree_centrality': degree_cent[node],
                'betweenness_centrality': betweenness_cent[node],
                'closeness_centrality': closeness_cent[node],
                'eigenvector_centrality': eigenvector_cent[node],
                'clustering_coefficient': clustering[node],
                'pagerank': pagerank[node]
            }
            
            # Structural holes metrics (Burt 1992)
            if include_structural_holes:
                constraint = self._compute_constraint(G, node)
                effective_size = self._compute_effective_size(G, node)
                efficiency = effective_size / G.degree(node) if G.degree(node) > 0 else 0
                
                node_metrics.update({
                    'constraint': constraint,
                    'effective_size': effective_size,
                    'efficiency': efficiency,
                    'structural_holes_score': 1 - constraint  # Higher = more structural holes
                })
                
            metrics.append(node_metrics)
            
        metrics_df = pd.DataFrame(metrics)
        
        # Add company names if available
        if 'name' in G.nodes[list(G.nodes())[0]]:
            name_dict = nx.get_node_attributes(G, 'name')
            metrics_df['company_name'] = metrics_df['company_id'].map(name_dict)
            
        # Add board size if board_data provided
        if board_data is not None and 'company_id' in board_data.columns:
            board_size = board_data.groupby('company_id')['director_id'].nunique().reset_index()
            board_size.columns = ['company_id', 'board_size']
            metrics_df = metrics_df.merge(board_size, on='company_id', how='left')
            
        logger.info(f"Computed metrics for {len(metrics_df)} firms")
        
        self.metrics_df = metrics_df
        return metrics_df
        
    def _compute_constraint(self, G: nx.Graph, node) -> float:
        """
        Compute Burt's constraint measure for structural holes.
        
        Constraint measures the extent to which ego's contacts are connected
        to each other. High constraint = few structural holes.
        
        Formula: C_i = Σ_j (p_ij + Σ_q p_iq * p_qj)^2
        where p_ij = proportion of ego's relations invested in contact j
        """
        neighbors = list(G.neighbors(node))
        if len(neighbors) == 0:
            return 1.0  # Isolated node has maximum constraint
            
        total_weight = sum(G[node][neighbor].get('weight', 1) for neighbor in neighbors)
        constraint = 0.0
        
        for j in neighbors:
            # Direct investment in j
            p_ij = G[node][j].get('weight', 1) / total_weight
            
            # Indirect investment through common neighbors
            indirect = 0.0
            for q in neighbors:
                if q != j and G.has_edge(j, q):
                    p_iq = G[node][q].get('weight', 1) / total_weight
                    p_qj = 1.0  # Simplified: assume equal weight
                    indirect += p_iq * p_qj
                    
            constraint += (p_ij + indirect) ** 2
            
        return constraint
        
    def _compute_effective_size(self, G: nx.Graph, node) -> float:
        """
        Compute effective size of ego network (Burt 1992).
        
        Effective Size = n - (2t/n)
        where n = number of alters, t = number of ties among alters
        
        Higher effective size = more structural holes
        """
        neighbors = list(G.neighbors(node))
        n = len(neighbors)
        
        if n <= 1:
            return float(n)
            
        # Count ties among neighbors
        ties_among_neighbors = 0
        for i, j in combinations(neighbors, 2):
            if G.has_edge(i, j):
                ties_among_neighbors += 1
                
        effective_size = n - (2 * ties_among_neighbors / n)
        return effective_size
        
    def detect_communities(
        self,
        G: nx.Graph,
        method: str = 'louvain'
    ) -> Dict[int, int]:
        """
        Detect communities in the network.
        
        Parameters:
        -----------
        G : networkx.Graph
            Firm network
        method : str
            Community detection method: 'louvain', 'girvan_newman', 'label_propagation'
            
        Returns:
        --------
        communities : dict
            Mapping of node -> community_id
        """
        logger.info(f"Detecting communities using {method} method...")
        
        if method == 'louvain':
            try:
                import community.community_louvain as community_louvain
                communities = community_louvain.best_partition(G, weight='weight')
            except ImportError:
                logger.warning("python-louvain not installed. Using label propagation instead.")
                method = 'label_propagation'
                
        if method == 'label_propagation':
            from networkx.algorithms.community import label_propagation_communities
            comm_list = list(label_propagation_communities(G))
            communities = {}
            for i, comm in enumerate(comm_list):
                for node in comm:
                    communities[node] = i
                    
        elif method == 'girvan_newman':
            from networkx.algorithms.community import girvan_newman
            comm_iter = girvan_newman(G)
            # Get first level of communities
            comm_list = next(comm_iter)
            communities = {}
            for i, comm in enumerate(comm_list):
                for node in comm:
                    communities[node] = i
                    
        logger.info(f"Found {len(set(communities.values()))} communities")
        return communities
        
    def analyze_temporal_evolution(
        self,
        board_data: pd.DataFrame,
        start_year: int,
        end_year: int
    ) -> pd.DataFrame:
        """
        Analyze how network structure evolves over time.
        
        Parameters:
        -----------
        board_data : DataFrame
            Board composition data with 'year' column
        start_year, end_year : int
            Year range to analyze
            
        Returns:
        --------
        evolution_df : DataFrame
            Network-level metrics over time
        """
        logger.info(f"Analyzing network evolution from {start_year} to {end_year}...")
        
        evolution = []
        
        for year in range(start_year, end_year + 1):
            G = self.build_interlock_network(board_data, year=year)
            
            # Network-level metrics
            metrics = {
                'year': year,
                'num_firms': G.number_of_nodes(),
                'num_interlocks': G.number_of_edges(),
                'density': nx.density(G),
                'avg_degree': np.mean([d for n, d in G.degree()]),
                'avg_clustering': nx.average_clustering(G, weight='weight'),
            }
            
            # Connected components
            components = list(nx.connected_components(G))
            metrics['num_components'] = len(components)
            metrics['largest_component_size'] = len(max(components, key=len)) if components else 0
            
            # Small-world properties
            if G.number_of_nodes() > 10 and G.number_of_edges() > 0:
                # Average path length (for largest component)
                largest_cc = G.subgraph(max(components, key=len))
                if largest_cc.number_of_nodes() > 1:
                    metrics['avg_path_length'] = nx.average_shortest_path_length(largest_cc)
                    
            evolution.append(metrics)
            
        evolution_df = pd.DataFrame(evolution)
        logger.info(f"Computed evolution metrics for {len(evolution_df)} years")
        
        return evolution_df
        
    def visualize_network(
        self,
        G: nx.Graph,
        output_path: Optional[str] = None,
        node_color_attr: Optional[str] = None,
        node_size_attr: str = 'degree',
        layout: str = 'spring',
        figsize: Tuple[int, int] = (12, 10)
    ):
        """
        Visualize the board interlock network.
        
        Parameters:
        -----------
        G : networkx.Graph
            Network to visualize
        output_path : str, optional
            Path to save figure
        node_color_attr : str, optional
            Node attribute to use for coloring (e.g., 'community', 'industry')
        node_size_attr : str
            Node attribute to use for sizing (default: 'degree')
        layout : str
            Layout algorithm: 'spring', 'circular', 'kamada_kawai'
        figsize : tuple
            Figure size
        """
        logger.info("Visualizing network...")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Choose layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)
            
        # Node sizes based on attribute
        if node_size_attr == 'degree':
            node_sizes = [G.degree(node) * 100 for node in G.nodes()]
        else:
            sizes = nx.get_node_attributes(G, node_size_attr)
            node_sizes = [sizes.get(node, 100) for node in G.nodes()]
            
        # Node colors
        if node_color_attr:
            colors = nx.get_node_attributes(G, node_color_attr)
            node_colors = [colors.get(node, 0) for node in G.nodes()]
        else:
            node_colors = 'lightblue'
            
        # Edge widths based on weight
        edge_widths = [G[u][v].get('weight', 1) * 0.5 for u, v in G.edges()]
        
        # Draw network
        nx.draw_networkx_nodes(
            G, pos,
            node_size=node_sizes,
            node_color=node_colors,
            cmap=plt.cm.Set3,
            alpha=0.7,
            ax=ax
        )
        
        nx.draw_networkx_edges(
            G, pos,
            width=edge_widths,
            alpha=0.3,
            ax=ax
        )
        
        # Add labels for high-degree nodes
        high_degree_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]
        label_dict = {}
        if 'name' in G.nodes[list(G.nodes())[0]]:
            name_dict = nx.get_node_attributes(G, 'name')
            for node, degree in high_degree_nodes:
                label_dict[node] = name_dict.get(node, str(node))[:15]  # Truncate long names
        else:
            for node, degree in high_degree_nodes:
                label_dict[node] = str(node)
                
        nx.draw_networkx_labels(
            G, pos,
            labels=label_dict,
            font_size=8,
            ax=ax
        )
        
        ax.set_title(f'Board Interlock Network (n={G.number_of_nodes()}, edges={G.number_of_edges()})',
                    fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"Network visualization saved to {output_path}")
        else:
            plt.show()
            
        plt.close()


class AllianceNetworkAnalyzer:
    """
    Analyze strategic alliance networks.
    
    Usage:
    ```python
    analyzer = AllianceNetworkAnalyzer()
    
    # Input: DataFrame with columns [firm1_id, firm2_id, alliance_type, year, value]
    alliance_data = pd.read_csv('alliances.csv')
    
    # Build network
    G = analyzer.build_alliance_network(alliance_data, year=2020)
    
    # Compute metrics
    metrics = analyzer.compute_partner_diversity(G, alliance_data)
    
    # Analyze partner selection patterns
    patterns = analyzer.analyze_partner_selection(alliance_data)
    ```
    """
    
    def __init__(self):
        self.G = None
        
    def build_alliance_network(
        self,
        alliance_data: pd.DataFrame,
        year: Optional[int] = None,
        alliance_types: Optional[List[str]] = None,
        directed: bool = False
    ) -> Union[nx.Graph, nx.DiGraph]:
        """
        Build strategic alliance network.
        
        Parameters:
        -----------
        alliance_data : DataFrame
            Must contain: firm1_id, firm2_id, year
            Optional: alliance_type, value
        year : int, optional
            Filter to specific year
        alliance_types : list, optional
            Filter to specific alliance types (e.g., ['JV', 'R&D'])
        directed : bool
            Whether to create directed network (default: undirected)
            
        Returns:
        --------
        G : networkx.Graph or DiGraph
            Alliance network
        """
        logger.info("Building alliance network...")
        
        df = alliance_data.copy()
        
        # Filter by year
        if year is not None:
            df = df[df['year'] == year]
            
        # Filter by alliance type
        if alliance_types is not None and 'alliance_type' in df.columns:
            df = df[df['alliance_type'].isin(alliance_types)]
            
        # Create network
        if directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
            
        # Add edges
        for _, row in df.iterrows():
            firm1, firm2 = row['firm1_id'], row['firm2_id']
            
            if G.has_edge(firm1, firm2):
                # Multiple alliances between same firms
                G[firm1][firm2]['weight'] += 1
                G[firm1][firm2]['alliances'].append(row.to_dict())
            else:
                attrs = {'weight': 1, 'alliances': [row.to_dict()]}
                if 'value' in row:
                    attrs['total_value'] = row['value']
                G.add_edge(firm1, firm2, **attrs)
                
        logger.info(f"Alliance network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        self.G = G
        return G
        
    def compute_partner_diversity(
        self,
        G: nx.Graph,
        alliance_data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Compute partner diversity metrics for each firm.
        
        Metrics:
        - Number of unique partners
        - Partner diversity (Herfindahl index)
        - Geographic diversity
        - Industry diversity
        
        Parameters:
        -----------
        G : networkx.Graph
            Alliance network
        alliance_data : DataFrame
            Original alliance data with firm attributes
            
        Returns:
        --------
        diversity_df : DataFrame
            Firm-level partner diversity metrics
        """
        logger.info("Computing partner diversity metrics...")
        
        diversity_metrics = []
        
        for firm in G.nodes():
            partners = list(G.neighbors(firm))
            num_partners = len(partners)
            
            if num_partners == 0:
                diversity_metrics.append({
                    'firm_id': firm,
                    'num_partners': 0,
                    'partner_diversity_hhi': 0,
                    'repeat_partner_ratio': 0
                })
                continue
                
            # Partner concentration (Herfindahl)
            partner_weights = [G[firm][partner]['weight'] for partner in partners]
            total_alliances = sum(partner_weights)
            partner_shares = [w / total_alliances for w in partner_weights]
            hhi = sum(s ** 2 for s in partner_shares)
            diversity_hhi = 1 - hhi  # Higher = more diverse
            
            # Repeat partnership ratio
            repeat_partners = sum(1 for w in partner_weights if w > 1)
            repeat_ratio = repeat_partners / num_partners if num_partners > 0 else 0
            
            diversity_metrics.append({
                'firm_id': firm,
                'num_partners': num_partners,
                'total_alliances': total_alliances,
                'partner_diversity_hhi': diversity_hhi,
                'repeat_partner_ratio': repeat_ratio,
                'avg_alliances_per_partner': total_alliances / num_partners
            })
            
        diversity_df = pd.DataFrame(diversity_metrics)
        return diversity_df
        
    def analyze_partner_selection(
        self,
        alliance_data: pd.DataFrame,
        firm_attributes: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Analyze patterns in partner selection (homophily vs. heterophily).
        
        Parameters:
        -----------
        alliance_data : DataFrame
            Alliance records
        firm_attributes : DataFrame
            Firm attributes (size, industry, location, etc.)
            
        Returns:
        --------
        selection_patterns : DataFrame
            Analysis of partner selection patterns
        """
        logger.info("Analyzing partner selection patterns...")
        
        # Merge firm attributes
        df = alliance_data.merge(
            firm_attributes,
            left_on='firm1_id',
            right_on='firm_id',
            how='left',
            suffixes=('', '_firm1')
        ).merge(
            firm_attributes,
            left_on='firm2_id',
            right_on='firm_id',
            how='left',
            suffixes=('_firm1', '_firm2')
        )
        
        patterns = {}
        
        # Industry homophily
        if 'industry_firm1' in df.columns and 'industry_firm2' in df.columns:
            same_industry = (df['industry_firm1'] == df['industry_firm2']).mean()
            patterns['same_industry_ratio'] = same_industry
            
        # Size similarity
        if 'size_firm1' in df.columns and 'size_firm2' in df.columns:
            # Compute size similarity
            df['size_diff_pct'] = abs(df['size_firm1'] - df['size_firm2']) / \
                                 ((df['size_firm1'] + df['size_firm2']) / 2)
            patterns['avg_size_diff_pct'] = df['size_diff_pct'].mean()
            patterns['similar_size_ratio'] = (df['size_diff_pct'] < 0.5).mean()
            
        # Geographic proximity
        if 'country_firm1' in df.columns and 'country_firm2' in df.columns:
            same_country = (df['country_firm1'] == df['country_firm2']).mean()
            patterns['same_country_ratio'] = same_country
            
        selection_df = pd.DataFrame([patterns])
        return selection_df


class PatentCitationNetworkAnalyzer:
    """
    Analyze patent citation networks for knowledge flow analysis.
    
    Usage:
    ```python
    analyzer = PatentCitationNetworkAnalyzer()
    
    # Input: DataFrame with columns [citing_patent_id, cited_patent_id, year, assignee_id]
    citation_data = pd.read_csv('patent_citations.csv')
    
    # Build network
    G = analyzer.build_citation_network(citation_data)
    
    # Compute knowledge flow metrics
    metrics = analyzer.compute_knowledge_flow_metrics(G, citation_data)
    
    # Identify technological領域
    tech_positions = analyzer.identify_tech_positions(G)
    ```
    """
    
    def __init__(self):
        self.G = None
        
    def build_citation_network(
        self,
        citation_data: pd.DataFrame,
        year_range: Optional[Tuple[int, int]] = None
    ) -> nx.DiGraph:
        """
        Build directed patent citation network.
        
        Parameters:
        -----------
        citation_data : DataFrame
            Must contain: citing_patent_id, cited_patent_id
            Optional: year, assignee_id, ipc_class
        year_range : tuple, optional
            (start_year, end_year) to filter citations
            
        Returns:
        --------
        G : networkx.DiGraph
            Patent citation network (directed: citing -> cited)
        """
        logger.info("Building patent citation network...")
        
        df = citation_data.copy()
        
        # Filter by year range
        if year_range and 'year' in df.columns:
            df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
            
        # Create directed network
        G = nx.DiGraph()
        
        for _, row in df.iterrows():
            citing = row['citing_patent_id']
            cited = row['cited_patent_id']
            
            # Add edge attributes
            attrs = {}
            if 'year' in row:
                attrs['year'] = row['year']
            if 'assignee_id' in row:
                attrs['assignee_id'] = row['assignee_id']
                
            G.add_edge(citing, cited, **attrs)
            
        logger.info(f"Patent network: {G.number_of_nodes()} patents, {G.number_of_edges()} citations")
        
        self.G = G
        return G
        
    def compute_knowledge_flow_metrics(
        self,
        G: nx.DiGraph,
        patent_data: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Compute knowledge flow metrics for each patent/firm.
        
        Metrics:
        - **Forward citations**: Number of times cited (impact)
        - **Backward citations**: Number of citations made (breadth)
        - **Citation lag**: Average time between patent and citations
        - **Self-citations**: Citations within same firm
        - **Generality**: Diversity of technology classes citing the patent
        
        Parameters:
        -----------
        G : networkx.DiGraph
            Patent citation network
        patent_data : DataFrame, optional
            Patent metadata (year, assignee, ipc_class)
            
        Returns:
        --------
        metrics_df : DataFrame
            Patent-level knowledge flow metrics
        """
        logger.info("Computing knowledge flow metrics...")
        
        metrics = []
        
        for patent in G.nodes():
            # Forward citations (in-degree:被引用数)
            forward_citations = G.in_degree(patent)
            
            # Backward citations (out-degree: 引用数)
            backward_citations = G.out_degree(patent)
            
            # PageRank (scientific impact)
            # pagerank = nx.pagerank(G).get(patent, 0)
            
            patent_metrics = {
                'patent_id': patent,
                'forward_citations': forward_citations,
                'backward_citations': backward_citations,
                # 'pagerank_score': pagerank
            }
            
            metrics.append(patent_metrics)
            
        metrics_df = pd.DataFrame(metrics)
        
        # Add patent metadata if provided
        if patent_data is not None:
            metrics_df = metrics_df.merge(
                patent_data[['patent_id', 'year', 'assignee_id']],
                on='patent_id',
                how='left'
            )
            
        logger.info(f"Computed knowledge flow metrics for {len(metrics_df)} patents")
        
        return metrics_df
        
    def compute_firm_level_metrics(
        self,
        G: nx.DiGraph,
        patent_firm_mapping: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Aggregate patent metrics to firm level.
        
        Parameters:
        -----------
        G : networkx.DiGraph
            Patent citation network
        patent_firm_mapping : DataFrame
            Mapping of patent_id to firm_id
            
        Returns:
        --------
        firm_metrics_df : DataFrame
            Firm-level innovation metrics
        """
        logger.info("Computing firm-level innovation metrics...")
        
        # Get patent-level metrics
        patent_metrics = self.compute_knowledge_flow_metrics(G)
        
        # Merge with firm mapping
        df = patent_metrics.merge(patent_firm_mapping, on='patent_id', how='left')
        
        # Aggregate to firm level
        firm_metrics = df.groupby('firm_id').agg({
            'patent_id': 'count',
            'forward_citations': ['sum', 'mean', 'max'],
            'backward_citations': ['sum', 'mean']
        }).reset_index()
        
        firm_metrics.columns = [
            'firm_id',
            'num_patents',
            'total_forward_citations',
            'avg_forward_citations',
            'max_forward_citations',
            'total_backward_citations',
            'avg_backward_citations'
        ]
        
        # Citation impact per patent
        firm_metrics['citations_per_patent'] = \
            firm_metrics['total_forward_citations'] / firm_metrics['num_patents']
            
        return firm_metrics


def export_network_to_gephi(
    G: Union[nx.Graph, nx.DiGraph],
    output_path: str,
    node_attributes: Optional[List[str]] = None
):
    """
    Export network to GEXF format for Gephi visualization.
    
    Parameters:
    -----------
    G : networkx.Graph or DiGraph
        Network to export
    output_path : str
        Output .gexf file path
    node_attributes : list, optional
        List of node attributes to include
    """
    logger.info(f"Exporting network to {output_path}...")
    
    nx.write_gexf(G, output_path)
    logger.info(f"Network exported successfully. Import into Gephi for visualization.")


# Example usage
if __name__ == "__main__":
    # Example 1: Board Interlock Analysis
    print("=" * 80)
    print("Example 1: Board Interlock Network Analysis")
    print("=" * 80)
    
    # Sample board data
    board_data = pd.DataFrame({
        'company_id': ['C1', 'C1', 'C2', 'C2', 'C3', 'C3', 'C4', 'C4', 'C5'],
        'company_name': ['Firm A', 'Firm A', 'Firm B', 'Firm B', 'Firm C', 'Firm C', 'Firm D', 'Firm D', 'Firm E'],
        'director_id': ['D1', 'D2', 'D2', 'D3', 'D3', 'D4', 'D4', 'D5', 'D5'],
        'director_name': ['Alice', 'Bob', 'Bob', 'Carol', 'Carol', 'David', 'David', 'Eve', 'Eve'],
        'year': [2020] * 9
    })
    
    analyzer = BoardInterlockAnalyzer()
    G = analyzer.build_interlock_network(board_data, year=2020)
    metrics = analyzer.compute_network_metrics(G, board_data)
    
    print("\nFirm-level Network Metrics:")
    print(metrics[['company_name', 'degree', 'betweenness_centrality', 
                  'structural_holes_score', 'board_size']].to_string(index=False))
    
    # Detect communities
    communities = analyzer.detect_communities(G)
    print(f"\nDetected {len(set(communities.values()))} communities")
    
    print("\n" + "=" * 80)
    print("Network analysis module ready for use!")
    print("=" * 80)
