"""
run_esg_study.py

ESG Performance Research - Complete Pipeline

This script demonstrates executing the full research pipeline for an
ESG-financial performance study.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / 'scripts'
sys.path.append(str(scripts_dir))

from research_pipeline import StrategicResearchPipeline


def generate_esg_data():
    """
    Generate demo ESG data
    
    In production, this would connect to:
    - MSCI ESG ratings
    - CDP climate data
    - Sustainalytics
    """
    np.random.seed(42)
    
    n_firms = 300
    years = range(2015, 2024)
    
    data = []
    for firm_id in range(1, n_firms + 1):
        # Firm characteristics
        industry = np.random.choice(['Technology', 'Manufacturing', 'Finance', 
                                    'Energy', 'Healthcare', 'Consumer'])
        base_esg = np.random.uniform(40, 80)  # ESG score out of 100
        base_size = np.random.lognormal(9, 2)
        
        for year in years:
            # ESG improves slightly over time
            esg_trend = (year - 2015) * 0.5
            
            esg_total = base_esg + esg_trend + np.random.normal(0, 5)
            esg_e = esg_total * np.random.uniform(0.9, 1.1)  # Environmental
            esg_s = esg_total * np.random.uniform(0.9, 1.1)  # Social
            esg_g = esg_total * np.random.uniform(0.9, 1.1)  # Governance
            
            # Financial performance positively correlated with ESG
            esg_effect = (esg_total - 60) * 0.0002  # Small positive effect
            
            data.append({
                'firm_id': firm_id,
                'year': year,
                'industry': industry,
                'esg_total_score': esg_total,
                'esg_environmental': esg_e,
                'esg_social': esg_s,
                'esg_governance': esg_g,
                'roa': 0.05 + esg_effect + np.random.normal(0, 0.02),
                'roe': 0.12 + esg_effect * 2 + np.random.normal(0, 0.05),
                'tobin_q': 1.5 + esg_effect * 10 + np.random.normal(0, 0.3),
                'sales': base_size * np.random.lognormal(0, 0.3),
                'assets': base_size * 2 * np.random.lognormal(0, 0.2),
                'leverage': np.random.uniform(0.2, 0.6),
                'firm_age': 2024 - year + np.random.randint(10, 50),
                'carbon_emissions': base_size * 1000 * (1 - esg_e / 100) * np.random.uniform(0.8, 1.2),
                'employee_satisfaction': esg_s * 0.8 + np.random.normal(0, 5)
            })
    
    return pd.DataFrame(data)


def main():
    """
    Execute ESG performance study
    """
    print("=" * 80)
    print("ESG Performance Research - Complete Pipeline")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = StrategicResearchPipeline(
        research_question="Does ESG performance affect financial performance?",
        output_dir="./output/"
    )
    
    # Configure for ESG study
    pipeline.config.update({
        'sample_criteria': {
            'start_year': 2015,
            'end_year': 2023,
            'min_observations': 5,
            'industries': None  # All industries
        },
        'data_quality': {
            'max_missing_pct': 0.3,
            'outlier_threshold': 3.0,
            'min_firm_years': 5
        },
        'analysis': {
            'panel_method': 'fixed_effects',
            'cluster_var': 'firm_id',
            'robust_se': True
        }
    })
    
    print("\n📊 Generating ESG demo data...")
    df_esg = generate_esg_data()
    print(f"   ✓ Generated {len(df_esg):,} observations")
    print(f"   ✓ {df_esg['firm_id'].nunique()} firms")
    print(f"   ✓ {df_esg['year'].min()}-{df_esg['year'].max()}")
    
    # Execute full pipeline
    print("\n🚀 Executing Phase 1-8...")
    result = pipeline.run_full_pipeline(input_data=df_esg)
    
    # Display results
    print("\n" + "=" * 80)
    print("Pipeline Execution Results")
    print("=" * 80)
    
    if result['status'] == 'success':
        print("\n✅ Status: SUCCESS")
        print(f"⏱️  Duration: {result['duration_seconds']:.2f} seconds")
        print(f"📁 Output directory: {result['output_directory']}")
        print(f"📄 Final report: {result['final_report']}")
        
        # Display key ESG findings
        print("\n" + "=" * 80)
        print("ESG Study Key Findings")
        print("=" * 80)
        
        if 'phase_3' in pipeline.results:
            stats = pipeline.results['phase_3']['statistics']
            print("\n📊 Sample:")
            print(f"   Total observations: {stats['total_observations']:,}")
            print(f"   Total firms: {stats['total_firms']:,}")
        
        if 'phase_7' in pipeline.results:
            print("\n📈 Analysis:")
            reg_results = pipeline.results['phase_7'].get('regression', {})
            if 'coefficient' in reg_results:
                print(f"   ESG-Performance correlation: {reg_results['coefficient']:.4f}")
        
        # ESG-specific statistics
        print("\n🌍 ESG Metrics (from data):")
        print(f"   Mean ESG score: {df_esg['esg_total_score'].mean():.1f}")
        print(f"   Mean Environmental: {df_esg['esg_environmental'].mean():.1f}")
        print(f"   Mean Social: {df_esg['esg_social'].mean():.1f}")
        print(f"   Mean Governance: {df_esg['esg_governance'].mean():.1f}")
        
        print("\n💰 Financial Performance:")
        print(f"   Mean ROA: {df_esg['roa'].mean():.3f}")
        print(f"   Mean ROE: {df_esg['roe'].mean():.3f}")
        print(f"   Mean Tobin's Q: {df_esg['tobin_q'].mean():.2f}")
        
        print("\n" + "=" * 80)
        print("Next Steps")
        print("=" * 80)
        print("\n1. Review final report:")
        print("   cat ./output/phase8_final_report.md")
        
        print("\n2. Advanced ESG analysis:")
        print("   - Use 'esg-sustainability-data' skill for detailed ESG metrics")
        print("   - Use 'causal-ml-toolkit' skill for heterogeneous treatment effects")
        print("   - Use 'text-analysis' skill for sustainability report analysis")
        
        print("\n3. Industry-specific analysis:")
        print("   - Compare ESG effects across industries")
        print("   - Examine E/S/G component effects separately")
        
        print("\n" + "=" * 80)
        print("🎉 ESG study completed successfully!")
        print("=" * 80)
        
    else:
        print("\n❌ Status: FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
