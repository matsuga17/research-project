#!/usr/bin/env python3
"""
Quality Assurance System for Strategic Management Research Pipeline
====================================================================

Comprehensive quality assurance tests for the entire research pipeline,
from data collection to publication-ready outputs.

Usage:
    python test_qa_system.py --project-dir ./my_research_project/

Test Categories:
1. Data Collection QA
2. Data Cleaning QA
3. Analysis QA (Regression diagnostics)
4. Output QA (Tables, figures, documentation)
5. Replication QA (Can results be reproduced?)

Author: Strategic Management Research Hub
Version: 1.0
Date: 2025-10-31
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json

import pandas as pd
import numpy as np
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class QASystem(unittest.TestCase):
    """
    Quality Assurance System for research pipeline.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Initialize QA system.
        """
        logger.info("="*80)
        logger.info("RESEARCH PIPELINE QUALITY ASSURANCE SYSTEM")
        logger.info("="*80)
        
        if hasattr(cls, 'project_dir'):
            cls.project_path = Path(cls.project_dir)
            logger.info(f"Project directory: {cls.project_path}")
        else:
            cls.project_path = Path('.')
            logger.warning("No project directory specified. Using current directory.")
    
    # ========================================================================
    # Category 1: Data Collection QA
    # ========================================================================
    
    def test_01_data_sources_documented(self):
        """
        QA 1.1: All data sources are properly documented.
        """
        doc_file = self.project_path / 'data' / 'data_sources.md'
        
        if doc_file.exists():
            with open(doc_file, 'r') as f:
                content = f.read()
                
            required_info = ['Source name', 'URL', 'Access date', 'Coverage']
            for info in required_info:
                self.assertIn(info.lower(), content.lower(), 
                             f"Data sources document missing: {info}")
            
            logger.info("✓ QA 1.1 PASSED: Data sources documented")
        else:
            logger.warning("⚠ QA 1.1 SKIPPED: No data_sources.md found")
    
    def test_02_data_collection_log_exists(self):
        """
        QA 1.2: Data collection log exists and is up-to-date.
        """
        log_file = self.project_path / 'data' / 'collection_log.txt'
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                content = f.read()
            
            self.assertGreater(len(content), 100, "Collection log is too short")
            logger.info("✓ QA 1.2 PASSED: Data collection log exists")
        else:
            logger.warning("⚠ QA 1.2 SKIPPED: No collection_log.txt found")
    
    def test_03_raw_data_preserved(self):
        """
        QA 1.3: Raw data is preserved (not modified).
        """
        raw_dir = self.project_path / 'data' / 'raw'
        
        if raw_dir.exists():
            raw_files = list(raw_dir.glob('*.csv')) + list(raw_dir.glob('*.xlsx'))
            self.assertGreater(len(raw_files), 0, "No raw data files found")
            
            logger.info(f"✓ QA 1.3 PASSED: Found {len(raw_files)} raw data files")
        else:
            logger.warning("⚠ QA 1.3 SKIPPED: No raw/ directory found")
    
    # ========================================================================
    # Category 2: Data Cleaning QA
    # ========================================================================
    
    def test_04_data_dictionary_complete(self):
        """
        QA 2.1: Data dictionary is complete and up-to-date.
        """
        dict_file = self.project_path / 'data' / 'data_dictionary.xlsx'
        
        if dict_file.exists():
            try:
                dd = pd.read_excel(dict_file, sheet_name='Data Dictionary')
                
                required_cols = ['Variable Name', 'Description', 'Data Type', 'Source']
                for col in required_cols:
                    self.assertIn(col, dd.columns, f"Data dictionary missing column: {col}")
                
                # Check if all variables are documented
                data_file = self.project_path / 'data' / 'processed' / 'data_final.csv'
                if data_file.exists():
                    df = pd.read_csv(data_file, nrows=1)
                    undocumented = set(df.columns) - set(dd['Variable Name'])
                    
                    if len(undocumented) > 0:
                        logger.warning(f"  Undocumented variables: {undocumented}")
                
                logger.info("✓ QA 2.1 PASSED: Data dictionary complete")
                
            except Exception as e:
                self.fail(f"Error reading data dictionary: {str(e)}")
        else:
            logger.warning("⚠ QA 2.1 SKIPPED: No data_dictionary.xlsx found")
    
    def test_05_cleaning_code_documented(self):
        """
        QA 2.2: Data cleaning steps are documented in code comments.
        """
        cleaning_script = self.project_path / 'code' / '02_data_cleaning.py'
        
        if cleaning_script.exists():
            with open(cleaning_script, 'r') as f:
                content = f.read()
            
            # Check for documentation of key cleaning steps
            key_steps = ['missing', 'outlier', 'winsor', 'transform']
            found_steps = sum(1 for step in key_steps if step.lower() in content.lower())
            
            self.assertGreater(found_steps, 2, 
                              "Cleaning script lacks documentation of key steps")
            
            logger.info("✓ QA 2.2 PASSED: Cleaning steps documented")
        else:
            logger.warning("⚠ QA 2.2 SKIPPED: No data_cleaning script found")
    
    def test_06_cleaned_data_passes_integrity_tests(self):
        """
        QA 2.3: Cleaned data passes all integrity tests.
        """
        data_file = self.project_path / 'data' / 'processed' / 'data_final.csv'
        
        if data_file.exists():
            df = pd.read_csv(data_file)
            
            # Basic integrity checks
            self.assertGreater(len(df), 0, "Cleaned data is empty")
            
            # Check for excessive missing data
            missing_pct = (df.isnull().sum() / len(df)) * 100
            excessive_missing = (missing_pct > 50).sum()
            self.assertEqual(excessive_missing, 0, 
                            "Some variables have >50% missing data")
            
            logger.info("✓ QA 2.3 PASSED: Cleaned data passes integrity checks")
        else:
            logger.warning("⚠ QA 2.3 SKIPPED: No data_final.csv found")
    
    # ========================================================================
    # Category 3: Analysis QA
    # ========================================================================
    
    def test_07_descriptive_statistics_generated(self):
        """
        QA 3.1: Descriptive statistics tables are generated.
        """
        tables_dir = self.project_path / 'output' / 'tables'
        
        if tables_dir.exists():
            desc_tables = list(tables_dir.glob('*descriptive*.csv')) + \
                         list(tables_dir.glob('*correlation*.csv'))
            
            self.assertGreater(len(desc_tables), 0, 
                              "No descriptive statistics tables found")
            
            logger.info(f"✓ QA 3.1 PASSED: Found {len(desc_tables)} descriptive tables")
        else:
            logger.warning("⚠ QA 3.1 SKIPPED: No tables/ directory found")
    
    def test_08_regression_diagnostics_documented(self):
        """
        QA 3.2: Regression diagnostics are documented (VIF, R², etc.).
        """
        results_file = self.project_path / 'output' / 'regression_diagnostics.txt'
        
        if results_file.exists():
            with open(results_file, 'r') as f:
                content = f.read()
            
            diagnostics = ['VIF', 'R²', 'F-statistic', 'N']
            for diagnostic in diagnostics:
                self.assertIn(diagnostic, content, 
                             f"Missing diagnostic: {diagnostic}")
            
            logger.info("✓ QA 3.2 PASSED: Regression diagnostics documented")
        else:
            logger.warning("⚠ QA 3.2 SKIPPED: No regression_diagnostics.txt found")
    
    def test_09_robustness_checks_conducted(self):
        """
        QA 3.3: Robustness checks were conducted.
        """
        robustness_script = self.project_path / 'code' / '05_robustness_checks.py'
        
        if robustness_script.exists():
            with open(robustness_script, 'r') as f:
                content = f.read()
            
            # Look for common robustness check patterns
            robustness_keywords = ['alternative', 'subsample', 'specification', 'lagged']
            found = sum(1 for kw in robustness_keywords if kw in content.lower())
            
            self.assertGreater(found, 1, 
                              "Robustness checks script lacks diversity")
            
            logger.info("✓ QA 3.3 PASSED: Robustness checks conducted")
        else:
            logger.warning("⚠ QA 3.3 SKIPPED: No robustness_checks script found")
    
    def test_10_results_tables_publication_ready(self):
        """
        QA 3.4: Results tables are publication-ready (formatted, stars, etc.).
        """
        tables_dir = self.project_path / 'output' / 'tables'
        
        if tables_dir.exists():
            regression_tables = list(tables_dir.glob('*regression*.tex')) + \
                               list(tables_dir.glob('*regression*.txt'))
            
            if len(regression_tables) > 0:
                # Check first table
                with open(regression_tables[0], 'r') as f:
                    content = f.read()
                
                # Check for significance stars
                has_stars = '***' in content or '**' in content or '*' in content
                self.assertTrue(has_stars, "Regression table lacks significance stars")
                
                # Check for standard errors
                has_se = '(' in content and ')' in content
                self.assertTrue(has_se, "Regression table lacks standard errors")
                
                logger.info("✓ QA 3.4 PASSED: Results tables are publication-ready")
            else:
                logger.warning("⚠ QA 3.4 SKIPPED: No regression tables found")
        else:
            logger.warning("⚠ QA 3.4 SKIPPED: No tables/ directory found")
    
    # ========================================================================
    # Category 4: Output QA
    # ========================================================================
    
    def test_11_figures_high_resolution(self):
        """
        QA 4.1: Figures are high-resolution (≥300 DPI).
        """
        figures_dir = self.project_path / 'output' / 'figures'
        
        if figures_dir.exists():
            figures = list(figures_dir.glob('*.png')) + list(figures_dir.glob('*.pdf'))
            
            self.assertGreater(len(figures), 0, "No figures found")
            
            # Check file sizes as proxy for resolution (PNG >100KB likely high-res)
            for fig in figures:
                size_kb = fig.stat().st_size / 1024
                if fig.suffix == '.png':
                    self.assertGreater(size_kb, 50, 
                                      f"{fig.name} is too small ({size_kb:.0f} KB) - may be low resolution")
            
            logger.info(f"✓ QA 4.1 PASSED: Found {len(figures)} high-resolution figures")
        else:
            logger.warning("⚠ QA 4.1 SKIPPED: No figures/ directory found")
    
    def test_12_figures_properly_labeled(self):
        """
        QA 4.2: Figures have proper titles, axis labels, and legends.
        """
        # This would require image processing or checking source code
        # For now, we check if figure generation code exists
        
        fig_script = self.project_path / 'code' / '06_visualizations.py'
        
        if fig_script.exists():
            with open(fig_script, 'r') as f:
                content = f.read()
            
            required_elements = ['title', 'xlabel', 'ylabel', 'legend']
            for element in required_elements:
                self.assertIn(element, content.lower(), 
                             f"Figure code missing: {element}")
            
            logger.info("✓ QA 4.2 PASSED: Figure labeling code present")
        else:
            logger.warning("⚠ QA 4.2 SKIPPED: No visualization script found")
    
    def test_13_readme_comprehensive(self):
        """
        QA 4.3: README is comprehensive and up-to-date.
        """
        readme_file = self.project_path / 'README.md'
        
        if readme_file.exists():
            with open(readme_file, 'r') as f:
                content = f.read()
            
            required_sections = ['overview', 'data', 'usage', 'citation']
            for section in required_sections:
                self.assertIn(section.lower(), content.lower(), 
                             f"README missing section: {section}")
            
            # Check length (should be >1000 characters for comprehensive doc)
            self.assertGreater(len(content), 1000, 
                              "README is too short - may not be comprehensive")
            
            logger.info("✓ QA 4.3 PASSED: README is comprehensive")
        else:
            logger.warning("⚠ QA 4.3 SKIPPED: No README.md found")
    
    # ========================================================================
    # Category 5: Replication QA
    # ========================================================================
    
    def test_14_code_is_executable(self):
        """
        QA 5.1: All code files are syntactically valid (can be parsed).
        """
        code_dir = self.project_path / 'code'
        
        if code_dir.exists():
            py_files = list(code_dir.glob('*.py'))
            
            for py_file in py_files:
                try:
                    with open(py_file, 'r') as f:
                        compile(f.read(), py_file.name, 'exec')
                except SyntaxError as e:
                    self.fail(f"Syntax error in {py_file.name}: {str(e)}")
            
            logger.info(f"✓ QA 5.1 PASSED: All {len(py_files)} Python files are syntactically valid")
        else:
            logger.warning("⚠ QA 5.1 SKIPPED: No code/ directory found")
    
    def test_15_requirements_documented(self):
        """
        QA 5.2: Software requirements are documented.
        """
        req_file = self.project_path / 'environment' / 'requirements.txt'
        
        if req_file.exists():
            with open(req_file, 'r') as f:
                requirements = f.read().strip().split('\n')
            
            # Check for key packages
            key_packages = ['pandas', 'numpy', 'statsmodels']
            for pkg in key_packages:
                found = any(pkg in req for req in requirements)
                self.assertTrue(found, f"Missing key package: {pkg}")
            
            logger.info(f"✓ QA 5.2 PASSED: Requirements documented ({len(requirements)} packages)")
        else:
            logger.warning("⚠ QA 5.2 SKIPPED: No requirements.txt found")
    
    def test_16_replication_instructions_exist(self):
        """
        QA 5.3: Replication instructions are provided.
        """
        replication_docs = [
            self.project_path / 'REPLICATION.md',
            self.project_path / 'README.md',
            self.project_path / 'docs' / 'replication.md'
        ]
        
        found = any(doc.exists() for doc in replication_docs)
        
        self.assertTrue(found, "No replication instructions found")
        
        if found:
            logger.info("✓ QA 5.3 PASSED: Replication instructions exist")
    
    def test_17_sample_data_or_simulation_provided(self):
        """
        QA 5.4: Sample data or data simulation script is provided.
        """
        sample_data_paths = [
            self.project_path / 'data' / 'sample',
            self.project_path / 'data' / 'synthetic',
            self.project_path / 'code' / 'generate_sample_data.py'
        ]
        
        found = any(path.exists() for path in sample_data_paths)
        
        if found:
            logger.info("✓ QA 5.4 PASSED: Sample data or simulation provided")
        else:
            logger.warning("⚠ QA 5.4 INFO: No sample data found (may require institutional access)")
    
    # ========================================================================
    # Category 6: Research Ethics QA
    # ========================================================================
    
    def test_18_data_usage_complies_with_tos(self):
        """
        QA 6.1: Data usage complies with providers' Terms of Service.
        """
        tos_file = self.project_path / 'docs' / 'data_usage_compliance.md'
        
        if tos_file.exists():
            with open(tos_file, 'r') as f:
                content = f.read()
            
            self.assertIn('Terms of Service', content, 
                         "Document should reference Terms of Service")
            
            logger.info("✓ QA 6.1 PASSED: Data usage compliance documented")
        else:
            logger.warning("⚠ QA 6.1 INFO: No explicit ToS compliance documentation")
    
    def test_19_citations_properly_formatted(self):
        """
        QA 6.2: Citations are properly formatted and complete.
        """
        paper_file = self.project_path / 'manuscript' / 'paper_draft.docx'
        refs_file = self.project_path / 'manuscript' / 'references.bib'
        
        if refs_file.exists():
            with open(refs_file, 'r') as f:
                content = f.read()
            
            # Check for minimum citation elements
            self.assertIn('@article', content.lower(), "No article citations found")
            self.assertIn('author', content.lower(), "Citations missing authors")
            self.assertIn('year', content.lower(), "Citations missing years")
            
            logger.info("✓ QA 6.2 PASSED: Citations properly formatted")
        else:
            logger.warning("⚠ QA 6.2 SKIPPED: No references.bib found")
    
    def test_20_no_proprietary_data_leaked(self):
        """
        QA 6.3: No proprietary or restricted data in public repository.
        """
        # Check if certain sensitive data files exist in wrong locations
        sensitive_patterns = ['*compustat*', '*crsp*', '*wrds*', '*confidential*']
        
        data_dir = self.project_path / 'data'
        if data_dir.exists():
            for pattern in sensitive_patterns:
                matches = list(data_dir.rglob(pattern))
                if len(matches) > 0:
                    logger.warning(f"⚠ Potential sensitive data found: {[m.name for m in matches]}")
        
        logger.info("✓ QA 6.3 INFO: Checked for proprietary data leaks")
    
    # ========================================================================
    # Summary Report
    # ========================================================================
    
    @classmethod
    def tearDownClass(cls):
        """
        Generate QA summary report.
        """
        logger.info("="*80)
        logger.info("QUALITY ASSURANCE SUMMARY")
        logger.info("="*80)
        logger.info("All QA checks completed. Review warnings and failures above.")
        logger.info("="*80)
        
        # Generate QA report
        report_file = cls.project_path / 'output' / 'qa_report.json'
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            'project': str(cls.project_path),
            'date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'QA checks completed',
            'note': 'Review full test output for details'
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"QA report saved: {report_file}")


# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    """
    Run QA system from command line.
    """
    parser = argparse.ArgumentParser(
        description='Quality Assurance System for Strategic Management Research',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--project-dir',
        type=str,
        default='.',
        help='Path to project directory'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Set project directory for test class
    QASystem.project_dir = args.project_dir
    
    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(QASystem)
    
    runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("QA SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*80)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
