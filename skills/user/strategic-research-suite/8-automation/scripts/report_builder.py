"""
report_builder.py

Automated Research Report Generation

This module generates comprehensive, publication-ready research reports
from pipeline results, including tables, figures, and formatted text.

Key Features:
- Markdown report generation
- LaTeX table formatting
- Figure management
- Citation formatting
- Reproducibility documentation

Usage:
    from report_builder import ReportBuilder
    
    builder = ReportBuilder(output_dir='./reports/')
    
    # Add sections
    builder.add_introduction("This study examines...")
    builder.add_table(regression_results, caption="Main Results")
    builder.add_figure('results.png', caption="Performance over time")
    
    # Generate report
    report_path = builder.generate_report()

Version: 4.0
Last Updated: 2025-11-02
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportBuilder:
    """
    Build comprehensive research reports
    
    Attributes:
        output_dir: Output directory for report
        sections: List of report sections
        tables: Dictionary of tables
        figures: Dictionary of figures
        citations: List of citations
    """
    
    def __init__(self, output_dir: str = './reports/', title: str = "Research Report"):
        """
        Initialize report builder
        
        Args:
            output_dir: Directory for output files
            title: Report title
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.title = title
        self.sections = []
        self.tables = {}
        self.figures = {}
        self.citations = []
        self.metadata = {
            'created': datetime.now().isoformat(),
            'title': title
        }
        
        logger.info(f"ReportBuilder initialized: {output_dir}")
    
    # =========================================================================
    # Section Management
    # =========================================================================
    
    def add_section(self, title: str, content: str, level: int = 2):
        """
        Add a section to report
        
        Args:
            title: Section title
            content: Section content (markdown)
            level: Heading level (1-6)
        """
        section = {
            'title': title,
            'content': content,
            'level': level,
            'timestamp': datetime.now().isoformat()
        }
        
        self.sections.append(section)
        logger.info(f"Added section: {title}")
    
    def add_introduction(self, content: str):
        """Add introduction section"""
        self.add_section("Introduction", content, level=2)
    
    def add_methods(self, content: str):
        """Add methods section"""
        self.add_section("Methods", content, level=2)
    
    def add_results(self, content: str):
        """Add results section"""
        self.add_section("Results", content, level=2)
    
    def add_discussion(self, content: str):
        """Add discussion section"""
        self.add_section("Discussion", content, level=2)
    
    def add_conclusion(self, content: str):
        """Add conclusion section"""
        self.add_section("Conclusion", content, level=2)
    
    # =========================================================================
    # Table Management
    # =========================================================================
    
    def add_table(self, 
                 table: Union[pd.DataFrame, Dict],
                 name: str,
                 caption: str = "",
                 format: str = 'markdown') -> str:
        """
        Add table to report
        
        Args:
            table: DataFrame or dictionary
            name: Table identifier (e.g., "table1")
            caption: Table caption
            format: Output format ('markdown', 'latex', 'html')
        
        Returns:
            Table reference string
        """
        if isinstance(table, dict):
            table = pd.DataFrame(table)
        
        table_data = {
            'name': name,
            'caption': caption,
            'data': table,
            'format': format,
            'timestamp': datetime.now().isoformat()
        }
        
        self.tables[name] = table_data
        
        # Save table file
        if format == 'markdown':
            table_file = self.output_dir / f'{name}.md'
            with open(table_file, 'w') as f:
                f.write(f"**{caption}**\n\n")
                f.write(table.to_markdown(index=True))
        elif format == 'latex':
            table_file = self.output_dir / f'{name}.tex'
            with open(table_file, 'w') as f:
                f.write(table.to_latex(index=True, caption=caption))
        elif format == 'csv':
            table_file = self.output_dir / f'{name}.csv'
            table.to_csv(table_file)
        
        logger.info(f"Added table: {name} ({format})")
        
        return f"[Table: {name}]"
    
    def add_regression_table(self, 
                           results_list: List[Any],
                           name: str = "regression_results",
                           caption: str = "Regression Results",
                           model_names: Optional[List[str]] = None) -> str:
        """
        Add regression results table
        
        Args:
            results_list: List of regression results (statsmodels/linearmodels)
            name: Table identifier
            caption: Table caption
            model_names: Optional list of model names
        
        Returns:
            Table reference string
        """
        # Extract key statistics
        table_data = []
        
        for i, result in enumerate(results_list):
            model_name = model_names[i] if model_names else f"Model {i+1}"
            
            # Extract coefficients and statistics
            if hasattr(result, 'params'):
                params = result.params
                pvalues = result.pvalues
                
                for var in params.index:
                    table_data.append({
                        'model': model_name,
                        'variable': var,
                        'coefficient': params[var],
                        'p_value': pvalues[var],
                        'significance': self._get_significance_stars(pvalues[var])
                    })
        
        df = pd.DataFrame(table_data)
        
        # Pivot to wide format
        df_wide = df.pivot(index='variable', columns='model', values='coefficient')
        
        return self.add_table(df_wide, name, caption, format='markdown')
    
    @staticmethod
    def _get_significance_stars(p_value: float) -> str:
        """Get significance stars for p-value"""
        if p_value < 0.001:
            return '***'
        elif p_value < 0.01:
            return '**'
        elif p_value < 0.05:
            return '*'
        else:
            return ''
    
    def add_descriptive_statistics(self,
                                  df: pd.DataFrame,
                                  name: str = "descriptive_stats",
                                  caption: str = "Descriptive Statistics") -> str:
        """
        Add descriptive statistics table
        
        Args:
            df: DataFrame with data
            name: Table identifier
            caption: Table caption
        
        Returns:
            Table reference string
        """
        desc_stats = df.describe().T
        desc_stats['missing'] = df.isnull().sum()
        desc_stats['missing_pct'] = (df.isnull().sum() / len(df) * 100).round(2)
        
        # Round numeric columns
        numeric_cols = desc_stats.select_dtypes(include=[np.number]).columns
        desc_stats[numeric_cols] = desc_stats[numeric_cols].round(3)
        
        return self.add_table(desc_stats, name, caption, format='markdown')
    
    # =========================================================================
    # Figure Management
    # =========================================================================
    
    def add_figure(self, 
                  filepath: Union[str, Path],
                  name: str,
                  caption: str = "",
                  alt_text: str = "") -> str:
        """
        Add figure to report
        
        Args:
            filepath: Path to figure file
            name: Figure identifier
            caption: Figure caption
            alt_text: Alternative text for accessibility
        
        Returns:
            Figure reference string
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            logger.warning(f"Figure file not found: {filepath}")
            return f"[Figure: {name} - FILE NOT FOUND]"
        
        figure_data = {
            'name': name,
            'filepath': str(filepath),
            'caption': caption,
            'alt_text': alt_text or caption,
            'timestamp': datetime.now().isoformat()
        }
        
        self.figures[name] = figure_data
        
        logger.info(f"Added figure: {name}")
        
        return f"[Figure: {name}]"
    
    # =========================================================================
    # Citation Management
    # =========================================================================
    
    def add_citation(self, 
                    authors: str,
                    year: int,
                    title: str,
                    journal: str = "",
                    volume: str = "",
                    pages: str = "",
                    doi: str = "") -> str:
        """
        Add citation to bibliography
        
        Args:
            authors: Author names (e.g., "Smith, J. and Doe, J.")
            year: Publication year
            title: Article title
            journal: Journal name
            volume: Volume number
            pages: Page range
            doi: DOI
        
        Returns:
            Citation key
        """
        # Generate citation key (first author + year)
        first_author = authors.split(',')[0].split()[-1]
        citation_key = f"{first_author}{year}"
        
        citation = {
            'key': citation_key,
            'authors': authors,
            'year': year,
            'title': title,
            'journal': journal,
            'volume': volume,
            'pages': pages,
            'doi': doi
        }
        
        self.citations.append(citation)
        
        return citation_key
    
    def format_citation(self, citation_key: str) -> str:
        """Format citation for inline use"""
        citation = next((c for c in self.citations if c['key'] == citation_key), None)
        
        if citation:
            return f"({citation['authors'].split(',')[0].split()[-1]}, {citation['year']})"
        else:
            return f"({citation_key})"
    
    # =========================================================================
    # Report Generation
    # =========================================================================
    
    def generate_report(self, 
                       filename: str = "research_report.md",
                       include_metadata: bool = True) -> str:
        """
        Generate complete research report
        
        Args:
            filename: Output filename
            include_metadata: Include metadata section
        
        Returns:
            Path to generated report
        """
        logger.info("Generating research report...")
        
        report_path = self.output_dir / filename
        
        with open(report_path, 'w') as f:
            # Title
            f.write(f"# {self.title}\n\n")
            
            # Metadata
            if include_metadata:
                f.write("---\n\n")
                f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
                f.write(f"**Report Type**: Research Report  \n")
                f.write("\n---\n\n")
            
            # Table of Contents
            if len(self.sections) > 0:
                f.write("## Table of Contents\n\n")
                for i, section in enumerate(self.sections, 1):
                    f.write(f"{i}. [{section['title']}](#{section['title'].lower().replace(' ', '-')})\n")
                f.write("\n---\n\n")
            
            # Sections
            for section in self.sections:
                heading = '#' * section['level']
                f.write(f"{heading} {section['title']}\n\n")
                f.write(f"{section['content']}\n\n")
            
            # Tables
            if self.tables:
                f.write("## Tables\n\n")
                for name, table_data in self.tables.items():
                    f.write(f"### {table_data['caption']}\n\n")
                    f.write(table_data['data'].to_markdown(index=True))
                    f.write("\n\n")
            
            # Figures
            if self.figures:
                f.write("## Figures\n\n")
                for name, figure_data in self.figures.items():
                    f.write(f"### {figure_data['caption']}\n\n")
                    f.write(f"![{figure_data['alt_text']}]({figure_data['filepath']})\n\n")
                    f.write(f"*{figure_data['caption']}*\n\n")
            
            # Bibliography
            if self.citations:
                f.write("## References\n\n")
                for citation in sorted(self.citations, key=lambda x: (x['authors'], x['year'])):
                    f.write(self._format_apa_citation(citation))
                    f.write("\n\n")
        
        logger.info(f"✓ Report generated: {report_path}")
        
        return str(report_path)
    
    def _format_apa_citation(self, citation: Dict) -> str:
        """Format citation in APA style"""
        parts = [
            f"{citation['authors']} ({citation['year']}).",
            f"*{citation['title']}*."
        ]
        
        if citation['journal']:
            journal_part = f"*{citation['journal']}*"
            if citation['volume']:
                journal_part += f", {citation['volume']}"
            if citation['pages']:
                journal_part += f", {citation['pages']}"
            parts.append(journal_part + ".")
        
        if citation['doi']:
            parts.append(f"https://doi.org/{citation['doi']}")
        
        return " ".join(parts)
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate report summary
        
        Returns:
            Dictionary with report statistics
        """
        return {
            'title': self.title,
            'sections': len(self.sections),
            'tables': len(self.tables),
            'figures': len(self.figures),
            'citations': len(self.citations),
            'created': self.metadata['created']
        }
    
    # =========================================================================
    # Export Methods
    # =========================================================================
    
    def export_to_latex(self, filename: str = "report.tex") -> str:
        """
        Export report to LaTeX format
        
        Args:
            filename: Output filename
        
        Returns:
            Path to LaTeX file
        """
        latex_path = self.output_dir / filename
        
        with open(latex_path, 'w') as f:
            # Document class and packages
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{booktabs}\n")
            f.write("\\usepackage{graphicx}\n")
            f.write("\\usepackage{hyperref}\n\n")
            
            f.write("\\begin{document}\n\n")
            
            # Title
            f.write(f"\\title{{{self.title}}}\n")
            f.write("\\maketitle\n\n")
            
            # Sections
            for section in self.sections:
                if section['level'] == 2:
                    f.write(f"\\section{{{section['title']}}}\n\n")
                elif section['level'] == 3:
                    f.write(f"\\subsection{{{section['title']}}}\n\n")
                
                f.write(f"{section['content']}\n\n")
            
            f.write("\\end{document}\n")
        
        logger.info(f"✓ LaTeX exported: {latex_path}")
        
        return str(latex_path)


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("REPORT BUILDER DEMO")
    print("=" * 80)
    
    # Initialize builder
    builder = ReportBuilder(
        output_dir='./demo_report/',
        title="The Impact of R&D Investment on Firm Performance"
    )
    
    # Add sections
    builder.add_introduction(
        "This study examines the relationship between R&D investment intensity "
        "and firm financial performance using panel data from 2015-2022."
    )
    
    builder.add_methods(
        "We employ panel fixed effects regression to estimate the effect of "
        "lagged R&D intensity on return on assets (ROA), controlling for "
        "firm size, leverage, and industry-year fixed effects."
    )
    
    # Add sample table
    desc_stats = pd.DataFrame({
        'Variable': ['ROA', 'R&D Intensity', 'Firm Size', 'Leverage'],
        'Mean': [0.08, 0.05, 12.5, 0.35],
        'Std': [0.12, 0.04, 1.8, 0.22],
        'Min': [-0.20, 0.00, 8.2, 0.05],
        'Max': [0.45, 0.25, 16.3, 0.85]
    }).set_index('Variable')
    
    builder.add_table(
        desc_stats,
        name='descriptive_stats',
        caption='Descriptive Statistics',
        format='markdown'
    )
    
    builder.add_results(
        "The regression results show a positive and statistically significant "
        "relationship between R&D intensity and ROA (β = 0.45, p < 0.01). "
        "This suggests that firms investing more in R&D tend to achieve "
        "higher financial performance."
    )
    
    builder.add_conclusion(
        "Our findings support the hypothesis that R&D investment positively "
        "affects firm performance. The results have important implications "
        "for strategic management and innovation policy."
    )
    
    # Add citation
    builder.add_citation(
        authors="Smith, J. and Doe, J.",
        year=2020,
        title="R&D and Firm Performance: A Meta-Analysis",
        journal="Strategic Management Journal",
        volume="41",
        pages="1234-1250",
        doi="10.1002/smj.12345"
    )
    
    # Generate report
    report_path = builder.generate_report()
    
    # Show summary
    summary = builder.generate_summary()
    print("\n" + "=" * 80)
    print("REPORT SUMMARY")
    print("=" * 80)
    print(f"Title: {summary['title']}")
    print(f"Sections: {summary['sections']}")
    print(f"Tables: {summary['tables']}")
    print(f"Figures: {summary['figures']}")
    print(f"Citations: {summary['citations']}")
    print(f"\nReport saved: {report_path}")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETED")
    print("=" * 80)
