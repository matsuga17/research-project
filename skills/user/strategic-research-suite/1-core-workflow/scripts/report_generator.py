"""
report_generator.py

Comprehensive Report Generator for Strategic Management Research

This module generates publication-ready research reports including:
- Executive summaries
- Methodology descriptions
- Results tables and figures
- Discussion and implications
- Appendices

Usage:
    from report_generator import ResearchReportGenerator
    
    generator = ResearchReportGenerator(
        research_question="How does R&D affect performance?",
        results_dir="./output/"
    )
    
    report = generator.generate_full_report()
    generator.save_report(report, "final_report.md")
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class ResearchReportGenerator:
    """
    Generate comprehensive research reports from pipeline results
    
    Attributes:
        research_question: Main research question
        results_dir: Directory containing pipeline results
        report_sections: Dictionary of report sections
    """
    
    def __init__(self, research_question: str, results_dir: str):
        """
        Initialize the report generator
        
        Args:
            research_question: Main research question
            results_dir: Path to directory with pipeline results
        """
        self.research_question = research_question
        self.results_dir = Path(results_dir)
        self.report_sections = {}
        
        # Load results from pipeline phases
        self._load_phase_results()
    
    def _load_phase_results(self):
        """Load results from all pipeline phases"""
        # Phase 1: Research Design
        phase1_file = self.results_dir / 'phase1_research_design.json'
        if phase1_file.exists():
            with open(phase1_file, 'r') as f:
                self.phase1_results = json.load(f)
        else:
            self.phase1_results = {}
        
        # Phase 3: Sample Statistics
        phase3_file = self.results_dir / 'phase3_sample_stats.json'
        if phase3_file.exists():
            with open(phase3_file, 'r') as f:
                self.phase3_results = json.load(f)
        else:
            self.phase3_results = {}
        
        # Phase 7: Statistical Results
        phase7_file = self.results_dir / 'phase7_regression_results.json'
        if phase7_file.exists():
            with open(phase7_file, 'r') as f:
                self.phase7_results = json.load(f)
        else:
            self.phase7_results = {}
        
        # Load descriptive statistics
        desc_file = self.results_dir / 'phase7_descriptive_stats.csv'
        if desc_file.exists():
            self.desc_stats = pd.read_csv(desc_file, index_col=0)
        else:
            self.desc_stats = None
        
        # Load correlation matrix
        corr_file = self.results_dir / 'phase7_correlation_matrix.csv'
        if corr_file.exists():
            self.corr_matrix = pd.read_csv(corr_file, index_col=0)
        else:
            self.corr_matrix = None

    
    def generate_full_report(self, format: str = 'markdown') -> str:
        """
        Generate complete research report
        
        Args:
            format: Output format ('markdown', 'html', or 'latex')
        
        Returns:
            Full report as string
        """
        if format == 'markdown':
            return self._generate_markdown_report()
        elif format == 'html':
            return self._generate_html_report()
        elif format == 'latex':
            return self._generate_latex_report()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown format report"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        report = f"""# Strategic Management Research Report

**Date**: {timestamp}  
**Research Question**: {self.research_question}

---

## Abstract

This study investigates {self.research_question.lower()} using panel data analysis. 
We construct a sample of {self.phase3_results.get('total_firms', 'N/A')} firms over 
{self.phase3_results.get('year_range', 'N/A')} years, resulting in 
{self.phase3_results.get('total_observations', 'N/A'):,} observations. 

**Key findings**: {self._summarize_key_findings()}

---

## 1. Introduction

### 1.1 Research Question

{self.research_question}

### 1.2 Theoretical Framework

**Theoretical lens**: {self.phase1_results.get('theoretical_framework', 'To be specified')}

### 1.3 Hypotheses

"""
        
        # Add hypotheses
        for i, hyp in enumerate(self.phase1_results.get('hypotheses', []), 1):
            report += f"**H{i}**: {hyp}\n\n"
        
        report += """
---

## 2. Methodology

### 2.1 Sample Construction

"""
        
        # Add sample details
        if self.phase3_results:
            report += f"""- **Total observations**: {self.phase3_results.get('total_observations', 'N/A'):,}
- **Total firms**: {self.phase3_results.get('total_firms', 'N/A'):,}
- **Time period**: {self.phase3_results.get('year_range', ['N/A', 'N/A'])[0]}-{self.phase3_results.get('year_range', ['N/A', 'N/A'])[1]}
- **Average observations per firm**: {self.phase3_results.get('avg_observations_per_firm', 0):.2f}
"""
        
        report += """
### 2.2 Variables

"""
        
        # Add variable definitions
        if 'variables' in self.phase1_results:
            vars_def = self.phase1_results['variables']
            report += f"""**Dependent Variable(s)**:
- {', '.join(vars_def.get('dependent', []))}

**Independent Variable(s)**:
- {', '.join(vars_def.get('independent', []))}

**Control Variables**:
- {', '.join(vars_def.get('control', []))}
"""
        
        report += """
### 2.3 Analytical Method

Panel data regression with firm and year fixed effects.

---

## 3. Results

### 3.1 Descriptive Statistics

"""
        
        # Add descriptive statistics table
        if self.desc_stats is not None:
            report += self._format_table_markdown(self.desc_stats, "Descriptive Statistics")
        
        report += """
### 3.2 Correlation Matrix

"""
        
        # Add correlation matrix
        if self.corr_matrix is not None:
            report += self._format_table_markdown(self.corr_matrix, "Correlation Matrix")
        
        report += """
### 3.3 Regression Results

"""
        
        # Add regression results
        if self.phase7_results:
            report += f"""**Model**: {self.phase7_results.get('model', 'N/A')}

**Dependent Variable**: {self.phase7_results.get('dependent_variable', 'N/A')}

**Key coefficient**:
- {self.phase7_results.get('independent_variable', 'N/A')}: {self.phase7_results.get('coefficient', 'N/A'):.4f}

Note: {self.phase7_results.get('note', '')}
"""
        
        report += """
---

## 4. Discussion

### 4.1 Key Findings

"""
        
        report += self._generate_discussion()
        
        report += """
### 4.2 Theoretical Implications

[To be developed based on specific findings]

### 4.3 Managerial Implications

[To be developed based on specific findings]

### 4.4 Limitations

- Sample limited to available data sources
- Endogeneity concerns require further robustness checks
- Generalizability to other contexts needs investigation

---

## 5. Conclusion

This study provides evidence regarding {self.research_question.lower()}. 
The findings contribute to the literature on strategic management and have 
implications for both theory and practice.

---

## References

[References to be added]

---

## Appendices

### Appendix A: Data Sources

See `phase2_data_sources.json` for complete list of data sources.

### Appendix B: Variable Definitions

See `phase6_variable_definitions.json` for detailed variable definitions.

### Appendix C: Robustness Checks

[To be added]

---

**Report generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Pipeline output directory**: {self.results_dir}
"""
        
        return report

    
    def _summarize_key_findings(self) -> str:
        """Generate key findings summary"""
        if not self.phase7_results:
            return "Statistical analysis in progress."
        
        coef = self.phase7_results.get('coefficient', 0)
        if coef > 0:
            direction = "positively associated with"
        elif coef < 0:
            direction = "negatively associated with"
        else:
            direction = "not significantly associated with"
        
        iv = self.phase7_results.get('independent_variable', 'the independent variable')
        dv = self.phase7_results.get('dependent_variable', 'the dependent variable')
        
        return f"{iv.upper()} is {direction} {dv.upper()} (β = {coef:.4f})."
    
    def _generate_discussion(self) -> str:
        """Generate discussion section"""
        findings = self._summarize_key_findings()
        
        discussion = f"""The analysis reveals that {findings}

This finding supports the theoretical argument that [elaborate based on specific results].

**Implications for theory**:
- Contributes to understanding of [specify theoretical contribution]
- Extends prior research by [specify extension]

**Implications for practice**:
- Managers should consider [specify practical implication]
- Organizations can benefit from [specify benefit]
"""
        
        return discussion
    
    def _format_table_markdown(self, df: pd.DataFrame, title: str) -> str:
        """Format DataFrame as markdown table"""
        table = f"\n**Table: {title}**\n\n"
        table += df.to_markdown() + "\n\n"
        return table
    
    def _generate_html_report(self) -> str:
        """Generate HTML format report"""
        # Convert markdown to HTML (simplified version)
        md_report = self._generate_markdown_report()
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Research Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; }}
        h2 {{ color: #34495e; border-bottom: 1px solid #95a5a6; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        .abstract {{ background-color: #ecf0f1; padding: 15px; border-left: 4px solid #3498db; }}
    </style>
</head>
<body>
    <pre>{md_report}</pre>
</body>
</html>
"""
        
        return html
    
    def _generate_latex_report(self) -> str:
        """Generate LaTeX format report"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        latex = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{booktabs}
\usepackage{hyperref}

\title{Strategic Management Research Report}
\author{[Author Name]}
\date{""" + timestamp + r"""}

\begin{document}

\maketitle

\begin{abstract}
""" + f"This study investigates {self.research_question.lower()}." + r"""
\end{abstract}

\section{Introduction}
""" + f"{self.research_question}" + r"""

\section{Methodology}
Panel data analysis with fixed effects.

\section{Results}
[Results tables to be inserted]

\section{Discussion}
[Discussion to be developed]

\section{Conclusion}
[Conclusion to be developed]

\end{document}
"""
        
        return latex
    
    def save_report(self, report: str, filename: str, output_dir: Optional[str] = None):
        """
        Save report to file
        
        Args:
            report: Report content
            filename: Output filename
            output_dir: Output directory (defaults to results_dir)
        """
        if output_dir:
            save_path = Path(output_dir) / filename
        else:
            save_path = self.results_dir / filename
        
        with open(save_path, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved to: {save_path}")
        return save_path


# ==================== Command Line Interface ====================

def main():
    """Command line interface for report generation"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate research report from pipeline results'
    )
    parser.add_argument(
        '--question',
        type=str,
        required=True,
        help='Research question'
    )
    parser.add_argument(
        '--results-dir',
        type=str,
        required=True,
        help='Directory containing pipeline results'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='research_report.md',
        help='Output filename'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['markdown', 'html', 'latex'],
        default='markdown',
        help='Report format'
    )
    
    args = parser.parse_args()
    
    # Generate report
    generator = ResearchReportGenerator(
        research_question=args.question,
        results_dir=args.results_dir
    )
    
    report = generator.generate_full_report(format=args.format)
    
    # Adjust filename extension based on format
    if args.format == 'html' and not args.output.endswith('.html'):
        output_file = args.output.replace('.md', '.html')
    elif args.format == 'latex' and not args.output.endswith('.tex'):
        output_file = args.output.replace('.md', '.tex')
    else:
        output_file = args.output
    
    generator.save_report(report, output_file)
    
    print(f"\n✓ Report generation completed!")
    print(f"  Format: {args.format}")
    print(f"  Output: {output_file}")


if __name__ == "__main__":
    main()
