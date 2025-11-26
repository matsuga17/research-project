# Research Project Template

## Overview

This template provides a standardized structure for strategic management research projects following the Phase 1-8 workflow.

## Directory Structure

```
research_project/
├── README.md                  # This file
├── config.yaml                # Configuration settings
├── data/
│   ├── raw/                   # Original, immutable data
│   ├── processed/             # Cleaned and transformed data
│   └── final/                 # Final analysis dataset
├── scripts/
│   ├── 01_data_collection.py  # Data collection from sources
│   ├── 02_panel_construction.py  # Panel dataset construction
│   ├── 03_variable_construction.py  # Variable operationalization
│   ├── 04_analysis.py         # Statistical analysis
│   └── 05_visualization.py    # Figure and table generation
├── output/
│   ├── figures/               # Generated plots and charts
│   ├── tables/                # Statistical results tables
│   └── logs/                  # Execution logs
└── notebooks/
    └── exploratory_analysis.ipynb  # Jupyter notebook for exploration
```

## Quick Start

### 1. Configure Your Project

Edit `config.yaml` to specify:
- Research question
- Sample criteria (industry, country, time period)
- Data sources
- Variable definitions

### 2. Data Collection

```bash
python scripts/01_data_collection.py
```

This script will:
- Connect to specified data sources
- Download raw data according to sample criteria
- Save to `data/raw/`

### 3. Panel Construction

```bash
python scripts/02_panel_construction.py
```

This script will:
- Load raw data
- Clean and standardize
- Construct balanced/unbalanced panel
- Save to `data/processed/`

### 4. Variable Construction

```bash
python scripts/03_variable_construction.py
```

This script will:
- Calculate financial ratios
- Construct independent/dependent variables
- Create control variables
- Save to `data/final/`

### 5. Statistical Analysis

```bash
python scripts/04_analysis.py
```

This script will:
- Run regression models
- Perform robustness checks
- Generate results tables
- Save to `output/tables/`

### 6. Visualization

```bash
python scripts/05_visualization.py
```

This script will:
- Create descriptive plots
- Generate regression diagnostics
- Save to `output/figures/`

## Best Practices

### Data Management
- **Never modify raw data**: Keep `data/raw/` immutable
- **Document transformations**: Log all data processing steps
- **Version control data**: Track data versions in logs

### Code Quality
- **Modular scripts**: Each script does one thing well
- **Error handling**: Include try-except blocks
- **Logging**: Write execution logs to `output/logs/`

### Reproducibility
- **Fix random seeds**: Set `random_state=42` in all scripts
- **Document dependencies**: List all required packages
- **Version control**: Use git for code versioning

## Configuration File

The `config.yaml` file should contain:

```yaml
project:
  name: "Your Research Project"
  author: "Your Name"
  date: "2025-11-01"

research_question: |
  Does R&D investment enhance firm performance in 
  Japanese manufacturing firms?

sample:
  industry: "manufacturing"
  country: "Japan"
  start_year: 2010
  end_year: 2023
  min_observations: 5

data_sources:
  - name: "EDINET"
    type: "financial"
  - name: "JPX"
    type: "market"

variables:
  dependent:
    - name: "roa"
      definition: "Return on Assets"
  independent:
    - name: "rd_intensity"
      definition: "R&D / Sales"
  controls:
    - "firm_size"
    - "firm_age"
    - "leverage"
```

## Troubleshooting

### Common Issues

**Issue**: Data download fails
- **Solution**: Check API credentials in config.yaml
- **Solution**: Verify network connection
- **Solution**: Check API rate limits

**Issue**: Panel construction produces errors
- **Solution**: Check for missing values in raw data
- **Solution**: Verify firm_id and year columns exist
- **Solution**: Review data types (numeric vs. string)

**Issue**: Analysis script fails
- **Solution**: Ensure all required variables are present
- **Solution**: Check for multicollinearity (VIF > 10)
- **Solution**: Verify sufficient observations per firm

## Next Steps

1. Customize scripts for your specific research question
2. Add additional analysis methods as needed
3. Integrate with automation pipeline for end-to-end execution

## References

- Strategic Research Suite Documentation: ../SKILL.md
- Data Quality Standards: ../_shared/data-quality-standards.md
- Variable Definitions: ../_shared/common-definitions.md
