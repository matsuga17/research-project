"""
cluster_firms.py

Firm Clustering Example - Strategic Group Analysis

This example demonstrates how to:
1. Generate sample firm data (or load real data)
2. Select features for clustering
3. Find optimal number of clusters
4. Perform K-means clustering
5. Describe and visualize clusters
6. Save results

Usage:
    cd 9-data-mining/examples/firm_clustering/
    python cluster_firms.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from clustering import FirmClusterer


def generate_sample_firms(n_firms: int = 300) -> pd.DataFrame:
    """
    Generate sample firm data with 3 distinct strategic groups
    
    Args:
        n_firms: Number of firms to generate
    
    Returns:
        DataFrame with firm data
    """
    print(f"Generating sample data: {n_firms} firms...")
    
    np.random.seed(42)  # For reproducibility
    
    # Define 3 strategic groups
    # Group 1: Innovators (High R&D, High ROA, Low Leverage)
    # Group 2: Balanced (Medium across all dimensions)
    # Group 3: Cost Leaders (Low R&D, Medium ROA, High Leverage)
    
    n_per_group = n_firms // 3
    
    df = pd.DataFrame({
        'firm_id': range(n_firms),
        'firm_name': [f'Company_{i:03d}' for i in range(n_firms)],
        
        # ROA: Return on Assets
        'roa': np.concatenate([
            np.random.normal(0.12, 0.02, n_per_group),   # Innovators: High
            np.random.normal(0.06, 0.02, n_per_group),   # Balanced: Medium
            np.random.normal(0.04, 0.02, n_firms - 2*n_per_group)  # Cost Leaders: Low-Medium
        ]),
        
        # Sales Growth
        'sales_growth': np.concatenate([
            np.random.normal(0.15, 0.05, n_per_group),   # Innovators: High
            np.random.normal(0.08, 0.04, n_per_group),   # Balanced: Medium
            np.random.normal(0.05, 0.03, n_firms - 2*n_per_group)  # Cost Leaders: Low
        ]),
        
        # R&D Intensity
        'rd_intensity': np.concatenate([
            np.random.uniform(0.08, 0.15, n_per_group),  # Innovators: High
            np.random.uniform(0.02, 0.06, n_per_group),  # Balanced: Medium
            np.random.uniform(0, 0.02, n_firms - 2*n_per_group)    # Cost Leaders: Low
        ]),
        
        # Leverage (Debt/Assets)
        'leverage': np.concatenate([
            np.random.uniform(0.2, 0.4, n_per_group),    # Innovators: Low
            np.random.uniform(0.4, 0.6, n_per_group),    # Balanced: Medium
            np.random.uniform(0.6, 0.8, n_firms - 2*n_per_group)  # Cost Leaders: High
        ]),
        
        # Firm Size (log total assets)
        'firm_size': np.random.lognormal(10, 2, n_firms)
    })
    
    print(f"✓ Generated {len(df)} firms")
    print(f"  Features: {list(df.columns)}")
    print()
    
    return df


def main():
    """Execute firm clustering analysis"""
    
    print("=" * 80)
    print("STRATEGIC GROUP ANALYSIS - FIRM CLUSTERING EXAMPLE")
    print("=" * 80)
    print()
    
    # Step 1: Generate or load data
    print("[Step 1] Data Generation")
    print("-" * 80)
    df = generate_sample_firms(n_firms=300)
    
    print("Sample data preview:")
    print(df.head())
    print()
    
    # Step 2: Select features for clustering
    print("[Step 2] Feature Selection")
    print("-" * 80)
    
    features = ['roa', 'sales_growth', 'rd_intensity', 'leverage']
    print(f"Selected features: {features}")
    print()
    
    # Descriptive statistics
    print("Descriptive statistics:")
    print(df[features].describe().round(3))
    print()
