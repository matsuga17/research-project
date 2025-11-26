# Research Data Collection Skill

A comprehensive Claude Skill for managing the entire data collection workflow in empirical research projects across economics, medicine, sociology, public health, and other fields.

## 📋 Overview

This skill provides systematic support for:
- ✅ Data source discovery and evaluation
- ✅ Collection strategy design and planning
- ✅ Automated data collection with quality checks
- ✅ Progress tracking and risk management
- ✅ Integration with K-Dense-AI scientific skills
- ✅ Documentation and reproducibility

## 🎯 Key Features

- **6-Phase Workflow**: Structured progression from requirements analysis to documentation
- **Multi-Source Integration**: Combine data from multiple APIs and databases
- **Automated Quality Checks**: Built-in data validation and quality assurance
- **Field-Specific Guidance**: Tailored best practices for economics, medicine, and sociology
- **Risk Management**: Proactive identification and mitigation of common issues
- **Progress Tracking**: Monitor milestones and collection status

## 📁 File Structure

```
research-data-collection/
├── SKILL.md                          # Main skill definition (start here!)
├── README.md                         # This file
├── scripts/
│   ├── data_collector.py            # Generic data collection script
│   ├── quality_checker.py           # Automated quality assessment
│   └── api_connector.py             # API helper utilities (coming soon)
├── resources/
│   ├── data_sources.json            # Comprehensive data source catalog
│   ├── collection_plan_template.md  # Collection plan template
│   └── templates/
│       ├── qa_checklist.md          # Quality assurance checklist
│       ├── data_dictionary.xlsx     # Data dictionary template
│       └── methods_template.md      # Methods section template
└── examples/
    ├── economics_example.md         # Economics research example
    ├── medical_example.md           # Medical research example
    └── sociology_example.md         # Sociology research example
```

## 🚀 Installation

### For Claude.ai (Desktop)

1. **Prepare the Skill Folder**
   - Create a folder named `research-data-collection`
   - Place all skill files in this folder maintaining the structure above

2. **Upload to Claude.ai**
   - Go to Settings → Capabilities → Skills
   - Click "Upload Skill"
   - Select the `research-data-collection` folder
   - Claude will validate and activate the skill

3. **Verify Installation**
   - Start a new conversation
   - Type: "Use research-data-collection skill to help me plan a data collection project"
   - Claude should recognize and activate the skill

### For Claude Code

1. **Add as Plugin**
   ```bash
   # Navigate to your skills directory
   cd ~/.claude/skills
   
   # Create the skill folder
   mkdir research-data-collection
   cd research-data-collection
   
   # Copy all skill files here
   ```

2. **Or Install via Plugin Marketplace** (if you publish to GitHub)
   ```bash
   /plugin marketplace add [your-github-username]/research-data-collection
   /plugin install research-data-collection@[marketplace-name]
   ```

### For API Usage

Skills can also be used via the Claude API. See [Skills API Documentation](https://docs.claude.com/en/api/skills-guide) for details.

## 📖 Quick Start Guide

### Step 1: Start a New Project

Simply say:
```
"Start a new data collection project for [your research topic]"
```

Claude will guide you through Phase 1: Research Requirements Analysis.

### Step 2: Discover Data Sources

```
"Find data sources for [variables] covering [region] from [time period]"
```

Claude will search the data sources catalog and recommend options.

### Step 3: Create Collection Plan

```
"Create a data collection plan for my project"
```

Claude will generate a comprehensive plan using the template, customized to your needs.

### Step 4: Execute Collection

**For automated collection:**
```python
# Claude will help you adapt and run scripts
python scripts/data_collector.py
```

**For guided collection:**
```
"Guide me through collecting data from [source name]"
```

### Step 5: Quality Assurance

```
"Check data quality for my collected data"
```

Claude will run quality checks and provide a comprehensive report.

## 💡 Usage Examples

### Example 1: Economics Research

```
User: "I need panel data on GDP, inflation, and trade for OECD countries, 2000-2023, 
for my research on monetary policy effectiveness."

Claude: [Activates research-data-collection skill]
I'll help you collect this data systematically. Let me analyze your requirements:

Phase 1: Research Requirements Analysis
- Data type: Panel data
- Geographic scope: OECD countries (38 countries)
- Temporal scope: 2000-2023 (24 years)
- Required variables: GDP, inflation rate, trade metrics
- Frequency: Annual (recommended for monetary policy analysis)

Phase 2: Data Source Discovery
Recommended sources:
1. OECD Data (https://data.oecd.org/) - PRIMARY RECOMMENDATION
   - ✓ Complete coverage of all OECD countries
   - ✓ All required variables available
   - ✓ Free access, no authentication
   - ✓ API and bulk download options

Would you like me to proceed with creating a detailed collection plan?
```

### Example 2: Medical Research

```
User: "Find clinical trials on diabetes treatment published in the last 5 years."

Claude: [Activates research-data-collection skill]
I'll search ClinicalTrials.gov for diabetes trials. I can also integrate with 
the K-Dense-AI scientific-databases skill for more comprehensive access.

Searching ClinicalTrials.gov:
- Condition: Diabetes Mellitus
- Date range: 2020-2025
- Status: Completed, recruiting, active

Would you like me to:
1. Extract trial metadata (interventions, outcomes, locations)?
2. Filter by specific trial phases?
3. Create a data dictionary for the collected information?
```

### Example 3: Progress Tracking

```
User: "What's my current progress on data collection?"

Claude: [Retrieves project state]
Project: Economic Policy Analysis
Status: Phase 3 - Full Collection (In Progress)

Progress:
✓ Phase 1: Requirements defined
✓ Phase 2: Data sources identified (OECD, World Bank)
⏳ Phase 3: Collection - 65% complete
   - OECD data: ✓ Complete
   - World Bank data: ⏳ In progress (2015-2023 remaining)
○ Phase 4: Quality assurance (Not started)
○ Phase 5: Documentation (Not started)

Timeline status: On track (3 days remaining in Phase 3)
Next action: Complete World Bank data download, then run quality checks.
```

## 🔗 Integration with Other Skills

### K-Dense-AI Scientific Skills

This skill is designed to work seamlessly with [K-Dense-AI claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills):

```
# Install K-Dense-AI skills first
/plugin marketplace add K-Dense-AI/claude-scientific-skills
/plugin install scientific-databases@claude-scientific-skills

# Then use together
"Use research-data-collection to plan my study, then use PubMed skill 
from scientific-databases to gather literature data"
```

### csv-data-summarizer Skill

Automatically analyze collected CSV data:

```
"After collecting my data, use csv-data-summarizer to generate a quality report"
```

### Document Skills (xlsx, pdf, docx)

Extract data from documents or create formatted outputs:

```
"Use pdf skill to extract tables from this government report, 
then integrate into my data collection"
```

## 🛠️ Python Dependencies

The scripts require these packages:

```bash
pip install pandas numpy requests openpyxl
```

Optional (for enhanced features):
```bash
pip install beautifulsoup4 selenium  # For web scraping
pip install matplotlib seaborn        # For visualization in quality checks
```

## 📊 Data Sources Catalog

The skill includes a comprehensive catalog of 30+ data sources across multiple fields:

**Economics & Finance:**
- World Bank Open Data, OECD, IMF, FRED, US Census

**Medical & Public Health:**
- PubMed, ClinicalTrials.gov, FDA (openFDA), WHO, GWAS Catalog

**Sociology & Social Science:**
- ICPSR, General Social Survey, IPUMS, Eurostat

**General Academic:**
- Harvard Dataverse, Zenodo

See `resources/data_sources.json` for complete details including API documentation, rate limits, and access requirements.

## ⚙️ Configuration

### API Keys

For sources requiring authentication, create a `.env` file:

```bash
# Example .env file
WORLD_BANK_API_KEY=your_key_here
FRED_API_KEY=your_key_here
CENSUS_API_KEY=your_key_here
```

### Custom Data Sources

Add your own data sources to `resources/data_sources.json`:

```json
{
  "your_category": {
    "your_source": {
      "name": "Your Data Source",
      "url": "https://...",
      "api": "https://api...",
      "coverage": {...},
      "access": {...}
    }
  }
}
```

## 🎓 Best Practices

1. **Start Early**: Data discovery and access can take weeks
2. **Test First**: Always pilot with a small sample
3. **Document Everything**: Future you will thank present you
4. **Version Control**: Keep raw data immutable
5. **Automate**: Use scripts for reproducibility
6. **Validate Continuously**: Check quality at each stage
7. **Plan for Issues**: Budget 20-30% time buffer
8. **Backup Religiously**: 3-2-1 rule (3 copies, 2 media types, 1 offsite)

## 🐛 Troubleshooting

### Issue: Skill not activating

**Solution**: Ensure SKILL.md is in the root of the skill folder and contains valid YAML frontmatter.

### Issue: API rate limit exceeded

**Solution**: The data_collector.py includes retry logic. Increase `retry_delay` or implement exponential backoff.

### Issue: Missing Python dependencies

**Solution**: 
```bash
pip install -r requirements.txt  # If you create one
# Or install individually as needed
```

### Issue: Data quality below acceptable threshold

**Solution**: 
1. Review quality_checker.py output
2. Check for systematic issues (data source problem vs. collection error)
3. Consider alternative data sources
4. Document limitations if issue persists

## 📚 Documentation Templates

The skill includes templates for:

- **Collection Plan** (`resources/collection_plan_template.md`) - Comprehensive planning document
- **Quality Assurance Checklist** - Step-by-step QA process
- **Data Dictionary** - Variable definitions and metadata
- **Methods Section** - Ready-to-use text for papers

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional data source integrations
- More field-specific examples
- Enhanced automation scripts
- Bug fixes and documentation improvements

## 📄 License

[Specify your license - e.g., MIT, Apache 2.0, etc.]

## 🙏 Acknowledgments

- Anthropic for the Claude Skills framework
- K-Dense-AI for scientific skills integration patterns
- Research community for best practices

## 📞 Support

For issues or questions:
1. Check this README and SKILL.md documentation
2. Review examples in `examples/` folder
3. Consult data sources documentation
4. [Create an issue on GitHub if published]

## 🔄 Version History

**v1.0** (2025-10-30)
- Initial release
- 6-phase workflow
- 30+ data sources
- Integration with K-Dense-AI skills
- Python automation scripts
- Comprehensive documentation

---

**Ready to revolutionize your data collection workflow?**

Start with: `"Use research-data-collection skill to help me plan my research project on [topic]"`

---

## 📖 Additional Resources

- [Claude Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [K-Dense-AI Scientific Skills](https://github.com/K-Dense-AI/claude-scientific-skills)
- [Anthropic Skills Cookbook](https://github.com/anthropics/skills)
- [Data Management Best Practices](https://www.icpsr.umich.edu/web/pages/datamanagement/)

---

**Last Updated:** 2025-10-30  
**Skill Version:** 1.0  
**Compatibility:** Claude Sonnet 4.5, Claude Code, Claude API