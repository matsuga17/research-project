"""
3_full_pipeline.py

Complete Pipeline Execution for Japan Innovation Study

This script demonstrates executing the full research pipeline (Phase 1-8)
with Japanese firm data.
"""

import sys
from pathlib import Path
import pandas as pd

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / 'scripts'
sys.path.append(str(scripts_dir))

from research_pipeline import StrategicResearchPipeline


def main():
    """
    Execute complete research pipeline for Japan innovation study
    """
    print("=" * 80)
    print("Japan Innovation Research - Complete Pipeline Execution")
    print("=" * 80)
    
    # Initialize pipeline
    pipeline = StrategicResearchPipeline(
        research_question="How does R&D intensity affect firm performance in Japanese manufacturing firms?",
        output_dir="./output/"
    )
    
    # Configure for Japan study
    pipeline.config.update({
        'sample_criteria': {
            'start_year': 2015,  # Focus on recent period
            'end_year': 2023,
            'min_observations': 5,  # Minimum 5 years per firm
            'country': 'Japan',
            'industries': ['電気機器', '機械', '化学', '自動車', '医薬品']
        },
        'data_quality': {
            'max_missing_pct': 0.4,  # Allow 40% missing
            'outlier_threshold': 3.0,
            'min_firm_years': 5
        },
        'analysis': {
            'panel_method': 'fixed_effects',
            'cluster_var': 'firm_code',
            'robust_se': True
        }
    })
    
    # Check if data already collected
    data_file = Path("./output/japan_firms_raw.csv")
    
    if data_file.exists():
        print("\n✓ Using existing data from previous collection")
        print(f"  File: {data_file}")
        
        # Load existing data
        df_input = pd.read_csv(data_file)
        print(f"  Loaded {len(df_input):,} observations")
        
        # Execute full pipeline with existing data
        print("\n🚀 Executing Phase 1-8...")
        result = pipeline.run_full_pipeline(input_data=df_input)
        
    else:
        print("\n⚠️  No existing data found. Collecting new data...")
        print("   (Or run 2_data_collection.py first)")
        
        # Execute full pipeline (will collect demo data internally)
        print("\n🚀 Executing Phase 1-8...")
        result = pipeline.run_full_pipeline()
    
    # Display results
    print("\n" + "=" * 80)
    print("Pipeline Execution Results")
    print("=" * 80)
    
    if result['status'] == 'success':
        print("\n✅ Status: SUCCESS")
        print(f"⏱️  Duration: {result['duration_seconds']:.2f} seconds")
        print(f"📁 Output directory: {result['output_directory']}")
        print(f"📄 Final report: {result['final_report']}")
        
        # Display key findings from each phase
        print("\n" + "=" * 80)
        print("Key Findings by Phase")
        print("=" * 80)
        
        # Phase 1
        if 'phase_1' in pipeline.results:
            print("\n📋 Phase 1: Research Design")
            print(f"   Research Question: {pipeline.results['phase_1']['research_question']}")
            print(f"   Hypotheses: {len(pipeline.results['phase_1']['hypotheses'])} hypotheses developed")
        
        # Phase 3
        if 'phase_3' in pipeline.results:
            stats = pipeline.results['phase_3']['statistics']
            print("\n📊 Phase 3: Sample Construction")
            print(f"   Total observations: {stats['total_observations']:,}")
            print(f"   Total firms: {stats['total_firms']:,}")
            print(f"   Year range: {stats['year_range']}")
            print(f"   Avg observations/firm: {stats['avg_observations_per_firm']:.1f}")
        
        # Phase 7
        if 'phase_7' in pipeline.results:
            print("\n📈 Phase 7: Statistical Analysis")
            reg_results = pipeline.results['phase_7'].get('regression', {})
            if 'coefficient' in reg_results:
                coef = reg_results['coefficient']
                direction = "positive" if coef > 0 else "negative" if coef < 0 else "no"
                print(f"   R&D-Performance relationship: {direction} (β = {coef:.4f})")
            print("   ✓ Descriptive statistics computed")
            print("   ✓ Correlation analysis completed")
        
        # Phase 8
        print("\n📝 Phase 8: Final Report")
        print(f"   Report generated: {result['final_report']}")
        
        print("\n" + "=" * 80)
        print("Output Files")
        print("=" * 80)
        print("\nAll results saved to: ./output/")
        print("\nKey files:")
        print("  - phase1_research_design.json")
        print("  - phase3_sample.csv")
        print("  - phase5_cleaned_data.csv")
        print("  - phase6_variables.csv")
        print("  - phase7_descriptive_stats.csv")
        print("  - phase7_correlation_matrix.csv")
        print("  - phase7_regression_results.json")
        print("  - phase8_final_report.md  ← 最終レポート")
        
        print("\n" + "=" * 80)
        print("Next Steps")
        print("=" * 80)
        print("\n1. Review final report:")
        print("   cat ./output/phase8_final_report.md")
        
        print("\n2. Examine descriptive statistics:")
        print("   cat ./output/phase7_descriptive_stats.csv")
        
        print("\n3. Check data quality:")
        print("   cat ./output/phase5_quality_report.txt")
        
        print("\n4. Advanced analysis:")
        print("   - Use 'statistical-methods' skill for panel regression")
        print("   - Use 'text-analysis' skill for MD&A analysis")
        print("   - Use 'data-mining' skill for firm clustering")
        
        print("\n" + "=" * 80)
        print("🎉 Complete pipeline execution finished successfully!")
        print("=" * 80)
        
    else:
        print("\n❌ Status: FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}")
        print("\nCheck logs in ./output/logs/ for details")


if __name__ == "__main__":
    main()
