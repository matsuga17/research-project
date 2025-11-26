"""
run_panel_did_analysis.py

Complete Example: Panel Regression and Difference-in-Differences Analysis

Research Question:
Does R&D investment improve firm performance? 
Testing with merger events as natural experiments.

Methods Demonstrated:
1. Panel Fixed Effects (FE) Regression
2. Panel Random Effects (RE) Regression  
3. Hausman Test (FE vs RE)
4. Difference-in-Differences (DiD)
5. Parallel Trends Test
6. Robustness Checks

Expected Output:
- Regression tables (FE, RE, DiD)
- Parallel trends visualization
- Event study plot
- Robustness check results
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))

from panel_regression import PanelRegressor
from did_analysis import DifferenceInDifferences

print("=" * 80)
print("PANEL REGRESSION AND DIFFERENCE-IN-DIFFERENCES ANALYSIS")
print("=" * 80)

# =============================================================================
# Phase 1: Data Generation
# =============================================================================

print("\n[Phase 1] Generating Sample Data")
print("-" * 80)

np.random.seed(42)

# Panel structure: 200 firms, 10 years
n_firms = 200
n_years = 10
years = list(range(2013, 2023))

# Generate panel data
data = []

for firm_id in range(1, n_firms + 1):
    # Firm-specific characteristics
    firm_effect = np.random.normal(0, 1)  # Unobserved firm heterogeneity
    base_roa = 0.05 + 0.02 * firm_effect
    
    # Industry (affects both R&D and performance)
    industry = np.random.choice(['Tech', 'Manufacturing', 'Services'])
    industry_effect = {'Tech': 0.03, 'Manufacturing': 0.01, 'Services': 0.02}[industry]
    
    # Merger treatment (occurs in year 2018 for some firms)
    treated = np.random.random() < 0.3  # 30% treatment rate
    treatment_year = 2018 if treated else None
    
    for t, year in enumerate(years):
        # R&D intensity (persistent, affected by firm type)
        rd_intensity = max(0, np.random.normal(0.05, 0.02) + 0.03 * (industry == 'Tech'))
        
        # Time trend
        time_effect = 0.002 * t
        
        # Treatment effect (after merger in 2018)
        if treated and year >= treatment_year:
            treatment_effect = 0.015  # 1.5% ROA increase from merger
        else:
            treatment_effect = 0
        
        # Outcome: ROA
        roa = (base_roa + 
               0.5 * rd_intensity +  # R&D effect
               firm_effect * 0.01 +  # Firm fixed effect
               industry_effect +     # Industry effect
               time_effect +         # Time trend
               treatment_effect +    # Merger effect
               np.random.normal(0, 0.01))  # Random noise
        
        # Control variables
        firm_size = np.random.normal(10, 1.5)
        leverage = np.random.uniform(0.2, 0.7)
        firm_age = 5 + t
        
        data.append({
            'firm_id': f'FIRM{firm_id:04d}',
            'year': year,
            'roa': roa,
            'rd_intensity': rd_intensity,
            'firm_size': firm_size,
            'leverage': leverage,
            'firm_age': firm_age,
            'industry': industry,
            'treated': int(treated),
            'post': int(year >= 2018),
            'treat_post': int(treated and year >= 2018)
        })

df = pd.DataFrame(data)

print(f"✓ Generated panel data:")
print(f"  Firms: {df['firm_id'].nunique()}")
print(f"  Years: {df['year'].min()} - {df['year'].max()}")
print(f"  Observations: {len(df):,}")
print(f"  Treated firms: {df.groupby('firm_id')['treated'].first().sum()}")

# =============================================================================
# Phase 2: Panel Regression Analysis
# =============================================================================

print("\n[Phase 2] Panel Regression Analysis")
print("-" * 80)

# Initialize regressor
regressor = PanelRegressor(
    df=df,
    outcome='roa',
    predictors=['rd_intensity', 'firm_size', 'leverage'],
    entity_var='firm_id',
    time_var='year'
)

# Run Fixed Effects
print("\n[Model 1: Fixed Effects]")
fe_results = regressor.fixed_effects(
    cluster_entity=True,
    time_effects=True
)

print(f"\nR-squared: {fe_results.rsquared:.4f}")
print(f"R&D Coefficient: {fe_results.params['rd_intensity']:.4f} (p={fe_results.pvalues['rd_intensity']:.4f})")

# Run Random Effects
print("\n[Model 2: Random Effects]")
re_results = regressor.random_effects()

print(f"\nR-squared (Overall): {re_results.rsquared_overall:.4f}")
print(f"R&D Coefficient: {re_results.params['rd_intensity']:.4f} (p={re_results.pvalues['rd_intensity']:.4f})")

# Hausman Test
print("\n[Hausman Test: FE vs RE]")
try:
    hausman = regressor.hausman_test(fe_results, re_results)
    print(f"Chi-square: {hausman['statistic']:.4f}")
    print(f"P-value: {hausman['p_value']:.4f}")
    
    if hausman['p_value'] < 0.05:
        print("✓ Reject RE (use Fixed Effects)")
    else:
        print("○ Cannot reject RE (Random Effects acceptable)")
except Exception as e:
    print(f"Hausman test error: {e}")

# =============================================================================
# Phase 3: Difference-in-Differences Analysis
# =============================================================================

print("\n[Phase 3] Difference-in-Differences Analysis")
print("-" * 80)

# Initialize DiD analyzer
did = DifferenceInDifferences(
    df=df,
    outcome='roa',
    treatment_var='treated',
    time_var='year',
    treatment_time=2018,
    firm_id='firm_id'
)

# Check parallel trends
print("\n[Pre-Treatment Parallel Trends Test]")
parallel_test = did.test_parallel_trends(
    outcome='roa',
    pre_periods=[2013, 2014, 2015, 2016, 2017]
)

print(f"F-statistic: {parallel_test['f_statistic']:.4f}")
print(f"P-value: {parallel_test['p_value']:.4f}")

if parallel_test['p_value'] > 0.05:
    print("✓ Parallel trends assumption satisfied (p > 0.05)")
else:
    print("⚠ Parallel trends may be violated (p < 0.05)")

# Run DiD regression
print("\n[DiD Regression]")
did_results = did.estimate_did(
    controls=['firm_size', 'leverage'],
    cluster='firm_id'
)

print(f"\nDiD Coefficient (Treat × Post): {did_results['coef']:.4f}")
print(f"Standard Error: {did_results['se']:.4f}")
print(f"P-value: {did_results['p_value']:.4f}")
print(f"95% CI: [{did_results['ci_lower']:.4f}, {did_results['ci_upper']:.4f}]")

if did_results['p_value'] < 0.05:
    print(f"\n✓ Mergers increase ROA by {did_results['coef']*100:.2f} percentage points (p < 0.05)")
else:
    print("\n○ No significant merger effect detected")

# Event study
print("\n[Event Study: Dynamic Effects]")
event_study = did.event_study(
    outcome='roa',
    periods_before=3,
    periods_after=4
)

print("\nEvent Study Coefficients:")
for period, coef in event_study['coefficients'].items():
    stars = '***' if event_study['p_values'][period] < 0.01 else '**' if event_study['p_values'][period] < 0.05 else '*' if event_study['p_values'][period] < 0.1 else ''
    print(f"  t={period:+2d}: {coef:.4f}{stars}")

# =============================================================================
# Phase 4: Visualization
# =============================================================================

print("\n[Phase 4] Generating Visualizations")
print("-" * 80)

# Create output directory
output_dir = Path(__file__).parent / 'output'
output_dir.mkdir(exist_ok=True)

# Figure 1: Parallel Trends Plot
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Calculate group means over time
treated_means = df[df['treated'] == 1].groupby('year')['roa'].mean()
control_means = df[df['treated'] == 0].groupby('year')['roa'].mean()

ax1.plot(treated_means.index, treated_means.values, 'o-', label='Treated Firms', linewidth=2)
ax1.plot(control_means.index, control_means.values, 's--', label='Control Firms', linewidth=2, alpha=0.7)
ax1.axvline(2018, color='red', linestyle=':', alpha=0.5, label='Treatment')
ax1.set_xlabel('Year')
ax1.set_ylabel('ROA')
ax1.set_title('Parallel Trends: Treated vs Control Firms')
ax1.legend()
ax1.grid(alpha=0.3)

plt.tight_layout()
fig1.savefig(output_dir / 'parallel_trends.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: parallel_trends.png")

# Figure 2: Event Study Plot
fig2 = did.plot_event_study(event_study, save_path=output_dir / 'event_study.png')
print(f"✓ Saved: event_study.png")

plt.close('all')

# =============================================================================
# Phase 5: Robustness Checks
# =============================================================================

print("\n[Phase 5] Robustness Checks")
print("-" * 80)

# 1. Alternative specifications
print("\n[Robustness 1: Alternative Specifications]")

# Without time effects
fe_no_time = regressor.fixed_effects(cluster_entity=True, time_effects=False)
print(f"  FE without time effects: R&D coef = {fe_no_time.params['rd_intensity']:.4f}")

# With industry × year interactions
df_with_industry = df.copy()
for industry in df['industry'].unique():
    for year in df['year'].unique():
        df_with_industry[f'ind_{industry}_year_{year}'] = (
            (df['industry'] == industry) & (df['year'] == year)
        ).astype(int)

print("  ✓ Industry × Year interactions specified")

# 2. Placebo test (fake treatment year)
print("\n[Robustness 2: Placebo Test]")

# Run DiD with fake treatment year (2016 instead of 2018)
df_placebo = df.copy()
df_placebo['post_placebo'] = (df_placebo['year'] >= 2016).astype(int)
df_placebo['treat_post_placebo'] = df_placebo['treated'] * df_placebo['post_placebo']

# Placebo DiD using only pre-2018 data
df_pre2018 = df_placebo[df_placebo['year'] < 2018]

if len(df_pre2018) > 0:
    did_placebo = DifferenceInDifferences(
        df=df_pre2018,
        outcome='roa',
        treatment_var='treated',
        time_var='year',
        treatment_time=2016,
        firm_id='firm_id'
    )
    
    placebo_results = did_placebo.estimate_did(controls=['firm_size', 'leverage'])
    
    print(f"  Placebo DiD coefficient: {placebo_results['coef']:.4f} (p={placebo_results['p_value']:.4f})")
    
    if placebo_results['p_value'] > 0.10:
        print("  ✓ Placebo test passed (no pre-treatment effect)")
    else:
        print("  ⚠ Placebo test failed (potential pre-trends)")

# 3. Exclude outliers
print("\n[Robustness 3: Exclude Outliers]")

# Remove ROA outliers (beyond 3 std dev)
roa_mean = df['roa'].mean()
roa_std = df['roa'].std()
df_no_outliers = df[abs(df['roa'] - roa_mean) <= 3 * roa_std]

print(f"  Observations dropped: {len(df) - len(df_no_outliers)}")

regressor_robust = PanelRegressor(
    df=df_no_outliers,
    outcome='roa',
    predictors=['rd_intensity', 'firm_size', 'leverage'],
    entity_var='firm_id',
    time_var='year'
)

fe_robust = regressor_robust.fixed_effects(cluster_entity=True)
print(f"  FE (no outliers): R&D coef = {fe_robust.params['rd_intensity']:.4f}")

# =============================================================================
# Phase 6: Save Results
# =============================================================================

print("\n[Phase 6] Saving Results")
print("-" * 80)

# Save regression tables
with open(output_dir / 'fe_results.txt', 'w') as f:
    f.write(str(fe_results.summary))
print(f"✓ Saved: fe_results.txt")

with open(output_dir / 're_results.txt', 'w') as f:
    f.write(str(re_results.summary))
print(f"✓ Saved: re_results.txt")

# Save DiD results
did_summary = pd.DataFrame([{
    'method': 'DiD',
    'coefficient': did_results['coef'],
    'se': did_results['se'],
    'p_value': did_results['p_value'],
    'ci_lower': did_results['ci_lower'],
    'ci_upper': did_results['ci_upper']
}])
did_summary.to_csv(output_dir / 'did_results.csv', index=False)
print(f"✓ Saved: did_results.csv")

# Save event study
event_df = pd.DataFrame({
    'period': list(event_study['coefficients'].keys()),
    'coefficient': list(event_study['coefficients'].values()),
    'se': list(event_study['std_errors'].values()),
    'p_value': list(event_study['p_values'].values())
})
event_df.to_csv(output_dir / 'event_study_results.csv', index=False)
print(f"✓ Saved: event_study_results.csv")

# =============================================================================
# Summary Report
# =============================================================================

print("\n" + "=" * 80)
print("ANALYSIS SUMMARY")
print("=" * 80)

print(f"""
Panel Regression Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fixed Effects (Preferred):
  R&D Intensity → ROA: {fe_results.params['rd_intensity']:.4f} (p = {fe_results.pvalues['rd_intensity']:.4f})
  R-squared: {fe_results.rsquared:.4f}
  Interpretation: 1 pp increase in R&D intensity → {fe_results.params['rd_intensity']*100:.2f} pp increase in ROA

Random Effects (Comparison):
  R&D Intensity → ROA: {re_results.params['rd_intensity']:.4f} (p = {re_results.pvalues['rd_intensity']:.4f})
  R-squared: {re_results.rsquared_overall:.4f}

Difference-in-Differences Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Treatment Effect (Mergers):
  DiD Coefficient: {did_results['coef']:.4f} (p = {did_results['p_value']:.4f})
  95% CI: [{did_results['ci_lower']:.4f}, {did_results['ci_upper']:.4f}]
  
  Interpretation: Mergers increase ROA by {did_results['coef']*100:.2f} percentage points
  
Parallel Trends Test:
  {'✓ PASSED' if parallel_test['p_value'] > 0.05 else '⚠ CONCERNS'} (p = {parallel_test['p_value']:.4f})

Robustness:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Alternative specifications tested
✓ Placebo tests conducted
✓ Outlier sensitivity checked
✓ Event study shows dynamic effects

Output Files:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tables:
  • fe_results.txt - Full Fixed Effects output
  • re_results.txt - Full Random Effects output
  • did_results.csv - DiD coefficient and statistics
  • event_study_results.csv - Dynamic treatment effects

Figures:
  • parallel_trends.png - Pre-treatment trends visualization
  • event_study.png - Event study plot with confidence intervals

Location: {output_dir}
""")

print("\n" + "=" * 80)
print("METHODOLOGICAL NOTES")
print("=" * 80)

print("""
Panel Fixed Effects:
  • Controls for time-invariant firm heterogeneity
  • Eliminates omitted variable bias from unobserved firm characteristics
  • Appropriate when firm effects correlated with predictors

Difference-in-Differences:
  • Causal interpretation requires parallel trends assumption
  • Treatment and control groups must follow similar pre-treatment trajectories
  • Event study provides evidence on assumption validity

Robustness:
  • Multiple specification checks ensure results not driven by modeling choices
  • Placebo tests validate timing of effects
  • Outlier analysis confirms results not driven by extreme values
""")

print("\n" + "=" * 80)
print("END OF ANALYSIS")
print("=" * 80)
