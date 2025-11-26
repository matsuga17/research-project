"""
run_example.py

Basic Workflow Example - Complete End-to-End Demo

This script demonstrates a complete research workflow:
1. Generate sample panel data
2. Run quality checks
3. Calculate descriptive statistics
4. Perform correlation analysis
5. Save results

Usage:
    cd 1-core-workflow/examples/basic_workflow/
    python run_example.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from data_quality_checker import DataQualityChecker


def generate_sample_data(n_firms: int = 100, n_years: int = 10) -> pd.DataFrame:
    """
    Generate sample panel dataset
    
    Args:
        n_firms: Number of firms
        n_years: Number of years per firm
    
    Returns:
        Panel dataset with firm-year observations
    """
    print(f"Generating sample data: {n_firms} firms × {n_years} years...")
    
    np.random.seed(42)  # For reproducibility
    
    data = []
    for firm in range(1, n_firms + 1):
        for year in range(2013, 2013 + n_years):
            data.append({
                'firm_id': firm,
                'year': year,
                'firm_name': f'Company_{firm:03d}',
                'roa': np.random.normal(0.05, 0.02),  # 5% average ROA
                'roe': np.random.normal(0.10, 0.04),  # 10% average ROE
                'sales': np.random.lognormal(10, 2),  # Log-normal sales
                'rd_intensity': np.random.uniform(0, 0.1),  # 0-10% R&D
                'leverage': np.random.uniform(0.2, 0.8),  # 20-80% leverage
                'firm_age': year - 2000 + np.random.randint(-5, 5)
            })
    
    df = pd.DataFrame(data)
    
    # Randomly introduce missing values (5% of R&D data)
    missing_indices = np.random.choice(
        len(df), 
        size=int(len(df) * 0.05), 
        replace=False
    )
    df.loc[missing_indices, 'rd_intensity'] = np.nan
    
    print(f"✓ Generated {len(df):,} observations")
    print(f"  - Firms: {df['firm_id'].nunique()}")
    print(f"  - Years: {df['year'].min()}-{df['year'].max()}")
    print(f"  - Variables: {len(df.columns)}")
    
    return df


def run_basic_workflow():
    """Execute complete basic workflow"""
    
    print("=" * 80)
    print("STRATEGIC RESEARCH BASIC WORKFLOW EXAMPLE")
    print("=" * 80)
    print()
    
    # Step 1: Generate sample data
    print("[Step 1] Data Generation")
    print("-" * 80)
    df = generate_sample_data(n_firms=100, n_years=10)
    print()
    
    # Step 2: Data quality checks
    print("[Step 2] Data Quality Checks")
    print("-" * 80)
    checker = DataQualityChecker(df)
    report = checker.check_all()
    
    print(f"✓ Quality checks completed:")
    print(f"  - Missing values: {report['missing']['total_missing']}")
    print(f"  - Panel balance: {'Balanced' if report['balance']['balanced'] else 'Unbalanced'}")
    print(f"  - Duplicates: {report['duplicates']['key_duplicates']}")
    print()
    
    # Step 3: Descriptive statistics
    print("[Step 3] Descriptive Statistics")
    print("-" * 80)
    
    numeric_cols = ['roa', 'roe', 'sales', 'rd_intensity', 'leverage', 'firm_age']
    desc_stats = df[numeric_cols].describe()
    
    print(desc_stats.round(3))
    print()
    
    # Step 4: Correlation analysis
    print("[Step 4] Correlation Analysis")
    print("-" * 80)
    
    corr_cols = ['roa', 'rd_intensity', 'leverage', 'firm_age']
    correlation = df[corr_cols].corr()
    
    print(correlation.round(3))
    print()
    
    # Step 5: Save results
    print("[Step 5] Saving Results")
    print("-" * 80)
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Save data
    df.to_csv(output_dir / 'sample_panel_data.csv', index=False)
    print(f"✓ Data saved: {output_dir / 'sample_panel_data.csv'}")
    
    # Save quality report
    with open(output_dir / 'quality_report.txt', 'w') as f:
        f.write(checker.generate_report())
    print(f"✓ Quality report saved: {output_dir / 'quality_report.txt'}")
    
    # Save descriptive statistics
    desc_stats.to_csv(output_dir / 'descriptive_statistics.csv')
    print(f"✓ Descriptive statistics saved: {output_dir / 'descriptive_statistics.csv'}")
    
    # Save correlation matrix
    correlation.to_csv(output_dir / 'correlation_matrix.csv')
    print(f"✓ Correlation matrix saved: {output_dir / 'correlation_matrix.csv'}")
    
    print()
    print("=" * 80)
    print("WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Review quality report: output/quality_report.txt")
    print("  2. Examine data: output/sample_panel_data.csv")
    print("  3. Proceed to advanced analysis (Phase 7)")
    print()


if __name__ == "__main__":
    run_basic_workflow()
