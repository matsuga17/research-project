---
name: corporate-research-data-hub
description: Publication-grade data collection and management system (v2.0) specialized for empirical research in corporate finance, strategic management, corporate governance, and organizational studies. Features advanced quality assurance (Benford's Law, multivariate outlier detection), statistical power analysis, complete data lineage tracking (AEA-compliant), research progress management, and Docker-based reproducibility. Supports 11 Asian countries plus global free data sources. Includes pytest test suite and comprehensive tutorials. Perfect for researchers needing rigorous, reproducible workflows meeting top journal standards (JF, JFE, RFS, MS, SMJ).
metadata:
  version: "2.0"
  last_updated: "2025-10-31"
---

# Corporate Research Data Hub v2.0

A specialized skill for managing the entire data lifecycle in corporate and management research, from data discovery to panel dataset construction, with publication-grade quality assurance and complete reproducibility.

## 🎯 v2.0 Major Updates

- ✅ **Advanced Quality Assurance**: Top-journal standard statistical quality checks
- ✅ **Research Checklist Manager**: 7-phase progress tracking system
- ✅ **Data Lineage Tracker**: Complete provenance tracking (AEA-compliant)
- ✅ **Test Suite**: pytest-based comprehensive testing
- ✅ **Docker Support**: Full environment reproducibility
- ✅ **Enhanced Error Handling**: Production-ready robust error handling

## When to Use This Skill

This skill should be used when:
- Planning data collection for corporate finance or management research
- Searching for firm-level data (financial, market, governance, innovation, ESG)
- Constructing panel datasets with firm-year observations
- Integrating multiple corporate databases (e.g., Compustat + PatentsView)
- Handling survival bias, mergers, and corporate restructuring
- Standardizing financial variables across countries or time periods
- Performing quality checks specific to corporate data
- Managing industry classification and firm matching
- Documenting corporate data collection for publication

## Core Workflow Phases

### Phase 1: Research Design & Data Requirements

**Objective**: Define precise data requirements based on research questions in corporate studies

**Research Domains Covered**:
- **Corporate Finance**: Capital structure, dividend policy, investment decisions, firm valuation
- **Corporate Governance**: Board composition, ownership structure, executive compensation, shareholder activism
- **Strategic Management**: Diversification, internationalization, innovation, competitive dynamics
- **Organizational Behavior**: Human capital, organizational culture, leadership, employee relations
- **ESG & Sustainability**: Environmental performance, social responsibility, sustainability reporting

**Key Questions to Address**:
1. **Unit of Analysis**: Firm-level, firm-year, firm-quarter, business unit, industry-level?
2. **Sample Selection**:
   - Geographic scope (country, region, global)
   - Industry scope (specific industries vs. broad sample)
   - Firm size (SMEs, large firms, listed firms only)
   - Time period (start year, end year, data frequency)
   - Inclusion criteria (e.g., "publicly traded firms with >$100M revenue")
3. **Variable Requirements**:
   - **Dependent variables**: Firm performance (ROA, ROE, Tobin's Q), innovation output, ESG scores
   - **Independent variables**: Governance metrics, strategic choices, organizational characteristics
   - **Control variables**: Firm size, age, industry, leverage, R&D intensity
   - **Moderating/Mediating variables**: Environmental uncertainty, institutional factors

**Output**: Structured data requirements document with sample selection criteria

---

### Phase 2: Data Source Discovery & Evaluation

**Objective**: Identify optimal corporate databases and data sources

#### A. Primary Corporate Databases

**North America**:
1. **Compustat (S&P Capital IQ)**
   - Coverage: U.S. and Canadian public companies (1950-present)
   - Data: Comprehensive financial statements, market data, segment data
   - Access: Subscription through WRDS (Wharton Research Data Services)
   - Strengths: High quality, extensive history, well-documented
   - Limitations: Survivorship bias, restatement issues
   
2. **CRSP (Center for Research in Security Prices)**
   - Coverage: U.S. stock market data (1926-present)
   - Data: Daily/monthly stock prices, returns, trading volume, delisting information
   - Access: Subscription through WRDS
   - Strengths: Survivor-bias-free returns, adjustment for corporate actions
   - Use with: Compustat for comprehensive analysis

3. **ExecuComp**
   - Coverage: S&P 1500 executives (1992-present)
   - Data: Executive compensation, board characteristics, insider trading
   - Access: Subscription through WRDS
   - Integration: Links to Compustat via GVKEY

**Europe**:
1. **Bureau van Dijk (BvD) - Orbis**
   - Coverage: 400M+ companies globally, strong European coverage
   - Data: Financial statements, ownership, M&A, news
   - Access: Subscription (university or direct)
   - Strengths: Private and public firms, ownership structures
   - Limitations: Data quality varies by country, historical depth limited for some countries

2. **Datastream (Refinitiv)**
   - Coverage: Global market data, 175 countries
   - Data: Stock prices, indices, economic indicators, company financials
   - Access: Subscription
   - Strengths: Real-time and historical market data

**Asia-Pacific**:
1. **NEEDS-FinancialQUEST (Japan)**
   - Coverage: Japanese listed companies (1950s-present)
   - Data: Financial statements, stock prices, corporate actions
   - Access: Subscription (Nikkei)
   - Language: Japanese interface, data in Japanese accounting standards

2. **CSMAR (China)**
   - Coverage: Chinese listed companies (1990-present)
   - Data: Financial, market, governance data for A-shares, B-shares
   - Access: Subscription
   - Note: Requires understanding of Chinese accounting standards

3. **CMIE Prowess (India)**
   - Coverage: 40,000+ Indian companies
   - Data: Financial statements, ownership, projects
   - Access: Subscription

**Global Multi-Country**:
1. **Thomson Reuters Worldscope**
   - Coverage: 70+ countries, 70,000+ companies
   - Data: Standardized financial data, comparable across countries
   - Strengths: Cross-country consistency

2. **FactSet**
   - Coverage: Global coverage
   - Data: Financials, ownership, estimates, transcripts
   - Access: Subscription

#### B. Specialized Data Sources

**Innovation & Patents**:
1. **USPTO PatentsView**
   - Coverage: All U.S. patents (1976-present)
   - Data: Patent citations, inventors, assignees, classifications
   - Access: Free bulk download or API
   - Integration: Match to firms using company names/subsidiaries

2. **PATSTAT (EPO)**
   - Coverage: Global patent data from 90+ patent offices
   - Data: Patent applications, grants, citations, families
   - Access: Subscription or DVD purchase

3. **Kogan et al. (2017) Patent Value Dataset**
   - Coverage: U.S. patents with market-based valuations
   - Access: Free download from academic websites
   - Citation: Kogan, L., Papanikolaou, D., Seru, A., & Stoffman, N. (2017)

**ESG & Sustainability**:
1. **MSCI ESG Ratings**
   - Coverage: 14,000+ companies globally
   - Data: Environmental, social, governance scores
   - Access: Subscription (expensive)

2. **Refinitiv (Thomson Reuters) ESG**
   - Coverage: 11,000+ companies
   - Data: 630+ ESG metrics
   - Access: Subscription

3. **CDP (Carbon Disclosure Project)**
   - Coverage: 13,000+ companies
   - Data: Climate change, water, forest data
   - Access: Free for researchers (application required)

4. **Sustainalytics**
   - Coverage: 20,000+ companies
   - Data: ESG risk ratings
   - Access: Subscription

**Mergers & Acquisitions**:
1. **SDC Platinum (Thomson Reuters)**
   - Coverage: Global M&A, IPOs, joint ventures (1970s-present)
   - Data: Deal terms, parties, advisors, outcomes
   - Access: Subscription through WRDS

2. **Bureau van Dijk - Zephyr**
   - Coverage: Global M&A and IPO database
   - Data: Deal information, financials of involved parties

**Governance & Ownership**:
1. **ISS (Institutional Shareholder Services)**
   - Coverage: Board composition, voting results
   - Data: Director characteristics, committee memberships, proposals

2. **Thomson Reuters 13F**
   - Coverage: U.S. institutional ownership (13F filers)
   - Data: Quarterly holdings of institutional investors
   - Access: Through WRDS

**Analyst Forecasts & Recommendations**:
1. **I/B/E/S (Refinitiv)**
   - Coverage: Global analyst forecasts (1976-present)
   - Data: Earnings estimates, recommendations, price targets
   - Access: Through WRDS

**Macro & Industry Data**:
1. **World Bank Open Data**
   - Coverage: 200+ countries, 1960-present
   - Data: GDP, inflation, trade, governance indicators
   - Access: Free API and bulk download

2. **OECD Data**
   - Coverage: OECD countries + partners
   - Data: Economic indicators, industry statistics
   - Access: Free API

3. **Fama-French Data Library**
   - Coverage: U.S. market factors (1926-present)
   - Data: Market, size, value, profitability, investment factors
   - Access: Free download from Kenneth French's website

#### C. Free and Low-Cost Data Sources for Budget-Conscious Researchers

**🆕 COMPREHENSIVE GUIDE AVAILABLE**: See [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md) for detailed guidance on 70+ free data sources covering 11 Asian countries/regions plus global databases.

**Asia-Pacific Free Sources** (Complete coverage in FREE_LOW_COST_DATA_SOURCES.md):

1. **Japan** 🇯🇵
   - EDINET API: Financial statements (API available)
   - JPX: Stock prices (CSV)
   - e-Stat: Government statistics (API available)
   - **Cost**: ¥0

2. **South Korea** 🇰🇷
   - Open DART: Financial statements, governance (API available)
   - KRX: Stock prices (CSV)
   - KOSTAT: Corporate statistics (API available)
   - **Cost**: ¥0 (free API registration)

3. **China** 🇨🇳
   - CNINFO (巨潮資訊): Financial statements (HTML)
   - Tushare: Stock prices and financials (API, basic free)
   - AKShare: Completely free API (no registration)
   - **Cost**: ¥0

4. **Taiwan** 🇹🇼
   - TWSE: Stock prices (API available)
   - MOPS: Financial statements (HTML)
   - **Cost**: ¥0

5. **ASEAN Countries** 🌏
   - Singapore (SGX), Vietnam (HOSE/HNX), Malaysia (Bursa), Thailand (SET), Indonesia (IDX), Philippines (PSE)
   - **Cost**: ¥0 (varying data formats)

**Global Free Sources**:
- World Bank API: Macro indicators for 200+ countries
- IMF Data: Balance of payments, exchange rates
- OECD Data: Industry statistics, R&D data
- CDP Open Data: ESG data (free for researchers)
- Patent offices: USPTO, EPO, JPO (free bulk downloads)

**Practical Implementation**:
- Python scripts provided in [scripts/asian_data_collectors.py](scripts/asian_data_collectors.py)
- Sample project with ¥0 budget: [templates/sample_project_asian_roa.md](templates/sample_project_asian_roa.md)
- Quick start guide: [QUICKSTART.md](QUICKSTART.md)

**Key Advantages**:
- **Zero cost**: Suitable for researchers with no budget
- **API access**: Automated data collection possible
- **Official sources**: High data quality from government agencies
- **Research-grade**: Sufficient for top-tier journal publications

**When to Use Free Sources**:
- ✓ Budget-constrained PhD students and early-career researchers
- ✓ Asia-focused research (excellent coverage)
- ✓ Pilot studies before committing to paid databases
- ✓ Complementing commercial databases with additional variables

#### D. Data Source Evaluation Matrix

For each potential source, evaluate:

| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| **Variable Coverage** | 30% | Does it have all required variables? |
| **Sample Coverage** | 25% | Does it cover your geographic/industry/time scope? |
| **Data Quality** | 20% | Completeness, accuracy, consistency? |
| **Accessibility** | 15% | Cost, institutional access, download options? |
| **Documentation** | 10% | Clear variable definitions, known issues documented? |

**Decision Rules**:
- Score ≥80%: Primary data source
- Score 60-79%: Secondary source or supplementary data
- Score <60%: Consider alternatives

**Output**: Data source evaluation matrix with access plan

---

### Phase 3: Sample Construction & Data Collection Strategy

**Objective**: Design robust sample selection and data extraction plan

#### A. Sample Selection Procedure

**Step 1: Define Population**
```
Example:
- Population: All publicly traded firms in the U.S. manufacturing sector (SIC 2000-3999)
- Time Period: 2000-2023
- Data Frequency: Annual
```

**Step 2: Apply Inclusion Criteria**
Common inclusion criteria:
- Listed on major exchange (NYSE, NASDAQ, AMEX)
- Non-financial, non-utility firms (often excluded due to different accounting)
- Minimum data requirements (e.g., "must have complete financial data for ≥3 consecutive years")
- Minimum size threshold (e.g., "total assets ≥$10M in 2023 dollars")

**Step 3: Apply Exclusion Criteria**
Common exclusion criteria:
- Firms with negative book value of equity
- Firms with extreme values (e.g., leverage >10)
- Firms undergoing major restructuring
- ADRs or duplicate listings

**Step 4: Handle Survival Bias**

⚠️ **Critical Issue in Corporate Research**

**Problem**: Databases often exclude delisted/bankrupt firms, creating upward bias in performance measures.

**Solutions**:
1. **Use CRSP Delisting Information**:
   - CRSP provides delisting returns and reasons (dlret, dlstcd)
   - Include delisted firms up to their delisting date
   - Adjust returns for delisting events

2. **Use Historical Vintages**:
   - Some databases provide "as-of" snapshots
   - Capture firms that existed at each point in time

3. **Document and Test**:
   - Report % of firms delisted during sample period
   - Compare results with and without delisted firms
   - Conduct robustness checks

**Step 5: Create Unique Firm Identifier**

Most databases use proprietary identifiers:
- Compustat: GVKEY (permanent), permco (CRSP link)
- CRSP: PERMNO (security-level), PERMCO (company-level)
- Orbis: BvD ID number
- Datastream: ISIN

**Best Practice**: Create a master crosswalk file linking identifiers across databases.

```
Example Crosswalk:
| firm_id | gvkey | permno | cusip | isin | ticker | firm_name |
|---------|-------|--------|-------|------|--------|-----------|
```

#### B. Data Extraction Strategy

**For SQL-based Databases (e.g., WRDS)**:

```sql
-- Example: Extract Compustat annual financial data
SELECT 
    gvkey,
    fyear,
    datadate,
    at,      -- Total assets
    sale,    -- Sales revenue
    ni,      -- Net income
    ceq,     -- Common equity
    dltt,    -- Long-term debt
    dlc,     -- Short-term debt
    xrd,     -- R&D expenditure
    capx,    -- Capital expenditure
    sich     -- SIC code
FROM 
    comp.funda
WHERE 
    fyear BETWEEN 2000 AND 2023
    AND indfmt = 'INDL'    -- Industrial format
    AND datafmt = 'STD'     -- Standardized
    AND popsrc = 'D'        -- Domestic (for U.S. firms)
    AND consol = 'C'        -- Consolidated statements
    AND sich BETWEEN 2000 AND 3999  -- Manufacturing
;
```

**For API-based Sources**:
- Use rate-limited requests (e.g., max 10 requests/minute)
- Implement exponential backoff for failed requests
- Cache responses to avoid redundant calls
- Document API version and access date

**For Web-based Downloads**:
- Check Terms of Service before automated scraping
- For one-time downloads: manually download and document source
- For updates: consider APIs or subscription services

**Output**: 
- Extraction scripts with clear comments
- Raw data files with original variable names
- Extraction log (date, source, query used)

---

### Phase 3.5: Statistical Power Analysis & Sample Size Design

**Objective**: Ensure adequate statistical power BEFORE data collection

#### Why Statistical Power Matters

**Common Mistake**: Researchers collect "all available data" without considering:
1. **Type II Error Rate (β)**: Probability of failing to detect a true effect
2. **Statistical Power (1-β)**: Ability to detect effects when they exist  
3. **Minimum Detectable Effect (MDE)**: Smallest effect the study can reliably detect

**Consequences of Underpowered Studies**:
- False negatives: Missing real effects
- Overestimation of effect sizes (winner's curse)
- Irreplicable results
- Wasted research resources

#### Pre-Registration of Sample Size

**Best Practice**: Calculate required sample size BEFORE data collection.

**Steps**:

1. **Specify Expected Effect Size**
   - Literature review: What effect sizes do similar studies find?
   - Practical significance: What effect size matters for theory/practice?
   - Conservative approach: Use lower bound of prior estimates

2. **Set Statistical Parameters**
   - α (Type I error): Typically 0.05
   - 1-β (Power): Standard is 0.80, but 0.90 recommended for high-stakes studies
   - Two-sided vs. one-sided tests

3. **Calculate Required Sample**

```python
from data_quality_checker import SampleSizeCalculator

calc = SampleSizeCalculator()

# For regression with 8 control variables
result = calc.regression_sample_size(
    num_predictors=8,
    expected_r2=0.12,  # Based on pilot or literature
    power=0.80
)

print(f"Required N: {result['recommended_n']}")
```

4. **Adjust for Data Constraints**
   - Cluster-robust SE: Increase required N by design effect
   - Missing data: Add buffer (e.g., 20% more)
   - Subgroup analysis: Multiply by number of subgroups

5. **Document Pre-Analysis Plan**
   - Register at: OSF (osf.io), AsPredicted.org, or AEA RCT Registry
   - Include: Hypotheses, sample size justification, analysis plan

#### Sensitivity Analysis

If required sample size exceeds availability:

**Option 1: Adjust Research Question**
- Focus on larger effects
- Use stronger treatments/interventions
- Compare more distinct groups

**Option 2: Report Minimum Detectable Effect**

```python
# Calculate what effect can be detected with available N
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
mde = analysis.solve_power(
    nobs1=250,  # Available sample size per group
    alpha=0.05,
    power=0.80,
    alternative='two-sided'
)
print(f"MDE (Cohen's d): {mde:.3f}")
```

**Option 3: Conduct Pilot Study**
- Collect small sample to refine effect size estimates
- Use for power analysis of main study
- Report pilot results separately

#### Panel Data Considerations

**Additional Factors**:
- **Clustering**: Firms cluster observations → reduce effective N
- **Fixed Effects**: Consume degrees of freedom
- **Attrition**: Firms exit sample → imbalanced panel

**Solution**: Use panel-specific power calculators:

```python
calc = SampleSizeCalculator()

panel_result = calc.panel_data_sample_size(
    num_firms=300,
    num_periods=5,
    effect_size='medium',
    power=0.80
)

print(f"Required firms: {panel_result['required_firms']}")
print(f"Design effect: {panel_result['design_effect']:.2f}")
```

#### Reporting Standards

**In Methodology Section**, include:
- Expected effect size and its source
- Power analysis results
- Actual achieved power (post-hoc)
- Justification if underpowered

**Example Language**:
> "Based on Cohen et al. (2020)'s meta-analysis reporting a mean effect size of 
> d=0.45, we conducted an a priori power analysis. To detect this effect with 
> 80% power at α=0.05, we require N=158 per group. Our final sample of N=180 
> per group provides 85% power."

#### Tools and Resources

**Python Libraries**:
- `statsmodels.stats.power`: Parametric power analysis
- `pingouin`: General-purpose power analysis
- `pwr` (R): Comprehensive power analysis suite

**Online Calculators**:
- G*Power: https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower
- PASS: https://www.ncss.com/software/pass/

**Reference**:
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Routledge.

---

### Phase 4: Data Cleaning & Standardization

**Objective**: Transform raw data into analysis-ready panel dataset

#### A. Financial Data Standardization

**Issue**: Raw financial data requires substantial cleaning.

**Common Problems**:
1. **Currency inconsistencies**: Mixing thousands, millions, billions
2. **Negative values**: Some databases use negative signs for expenses
3. **Missing data codes**: -9999, 0, NULL all mean different things
4. **Restatements**: Historical data may change
5. **Fiscal year misalignment**: Different fiscal year ends

**Standardization Procedure**:

**Step 1: Identify and Document Units**
```python
# Example: Compustat data is in millions
# Convert all to consistent units (e.g., thousands)
df['total_assets'] = df['at'] * 1000
```

**Step 2: Handle Missing Data**
```python
# Distinguish between "truly zero" and "missing"
# Compustat: missing = NaN, zero = 0, not available = -9999 (varies by field)

# Replace data errors with NaN
df.loc[df['xrd'] < 0, 'xrd'] = np.nan  # R&D cannot be negative

# For some variables, 0 may be meaningful (no debt, no dividend)
# Document your decisions
```

**Step 3: Winsorize Extreme Values**
```python
# Common practice: winsorize continuous variables at 1% and 99%
from scipy.stats.mstats import winsorize

df['roa'] = winsorize(df['roa'], limits=[0.01, 0.01])
```

**Step 4: Construct Financial Ratios**
```python
# Return on Assets (ROA)
df['roa'] = df['net_income'] / df['total_assets']

# Leverage
df['leverage'] = (df['long_term_debt'] + df['short_term_debt']) / df['total_assets']

# Tobin's Q (approximation)
df['tobins_q'] = (df['market_value'] + df['book_debt']) / df['total_assets']

# R&D Intensity
df['rd_intensity'] = df['xrd'] / df['sale']
# Handle missing R&D (common in non-tech industries)
df['rd_intensity'].fillna(0, inplace=True)
df['rd_missing'] = df['xrd'].isna().astype(int)  # Create indicator
```

**Step 5: Adjust for Inflation**
```python
# Use GDP deflator or CPI to convert to constant dollars
# Get deflator from FRED API or World Bank

# Example: Convert to 2023 dollars
df['real_sales'] = df['sales'] * (cpi_2023 / df['cpi_year'])
```

**Step 6: Log Transformations**
```python
# Common for size variables (assets, sales, employees)
df['log_assets'] = np.log(df['total_assets'])
# Add 1 if zeros are present
df['log_rd'] = np.log(df['xrd'] + 1)
```

#### B. Industry Classification Standardization

**Problem**: Multiple classification systems exist, and they change over time.

**Common Systems**:
- **SIC (Standard Industrial Classification)**: 4-digit, U.S.-centric, outdated (last updated 1987)
- **NAICS (North American Industry Classification System)**: 6-digit, updated every 5 years
- **GICS (Global Industry Classification Standard)**: 8-digit, by S&P and MSCI, used globally
- **Fama-French Industry Classifications**: 5, 10, 12, 17, 30, 38, 48, 49 industry groups

**Conversion Strategy**:
1. **Use Primary Classification Consistently**:
   - If using U.S. data pre-2000: Use SIC
   - If using U.S. data post-2000: Consider NAICS
   - If comparing across countries: Use GICS

2. **Apply Concordance Tables**:
   - SIC to NAICS: U.S. Census Bureau provides concordance
   - NAICS to SIC: Available from Census
   - SIC/NAICS to Fama-French: Kenneth French's website

3. **Create Industry Indicators**:
```python
# Fama-French 12 industry classification (example)
def ff12_industry(sic):
    if 100 <= sic <= 999: return 1   # Consumer NonDurables
    elif 2000 <= sic <= 2399: return 2  # Consumer Durables
    # ... (see full mapping)
    else: return 12  # Other

df['ff12_ind'] = df['sich'].apply(ff12_industry)
```

4. **Handle Industry Changes**:
   - Firms sometimes change industries (M&A, diversification)
   - Use historical industry codes when available
   - Document any manual adjustments

**Output**: Standardized industry classification with documentation

#### C. Time Alignment

**Issue**: Data from different sources may have different timing conventions.

**Common Misalignments**:
1. **Fiscal Year vs. Calendar Year**:
   - Firm with fiscal year ending June 30, 2023 → fyear=2023 but covers July 2022-June 2023
   - Market data is calendar-year
   
2. **Reporting Lags**:
   - Financial statements released 2-3 months after fiscal year end
   - Investors cannot act on FY2023 data until Mar/Apr 2024

**Solutions**:
1. **Align to Calendar Year**:
```python
# Use datadate (statement date) instead of fyear
df['calendar_year'] = df['datadate'].dt.year
```

2. **Implement Point-in-Time Alignment**:
```python
# Lag financial data by 4 months to account for reporting lag
df['report_year'] = df['datadate'] + pd.DateOffset(months=4)
df['analysis_year'] = df['report_year'].dt.year
```

3. **For Regressions with Lagged Variables**:
```python
# Lagged variables (t-1)
df['lag_roa'] = df.groupby('firm_id')['roa'].shift(1)
df['lag_size'] = df.groupby('firm_id')['log_assets'].shift(1)

# Lead variables (t+1) for future outcomes
df['lead_performance'] = df.groupby('firm_id')['roa'].shift(-1)
```

**Output**: Time-aligned panel dataset

---

### Phase 5: Multi-Source Data Integration

**Objective**: Merge data from multiple sources while preserving data integrity

#### A. Matching Strategies

**Strategy 1: Direct Identifier Matching** (Preferred)
- Use GVKEY, PERMNO, CUSIP, ISIN when available
- Most reliable but requires crosswalk files

**Strategy 2: Name Matching** (When identifiers unavailable)
- Clean company names (remove Inc., Ltd., Corp., etc.)
- Standardize (uppercase, remove spaces)
- Use fuzzy matching for imperfect matches

```python
from fuzzywuzzy import fuzz, process

# Example: Match patent assignee names to Compustat firms
def fuzzy_match(name, choices, threshold=85):
    match, score = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if score >= threshold:
        return match
    else:
        return None

df_patents['matched_firm'] = df_patents['assignee'].apply(
    lambda x: fuzzy_match(x, df_compustat['firm_name'].tolist())
)
```

⚠️ **Caution**: Fuzzy matching can produce false positives. Manually verify a random sample.

**Strategy 3: CUSIP/Ticker Matching**
- CUSIP (9-character): Unique security identifier
- First 6 characters: Issuer identifier (same for all securities of a firm)
- Tickers change frequently (mergers, rebranding)

**Best Practice**: Use CUSIP6 or GVKEY-PERMNO links.

#### B. Panel Data Merging

**Common Merge Types**:

1. **One-to-One Merge** (firm-year to firm-year):
```python
df_merged = pd.merge(
    df_financial,      # Compustat data
    df_governance,     # ISS data
    on=['gvkey', 'year'],
    how='inner',       # Keep only matched observations
    validate='one_to_one',  # Ensure no duplicates
    indicator=True     # Track merge success
)

# Check merge results
print(df_merged['_merge'].value_counts())
```

2. **Many-to-One Merge** (multiple securities per firm):
```python
# Example: Merge CRSP (security-level) with Compustat (firm-level)
df_merged = pd.merge(
    df_crsp,           # Security-level returns
    df_compustat,      # Firm-level financials
    left_on=['permco', 'year'],
    right_on=['permco', 'year'],
    how='left',
    validate='many_to_one'
)
```

3. **Many-to-Many Merge** (Use with caution):
```python
# Example: Merge patent data (multiple patents per firm-year) with financial data
# Step 1: Aggregate patents to firm-year level first
df_patents_agg = df_patents.groupby(['firm_id', 'year']).agg({
    'patent_count': 'sum',
    'citation_count': 'sum',
    'patent_value': 'mean'
}).reset_index()

# Step 2: Then merge
df_merged = pd.merge(df_financial, df_patents_agg, on=['firm_id', 'year'], how='left')
# Fill missing patent counts with 0 (firms with no patents)
df_merged[['patent_count', 'citation_count']].fillna(0, inplace=True)
```

#### C. Merge Validation

**Critical Checks**:

1. **Record Count Validation**:
```python
print(f"Pre-merge: Financial data has {len(df_financial)} observations")
print(f"Pre-merge: Governance data has {len(df_governance)} observations")
print(f"Post-merge: {len(df_merged)} observations")

# Check for unexpected duplication
assert len(df_merged) <= len(df_financial) + len(df_governance), "Unexpected duplication!"
```

2. **Key Variable Preservation**:
```python
# Ensure no data loss in critical variables
assert df_financial['total_assets'].sum() == df_merged['total_assets'].sum(), "Asset values changed!"
```

3. **Missing Data Pattern Analysis**:
```python
# Check which observations were not matched
unmatched = df_merged[df_merged['_merge'] != 'both']
print(f"Unmatched observations: {len(unmatched)} ({len(unmatched)/len(df_merged)*100:.1f}%)")

# Analyze unmatched by year (may indicate database coverage gaps)
print(unmatched.groupby('year').size())
```

4. **Systematic Bias Check**:
```python
# Test if matched firms differ systematically from unmatched
from scipy.stats import ttest_ind

matched = df_merged[df_merged['_merge'] == 'both']
unmatched = df_merged[df_merged['_merge'] != 'both']

t_stat, p_value = ttest_ind(matched['total_assets'], unmatched['total_assets'], nan_policy='omit')
print(f"T-test for size difference: t={t_stat:.2f}, p={p_value:.3f}")

# If p < 0.05: Matched and unmatched firms differ significantly → potential selection bias
```

**Output**:
- Integrated panel dataset (firm-year observations)
- Merge report documenting match rates
- List of unmatched observations for manual review

---

### Phase 6: Advanced Quality Assurance for Corporate Data

**Objective**: Implement statistically rigorous quality assurance procedures meeting top-journal standards

**Why Phase 6 is Critical**:
- Top journals (JF, JFE, RFS, MS, SMJ) require documented quality assurance
- Data errors can invalidate entire studies
- Fraud detection prevents retractions
- Comprehensive QA builds reviewer confidence

**Quality Assurance Framework**: 7 complementary tests

---

#### A. Multivariate Outlier Detection (Ensemble Method)

**Challenge**: Single-method outlier detection is unreliable.

**Solution**: Use 3 methods and require consensus (2/3 agreement).

**Method 1: Mahalanobis Distance**
- Measures multivariate distance from centroid
- Accounts for correlations between variables
- Threshold: Chi-square distribution (α=0.001)

**Method 2: Isolation Forest**
- Machine learning approach
- Isolates anomalies efficiently
- Contamination rate: 1%

**Method 3: Local Outlier Factor (LOF)**
- Density-based method
- Identifies local deviations
- Neighbors: 20

```python
from data_quality_checker import AdvancedQualityAssurance

# Initialize QA system
qa = AdvancedQualityAssurance(
    df, 
    firm_id='firm_id', 
    time_var='year',
    verbose=True
)

# Run comprehensive QA
report = qa.run_comprehensive_qa()

# Outlier detection results
print(f"Total outliers: {report['outliers']['total_outliers']}")
print(f"High confidence (3/3 methods): {report['outliers']['high_confidence_outliers']}")

# Outlier flags added to dataframe
# df['outlier_flag'] = 1 if outlier
# df['outlier_confidence'] = 0.0-1.0 (proportion of methods detecting)
```

**Decision Rules**:
- **High confidence outliers (3/3 methods)**: Investigate individually
- **Medium confidence (2/3 methods)**: Include but flag
- **Low confidence (1/3 methods)**: Retain without flagging

**Typical Outlier Rate**: 1-3% (if higher, check data source issues)

---

#### B. Fraud Detection: Benford's Law Test

**Theory**: In naturally occurring data, first digits follow Benford's distribution:
```
P(first digit = d) = log₁₀(1 + 1/d)
```

**Application**: Test financial variables (sales, assets, income)

```python
# Benford's Law test (automatically run by AdvancedQualityAssurance)
benford_result = report['benfords_law']

if not benford_result['conforms_to_benford']:
    print("⚠️ WARNING: Deviation from Benford's Law detected")
    print(f"   χ² = {benford_result['chi2_statistic']:.2f}")
    print(f"   p-value = {benford_result['p_value']:.4f}")
    print("   Possible causes:")
    print("   - Data manipulation")
    print("   - Artificial data generation")
    print("   - Specific selection criteria")
```

**Interpretation**:
- **p > 0.05**: Data conforms (normal)
- **p < 0.05**: Investigate potential manipulation
- **Note**: Benford's Law may not apply to:
  - Assigned numbers (IDs, codes)
  - Data with built-in constraints
  - Very small samples (n < 100)

**What to do if test fails**:
1. Verify data collection process
2. Check for artificial constraints
3. Examine data source documentation
4. Consider excluding suspect data
5. Document in limitations section

---

#### C. Regression-Based Anomaly Detection

**Concept**: Flag observations with large prediction errors from expected values.

**Method**:
1. Regress outcome on predictors (e.g., ROA ~ log_assets + leverage + age)
2. Calculate standardized residuals
3. Flag observations with |residual| > 3σ

```python
# Automatically identifies anomalies
anomaly_result = report['anomalies']

print(f"Anomalies detected: {anomaly_result['total_anomalies']}")
print(f"Model R² = {anomaly_result['r_squared']:.3f}")

# Anomaly flags added to dataframe
# df['anomaly_flag'] = 1 if anomaly
# df['regression_residual'] = standardized residual
```

**Common Causes of Anomalies**:
- Mergers & acquisitions (M&A)
- Divestitures / spin-offs
- Extraordinary items
- Measurement errors
- Data entry errors

**Treatment**:
1. Review anomalous observations individually
2. Check 10-K filings for explanations
3. Document legitimate anomalies (M&A, etc.)
4. Correct or exclude erroneous data

---

#### D. Structural Break Detection (Chow Test)

**Purpose**: Identify discontinuities in time series that may indicate:
- Accounting standard changes
- Database updates
- Systematic errors

**Method**: F-test for equality of means across time periods

```python
# Structural break test
break_result = report['structural_breaks']

if break_result['breaks_detected'] > 0:
    print(f"⚠️ {break_result['breaks_detected']} structural breaks found:")
    for bp in break_result['break_points']:
        print(f"   Year {bp['time']}: F={bp['f_statistic']:.2f}, p={bp['p_value']:.4f}")
```

**What to do with breaks**:
1. **Accounting changes**: Document and control in regressions
2. **Database updates**: Verify with data provider
3. **Real economic shocks**: Legitimate (e.g., 2008 crisis) - document
4. **Data errors**: Exclude affected periods

**Example**: FASB ASC 606 revenue recognition change (2018)
- Expected break in revenue variables
- Control with post-2018 dummy variable

---

#### E. Influential Observations (Cook's Distance)

**Question**: Which observations disproportionately influence regression results?

**Measure**: Cook's Distance
- Combines leverage (unusual X values) and residuals (unusual Y values)
- Threshold: 4/n (common rule)

```python
# Influential observation detection
influence_result = report['influential_obs']

print(f"Influential observations: {influence_result['total_influential']}")
print(f"Cook's D threshold: {influence_result['threshold']:.4f}")

# Cook's distance added to dataframe
# df['cooks_distance'] = Cook's D value
# df['influential_flag'] = 1 if influential
```

**Treatment**:
1. **Investigate** all influential observations
2. **Check** for data errors
3. **Document** legitimate high-influence cases
4. **Robustness check**: Re-run analysis excluding influential observations
5. **Report** whether results change substantially

**Reporting Standard**:
> "We identified 12 influential observations (Cook's D > 0.02). Excluding these 
> observations, our main result remains significant (β = 0.045, p < 0.01), 
> confirming robustness."

---

#### F. Publication Bias Test (Egger's Test)

**Context**: When synthesizing multiple studies or effect sizes

**Problem**: Positive results more likely to be published → biased literature

**Test**: Regress effect sizes on precision (1/SE)
- Significant intercept → publication bias likely

```python
# If your dataset contains effect sizes and standard errors
if 'effect_size' in df.columns and 'standard_error' in df.columns:
    pub_bias_result = report['publication_bias']
    
    if pub_bias_result['bias_detected']:
        print("⚠️ Publication bias detected")
        print(f"   Intercept = {pub_bias_result['intercept']:.4f}")
        print(f"   p-value = {pub_bias_result['p_value']:.4f}")
```

**Interpretation**:
- **p < 0.10**: Evidence of publication bias
- **p ≥ 0.10**: No strong evidence

**Application**:
- Meta-analyses
- Multi-study datasets
- Replication studies

---

#### G. Sample Selection Bias Tests

**Types of Selection Bias**:

**1. Survival Bias**
- Only successful (surviving) firms in sample
- Ignores firms that exited/failed
- Overestimates average performance

**2. Attrition Bias**
- Firms systematically drop out over time
- Non-random attrition affects results

**Test 1: Balance Panel Analysis**
```python
selection_result = report['selection_bias']

print(f"Total firms: {selection_result['total_firms']}")
print(f"Balanced panel firms: {selection_result['balanced_firms']} ({selection_result['balance_rate']:.1f}%)")
print(f"Attrition rate: {selection_result['attrition_rate']:.1f}%")

if selection_result['warning']:
    print("⚠️ WARNING: High attrition rate (>30%) suggests selection bias")
```

**Test 2: Heckman Selection Model** (if needed)
```python
# For severe selection bias, implement Heckman two-stage
from statsmodels.regression.linear_model import OLS
from statsmodels.discrete.discrete_model import Probit

# Stage 1: Probit model for selection
selection_model = Probit(df['in_sample'], df[['log_assets', 'age', 'roa']]).fit()
df['inverse_mills_ratio'] = selection_model.predict()

# Stage 2: OLS with IMR as control
outcome_model = OLS(df['outcome'], df[['predictor', 'inverse_mills_ratio']]).fit()
```

**Reporting Standards**:
- Document attrition rates
- Test if attritors differ systematically
- Use Heckman if attrition >20% and systematic

---

#### H. Accounting Identity Verification

**Critical Identities to Check**:

**Identity 1: Balance Sheet**
```
Assets = Liabilities + Shareholders' Equity
```

**Identity 2: Cash Flow Statement**
```
Δ Cash = Operating CF + Investing CF + Financing CF
```

**Identity 3: Income Statement Links**
```
Retained Earnings(t) = Retained Earnings(t-1) + Net Income(t) - Dividends(t)
```

**Implementation**:
```python
# Accounting identity checks (automatically run)
# Check Balance Sheet identity
df['bs_error'] = abs(df['at'] - (df['lt'] + df['ceq']))
df['bs_error_pct'] = df['bs_error'] / df['at']

# Flag errors >1%
bs_errors = df[df['bs_error_pct'] > 0.01]
print(f"Balance sheet errors (>1%): {len(bs_errors)} ({len(bs_errors)/len(df)*100:.2f}%)")

# Acceptable error rate: <2%
# If >5%: Data source issue - investigate immediately
```

**What to do with errors**:
- **<1% error**: Likely rounding - acceptable
- **1-5% error**: Flag but retain
- **>5% error**: Investigate data source, consider excluding

---

#### I. Temporal Consistency Checks

**Principle**: Corporate fundamentals evolve gradually (except for discrete events)

**Tests**:

**Test 1: Growth Rate Bounds**
```python
# Sales growth should not exceed ±500% (except M&A)
df['sales_growth'] = df.groupby('firm_id')['sale'].pct_change()

extreme_growth = df[
    (df['sales_growth'] > 5) | (df['sales_growth'] < -0.9)
]

# Review each case individually
for idx, row in extreme_growth.iterrows():
    print(f"Firm {row['firm_id']} year {row['year']}: growth = {row['sales_growth']*100:.1f}%")
    # Check for M&A, spin-offs, accounting changes
```

**Test 2: Sequential Plausibility**
```python
# Variables should be non-negative
assert (df['at'] >= 0).all(), "Negative assets detected!"
assert (df['sale'] >= 0).all(), "Negative sales detected!"

# Debt ratio should be [0, ~2]
leverage_issues = df[(df['leverage'] < 0) | (df['leverage'] > 3)]
if len(leverage_issues) > 0:
    print(f"⚠️ {len(leverage_issues)} observations with implausible leverage")
```

---

#### J. Cross-Sectional Reasonableness

**Industry Benchmarks**: Compare to known industry norms

```python
# Industry statistics
industry_stats = df.groupby('ff12_ind').agg({
    'roa': ['mean', 'median', 'std'],
    'leverage': ['mean', 'median'],
    'firm_id': 'count'
}).round(3)

print(industry_stats)

# Flag industries with suspicious patterns
# Example: Banking industry with average leverage < 0.5 → suspicious
```

**Known Industry Benchmarks** (approximate):
- **Technology**: ROA ~10-15%, Leverage ~20-30%
- **Manufacturing**: ROA ~5-8%, Leverage ~30-40%
- **Retail**: ROA ~3-5%, Leverage ~40-50%
- **Utilities**: ROA ~4-6%, Leverage ~50-60%
- **Finance**: ROA ~1-2% (of assets), Leverage 80-90%

**Flags**:
- Industry average ROA < -10% or > 20%
- Industry average leverage < 0% or > 90% (non-financial)
- Industry standard deviation > 3× typical

---

#### K. Quality Assurance Documentation

**Required QA Report Sections**:

**1. Sample Construction**:
```
Initial observations: 45,230
Dropped: Missing financial data (3,402)
Dropped: Insufficient years (<3) (1,234)
Dropped: Failed accounting identities (234)
Dropped: Outliers (567)
Final sample: 39,793 observations
```

**2. Outlier Treatment**:
```
Method: Ensemble outlier detection (3 methods)
Outliers detected: 612 (1.5%)
Treatment: Winsorized at 1st and 99th percentiles
Variables winsorized: ROA, Leverage, Tobin's Q
```

**3. Quality Test Results**:
| Test | Result | Status |
|------|--------|--------|
| Benford's Law | χ²=8.3, p=0.12 | ✓ Pass |
| Accounting Identities | 1.2% error rate | ✓ Pass |
| Structural Breaks | 0 detected | ✓ Pass |
| Attrition Rate | 18% | ✓ Acceptable |

**4. Known Limitations**:
- Survival bias: Sample excludes bankrupt firms (may overstate avg. performance)
- Coverage: Limited to publicly traded firms
- Variable measurement: R&D data missing for 23% of firms

**5. Robustness Checks Performed**:
- [ ] Excluding influential observations
- [ ] Alternative variable definitions
- [ ] Alternative sample periods
- [ ] Subgroup analysis

**Output**: 
- `QA_Report.html` (interactive)
- `QA_Report.pdf` (for appendix)
- `qa_summary.json` (machine-readable)

---

#### L. Best Practice Checklist

Before proceeding to Phase 7, ensure:

- [ ] All 7 quality tests completed
- [ ] Outlier detection results documented
- [ ] Accounting identities verified (<2% error rate)
- [ ] Benford's Law test passed OR exception documented
- [ ] Structural breaks identified and explained
- [ ] Influential observations investigated
- [ ] Attrition/survival bias assessed
- [ ] QA report generated and reviewed
- [ ] Known data limitations documented
- [ ] Robustness checks planned

**Gold Standard**: Anticipate reviewer questions
- "How do you know your data is accurate?"
- "Did you check for outliers?"
- "What about survival bias?"
- "Could data manipulation explain the results?"

**A comprehensive Phase 6 QA process answers all these questions proactively.**

---

### Phase 7: Final Dataset Construction & Documentation

**Objective**: Create publication-ready dataset with complete documentation

#### A. Dataset Structuring

**Panel Data Format** (Long format preferred):
```
| firm_id | year | industry | country | total_assets | sales | net_income | roa | ... |
|---------|------|----------|---------|--------------|-------|------------|-----|-----|
| 001     | 2020 | Manuf    | USA     | 1000         | 500   | 50         | 0.05| ... |
| 001     | 2021 | Manuf    | USA     | 1100         | 550   | 55         | 0.05| ... |
| 002     | 2020 | Tech     | USA     | 2000         | 800   | 160        | 0.08| ... |
```

**Variable Naming Conventions**:
- Use descriptive names: `total_assets` not `at`
- Add units suffix: `sales_millions`, `market_cap_billions`
- Indicate transformations: `log_assets`, `winsor_roa`
- Lag indicators: `lag1_sales`, `lead1_performance`

**Variable Ordering**:
1. Identifiers: firm_id, gvkey, permno, cusip
2. Time: year, quarter, date
3. Firm characteristics: industry, country, firm_name
4. Dependent variables
5. Independent variables
6. Control variables
7. Instrumental variables (if any)

**Save Multiple Formats**:
```python
# Stata format (common in economics/finance)
df.to_stata('final_dataset.dta', write_index=False, version=117)

# CSV (universal)
df.to_csv('final_dataset.csv', index=False)

# Parquet (efficient for large datasets)
df.to_parquet('final_dataset.parquet', index=False, compression='gzip')

# Excel (for reviewers who prefer Excel)
df.to_excel('final_dataset.xlsx', index=False, sheet_name='Main')
```

#### B. Data Dictionary

**Required Information for Each Variable**:

| Variable | Description | Source | Unit | Construction | Notes |
|----------|-------------|--------|------|--------------|-------|
| gvkey | Compustat firm identifier | Compustat | - | Direct from source | Permanent identifier |
| year | Fiscal year | Compustat | Year | Direct from fyear | Not calendar year |
| total_assets | Total assets | Compustat | Millions USD | Compustat item: at | Winsorized at 1%/99% |
| roa | Return on assets | Computed | Ratio | net_income / total_assets | Winsorized at 1%/99% |
| log_assets | Natural log of total assets | Computed | Log(Millions) | ln(total_assets) | Proxy for firm size |
| rd_intensity | R&D intensity | Computed | Ratio | xrd / sales | Missing R&D set to 0 with indicator |

**Variable Classification**:
- **Identifiers**: gvkey, permno, cusip, firm_id
- **Time Variables**: year, quarter, date
- **Firm Characteristics**: industry, country, age, listing_year
- **Financial Variables**: total_assets, sales, net_income, cash, debt
- **Performance Variables**: roa, roe, tobins_q, market_to_book
- **Innovation Variables**: rd_expenditure, patent_count, citation_count
- **Governance Variables**: board_size, ceo_duality, institutional_ownership
- **ESG Variables**: environmental_score, social_score, governance_score

**Output**: Data dictionary in Excel or PDF format

#### C. Codebook & Replication Materials

**Codebook Contents**:
1. **Data Sources Section**:
   - List all databases used
   - Access dates
   - Database versions (if applicable)
   - Query scripts or manual download procedures

2. **Sample Selection Section**:
   - Population definition
   - Inclusion criteria with application order
   - Exclusion criteria with counts
   - Final sample composition

3. **Variable Construction Section**:
   - For each constructed variable:
     - Formula
     - Raw data items used
     - Transformations applied
     - Treatment of missing values

4. **Merging Procedures Section**:
   - Merge sequence (order matters!)
   - Identifiers used
   - Merge type (inner, left, outer)
   - Match rates
   - Treatment of unmatched observations

5. **Data Cleaning Section**:
   - Winsorization levels
   - Outlier treatment
   - Missing data imputation (if any)
   - Correction of data errors

**Replication Scripts**:
```
/replication/
├── 1_data_download/
│   ├── download_compustat.sas
│   ├── download_crsp.sas
│   └── download_patents.py
├── 2_data_cleaning/
│   ├── clean_financial_data.py
│   ├── construct_variables.py
│   └── handle_outliers.py
├── 3_data_merging/
│   ├── merge_compustat_crsp.py
│   ├── merge_patents.py
│   └── validate_merges.py
├── 4_quality_checks/
│   ├── qa_accounting_identities.py
│   ├── qa_temporal_consistency.py
│   └── generate_qa_report.py
└── README.md (explains execution order and dependencies)
```

**README Template**:
```markdown
# Replication Instructions for [Paper Title]

## System Requirements
- Python 3.8+
- Required packages: pandas, numpy, scipy, statsmodels (see requirements.txt)
- Access to WRDS (Compustat, CRSP) or equivalent data sources

## Data Access
1. Compustat: Requires WRDS subscription
2. PatentsView: Free bulk download from https://patentsview.org/download/data-download-tables
3. Macro data: World Bank API (no authentication required)

## Execution Steps
1. Run scripts in /1_data_download/ (may take 2-3 hours)
2. Run scripts in /2_data_cleaning/ (1 hour)
3. Run scripts in /3_data_merging/ (30 minutes)
4. Run scripts in /4_quality_checks/ (30 minutes)
5. Output: final_dataset.dta in /output/

## Expected Output
- Final dataset: 50,000 firm-year observations, 2000-2023
- Data dictionary: output/data_dictionary.xlsx
- Quality assurance report: output/QA_Report.pdf

## Troubleshooting
- If SAS scripts fail: Check WRDS username/password in config.ini
- If Python scripts fail: Verify all packages installed via `pip install -r requirements.txt`

## Contact
[Your name and email]
```

---

## Advanced Topics

### A. Handling Corporate Events

#### Mergers & Acquisitions

**Problem**: Firms may merge, be acquired, or split, complicating panel structure.

**Identification**:
1. Use SDC Platinum M&A database
2. Check CRSP delisting codes (dlstcd):
   - 200-399: Mergers
   - 400-490: Exchanges
   - 500-599: Liquidations

**Treatment Options**:
1. **Drop Involved Firms**: Conservative approach
   ```python
   # Drop firm-years around M&A event (e.g., ±1 year)
   ma_firms = ma_data['target_gvkey'].unique()
   df = df[~df['gvkey'].isin(ma_firms)]
   ```

2. **Create Combined Entity**: For large M&A
   ```python
   # Sum assets of acquirer and target pre-merger
   # Continue with acquirer ID post-merger
   ```

3. **Include with Indicator**: Control for M&A effects
   ```python
   df['ma_year'] = df['gvkey'].isin(ma_data['target_gvkey']).astype(int)
   ```

**Best Practice**: Document M&A treatment and conduct robustness checks excluding M&A years.

#### Spin-offs & Divestitures

**Problem**: Parent firm's financials change discontinuously.

**Identification**:
- CRSP delisting codes
- Compustat segment data (sudden loss of segments)
- SDC Platinum M&A database (divestitures)

**Treatment**:
- Adjust for pro-forma financials if available
- Use segment-level data when studying divisions
- Include indicator for divestiture year

#### Name Changes & Reincorporations

**Problem**: Firm changes legal name or reincorporates (e.g., from Delaware to Nevada).

**Identification**:
- CRSP: Name change history (COMNAM, NAMEDT, NAMEENDDT)
- Compustat: Generally preserves GVKEY

**Treatment**: Usually no action needed if using permanent identifiers (GVKEY, PERMCO).

### B. Cross-Country Research

**Additional Challenges**:
1. **Accounting Standards**:
   - US GAAP vs. IFRS vs. local GAAP
   - Use country-level controls
   - Standardize variables (e.g., sales-to-assets ratio less affected)

2. **Currency Conversions**:
   - Use consistent currency (USD or local)
   - Apply historical exchange rates from date of financial statement
   - Source: World Bank, IMF, or database native (e.g., Worldscope has USD-converted data)

3. **Institutional Differences**:
   - Legal systems (common law vs. civil law)
   - Corporate governance norms
   - Disclosure requirements
   - Include country fixed effects in models

4. **Data Quality Variation**:
   - Developed markets: high quality
   - Emerging markets: more missing data, less reliable
   - Document country-specific sample sizes

**Best Practices**:
```python
# Country-level controls
country_controls = ['gdp_per_capita', 'rule_of_law', 'disclosure_index']

# Include country fixed effects
model = 'y ~ x + controls + C(country) + C(year)'

# Cluster standard errors by country
results = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': df['country']})
```

### C. Dealing with Private Firms

**Data Sources**:
- Bureau van Dijk (Orbis): 400M+ private firms
- PrivCo: U.S. private companies
- National registries (e.g., Companies House in UK)

**Challenges**:
1. **Limited Financial Disclosure**: Many private firms disclose minimal data
2. **Data Quality**: Less standardized, more missing values
3. **Selection Bias**: Larger private firms more likely to disclose

**Analysis Strategies**:
1. **Separate Analysis**: Analyze private and public firms separately
2. **Propensity Score Matching**: Match private to similar public firms
3. **Acknowledge Limitations**: Be transparent about data constraints

---

## Integration with Statistical Analysis

### Preparing Data for Regression Analysis

**Panel Data Models**:

1. **Pooled OLS**: Ignores panel structure
```stata
reg y x1 x2 controls, robust
```

2. **Fixed Effects (FE)**: Controls for time-invariant unobserved heterogeneity
```stata
xtreg y x1 x2 controls, fe vce(cluster firm_id)
```

3. **Random Effects (RE)**: Assumes unobserved effects uncorrelated with regressors
```stata
xtreg y x1 x2 controls, re vce(cluster firm_id)
```

4. **Difference-in-Differences (DiD)**:
```stata
# Treatment indicator * Post-period indicator
reg y treatment##post controls i.firm_id i.year, vce(cluster firm_id)
```

**Standard Error Adjustments**:
- **Cluster by Firm**: Accounts for within-firm correlation
- **Cluster by Industry-Year**: Accounts for industry shocks
- **Two-Way Clustering**: Cluster by firm and year

**Data Preparation Checklist**:
- [ ] Winsorize continuous variables
- [ ] Create lagged independent variables (to address endogeneity)
- [ ] Generate interaction terms if needed
- [ ] Create indicator variables for categorical predictors
- [ ] Check for perfect multicollinearity
- [ ] Verify no missing values in regression sample (or handle explicitly)

---

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Ignoring Survival Bias
**Problem**: Using only currently existing firms overstates performance.
**Solution**: Include delisted/bankrupt firms using CRSP delisting data.

### Pitfall 2: Look-Ahead Bias
**Problem**: Using information not available at the time of decision.
**Example**: Using full-year earnings to predict Q1 stock returns.
**Solution**: Implement point-in-time data alignment with reporting lags.

### Pitfall 3: Incorrect Variable Scaling
**Problem**: Mixing thousands and millions, or not adjusting for inflation.
**Solution**: Standardize all currency units, adjust for inflation, document clearly.

### Pitfall 4: Restatement Issues
**Problem**: Historical data may be restated, changing values.
**Solution**: Use "as-reported" data if available, or note use of restated data.

### Pitfall 5: Ignoring Clustered Standard Errors
**Problem**: Understated standard errors due to within-cluster correlation.
**Solution**: Always cluster at appropriate level (usually firm).

### Pitfall 6: Overly Restrictive Sample Selection
**Problem**: Requiring complete data on all variables drops many observations.
**Solution**: Use pairwise deletion or multiple imputation when appropriate.

### Pitfall 7: Not Documenting Data Choices
**Problem**: Inability to replicate results or explain decisions to reviewers.
**Solution**: Maintain detailed logs, commented scripts, and decision justifications.

### Pitfall 8: Mixing Fiscal and Calendar Years
**Problem**: Temporal misalignment between variables.
**Solution**: Clearly define time alignment, document fiscal year calendars.

---

## Field-Specific Extensions

### Corporate Finance Research
**Key Variables**: Capital structure (leverage), dividend policy, investment (capex), cash holdings
**Common Models**: Fama-French factors, market model, Q-theory of investment
**Data**: Compustat, CRSP, I/B/E/S, SDC Platinum

### Strategic Management Research
**Key Variables**: Diversification (segment data), internationalization (geographic segments), innovation (patents, R&D)
**Common Models**: Resource-based view, dynamic capabilities, transaction cost economics
**Data**: Compustat Segments, Orbis, PatentsView, trade data

### Corporate Governance Research
**Key Variables**: Board composition, ownership structure, CEO compensation, shareholder activism
**Common Models**: Agency theory, stewardship theory
**Data**: ExecuComp, ISS, Thomson Reuters 13F, proxy statements

### ESG & Sustainability Research
**Key Variables**: Carbon emissions, ESG ratings, sustainability reports, CSR activities
**Common Models**: Stakeholder theory, legitimacy theory
**Data**: CDP, MSCI ESG, Sustainalytics, GRI database, newstext analysis

---

## Emerging Data Sources

### Alternative Data

1. **Text Data**:
   - **10-K/10-Q Filings**: Textual analysis of MD&A, risk factors
   - **Earnings Call Transcripts**: Tone, readability, forward-looking statements
   - **News Articles**: Sentiment analysis, media coverage
   - Tools: Python (NLTK, spaCy), LexisNexis, RavenPack

2. **Web Scraping**:
   - Company websites, Glassdoor reviews, LinkedIn employee data
   - ⚠️ Check Terms of Service, respect robots.txt

3. **Satellite Imagery**:
   - Parking lot activity (retail traffic), construction activity
   - Providers: Orbital Insight, RS Metrics

4. **Credit Card Transactions**:
   - Consumer spending patterns (aggregated, anonymized)
   - Providers: Envestnet Yodlee, Earnest Research

**Considerations**:
- Data quality and validation required
- Ethical and legal compliance
- Increasing use in recent research (cite: Gentzkow et al., 2019)

---

## Best Practices Summary

1. **Plan Comprehensively**: Data collection takes 30-50% of research time
2. **Start with Clear Hypotheses**: Drives sample selection and variable choices
3. **Test Early**: Download and inspect a small sample before full collection
4. **Document Everything**: Future collaborators (and reviewers) will thank you
5. **Version Control**: Use Git for scripts, document data versions
6. **Quality Over Quantity**: Better to have 10,000 high-quality observations than 100,000 suspect ones
7. **Validate Extensively**: Cross-check against original sources, plot time series
8. **Handle Missing Data Thoughtfully**: Distinguish "missing" from "zero" from "not applicable"
9. **Prepare for Revisions**: Structure scripts to easily update data or modify sample
10. **Share Responsibly**: Follow data provider terms, anonymize if required

---

## Templates & Resources

### Project Directory Structure
```
/project_name/
├── /data/
│   ├── /raw/                 # Original downloads (never modify)
│   ├── /processed/            # Cleaned data
│   └── /final/                # Analysis-ready datasets
├── /scripts/
│   ├── 1_download.py
│   ├── 2_clean.py
│   ├── 3_merge.py
│   └── 4_analysis.py
├── /output/
│   ├── /tables/
│   ├── /figures/
│   └── /logs/
├── /documentation/
│   ├── data_dictionary.xlsx
│   ├── codebook.pdf
│   └── QA_report.pdf
├── README.md
├── requirements.txt           # Python package versions
└── .gitignore                 # Don't commit large data files
```

### Data Collection Checklist
- [ ] Research question clearly defined
- [ ] Variables and sample scope identified
- [ ] Data sources evaluated and selected
- [ ] Access credentials obtained
- [ ] Sample selection criteria documented
- [ ] Data extraction scripts written and tested
- [ ] Raw data downloaded and backed up
- [ ] Data cleaning procedures documented
- [ ] Variables constructed and verified
- [ ] Multi-source merges completed and validated
- [ ] Quality checks performed
- [ ] Outliers addressed
- [ ] Missing data patterns analyzed
- [ ] Industry classification standardized
- [ ] Time alignment verified
- [ ] Final dataset created
- [ ] Data dictionary completed
- [ ] Codebook written
- [ ] Replication scripts organized
- [ ] All outputs backed up (3-2-1 rule)

---

## Troubleshooting Guide

### Issue: WRDS Query Timeout
**Symptom**: SAS query exceeds time limit.
**Solution**:
- Break query into smaller chunks (by year or industry)
- Use more restrictive WHERE clauses
- Download full table and filter locally

### Issue: Merge Produces Duplicates
**Symptom**: Record count after merge exceeds expectations.
**Solution**:
- Check for non-unique keys using `df.duplicated(['firm_id', 'year']).sum()`
- Investigate source: one-to-many or many-to-many relationship
- Aggregate one side to create one-to-one relationship

### Issue: Variables Have Unexpected Values
**Symptom**: ROA = 500 or Sales = -1 billion.
**Solution**:
- Check data dictionary for special codes (e.g., -9999 = missing)
- Verify currency units (thousands vs. millions)
- Inspect raw data from source

### Issue: Low Match Rates Between Databases
**Symptom**: Only 30% of firms matched between Compustat and patent data.
**Solution**:
- Use broader matching (CUSIP6 instead of exact name)
- Check temporal overlap (do databases cover same years?)
- Accept low match rate if expected (not all firms patent)

### Issue: Results Change with Sample Restrictions
**Symptom**: Coefficients flip sign when changing sample.
**Solution**:
- Natural if sample characteristics differ
- Report multiple specifications
- Investigate which restrictions drive changes

---

## Version History

**v2.0** (2025-10-31)
- **Major enhancements**: Advanced quality assurance module, research checklist, data lineage tracker
- **New features**: Statistical power analysis, pytest test suite, Docker support
- **Expanded coverage**: Comprehensive free data sources for 11 Asian countries
- **Improved documentation**: Detailed tutorials, sample projects, quick start guide

**v1.0** (Initial release)
- Comprehensive corporate research data collection workflow
- Integration of financial, market, governance, innovation, and ESG data
- Specialized procedures for panel data construction
- Multi-source integration strategies
- Survival bias and corporate event handling
- Cross-country research guidance
- Field-specific extensions
- Replication materials guidance

---

## Citation

If this skill significantly aids your research, consider acknowledging it:

```
Data collection and quality assurance procedures followed systematic protocols 
for corporate empirical research (corporate-research-data-hub skill v2.0), 
ensuring reproducibility and data integrity throughout the research process.
```

---

## License & Terms of Use

This skill is a tool for research planning and execution. Researchers remain responsible for:
1. Complying with all data provider terms of service
2. Obtaining necessary institutional approvals (IRB, data agreements)
3. Properly citing data sources in publications
4. Ensuring ethical use of data
5. Verifying data accuracy and appropriateness for their research

---

**Ready to begin?** 

Simply describe your research question, and I will guide you through:
1. Defining data requirements (Phase 1)
2. Identifying optimal data sources (Phase 2)
3. Designing collection strategy (Phase 3)
4. Cleaning and standardizing data (Phase 4)
5. Integrating multiple sources (Phase 5)
6. Performing quality assurance (Phase 6)
7. Creating publication-ready dataset (Phase 7)

Example starting prompts:
- "I'm studying the relationship between board diversity and firm innovation in U.S. tech companies."
- "I need to collect ESG data for European manufacturing firms, 2010-2023."
- "Help me construct a panel dataset merging Compustat financials with patent data."
- "What free data sources are available for Korean and Japanese manufacturing companies?"
- "I'm on a zero budget - how can I collect data for Asian corporate governance research?"

---

## Quick Reference: Additional Resources

### For Beginners
- **Start here**: [QUICKSTART.md](QUICKSTART.md) - Get your first dataset in 15 minutes
- **Templates**: [templates/](templates/) - Data collection plans and checklists

### Free Data Sources
- **Complete guide**: [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)
  - 70+ free data sources
  - 11 Asian countries/regions covered
  - API access guides
  - Zero-cost research examples

### Practical Tools
- **Python scripts**: [scripts/](scripts/)
  - `asian_data_collectors.py` - Data collection for Japan, Korea, China, Taiwan
  - `corporate_data_utils.py` - Data processing utilities
  - `data_quality_checker.py` - Automated quality assurance
- **Sample project**: [templates/sample_project_asian_roa.md](templates/sample_project_asian_roa.md)
  - Complete workflow example
  - Zero-budget research
  - Reproducible code

### Common Tasks
- **Free data for Asian research** → [FREE_LOW_COST_DATA_SOURCES.md](FREE_LOW_COST_DATA_SOURCES.md)
- **Panel data construction** → Phase 3 & 4 in this document
- **Quality checks** → Phase 6 + [scripts/data_quality_checker.py](scripts/data_quality_checker.py)
- **Multi-country research** → Section 8.4 + FREE_LOW_COST_DATA_SOURCES.md
