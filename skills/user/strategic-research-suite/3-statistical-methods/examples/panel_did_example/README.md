# Panel Regression and DiD Analysis Example

## Overview

Comprehensive example demonstrating **Panel Fixed Effects** and **Difference-in-Differences** analysis for strategic management research.

## Research Question

**Does R&D investment improve firm performance, and what is the causal effect of mergers?**

## Methods Demonstrated

### 1. Panel Regression
- **Fixed Effects (FE)**: Controls for unobserved firm heterogeneity
- **Random Effects (RE)**: Assumes random firm-specific effects
- **Hausman Test**: Tests FE vs RE specification

### 2. Difference-in-Differences (DiD)
- **Parallel Trends Test**: Pre-treatment trend validation
- **DiD Regression**: Causal effect estimation
- **Event Study**: Dynamic treatment effects
- **Robustness Checks**: Placebo tests, alternative specs

## Usage

### Quick Start

```bash
python run_panel_did_analysis.py
```

### Expected Runtime
**30-60 seconds** (200 firms × 10 years)

## Data Structure

### Panel Data
- **Firms**: 200
- **Time periods**: 2013-2022 (10 years)
- **Treatment**: Mergers (30% of firms in 2018)

### Variables
- **Outcome**: ROA (Return on Assets)
- **Key predictor**: R&D intensity
- **Treatment**: Merger dummy
- **Controls**: Firm size, leverage, firm age

## Output Files

Generated in `output/` directory:

### 1. Regression Tables
- `fe_results.txt` - Fixed Effects full output
- `re_results.txt` - Random Effects full output
- `did_results.csv` - DiD coefficient and statistics

### 2. Event Study
- `event_study_results.csv` - Dynamic treatment effects
- `event_study.png` - Event study plot with CIs

### 3. Visualizations
- `parallel_trends.png` - Pre-treatment trends
- `event_study.png` - Dynamic effects plot

## Example Output

### Panel Fixed Effects

```
                          PanelOLS Estimation Summary                           
================================================================================
Dep. Variable:                    roa   R-squared:                      0.6234
Estimator:                   PanelOLS   R-squared (Between):            0.4521
No. Observations:                2000   R-squared (Within):             0.6234
Date:                  Sun, Nov 02 2025   R-squared (Overall):           0.5823
                                        F-statistic (Within):          412.34

                          Parameter Estimates                          
======================================================================
            Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
----------------------------------------------------------------------
rd_intensity   0.4856     0.0234    20.754     0.000      0.4397     0.5315
firm_size      0.0123     0.0045     2.733     0.006      0.0035     0.0211
leverage      -0.0456     0.0123    -3.707     0.000     -0.0697    -0.0215
----------------------------------------------------------------------
```

**Interpretation**: A 1 percentage point increase in R&D intensity increases ROA by 0.49 percentage points, controlling for firm fixed effects.

### Difference-in-Differences

```
DiD Coefficient (Treat × Post): 0.0152
Standard Error: 0.0045
P-value: 0.0007
95% CI: [0.0064, 0.0240]

✓ Mergers increase ROA by 1.52 percentage points (p < 0.05)
```

**Causal Interpretation**: Firms that underwent mergers in 2018 experienced a 1.52 percentage point increase in ROA compared to control firms, after accounting for time-invariant differences and common time trends.

### Event Study

```
Event Study Coefficients:
  t=-3: -0.0023     (Pre-treatment, not significant)
  t=-2: -0.0011     (Pre-treatment, not significant)
  t=-1:  0.0000     (Reference period)
  t= 0:  0.0089**   (Treatment begins)
  t=+1:  0.0145***  (Effect grows)
  t=+2:  0.0168***  (Peak effect)
  t=+3:  0.0152***  (Sustained effect)
  t=+4:  0.0149***  (Sustained effect)
```

## Key Findings

### 1. R&D Investment Effects
- **Coefficient**: 0.4856 (p < 0.001)
- **Economic significance**: 1 pp increase in R&D → 0.49 pp increase in ROA
- **Robust** across specifications

### 2. Merger Effects (DiD)
- **Treatment effect**: +1.52 pp in ROA
- **Timing**: Effect emerges immediately, peaks at t+2
- **Parallel trends**: ✓ Validated (p = 0.234)
- **Robustness**: ✓ Passes placebo tests

## Interpretation Guide

### Panel Fixed Effects

**When to use**:
- Multiple observations per firm over time
- Unobserved firm characteristics may confound relationship
- Need to control for time-invariant heterogeneity

**Key assumption**:
- Strict exogeneity: εit independent of Xit for all periods

**Advantages**:
- Eliminates time-invariant omitted variable bias
- No need to observe all firm characteristics

### Difference-in-Differences

**When to use**:
- Treatment occurs at specific time for subset of firms
- Need causal interpretation
- Have untreated comparison group

**Key assumption**:
- Parallel trends: Treatment and control follow same trends absent treatment

**Validation**:
1. Pre-treatment trends test (should be insignificant)
2. Event study (no pre-treatment effects)
3. Placebo tests (fake treatment years)

## Robustness Checks Included

### 1. Alternative Specifications
- ✓ Without time fixed effects
- ✓ With industry × year interactions
- ✓ Alternative control variables

### 2. Placebo Tests
- ✓ Fake treatment year (2016 instead of 2018)
- ✓ Should find no effect in pre-treatment period

### 3. Sensitivity Analysis
- ✓ Exclude outliers (±3 SD)
- ✓ Alternative SE clustering
- ✓ Balanced panel only

### 4. Dynamic Effects
- ✓ Event study shows effect timing
- ✓ No anticipation effects
- ✓ Persistent treatment effects

## Customization

### Change Sample Size

```python
# Line 40-41
n_firms = 500  # Increase to 500 firms
n_years = 15   # Extend to 15 years
```

### Different Treatment

```python
# Line 57-61
treated = np.random.random() < 0.5  # 50% treatment rate
treatment_year = 2017  # Treatment in 2017
```

### Additional Controls

```python
# Line 155-158
regressor = PanelRegressor(
    predictors=['rd_intensity', 'firm_size', 'leverage', 'cash_flow', 'sales_growth']
)
```

## Extensions

### 1. Heterogeneous Treatment Effects

```python
# Test if effect varies by firm size
df['treated_large'] = df['treated'] * (df['firm_size'] > df['firm_size'].median())
df['treated_small'] = df['treated'] * (df['firm_size'] <= df['firm_size'].median())
```

### 2. Multiple Treatment Periods

```python
# Staggered adoption design
df['treatment_year'] = df.groupby('firm_id')['treated'].transform(
    lambda x: 2017 if x.sum() > 0 and np.random.random() < 0.5 else 2019 if x.sum() > 0 else None
)
```

### 3. Triple Differences

```python
# Add another dimension (e.g., industry)
df['triple_diff'] = df['treated'] * df['post'] * (df['industry'] == 'Tech')
```

## Common Issues

### "linearmodels not found"
```bash
pip install linearmodels
```

### "Parallel trends violated"
- Check pre-treatment period trends
- Consider matching or synthetic control methods
- Examine heterogeneity in treatment effects

### "Weak instruments" (if using IV)
- F-statistic should be > 10
- Consider alternative instruments
- Test for overidentification

## Statistical Notes

### Fixed vs Random Effects

**Use Fixed Effects when**:
- Firm effects correlated with predictors
- Hausman test rejects RE (p < 0.05)
- Focus on within-firm variation

**Use Random Effects when**:
- Firm effects uncorrelated with predictors
- Need to estimate time-invariant variables
- More efficient under correct specification

### DiD Assumptions

**Parallel Trends** (Critical):
- Treatment and control groups must follow parallel paths absent treatment
- Test: Regress outcome on treatment × pre-period interactions
- Visual: Plot group means over time

**No Anticipation**:
- Treatment should not affect pre-treatment outcomes
- Test: Event study shows no effects before t=0

**SUTVA**:
- Stable Unit Treatment Value Assumption
- No spillovers between treated and control firms

## References

### Panel Methods

1. **Wooldridge, J. M. (2010).**  
   *Econometric Analysis of Cross Section and Panel Data* (2nd ed.).  
   MIT Press.

2. **Baltagi, B. H. (2013).**  
   *Econometric Analysis of Panel Data* (5th ed.).  
   Wiley.

### Difference-in-Differences

3. **Angrist, J. D., & Pischke, J. S. (2009).**  
   *Mostly Harmless Econometrics: An Empiricist's Companion.*  
   Princeton University Press.

4. **Bertrand, M., Duflo, E., & Mullainathan, S. (2004).**  
   "How much should we trust differences-in-differences estimates?"  
   *Quarterly Journal of Economics*, 119(1), 249-275.

5. **Callaway, B., & Sant'Anna, P. H. (2021).**  
   "Difference-in-differences with multiple time periods."  
   *Journal of Econometrics*, 225(2), 200-230.

## Citation

```
Strategic Research Suite - Statistical Methods Module
Panel Regression and DiD Analysis Example
https://github.com/[your-repo]/strategic-research-suite
```

## Support

- Review module scripts: `panel_regression.py`, `did_analysis.py`
- Check SKILL.md for detailed documentation
- Consult full pipeline in `8-automation`

---

**Last Updated**: 2025-11-02  
**Version**: 1.0  
**Complexity**: ⭐⭐⭐⭐ (Advanced)
