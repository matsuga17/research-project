---
name: research-data-collection
description: Comprehensive workflow management system for empirical research data collection. This skill activates when users need to plan, execute, or manage data collection for academic research, including data source discovery, collection strategy design, progress tracking, quality assurance, and risk management. Supports economics, medicine, sociology, public health, and other empirical research fields.
---

# Research Data Collection Manager

A comprehensive skill for managing the entire data collection workflow in empirical research projects.

## When to Use This Skill

This skill should be used when:
- Planning a new data collection project for empirical research
- Searching for appropriate data sources for specific research questions
- Designing data collection strategies and timelines
- Managing ongoing data collection progress
- Performing quality checks on collected data
- Troubleshooting data collection issues
- Documenting data collection procedures

## Core Workflow Phases

This skill guides users through 6 structured phases:

### Phase 1: Research Requirements Analysis
**Objective**: Define precise data requirements based on research questions

**Process**:
1. Clarify research question, hypotheses, and required variables
2. Determine data characteristics:
   - Data type (panel, cross-sectional, time-series, experimental)
   - Temporal scope (date range, frequency)
   - Geographic scope
   - Target sample size
   - Required variables (dependent, independent, control)
3. Identify analytical requirements (statistical power, minimum sample size)

**Output**: Structured data requirements document

### Phase 2: Data Source Discovery & Evaluation
**Objective**: Identify and evaluate potential data sources

**Process**:
1. Search existing data repositories:
   - For economics/finance: World Bank, OECD, IMF, national statistical agencies
   - For medicine/public health: PubMed, ClinicalTrials.gov, FDA databases, WHO
   - For sociology: Census data, survey archives (ICPSR, SSJDA), government statistics
   - Integration with K-Dense-AI scientific-databases skill when available
2. Evaluate each source on:
   - Coverage (temporal, geographic, variable availability)
   - Accessibility (free, paid, restricted)
   - Quality (completeness, reliability, documentation)
   - Format (API, CSV, Excel, PDF)
   - Update frequency
3. Compare multiple sources and identify optimal combination

**Output**: Data source evaluation matrix with recommendations

### Phase 3: Collection Strategy Design
**Objective**: Create detailed, executable data collection plan

**Process**:
1. For secondary data:
   - Identify access methods (API, bulk download, request)
   - Determine authentication/authorization requirements
   - Design data extraction scripts (use scripts/data_collector.py template)
   - Plan data harmonization across multiple sources
2. For primary data:
   - Survey design considerations
   - Sampling strategy
   - Ethical approval requirements
   - Budget and resource allocation
3. Create timeline with milestones
4. Identify risks and mitigation strategies

**Output**: 
- Detailed collection plan document
- Timeline with milestones
- Risk assessment matrix
- Budget estimate

### Phase 4: Implementation Support
**Objective**: Execute data collection with automated tools

**Tools Available**:
- `scripts/data_collector.py` - Generic data collection script template
- `scripts/api_connector.py` - API connection helper
- `scripts/web_scraper.py` - Web scraping template (use responsibly, check ToS)
- Integration with csv-data-summarizer-claude-skill for immediate quality checks

**Process**:
1. Set up data collection environment
2. Test data collection on small sample
3. Execute full collection
4. Monitor for errors and interruptions
5. Document collection process

**Output**: Raw collected data with collection log

### Phase 5: Quality Assurance
**Objective**: Verify data quality and completeness

**Automated Checks**:
1. Completeness:
   - Check expected vs. actual record count
   - Identify missing variables
   - Detect systematic gaps
2. Consistency:
   - Variable type verification
   - Range checks (outliers, impossible values)
   - Cross-variable consistency
3. Accuracy:
   - Sample checks against original sources
   - Duplicate detection
   - Temporal consistency

**Tools**:
- `scripts/quality_checker.py` - Automated quality assessment
- Integration with K-Dense-AI exploratory-data-analysis if available

**Output**: Quality assurance report with issues flagged

### Phase 6: Documentation & Archiving
**Objective**: Create reproducible documentation

**Required Documentation**:
1. Data collection protocol
2. Source documentation with URLs and access dates
3. Variable definitions and coding schemes
4. Known limitations and issues
5. Cleaning/transformation steps applied

**Output**: Comprehensive data documentation package

## Integration with Other Skills

This skill is designed to work seamlessly with:

### K-Dense-AI Scientific Skills
- **scientific-databases**: Direct access to 24+ scientific databases
- **scientific-packages**: Statistical analysis tools (statsmodels, pandas)
- **exploratory-data-analysis**: Automated EDA on collected data
- **scientific-writing**: Format data collection methods section

**Usage Example**:
```
"Use research-data-collection to design my data collection plan, 
then use scientific-databases skill to access PubMed and GWAS Catalog"
```

### csv-data-summarizer-claude-skill
- Automatic quality checks on CSV data immediately after collection
- Distribution analysis to detect anomalies

### Document Skills (xlsx, pdf, docx)
- Extract data from PDF reports
- Create Excel templates for data entry
- Generate Word documentation

## Field-Specific Guidance

### Economics & Finance Research
**Common Data Sources**:
- World Bank Open Data (API: https://data.worldbank.org/)
- OECD Data (https://data.oecd.org/)
- IMF Data (https://data.imf.org/)
- Federal Reserve Economic Data (FRED)
- National statistical agencies (e.g., U.S. Census Bureau, Eurostat)

**Typical Challenges**:
- Data frequency mismatches (monthly vs. quarterly)
- Currency conversions and purchasing power parity
- Seasonal adjustments
- Different accounting standards across countries

**Best Practices**:
- Always document data vintage (release date vs. reference period)
- Keep raw and processed data separate
- Maintain currency and unit consistency

### Medical & Public Health Research
**Common Data Sources**:
- PubMed/MEDLINE for literature
- ClinicalTrials.gov for trial data
- FDA databases for drug information
- WHO Global Health Observatory
- National health surveys (NHANES, BRFSS)

**Typical Challenges**:
- Patient privacy (HIPAA, GDPR compliance)
- Missing data in electronic health records
- Inconsistent diagnostic coding (ICD-9 vs. ICD-10)
- Selection bias in clinical databases

**Best Practices**:
- Obtain IRB approval before accessing patient data
- Use K-Dense-AI ClinicalTrials.gov skill for systematic searches
- Document inclusion/exclusion criteria precisely
- Consider multiple imputation for missing data

### Sociology & Social Science Research
**Common Data Sources**:
- ICPSR (Inter-university Consortium for Political and Social Research)
- General Social Survey (GSS)
- Census data repositories
- Survey data archives (SSJDA for Japan, UKDA for UK)
- Administrative records (when accessible)

**Typical Challenges**:
- Restricted data access (application required)
- Complex survey weights
- Changing questionnaire wording over time
- Non-response bias

**Best Practices**:
- Apply for data access early (can take weeks/months)
- Always use survey weights in analysis
- Document changes in measurement across waves
- Assess non-response patterns

## Advanced Features

### Automated Progress Tracking
The skill maintains a project state that tracks:
- Current phase
- Completed milestones
- Data collection percentage
- Outstanding issues
- Time spent vs. estimated

**Usage**:
```
"Show my data collection progress"
"What's the status of my project?"
"Update: completed data cleaning for 2020-2022"
```

### Risk Assessment
The skill proactively identifies risks:
- **Data availability risk**: Source may not have required coverage
- **Access risk**: Authentication/permission issues
- **Technical risk**: API rate limits, scraping blocks
- **Budget risk**: Paid data exceeds budget
- **Timeline risk**: Collection slower than expected

For each risk, the skill suggests mitigation strategies.

### Multi-Source Data Integration
When research requires combining multiple data sources:
1. Identify common keys (time periods, geographic units, identifiers)
2. Check key consistency across sources
3. Plan merge strategy (left/right/inner join)
4. Validate merged data (record count, missing values)

**Usage**:
```
"I need to merge World Bank GDP data with OECD education data. 
Help me design the integration strategy."
```

## Common Commands

### Starting a New Project
```
"Start a new data collection project for [research topic]"
"I need to collect data for a study on [topic]"
```

### Data Source Search
```
"Find data sources for [variables] in [region] from [time period]"
"What are the best databases for [field] research?"
```

### Progress Check
```
"Show my current progress"
"What's next in my data collection workflow?"
```

### Quality Check
```
"Check data quality for [file]"
"Validate my collected data against the plan"
```

### Documentation
```
"Generate data collection documentation"
"Create a methods section for my paper"
```

## Error Handling & Troubleshooting

### Common Issues

**Issue**: API rate limit exceeded
**Solution**: 
- Implement exponential backoff (built into scripts/api_connector.py)
- Distribute requests over time
- Consider paid API tier if available

**Issue**: Data format inconsistent across time periods
**Solution**:
- Document format changes with dates
- Create harmonization script
- Flag potentially affected analyses

**Issue**: Missing data beyond expected levels
**Solution**:
- Investigate patterns (systematic vs. random)
- Contact data provider if systematic
- Consider multiple imputation or alternative sources
- Document in limitations section

**Issue**: Data collection slower than planned
**Solution**:
- Reassess timeline and adjust milestones
- Identify bottlenecks (download speed, processing time)
- Consider parallel processing or cloud computing
- Prioritize essential variables if timeline is fixed

## Best Practices Summary

1. **Start Early**: Data discovery and access can take weeks to months
2. **Test First**: Always test on a small sample before full collection
3. **Document Everything**: Future you will thank present you
4. **Version Control**: Keep raw data immutable, version processed data
5. **Automate**: Use scripts for reproducibility and efficiency
6. **Validate Continuously**: Check quality at each stage, not just at the end
7. **Plan for Issues**: Assume something will go wrong and have backup plans
8. **Budget Buffer**: Add 20-30% time buffer for unexpected delays
9. **Communicate**: Keep collaborators informed of progress and issues
10. **Ethical Compliance**: Always verify data usage permissions and cite sources

## Output Templates

The skill provides templates for:
- Data collection plan (resources/templates/collection_plan.md)
- Quality assurance checklist (resources/templates/qa_checklist.md)
- Progress tracker (resources/templates/progress_tracker.xlsx)
- Methods section template (resources/templates/methods_template.md)
- Data dictionary template (resources/templates/data_dictionary.xlsx)

## Technical Requirements

### For API-based Collection
- Python 3.8+ with requests, pandas libraries
- Valid API credentials (when required)
- Stable internet connection

### For Web Scraping
- Python 3.8+ with BeautifulSoup, Selenium
- Check website Terms of Service before scraping
- Implement respectful scraping (delays, user-agent)

### For Large-Scale Collection
- Sufficient storage (estimate 2-3x raw data size for processing)
- Consider cloud storage (AWS S3, Google Cloud Storage) for large datasets
- Backup strategy (3-2-1 rule: 3 copies, 2 different media, 1 offsite)

## Getting Started Workflow

For new users, follow this quick-start sequence:

1. **Initial Consultation** (15 minutes)
   - Describe your research question
   - Let the skill analyze your data requirements

2. **Data Source Discovery** (30-60 minutes)
   - Review recommended data sources
   - Evaluate accessibility and quality

3. **Collection Plan Review** (30 minutes)
   - Review generated collection plan
   - Adjust timeline and resources
   - Approve or request modifications

4. **Implementation Setup** (1-2 hours)
   - Install required tools
   - Test scripts on sample data
   - Verify data quality checks work

5. **Full Collection** (varies)
   - Execute collection with monitoring
   - Address issues as they arise

6. **Quality Assurance** (2-4 hours)
   - Run automated quality checks
   - Manually verify sample records
   - Document any data issues

7. **Documentation** (2-3 hours)
   - Complete all documentation templates
   - Archive raw data and scripts
   - Prepare for analysis phase

## Version History

**v1.0** (2025-10-30)
- Initial release
- Core 6-phase workflow
- Integration with K-Dense-AI skills
- Field-specific guidance for economics, medicine, sociology
- Automated quality checking
- Progress tracking
- Risk assessment

## Support & Feedback

This skill is designed to evolve with user needs. Common feedback for improvements:
- Additional field-specific templates
- More data source coverage
- Enhanced automation scripts
- Integration with more existing skills

## License & Citation

If this skill helps your research, consider citing it in your methodology section:

```
Data collection was managed using a systematic workflow tool (research-data-collection skill v1.0) 
that ensured quality assurance and reproducibility throughout the collection process.
```

---

**Ready to start?** Simply say: "Start a new data collection project for [your research topic]" and I'll guide you through Phase 1.