# Economics Research Example: Trade Policy and Economic Growth

**Research Topic**: Impact of Trade Liberalization on Economic Growth in East Asian Countries  
**Field**: International Economics, Development Economics  
**Researcher**: [Sample Project]  
**Date**: 2025-10-31

---

## Project Overview

### Research Question
Does trade liberalization lead to higher economic growth rates in East Asian countries, and does this relationship vary by country income level and institutional quality?

### Hypotheses
1. **H1**: Countries with greater trade openness experience higher GDP growth rates
2. **H2**: The positive effect of trade openness is stronger in countries with better institutional quality
3. **H3**: The trade-growth relationship exhibits diminishing returns at very high levels of openness

---

## Phase 1: Research Requirements Analysis

### Data Requirements

**Temporal Scope**: 1990-2023 (34 years)  
**Geographic Scope**: 15 East Asian countries  
- High income: Japan, South Korea, Singapore, Hong Kong, Taiwan
- Upper-middle income: China, Malaysia, Thailand
- Lower-middle income: Indonesia, Philippines, Vietnam, Cambodia, Laos, Myanmar
- Low income: Timor-Leste

**Required Variables**:

1. **Dependent Variable**:
   - GDP growth rate (annual %)

2. **Key Independent Variables**:
   - Trade openness: (Exports + Imports) / GDP
   - Tariff rates
   - Trade policy index

3. **Control Variables**:
   - Population growth
   - Gross capital formation (% of GDP)
   - Government expenditure (% of GDP)
   - Inflation rate
   - Foreign direct investment (FDI) net inflows
   - Human capital index
   - Institutional quality index

4. **Moderating Variables**:
   - Governance indicators (rule of law, regulatory quality)
   - Income group classification

**Data Frequency**: Annual  
**Panel Structure**: Balanced panel (15 countries × 34 years = 510 country-year observations)

---

## Phase 2: Data Source Discovery

### Primary Data Sources Identified

#### 1. World Bank World Development Indicators (WDI)
- **URL**: https://data.worldbank.org/
- **Variables Available**:
  - GDP growth (annual %)
  - Trade (% of GDP)
  - Gross capital formation
  - Population growth
  - Government expenditure
  - Inflation, consumer prices
  - FDI, net inflows
- **Coverage**: All 15 countries, 1990-2023
- **Access**: Free, API available
- **API Endpoint**: `https://api.worldbank.org/v2/country/{code}/indicator/{indicator}`
- **Quality**: ★★★★★ (5/5) - Most reliable source for economic indicators
- **Update Frequency**: Annual, released with ~6-month lag

#### 2. World Trade Organization (WTO) Statistics
- **URL**: https://data.wto.org/
- **Variables Available**:
  - Applied tariff rates (MFN average)
  - Preferential tariff rates
- **Coverage**: WTO members (13/15 countries)
- **Access**: Free, bulk download available
- **Quality**: ★★★★☆ (4/5) - Official trade data but some missing values
- **Limitation**: Myanmar and Timor-Leste not WTO members during full period

#### 3. Penn World Table (PWT 10.01)
- **URL**: https://www.rug.nl/ggdc/productivity/pwt/
- **Variables Available**:
  - Human capital index
  - Real GDP (alternative measure)
  - Capital stock data
- **Coverage**: Most countries, 1950-2019
- **Access**: Free download (Excel/Stata/CSV)
- **Quality**: ★★★★★ (5/5) - Gold standard for cross-country comparisons
- **Limitation**: Ends in 2019, missing recent years

#### 4. World Bank Worldwide Governance Indicators (WGI)
- **URL**: https://www.worldbank.org/en/publication/worldwide-governance-indicators
- **Variables Available**:
  - Rule of law
  - Regulatory quality
  - Government effectiveness
  - Control of corruption
- **Coverage**: All countries, 1996-2022
- **Access**: Free, Excel download
- **Quality**: ★★★★☆ (4/5) - Widely used but subjective measures
- **Limitation**: Not available before 1996

#### 5. IMF International Financial Statistics (IFS)
- **URL**: https://data.imf.org/
- **Variables Available**:
  - Exchange rates
  - Balance of payments data
  - Alternative GDP data
- **Coverage**: IMF member countries
- **Access**: Free basic access, paid for full dataset
- **Quality**: ★★★★★ (5/5)
- **Note**: Use as backup for validation

### Data Source Selection Decision

**Primary**: World Bank WDI (comprehensive coverage, easy access)  
**Secondary**: WTO (tariff data), Penn World Table (human capital), WGI (institutional quality)  
**Tertiary**: IMF IFS (validation purposes)

**Rationale**:
- WDI covers 90% of required variables
- All sources are free and publicly accessible
- API availability enables automated collection
- Sources are well-documented and widely cited in economics literature

---

## Phase 3: Collection Strategy and Plan

### Collection Approach: Hybrid (Automated + Manual)

#### Automated Collection (75% of data)
**Tool**: Python with `wbdata` library for World Bank API

**Workflow**:
1. Define country list (ISO codes)
2. Define indicator codes
3. Loop through countries and indicators
4. API calls with error handling
5. Store in pandas DataFrame
6. Export to CSV

**Script**: `scripts/collect_wb_data.py`

**Estimated Time**: 2 hours (including script development and testing)

#### Manual Collection (25% of data)
**Sources**: Penn World Table, WGI

**Workflow**:
1. Download Excel files from websites
2. Extract relevant sheets
3. Filter to East Asian countries
4. Standardize column names
5. Merge into main dataset

**Estimated Time**: 3 hours

### Detailed Collection Plan

**Week 1: Setup and World Bank Data**
- Day 1: Set up Python environment, install libraries
- Day 2: Develop collection script for WDI
- Day 3: Run collection, validate output
- Day 4: Handle missing values, document issues
- Day 5: Initial exploratory data analysis

**Week 2: Supplementary Data**
- Day 1-2: Collect WTO tariff data
- Day 3: Download and process Penn World Table
- Day 4: Download and process WGI data
- Day 5: Merge all datasets

**Week 3: Quality Assurance**
- Day 1-2: Run quality checks (see Phase 4)
- Day 3: Cross-validate with IMF data for key countries
- Day 4: Address discrepancies
- Day 5: Finalize dataset, create data dictionary

**Total Time Budget**: 15 working days

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| API rate limits | Medium | Medium | Implement delays, retry logic |
| Missing data for small economies | High | Medium | Accept missing values, document in limitations |
| WGI data not available pre-1996 | Certain | High | Use sub-sample analysis (1996-2023) or find alternative indicators |
| Tariff data gaps | Medium | Low | Use regional averages for missing countries |
| Data revision by source | Low | Medium | Document collection date, version numbers |

---

## Phase 4: Quality Assurance

### Automated Quality Checks

**Script**: `scripts/quality_checker.py`

**Checks Implemented**:
1. **Completeness**: 
   - Missing value rate per variable < 10%
   - Complete coverage for all countries (at least 80% of years)

2. **Range Validation**:
   - GDP growth: -20% to 20% (flag outliers beyond)
   - Trade openness: 0% to 400% (some small economies exceed 200%)
   - Inflation: -5% to 50%

3. **Time-Series Consistency**:
   - No sudden jumps > 50% year-over-year (except crisis years)
   - Smooth trajectories for structural variables (population, human capital)

4. **Cross-Validation**:
   - Compare WDI GDP data with Penn World Table (correlation > 0.95 expected)
   - Check trade data consistency: Exports + Imports should match trade openness

### Quality Report Summary

**Completeness**:
- GDP growth: 100% coverage ✓
- Trade openness: 98% coverage (missing: Timor-Leste 1990-2001)
- Tariff rates: 87% coverage (missing: Myanmar 1990-1997, Timor-Leste 1990-2002)
- Human capital: 97% coverage (missing: 2020-2023 for all countries)
- Governance indicators: 79% coverage (not available pre-1996)

**Overall Quality Score**: 88/100 (Good - Suitable for analysis with documented limitations)

**Key Issues Identified**:
1. Human capital index ends in 2019 - use last available value for 2020-2023
2. Governance data not available before 1996 - run separate analysis for 1996-2023 subsample
3. Timor-Leste has extensive missing data - consider excluding from balanced panel

**Resolution**:
- Main analysis: 1990-2023, all 15 countries (510 observations)
- Robustness check 1: 1996-2023, all 15 countries (420 observations) with governance variables
- Robustness check 2: 1990-2023, excluding Timor-Leste (476 observations)

---

## Phase 5: Data Integration and Preparation

### Data Merging Strategy

**Merge Key**: Country ISO code + Year

**Steps**:
1. Load WDI data (primary dataset)
2. Left join WTO tariff data on (country, year)
3. Left join Penn World Table on (country, year)
4. Left join WGI data on (country, year)

**Script**: `scripts/merge_datasets.py`

### Variable Transformations

```python
# Trade openness (already in WDI as % of GDP)
df['trade_openness'] = df['trade_pct_gdp']

# Log transformations for non-linear relationships
df['log_gdp_per_capita'] = np.log(df['gdp_per_capita'])

# Lagged variables for growth models
df['trade_openness_lag1'] = df.groupby('country_code')['trade_openness'].shift(1)

# Interaction terms
df['trade_x_institution'] = df['trade_openness'] * df['rule_of_law']

# Income group dummies
df = pd.get_dummies(df, columns=['income_group'], drop_first=True)

# Crisis dummy (Asian Financial Crisis 1997-1998)
df['crisis_1997'] = ((df['year'] == 1997) | (df['year'] == 1998)).astype(int)
```

### Final Dataset Structure

**Dimensions**: 510 rows × 45 columns  
**Unit of Analysis**: Country-year  
**Format**: Panel data (long format)  
**File**: `data/final/east_asia_trade_growth_1990_2023.csv`

---

## Phase 6: Documentation

### Data Dictionary
[View complete dictionary: `data/data_dictionary.csv`]

**Key Variables Summary**:

| Variable | Description | Source | Years | Missing |
|----------|-------------|--------|-------|---------|
| gdp_growth | Annual GDP growth rate (%) | WDI | 1990-2023 | 0% |
| trade_openness | (Exports+Imports)/GDP (%) | WDI | 1990-2023 | 2% |
| tariff_rate | MFN applied tariff rate (%) | WTO | 1990-2023 | 13% |
| human_capital | Human capital index | PWT | 1990-2019 | 3% |
| rule_of_law | Governance indicator (-2.5 to 2.5) | WGI | 1996-2022 | 21% |

### Methods Section (For Paper)

```
We constructed a panel dataset covering 15 East Asian countries from 1990 to 2023,
yielding 510 country-year observations. Data were collected from four primary sources:
World Bank World Development Indicators (economic variables), World Trade Organization
Statistics (tariff data), Penn World Table 10.01 (human capital), and World Bank
Worldwide Governance Indicators (institutional quality).

Our main dependent variable, GDP growth rate, is sourced from the World Bank WDI.
Trade openness is measured as the sum of exports and imports as a percentage of GDP.
We control for population growth, capital formation, government spending, inflation,
and FDI inflows. Human capital is measured using the Penn World Table index.
Institutional quality is proxied by the World Bank's "rule of law" indicator,
available from 1996 onward.

Data were collected via API using Python (primary) and manual download (supplementary).
Missing values occur primarily in governance indicators before 1996 (21% missing) and
human capital after 2019 (3% missing due to PWT publication lag). We address this
through subsample analysis and robustness checks.

All data are publicly available and replication files are provided at [repository URL].
```

### Replication Package Contents

```
replication_package/
├── data/
│   ├── raw/
│   │   ├── wdi_raw.csv
│   │   ├── wto_tariffs.xlsx
│   │   ├── pwt1001.xlsx
│   │   └── wgi_data.xlsx
│   ├── processed/
│   │   └── east_asia_trade_growth_1990_2023.csv
│   └── data_dictionary.csv
├── scripts/
│   ├── 01_collect_wb_data.py
│   ├── 02_process_supplementary.py
│   ├── 03_merge_datasets.py
│   ├── 04_quality_checks.py
│   └── 05_descriptive_stats.R
├── output/
│   ├── descriptive_statistics.xlsx
│   ├── quality_report.pdf
│   └── correlation_matrix.png
├── documentation/
│   ├── codebook.pdf
│   ├── collection_log.md
│   └── data_sources_citation.bib
└── README.md
```

---

## Results Preview: Descriptive Statistics

### Sample Composition

**By Income Group (2023)**:
- High income: 5 countries (33%)
- Upper-middle income: 3 countries (20%)
- Lower-middle income: 6 countries (40%)
- Low income: 1 country (7%)

### Key Variable Statistics (1990-2023)

| Variable | Mean | SD | Min | Max | N |
|----------|------|----|----|-----|---|
| GDP growth (%) | 5.2 | 4.8 | -13.1 | 18.3 | 510 |
| Trade openness (%) | 92.4 | 75.3 | 18.2 | 437.3 | 500 |
| Tariff rate (%) | 8.4 | 6.2 | 0.0 | 35.6 | 444 |
| Human capital | 2.4 | 0.5 | 1.3 | 3.7 | 495 |
| Rule of law | 0.2 | 0.8 | -1.5 | 1.9 | 405 |

**Notable Patterns**:
- High heterogeneity in trade openness (SD = 75.3) due to small open economies (Singapore, Hong Kong)
- Average GDP growth higher in East Asia (5.2%) than global average (2.8%)
- Significant improvement in human capital over time (1990: 1.8 → 2023: 3.1)

---

## Lessons Learned

### What Worked Well
1. **API automation**: Saved 10+ hours compared to manual download
2. **Early quality checks**: Caught data entry errors before analysis
3. **Comprehensive documentation**: Made dataset reusable for future projects

### Challenges Faced
1. **Governance data gap**: Pre-1996 data not available - required subsample analysis
2. **Small economy outliers**: Singapore and Hong Kong trade openness > 300% - needed careful handling
3. **Source discrepancies**: WDI vs. Penn World Table GDP figures differ by up to 5% for some countries

### Recommendations for Similar Projects
1. Start with data discovery phase early (some sources have access delays)
2. Build in 20-30% time buffer for unexpected issues
3. Use version control (Git) for datasets - sources update historical data
4. Create automated quality checks from day 1
5. Document data collection decisions in real-time (not retrospectively)

---

## Timeline: Actual vs. Planned

| Phase | Planned | Actual | Variance |
|-------|---------|--------|----------|
| Phase 1: Requirements | 2 days | 2 days | 0% |
| Phase 2: Discovery | 3 days | 4 days | +33% |
| Phase 3: Collection | 10 days | 12 days | +20% |
| Phase 4: QA | 3 days | 4 days | +33% |
| Phase 5: Integration | 2 days | 2 days | 0% |
| Phase 6: Documentation | 2 days | 3 days | +50% |
| **Total** | **22 days** | **27 days** | **+23%** |

**Key Delays**:
- Discovering governance data limitation (+ 1 day)
- API rate limiting issues (+ 1 day)
- Additional validation for outliers (+ 2 days)
- More comprehensive documentation needed (+ 1 day)

---

## Next Steps: From Data Collection to Analysis

1. **Exploratory Data Analysis**:
   - Plot time-series trends for key variables
   - Create correlation matrices
   - Identify potential endogeneity issues

2. **Econometric Modeling**:
   - Fixed effects panel regression
   - Instrumental variables (if endogeneity detected)
   - Robustness checks with different specifications

3. **Visualization**:
   - Scatter plots: trade openness vs. GDP growth
   - Maps: trade openness by country and year
   - Time-series: trends before/after trade reforms

4. **Paper Writing**:
   - Use methods template from this skill
   - Prepare tables and figures
   - Write results and discussion sections

---

**Project Status**: ✅ Data Collection Complete  
**Dataset Ready for Analysis**: Yes  
**Quality Score**: 88/100  
**Time Investment**: 27 person-days  
**Next Milestone**: Complete econometric analysis by [DATE]

---

## References

World Bank. (2024). *World Development Indicators*. Retrieved from https://databank.worldbank.org/source/world-development-indicators. Accessed October 31, 2025.

World Trade Organization. (2024). *WTO Statistics Database*. Retrieved from https://data.wto.org/. Accessed October 31, 2025.

Feenstra, R. C., Inklaar, R., & Timmer, M. P. (2024). *Penn World Table version 10.01*. Retrieved from https://www.rug.nl/ggdc/productivity/pwt/. Accessed October 31, 2025.

Kaufmann, D., Kraay, A., & Mastruzzi, M. (2023). *The Worldwide Governance Indicators: Methodology and Analytical Issues*. World Bank Policy Research Working Paper.

---

**Example Version**: 1.0  
**Last Updated**: 2025-10-31  
**Field**: Economics (International Trade, Development)  
**Skill**: Research Data Collection v1.0
