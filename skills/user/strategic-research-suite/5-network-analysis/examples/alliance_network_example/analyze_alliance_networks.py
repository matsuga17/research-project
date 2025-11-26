"""
analyze_alliance_networks.py

Complete Example: Strategic Alliance Network Analysis

Research Question:
How does a firm's position in alliance networks affect innovation performance?

Methods Demonstrated:
1. Alliance network construction
2. Centrality measures (degree, betweenness, eigenvector)
3. Structural holes (constraint measure)
4. Alliance portfolio analysis
5. Network visualization
6. Regression analysis with network metrics

Expected Output:
- Network statistics
- Firm-level centrality metrics
- Strategic position identification
- Network visualizations
- Regression results
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))

from alliance_network import AllianceNetworkBuilder
from centrality_calculator import CentralityCalculator
from network_visualizer import NetworkVisualizer

print("=" * 80)
print("STRATEGIC ALLIANCE NETWORK ANALYSIS")
print("=" * 80)

# =============================================================================
# Phase 1: Data Generation
# =============================================================================

print("\n[Phase 1] Generating Alliance Network Data")
print("-" * 80)

np.random.seed(42)

# 100 firms in technology industry
n_firms = 100
firms = [f'FIRM{i:03d}' for i in range(1, n_firms + 1)]

# Generate alliance data (2015-2022)
alliances = []

# Core firms (high alliance propensity)
core_firms = firms[:20]

# Generate 300 alliances over 8 years
for _ in range(300):
    year = np.random.randint(2015, 2023)
    
    # Higher probability for core firms
    if np.random.random() < 0.6:
        # Alliance involving at least one core firm
        firm1 = np.random.choice(core_firms)
        firm2 = np.random.choice([f for f in firms if f != firm1])
    else:
        # Random alliance
        firm1, firm2 = np.random.choice(firms, 2, replace=False)
    
    alliance_type = np.random.choice([
        'R&D Collaboration', 
        'Technology Licensing',
        'Joint Venture',
        'Marketing Alliance',
        'Supply Chain'
    ], p=[0.35, 0.25, 0.15, 0.15, 0.10])
    
    alliances.append({
        'firm1': firm1,
        'firm2': firm2,
        'year': year,
        'alliance_type': alliance_type,
        'announcement_date': f'{year}-{np.random.randint(1,13):02d}-01'
    })

df_alliances = pd.DataFrame(alliances)

print(f"✓ Generated alliance data:")
print(f"  Alliances: {len(df_alliances)}")
print(f"  Time period: {df_alliances['year'].min()}-{df_alliances['year'].max()}")
print(f"  Alliance types: {df_alliances['alliance_type'].nunique()}")

print("\nAlliance type distribution:")
print(df_alliances['alliance_type'].value_counts())

# =============================================================================
# Phase 2: Build Alliance Network
# =============================================================================

print("\n[Phase 2] Building Alliance Network")
print("-" * 80)

# Initialize builder
builder = AllianceNetworkBuilder()

# Build full network
network = builder.build_from_dataframe(
    df=df_alliances,
    firm1_col='firm1',
    firm2_col='firm2',
    date_col='announcement_date',
    attributes=['alliance_type']
)

# Calculate network statistics
stats = builder.calculate_network_statistics()

print("\nNetwork Statistics:")
print(f"  Nodes (firms): {stats['n_firms']}")
print(f"  Edges (alliances): {stats['n_alliances']}")
print(f"  Density: {stats['density']:.4f}")
print(f"  Connected: {stats['is_connected']}")
print(f"  Components: {stats['n_components']}")
print(f"  Avg degree: {stats['avg_degree']:.2f}")
print(f"  Avg clustering: {stats['avg_clustering']:.4f}")
print(f"  Avg path length: {stats['avg_path_length']:.2f}")
print(f"  Diameter: {stats['diameter']}")

# =============================================================================
# Phase 3: Calculate Centrality Metrics
# =============================================================================

print("\n[Phase 3] Calculating Firm-Level Centrality Metrics")
print("-" * 80)

# Initialize centrality calculator
calc = CentralityCalculator(network)

# Calculate all centrality measures
centrality_metrics = calc.calculate_all_centralities()

print(f"✓ Calculated centrality metrics for {len(centrality_metrics)} firms")

# Calculate structural holes
constraint = calc.calculate_constraint()
centrality_metrics = centrality_metrics.merge(
    constraint,
    left_on='node',
    right_on='node',
    how='left'
)

print("\nTop 5 firms by degree centrality:")
print(centrality_metrics.nlargest(5, 'degree_centrality')[['node', 'degree_centrality', 'degree']])

print("\nTop 5 firms by betweenness (brokers):")
print(centrality_metrics.nlargest(5, 'betweenness_centrality')[['node', 'betweenness_centrality']])

print("\nTop 5 firms by structural holes (low constraint):")
print(centrality_metrics.nsmallest(5, 'constraint')[['node', 'constraint']])

# =============================================================================
# Phase 4: Identify Strategic Positions
# =============================================================================

print("\n[Phase 4] Identifying Strategic Network Positions")
print("-" * 80)

positions = builder.identify_strategic_positions()

print("Strategic Position Distribution:")
for pos_type, firm_list in positions.items():
    print(f"  {pos_type.title()}: {len(firm_list)} firms")
    if len(firm_list) > 0 and len(firm_list) <= 3:
        print(f"    {firm_list}")

# =============================================================================
# Phase 5: Alliance Portfolio Analysis
# =============================================================================

print("\n[Phase 5] Alliance Portfolio Analysis")
print("-" * 80)

# Analyze portfolio for top central firms
if len(positions['central_players']) > 0:
    focal_firm = positions['central_players'][0]
    
    portfolio = builder.analyze_alliance_portfolio(focal_firm)
    
    print(f"\nAlliance Portfolio: {focal_firm}")
    print(f"  Portfolio size: {portfolio['portfolio_size']} partners")
    print(f"  Network reach: {portfolio['network_reach']} second-order connections")
    print(f"  Redundancy: {portfolio['redundancy']:.3f}")
    print(f"  Avg partner degree: {portfolio['avg_partner_degree']:.2f}")
    
    print(f"\n  Partners: {portfolio['partners'][:5]}...")

# =============================================================================
# Phase 6: Add Innovation Performance Data
# =============================================================================

print("\n[Phase 6] Generating Innovation Performance Data")
print("-" * 80)

# Generate firm performance data
# Performance is positively related to network centrality

performance_data = []

for firm in firms:
    # Get centrality metrics
    firm_metrics = centrality_metrics[centrality_metrics['node'] == firm]
    
    if len(firm_metrics) > 0:
        degree_cent = firm_metrics['degree_centrality'].values[0]
        betweenness = firm_metrics['betweenness_centrality'].values[0]
        constraint_val = firm_metrics['constraint'].values[0] if 'constraint' in firm_metrics.columns else 0.5
    else:
        # Isolated firm
        degree_cent = 0
        betweenness = 0
        constraint_val = 1.0
    
    # Innovation output (patents)
    # Positively related to centrality, negatively to constraint
    base_patents = 10
    centrality_effect = 30 * degree_cent
    structural_holes_effect = 20 * (1 - constraint_val)
    noise = np.random.normal(0, 5)
    
    patents = max(0, base_patents + centrality_effect + structural_holes_effect + noise)
    
    # Firm characteristics
    firm_size = np.random.normal(10, 1.5)
    rd_intensity = np.random.uniform(0.05, 0.15)
    
    performance_data.append({
        'firm_id': firm,
        'patents': patents,
        'firm_size': firm_size,
        'rd_intensity': rd_intensity,
        'degree_centrality': degree_cent,
        'betweenness_centrality': betweenness,
        'constraint': constraint_val
    })

df_performance = pd.DataFrame(performance_data)

print(f"✓ Performance data generated for {len(df_performance)} firms")

# Summary statistics
print("\nInnovation Performance Summary:")
print(df_performance[['patents', 'degree_centrality', 'betweenness_centrality', 'constraint']].describe())

# =============================================================================
# Phase 7: Regression Analysis
# =============================================================================

print("\n[Phase 7] Regression Analysis: Network Position → Innovation")
print("-" * 80)

try:
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    
    # Model 1: Degree centrality
    formula1 = 'patents ~ degree_centrality + firm_size + rd_intensity'
    model1 = ols(formula1, data=df_performance).fit()
    
    print("\n[Model 1: Degree Centrality → Patents]")
    print(model1.summary().tables[1])
    
    # Model 2: Betweenness centrality (brokerage)
    formula2 = 'patents ~ betweenness_centrality + firm_size + rd_intensity'
    model2 = ols(formula2, data=df_performance).fit()
    
    print("\n[Model 2: Betweenness Centrality → Patents]")
    print(model2.summary().tables[1])
    
    # Model 3: Structural holes (constraint)
    formula3 = 'patents ~ constraint + firm_size + rd_intensity'
    model3 = ols(formula3, data=df_performance).fit()
    
    print("\n[Model 3: Structural Holes (Constraint) → Patents]")
    print(model3.summary().tables[1])
    
    # Model 4: Combined
    formula4 = 'patents ~ degree_centrality + betweenness_centrality + constraint + firm_size + rd_intensity'
    model4 = ols(formula4, data=df_performance).fit()
    
    print("\n[Model 4: Combined Network Effects]")
    print(model4.summary().tables[1])

except ImportError:
    print("\nstatsmodels not available. Install with: pip install statsmodels")
    print("Skipping regression analysis...")

# =============================================================================
# Phase 8: Visualization
# =============================================================================

print("\n[Phase 8] Generating Network Visualizations")
print("-" * 80)

# Create output directory
output_dir = Path(__file__).parent / 'output'
output_dir.mkdir(exist_ok=True)

# Initialize visualizer
viz = NetworkVisualizer(network)

# Figure 1: Network layout
print("\nGenerating network layout...")
fig1 = viz.plot_network_layout(
    node_size_by='degree',
    node_color_by='betweenness_centrality',
    layout='spring',
    figsize=(14, 10)
)
fig1.savefig(output_dir / 'network_layout.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: network_layout.png")

# Figure 2: Degree distribution
print("\nGenerating degree distribution...")
fig2 = viz.plot_degree_distribution()
fig2.savefig(output_dir / 'degree_distribution.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: degree_distribution.png")

# Figure 3: Centrality comparison
print("\nGenerating centrality scatter plot...")
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.scatter(
    centrality_metrics['degree_centrality'],
    centrality_metrics['betweenness_centrality'],
    alpha=0.6, s=100
)
ax3.set_xlabel('Degree Centrality')
ax3.set_ylabel('Betweenness Centrality')
ax3.set_title('Degree vs Betweenness Centrality')
ax3.grid(alpha=0.3)
plt.tight_layout()
fig3.savefig(output_dir / 'centrality_comparison.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: centrality_comparison.png")

# Figure 4: Network position and innovation
if 'model1' in locals():
    fig4, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Degree centrality
    axes[0].scatter(df_performance['degree_centrality'], df_performance['patents'], alpha=0.6)
    axes[0].set_xlabel('Degree Centrality')
    axes[0].set_ylabel('Patents')
    axes[0].set_title('Degree Centrality → Innovation')
    axes[0].grid(alpha=0.3)
    
    # Betweenness centrality
    axes[1].scatter(df_performance['betweenness_centrality'], df_performance['patents'], alpha=0.6)
    axes[1].set_xlabel('Betweenness Centrality')
    axes[1].set_ylabel('Patents')
    axes[1].set_title('Betweenness → Innovation')
    axes[1].grid(alpha=0.3)
    
    # Structural holes (constraint)
    axes[2].scatter(df_performance['constraint'], df_performance['patents'], alpha=0.6)
    axes[2].set_xlabel('Constraint (Higher = Fewer Structural Holes)')
    axes[2].set_ylabel('Patents')
    axes[2].set_title('Structural Holes → Innovation')
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    fig4.savefig(output_dir / 'network_innovation_relationships.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: network_innovation_relationships.png")

plt.close('all')

# =============================================================================
# Phase 9: Save Results
# =============================================================================

print("\n[Phase 9] Saving Results")
print("-" * 80)

# Save centrality metrics
centrality_metrics.to_csv(output_dir / 'centrality_metrics.csv', index=False)
print(f"✓ Saved: centrality_metrics.csv")

# Save performance data
df_performance.to_csv(output_dir / 'firm_performance.csv', index=False)
print(f"✓ Saved: firm_performance.csv")

# Save network (GraphML format for Gephi/Cytoscape)
builder.export_network(output_dir / 'alliance_network.graphml', format='graphml')
print(f"✓ Saved: alliance_network.graphml")

# Save regression results
if 'model1' in locals():
    with open(output_dir / 'regression_results.txt', 'w') as f:
        f.write("Model 1: Degree Centrality\n")
        f.write("=" * 80 + "\n")
        f.write(str(model1.summary()))
        f.write("\n\nModel 2: Betweenness Centrality\n")
        f.write("=" * 80 + "\n")
        f.write(str(model2.summary()))
        f.write("\n\nModel 3: Structural Holes\n")
        f.write("=" * 80 + "\n")
        f.write(str(model3.summary()))
        f.write("\n\nModel 4: Combined Effects\n")
        f.write("=" * 80 + "\n")
        f.write(str(model4.summary()))
    
    print(f"✓ Saved: regression_results.txt")

# =============================================================================
# Summary Report
# =============================================================================

print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

print(f"""
Network Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Firms: {stats['n_firms']}
  Alliances: {stats['n_alliances']}
  Density: {stats['density']:.4f}
  Avg Clustering: {stats['avg_clustering']:.4f}
  Avg Path Length: {stats['avg_path_length']:.2f}

Strategic Positions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Central Players: {len(positions['central_players'])} firms (high degree + betweenness)
  Hubs: {len(positions['hubs'])} firms (high degree, moderate betweenness)
  Brokers: {len(positions['brokers'])} firms (moderate degree, high betweenness)
  Peripheral: {len(positions['peripheral'])} firms (low connectivity)
""")

if 'model4' in locals():
    print(f"""
Key Findings (Regression Results):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model 1 - Degree Centrality:
  Coefficient: {model1.params['degree_centrality']:.3f} (p = {model1.pvalues['degree_centrality']:.4f})
  R-squared: {model1.rsquared:.4f}
  Interpretation: Higher connectivity → more innovation

Model 2 - Betweenness Centrality:
  Coefficient: {model2.params['betweenness_centrality']:.3f} (p = {model2.pvalues['betweenness_centrality']:.4f})
  R-squared: {model2.rsquared:.4f}
  Interpretation: Brokerage position → innovation advantage

Model 3 - Structural Holes:
  Coefficient: {model3.params['constraint']:.3f} (p = {model3.pvalues['constraint']:.4f})
  R-squared: {model3.rsquared:.4f}
  Interpretation: Fewer structural holes → more innovation

Model 4 - Combined:
  R-squared: {model4.rsquared:.4f}
  Controls included: firm_size, rd_intensity
""")

print(f"""
Output Files:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Data:
  • centrality_metrics.csv - Firm-level network metrics
  • firm_performance.csv - Performance and network data
  • alliance_network.graphml - Network for Gephi/Cytoscape

Results:
  • regression_results.txt - Full regression output

Visualizations:
  • network_layout.png - Network structure visualization
  • degree_distribution.png - Degree distribution
  • centrality_comparison.png - Centrality measures comparison
  • network_innovation_relationships.png - Network position → Innovation

Location: {output_dir}
""")

print("\n" + "=" * 80)
print("THEORETICAL IMPLICATIONS")
print("=" * 80)

print("""
Social Capital Theory (Coleman, 1988; Burt, 1992):
  • Network position provides access to information and resources
  • Central firms have information advantages
  • Structural holes create brokerage opportunities

Empirical Evidence from this Analysis:
  • Degree centrality: More partners → more innovation
  • Betweenness: Brokerage position provides unique information access
  • Structural holes: Non-redundant ties enhance information diversity

Managerial Implications:
  1. Strategic alliance formation should consider network position
  2. Brokerage positions offer innovation advantages
  3. Portfolio diversity (structural holes) matters for knowledge access
  4. Not all network positions are equally valuable
""")

print("\n" + "=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
