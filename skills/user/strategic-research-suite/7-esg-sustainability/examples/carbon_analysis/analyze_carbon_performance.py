"""
analyze_carbon_performance.py

Complete Example: Carbon Performance and Firm Value Analysis

This example demonstrates a full ESG research workflow using:
1. CDP data collection (carbon emissions)
2. ESG variable construction
3. Panel regression analysis
4. Robustness checks

Research Question:
Does carbon performance (lower carbon intensity) positively affect firm value?

Expected Output:
- ESG panel dataset
- Descriptive statistics
- Regression tables
- Visualization of results
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add parent directories to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
sys.path.append(str(Path(__file__).parent.parent.parent.parent / '1-core-workflow' / 'scripts'))

# Import modules
from cdp_collector import CDPCollector
from esg_variable_builder import ESGVariableBuilder

print("=" * 80)
print("CARBON PERFORMANCE AND FIRM VALUE ANALYSIS")
print("=" * 80)

# =============================================================================
# Phase 1: Data Collection
# =============================================================================

print("\n[Phase 1] Collecting CDP Carbon Data")
print("-" * 80)

# Initialize CDP collector (demo mode)
collector = CDPCollector()

# Sample companies (S&P 500 tech companies)
companies = [
    'Apple Inc.',
    'Microsoft Corp.',
    'Amazon.com Inc.',
    'Alphabet Inc.',
    'Meta Platforms Inc.',
    'Tesla Inc.',
    'NVIDIA Corp.',
    'Adobe Inc.',
    'Salesforce Inc.',
    'Intel Corp.'
]

# Collect data for 2018-2022
years = list(range(2018, 2023))

print(f"\nCollecting data for {len(companies)} companies, {len(years)} years...")

# Collect carbon emissions
emissions_df = collector.collect_carbon_emissions(companies, years)
print(f"✓ Emissions data: {len(emissions_df)} records")

# Collect climate scores
scores_df = collector.collect_climate_scores(companies, years)
print(f"✓ Climate scores: {len(scores_df)} records")

# Build comprehensive ESG panel
esg_panel = collector.build_esg_panel(
    companies=companies,
    start_year=2018,
    end_year=2022,
    include_scores=True,
    include_emissions=True
)

print(f"✓ ESG panel built: {len(esg_panel)} observations")
print(f"\nPanel structure:")
print(f"  Companies: {esg_panel['company'].nunique()}")
print(f"  Years: {esg_panel['year'].min()} - {esg_panel['year'].max()}")
print(f"  Variables: {len(esg_panel.columns)}")

# =============================================================================
# Phase 2: Add Financial Data (Simulated)
# =============================================================================

print("\n[Phase 2] Adding Financial Data")
print("-" * 80)

# In production, this would come from Compustat/CRSP
# For demo, we simulate financial data
np.random.seed(42)

financial_data = []
for company in companies:
    for year in years:
        # Simulate financial metrics
        financial_data.append({
            'company': company,
            'year': year,
            'revenue': np.random.lognormal(15, 1.5),  # Revenue in millions
            'total_assets': np.random.lognormal(16, 1.5),
            'market_value': np.random.lognormal(16.5, 2),
            'firm_size': np.random.normal(10, 1),
            'leverage': np.random.uniform(0.2, 0.6),
            'roa': np.random.uniform(0.02, 0.15),
            'tobin_q': np.random.uniform(0.8, 3.5),
            'industry': 'Technology'
        })

financial_df = pd.DataFrame(financial_data)

print(f"✓ Financial data simulated: {len(financial_df)} records")

# =============================================================================
# Phase 3: ESG Variable Construction
# =============================================================================

print("\n[Phase 3] Constructing ESG Variables")
print("-" * 80)

# Initialize ESG variable builder
builder = ESGVariableBuilder(
    esg_data=esg_panel,
    financial_data=financial_df,
    company_id='company',
    year_id='year',
    industry_id='industry'
)

# Build all ESG variables
esg_vars = builder.build_all_variables()

print(f"✓ ESG variables constructed:")
print(f"  Total variables: {len(esg_vars.columns)}")
print(f"  Carbon intensity: {'carbon_intensity' in esg_vars.columns}")
print(f"  Standardized scores: {any('_std' in col for col in esg_vars.columns)}")
print(f"  Performance ranks: {any('_percentile' in col for col in esg_vars.columns)}")

# Generate summary statistics
summary = builder.generate_summary_statistics()
print(f"\n✓ Summary statistics calculated for {len(summary)} variables")

# =============================================================================
# Phase 4: Descriptive Analysis
# =============================================================================

print("\n[Phase 4] Descriptive Analysis")
print("-" * 80)

# Key variables for analysis
key_vars = ['carbon_intensity', 'tobin_q', 'roa', 'firm_size', 'leverage']

print("\nDescriptive Statistics:")
print(esg_vars[key_vars].describe())

# Correlation matrix
print("\nCorrelation Matrix:")
corr_matrix = esg_vars[key_vars].corr()
print(corr_matrix.round(3))

# =============================================================================
# Phase 5: Regression Analysis
# =============================================================================

print("\n[Phase 5] Panel Regression Analysis")
print("-" * 80)

# Prepare data for regression
regression_data = esg_vars[[
    'company', 'year', 'tobin_q', 'carbon_intensity',
    'firm_size', 'leverage', 'roa'
]].dropna()

# Set panel index
regression_data = regression_data.set_index(['company', 'year'])

print(f"\nRegression sample: {len(regression_data)} observations")

# Run panel fixed effects regression
try:
    from linearmodels.panel import PanelOLS
    
    # Model: tobin_q ~ carbon_intensity + controls + FE
    formula = 'tobin_q ~ carbon_intensity + firm_size + leverage + roa + EntityEffects'
    
    model = PanelOLS.from_formula(formula, data=regression_data)
    result = model.fit(cov_type='clustered', cluster_entity=True)
    
    print("\n" + "=" * 80)
    print("REGRESSION RESULTS: Carbon Intensity → Firm Value (Tobin's Q)")
    print("=" * 80)
    print(result.summary)
    
    # Extract key coefficient
    carbon_coef = result.params['carbon_intensity']
    carbon_pval = result.pvalues['carbon_intensity']
    
    print("\n" + "=" * 80)
    print("KEY FINDING")
    print("=" * 80)
    print(f"Carbon Intensity Coefficient: {carbon_coef:.4f}")
    print(f"P-value: {carbon_pval:.4f}")
    
    if carbon_pval < 0.05:
        if carbon_coef < 0:
            print("\n✓ Lower carbon intensity significantly increases firm value (p < 0.05)")
        else:
            print("\n⚠ Higher carbon intensity significantly increases firm value (p < 0.05)")
    else:
        print("\n○ No significant relationship between carbon intensity and firm value")

except ImportError:
    print("\nlinearmodels not available. Install with: pip install linearmodels")
    print("Skipping regression analysis...")

# =============================================================================
# Phase 6: Save Outputs
# =============================================================================

print("\n[Phase 6] Saving Outputs")
print("-" * 80)

# Create output directory
output_dir = Path(__file__).parent / 'output'
output_dir.mkdir(exist_ok=True)

# Save datasets
esg_vars.to_csv(output_dir / 'esg_research_dataset.csv', index=False)
print(f"✓ Saved: esg_research_dataset.csv")

summary.to_csv(output_dir / 'summary_statistics.csv')
print(f"✓ Saved: summary_statistics.csv")

corr_matrix.to_csv(output_dir / 'correlation_matrix.csv')
print(f"✓ Saved: correlation_matrix.csv")

if 'result' in locals():
    with open(output_dir / 'regression_results.txt', 'w') as f:
        f.write(str(result.summary))
    print(f"✓ Saved: regression_results.txt")

# Generate report
report_path = builder.generate_report(output_dir)
print(f"✓ Saved: ESG variable report")

# =============================================================================
# Summary
# =============================================================================

print("\n" + "=" * 80)
print("ANALYSIS COMPLETED")
print("=" * 80)

print(f"\n✓ All outputs saved to: {output_dir}")
print("\nGenerated files:")
print("  1. esg_research_dataset.csv - Full research dataset")
print("  2. summary_statistics.csv - Descriptive statistics")
print("  3. correlation_matrix.csv - Variable correlations")
print("  4. regression_results.txt - Panel regression output")
print("  5. esg_variable_report.md - Comprehensive variable report")

print("\n" + "=" * 80)
print("RESEARCH IMPLICATIONS")
print("=" * 80)

print("""
This example demonstrates:

1. **Data Integration**: Combining ESG (CDP) and financial data

2. **Variable Construction**: Creating research-ready ESG metrics
   - Carbon intensity (emissions per revenue)
   - Standardized scores
   - Industry-adjusted metrics
   - Temporal changes

3. **Empirical Analysis**: Panel regression with firm fixed effects
   - Controls for unobserved firm heterogeneity
   - Clustered standard errors for robustness

4. **Practical Application**: Full workflow from data to insights

Next Steps:
- Add additional control variables
- Test alternative ESG metrics
- Examine heterogeneous effects by industry
- Conduct robustness checks (IV, matching)
- Extend to event studies or DiD designs
""")

print("\n" + "=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
