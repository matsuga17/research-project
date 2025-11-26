# Corporate Data Quality Assurance Checklist

## Project Information
- **Project Name**: ___________________________
- **Researcher**: ___________________________
- **Date**: ___________________________
- **Data Sources**: ___________________________
- **Sample Period**: ___________________________
- **Final Sample Size**: _________ firm-years

---

## Phase 1: Data Collection Verification

### 1.1 Source Data Integrity
- [ ] All planned data sources successfully accessed
- [ ] Download dates documented for each source
- [ ] Raw data files backed up in `/data/raw/`
- [ ] Database versions recorded (if applicable)
- [ ] API queries or SQL scripts saved and commented

**Notes**: _________________________________

### 1.2 Data Completeness
- [ ] All expected variables present in raw data
- [ ] Record counts match expected values (±5%)
- [ ] Time coverage matches planned period
- [ ] Geographic/industry coverage as expected

**Expected vs. Actual**:
- Expected records: _________
- Actual records: _________
- Difference: _________ (______%)

**Notes**: _________________________________

---

## Phase 2: Data Cleaning Verification

### 2.1 Missing Data Analysis
- [ ] Missing data percentages calculated for all variables
- [ ] Missing data patterns investigated (random vs. systematic)
- [ ] Missing data treatment documented
- [ ] Missing data indicators created (where appropriate)

**Missing Data Summary**:
| Variable | Missing % | Treatment | Justification |
|----------|-----------|-----------|---------------|
| ________ | ________% | _________ | _____________ |
| ________ | ________% | _________ | _____________ |

**Notes**: _________________________________

### 2.2 Variable Type & Range Checks
- [ ] All numeric variables are indeed numeric (no text in numeric fields)
- [ ] Date variables properly formatted
- [ ] Categorical variables have expected categories only
- [ ] Negative values appropriate (or flagged for review)

**Issues Found & Resolved**:
1. _________________________________
2. _________________________________

### 2.3 Unit Consistency
- [ ] Currency units consistent across all sources
- [ ] Verified thousands vs. millions vs. billions
- [ ] Inflation adjustments applied (if planned)
- [ ] Exchange rate conversions documented (if multi-country)

**Standardization Applied**:
- Base currency: _________
- Base year for inflation: _________
- All monetary values in: _________ [units]

**Notes**: _________________________________

### 2.4 Outlier Treatment
- [ ] Outlier detection performed
- [ ] Outlier treatment method documented
- [ ] Thresholds specified (e.g., 1st/99th percentile)
- [ ] Number of observations winsorized/trimmed recorded

**Outlier Treatment Summary**:
| Variable | Method | Threshold | # Affected |
|----------|--------|-----------|------------|
| ________ | Winsorize | 1%/99% | _________ |
| ________ | Trimming | 3 SD | _________ |

**Notes**: _________________________________

---

## Phase 3: Variable Construction Verification

### 3.1 Financial Ratios
- [ ] ROA calculated correctly: Net Income / Total Assets
- [ ] Leverage calculated correctly: (LT Debt + ST Debt) / Total Assets
- [ ] Tobin's Q calculated correctly (or reasonable approximation documented)
- [ ] All ratio components sourced from same fiscal period

**Formula Verification** (spot check 10 random observations):
- [ ] ROA: Manually verified for _____ observations
- [ ] Leverage: Manually verified for _____ observations
- [ ] Tobin's Q: Manually verified for _____ observations

**Notes**: _________________________________

### 3.2 Transformations
- [ ] Log transformations applied to appropriate variables
- [ ] Handling of zero/negative values documented (e.g., log(x+1))
- [ ] Standardization/normalization (if used) applied correctly
- [ ] Lagged variables created with correct time alignment

**Transformation Check**:
| Original Var | Transformation | New Var | Verification |
|--------------|----------------|---------|--------------|
| Total Assets | ln(x) | log_assets | ✓ |
| __________ | __________ | __________ | __________ |

**Notes**: _________________________________

### 3.3 Indicator Variables
- [ ] Industry indicators created correctly
- [ ] Year indicators created correctly
- [ ] Missing data indicators match missing patterns
- [ ] Treatment/event indicators align with event dates

**Notes**: _________________________________

---

## Phase 4: Data Integration Verification

### 4.1 Merge Validation
- [ ] Merge keys validated (no duplicates in key variables)
- [ ] Match rates documented for each merge
- [ ] Unmatched observations identified and reviewed
- [ ] Merge type justified (inner, left, outer)

**Merge Statistics**:
| Source A | Source B | Match Key | Match Rate | Observations |
|----------|----------|-----------|------------|--------------|
| ________ | ________ | _________ | ________% | ____________ |
| ________ | ________ | _________ | ________% | ____________ |

**Unmatched Observations**: _____ (____%)
- Reason for non-match: _________________________________
- Action taken: _________________________________

### 4.2 Record Count Consistency
- [ ] No unexpected duplication after merges
- [ ] Record counts make logical sense
- [ ] Comparison with expected sample size

**Pre- and Post-Merge Counts**:
- Before first merge: _____ observations
- After first merge: _____ observations
- After second merge: _____ observations
- Final dataset: _____ observations

**Notes**: _________________________________

### 4.3 Variable Preservation
- [ ] Key variables from all sources retained
- [ ] No unintended data loss during merges
- [ ] Variable names clear and non-conflicting

**Notes**: _________________________________

---

## Phase 5: Panel Structure Verification

### 5.1 Panel Balance
- [ ] Panel structure documented (balanced vs. unbalanced)
- [ ] Firms with insufficient observations identified and handled
- [ ] Temporal gaps in firm data documented

**Panel Structure Summary**:
- Total unique firms: _________
- Average observations per firm: _________
- Min observations per firm: _________
- Max observations per firm: _________
- % of firms with complete time series: _________%

**Firms Dropped Due to Insufficient Data**: _____ firms
- Minimum threshold used: _____ years
- Justification: _________________________________

### 5.2 Firm Identifiers
- [ ] Unique firm identifier consistent across dataset
- [ ] No duplicate firm-year observations
- [ ] Firm identifiers link correctly across sources

**Duplicate Check**:
```python
df.duplicated(['firm_id', 'year']).sum() = _____
```
- If >0: Duplicates investigated and resolved: [ ]

**Notes**: _________________________________

### 5.3 Time Consistency
- [ ] Years in correct chronological order
- [ ] No firms with future data (look-ahead bias check)
- [ ] Fiscal year vs. calendar year alignment documented
- [ ] Reporting lags accounted for (if applicable)

**Time Alignment**:
- Using fiscal year: [ ] or calendar year: [ ]
- Reporting lag implemented: [ ] (_____ months)

**Notes**: _________________________________

---

## Phase 6: Domain-Specific Checks

### 6.1 Accounting Identity Verification
- [ ] Assets = Liabilities + Equity (within tolerance)
- [ ] Income statement coherence (Sales - Expenses ≈ Net Income)
- [ ] Cash flow statement coherence

**Accounting Errors**:
```python
df['accounting_error_pct'] = abs(at - (lt + ceq)) / at
```
- Observations with error >1%: _____ (____%)
- Action taken: _________________________________

**Notes**: _________________________________

### 6.2 Temporal Consistency
- [ ] No extreme year-over-year changes (without explanation)
- [ ] Sales growth rates reasonable
- [ ] Asset growth rates reasonable
- [ ] Negative growth rates investigated

**Extreme Changes** (flagged for review):
- Sales growth >500% or <-90%: _____ observations
- Asset growth >500% or <-90%: _____ observations
- Investigated and resolved: [ ]

**Notes**: _________________________________

### 6.3 Cross-Sectional Reasonableness
- [ ] Industry averages within expected ranges
- [ ] Firm size distribution reasonable
- [ ] Performance metrics (ROA, leverage) within typical ranges
- [ ] Comparison with published statistics (e.g., Compustat annual reports)

**Industry Averages** (spot check):
| Industry | Avg ROA | Avg Leverage | # Firms | Notes |
|----------|---------|--------------|---------|-------|
| ________ | _____% | _____% | _____ | _____ |
| ________ | _____% | _____% | _____ | _____ |

**Notes**: _________________________________

---

## Phase 7: Sample Selection Verification

### 7.1 Inclusion Criteria Applied
- [ ] All inclusion criteria applied in correct sequence
- [ ] Number of observations at each step documented
- [ ] Criteria justified and consistent with research design

**Sample Selection Sequence**:
| Step | Criterion | Observations Remaining | Observations Dropped |
|------|-----------|------------------------|----------------------|
| 0 | Initial raw data | __________ | --- |
| 1 | [Criterion 1] | __________ | __________ |
| 2 | [Criterion 2] | __________ | __________ |
| 3 | [Criterion 3] | __________ | __________ |
| Final | | __________ | Total: __________ |

**Notes**: _________________________________

### 7.2 Exclusion Criteria Applied
- [ ] Financial firms excluded (if planned): SIC 6000-6999
- [ ] Utilities excluded (if planned): SIC 4900-4999
- [ ] Other exclusions applied as planned

**Exclusions**:
- Financial firms dropped: _____ observations
- Utilities dropped: _____ observations
- Other exclusions: _____ observations
- Reason: _________________________________

**Notes**: _________________________________

### 7.3 Survival Bias Check
- [ ] Delisted/bankrupt firms included (if planned)
- [ ] Delisting information from CRSP incorporated
- [ ] Comparison of results with/without delisted firms (robustness)

**Survival Bias Assessment**:
- Firms delisted during sample period: _____ (____%)
- Delisting returns incorporated: [ ] Yes [ ] No
- Delisting reasons documented: [ ]

**Notes**: _________________________________

---

## Phase 8: Manual Validation

### 8.1 Sample-Based Verification
- [ ] Random sample of _____ observations selected for manual review
- [ ] Key variables cross-checked against original sources
- [ ] Discrepancies documented and resolved

**Sample Verification**:
- Sample size: _____ observations
- Sources checked: [e.g., SEC EDGAR 10-K filings]
- Error rate: _____% (_____ errors found)
- Errors corrected: [ ] Yes [ ] No

**Discrepancies Found**:
1. _________________________________
2. _________________________________

**Notes**: _________________________________

### 8.2 Extreme Value Verification
- [ ] Top and bottom 1% of each variable reviewed
- [ ] Extreme values verified against original sources
- [ ] Genuine vs. data errors distinguished

**Extreme Values Reviewed**:
| Variable | Extreme Type | # Reviewed | Genuine | Data Error |
|----------|--------------|------------|---------|------------|
| ________ | Top 1% | _____ | _____ | _____ |
| ________ | Bottom 1% | _____ | _____ | _____ |

**Actions Taken**: _________________________________

### 8.3 Time Series Visualization
- [ ] Time series plots created for random sample of firms
- [ ] Visual inspection for anomalies completed
- [ ] Identified anomalies investigated

**Sample Firms Plotted**: _____ firms
**Anomalies Found**: _____
- Description: _________________________________
- Resolution: _________________________________

**Notes**: _________________________________

---

## Phase 9: Documentation Completeness

### 9.1 Data Dictionary
- [ ] All variables documented with clear definitions
- [ ] Data sources specified for each variable
- [ ] Units specified (millions, thousands, etc.)
- [ ] Construction formulas provided for derived variables
- [ ] Missing value codes explained

**Data Dictionary Completion**: _____% complete

**Notes**: _________________________________

### 9.2 Codebook
- [ ] Sample selection process fully documented
- [ ] All inclusion/exclusion criteria listed with justifications
- [ ] Data cleaning steps documented with rationales
- [ ] Variable construction procedures detailed
- [ ] Merge procedures described

**Codebook Completion**: _____% complete

**Notes**: _________________________________

### 9.3 Replication Materials
- [ ] All data download scripts saved and commented
- [ ] Data cleaning scripts organized and documented
- [ ] Merge scripts saved with clear logic
- [ ] Scripts tested for reproducibility
- [ ] README file created with execution instructions

**Replication Package Completion**: _____% complete

**Notes**: _________________________________

---

## Phase 10: Final Dataset Checks

### 10.1 File Integrity
- [ ] Final dataset saved in multiple formats (.dta, .csv, .parquet)
- [ ] File sizes reasonable (not corrupted)
- [ ] Variable names consistent across formats
- [ ] Datasets loadable without errors

**File Information**:
- .dta file size: _____ MB
- .csv file size: _____ MB
- # Variables: _____
- # Observations: _____

**Notes**: _________________________________

### 10.2 Variable Summary Statistics
- [ ] Summary statistics generated for all variables
- [ ] Means, medians, SDs within expected ranges
- [ ] Min/max values reasonable
- [ ] Comparison with literature benchmarks

**Key Variables Summary**:
| Variable | Mean | Median | SD | Min | Max | N |
|----------|------|--------|----|----|-----|---|
| ________ | ____ | ______ | __ | __ | ___ | __ |
| ________ | ____ | ______ | __ | __ | ___ | __ |

**Notes**: _________________________________

### 10.3 Correlation Matrix
- [ ] Correlation matrix generated for key variables
- [ ] No perfect or near-perfect correlations (multicollinearity check)
- [ ] Correlations in expected directions

**Potential Multicollinearity Issues**:
- Variable pairs with r > 0.9: _________________________________
- Action taken: _________________________________

**Notes**: _________________________________

---

## Phase 11: Quality Assurance Report

### 11.1 Issues Log
**Major Issues Encountered**:
| Issue # | Description | Date Found | Resolution | Date Resolved |
|---------|-------------|------------|------------|---------------|
| 1 | __________ | ________ | __________ | __________ |
| 2 | __________ | ________ | __________ | __________ |

### 11.2 Known Limitations
**Documented Limitations**:
1. _________________________________
2. _________________________________
3. _________________________________

### 11.3 Recommendations for Users
**Important Notes for Data Users**:
1. _________________________________
2. _________________________________
3. _________________________________

---

## Final Sign-Off

### Quality Assurance Completion
- [ ] All checks completed
- [ ] All critical issues resolved
- [ ] Known limitations documented
- [ ] Dataset ready for analysis

**QA Performed By**: ___________________ (Name)
**Date**: ___________________
**Signature**: ___________________

**Reviewed By**: ___________________ (Name, if applicable)
**Date**: ___________________
**Signature**: ___________________

### Data Release Approval
- [ ] Dataset approved for analysis
- [ ] Documentation complete
- [ ] Replication materials prepared
- [ ] Backup copies secured

**Approved By**: ___________________ (PI or Data Manager)
**Date**: ___________________
**Signature**: ___________________

---

## Appendices

### Appendix A: Detailed Issue Descriptions
[Attach detailed descriptions of complex issues and their resolutions]

### Appendix B: Validation Sample Details
[List specific observations manually verified]

### Appendix C: Correspondence with Data Providers
[Document any clarifications received from database providers]

### Appendix D: Code Validation Outputs
[Attach outputs from quality check scripts]

---

**Notes Section**:
[Use this space for additional comments, observations, or documentation that doesn't fit elsewhere]