# Complete Automated Research Example

This example demonstrates full automation of a strategic research project from design to publication-ready output.

## Research Question

**"Does R&D investment improve firm performance?"**

## What This Example Does

The automated pipeline executes all 8 phases:

1. **Research Design** - Formulates hypotheses and constructs
2. **Data Collection** - Collects from Compustat and CRSP
3. **Data Integration** - Merges multiple data sources
4. **Panel Construction** - Creates firm-year panel dataset
5. **Quality Assurance** - Checks for missing values and outliers
6. **Variable Construction** - Builds key research variables
7. **Statistical Analysis** - Runs panel regressions
8. **Documentation** - Generates comprehensive report

## Prerequisites

```bash
# Install required packages
pip install pandas numpy statsmodels linearmodels scipy pyyaml
```

## Quick Start

```bash
# Run automated research
python run_automated_research.py
```

## Expected Runtime

**5-10 minutes** for complete execution

## Output Structure

After execution, the `output_automated/` directory will contain:

```
output_automated/
├── data/
│   ├── Compustat North America_raw.csv
│   ├── CRSP_raw.csv
│   ├── panel_merged.csv
│   └── panel_final.csv
├── tables/
│   ├── panel_fe_results.txt
│   └── panel_re_results.txt
├── figures/
│   └── (if visualization enabled)
├── logs/
│   └── pipeline_YYYYMMDD_HHMMSS.log
├── reports/
│   ├── research_design.yaml
│   ├── research_report.md
│   ├── data_dictionary.csv
│   └── quality_report.txt
└── replication/
    ├── README.md
    ├── requirements.txt
    └── config.yaml
```

## Detailed Workflow

### Phase 1: Research Design

```yaml
research_question: "Does R&D investment improve firm performance?"
hypotheses:
  - "H1: R&D intensity positively affects ROA"
  - "H2: The effect is stronger in high-tech industries"
  - "H3: The effect persists after controlling for firm characteristics"
```

### Phase 2-3: Data Collection

- **Compustat**: Financial data (n=200 firms, 2015-2022)
- **CRSP**: Stock market data (n=200 firms, 2015-2022)

### Phase 4: Panel Construction

- Merge on `firm_id` and `year`
- Set MultiIndex for panel structure
- Result: ~1,400 firm-year observations

### Phase 5: Quality Assurance

- Missing value detection
- Outlier identification (|z| > 3)
- Data distribution checks

### Phase 6: Variable Construction

Key variables created:
- `roa` = net_income / total_assets
- `rd_intensity` = rd_expense / revenue
- `firm_size` = log(total_assets)
- `leverage` = total_debt / total_assets
- `rd_intensity_lag1` = lagged R&D intensity

### Phase 7: Statistical Analysis

Models estimated:
1. **Panel Fixed Effects**
   ```
   roa ~ rd_intensity_lag1 + firm_size + leverage + EntityEffects + TimeEffects
   ```

2. **Panel Random Effects**
   ```
   roa ~ rd_intensity_lag1 + firm_size + leverage
   ```

### Phase 8: Documentation

Generates:
- Comprehensive research report (Markdown)
- Data dictionary with variable definitions
- Quality assurance report
- Complete replication package

## Configuration

Edit `research_config.yaml` to customize:

```yaml
# Modify sample size
data_sources:
  - name: Compustat North America
    params:
      n_firms: 500  # Change to 500 firms
      years: range(2010, 2023)  # Extend time period

# Modify model specification
panel_formula: 'roa ~ rd_intensity_lag1 + firm_size + leverage + interaction_term + EntityEffects + TimeEffects'

# Add more statistical methods
statistical_methods:
  - panel_fe
  - panel_re
  - iv_2sls  # Add instrumental variables
```

## Replication Package

The generated replication package includes:

1. **README.md** - Complete replication instructions
2. **requirements.txt** - All Python dependencies
3. **config.yaml** - Exact configuration used
4. **Data sources** - Documentation of data sources
5. **Execution script** - Command to replicate results

To share your results:

```bash
# Create replication archive
cd output_automated/
zip -r ../replication_package.zip replication/

# Share the archive
# Recipients can extract and run:
#   pip install -r requirements.txt
#   python full_pipeline.py --config config.yaml
```

## Troubleshooting

### Memory Errors

If you encounter memory errors with large datasets:

```python
# In research_config.yaml, reduce sample size
data_sources:
  - params:
      n_firms: 100  # Reduce from 200
```

### Long Runtime

To speed up execution:

```python
# Reduce time period
data_sources:
  - params:
      years: range(2018, 2023)  # 5 years instead of 8
```

### Missing Dependencies

```bash
# Install all required packages
pip install -r ../../requirements.txt
```

## Advanced Usage

### Phase-by-Phase Execution

Instead of running the complete pipeline, execute phases individually:

```python
from phase_executor import PhaseExecutor

executor = PhaseExecutor(state_dir='./state/', config=config)

# Execute Phase 1 only
executor.execute_phase(1)

# Execute Phases 2-5
executor.execute_phases(start_phase=2, end_phase=5)

# Resume from checkpoint
executor.resume_from_checkpoint()
```

### Error Handling

```python
from error_handler import ErrorHandler, retry_with_backoff

handler = ErrorHandler(log_file='my_errors.log')

@retry_with_backoff(max_retries=3)
def collect_data():
    # Data collection code with automatic retry
    pass
```

### Custom Reports

```python
from report_builder import ReportBuilder

builder = ReportBuilder(output_dir='./custom_report/')
builder.add_introduction("My custom introduction...")
builder.add_table(results_df, name='custom_table', caption='Custom Results')
builder.generate_report()
```

## Next Steps

1. **Customize the analysis**
   - Modify hypotheses in `research_config.yaml`
   - Add industry interactions
   - Test robustness with alternative specifications

2. **Extend the pipeline**
   - Add text analysis (MD&A sentiment)
   - Include network analysis (board interlocks)
   - Incorporate ESG metrics (CDP data)

3. **Scale to production**
   - Use actual API credentials for data sources
   - Schedule periodic execution (cron jobs)
   - Containerize with Docker

## Related Examples

- `../advanced_automation/` - Multi-study parallel execution
- `../../6-causal-ml/examples/` - Causal Forest integration
- `../../7-esg-sustainability/examples/` - ESG data integration

## References

This example implements the workflow described in:

- Christensen, G., & Miguel, E. (2018). "Transparency, reproducibility, and the credibility of economics research." *Journal of Economic Literature*, 56(3), 920-980.

## Support

For questions or issues:
1. Check the main documentation: `../../README.md`
2. Review troubleshooting section above
3. Check logs in `output_automated/logs/`

---

**Version**: 4.0  
**Last Updated**: 2025-11-02  
**Estimated Completion**: 95%
