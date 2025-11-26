"""
analyze_merger_effect.py

Comprehensive Merger Effect Analysis using Causal ML Methods

This example demonstrates how to use all three causal ML methods to analyze
the effect of a merger on firm performance:
1. Causal Forest - for heterogeneous treatment effects
2. Double ML - for robust average treatment effect with high-dimensional controls
3. Synthetic Control - for case study of a specific merger

Run this example to see complete causal inference workflow.

Usage:
    cd 6-causal-ml/examples/merger_effect/
    python analyze_merger_effect.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))

try:
    from causal_forest import CausalForestAnalyzer
    from double_ml import DoubleMLAnalyzer
    from synthetic_control import SyntheticControlAnalyzer
    CAUSAL_ML_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import causal ML modules: {e}")
    CAUSAL_ML_AVAILABLE = False


def generate_merger_data(n_firms: int = 200, n_years: int = 10) -> pd.DataFrame:
    """
    Generate realistic panel data for merger analysis
    
    Args:
        n_firms: Number of firms
        n_years: Number of years
    
    Returns:
        Panel dataset with merger dummy and firm characteristics
    """
    print(f"Generating merger data: {n_firms} firms × {n_years} years...")
    
    np.random.seed(42)
    
    data = []
    merger_year = 2017  # Treatment occurs in 2017
    
    for firm in range(1, n_firms + 1):
        # Firm-specific characteristics
        firm_size = np.random.lognormal(10, 1.5)
        base_roa = np.random.normal(0.05, 0.02)
        rd_intensity = np.random.uniform(0, 0.15)
        leverage_base = np.random.uniform(0.2, 0.8)
        industry = np.random.choice(['tech', 'manufacturing', 'services'], p=[0.3, 0.4, 0.3])
        
        # Determine if firm will merge (selection on observables)
        # Larger, more profitable firms with higher R&D more likely to merge
        merger_prob = 0.15 + 0.1 * (firm_size > np.median(np.random.lognormal(10, 1.5, n_firms)))
        merger_prob += 0.05 * (rd_intensity > 0.05)
        merged = np.random.random() < merger_prob
        
        for year in range(2013, 2013 + n_years):
            # Time-varying variables
            year_idx = year - 2013
            
            # Sales grow over time
            sales = firm_size * (1 + 0.05 * year_idx) * np.random.lognormal(0, 0.1)
            
            # R&D intensity varies slightly over time
            rd = rd_intensity + np.random.normal(0, 0.01)
            rd = max(0, min(0.3, rd))  # Keep between 0 and 30%
            
            # Leverage varies
            leverage = leverage_base + np.random.normal(0, 0.05)
            leverage = max(0.1, min(0.9, leverage))
            
            # Firm age
            firm_age = year - 2000 + np.random.randint(-3, 3)
            
            # ROA with time trend and firm heterogeneity
            roa = base_roa + 0.002 * year_idx  # Slight upward trend
            roa += 0.0001 * sales / 1e6  # Size effect
            roa += 0.1 * rd  # R&D effect
            roa -= 0.03 * leverage  # Leverage penalty
            
            # Merger effect (heterogeneous)
            merger_dummy = 0
            if merged and year >= merger_year:
                merger_dummy = 1
                # Treatment effect varies by firm characteristics
                treatment_effect = 0.015  # Base effect
                treatment_effect += 0.02 * rd  # Stronger for high R&D firms
                treatment_effect += 0.005 if industry == 'tech' else 0  # Tech premium
                roa += treatment_effect
            
            # Add noise
            roa += np.random.normal(0, 0.015)
            
            data.append({
                'firm_id': firm,
                'year': year,
                'merger_dummy': merger_dummy,
                'roa': roa,
                'sales': sales,
                'rd_intensity': rd,
                'leverage': leverage,
                'firm_age': firm_age,
                'industry': industry,
                'firm_size': sales / 1e6  # Size in millions
            })
    
    df = pd.DataFrame(data)
    
    print(f"✓ Generated {len(df):,} observations")
    print(f"  Merged firms: {df[df['merger_dummy']==1]['firm_id'].nunique()}")
    print(f"  Control firms: {df[df['merger_dummy']==0]['firm_id'].nunique()}")
    print(f"  Treatment year: {merger_year}")
    
    return df


def run_causal_forest_analysis(df: pd.DataFrame, output_dir: Path):
    """Run Causal Forest analysis"""
    print("\n" + "=" * 80)
    print("[Method 1] CAUSAL FOREST - Heterogeneous Treatment Effects")
    print("=" * 80)
    
    # Focus on firms in treatment year and after
    df_cf = df[df['year'] >= 2017].copy()
    
    analyzer = CausalForestAnalyzer(
        df=df_cf,
        treatment='merger_dummy',
        outcome='roa',
        features=['firm_size', 'rd_intensity', 'leverage', 'firm_age']
    )
    
    # Estimate CATE
    cate_results = analyzer.estimate_cate()
    
    # Analyze heterogeneity
    het_stats = analyzer.analyze_heterogeneity()
    
    print(f"\n✓ Causal Forest completed")
    print(f"  Mean CATE: {het_stats['mean']:.4f}")
    print(f"  Heterogeneity: {'Significant' if het_stats['heterogeneity_test']['significant'] else 'Not significant'}")
    
    # Generate report
    cf_dir = output_dir / 'causal_forest'
    analyzer.generate_report(cf_dir)
    
    print(f"  Report saved: {cf_dir}")
    
    return het_stats


def run_double_ml_analysis(df: pd.DataFrame, output_dir: Path):
    """Run Double ML analysis"""
    print("\n" + "=" * 80)
    print("[Method 2] DOUBLE ML - Robust ATE with High-Dimensional Controls")
    print("=" * 80)
    
    # Use all years
    controls = ['firm_size', 'rd_intensity', 'leverage', 'firm_age']
    # Add year fixed effects
    for year in df['year'].unique()[:-1]:  # Exclude last year as reference
        df[f'year_{year}'] = (df['year'] == year).astype(int)
        controls.append(f'year_{year}')
    
    # Add industry dummies
    for ind in ['tech', 'manufacturing']:  # Exclude 'services' as reference
        df[f'industry_{ind}'] = (df['industry'] == ind).astype(int)
        controls.append(f'industry_{ind}')
    
    analyzer = DoubleMLAnalyzer(
        df=df,
        treatment='merger_dummy',
        outcome='roa',
        controls=controls
    )
    
    # Estimate ATE
    results = analyzer.estimate_plm()
    
    print(f"\n✓ Double ML completed")
    print(f"  ATE: {results['ate']:.4f} (SE: {results['se']:.4f})")
    print(f"  95% CI: [{results['ci_lower']:.4f}, {results['ci_upper']:.4f}]")
    print(f"  Significant: {'Yes' if results['p_value'] < 0.05 else 'No'}")
    
    # Generate report
    dml_dir = output_dir / 'double_ml'
    analyzer.generate_report(dml_dir)
    
    print(f"  Report saved: {dml_dir}")
    
    return results


def run_synthetic_control_analysis(df: pd.DataFrame, output_dir: Path):
    """Run Synthetic Control analysis"""
    print("\n" + "=" * 80)
    print("[Method 3] SYNTHETIC CONTROL - Case Study of Single Merger")
    print("=" * 80)
    
    # Select a specific merged firm for case study
    merged_firms = df[df['merger_dummy'] == 1]['firm_id'].unique()
    focal_firm = merged_firms[0]  # Study first merged firm
    
    print(f"  Analyzing merger of Firm {focal_firm}")
    
    analyzer = SyntheticControlAnalyzer(
        df=df,
        treated_unit=focal_firm,
        treatment_time=2017,
        outcome='roa',
        predictors=['firm_size', 'rd_intensity', 'leverage']
    )
    
    # Estimate
    results = analyzer.estimate()
    
    print(f"\n✓ Synthetic Control completed")
    print(f"  Pre-treatment RMSPE: {results['pre_rmspe']:.4f}")
    print(f"  Post-treatment gap: {results['post_mean_gap']:.4f}")
    print(f"  Active donors: {results['donor_units']}")
    
    # Generate report
    sc_dir = output_dir / 'synthetic_control'
    analyzer.generate_report(sc_dir)
    
    print(f"  Report saved: {sc_dir}")
    
    return results


def run_complete_analysis():
    """Run complete merger effect analysis"""
    
    print("=" * 80)
    print("COMPREHENSIVE MERGER EFFECT ANALYSIS")
    print("Using Three Causal ML Methods")
    print("=" * 80)
    
    if not CAUSAL_ML_AVAILABLE:
        print("\n❌ Error: Causal ML modules not available")
        print("Please install: pip install econml scikit-learn")
        return
    
    # Step 1: Generate data
    print("\n[Step 1] Data Generation")
    print("-" * 80)
    df = generate_merger_data(n_firms=200, n_years=10)
    
    # Save data
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    df.to_csv(output_dir / 'merger_panel_data.csv', index=False)
    print(f"  Data saved: {output_dir / 'merger_panel_data.csv'}")
    
    # Step 2: Causal Forest
    cf_results = run_causal_forest_analysis(df, output_dir)
    
    # Step 3: Double ML
    dml_results = run_double_ml_analysis(df, output_dir)
    
    # Step 4: Synthetic Control
    sc_results = run_synthetic_control_analysis(df, output_dir)
    
    # Step 5: Compare results
    print("\n" + "=" * 80)
    print("RESULTS COMPARISON")
    print("=" * 80)
    
    comparison = pd.DataFrame({
        'Method': ['Causal Forest', 'Double ML', 'Synthetic Control'],
        'Effect': [
            cf_results['mean'],
            dml_results['ate'],
            sc_results['post_mean_gap']
        ],
        'Inference': [
            'Heterogeneity analysis',
            f"95% CI: [{dml_results['ci_lower']:.3f}, {dml_results['ci_upper']:.3f}]",
            f"Pre-RMSPE: {sc_results['pre_rmspe']:.3f}"
        ]
    })
    
    print("\n", comparison.to_string(index=False))
    
    comparison.to_csv(output_dir / 'method_comparison.csv', index=False)
    
    # Final summary
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("=" * 80)
    print(f"\nAll results saved to: {output_dir}")
    print("\nKey findings:")
    print(f"  1. Causal Forest: Mean CATE = {cf_results['mean']:.4f}")
    print(f"     → Heterogeneity: {cf_results['heterogeneity_test']['significant']}")
    print(f"  2. Double ML: ATE = {dml_results['ate']:.4f}")
    print(f"     → Significant: {dml_results['p_value'] < 0.05}")
    print(f"  3. Synthetic Control: Gap = {sc_results['post_mean_gap']:.4f}")
    print(f"     → Pre-fit quality: {sc_results['pre_rmspe']:.4f}")
    
    print("\n" + "=" * 80)
    print("Next steps:")
    print("  1. Review detailed reports in output/ subdirectories")
    print("  2. Examine visualizations (.png files)")
    print("  3. Check robustness with different specifications")
    print("=" * 80)


if __name__ == "__main__":
    run_complete_analysis()
