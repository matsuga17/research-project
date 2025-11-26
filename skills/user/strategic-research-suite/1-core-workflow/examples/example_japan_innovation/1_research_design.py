"""
1_research_design.py

Phase 1: Research Design for Japan Innovation Study

This script demonstrates how to execute Phase 1 independently.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / 'scripts'
sys.path.append(str(scripts_dir))

from research_pipeline import StrategicResearchPipeline


def main():
    """
    Execute Phase 1: Research Design
    """
    print("=" * 70)
    print("Japan Innovation Research - Phase 1: Research Design")
    print("=" * 70)
    
    # Initialize pipeline
    pipeline = StrategicResearchPipeline(
        research_question="How does R&D intensity affect firm performance in Japanese manufacturing firms?",
        output_dir="./output/"
    )
    
    # Set Japan-specific configuration
    pipeline.config.update({
        'sample_criteria': {
            'start_year': 2010,
            'end_year': 2023,
            'min_observations': 5,
            'country': 'Japan',
            'industries': ['Manufacturing']  # 製造業に限定
        },
        'data_sources': {
            'primary': ['EDINET'],
            'supplementary': ['Patent Office', 'e-Stat']
        }
    })
    
    # Execute Phase 1
    print("\nExecuting Phase 1...")
    result = pipeline.run_phase_1_research_design()
    
    # Display results
    print("\n" + "=" * 70)
    print("Phase 1 Completed Successfully!")
    print("=" * 70)
    
    print("\n📋 Research Question:")
    print(f"  {result['research_question']}")
    
    print("\n📚 Theoretical Framework:")
    print(f"  {result['theoretical_framework']}")
    
    print("\n🎯 Hypotheses:")
    for i, hyp in enumerate(result['hypotheses'], 1):
        print(f"  H{i}: {hyp}")
    
    print("\n📊 Variables:")
    vars_def = result['variables']
    print(f"  Dependent: {', '.join(vars_def['dependent'])}")
    print(f"  Independent: {', '.join(vars_def['independent'])}")
    print(f"  Control: {', '.join(vars_def['control'])}")
    
    print("\n💾 Output saved to:")
    print(f"  ./output/phase1_research_design.json")
    
    print("\n📝 Next Step:")
    print("  Run 2_data_collection.py to collect Japanese firm data")
    print("=" * 70)


if __name__ == "__main__":
    main()
