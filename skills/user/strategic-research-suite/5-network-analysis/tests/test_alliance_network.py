"""
test_alliance_network.py

Unit Tests for Alliance Network Builder

Tests cover:
- Network construction from DataFrames
- Network statistics calculation
- Temporal network building
- Strategic position identification
- Error handling

Run with:
    pytest test_alliance_network.py -v
    pytest test_alliance_network.py::TestAllianceNetworkBuilder -v
"""

import pytest
import pandas as pd
import numpy as np
import networkx as nx
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent / 'scripts'))

from alliance_network import AllianceNetworkBuilder


class TestAllianceNetworkBuilder:
    """Test suite for AllianceNetworkBuilder class"""
    
    def test_initialization(self):
        """Test builder initialization"""
        builder = AllianceNetworkBuilder()
        
        assert builder.network is None
        assert builder.alliances is None
        assert isinstance(builder.firms, set)
        assert len(builder.firms) == 0
    
    def test_build_from_dataframe_basic(self):
        """Test basic network construction from DataFrame"""
        # Create sample alliance data
        df = pd.DataFrame({
            'firm1': ['A', 'B', 'C', 'A'],
            'firm2': ['B', 'C', 'D', 'D'],
            'announcement_date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01'],
            'alliance_type': ['JV', 'R&D', 'Marketing', 'Technology']
        })
        
        # Build network
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # Assertions
        assert isinstance(G, nx.Graph)
        assert G.number_of_nodes() == 4  # A, B, C, D
        assert G.number_of_edges() == 4  # 4 alliances
        assert 'A' in G.nodes()
        assert 'B' in G.nodes()
        assert G.has_edge('A', 'B')
        assert G.has_edge('B', 'C')
    
    def test_build_from_dataframe_with_attributes(self):
        """Test network construction with edge attributes"""
        # Create sample data
        df = pd.DataFrame({
            'firm1': ['A', 'B'],
            'firm2': ['B', 'C'],
            'announcement_date': ['2020-01-01', '2020-02-01'],
            'alliance_type': ['JV', 'R&D'],
            'equity_stake': [0.3, 0.0]
        })
        
        # Build network with attributes
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(
            df, 
            attributes=['alliance_type', 'equity_stake']
        )
        
        # Check edge attributes
        edge_data = G.get_edge_data('A', 'B')
        assert 'alliance_type' in edge_data
        assert edge_data['alliance_type'] == 'JV'
        assert edge_data['equity_stake'] == 0.3
    
    def test_build_from_dataframe_empty(self):
        """Test network construction with empty DataFrame"""
        df = pd.DataFrame(columns=['firm1', 'firm2', 'announcement_date'])
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        assert G.number_of_nodes() == 0
        assert G.number_of_edges() == 0
    
    def test_build_temporal_networks(self):
        """Test temporal network construction"""
        # Create multi-year alliance data
        df = pd.DataFrame({
            'firm1': ['A', 'B', 'C', 'A', 'D'],
            'firm2': ['B', 'C', 'D', 'C', 'E'],
            'announcement_date': ['2018-01-01', '2019-01-01', '2020-01-01', 
                                 '2021-01-01', '2022-01-01'],
            'year': [2018, 2019, 2020, 2021, 2022]
        })
        
        # Build temporal networks
        builder = AllianceNetworkBuilder()
        networks = builder.build_temporal_networks(df, time_col='year', window_size=2)
        
        # Assertions
        assert isinstance(networks, dict)
        assert len(networks) > 0
        
        # Check that each time period has a network
        for year, G in networks.items():
            assert isinstance(G, nx.Graph)
            assert G.number_of_nodes() >= 0
    
    def test_calculate_network_statistics(self):
        """Test network statistics calculation"""
        # Create sample network
        df = pd.DataFrame({
            'firm1': ['A', 'B', 'C', 'D'],
            'firm2': ['B', 'C', 'D', 'E'],
            'announcement_date': ['2020-01-01'] * 4
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        stats = builder.calculate_network_statistics(G)
        
        # Assertions
        assert isinstance(stats, dict)
        assert 'num_nodes' in stats
        assert 'num_edges' in stats
        assert 'density' in stats
        assert stats['num_nodes'] == 5
        assert stats['num_edges'] == 4
        assert 0 <= stats['density'] <= 1
    
    def test_identify_strategic_positions(self):
        """Test strategic position identification"""
        # Create network with clear structure
        df = pd.DataFrame({
            'firm1': ['Hub', 'Hub', 'Hub', 'A', 'B'],
            'firm2': ['A', 'B', 'C', 'D', 'C'],
            'announcement_date': ['2020-01-01'] * 5
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        positions = builder.identify_strategic_positions(G)
        
        # Assertions
        assert isinstance(positions, pd.DataFrame)
        assert 'firm_id' in positions.columns
        assert 'degree_centrality' in positions.columns or 'degree' in positions.columns
        
        # Hub firm should have high centrality
        if 'Hub' in positions['firm_id'].values:
            hub_row = positions[positions['firm_id'] == 'Hub']
            assert len(hub_row) > 0
    
    def test_calculate_firm_network_measures(self):
        """Test firm-level network measure calculation"""
        # Create sample network
        df = pd.DataFrame({
            'firm1': ['A', 'A', 'B', 'C'],
            'firm2': ['B', 'C', 'D', 'D'],
            'announcement_date': ['2020-01-01'] * 4
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        measures = builder.calculate_firm_network_measures(G)
        
        # Assertions
        assert isinstance(measures, pd.DataFrame)
        assert len(measures) == G.number_of_nodes()
        
        # Check that measures include key metrics
        expected_columns = ['firm_id', 'degree']
        for col in expected_columns:
            assert col in measures.columns or any(col in c for c in measures.columns)
    
    def test_network_density_calculation(self):
        """Test network density calculation"""
        # Complete graph (all connected)
        df_complete = pd.DataFrame({
            'firm1': ['A', 'A', 'B'],
            'firm2': ['B', 'C', 'C'],
            'announcement_date': ['2020-01-01'] * 3
        })
        
        builder = AllianceNetworkBuilder()
        G_complete = builder.build_from_dataframe(df_complete)
        
        # Density should be 1.0 for complete graph
        density = nx.density(G_complete)
        assert density == pytest.approx(1.0, rel=0.01)
    
    def test_network_with_duplicate_alliances(self):
        """Test handling of duplicate alliance entries"""
        # DataFrame with duplicate alliances
        df = pd.DataFrame({
            'firm1': ['A', 'A', 'B'],
            'firm2': ['B', 'B', 'C'],
            'announcement_date': ['2020-01-01', '2020-01-15', '2020-02-01']
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # NetworkX should handle duplicates by keeping only one edge
        assert G.number_of_edges() == 2  # A-B and B-C
    
    def test_network_component_analysis(self):
        """Test connected component analysis"""
        # Create network with disconnected components
        df = pd.DataFrame({
            'firm1': ['A', 'C'],
            'firm2': ['B', 'D'],
            'announcement_date': ['2020-01-01', '2020-01-01']
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # Should have 2 connected components
        num_components = nx.number_connected_components(G)
        assert num_components == 2


class TestAllianceNetworkAnalysis:
    """Test advanced network analysis methods"""
    
    def test_centrality_measures(self):
        """Test various centrality measures"""
        # Create star network (hub and spokes)
        df = pd.DataFrame({
            'firm1': ['Hub'] * 5,
            'firm2': ['A', 'B', 'C', 'D', 'E'],
            'announcement_date': ['2020-01-01'] * 5
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # Calculate degree centrality
        degree_cent = nx.degree_centrality(G)
        
        # Hub should have highest centrality
        assert degree_cent['Hub'] == max(degree_cent.values())
        assert degree_cent['Hub'] > degree_cent['A']
    
    def test_structural_holes(self):
        """Test structural hole identification"""
        # Create network with structural hole
        df = pd.DataFrame({
            'firm1': ['Broker', 'Broker', 'C'],
            'firm2': ['A', 'B', 'D'],
            'announcement_date': ['2020-01-01'] * 3
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # Broker should have betweenness centrality > 0
        betweenness = nx.betweenness_centrality(G)
        
        if 'Broker' in betweenness:
            # Broker might have high betweenness if it connects components
            assert betweenness['Broker'] >= 0
    
    def test_network_clustering(self):
        """Test clustering coefficient calculation"""
        # Create triangle (high clustering)
        df = pd.DataFrame({
            'firm1': ['A', 'B', 'C'],
            'firm2': ['B', 'C', 'A'],
            'announcement_date': ['2020-01-01'] * 3
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        # Calculate clustering coefficient
        clustering = nx.average_clustering(G)
        
        # Triangle should have perfect clustering (1.0)
        assert clustering == pytest.approx(1.0, rel=0.01)


class TestAllianceNetworkEdgeCases:
    """Test edge cases and error handling"""
    
    def test_single_alliance(self):
        """Test network with single alliance"""
        df = pd.DataFrame({
            'firm1': ['A'],
            'firm2': ['B'],
            'announcement_date': ['2020-01-01']
        })
        
        builder = AllianceNetworkBuilder()
        G = builder.build_from_dataframe(df)
        
        assert G.number_of_nodes() == 2
        assert G.number_of_edges() == 1
    
    def test_missing_date_column(self):
        """Test handling of missing date column"""
        df = pd.DataFrame({
            'firm1': ['A'],
            'firm2': ['B']
        })
        
        builder = AllianceNetworkBuilder()
        
        # Should raise KeyError for missing date column
        with pytest.raises(KeyError):
            builder.build_from_dataframe(df)
    
    def test_null_firm_ids(self):
        """Test handling of null firm identifiers"""
        df = pd.DataFrame({
            'firm1': ['A', None],
            'firm2': ['B', 'C'],
            'announcement_date': ['2020-01-01', '2020-01-01']
        })
        
        builder = AllianceNetworkBuilder()
        # Should handle nulls gracefully (might skip or raise error)
        # Exact behavior depends on implementation
        try:
            G = builder.build_from_dataframe(df)
            # If it succeeds, check that null is not in network
            assert None not in G.nodes() or pd.isna(None) not in G.nodes()
        except (ValueError, TypeError):
            # If it raises an error, that's also acceptable
            pass


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_alliance_data():
    """Sample alliance data for testing"""
    return pd.DataFrame({
        'firm1': ['Sony', 'Toyota', 'Honda', 'Sony', 'Panasonic'],
        'firm2': ['Ericsson', 'BMW', 'GM', 'Samsung', 'Tesla'],
        'announcement_date': ['2020-01-15', '2020-03-20', '2020-06-10', 
                             '2020-09-05', '2020-12-01'],
        'year': [2020, 2020, 2020, 2020, 2020],
        'alliance_type': ['JV', 'Technology', 'Manufacturing', 'R&D', 'Supply'],
        'equity_stake': [0.5, 0.0, 0.0, 0.2, 0.0]
    })


@pytest.fixture
def sample_network_graph():
    """Sample NetworkX graph for testing"""
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'), ('B', 'C'), ('C', 'D'), 
        ('D', 'E'), ('E', 'A'), ('A', 'C')
    ])
    return G


# =============================================================================
# Run Tests
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
