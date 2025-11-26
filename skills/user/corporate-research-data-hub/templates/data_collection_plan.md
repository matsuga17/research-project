# Data Collection Plan Template

## 1. Research Context

### 1.1 Research Question
[Clearly state your research question]

### 1.2 Hypotheses
- H1: [Hypothesis 1]
- H2: [Hypothesis 2]
- H3: [Hypothesis 3]

### 1.3 Research Domain
- [ ] Corporate Finance
- [ ] Strategic Management
- [ ] Corporate Governance
- [ ] Organizational Behavior
- [ ] ESG & Sustainability
- [ ] Other: ___________

---

## 2. Sample Definition

### 2.1 Population
- **Geographic Scope**: [e.g., United States, Europe, Global]
- **Industry Scope**: [e.g., All industries, Manufacturing (SIC 2000-3999), Technology]
- **Firm Type**: [e.g., Publicly traded, Private, Both]
- **Time Period**: [Start Year] to [End Year]
- **Data Frequency**: [Annual, Quarterly, Monthly]

### 2.2 Inclusion Criteria
1. [Criterion 1, e.g., "Listed on major stock exchange"]
2. [Criterion 2, e.g., "Total assets ≥ $10M"]
3. [Criterion 3, e.g., "At least 3 consecutive years of data"]
4. [Add more as needed]

**Justification**: [Why these criteria?]

### 2.3 Exclusion Criteria
1. [Criterion 1, e.g., "Financial firms (SIC 6000-6999)"]
2. [Criterion 2, e.g., "Utilities (SIC 4900-4999)"]
3. [Criterion 3, e.g., "Firms with negative book equity"]
4. [Add more as needed]

**Justification**: [Why exclude these?]

### 2.4 Expected Sample Size
- **Expected Firms**: [Estimated number]
- **Expected Firm-Years**: [Estimated number]
- **Statistical Power**: [If calculated]

---

## 3. Variable Requirements

### 3.1 Dependent Variables
| Variable | Definition | Source | Expected Availability |
|----------|------------|--------|----------------------|
| [var1] | [Definition] | [Database] | [%] |
| [var2] | [Definition] | [Database] | [%] |

### 3.2 Independent Variables
| Variable | Definition | Source | Expected Availability |
|----------|------------|--------|----------------------|
| [var1] | [Definition] | [Database] | [%] |
| [var2] | [Definition] | [Database] | [%] |

### 3.3 Control Variables
| Variable | Definition | Source | Expected Availability |
|----------|------------|--------|----------------------|
| Firm Size | Log of total assets | Compustat | 95% |
| Firm Age | Years since founding | Compustat | 90% |
| [Add more] | [Definition] | [Database] | [%] |

### 3.4 Moderating/Mediating Variables (if applicable)
| Variable | Definition | Source | Expected Availability |
|----------|------------|--------|----------------------|
| [var1] | [Definition] | [Database] | [%] |

---

## 4. Data Sources

### 4.1 Primary Data Sources
| Source | Purpose | Variables | Access Method | Cost |
|--------|---------|-----------|---------------|------|
| Compustat | Financial data | Assets, Sales, ROA | WRDS subscription | Institutional |
| CRSP | Market data | Returns, Prices | WRDS subscription | Institutional |
| [Add more] | [Purpose] | [Variables] | [Method] | [Cost] |

### 4.2 Secondary/Supplementary Sources
| Source | Purpose | Variables | Access Method | Cost |
|--------|---------|-----------|---------------|------|
| [Source] | [Purpose] | [Variables] | [Method] | [Cost] |

### 4.3 Data Source Evaluation
For each major source:
- **Coverage**: [Temporal, geographic, variable coverage]
- **Quality**: [Completeness, reliability, known issues]
- **Accessibility**: [How to access, authentication required?]
- **Alternatives**: [Backup sources if primary unavailable]

---

## 5. Data Collection Timeline

### 5.1 Milestones
| Phase | Task | Start Date | End Date | Duration | Status |
|-------|------|------------|----------|----------|--------|
| 1 | Obtain data access | [Date] | [Date] | [Days] | [ ] |
| 2 | Download Source A | [Date] | [Date] | [Days] | [ ] |
| 3 | Download Source B | [Date] | [Date] | [Days] | [ ] |
| 4 | Data cleaning | [Date] | [Date] | [Days] | [ ] |
| 5 | Data merging | [Date] | [Date] | [Days] | [ ] |
| 6 | Quality checks | [Date] | [Date] | [Days] | [ ] |
| 7 | Final dataset | [Date] | [Date] | [Days] | [ ] |
| **Total** | | | | [Total Days] | |

### 5.2 Critical Path
- [Identify which tasks are on critical path]
- [Which delays would push overall timeline?]

### 5.3 Buffer Time
- **Planned Buffer**: [% or days]
- **Rationale**: [Why this buffer?]

---

## 6. Data Collection Procedures

### 6.1 Source A: [Database Name]
**Access Method**:
- [ ] Direct download
- [ ] API
- [ ] SQL query
- [ ] Manual extraction

**Procedure**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Output**:
- File format: [CSV, SAS, Stata, etc.]
- File size: [Approximate size]
- Variables included: [List key variables]

**Authentication**:
- Username: [Institution or personal]
- Access expires: [Date if applicable]

### 6.2 Source B: [Database Name]
[Repeat structure from 6.1]

---

## 7. Data Integration Plan

### 7.1 Matching Strategy
| Source A | Source B | Match Key | Match Type | Expected Match Rate |
|----------|----------|-----------|------------|---------------------|
| Compustat | CRSP | GVKEY-PERMNO link | One-to-one | 95% |
| [Source A] | [Source B] | [Key] | [Type] | [%] |

### 7.2 Merge Sequence
1. [First merge: Source A + Source B on key X]
2. [Second merge: Result + Source C on key Y]
3. [Final merge: Result + Source D on key Z]

**Rationale for sequence**: [Why this order?]

### 7.3 Handling Unmatched Observations
- [Strategy for observations in A but not B]
- [Strategy for observations in B but not A]
- [Documentation plan for unmatched cases]

---

## 8. Data Cleaning & Standardization

### 8.1 Unit Standardization
- **Currency**: Convert to [USD, Local, etc.]
- **Units**: [Thousands, Millions, Billions]
- **Inflation Adjustment**: [Yes/No, Base year: ___]

### 8.2 Missing Data Strategy
| Variable | Missing % (Expected) | Treatment |
|----------|----------------------|-----------|
| R&D Expenditure | 40% | Set to 0 with indicator variable |
| [Variable] | [%] | [Strategy] |

### 8.3 Outlier Treatment
- **Method**: [Winsorization / Trimming / Case-by-case]
- **Thresholds**: [1st and 99th percentiles / 3 SD / Custom]
- **Variables to treat**: [List]

### 8.4 Variable Transformations
| Original Variable | Transformation | New Variable | Rationale |
|-------------------|----------------|--------------|-----------|
| Total Assets | Natural log | log_assets | Normalize distribution |
| [Variable] | [Transformation] | [New name] | [Rationale] |

---

## 9. Quality Assurance Plan

### 9.1 Automated Checks
- [ ] Record count validation
- [ ] Accounting identity verification
- [ ] Temporal consistency checks
- [ ] Cross-sectional reasonableness
- [ ] Outlier detection
- [ ] Missing data pattern analysis

### 9.2 Manual Validation
- [ ] Sample-based verification (n = [50-100])
- [ ] Cross-check against original sources
- [ ] Time series plots for selected firms
- [ ] Comparison with literature benchmarks

### 9.3 Quality Metrics
- Target completeness: [%, e.g., 90% of variables ≥80% complete]
- Acceptable error rate: [%, e.g., <1% of manual checks reveal errors]
- Match rate threshold: [%, e.g., ≥85% match rate for key merges]

---

## 10. Risk Assessment & Mitigation

### 10.1 Identified Risks
| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Data access denied | Low | High | Apply for access 6 months in advance |
| API rate limits | Medium | Medium | Implement exponential backoff |
| Poor match rates | Medium | High | Prepare alternative matching strategies |
| [Add risk] | [L/M/H] | [L/M/H] | [Strategy] |

### 10.2 Contingency Plans
- **If primary data source unavailable**: [Alternative source or approach]
- **If match rates below threshold**: [Plan B for integration]
- **If timeline exceeded**: [Which corners can be cut safely?]

---

## 11. Documentation Requirements

### 11.1 During Collection
- [ ] Daily log of data collection activities
- [ ] Issues encountered and resolutions
- [ ] Query scripts and download dates
- [ ] Intermediate file versions

### 11.2 Final Documentation
- [ ] Data dictionary (all variables defined)
- [ ] Codebook (sample selection, variable construction)
- [ ] Quality assurance report
- [ ] Replication scripts
- [ ] README file for collaborators

---

## 12. Budget (if applicable)

| Item | Cost | Notes |
|------|------|-------|
| Database subscriptions | [Amount] | [Details] |
| Cloud storage | [Amount] | [Details] |
| Computing resources | [Amount] | [Details] |
| Research assistants | [Amount] | [Details] |
| **Total** | [Total Amount] | |

---

## 13. Team Responsibilities

| Team Member | Role | Responsibilities | Contact |
|-------------|------|------------------|---------|
| [Name] | PI | Overall supervision, design | [Email] |
| [Name] | Data Manager | Data collection, cleaning | [Email] |
| [Name] | RA | Quality checks, documentation | [Email] |

---

## 14. Approvals & Compliance

### 14.1 Institutional Review
- [ ] IRB approval required? [Yes/No]
  - If Yes: Application submitted: [Date]
  - Approval received: [Date]
  - Protocol number: [Number]

### 14.2 Data Use Agreements
- [ ] Compustat/WRDS: [Agreement signed: Date]
- [ ] [Other database]: [Agreement signed: Date]

### 14.3 License Compliance
- [ ] Reviewed terms of service for all sources
- [ ] Citation requirements documented
- [ ] Data sharing restrictions noted

---

## 15. Review & Approval

### 15.1 Plan Review Checklist
- [ ] Research question clearly defined
- [ ] Sample selection justified
- [ ] All required variables identified
- [ ] Data sources evaluated and accessible
- [ ] Timeline realistic with buffers
- [ ] Risks identified with mitigation plans
- [ ] Budget adequate (if applicable)
- [ ] Documentation plan complete

### 15.2 Approval
**Prepared by**: [Name], [Date]
**Reviewed by**: [Name], [Date]
**Approved by**: [Name], [Date]

### 15.3 Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Name] | Initial plan |
| 1.1 | [Date] | [Name] | Updated timeline |

---

## 16. Notes & Comments

[Space for additional notes, decisions, or comments]

---

**Next Steps After Plan Approval**:
1. Obtain necessary data access
2. Set up project directory structure
3. Download test data (small sample)
4. Validate collection procedures
5. Begin full data collection

**Contact for Questions**: [Name, Email]