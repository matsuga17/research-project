"""
research_pipeline.py

Strategic Management Research Pipeline - Phase 1-8 Automation

This module provides a complete automated pipeline for conducting strategic
management research following the 8-phase framework:
- Phase 1: Research Design
- Phase 2: Data Source Discovery
- Phase 3: Sample Construction
- Phase 4: Data Collection
- Phase 5: Data Cleaning
- Phase 6: Variable Construction
- Phase 7: Statistical Analysis
- Phase 8: Reporting

Usage:
    from research_pipeline import StrategicResearchPipeline
    
    pipeline = StrategicResearchPipeline(
        research_question="How does R&D intensity affect firm performance?",
        output_dir="./my_research/"
    )
    
    results = pipeline.run_full_pipeline()
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import yaml
import json

# Import related modules
try:
    from .data_quality_checker import DataQualityChecker
except ImportError:
    from data_quality_checker import DataQualityChecker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StrategicResearchPipeline:
    """
    Complete automated pipeline for strategic management research
    
    Attributes:
        research_question: Main research question
        output_dir: Directory for outputs
        config: Configuration dictionary
        results: Results from each phase
    """
    
    def __init__(self, 
                 research_question: str,
                 output_dir: str = "./output/",
                 config_path: Optional[str] = None):
        """
        Initialize the research pipeline
        
        Args:
            research_question: Main research question to investigate
            output_dir: Directory to save all outputs
            config_path: Path to YAML configuration file (optional)
        """
        self.research_question = research_question
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self._default_config()
        
        # Initialize results storage
        self.results = {}
        
        # Setup logging
        self._setup_logging()
        
        logger.info(f"Pipeline initialized for: {research_question}")
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'sample_criteria': {
                'start_year': 2010,
                'end_year': 2023,
                'min_observations': 3,
                'industries': None  # None = all industries
            },
            'data_quality': {
                'max_missing_pct': 0.5,
                'outlier_threshold': 3.0,
                'min_firm_years': 3
            },
            'analysis': {
                'panel_method': 'fixed_effects',
                'cluster_var': 'firm_id',
                'robust_se': True
            }
        }
    
    def _setup_logging(self):
        """Setup detailed logging to file"""
        log_dir = self.output_dir / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'pipeline_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"Logging to: {log_file}")

    
    # ==================== Phase 1: Research Design ====================
    
    def run_phase_1_research_design(self) -> Dict:
        """
        Phase 1: Define research question and theoretical framework
        
        Returns:
            Dictionary with research design details
        """
        logger.info("=" * 60)
        logger.info("PHASE 1: Research Design")
        logger.info("=" * 60)
        
        design = {
            'research_question': self.research_question,
            'phase': 1,
            'timestamp': datetime.now().isoformat(),
            'hypotheses': self._generate_hypotheses(),
            'variables': self._define_variables(),
            'theoretical_framework': 'Resource-Based View, Dynamic Capabilities',
            'sample_criteria': self.config['sample_criteria']
        }
        
        # Save design
        design_file = self.output_dir / 'phase1_research_design.json'
        with open(design_file, 'w') as f:
            json.dump(design, f, indent=2)
        
        logger.info(f"✓ Research design saved to: {design_file}")
        self.results['phase_1'] = design
        
        return design
    
    def _generate_hypotheses(self) -> List[str]:
        """Generate hypotheses based on research question"""
        # Placeholder - in real implementation, this could use NLP or templates
        if 'R&D' in self.research_question or 'innovation' in self.research_question:
            return [
                "H1: R&D intensity positively affects firm performance",
                "H2: The effect is moderated by firm size",
                "H3: Industry competition moderates the relationship"
            ]
        elif 'ESG' in self.research_question:
            return [
                "H1: ESG performance positively affects financial performance",
                "H2: The effect varies by industry",
                "H3: Stakeholder pressure moderates the relationship"
            ]
        else:
            return ["H1: To be defined based on literature review"]
    
    def _define_variables(self) -> Dict:
        """Define dependent, independent, and control variables"""
        return {
            'dependent': ['roa', 'roe', 'tobin_q'],
            'independent': ['rd_intensity', 'innovation_count'],
            'control': ['firm_size', 'firm_age', 'leverage', 'industry', 'year'],
            'moderator': ['industry_concentration', 'market_growth']
        }

    
    # ==================== Phase 2: Data Source Discovery ====================
    
    def run_phase_2_data_sources(self) -> Dict:
        """
        Phase 2: Identify and evaluate data sources
        
        Returns:
            Dictionary with recommended data sources
        """
        logger.info("=" * 60)
        logger.info("PHASE 2: Data Source Discovery")
        logger.info("=" * 60)
        
        sources = {
            'phase': 2,
            'timestamp': datetime.now().isoformat(),
            'primary_sources': self._identify_primary_sources(),
            'supplementary_sources': self._identify_supplementary_sources(),
            'access_status': 'To be verified',
            'estimated_cost': 'To be determined'
        }
        
        # Save source list
        sources_file = self.output_dir / 'phase2_data_sources.json'
        with open(sources_file, 'w') as f:
            json.dump(sources, f, indent=2)
        
        logger.info(f"✓ Data sources saved to: {sources_file}")
        self.results['phase_2'] = sources
        
        return sources
    
    def _identify_primary_sources(self) -> List[Dict]:
        """Identify primary data sources based on research context"""
        # This would ideally query the data-sources-catalog skill
        return [
            {
                'name': 'Compustat North America',
                'type': 'Financial data',
                'coverage': 'US & Canada listed firms',
                'variables': ['financials', 'accounting', 'market data']
            },
            {
                'name': 'CRSP',
                'type': 'Stock market data',
                'coverage': 'US stock returns',
                'variables': ['returns', 'trading volume', 'market cap']
            }
        ]
    
    def _identify_supplementary_sources(self) -> List[Dict]:
        """Identify supplementary data sources"""
        return [
            {
                'name': 'USPTO Patent Database',
                'type': 'Innovation data',
                'coverage': 'US patents',
                'variables': ['patent counts', 'citations']
            },
            {
                'name': 'Bureau of Economic Analysis',
                'type': 'Industry data',
                'coverage': 'US industries',
                'variables': ['industry growth', 'concentration']
            }
        ]

    
    # ==================== Phase 3: Sample Construction ====================
    
    def run_phase_3_sample_construction(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Phase 3: Define sample and apply selection criteria
        
        Args:
            df: Input DataFrame (if None, uses placeholder data)
        
        Returns:
            Filtered DataFrame meeting sample criteria
        """
        logger.info("=" * 60)
        logger.info("PHASE 3: Sample Construction")
        logger.info("=" * 60)
        
        if df is None:
            logger.warning("No input data provided. Using placeholder data.")
            df = self._generate_placeholder_data()
        
        logger.info(f"Initial sample size: {len(df):,} observations")
        
        # Apply sample criteria
        criteria = self.config['sample_criteria']
        
        # Filter by year range
        if 'start_year' in criteria and 'end_year' in criteria:
            df_filtered = df[
                (df['year'] >= criteria['start_year']) & 
                (df['year'] <= criteria['end_year'])
            ].copy()
            logger.info(f"After year filter ({criteria['start_year']}-{criteria['end_year']}): "
                       f"{len(df_filtered):,} observations")
        else:
            df_filtered = df.copy()
        
        # Filter by minimum observations per firm
        if 'min_observations' in criteria:
            firm_counts = df_filtered.groupby('firm_id').size()
            valid_firms = firm_counts[firm_counts >= criteria['min_observations']].index
            df_filtered = df_filtered[df_filtered['firm_id'].isin(valid_firms)]
            logger.info(f"After min observations filter (>={criteria['min_observations']}): "
                       f"{len(df_filtered):,} observations, {len(valid_firms):,} firms")
        
        # Save sample
        sample_file = self.output_dir / 'phase3_sample.csv'
        df_filtered.to_csv(sample_file, index=False)
        logger.info(f"✓ Sample saved to: {sample_file}")
        
        # Generate sample statistics
        sample_stats = {
            'phase': 3,
            'timestamp': datetime.now().isoformat(),
            'total_observations': len(df_filtered),
            'total_firms': df_filtered['firm_id'].nunique(),
            'year_range': [int(df_filtered['year'].min()), int(df_filtered['year'].max())],
            'avg_observations_per_firm': len(df_filtered) / df_filtered['firm_id'].nunique()
        }
        
        stats_file = self.output_dir / 'phase3_sample_stats.json'
        with open(stats_file, 'w') as f:
            json.dump(sample_stats, f, indent=2)
        
        self.results['phase_3'] = {
            'data': df_filtered,
            'statistics': sample_stats
        }
        
        return df_filtered

    
    # ==================== Phase 4: Data Collection ====================
    
    def run_phase_4_data_collection(self) -> pd.DataFrame:
        """
        Phase 4: Collect data from identified sources
        
        Returns:
            Collected raw data
        """
        logger.info("=" * 60)
        logger.info("PHASE 4: Data Collection")
        logger.info("=" * 60)
        
        # In real implementation, this would call data collectors
        # For now, generate placeholder data
        logger.warning("Using placeholder data. In production, this would call:")
        logger.warning("  - EDINET collector for Japanese data")
        logger.warning("  - SEC EDGAR for US data")
        logger.warning("  - Compustat API for financial data")
        
        df_raw = self._generate_placeholder_data()
        
        # Save raw data
        raw_file = self.output_dir / 'phase4_raw_data.csv'
        df_raw.to_csv(raw_file, index=False)
        logger.info(f"✓ Raw data saved to: {raw_file}")
        
        self.results['phase_4'] = {'data': df_raw}
        
        return df_raw
    
    def _generate_placeholder_data(self) -> pd.DataFrame:
        """Generate placeholder panel data for demonstration"""
        np.random.seed(42)
        
        n_firms = 100
        years = range(2010, 2024)
        
        data = []
        for firm_id in range(1, n_firms + 1):
            for year in years:
                data.append({
                    'firm_id': firm_id,
                    'year': year,
                    'roa': np.random.normal(0.05, 0.02),
                    'sales': np.random.lognormal(15, 1.5),
                    'rd_intensity': np.random.uniform(0, 0.15),
                    'firm_age': year - 2000 + np.random.randint(-3, 3),
                    'leverage': np.random.uniform(0.2, 0.6),
                    'industry': np.random.choice(['Tech', 'Manufacturing', 'Finance', 'Retail'], 
                                                p=[0.3, 0.3, 0.2, 0.2])
                })
        
        return pd.DataFrame(data)

    
    # ==================== Phase 5: Data Cleaning ====================
    
    def run_phase_5_data_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Phase 5: Clean data and handle quality issues
        
        Args:
            df: Raw data from Phase 4
        
        Returns:
            Cleaned DataFrame
        """
        logger.info("=" * 60)
        logger.info("PHASE 5: Data Cleaning")
        logger.info("=" * 60)
        
        df_clean = df.copy()
        
        # Run quality checks
        logger.info("Running data quality checks...")
        checker = DataQualityChecker(df_clean, firm_id='firm_id', time_id='year')
        quality_report = checker.check_all()
        
        # Save quality report
        report_text = checker.generate_report()
        report_file = self.output_dir / 'phase5_quality_report.txt'
        with open(report_file, 'w') as f:
            f.write(report_text)
        logger.info(f"✓ Quality report saved to: {report_file}")
        
        # Handle missing values
        logger.info("Handling missing values...")
        initial_count = len(df_clean)
        
        # Drop rows with missing values in key variables
        key_vars = ['firm_id', 'year', 'roa', 'sales']
        df_clean = df_clean.dropna(subset=key_vars)
        
        logger.info(f"  Dropped {initial_count - len(df_clean)} rows with missing key variables")
        
        # Handle outliers
        logger.info("Handling outliers...")
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        threshold = self.config['data_quality']['outlier_threshold']
        
        for col in numeric_cols:
            if col not in ['firm_id', 'year']:
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                df_clean[col] = df_clean[col].clip(
                    lower=mean - threshold * std,
                    upper=mean + threshold * std
                )
        
        # Save cleaned data
        clean_file = self.output_dir / 'phase5_cleaned_data.csv'
        df_clean.to_csv(clean_file, index=False)
        logger.info(f"✓ Cleaned data saved to: {clean_file}")
        
        self.results['phase_5'] = {
            'data': df_clean,
            'quality_report': quality_report
        }
        
        return df_clean

    
    # ==================== Phase 6: Variable Construction ====================
    
    def run_phase_6_variable_construction(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Phase 6: Construct research variables
        
        Args:
            df: Cleaned data from Phase 5
        
        Returns:
            DataFrame with constructed variables
        """
        logger.info("=" * 60)
        logger.info("PHASE 6: Variable Construction")
        logger.info("=" * 60)
        
        df_vars = df.copy()
        
        # Construct dependent variables (already present in this example)
        logger.info("Constructing dependent variables...")
        # ROA, ROE already exist
        
        # Construct independent variables
        logger.info("Constructing independent variables...")
        # rd_intensity already exists
        
        # Construct control variables
        logger.info("Constructing control variables...")
        df_vars['log_sales'] = np.log(df_vars['sales'] + 1)
        df_vars['leverage_squared'] = df_vars['leverage'] ** 2
        
        # Create industry and year dummies
        df_vars = pd.get_dummies(df_vars, columns=['industry'], prefix='ind', drop_first=True)
        df_vars['year_dummy'] = df_vars['year']  # Placeholder for year FE
        
        # Save constructed variables
        vars_file = self.output_dir / 'phase6_variables.csv'
        df_vars.to_csv(vars_file, index=False)
        logger.info(f"✓ Variables saved to: {vars_file}")
        
        # Document variable definitions
        var_definitions = {
            'phase': 6,
            'timestamp': datetime.now().isoformat(),
            'dependent_variables': {
                'roa': 'Return on Assets',
            },
            'independent_variables': {
                'rd_intensity': 'R&D expenditure / Sales',
            },
            'control_variables': {
                'log_sales': 'Log of sales revenue',
                'firm_age': 'Years since founding',
                'leverage': 'Total debt / Total assets',
                'leverage_squared': 'Squared term of leverage',
                'industry_dummies': 'Industry fixed effects',
                'year_dummy': 'Year fixed effects'
            }
        }
        
        var_def_file = self.output_dir / 'phase6_variable_definitions.json'
        with open(var_def_file, 'w') as f:
            json.dump(var_definitions, f, indent=2)
        
        self.results['phase_6'] = {
            'data': df_vars,
            'definitions': var_definitions
        }
        
        return df_vars

    
    # ==================== Phase 7: Statistical Analysis ====================
    
    def run_phase_7_statistical_analysis(self, df: pd.DataFrame) -> Dict:
        """
        Phase 7: Conduct statistical analysis
        
        Args:
            df: Data with constructed variables from Phase 6
        
        Returns:
            Dictionary with analysis results
        """
        logger.info("=" * 60)
        logger.info("PHASE 7: Statistical Analysis")
        logger.info("=" * 60)
        
        results = {}
        
        # Descriptive statistics
        logger.info("Computing descriptive statistics...")
        desc_stats = df.describe()
        desc_file = self.output_dir / 'phase7_descriptive_stats.csv'
        desc_stats.to_csv(desc_file)
        logger.info(f"✓ Descriptive statistics saved to: {desc_file}")
        results['descriptive'] = desc_stats
        
        # Correlation matrix
        logger.info("Computing correlation matrix...")
        numeric_cols = ['roa', 'rd_intensity', 'log_sales', 'firm_age', 'leverage']
        corr_matrix = df[numeric_cols].corr()
        corr_file = self.output_dir / 'phase7_correlation_matrix.csv'
        corr_matrix.to_csv(corr_file)
        logger.info(f"✓ Correlation matrix saved to: {corr_file}")
        results['correlation'] = corr_matrix
        
        # Regression analysis (placeholder - would use statsmodels in real implementation)
        logger.info("Running regression analysis...")
        logger.warning("  Note: Using simplified OLS. For panel data, use statistical-methods skill")
        
        # Calculate simple correlation as proxy for regression coefficient
        beta_rd = df[['roa', 'rd_intensity']].corr().iloc[0, 1]
        
        regression_results = {
            'model': 'OLS (simplified)',
            'dependent_variable': 'roa',
            'independent_variable': 'rd_intensity',
            'coefficient': float(beta_rd),
            'note': 'Use statistical-methods skill for proper panel regression'
        }
        
        reg_file = self.output_dir / 'phase7_regression_results.json'
        with open(reg_file, 'w') as f:
            json.dump(regression_results, f, indent=2)
        logger.info(f"✓ Regression results saved to: {reg_file}")
        results['regression'] = regression_results
        
        self.results['phase_7'] = results
        
        return results

    
    # ==================== Phase 8: Reporting ====================
    
    def run_phase_8_reporting(self) -> str:
        """
        Phase 8: Generate comprehensive research report
        
        Returns:
            Path to generated report
        """
        logger.info("=" * 60)
        logger.info("PHASE 8: Reporting")
        logger.info("=" * 60)
        
        # Generate summary report
        report = self._generate_summary_report()
        
        report_file = self.output_dir / 'phase8_final_report.md'
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"✓ Final report saved to: {report_file}")
        
        self.results['phase_8'] = {'report_path': str(report_file)}
        
        return str(report_file)
    
    def _generate_summary_report(self) -> str:
        """Generate markdown summary report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# Strategic Management Research Report

**Generated**: {timestamp}  
**Research Question**: {self.research_question}

---

## Executive Summary

This report summarizes the complete research pipeline execution from Phase 1 (Research Design) 
through Phase 8 (Reporting).

## Phase 1: Research Design

**Research Question**: {self.research_question}

**Theoretical Framework**: {self.results.get('phase_1', {}).get('theoretical_framework', 'N/A')}

**Hypotheses**:
"""
        
        if 'phase_1' in self.results:
            for i, hyp in enumerate(self.results['phase_1'].get('hypotheses', []), 1):
                report += f"{i}. {hyp}\n"
        
        report += f"""
## Phase 2: Data Sources

**Primary Sources**: 
"""
        
        if 'phase_2' in self.results:
            for source in self.results['phase_2'].get('primary_sources', []):
                report += f"- {source.get('name', 'N/A')}: {source.get('type', 'N/A')}\n"
        
        report += f"""
## Phase 3: Sample Construction

"""
        
        if 'phase_3' in self.results:
            stats = self.results['phase_3'].get('statistics', {})
            report += f"""- Total observations: {stats.get('total_observations', 'N/A'):,}
- Total firms: {stats.get('total_firms', 'N/A'):,}
- Year range: {stats.get('year_range', 'N/A')}
- Average observations per firm: {stats.get('avg_observations_per_firm', 0):.1f}
"""
        
        report += """
## Phase 4: Data Collection

Data collected from identified sources. See `phase4_raw_data.csv` for details.

## Phase 5: Data Cleaning

Data quality checks completed. See `phase5_quality_report.txt` for detailed quality metrics.

## Phase 6: Variable Construction

Research variables constructed according to theoretical framework. 
See `phase6_variable_definitions.json` for variable definitions.

## Phase 7: Statistical Analysis

Statistical analyses completed:
- Descriptive statistics
- Correlation analysis
- Regression analysis

Key findings: See `phase7_regression_results.json`

## Phase 8: Reporting

This comprehensive report documents the entire research process.

---

## Next Steps

1. Review regression results and validate findings
2. Conduct robustness checks (use statistical-methods skill)
3. Prepare manuscript for journal submission
4. Consider additional analyses or extensions

## Files Generated

All output files are saved in: `{self.output_dir}`

- Phase 1: `phase1_research_design.json`
- Phase 2: `phase2_data_sources.json`
- Phase 3: `phase3_sample.csv`, `phase3_sample_stats.json`
- Phase 4: `phase4_raw_data.csv`
- Phase 5: `phase5_cleaned_data.csv`, `phase5_quality_report.txt`
- Phase 6: `phase6_variables.csv`, `phase6_variable_definitions.json`
- Phase 7: `phase7_descriptive_stats.csv`, `phase7_correlation_matrix.csv`, `phase7_regression_results.json`
- Phase 8: `phase8_final_report.md`

---

**Pipeline completed successfully at**: {timestamp}
"""
        
        return report

    
    # ==================== Full Pipeline Execution ====================
    
    def run_full_pipeline(self, input_data: Optional[pd.DataFrame] = None) -> Dict:
        """
        Execute complete research pipeline (Phase 1-8)
        
        Args:
            input_data: Optional input DataFrame (if None, collects data in Phase 4)
        
        Returns:
            Dictionary with all results from each phase
        """
        logger.info("=" * 80)
        logger.info("STRATEGIC MANAGEMENT RESEARCH PIPELINE")
        logger.info(f"Research Question: {self.research_question}")
        logger.info("=" * 80)
        
        start_time = datetime.now()
        
        try:
            # Phase 1: Research Design
            self.run_phase_1_research_design()
            
            # Phase 2: Data Source Discovery
            self.run_phase_2_data_sources()
            
            # Phase 3: Sample Construction (needs data first)
            # Phase 4: Data Collection
            if input_data is None:
                df_raw = self.run_phase_4_data_collection()
            else:
                df_raw = input_data
                logger.info("Using provided input data")
            
            # Now run Phase 3 with collected data
            df_sample = self.run_phase_3_sample_construction(df_raw)
            
            # Phase 5: Data Cleaning
            df_clean = self.run_phase_5_data_cleaning(df_sample)
            
            # Phase 6: Variable Construction
            df_vars = self.run_phase_6_variable_construction(df_clean)
            
            # Phase 7: Statistical Analysis
            analysis_results = self.run_phase_7_statistical_analysis(df_vars)
            
            # Phase 8: Reporting
            report_path = self.run_phase_8_reporting()
            
            # Completion
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("=" * 80)
            logger.info(f"PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Total duration: {duration:.2f} seconds")
            logger.info(f"Output directory: {self.output_dir}")
            logger.info(f"Final report: {report_path}")
            logger.info("=" * 80)
            
            return {
                'status': 'success',
                'duration_seconds': duration,
                'output_directory': str(self.output_dir),
                'final_report': report_path,
                'results': self.results
            }
        
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            return {
                'status': 'failed',
                'error': str(e),
                'results': self.results
            }
    
    def run_specific_phase(self, phase_number: int, **kwargs) -> Any:
        """
        Run a specific phase of the pipeline
        
        Args:
            phase_number: Phase number (1-8)
            **kwargs: Phase-specific arguments
        
        Returns:
            Phase-specific results
        """
        phase_methods = {
            1: self.run_phase_1_research_design,
            2: self.run_phase_2_data_sources,
            3: self.run_phase_3_sample_construction,
            4: self.run_phase_4_data_collection,
            5: self.run_phase_5_data_cleaning,
            6: self.run_phase_6_variable_construction,
            7: self.run_phase_7_statistical_analysis,
            8: self.run_phase_8_reporting
        }
        
        if phase_number not in phase_methods:
            raise ValueError(f"Invalid phase number: {phase_number}. Must be 1-8.")
        
        logger.info(f"Running Phase {phase_number} independently...")
        return phase_methods[phase_number](**kwargs)


# ==================== Command Line Interface ====================

def main():
    """Command line interface for the research pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Strategic Management Research Pipeline'
    )
    parser.add_argument(
        '--question',
        type=str,
        required=True,
        help='Research question to investigate'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output/',
        help='Output directory for results'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration YAML file'
    )
    parser.add_argument(
        '--phase',
        type=int,
        choices=range(1, 9),
        help='Run specific phase only (1-8)'
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = StrategicResearchPipeline(
        research_question=args.question,
        output_dir=args.output_dir,
        config_path=args.config
    )
    
    # Run pipeline
    if args.phase:
        result = pipeline.run_specific_phase(args.phase)
        print(f"\nPhase {args.phase} completed. Results saved to {args.output_dir}")
    else:
        result = pipeline.run_full_pipeline()
        print(f"\nPipeline completed. Status: {result['status']}")
        print(f"Final report: {result.get('final_report', 'N/A')}")


if __name__ == "__main__":
    main()
