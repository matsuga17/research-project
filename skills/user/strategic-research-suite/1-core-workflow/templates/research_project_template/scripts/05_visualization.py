"""
05_visualization.py

Data Visualization Script

This script creates standard visualizations for strategic management research:
- Time series plots
- Distribution plots
- Scatter plots with regression lines
- Heatmaps (correlation matrices)
- Panel-specific visualizations

Usage:
    python 05_visualization.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11


def plot_time_series(df: pd.DataFrame, 
                     variable: str,
                     firm_id: str = 'firm_id',
                     time_id: str = 'year',
                     sample_firms: int = 10,
                     aggregate: bool = True) -> plt.Figure:
    """
    Plot time series
    
    Args:
        df: Panel DataFrame
        variable: Variable to plot
        firm_id: Firm identifier
        time_id: Time identifier
        sample_firms: Number of firms to plot individually (0 for aggregate only)
        aggregate: Whether to plot aggregate trend
    
    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot individual firm trajectories (sample)
    if sample_firms > 0:
        firms = df[firm_id].unique()
        sample = np.random.choice(firms, min(sample_firms, len(firms)), replace=False)
        
        for firm in sample:
            firm_data = df[df[firm_id] == firm].sort_values(time_id)
            ax.plot(firm_data[time_id], firm_data[variable], 
                   alpha=0.3, linewidth=1, color='gray')
    
    # Plot aggregate trend
    if aggregate:
        agg_data = df.groupby(time_id)[variable].mean().reset_index()
        ax.plot(agg_data[time_id], agg_data[variable],
               linewidth=2.5, color='red', label='Mean', marker='o')
    
    ax.set_xlabel('Year')
    ax.set_ylabel(variable.replace('_', ' ').title())
    ax.set_title(f'Time Series: {variable.replace("_", " ").title()}')
    if aggregate:
        ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_distribution(df: pd.DataFrame,
                     variables: list,
                     bins: int = 30) -> plt.Figure:
    """
    Plot distribution histograms
    
    Args:
        df: DataFrame
        variables: List of variables to plot
        bins: Number of bins
    
    Returns:
        matplotlib Figure
    """
    n_vars = len(variables)
    n_cols = min(3, n_vars)
    n_rows = (n_vars + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
    
    if n_vars == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for i, var in enumerate(variables):
        if var in df.columns:
            axes[i].hist(df[var].dropna(), bins=bins, alpha=0.7, color='steelblue', edgecolor='black')
            axes[i].set_xlabel(var.replace('_', ' ').title())
            axes[i].set_ylabel('Frequency')
            axes[i].set_title(f'Distribution: {var.replace("_", " ").title()}')
            axes[i].grid(True, alpha=0.3)
    
    # Hide empty subplots
    for i in range(n_vars, len(axes)):
        axes[i].axis('off')
    
    plt.tight_layout()
    return fig


def plot_scatter(df: pd.DataFrame,
                x_var: str,
                y_var: str,
                fit_line: bool = True) -> plt.Figure:
    """
    Create scatter plot with optional regression line
    
    Args:
        df: DataFrame
        x_var: X-axis variable
        y_var: Y-axis variable
        fit_line: Whether to add regression line
    
    Returns:
        matplotlib Figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Drop missing values
    plot_data = df[[x_var, y_var]].dropna()
    
    # Scatter plot
    ax.scatter(plot_data[x_var], plot_data[y_var], 
              alpha=0.5, s=30, color='steelblue')
    
    # Add regression line
    if fit_line:
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            plot_data[x_var], plot_data[y_var]
        )
        line_x = np.array([plot_data[x_var].min(), plot_data[x_var].max()])
        line_y = slope * line_x + intercept
        ax.plot(line_x, line_y, 'r-', linewidth=2, 
               label=f'R² = {r_value**2:.3f}')
        ax.legend()
    
    ax.set_xlabel(x_var.replace('_', ' ').title())
    ax.set_ylabel(y_var.replace('_', ' ').title())
    ax.set_title(f'{y_var.replace("_", " ").title()} vs {x_var.replace("_", " ").title()}')
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_correlation_heatmap(df: pd.DataFrame,
                            variables: list = None,
                            annot: bool = True) -> plt.Figure:
    """
    Create correlation heatmap
    
    Args:
        df: DataFrame
        variables: List of variables (default: all numeric)
        annot: Whether to annotate cells with values
    
    Returns:
        matplotlib Figure
    """
    if variables is None:
        variables = df.select_dtypes(include=[np.number]).columns.tolist()
    
    corr = df[variables].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr, annot=annot, fmt='.2f', cmap='coolwarm', 
               center=0, square=True, linewidths=1,
               cbar_kws={"shrink": 0.8}, ax=ax)
    
    ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def main():
    """Main execution function"""
    
    logger.info("=" * 60)
    logger.info("Data Visualization Pipeline")
    logger.info("=" * 60)
    
    # Define paths
    base_dir = Path(__file__).parent.parent
    final_data_dir = base_dir / 'data' / 'final'
    output_dir = base_dir / 'output' / 'figures'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Load data
    logger.info("\n[Step 1] Loading analysis dataset...")
    data_file = final_data_dir / 'analysis_dataset.csv'
    
    if not data_file.exists():
        logger.error(f"Analysis dataset not found: {data_file}")
        logger.error("Please run 03_variable_construction.py first")
        return
    
    df = pd.read_csv(data_file)
    logger.info(f"Loaded {len(df)} observations")
    
    # Identify key variables
    key_vars = []
    for var in ['roa', 'sales_growth', 'rd_intensity', 'leverage']:
        if var in df.columns:
            key_vars.append(var)
    
    if not key_vars:
        logger.warning("No key variables found in dataset")
        return
    
    # Step 2: Time series plots
    logger.info("\n[Step 2] Creating time series plots...")
    for var in key_vars:
        try:
            fig = plot_time_series(df, variable=var, sample_firms=5)
            filename = output_dir / f'timeseries_{var}.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Saved: {filename.name}")
            plt.close(fig)
        except Exception as e:
            logger.warning(f"  ✗ Could not plot {var}: {e}")
    
    # Step 3: Distribution plots
    logger.info("\n[Step 3] Creating distribution plots...")
    try:
        fig = plot_distribution(df, variables=key_vars)
        filename = output_dir / 'distributions.png'
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"  ✓ Saved: {filename.name}")
        plt.close(fig)
    except Exception as e:
        logger.warning(f"  ✗ Could not create distribution plots: {e}")
    
    # Step 4: Scatter plots
    logger.info("\n[Step 4] Creating scatter plots...")
    
    # Example: R&D intensity vs ROA
    if 'rd_intensity' in df.columns and 'roa' in df.columns:
        try:
            fig = plot_scatter(df, x_var='rd_intensity', y_var='roa')
            filename = output_dir / 'scatter_rd_roa.png'
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            logger.info(f"  ✓ Saved: {filename.name}")
            plt.close(fig)
        except Exception as e:
            logger.warning(f"  ✗ Could not create scatter plot: {e}")
    
    # Step 5: Correlation heatmap
    logger.info("\n[Step 5] Creating correlation heatmap...")
    try:
        fig = plot_correlation_heatmap(df, variables=key_vars)
        filename = output_dir / 'correlation_heatmap.png'
        fig.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"  ✓ Saved: {filename.name}")
        plt.close(fig)
    except Exception as e:
        logger.warning(f"  ✗ Could not create heatmap: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Visualization completed successfully!")
    logger.info("=" * 60)
    logger.info(f"Figures saved to: {output_dir}")


if __name__ == "__main__":
    main()
