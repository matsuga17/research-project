# Methods Section Template for Data Collection

**Note**: このテンプレートは、学術論文のMethodsセクション（特にデータ収集部分）を作成するためのものです。研究分野や投稿先ジャーナルの要件に応じてカスタマイズしてください。

---

## Data Collection and Sources

### 1. Data Sources

We obtained data from [NUMBER] primary sources to construct our analytical dataset covering [TIME PERIOD] for [GEOGRAPHIC SCOPE]. The data sources were selected based on [SELECTION CRITERIA: e.g., data quality, temporal coverage, variable availability, and institutional credibility].

**Primary Data Source:**
[SOURCE NAME] ([ORGANIZATION], [YEAR]) provided [DESCRIPTION OF DATA]. This dataset includes [KEY VARIABLES] for [NUMBER] [UNITS: countries/individuals/firms] over [TIME PERIOD]. The data are publicly accessible at [URL] under [LICENSE TYPE] license. [SOURCE NAME] employs [METHODOLOGY DESCRIPTION] to ensure data quality and reliability. [If applicable: The database has been widely used in prior research (citations: Author1, Year; Author2, Year)].

**Secondary Data Sources:**
We supplemented the primary data with information from:

1. **[SOURCE 2 NAME]** ([ORGANIZATION], [YEAR]): [BRIEF DESCRIPTION]
   - Variables: [LIST KEY VARIABLES]
   - Coverage: [GEOGRAPHIC and TEMPORAL]
   - Access: [URL]
   - Merge key: [e.g., country-year identifier]

2. **[SOURCE 3 NAME]** ([ORGANIZATION], [YEAR]): [BRIEF DESCRIPTION]
   - Variables: [LIST KEY VARIABLES]
   - Coverage: [GEOGRAPHIC and TEMPORAL]
   - Access: [URL]
   - Merge key: [e.g., individual ID, firm identifier]

[If using APIs or automated collection:]
Data were collected programmatically using [API NAME/WEB SCRAPING TOOL] with [FREQUENCY: e.g., daily updates, one-time download]. All API calls and data extraction scripts are available in our replication package [CITE REPOSITORY].

---

### 2. Sample Selection and Inclusion Criteria

Our final analytical sample consists of [NUMBER] observations ([UNIT: country-years, individuals, firms, etc.]) selected through the following criteria:

**Inclusion Criteria:**
1. [CRITERION 1: e.g., Complete data for all key variables]
2. [CRITERION 2: e.g., Countries with population > 1 million]
3. [CRITERION 3: e.g., Firms operating continuously throughout the study period]

**Exclusion Criteria:**
1. [CRITERION 1: e.g., Missing more than 20% of observations]
2. [CRITERION 2: e.g., Outliers beyond 3 standard deviations (0.3% of sample)]
3. [CRITERION 3: e.g., Data quality flags from source organization]

[Figure/Table reference: Figure 1 presents a flowchart of the sample selection process, showing the number of observations at each stage.]

**Sample Attrition:**
[If applicable]
The initial dataset contained [N_initial] observations. After applying inclusion/exclusion criteria, [N_excluded] observations ([PERCENTAGE]%) were removed, resulting in [N_final] observations for analysis. Attrition analysis showed [RESULT: e.g., no systematic differences between included and excluded observations on observable characteristics; see Appendix Table A1].

---

### 3. Variable Construction and Measurement

**Dependent Variable:**
[VARIABLE NAME] measures [CONCEPT]. Following [PRIOR LITERATURE CITATION], we construct this variable as [FORMULA/DEFINITION]. [If applicable: We use log transformation to address skewness; original values ranged from X to Y with mean Z].

**Key Independent Variables:**
1. **[VARIABLE 1 NAME]**: [DEFINITION and MEASUREMENT]. Sourced from [DATA SOURCE]. [If constructed: Calculated as (formula)].
   - Mean: [VALUE], SD: [VALUE], Range: [MIN] to [MAX]

2. **[VARIABLE 2 NAME]**: [DEFINITION and MEASUREMENT]. Sourced from [DATA SOURCE].
   - Mean: [VALUE], SD: [VALUE], Range: [MIN] to [MAX]

**Control Variables:**
We include the following control variables based on prior research [CITATIONS]:
- [CONTROL 1]: [BRIEF DESCRIPTION and SOURCE]
- [CONTROL 2]: [BRIEF DESCRIPTION and SOURCE]
- [CONTROL 3]: [BRIEF DESCRIPTION and SOURCE]

[Table reference: Table 1 provides detailed variable definitions, data sources, and descriptive statistics.]

---

### 4. Data Quality and Validation

**Missing Data:**
Missing values occurred in [PERCENTAGE]% of observations for key variables. [DESCRIBE PATTERN: e.g., Missing values were primarily in earlier years (2000-2005) for developing countries]. We addressed missing data through [METHOD: listwise deletion / multiple imputation / interpolation / other]. [If imputation: We used [METHOD: e.g., chained equations with 20 imputed datasets]. Imputation models included [PREDICTOR VARIABLES].]

**Outliers:**
We identified outliers using [METHOD: e.g., Tukey's IQR method, z-scores > 3]. [NUMBER] observations ([PERCENTAGE]%) were flagged as outliers. [TREATMENT: We conducted robustness checks with and without outliers; main results remained consistent. / We winsorized variables at the 1st and 99th percentiles. / Other treatment].

**Data Validation:**
Data quality was verified through:
1. **Cross-validation**: We compared [VARIABLE] from [SOURCE 1] with [SOURCE 2] for [SAMPLE SIZE] overlapping observations, finding [CORRELATION/AGREEMENT LEVEL].
2. **Logic checks**: We implemented [NUMBER] logic rules (e.g., GDP > 0, age >= 18) and found [NUMBER] violations ([PERCENTAGE]%), which were [CORRECTED/EXCLUDED].
3. **Time-series consistency**: We checked for implausible year-to-year changes (>X%) and investigated [NUMBER] flagged cases.

**Harmonization:**
[If combining data from multiple sources or time periods:]
We harmonized variables across sources by [METHODS: e.g., standardizing units (all monetary values converted to 2020 USD using [DEFLATOR SOURCE]), reconciling different classification systems (we mapped [CLASSIFICATION A] to [CLASSIFICATION B] using [CROSSWALK SOURCE])].

---

### 5. Data Processing and Cleaning

Data processing followed these steps:

1. **Initial Import and Format Standardization** ([DATE]):
   - Raw data files downloaded from sources
   - Converted all files to [FORMAT: CSV/Parquet]
   - Standardized variable names to lowercase with underscores

2. **Variable Recoding** ([DATE]):
   - Recoded categorical variables to numeric codes (see codebook in Appendix)
   - Standardized date formats to YYYY-MM-DD
   - Created dummy variables for [CATEGORICAL VARIABLES]

3. **Data Merging** ([DATE]):
   - Merged datasets using [MERGE KEY: e.g., country ISO codes and year]
   - [If applicable: Many-to-one merge resulted in [N] matched observations out of [N_total] attempts, with [N_unmatched] unmatched ([PERCENTAGE]%)]

4. **Variable Construction** ([DATE]):
   - Created interaction terms, polynomials, and lagged variables
   - Calculated growth rates as: (Value_t - Value_{t-1}) / Value_{t-1} * 100

5. **Final Cleaning** ([DATE]):
   - Removed [N] duplicate observations
   - Applied exclusion criteria (see Section 2)
   - Final dataset: [N_obs] observations, [N_vars] variables

All data processing was conducted in [SOFTWARE: R 4.3.1 / Python 3.11 / Stata 18]. Processing scripts are available at [REPOSITORY URL].

---

### 6. Ethical Considerations and Data Availability

**Ethical Approval:**
[For human subjects data:]
This study was approved by [INSTITUTION] Institutional Review Board (IRB #[NUMBER], approval date: [DATE]). [If applicable: Participants provided informed consent. / Data were de-identified prior to analysis.]

[For publicly available data:]
All data used in this study are publicly available and do not contain personally identifiable information. Use of these data complies with the terms of service and licensing agreements of the data providers.

**Data Availability:**
[Choose appropriate statement:]

*Option 1 (Open data):*
All data and code used in this study are publicly available at [REPOSITORY: e.g., GitHub, Dataverse, OSF] ([DOI/URL]). The replication package includes:
- Raw data files (with source documentation)
- Data processing scripts
- Analysis code
- Codebook and data dictionary

*Option 2 (Restricted access):*
The data used in this study are subject to [RESTRICTIONS: licensing agreements / privacy regulations / institutional policies]. Researchers may request access by [PROCEDURE: contacting the data provider at [URL/EMAIL]]. Our analytical code is available at [REPOSITORY].

*Option 3 (Proprietary data):*
The data that support the findings of this study are available from [ORGANIZATION] but restrictions apply to the availability of these data, which were used under license for the current study. Data are available from the authors upon reasonable request and with permission of [ORGANIZATION].

---

### 7. Limitations

Our data collection approach has several limitations:

1. **Coverage Limitations**: [e.g., Data are available only for OECD countries, limiting generalizability to developing nations]

2. **Temporal Gaps**: [e.g., Several countries lack data for the 2008-2010 period due to the global financial crisis]

3. **Measurement Issues**: [e.g., Self-reported data may be subject to social desirability bias]

4. **Harmonization Challenges**: [e.g., Definition of [VARIABLE] changed in [YEAR], requiring adjustment that may introduce measurement error]

5. **Survivorship Bias**: [If applicable: Our sample includes only firms/countries that existed throughout the period, potentially biasing results]

We address these limitations through [MITIGATION STRATEGIES: robustness checks, sensitivity analyses, etc.] and acknowledge that results should be interpreted with these constraints in mind.

---

## Appendix: Additional Data Documentation

### A. Data Sources Summary Table

| Source Name | Organization | Variables | Coverage | Update Frequency | Access |
|------------|--------------|-----------|----------|------------------|--------|
| [SOURCE 1] | [ORG] | [LIST] | [GEO, TEMP] | [FREQ] | [URL] |
| [SOURCE 2] | [ORG] | [LIST] | [GEO, TEMP] | [FREQ] | [URL] |

### B. Sample Construction Flowchart

[Describe or reference figure showing:]
- Initial sample size from each source
- Observations excluded at each filtering step
- Final analytical sample size

### C. Variable Definitions Table

[Detailed table with:]
- Variable name
- Definition
- Data source
- Unit of measurement
- Calculation method (if constructed)

### D. Descriptive Statistics

[Table showing:]
- Variable names
- N (observations)
- Mean
- Standard deviation
- Min
- Max
- Missing (%)

### E. Missing Data Patterns

[If substantial missingness:]
- Describe which variables and observations have missing data
- Show correlation of missingness across variables
- Discuss whether missingness is random or systematic

---

## References for Methods Section

[List all data sources with full citations:]

[ORGANIZATION]. ([YEAR]). *[Database/Dataset Name]*. Retrieved from [URL]. Accessed on [DATE].

[If applicable, cite methodological papers:]

[AUTHOR]. ([YEAR]). [Title of paper on data collection methodology]. *Journal Name*, *Volume*(Issue), pages. DOI: [DOI]

---

## Customization Notes

**For Field-Specific Requirements:**

- **Economics**: Emphasize sample representativeness, selection bias, and econometric identification
- **Medicine/Public Health**: Include IRB approval details, CONSORT/STROBE guidelines compliance, and patient consent procedures
- **Sociology**: Discuss sampling strategy (probability vs. convenience), response rates, and demographic representativeness

**For Journal-Specific Requirements:**

- Check target journal's author guidelines for data availability statements
- Some journals require pre-registration (e.g., OSF, AsPredicted)
- Nature/Science often require data deposition in approved repositories

**Word Count Considerations:**

This template is comprehensive. For word-limited journals:
- Condense Sections 1-3 into main text (300-500 words)
- Move Sections 4-7 to Supplementary Materials
- Include only key citations in main text

---

**Template Version:** 1.0  
**Last Updated:** 2025-10-31  
**Compatible with:** APA 7th, Chicago, Vancouver styles (adapt citations accordingly)
