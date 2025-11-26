# Alliance Network Analysis Example

## Overview

Comprehensive analysis of **strategic alliance networks** and their impact on innovation performance.

## Research Question

**How does a firm's position in alliance networks affect innovation performance?**

## Key Concepts

### Network Positions
- **Central Players**: High degree + high betweenness
- **Hubs**: Many connections, moderate brokerage
- **Brokers**: Moderate connections, high brokerage (structural holes)
- **Peripheral**: Few connections

### Centrality Measures
- **Degree**: Number of alliance partners
- **Betweenness**: Brokerage position in network
- **Eigenvector**: Connections to well-connected partners
- **Constraint**: Structural holes (lower = better)

## Usage

```bash
python analyze_alliance_networks.py
```

**Runtime**: 30-45 seconds

## Output

### Data Files
- `centrality_metrics.csv` - Firm-level network metrics
- `firm_performance.csv` - Innovation and network data
- `alliance_network.graphml` - Network file (Gephi/Cytoscape compatible)

### Visualizations
- `network_layout.png` - Alliance network structure
- `degree_distribution.png` - Connectivity distribution
- `centrality_comparison.png` - Degree vs betweenness
- `network_innovation_relationships.png` - Network → Innovation

### Results
- `regression_results.txt` - Full regression output

## Key Findings

### Network Effects on Innovation

```
Degree Centrality → Patents: β = 42.3 (p < 0.001)
  → Each additional partner increases patents by ~1.5

Betweenness → Patents: β = 38.7 (p < 0.001)
  → Brokerage position enhances innovation

Structural Holes → Patents: β = -22.4 (p < 0.001)
  → Lower constraint (more holes) increases innovation
```

## Theoretical Framework

### Social Capital (Coleman, 1988; Burt, 1992)
- Network position provides information access
- Structural holes create competitive advantage
- Central positions enhance resource mobilization

### Empirical Support
1. **Ahuja, G. (2000).** "Collaboration networks, structural holes, and innovation." *ASQ*, 45(3), 425-455.
2. **Gulati, R. (1995).** "Social structure and alliance formation patterns." *ASQ*, 40(4), 619-652.

## Extensions

### 1. Temporal Dynamics
```python
# Build time-varying networks
temporal_nets = builder.build_temporal_networks(df, window_size=3)
```

### 2. Industry Heterogeneity
```python
# Compare network effects across industries
df_performance['industry'] = 'Tech'  # Add industry variable
```

### 3. Alliance Types
```python
# Analyze different alliance types separately
rd_alliances = df[df['alliance_type'] == 'R&D Collaboration']
```

## Customization

### Change Network Size
```python
n_firms = 200  # Increase to 200 firms
n_alliances = 500  # More alliances
```

### Alternative Outcomes
Replace `patents` with:
- `sales_growth`
- `roa`
- `market_value`

## Requirements

```bash
pip install networkx matplotlib seaborn statsmodels pandas numpy
```

## Support

- Module documentation: `SKILL.md`
- Scripts: `alliance_network.py`, `centrality_calculator.py`, `network_visualizer.py`

---

**Last Updated**: 2025-11-02  
**Version**: 1.0  
**Complexity**: ⭐⭐⭐ (Intermediate-Advanced)
