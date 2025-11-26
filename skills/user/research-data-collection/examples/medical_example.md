# Medical Research Example: Diabetes Treatment Outcomes

**Research Topic**: Comparative Effectiveness of Metformin vs. Sulfonylureas in Type 2 Diabetes  
**Field**: Clinical Medicine, Endocrinology, Pharmacoepidemiology  
**Researcher**: [Sample Project]  
**Date**: 2025-10-31  
**IRB Status**: Approved (IRB #2025-001, Approval Date: 2025-01-15)

---

## Project Overview

### Research Question
Among adults with newly diagnosed type 2 diabetes, does metformin monotherapy lead to better glycemic control and fewer adverse events compared to sulfonylurea monotherapy over a 12-month follow-up period?

### Study Design
- **Type**: Retrospective cohort study
- **Setting**: Multi-center electronic health records (EHR) data
- **Population**: Adults aged 18-75 with newly diagnosed type 2 diabetes (2018-2023)
- **Exposure**: First-line therapy (metformin vs. sulfonylureas)
- **Primary outcome**: Change in HbA1c from baseline to 12 months
- **Secondary outcomes**: Hypoglycemia events, gastrointestinal adverse effects, weight change, treatment discontinuation

### Clinical Significance
This study addresses a key clinical question in diabetes management. While metformin is guideline-recommended as first-line therapy, real-world comparative effectiveness data are needed, particularly for diverse patient populations and in routine clinical practice settings.

---

## Phase 1: Research Requirements Analysis

### Data Requirements

**Study Population**:
- **Inclusion Criteria**:
  - Age 18-75 years at diagnosis
  - New diagnosis of type 2 diabetes (ICD-10: E11.*)
  - No prior diabetes medication use
  - Prescribed metformin or sulfonylurea as first-line monotherapy
  - At least 12 months of follow-up data
  - Baseline and 12-month HbA1c measurements available

- **Exclusion Criteria**:
  - Type 1 diabetes (ICD-10: E10.*)
  - Gestational diabetes
  - Severe renal impairment (eGFR < 30 mL/min/1.73m²)
  - Severe liver disease
  - History of pancreatitis
  - Pregnancy during follow-up period

**Sample Size Target**: 2,000 patients (1,000 per treatment group)  
**Power Calculation**: 80% power to detect 0.3% difference in HbA1c (α=0.05)

**Required Data Elements**:

1. **Demographics**:
   - Age, sex, race/ethnicity
   - BMI at baseline
   - Insurance type

2. **Clinical Measurements**:
   - HbA1c (baseline, 3, 6, 12 months)
   - Fasting glucose
   - Lipid panel (LDL, HDL, triglycerides)
   - Blood pressure
   - eGFR (kidney function)
   - Weight/BMI trajectory

3. **Medication Data**:
   - Medication name, dose, frequency
   - Start and stop dates
   - Adherence metrics (medication possession ratio)

4. **Comorbidities** (ICD-10 codes):
   - Hypertension (I10-I15)
   - Hyperlipidemia (E78.*)
   - Coronary artery disease (I25.*)
   - Chronic kidney disease (N18.*)
   - Depression (F32-F33)

5. **Outcomes**:
   - Hypoglycemia events (glucose < 70 mg/dL, ICD-10: E16.2)
   - Gastrointestinal adverse events (ICD-10: K52.9, R10.*, R11.*)
   - Emergency department visits
   - Hospitalizations
   - Treatment discontinuation

---

## Phase 2: Data Source Discovery

### Primary Data Source

#### 1. Multi-Center EHR Research Network
- **Network**: [Hospital System] Research Data Warehouse
- **Coverage**: 5 hospitals, 120 outpatient clinics
- **Patient Volume**: ~500,000 active patients with diabetes
- **EHR System**: Epic Systems
- **Data Elements Available**:
  - Demographics
  - Diagnoses (ICD-10)
  - Medications (RxNorm codes)
  - Laboratory results (LOINC codes)
  - Vital signs
  - Clinical notes (via NLP, if needed)
- **Access**: Institutional data use agreement (DUA) required
- **De-identification**: HIPAA-compliant de-identification performed
- **Update Frequency**: Daily extraction, monthly research database refresh
- **Quality**: ★★★★☆ (4/5) - High completeness for structured data

### Secondary Data Sources (Validation)

#### 2. ClinicalTrials.gov
- **URL**: https://clinicaltrials.gov/
- **Purpose**: Identify existing RCTs for comparison
- **Variables**: Trial design, patient characteristics, outcomes
- **Use**: Literature review and contextualization
- **Access**: Free, API available

#### 3. PubMed (MEDLINE)
- **URL**: https://pubmed.ncbi.nlm.nih.gov/
- **Purpose**: Systematic review of prior studies
- **Search Strategy**: 
  ```
  ("metformin"[MeSH] OR "sulfonylureas"[MeSH]) 
  AND "diabetes mellitus, type 2"[MeSH] 
  AND "comparative effectiveness"[tiab]
  ```
- **Access**: Free, E-utilities API

#### 4. FDA Adverse Event Reporting System (FAERS)
- **URL**: https://open.fda.gov/data/faers/
- **Purpose**: National adverse event surveillance data
- **Use**: Contextualizing safety findings
- **Access**: Free, OpenFDA API

#### 5. National Health and Nutrition Examination Survey (NHANES)
- **URL**: https://www.cdc.gov/nchs/nhanes/
- **Purpose**: Nationally representative diabetes prevalence and management data
- **Use**: Compare study sample to national population
- **Access**: Free download

### Data Access Timeline

| Source | Access Request | Approval | Data Delivery | Status |
|--------|---------------|----------|---------------|--------|
| EHR Research Network | Week 1 | Week 4 | Week 6 | ✅ Complete |
| ClinicalTrials.gov | N/A (public) | N/A | Week 1 | ✅ Complete |
| PubMed | N/A (public) | N/A | Week 1 | ✅ Complete |
| FAERS | N/A (public API) | N/A | Week 2 | ✅ Complete |
| NHANES | N/A (public) | N/A | Week 1 | ✅ Complete |

---

## Phase 3: Collection Strategy and Plan

### Institutional Review Board (IRB) Approval

**Protocol**: Retrospective cohort study using de-identified EHR data  
**IRB Number**: 2025-001  
**Approval Date**: January 15, 2025  
**Expiration**: January 14, 2026  
**Determination**: Expedited review (Category 5: Research involving materials that have been collected solely for non-research purposes)  
**Patient Consent**: Waived (de-identified data, minimal risk)

### EHR Data Extraction Strategy

**Method**: SQL queries via secure research data warehouse

**Extraction Plan**:
1. **Cohort Identification** (Week 1-2):
   - Query patients with new T2D diagnosis (2018-2023)
   - Filter for first-line metformin or sulfonylurea monotherapy
   - Apply inclusion/exclusion criteria
   - Generate patient ID list

2. **Baseline Data Collection** (Week 3):
   - Demographics (age, sex, race, BMI)
   - Comorbidities (12 months prior to diagnosis)
   - Baseline labs (HbA1c, glucose, lipids, eGFR)
   - Baseline vitals (BP, weight)

3. **Medication Data** (Week 4):
   - Drug name, dose, start date
   - Refill history for adherence calculation
   - Treatment switches or discontinuations

4. **Longitudinal Data** (Week 5):
   - Labs at 3, 6, 12 months (±30 days window)
   - Adverse events during follow-up
   - Healthcare utilization (ED visits, hospitalizations)

5. **Quality Checks and Validation** (Week 6):
   - Missing data patterns
   - Outlier detection
   - Logical consistency checks

**Tools**:
- SQL Server Management Studio for queries
- Python (pandas) for data cleaning
- R (tidyverse) for final analysis preparation

### Sample SQL Query (Pseudocode)

```sql
-- Step 1: Identify new T2D diagnoses
WITH new_t2d AS (
    SELECT DISTINCT 
        patient_id,
        MIN(diagnosis_date) AS index_date
    FROM diagnoses
    WHERE icd10_code LIKE 'E11.%'
        AND diagnosis_date BETWEEN '2018-01-01' AND '2023-12-31'
    GROUP BY patient_id
),

-- Step 2: First diabetes medication
first_med AS (
    SELECT 
        m.patient_id,
        m.medication_name,
        m.start_date,
        CASE 
            WHEN m.medication_name LIKE '%metformin%' THEN 'Metformin'
            WHEN m.medication_name IN ('glipizide', 'glyburide', 'glimepiride') THEN 'Sulfonylurea'
            ELSE 'Other'
        END AS treatment_group
    FROM medications m
    INNER JOIN new_t2d t ON m.patient_id = t.patient_id
    WHERE m.start_date BETWEEN t.index_date AND DATEADD(day, 90, t.index_date)
        AND m.medication_class = 'Antidiabetic'
)

-- Step 3: Apply inclusion criteria
SELECT 
    t.patient_id,
    t.index_date,
    f.treatment_group,
    d.age,
    d.sex,
    d.race_ethnicity
FROM new_t2d t
INNER JOIN first_med f ON t.patient_id = f.patient_id
INNER JOIN demographics d ON t.patient_id = d.patient_id
WHERE f.treatment_group IN ('Metformin', 'Sulfonylurea')
    AND d.age BETWEEN 18 AND 75
    AND d.egfr >= 30  -- Exclude severe renal impairment
    -- Additional criteria...
```

### Literature Data Collection (PubMed)

**Python Script**: `scripts/pubmed_search.py` (using `api_connector.py`)

```python
from scripts.api_connector import PubMedAPI

pubmed = PubMedAPI(api_key='YOUR_KEY')
pmids = pubmed.search(
    query='(metformin[MeSH] OR sulfonylureas[MeSH]) AND diabetes mellitus type 2[MeSH] AND comparative effectiveness',
    max_results=100,
    start_date='2015/01/01',
    end_date='2025/12/31'
)

articles = pubmed.fetch_details(pmids)
```

---

## Phase 4: Quality Assurance

### Data Quality Checks

#### 1. Completeness Assessment

| Variable | Required | Actual | Missing % |
|----------|----------|--------|-----------|
| Age | 2000 | 2000 | 0% |
| Sex | 2000 | 2000 | 0% |
| Race/ethnicity | 2000 | 1876 | 6.2% |
| Baseline HbA1c | 2000 | 1945 | 2.8% |
| 12-month HbA1c | 2000 | 1823 | 8.9% |
| Baseline BMI | 2000 | 1988 | 0.6% |
| eGFR | 2000 | 1967 | 1.7% |

**Action**: 
- HbA1c missingness within acceptable range (<10%)
- Conduct sensitivity analysis excluding patients with missing 12-month HbA1c
- Use multiple imputation for missing race/ethnicity in secondary analyses

#### 2. Logical Consistency Checks

**Checks Performed**:
- Age range: All patients 18-75 ✓
- HbA1c range: 5.7-14.0% (diabetes diagnostic criteria met) ✓
- BMI range: 18.5-65 kg/m² (1 outlier: BMI=72, verified as correct) ✓
- eGFR: All ≥ 30 mL/min/1.73m² (exclusion criteria met) ✓
- Medication start date: All within 90 days of diagnosis ✓
- Follow-up duration: All ≥ 365 days ✓

**Issues Found**:
1. 3 patients with HbA1c < 5.7% at baseline → Manual chart review confirmed diabetes diagnosis, baseline measurement was 1-2 months post-diagnosis after lifestyle intervention
2. 12 patients with duplicate records → Resolved by keeping most recent entry

#### 3. Baseline Characteristics Balance

| Characteristic | Metformin (n=1,024) | Sulfonylurea (n=976) | P-value | SMD |
|----------------|---------------------|----------------------|---------|-----|
| Age (years) | 54.2 ± 10.3 | 58.6 ± 9.8 | <0.001 | 0.44 |
| Female (%) | 48.2% | 51.4% | 0.14 | 0.06 |
| Baseline HbA1c (%) | 8.1 ± 1.4 | 8.3 ± 1.5 | 0.02 | 0.14 |
| BMI (kg/m²) | 33.2 ± 6.8 | 30.1 ± 5.9 | <0.001 | 0.49 |

**Note**: Age and BMI significantly different between groups (SMD > 0.1), indicating non-random treatment assignment. **Statistical adjustment required** (propensity score matching or inverse probability weighting).

#### 4. Outcome Ascertainment

**Hypoglycemia Events**:
- Identified through: (1) ICD-10 codes, (2) Glucose < 70 mg/dL, (3) ED/hospital admissions
- Validation: Manual chart review of 50 random events → 94% confirmed
- False positive rate: 6% → Acceptable for sensitivity

**Treatment Discontinuation**:
- Definition: ≥ 90-day gap in medication supply
- Validation: Checked against provider notes → 89% confirmed
- Coding implemented: Binary variable (Yes/No)

### Quality Report Summary

**Overall Data Quality Score**: 92/100 (Excellent)

**Strengths**:
- High completeness for key variables (> 90%)
- Comprehensive outcome ascertainment
- Validated against clinical notes

**Limitations**:
- Treatment group imbalance → Requires propensity score adjustment
- 8.9% missing 12-month HbA1c → Loss to follow-up typical for real-world data
- Race/ethnicity missingness may introduce bias

---

## Phase 5: Data Integration and Statistical Analysis Preparation

### Cohort Flow Diagram (CONSORT-style)

```
Patients with T2D diagnosis (2018-2023)
n = 48,325
    ↓
Applied age criteria (18-75 years)
n = 39,102 (excluded: 9,223)
    ↓
First-line monotherapy (metformin or SU)
n = 6,847 (excluded: 32,255 - other meds/combinations)
    ↓
Adequate baseline data
n = 5,298 (excluded: 1,549 - missing HbA1c or labs)
    ↓
12-month follow-up available
n = 2,456 (excluded: 2,842 - insufficient follow-up)
    ↓
Exclusion criteria applied
n = 2,000 (excluded: 456 - renal impairment, pregnancy, etc.)
    ↓
Final Analytic Sample
Metformin: 1,024 (51.2%)
Sulfonylurea: 976 (48.8%)
```

### Variable Coding

```python
# Primary outcome: HbA1c change
df['hba1c_change'] = df['hba1c_12m'] - df['hba1c_baseline']
df['hba1c_target_achieved'] = (df['hba1c_12m'] < 7.0).astype(int)

# Treatment exposure
df['treatment'] = df['medication_group']  # 'Metformin' or 'Sulfonylurea'

# Covariates for propensity score
covariates = ['age', 'sex', 'race_ethnicity', 'bmi', 'hba1c_baseline',
              'egfr', 'hypertension', 'hyperlipidemia', 'cad']

# Time variables
df['follow_up_days'] = (df['last_visit_date'] - df['index_date']).dt.days

# Medication adherence (MPR = Medication Possession Ratio)
df['mpr'] = df['days_supply'] / df['follow_up_days']
df['adherent'] = (df['mpr'] >= 0.8).astype(int)
```

### Propensity Score Matching

**Method**: 1:1 nearest-neighbor matching without replacement  
**Caliper**: 0.2 standard deviations of the logit of propensity score  
**Software**: R `MatchIt` package

```r
library(MatchIt)

# Estimate propensity scores
ps_model <- glm(treatment ~ age + sex + race + bmi + hba1c_baseline + 
                egfr + hypertension + hyperlipidemia + cad,
                data = df, family = binomial())

# Perform matching
matched <- matchit(treatment ~ age + sex + race + bmi + hba1c_baseline + 
                   egfr + hypertension + hyperlipidemia + cad,
                   data = df, method = "nearest", ratio = 1, caliper = 0.2)

# Check balance
summary(matched)
```

**Post-Matching Sample Size**: 1,845 matched pairs (n = 1,845 per group)

---

## Phase 6: Documentation

### STROBE Checklist Compliance

**Study Design**: Observational cohort study  
**Reporting Guideline**: STROBE (Strengthening the Reporting of Observational Studies in Epidemiology)

| STROBE Item | Location in Manuscript |
|-------------|------------------------|
| Title/Abstract | ✓ |
| Background/Rationale | Introduction (p.2) |
| Objectives | Introduction (p.3) |
| Study design | Methods - Design (p.4) |
| Setting | Methods - Data Source (p.4) |
| Participants | Methods - Cohort (p.5), Figure 1 |
| Variables | Methods - Variables (p.6), Table 1 |
| Data sources/measurement | Methods - Data Collection (p.6-7) |
| Bias | Methods - Statistical Analysis (p.8) |
| Study size | Methods - Sample Size (p.5) |
| Quantitative variables | Table 1 (Baseline characteristics) |
| Statistical methods | Methods - Analysis (p.8-9) |
| Participants | Results - Flowchart (Figure 1) |
| Descriptive data | Results (p.10), Table 2 |
| Outcome data | Results (p.11-12), Table 3 |
| Main results | Results (p.12-13), Figure 2 |
| Other analyses | Results - Subgroup (p.14) |
| Key results | Discussion (p.15) |
| Limitations | Discussion - Limitations (p.17) |
| Interpretation | Discussion (p.15-17) |
| Generalizability | Discussion (p.18) |
| Funding | Acknowledgments (p.20) |

### Data Sharing Statement

**Data Availability**:
Due to institutional privacy policies and HIPAA regulations, the de-identified patient-level data used in this study cannot be made publicly available. Researchers interested in accessing the data may submit a proposal to the [Institution] Institutional Review Board and Data Access Committee. Requests should be directed to [contact email].

**Code Availability**:
All statistical analysis code (R and Python scripts) is publicly available at [GitHub repository URL]. The repository includes:
- Data extraction SQL queries (with synthetic examples)
- Data cleaning and preprocessing scripts
- Propensity score matching code
- Main analysis scripts
- Figure generation code

**Replication Package** (Available upon reasonable request):
- Study protocol
- IRB approval letter (redacted)
- Data dictionary
- STROBE checklist
- Analysis plan (pre-specified)

---

## Results Summary (Preliminary)

### Primary Outcome: HbA1c Change at 12 Months

| Outcome | Metformin | Sulfonylurea | Difference (95% CI) | P-value |
|---------|-----------|--------------|---------------------|---------|
| Mean HbA1c change (%) | -1.2 ± 1.1 | -1.1 ± 1.3 | -0.1 (-0.3 to 0.04) | 0.13 |
| Achieved HbA1c <7% | 62.3% | 58.1% | 4.2% (0.1% to 8.3%) | 0.045 |

**Interpretation**: Both treatments effectively lowered HbA1c. Metformin showed a small but statistically significant advantage in achieving guideline-recommended target.

### Secondary Outcomes

| Outcome | Metformin | Sulfonylurea | OR/HR (95% CI) | P-value |
|---------|-----------|--------------|----------------|---------|
| Hypoglycemia events | 3.2% | 8.7% | 0.35 (0.22-0.56) | <0.001 |
| GI adverse events | 18.4% | 9.2% | 2.21 (1.68-2.91) | <0.001 |
| Weight change (kg) | -2.4 ± 3.8 | +1.1 ± 3.2 | -3.5 (-4.1 to -2.9) | <0.001 |
| Treatment discontinuation | 14.2% | 11.8% | 1.24 (0.94-1.63) | 0.12 |

**Key Findings**:
- Metformin associated with **65% lower risk of hypoglycemia** (important safety advantage)
- Metformin associated with **2.2x higher GI adverse events** (consistent with known profile)
- Metformin led to **modest weight loss** vs. weight gain with sulfonylureas

---

## Clinical Implications

1. **Guideline Support**: Findings support current guideline recommendation for metformin as first-line therapy, particularly for overweight patients

2. **Patient Counseling**: Clinicians should inform patients about:
   - Lower hypoglycemia risk with metformin
   - Potential GI side effects (often transient)
   - Expected weight trajectory

3. **Personalized Treatment**: Sulfonylureas may be appropriate for:
   - Patients intolerant to metformin GI effects
   - Those with contraindications (severe renal impairment)
   - Patients requiring rapid glucose lowering

---

## Lessons Learned

### What Worked Well
1. **EHR Data Access**: Institutional data warehouse provided rich, comprehensive data
2. **Propensity Score Matching**: Successfully balanced treatment groups despite observational design
3. **Outcome Validation**: Chart review confirmed high accuracy of EHR-derived outcomes

### Challenges
1. **Treatment Assignment Bias**: Non-random prescribing required advanced statistical methods
2. **Loss to Follow-Up**: 9% missing 12-month outcomes, typical but requires sensitivity analysis
3. **Data Extraction Complexity**: Required 6 weeks of SQL queries and quality checks

### Recommendations for Future Studies
1. **Prospective Data Collection**: Consider pragmatic trial design for causal inference
2. **Multi-Center Data**: Increase generalizability with national EHR networks
3. **Patient-Reported Outcomes**: Add quality of life measures (missing in EHR)
4. **Longer Follow-Up**: Extend to 2-5 years for cardiovascular outcomes
5. **Pharmacogenomics**: Explore genetic predictors of treatment response

---

## Next Steps

1. **Manuscript Preparation**: Draft for submission to *Diabetes Care* (target: [DATE])
2. **Subgroup Analyses**: Explore effect modification by age, BMI, renal function
3. **Cost-Effectiveness**: Add economic analysis (medication costs, healthcare utilization)
4. **Conference Presentation**: Submit abstract to American Diabetes Association meeting

---

**Project Status**: ✅ Data Collection and Analysis Complete  
**Quality Score**: 92/100 (Excellent)  
**Sample Size**: 2,000 patients (Metformin: 1,024, Sulfonylurea: 976)  
**Time Investment**: 8 weeks (data access + collection + QA)  
**Next Milestone**: Manuscript submission by [DATE]

---

## References

American Diabetes Association. (2024). *Standards of Medical Care in Diabetes—2024*. *Diabetes Care*, 47(Suppl 1), S1-S321.

Maruthur, N. M., et al. (2016). *Diabetes medications as monotherapy or metformin-based combination therapy for type 2 diabetes: A systematic review and meta-analysis*. *Annals of Internal Medicine*, 164(11), 740-751.

Roumie, C. L., et al. (2014). *Association between intensification of metformin treatment with insulin vs sulfonylureas and cardiovascular events and all-cause mortality among patients with diabetes*. *JAMA*, 311(22), 2288-2296.

---

**Example Version**: 1.0  
**Last Updated**: 2025-10-31  
**Field**: Medicine (Endocrinology, Pharmacoepidemiology)  
**Skill**: Research Data Collection v1.0  
**IRB Approved**: Yes (IRB #2025-001)
