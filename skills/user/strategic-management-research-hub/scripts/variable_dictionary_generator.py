"""
Strategic Management Research Hub - Variable Dictionary Generator
==================================================================

Automatic generation of variable dictionaries for research reproducibility.

Creates standardized documentation in multiple formats:
- Excel workbook (editable)
- LaTeX table (for papers)
- Markdown (for README)
- JSON (for programmatic access)

Author: Strategic Management Research Hub
Version: 3.0
License: MIT
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Union
import json
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VariableDictionaryGenerator:
    """
    Generate comprehensive variable dictionaries for research projects.
    
    Usage:
    ```python
    generator = VariableDictionaryGenerator(df_panel)
    
    # Classify variables
    generator.classify_variables(
        dependent=['roa', 'roe'],
        independent=['rd_intensity'],
        moderators=['env_dynamism'],
        controls=['firm_size', 'leverage', 'firm_age']
    )
    
    # Generate documentation
    generator.generate_excel('data_dictionary.xlsx')
    generator.generate_latex('variables_table.tex')
    generator.generate_markdown('VARIABLES.md')
    ```
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize dictionary generator.
        
        Args:
            data: Panel DataFrame
        """
        self.data = data
        self.variable_info = {}
        self.classifications = {}
        
        logger.info(f"Dictionary Generator initialized: {data.shape[1]} variables")
    
    def classify_variables(
        self,
        dependent: Optional[List[str]] = None,
        independent: Optional[List[str]] = None,
        moderators: Optional[List[str]] = None,
        mediators: Optional[List[str]] = None,
        controls: Optional[List[str]] = None,
        identifiers: Optional[List[str]] = None
    ):
        """
        Classify variables by role in analysis.
        
        Args:
            dependent: Dependent variables
            independent: Independent variables
            moderators: Moderator variables
            mediators: Mediator variables
            controls: Control variables
            identifiers: ID variables (firm_id, year, etc.)
        """
        self.classifications = {
            'Dependent Variable': dependent or [],
            'Independent Variable': independent or [],
            'Moderator': moderators or [],
            'Mediator': mediators or [],
            'Control Variable': controls or [],
            'Identifier': identifiers or []
        }
        
        # Validate all variables exist
        all_vars = sum(self.classifications.values(), [])
        missing = set(all_vars) - set(self.data.columns)
        
        if missing:
            logger.warning(f"Variables not found in data: {missing}")
        
        logger.info(f"Classified {len(all_vars)} variables")
    
    def auto_detect_types(self):
        """
        Automatically detect variable types and characteristics.
        """
        for col in self.data.columns:
            var_info = {
                'variable_name': col,
                'dtype': str(self.data[col].dtype),
                'n_obs': int(self.data[col].notna().sum()),
                'n_missing': int(self.data[col].isna().sum()),
                'missing_rate': float(self.data[col].isna().mean())
            }
            
            # Type-specific statistics
            if pd.api.types.is_numeric_dtype(self.data[col]):
                var_info.update({
                    'mean': float(self.data[col].mean()),
                    'std': float(self.data[col].std()),
                    'min': float(self.data[col].min()),
                    'p25': float(self.data[col].quantile(0.25)),
                    'median': float(self.data[col].median()),
                    'p75': float(self.data[col].quantile(0.75)),
                    'max': float(self.data[col].max()),
                    'n_unique': int(self.data[col].nunique())
                })
                
                # Detect binary variables
                if self.data[col].nunique() == 2:
                    var_info['variable_type'] = 'Binary'
                # Detect categorical (few unique values)
                elif self.data[col].nunique() < 20:
                    var_info['variable_type'] = 'Categorical'
                else:
                    var_info['variable_type'] = 'Continuous'
            
            elif pd.api.types.is_string_dtype(self.data[col]) or \
                 pd.api.types.is_object_dtype(self.data[col]):
                var_info.update({
                    'n_unique': int(self.data[col].nunique()),
                    'variable_type': 'Categorical/String',
                    'most_common': str(self.data[col].mode()[0]) if len(self.data[col].mode()) > 0 else None
                })
            
            # Determine role (if not classified)
            if col not in sum(self.classifications.values(), []):
                role = self._infer_variable_role(col)
                var_info['role'] = role
            else:
                # Find role from classifications
                for role, vars_list in self.classifications.items():
                    if col in vars_list:
                        var_info['role'] = role
                        break
            
            self.variable_info[col] = var_info
        
        logger.info(f"Auto-detected types for {len(self.variable_info)} variables")
    
    def _infer_variable_role(self, col_name: str) -> str:
        """Infer variable role from name pattern"""
        col_lower = col_name.lower()
        
        # Common ID patterns
        if any(x in col_lower for x in ['id', 'gvkey', 'permno', 'cik', 'cusip']):
            return 'Identifier'
        
        # Time variables
        if any(x in col_lower for x in ['year', 'date', 'time', 'period']):
            return 'Identifier'
        
        # Common DVs
        if any(x in col_lower for x in ['roa', 'roe', 'performance', 'profit', 'return']):
            return 'Dependent Variable (inferred)'
        
        # Common controls
        if any(x in col_lower for x in ['size', 'age', 'leverage', 'cash']):
            return 'Control Variable (inferred)'
        
        return 'Unclassified'
    
    def add_descriptions(self, descriptions: Dict[str, str]):
        """
        Add manual descriptions for variables.
        
        Args:
            descriptions: Dict mapping variable names to descriptions
        """
        for var, desc in descriptions.items():
            if var in self.variable_info:
                self.variable_info[var]['description'] = desc
            else:
                logger.warning(f"Variable '{var}' not found")
        
        logger.info(f"Added descriptions for {len(descriptions)} variables")
    
    def add_sources(self, sources: Dict[str, str]):
        """
        Add data sources for variables.
        
        Args:
            sources: Dict mapping variable names to source descriptions
        """
        for var, source in sources.items():
            if var in self.variable_info:
                self.variable_info[var]['source'] = source
            else:
                logger.warning(f"Variable '{var}' not found")
        
        logger.info(f"Added sources for {len(sources)} variables")
    
    def add_formulas(self, formulas: Dict[str, str]):
        """
        Add calculation formulas for variables.
        
        Args:
            formulas: Dict mapping variable names to formula strings
        """
        for var, formula in formulas.items():
            if var in self.variable_info:
                self.variable_info[var]['formula'] = formula
            else:
                logger.warning(f"Variable '{var}' not found")
        
        logger.info(f"Added formulas for {len(formulas)} variables")
    
    def generate_excel(self, output_path: str):
        """
        Generate Excel workbook with variable dictionary.
        
        Args:
            output_path: Path to save Excel file
        """
        df_dict = pd.DataFrame.from_dict(self.variable_info, orient='index')
        
        # Reorder columns
        col_order = [
            'variable_name', 'role', 'variable_type', 'description',
            'formula', 'source', 'n_obs', 'n_missing', 'missing_rate',
            'mean', 'std', 'min', 'p25', 'median', 'p75', 'max',
            'n_unique', 'dtype'
        ]
        
        # Only include columns that exist
        col_order = [c for c in col_order if c in df_dict.columns]
        df_dict = df_dict[col_order]
        
        # Create Excel with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_dict.to_excel(writer, sheet_name='Data Dictionary', index=False)
            
            # Format worksheet
            worksheet = writer.sheets['Data Dictionary']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = max(len(str(cell.value or '')) for cell in column)
                worksheet.column_dimensions[column[0].column_letter].width = min(max_length + 2, 50)
            
            # Bold headers
            for cell in worksheet[1]:
                cell.font = cell.font.copy(bold=True)
        
        logger.info(f"Excel dictionary saved: {output_path}")
    
    def generate_latex(self, output_path: str, caption: str = "Variable Definitions"):
        """
        Generate LaTeX table of variable definitions.
        
        Args:
            output_path: Path to save .tex file
            caption: Table caption
        """
        df_dict = pd.DataFrame.from_dict(self.variable_info, orient='index')
        
        # Select key columns for paper
        cols = ['variable_name', 'role', 'description', 'mean', 'std']
        cols = [c for c in cols if c in df_dict.columns]
        df_latex = df_dict[cols].copy()
        
        # Format numbers
        if 'mean' in df_latex.columns:
            df_latex['mean'] = df_latex['mean'].apply(lambda x: f"{x:.3f}" if pd.notna(x) else "")
        if 'std' in df_latex.columns:
            df_latex['std'] = df_latex['std'].apply(lambda x: f"{x:.3f}" if pd.notna(x) else "")
        
        # Rename columns for display
        df_latex.columns = ['Variable', 'Role', 'Description', 'Mean', 'S.D.']
        
        # Generate LaTeX
        latex_str = df_latex.to_latex(
            index=False,
            caption=caption,
            label='tab:variables',
            escape=False,
            column_format='l' * len(df_latex.columns)
        )
        
        # Add table formatting
        latex_str = latex_str.replace(r'\begin{table}', r'\begin{table}[htbp]\centering\small')
        latex_str = latex_str.replace(r'\toprule', r'\hline\hline')
        latex_str = latex_str.replace(r'\midrule', r'\hline')
        latex_str = latex_str.replace(r'\bottomrule', r'\hline\hline')
        
        with open(output_path, 'w') as f:
            f.write(latex_str)
        
        logger.info(f"LaTeX table saved: {output_path}")
    
    def generate_markdown(self, output_path: str):
        """
        Generate Markdown variable dictionary.
        
        Args:
            output_path: Path to save .md file
        """
        md_content = "# Variable Dictionary\n\n"
        md_content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        md_content += f"Total Variables: {len(self.variable_info)}\n\n"
        
        # Group by role
        for role in ['Dependent Variable', 'Independent Variable', 'Moderator',
                     'Mediator', 'Control Variable', 'Identifier']:
            
            vars_in_role = [v for v, info in self.variable_info.items() 
                           if info.get('role') == role]
            
            if not vars_in_role:
                continue
            
            md_content += f"## {role}s\n\n"
            
            for var in vars_in_role:
                info = self.variable_info[var]
                md_content += f"### {var}\n\n"
                
                # Description
                if 'description' in info:
                    md_content += f"**Description:** {info['description']}\n\n"
                
                # Formula
                if 'formula' in info:
                    md_content += f"**Formula:** `{info['formula']}`\n\n"
                
                # Source
                if 'source' in info:
                    md_content += f"**Source:** {info['source']}\n\n"
                
                # Statistics (if numeric)
                if 'mean' in info:
                    md_content += f"**Statistics:**\n"
                    md_content += f"- N: {info['n_obs']}\n"
                    md_content += f"- Mean: {info['mean']:.3f}\n"
                    md_content += f"- Std: {info['std']:.3f}\n"
                    md_content += f"- Range: [{info['min']:.3f}, {info['max']:.3f}]\n"
                    md_content += f"- Missing: {info['missing_rate']*100:.1f}%\n\n"
                
                md_content += "---\n\n"
        
        with open(output_path, 'w') as f:
            f.write(md_content)
        
        logger.info(f"Markdown dictionary saved: {output_path}")
    
    def generate_json(self, output_path: str):
        """
        Generate JSON variable dictionary.
        
        Args:
            output_path: Path to save .json file
        """
        # Convert numpy types to native Python types
        json_data = {}
        for var, info in self.variable_info.items():
            json_data[var] = {k: (v.item() if isinstance(v, np.generic) else v) 
                             for k, v in info.items()}
        
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        logger.info(f"JSON dictionary saved: {output_path}")
    
    def validate_consistency(self) -> Dict[str, List[str]]:
        """
        Validate variable consistency.
        
        Returns:
            Dictionary of validation warnings
        """
        warnings = {
            'high_missing': [],
            'low_variance': [],
            'potential_errors': []
        }
        
        for var, info in self.variable_info.items():
            # High missing rate
            if info.get('missing_rate', 0) > 0.3:
                warnings['high_missing'].append(
                    f"{var}: {info['missing_rate']*100:.1f}% missing"
                )
            
            # Low variance (potential constant)
            if 'std' in info and info['std'] < 0.001:
                warnings['low_variance'].append(
                    f"{var}: Very low variance (SD={info['std']:.6f})"
                )
            
            # Potential data errors (outliers)
            if 'max' in info and 'mean' in info and 'std' in info:
                if abs(info['max'] - info['mean']) > 10 * info['std']:
                    warnings['potential_errors'].append(
                        f"{var}: Extreme outlier detected (max={info['max']:.2f})"
                    )
        
        # Print warnings
        if any(warnings.values()):
            logger.warning("Validation warnings detected:")
            for category, msgs in warnings.items():
                if msgs:
                    logger.warning(f"  {category}: {len(msgs)} issues")
        else:
            logger.info("✓ Validation passed: No major issues detected")
        
        return warnings


# Example usage
if __name__ == "__main__":
    
    # Generate sample data
    np.random.seed(42)
    n = 1000
    
    df_sample = pd.DataFrame({
        'gvkey': np.repeat(range(100), 10),
        'year': np.tile(range(2014, 2024), 100),
        'roa': np.random.normal(0.05, 0.03, n),
        'roe': np.random.normal(0.08, 0.05, n),
        'rd_intensity': np.random.beta(2, 5, n),
        'firm_size': np.random.lognormal(10, 2, n),
        'leverage': np.random.uniform(0.2, 0.6, n),
        'firm_age': np.random.poisson(20, n),
        'env_dynamism': np.random.uniform(0, 1, n)
    })
    
    print("\n" + "="*60)
    print("TESTING VARIABLE DICTIONARY GENERATOR")
    print("="*60)
    
    # Initialize
    generator = VariableDictionaryGenerator(df_sample)
    
    # Classify variables
    generator.classify_variables(
        dependent=['roa', 'roe'],
        independent=['rd_intensity'],
        moderators=['env_dynamism'],
        controls=['firm_size', 'leverage', 'firm_age'],
        identifiers=['gvkey', 'year']
    )
    
    # Auto-detect types
    generator.auto_detect_types()
    
    # Add descriptions
    descriptions = {
        'roa': 'Return on Assets = Net Income / Total Assets',
        'roe': 'Return on Equity = Net Income / Common Equity',
        'rd_intensity': 'R&D Intensity = R&D Expenditure / Sales',
        'firm_size': 'Firm Size = log(Total Assets)',
        'leverage': 'Financial Leverage = Total Debt / Total Assets',
        'firm_age': 'Firm Age = Years since founding',
        'env_dynamism': 'Environmental Dynamism = Sales volatility (5-year CV)'
    }
    generator.add_descriptions(descriptions)
    
    # Add sources
    sources = {
        'roa': 'Compustat (funda table)',
        'roe': 'Compustat (funda table)',
        'rd_intensity': 'Compustat xrd / sale',
        'firm_size': 'Compustat at (log-transformed)',
        'leverage': 'Compustat dltt / at',
        'firm_age': 'Compustat founding year',
        'env_dynamism': 'Calculated from sales time series'
    }
    generator.add_sources(sources)
    
    # Generate outputs
    output_dir = Path('./output/variable_dictionary/')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    generator.generate_excel(str(output_dir / 'data_dictionary.xlsx'))
    generator.generate_latex(str(output_dir / 'variables_table.tex'))
    generator.generate_markdown(str(output_dir / 'VARIABLES.md'))
    generator.generate_json(str(output_dir / 'variables.json'))
    
    # Validate
    warnings = generator.validate_consistency()
    
    print("\n✅ Variable dictionary generated successfully")
    print(f"   Output directory: {output_dir}")
    print(f"   Generated 4 formats: Excel, LaTeX, Markdown, JSON")
