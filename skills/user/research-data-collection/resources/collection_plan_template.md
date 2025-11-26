# Data Collection Plan

**Project Name:** [Enter project name]  
**Principal Investigator:** [Your name]  
**Date Created:** [YYYY-MM-DD]  
**Last Updated:** [YYYY-MM-DD]  
**Status:** [Planning / In Progress / Completed]

---

## 1. Research Overview

### 1.1 Research Question
[State your primary research question clearly and concisely]

### 1.2 Hypotheses
1. [Hypothesis 1]
2. [Hypothesis 2]
3. [Additional hypotheses as needed]

### 1.3 Research Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

---

## 2. Data Requirements

### 2.1 Required Variables

#### Dependent Variables
| Variable Name | Description | Expected Type | Expected Range/Values |
|--------------|-------------|---------------|----------------------|
| [var_1] | [description] | [numeric/categorical] | [range] |
| [var_2] | [description] | [numeric/categorical] | [range] |

#### Independent Variables
| Variable Name | Description | Expected Type | Expected Range/Values |
|--------------|-------------|---------------|----------------------|
| [var_1] | [description] | [numeric/categorical] | [range] |
| [var_2] | [description] | [numeric/categorical] | [range] |

#### Control Variables
| Variable Name | Description | Expected Type | Expected Range/Values |
|--------------|-------------|---------------|----------------------|
| [var_1] | [description] | [numeric/categorical] | [range] |
| [var_2] | [description] | [numeric/categorical] | [range] |

### 2.2 Data Characteristics

**Data Type:**
- [ ] Panel data
- [ ] Cross-sectional
- [ ] Time series
- [ ] Experimental
- [ ] Other: [specify]

**Temporal Scope:**
- Start date: [YYYY-MM-DD]
- End date: [YYYY-MM-DD]
- Frequency: [daily/monthly/quarterly/annual]

**Geographic Scope:**
- [ ] Global
- [ ] Multi-country (specify): [countries]
- [ ] National (specify): [country]
- [ ] Regional/State (specify): [region]
- [ ] Local (specify): [location]

**Sample Size:**
- Target N: [number]
- Minimum acceptable N: [number]
- Justification: [power analysis, literature precedent, etc.]

---

## 3. Data Sources

### 3.1 Primary Data Source

**Source Name:** [e.g., World Bank Open Data]  
**URL:** [full URL]  
**API Endpoint (if applicable):** [API URL]  

**Coverage Assessment:**
- Temporal coverage: [dates available]
- Geographic coverage: [regions/countries]
- Variable availability: [✓ All required / ⚠ Some missing / ✗ Insufficient]

**Access Details:**
- Cost: [Free / Paid: $X / Institutional access required]
- Authentication: [None / API key / Login required / Data use agreement]
- Rate limits: [requests per minute/hour/day]
- Download format: [CSV / JSON / Excel / Other]

**Quality Assessment:**
- Completeness: [Excellent / Good / Fair / Poor]
- Reliability: [High / Medium / Low]
- Documentation: [Comprehensive / Adequate / Limited / None]
- Last updated: [date]

### 3.2 Secondary Data Sources (if applicable)

Repeat above template for each additional source.

**Why multiple sources?**
[Explain need for data integration, e.g., different variables, coverage gaps, cross-validation]

---

## 4. Data Collection Strategy

### 4.1 Collection Method

**Primary approach:**
- [ ] API-based collection (automated)
- [ ] Bulk download
- [ ] Web scraping (check ToS first!)
- [ ] Manual download and entry
- [ ] Primary data collection (surveys/experiments)

**Tools to be used:**
- [ ] Python scripts (data_collector.py)
- [ ] R scripts
- [ ] Excel/manual
- [ ] Survey platform (e.g., Qualtrics, Google Forms)
- [ ] Other: [specify]

### 4.2 Data Collection Workflow

1. **Setup Phase** (Duration: [X days])
   - [ ] Obtain necessary API keys/credentials
   - [ ] Set up data collection environment
   - [ ] Test scripts on small sample
   - [ ] Verify data format and structure

2. **Pilot Collection** (Duration: [X days])
   - [ ] Collect 10% sample
   - [ ] Run quality checks (quality_checker.py)
   - [ ] Identify and resolve issues
   - [ ] Adjust collection strategy if needed

3. **Full Collection** (Duration: [X days/weeks])
   - [ ] Execute main data collection
   - [ ] Monitor progress daily
   - [ ] Log any issues or anomalies
   - [ ] Backup data incrementally

4. **Quality Assurance** (Duration: [X days])
   - [ ] Run comprehensive quality checks
   - [ ] Validate against source documentation
   - [ ] Document any data issues
   - [ ] Decide on handling of missing/problematic data

5. **Documentation** (Duration: [X days])
   - [ ] Complete data dictionary
   - [ ] Document collection procedures
   - [ ] Archive raw data and scripts
   - [ ] Prepare data for analysis

### 4.3 Data Integration Plan (if multiple sources)

**Common identifiers:**
- Time period: [how to align temporal data]
- Geographic units: [how to match locations]
- Entity IDs: [how to link records]

**Integration approach:**
- [ ] Left join on [keys]
- [ ] Inner join on [keys]
- [ ] Manual matching required for [cases]

**Expected challenges:**
- [Challenge 1 and mitigation strategy]
- [Challenge 2 and mitigation strategy]

---

## 5. Timeline and Milestones

| Phase | Task | Start Date | End Date | Duration | Status | Notes |
|-------|------|-----------|----------|----------|--------|-------|
| 1 | Setup | [date] | [date] | [X days] | [ ] Not started / [ ] In progress / [ ] Complete | |
| 2 | Pilot collection | [date] | [date] | [X days] | [ ] Not started / [ ] In progress / [ ] Complete | |
| 3 | Full collection | [date] | [date] | [X weeks] | [ ] Not started / [ ] In progress / [ ] Complete | |
| 4 | Quality assurance | [date] | [date] | [X days] | [ ] Not started / [ ] In progress / [ ] Complete | |
| 5 | Documentation | [date] | [date] | [X days] | [ ] Not started / [ ] In progress / [ ] Complete | |

**Critical deadlines:**
- [ ] IRB approval required by: [date]
- [ ] Data collection must complete by: [date]
- [ ] Analysis start date: [date]
- [ ] Manuscript submission target: [date]

---

## 6. Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy | Contingency Plan |
|------|------------|--------|---------------------|------------------|
| Data source unavailable | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |
| API rate limit issues | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |
| Missing key variables | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |
| Data quality below acceptable | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |
| Timeline delays | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |
| Budget exceeded | Low/Med/High | Low/Med/High | [strategy] | [backup plan] |

**Overall risk level:** [Low / Medium / High]

---

## 7. Budget

### 7.1 Direct Costs

| Item | Cost | Notes |
|------|------|-------|
| Data purchase/subscription | $[amount] | [details] |
| Cloud storage | $[amount] | [details] |
| Computing resources | $[amount] | [details] |
| Research assistant time | $[amount] | [hours × rate] |
| Survey incentives | $[amount] | [if applicable] |
| **Total Direct Costs** | **$[total]** | |

### 7.2 Indirect Costs

| Item | Cost | Notes |
|------|------|-------|
| Principal investigator time | $[amount] | [hours × rate] |
| Software licenses | $[amount] | [e.g., Stata, statistical software] |
| **Total Indirect Costs** | **$[total]** | |

**Total Budget:** $[total]  
**Budget Buffer (20%):** $[buffer amount]  
**Total with Buffer:** $[total with buffer]

---

## 8. Ethical and Legal Considerations

### 8.1 Ethics Review
- [ ] IRB approval required
  - Application submitted: [date]
  - Approval received: [date]
  - IRB protocol number: [number]
- [ ] No IRB approval needed (secondary data only)

### 8.2 Data Use Agreements
- [ ] Data use agreement required
  - Agreement signed: [date]
  - Valid until: [date]
- [ ] No agreement required

### 8.3 Privacy and Confidentiality
- [ ] Data contains PII (Personally Identifiable Information)
  - Anonymization strategy: [describe]
- [ ] Data is fully de-identified
- [ ] HIPAA compliance required (for US health data)
- [ ] GDPR compliance required (for EU data)

### 8.4 Data Citation and Attribution
**Primary source citation:**
[Full citation in appropriate format]

**Additional sources:**
1. [Citation]
2. [Citation]

---

## 9. Quality Assurance Plan

### 9.1 Quality Checks

**Completeness checks:**
- [ ] Verify expected number of records
- [ ] Check for missing variables
- [ ] Identify temporal/geographic gaps

**Consistency checks:**
- [ ] Validate data types
- [ ] Check value ranges
- [ ] Cross-variable consistency

**Accuracy checks:**
- [ ] Sample validation against source
- [ ] Duplicate detection
- [ ] Outlier analysis

### 9.2 Acceptance Criteria

Data will be acceptable if:
- [ ] Completeness ≥ [X]% (e.g., 95%)
- [ ] Missing data per variable < [X]% (e.g., 10%)
- [ ] Sample size ≥ [minimum N]
- [ ] Temporal coverage: [full range OR acceptable gaps documented]
- [ ] All required variables present

If criteria not met:
- [ ] Attempt re-collection
- [ ] Seek alternative sources
- [ ] Adjust research design
- [ ] Document limitations

---

## 10. Data Storage and Backup

### 10.1 Storage Plan

**Primary storage:**
- Location: [local drive / cloud storage / institutional server]
- Capacity: [GB needed]
- Access: [who has access]

**Backup storage:**
- Location 1: [secondary location]
- Location 2: [offsite backup]
- Backup frequency: [daily / weekly]
- Backup verification: [how ensured]

### 10.2 Version Control

**Raw data:**
- Stored as: [file naming convention]
- Version: [immutable, never modified]

**Processed data:**
- Stored as: [file naming convention]
- Version numbering: [v1.0, v1.1, etc.]
- Change log: [maintained in separate file]

### 10.3 Data Retention

- Data will be retained for: [5 years / 10 years / indefinitely]
- Deletion plan: [secure deletion method]
- Archive location: [for long-term storage]

---

## 11. Documentation Deliverables

### 11.1 Required Documentation

- [ ] Data collection protocol (this document)
- [ ] Data dictionary / codebook
- [ ] Collection log / audit trail
- [ ] Quality assurance report
- [ ] Data processing scripts (with comments)
- [ ] README file for data users

### 11.2 Methods Section Draft

[Draft the methods section for your paper here, including:
- Data sources with full citations
- Sample selection criteria
- Data collection procedures
- Quality assurance steps
- Known limitations]

---

## 12. Sign-off and Approval

**Prepared by:** [Name, Date]  
**Reviewed by:** [Advisor/Supervisor Name, Date]  
**Approved by:** [Department/IRB, Date]

---

## 13. Change Log

| Date | Version | Change Description | Modified By |
|------|---------|-------------------|-------------|
| [date] | 1.0 | Initial plan created | [name] |
| [date] | 1.1 | [description] | [name] |

---

## 14. Notes and Additional Information

[Use this section for any additional notes, considerations, or information that doesn't fit in the sections above]

---

**Document Status:** DRAFT / UNDER REVIEW / APPROVED  
**Next Review Date:** [date]