# Example Research Project: R&D Investment and Performance in Japanese Manufacturing Firms

## Research Question

**Does R&D investment improve financial performance in Japanese manufacturing firms, and is this relationship moderated by firm size and industry dynamism?**

---

## 1. Executive Summary

This example demonstrates a complete empirical research project examining the relationship between R&D intensity and firm performance (ROA) in Japanese publicly traded manufacturing firms from 2010 to 2023. The study tests hypotheses derived from the Resource-Based View and Dynamic Capabilities perspectives, using panel data analysis with firm fixed effects. Results show a positive and significant relationship between R&D intensity and ROA, which is stronger for larger firms and in more dynamic industries.

**Key Findings**:
- R&D intensity increases ROA by approximately 0.15 percentage points for each 1% increase in R&D/Sales ratio
- The effect is 50% stronger in large firms (top quartile by assets)
- The effect is 30% weaker in stable industries (low technological change)

---

## 2. Theoretical Framework

### 2.1 Literature Review

**Resource-Based View (RBV)**:
- Barney (1991) argues that firm resources that are Valuable, Rare, Inimitable, and Non-substitutable (VRIN) lead to sustained competitive advantage
- R&D creates knowledge resources that are difficult to imitate
- R&D-intensive firms should outperform competitors

**Dynamic Capabilities**:
- Teece, Pisano, & Shuen (1997) emphasize the ability to integrate, build, and reconfigure internal and external competences
- R&D investments build dynamic capabilities for innovation
- Particularly important in rapidly changing environments

**Japan-Specific Context**:
- Japanese firms historically emphasize long-term R&D investment (Odagiri & Goto, 1996)
- Keiretsu system facilitates patient capital for R&D (Hoshi, Kashyap, & Scharfstein, 1991)
- However, "lost decades" (1990s-2000s) raised questions about R&D effectiveness

### 2.2 Hypotheses

**H1**: R&D intensity is positively associated with firm financial performance (ROA).

*Theoretical reasoning*: Following RBV, firms that invest more in R&D develop valuable knowledge resources that competitors cannot easily replicate. These resources enable product differentiation, process improvements, and new market entry, all of which enhance profitability.

**H2**: The positive relationship between R&D intensity and firm performance is stronger for larger firms.

*Theoretical reasoning*: Larger firms possess complementary assets (marketing channels, production scale, financial resources) that enable them to better exploit R&D outputs. Small firms may generate innovations but lack resources to commercialize them effectively (Cohen & Klepper, 1996).

**H3**: The positive relationship between R&D intensity and firm performance is stronger in dynamic industries (high technological change).

*Theoretical reasoning*: Dynamic Capabilities theory suggests that R&D investments are particularly valuable in turbulent environments where firms must continuously adapt. In stable industries, existing capabilities suffice, reducing the marginal value of new R&D (Teece et al., 1997).

---

## 3. Research Design

### 3.1 Sample

- **Population**: Japanese manufacturing firms (SIC codes 20-39) listed on Tokyo Stock Exchange
- **Time Period**: 2010-2023 (14 years)
- **Initial Sample**: 1,850 firms
- **Final Sample**: 12,450 firm-year observations (after data cleaning)
  - Dropped firms with <3 years of data
  - Dropped firm-years with extreme outliers (>5σ)
  - Required non-missing values for all key variables

### 3.2 Data Sources

| Variable Type | Data Source | Access Method | Cost |
|--------------|-------------|---------------|------|
| Financial Data | EDINET (金融庁開示書類) | Free API | Free |
| Patent Data | USPTO PatentsView | Free API | Free |
| Industry Classification | EDINET | Free | Free |
| Macroeconomic Data | World Bank / OECD | Free API | Free |

**Note**: This entire study uses FREE data sources, demonstrating feasibility of zero-budget research.

---

## 4. Variables and Measurement

### 4.1 Dependent Variable

**ROA (Return on Assets)**:
```
ROA = (Net Income / Total Assets) × 100
```
- Source: EDINET 有価証券報告書
- Winsorized at 1% and 99% percentiles
- Mean: 5.2%, Std Dev: 4.8%, Range: [-10%, 20%]

### 4.2 Independent Variables

**R&D Intensity**:
```
RD_Intensity = (R&D Expenditure / Sales) × 100
```
- Source: EDINET 有価証券報告書 (研究開発費)
- Lagged by 1 year (t-1) to establish temporal precedence
- Missing R&D treated as zero (common in Japanese firms; non-tech firms often don't report)
- Created indicator variable: RD_Missing (1 if R&D not reported, 0 otherwise)
- Winsorized at 1% and 99%
- Mean: 3.2%, Std Dev: 2.8%, Range: [0%, 15%]

**Firm Size (FIRM_SIZE)**:
```
FIRM_SIZE = log(Total Assets in millions of yen)
```
- Source: EDINET
- Natural logarithm to reduce skewness
- Mean: 11.5 (log), Std Dev: 1.8

**Industry Dynamism (IND_DYNAMISM)**:
```
IND_DYNAMISM = Standard deviation of industry sales growth (3-digit SIC, 5-year rolling window)
```
- Calculated from EDINET data aggregated by industry
- Higher values = more dynamic/turbulent industry
- Mean: 0.15, Std Dev: 0.08

### 4.3 Control Variables

1. **Firm Age**: Years since founding
   - Source: EDINET corporate information
   - Mean: 55 years, Std Dev: 30 years

2. **Leverage**: Total Debt / Total Assets
   - Source: EDINET
   - Winsorized at 1% and 99%
   - Mean: 0.35, Std Dev: 0.18

3. **Sales Growth**: (Sales_t - Sales_t-1) / Sales_t-1
   - Source: EDINET
   - Winsorized at 1% and 99%
   - Mean: 0.03, Std Dev: 0.12

4. **Patent Stock**: log(1 + Cumulative patents over past 5 years)
   - Source: USPTO PatentsView (Japanese firms filing in US)
   - Mean: 2.1 (log), Std Dev: 2.5

5. **Industry Fixed Effects**: 2-digit SIC codes (21 industries)

6. **Year Fixed Effects**: 14 year dummies (2010-2023)

---

## 5. Analytical Approach

### 5.1 Main Model

**Panel Data Regression with Firm Fixed Effects**:

```
ROA_it = β0 + β1·RD_Intensity_i(t-1) + β2·FIRM_SIZE_it + β3·LEVERAGE_it 
         + β4·FIRM_AGE_it + β5·SALES_GROWTH_it + β6·PATENT_STOCK_it 
         + αi + δt + εit
```

Where:
- αi = Firm fixed effects (controls for time-invariant unobserved heterogeneity)
- δt = Year fixed effects (controls for macroeconomic trends)
- εit = Error term (clustered at firm level for robust standard errors)

**Why Fixed Effects?**
- Addresses endogeneity from unobserved firm heterogeneity (e.g., management quality, corporate culture)
- Within-firm estimation: Examines how changes in R&D within the same firm affect performance
- Hausman test confirms FE > RE (χ² = 45.6, p < 0.001)

### 5.2 Moderation Models

**Firm Size Moderation (H2)**:
```
ROA_it = β0 + β1·RD_Intensity_i(t-1) + β2·FIRM_SIZE_it 
         + β3·(RD_Intensity × FIRM_SIZE)_i(t-1) 
         + Controls + αi + δt + εit
```

**Industry Dynamism Moderation (H3)**:
```
ROA_it = β0 + β1·RD_Intensity_i(t-1) + β2·IND_DYNAMISM_jt 
         + β3·(RD_Intensity × IND_DYNAMISM)_i(t-1) 
         + Controls + αi + δt + εit
```

### 5.3 Estimation Details

- Software: Python 3.10 with `linearmodels` package
- Standard Errors: Clustered at firm level
- Multicollinearity: All VIF < 3 (acceptable)
- Heteroskedasticity: Robust standard errors address potential heteroskedasticity
- Serial Correlation: Firm fixed effects and clustering mitigate concerns

---

## 6. Results

### 6.1 Descriptive Statistics

| Variable | N | Mean | Std Dev | Min | P25 | Median | P75 | Max |
|----------|---|------|---------|-----|-----|--------|-----|-----|
| ROA (%) | 12,450 | 5.2 | 4.8 | -10.0 | 2.1 | 5.0 | 8.5 | 20.0 |
| RD_Intensity (%) | 12,450 | 3.2 | 2.8 | 0.0 | 0.8 | 2.5 | 4.8 | 15.0 |
| Firm Size (log) | 12,450 | 11.5 | 1.8 | 7.2 | 10.3 | 11.4 | 12.8 | 16.5 |
| Leverage | 12,450 | 0.35 | 0.18 | 0.0 | 0.21 | 0.33 | 0.48 | 0.80 |
| Firm Age (years) | 12,450 | 55 | 30 | 10 | 32 | 48 | 75 | 150 |

### 6.2 Correlation Matrix

|  | ROA | RD_Int | Size | Leverage | Age |
|--|-----|--------|------|----------|-----|
| ROA | 1.000 |  |  |  |  |
| RD_Intensity | 0.145*** | 1.000 |  |  |  |
| Firm Size | 0.234*** | 0.089** | 1.000 |  |  |
| Leverage | -0.187*** | -0.056* | 0.123*** | 1.000 |  |
| Firm Age | -0.045 | -0.012 | 0.267*** | 0.089** | 1.000 |

*Note*: *** p<0.01, ** p<0.05, * p<0.10

### 6.3 Regression Results

#### Table 1: Main Effects and Moderation

| Variable | Model 1 (Pooled OLS) | Model 2 (FE) | Model 3 (FE + Size) | Model 4 (FE + Dynamism) |
|----------|---------------------|--------------|---------------------|------------------------|
| **RD_Intensity (t-1)** | 0.145*** | 0.152*** | 0.089** | 0.121*** |
|  | (0.032) | (0.038) | (0.041) | (0.040) |
| **RD × Firm Size** |  |  | 0.045** |  |
|  |  |  | (0.018) |  |
| **RD × Ind Dynamism** |  |  |  | -0.082* |
|  |  |  |  | (0.043) |
| **Firm Size** | 0.234*** | 0.198*** | 0.175*** | 0.196*** |
|  | (0.045) | (0.052) | (0.054) | (0.052) |
| **Leverage** | -0.187*** | -0.165** | -0.162** | -0.164** |
|  | (0.056) | (0.064) | (0.064) | (0.064) |
| **Firm Age** | -0.012 | — | — | — |
|  | (0.015) |  |  |  |
| **Sales Growth** | 0.089** | 0.095** | 0.094** | 0.095** |
|  | (0.038) | (0.042) | (0.042) | (0.042) |
|  |  |  |  |  |
| **Industry FE** | Yes | — | — | — |
| **Year FE** | Yes | Yes | Yes | Yes |
| **Firm FE** | No | Yes | Yes | Yes |
|  |  |  |  |  |
| **N** | 12,450 | 12,450 | 12,450 | 12,450 |
| **R-squared** | 0.312 | 0.487 | 0.492 | 0.489 |
| **Adj R-squared** | 0.309 | 0.481 | 0.486 | 0.483 |
| **F-statistic** | 156.3*** | 203.5*** | 198.7*** | 201.2*** |

*Notes*: Standard errors in parentheses, clustered at firm level. *** p<0.01, ** p<0.05, * p<0.10.
Firm Age is time-invariant and absorbed by firm fixed effects in Models 2-4.

### 6.4 Interpretation

**H1 (R&D → Performance): SUPPORTED**
- Coefficient: β = 0.152, p < 0.01 (Model 2)
- Interpretation: A 1 percentage point increase in R&D intensity (e.g., from 3% to 4% of sales) is associated with a 0.152 percentage point increase in ROA (e.g., from 5.0% to 5.152%)
- Economic significance: For a firm with ¥100 billion in assets, this translates to ¥152 million additional net income

**H2 (Size Moderation): SUPPORTED**
- Interaction coefficient: β = 0.045, p < 0.05 (Model 3)
- Interpretation: The positive effect of R&D on ROA is stronger for larger firms
- Example: 
  - Small firm (10th percentile size, log assets = 9.5): Effect of RD = 0.089 + 0.045×9.5 = 0.52%
  - Large firm (90th percentile size, log assets = 13.5): Effect of RD = 0.089 + 0.045×13.5 = 0.70%
  - Difference: 35% stronger effect in large firms

**H3 (Dynamism Moderation): PARTIALLY SUPPORTED (opposite direction)**
- Interaction coefficient: β = -0.082, p < 0.10 (Model 4)
- **Unexpected result**: R&D effect is WEAKER (not stronger) in dynamic industries
- Possible explanation: In highly turbulent Japanese industries (e.g., consumer electronics), R&D investments face higher obsolescence risk. Stable industries (e.g., chemicals, materials) allow longer R&D payoff horizons.
- This contradicts Dynamic Capabilities theory but aligns with "Red Queen" effect (Barnett & Hansen, 1996): In very competitive environments, R&D is necessary just to survive, not to excel

---

## 7. Robustness Checks

### 7.1 Alternative Dependent Variables

| DV | Coefficient on RD | p-value | N |
|----|-------------------|---------|---|
| ROE (%) | 0.189** | 0.032 | 12,450 |
| Tobin's Q | 0.067* | 0.078 | 11,234 |
| ROS (%) | 0.134** | 0.041 | 12,450 |

*Note*: All models include firm FE, year FE, and controls. Results consistent with main findings.

### 7.2 Subsample Analysis

**By Firm Size**:
- Small firms (bottom quartile): β = 0.089, p = 0.124 (NOT significant)
- Large firms (top quartile): β = 0.187***, p < 0.001 (SIGNIFICANT)
- Confirms H2: R&D more effective in large firms

**By Industry**:
- High-Tech (Electronics, Precision): β = 0.178***, p < 0.001
- Low-Tech (Food, Textiles): β = 0.112**, p = 0.018
- Both significant, but effect 60% stronger in high-tech

### 7.3 Addressing Endogeneity

**Instrumental Variable Approach**:
- Instrument: Industry-average R&D intensity (excludes focal firm)
- Rationale: Industry norms affect individual firm R&D but don't directly affect firm performance
- First-stage F-statistic: 324.5 (strong instrument)
- Second-stage coefficient: β = 0.168** (p = 0.022)
- Conclusion: Endogeneity does not reverse findings

---

## 8. Discussion

### 8.1 Theoretical Contributions

1. **RBV in Japanese Context**: Confirms that R&D creates valuable, inimitable resources even in Japan's "lost decades." Challenges narrative of R&D ineffectiveness in mature economies.

2. **Size-Contingent Value of R&D**: Extends Cohen & Klepper (1996) to Japanese firms. Large firms' complementary assets (keiretsu networks, production scale) amplify R&D returns.

3. **Dynamic Capabilities Boundary Condition**: Contrary to prediction, R&D is LESS valuable in hyper-dynamic industries in Japan. Suggests "too much turbulence" limits ability to exploit R&D. Opens new research avenue on optimal environmental dynamism.

### 8.2 Practical Implications

1. **For Small Firms**: R&D alone insufficient; must develop complementary assets or partner with larger firms (e.g., through alliances, licensing).

2. **For Policymakers**: R&D tax credits should be size-differentiated. Small firms may need additional support for commercialization, not just R&D.

3. **For Managers in Dynamic Industries**: In highly turbulent sectors (e.g., consumer electronics), balance R&D investment with rapid commercialization and flexible strategy. Avoid "betting the company" on long-term R&D projects.

### 8.3 Limitations and Future Research

**Limitations**:
1. **Sample Bias**: Only publicly traded firms; excludes SMEs and private firms
2. **R&D Quality**: Cannot distinguish breakthrough vs. incremental R&D
3. **Omitted Variables**: Potential unobserved factors (e.g., R&D team quality, management capability)

**Future Research Directions**:
1. Use patent citations to measure R&D quality
2. Examine R&D collaboration networks (within keiretsu)
3. Conduct qualitative case studies to understand WHY R&D works better in large firms
4. Extend to other Asian economies (Korea, Taiwan) for comparative analysis

---

## 9. Step-by-Step Replication Guide

### 9.1 Data Collection (Week 1-2)

```python
# Step 1: Install required packages
pip install requests pandas numpy edinet-xbrl --break-system-packages

# Step 2: Collect financial data from EDINET
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_edinet_data(start_date, end_date):
    """
    Collect financial data from EDINET API
    """
    base_url = "https://disclosure2.edinet-fsa.go.jp/api/v2"
    
    # Get list of companies
    companies_url = f"{base_url}/documents.json"
    
    # Implementation details in scripts/data_collection_template.py
    pass

# Step 3: Collect patent data from USPTO
from scripts.Data_collection_template import USPTOPatentCollector

collector = USPTOPatentCollector()
patents = collector.get_patents_by_assignee(
    company_name="Toyota Motor Corporation",
    start_date="2010-01-01",
    end_date="2023-12-31"
)
```

### 9.2 Data Cleaning (Week 3-4)

```python
# Use data_cleaning_utils.py
from scripts.data_cleaning_utils import DataCleaningPipeline

pipeline = DataCleaningPipeline()
df_clean = pipeline.clean(
    df,
    continuous_vars=['roa', 'rd_intensity', 'firm_size', 'leverage'],
    categorical_vars=['industry_2digit'],
    entity_col='firm_id',
    time_col='year',
    winsorize=True,
    create_lags=True
)
```

### 9.3 Analysis (Week 5-6)

```python
# Use panel_data_analysis.py
from scripts.panel_data_analysis import PanelRegression

# Prepare panel structure
df_panel = df_clean.set_index(['firm_id', 'year'])

# Run fixed effects regression
results = PanelRegression.fixed_effects(
    df_panel,
    dependent_var='roa',
    independent_vars=['rd_intensity_lag1', 'firm_size', 'leverage', 
                      'sales_growth', 'patent_stock'],
    entity_effects=True,
    time_effects=True
)
```

### 9.4 Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Figure 1: R&D Intensity vs ROA (scatter plot)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='rd_intensity', y='roa', alpha=0.5)
plt.xlabel('R&D Intensity (%)')
plt.ylabel('ROA (%)')
plt.title('Relationship between R&D Intensity and Firm Performance')
plt.savefig('rd_roa_scatter.png', dpi=300)

# Figure 2: Moderation effect by firm size
# Plotting code omitted for brevity
```

---

## 10. File Organization

```
japan_rnd_performance/
├── data/
│   ├── raw/
│   │   ├── edinet_financial_2010_2023.csv
│   │   ├── uspto_patents_japanese_firms.csv
│   │   └── industry_classifications.csv
│   ├── processed/
│   │   ├── merged_dataset.csv
│   │   └── analysis_ready.csv
│   └── data_dictionary.xlsx
├── scripts/
│   ├── 01_collect_edinet.py
│   ├── 02_collect_patents.py
│   ├── 03_clean_data.py
│   ├── 04_construct_variables.py
│   └── 05_run_regressions.py
├── results/
│   ├── descriptive_stats.csv
│   ├── correlation_matrix.csv
│   ├── regression_results.txt
│   └── figures/
│       ├── rd_roa_scatter.png
│       └── moderation_plot.png
├── paper/
│   ├── manuscript.docx
│   ├── tables/
│   │   ├── table1_descriptive.tex
│   │   ├── table2_correlation.tex
│   │   └── table3_regression.tex
│   └── figures/
└── README.md
```

---

## 11. Timeline and Budget

### Timeline (12 weeks)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1-2 | Data collection | Raw datasets |
| 3-4 | Data cleaning | Analysis-ready dataset |
| 5-6 | Descriptive statistics & regression analysis | Regression results |
| 7-8 | Robustness checks | Additional analyses |
| 9-10 | Paper writing (first draft) | Manuscript draft |
| 11-12 | Revision and finalization | Final paper |

### Budget: $0

- All data sources are FREE (EDINET, USPTO PatentsView, World Bank)
- Software: FREE (Python, pandas, linearmodels, matplotlib)
- Compute: FREE (personal computer sufficient)

---

## 12. References

Barnett, W. P., & Hansen, M. T. (1996). The red queen in organizational evolution. *Strategic Management Journal, 17*(S1), 139-157.

Barney, J. (1991). Firm resources and sustained competitive advantage. *Journal of Management, 17*(1), 99-120.

Cohen, W. M., & Klepper, S. (1996). Firm size and the nature of innovation within industries: The case of process and product R&D. *Review of Economics and Statistics, 78*(2), 232-243.

Hoshi, T., Kashyap, A., & Scharfstein, D. (1991). Corporate structure, liquidity, and investment: Evidence from Japanese industrial groups. *Quarterly Journal of Economics, 106*(1), 33-60.

Odagiri, H., & Goto, A. (1996). *Technology and Industrial Development in Japan*. Oxford University Press.

Teece, D. J., Pisano, G., & Shuen, A. (1997). Dynamic capabilities and strategic management. *Strategic Management Journal, 18*(7), 509-533.

---

**End of Example**

This complete example demonstrates every step of an empirical research project from theory to findings. All data sources are free, making it fully replicable with zero budget.

#strategic_research #panel_data #japan_firms #rnd_performance #free_data_sources
