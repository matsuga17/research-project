"""
run_automated_research.py

Complete Automated Research Example

This example demonstrates end-to-end automation of a strategic research project,
from data collection to publication-ready output.

Research Question:
"Does R&D investment improve firm performance?"

Steps Automated:
1. Research design specification
2. Data collection from multiple sources
3. Panel dataset construction
4. Quality assurance
5. Variable construction
6. Statistical analysis
7. Report generation
8. Reproducibility package

Expected Runtime: 5-10 minutes
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))

from full_pipeline import StrategicResearchPipeline
import yaml


def create_research_config():
    """
    Create configuration for automated research
    
    Returns:
        Configuration dictionary
    """
    config = {
        # Research Design
        'research_question': 'Does R&D investment improve firm performance?',
        
        'hypotheses': [
            'H1: R&D intensity positively affects ROA',
            'H2: The effect is stronger in high-tech industries',
            'H3: The effect persists after controlling for firm characteristics'
        ],
        
        'constructs': {
            'roa': 'Return on Assets = Net Income / Total Assets',
            'rd_intensity': 'R&D Intensity = R&D Expense / Revenue',
            'firm_size': 'Firm Size = log(Total Assets)',
            'leverage': 'Leverage = Total Debt / Total Assets'
        },
        
        # Data Sources
        'data_sources': [
            {
                'name': 'Compustat North America',
                'type': 'compustat',
                'description': 'Financial and accounting data',
                'params': {
                    'n_firms': 200,
                    'years': range(2015, 2023),
                    'variables': ['total_assets', 'revenue', 'net_income', 
                                'rd_expense', 'total_debt']
                }
            },
            {
                'name': 'CRSP',
                'type': 'crsp',
                'description': 'Stock market data',
                'params': {
                    'n_firms': 200,
                    'years': range(2015, 2023),
                    'variables': ['stock_return', 'market_value', 'volatility']
                }
            }
        ],
        
        # Sample Criteria
        'sample_criteria': {
            'industry': 'manufacturing',
            'start_year': 2015,
            'end_year': 2022,
            'min_observations': 3,
            'exclude_financials': True
        },
        
        # Data Processing
        'merge_keys': ['firm_id', 'year'],
        
        'lag_variables': ['rd_intensity', 'firm_size', 'leverage'],
        
        # Statistical Analysis
        'statistical_methods': [
            'panel_fe',    # Panel fixed effects
            'panel_re',    # Panel random effects
        ],
        
        # Model Specification
        'panel_formula': 'roa ~ rd_intensity_lag1 + firm_size + leverage + EntityEffects + TimeEffects',
        
        # Output
        'output_dir': './output_automated/'
    }
    
    return config


def main():
    """Execute automated research pipeline"""
    
    print("=" * 80)
    print("AUTOMATED RESEARCH PIPELINE")
    print("=" * 80)
    print("\nResearch Question: Does R&D investment improve firm performance?")
    print("\nThis example will:")
    print("  1. Design the research study")
    print("  2. Collect data from Compustat and CRSP")
    print("  3. Construct panel dataset")
    print("  4. Check data quality")
    print("  5. Construct variables")
    print("  6. Run panel regressions")
    print("  7. Generate comprehensive report")
    print("  8. Create reproducibility package")
    print("\nEstimated runtime: 5-10 minutes")
    print("\n" + "=" * 80)
    
    input("\nPress Enter to start automated research...")
    
    # Create configuration
    config = create_research_config()
    
    # Save configuration for reference
    config_file = Path('research_config.yaml')
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"\n✓ Configuration saved: {config_file}")
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = StrategicResearchPipeline(config)
    
    # Run complete pipeline
    print("\nRunning automated research pipeline...\n")
    results = pipeline.run_full_pipeline()
    
    # Check results
    if results['status'] == 'success':
        print("\n" + "=" * 80)
        print("AUTOMATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        print(f"\nDuration: {results['metadata']['duration']:.1f} seconds")
        print(f"\nOutput directory: {config['output_dir']}")
        
        print("\nGenerated files:")
        print("  Data:")
        print("    - data/panel_merged.csv")
        print("    - data/panel_final.csv")
        
        print("\n  Analysis:")
        print("    - tables/panel_fe_results.txt")
        print("    - tables/panel_re_results.txt")
        
        print("\n  Reports:")
        print(f"    - {results['report_path']}")
        print("    - reports/data_dictionary.csv")
        print("    - reports/quality_report.txt")
        
        print("\n  Replication:")
        print("    - replication/README.md")
        print("    - replication/requirements.txt")
        print("    - replication/config.yaml")
        
        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)
        print("\n1. Review the research report:")
        print(f"   open {results['report_path']}")
        
        print("\n2. Check regression results:")
        print(f"   cat {config['output_dir']}/tables/panel_fe_results.txt")
        
        print("\n3. Examine data quality:")
        print(f"   cat {config['output_dir']}/reports/quality_report.txt")
        
        print("\n4. Share replication package:")
        print(f"   zip -r replication.zip {config['output_dir']}/replication/")
        
    else:
        print("\n" + "=" * 80)
        print("AUTOMATION FAILED")
        print("=" * 80)
        print(f"\nError: {results.get('error', 'Unknown error')}")
        print("\nCheck logs for details:")
        print(f"  {config['output_dir']}/logs/")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
