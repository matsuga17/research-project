"""
esg_variable_builder.py

ESG Variable Constructor for Strategic Research

This module constructs research-ready ESG variables from raw environmental,
social, and governance data. It provides standardized, industry-adjusted, and
theoretically grounded ESG metrics for empirical research.

Key Features:
- Carbon intensity calculation
- ESG score standardization
- Industry-adjusted metrics
- Temporal changes and trends
- ESG performance rankings
- Material ESG factors identification

Common Applications in Strategic Research:
- ESG performance and firm value
- Environmental leadership and competitive advantage
- Carbon disclosure and stock market valuation
- Stakeholder management and financial performance

Usage:
    from esg_variable_builder import ESGVariableBuilder
    
    builder = ESGVariableBuilder(
        esg_data=cdp_panel,
        financial_data=compustat_data
    )
    
    # Build variables
    esg_vars = builder.build_all_variables()
    
    # Save to file
    builder.save_variables('esg_research_variables.csv')
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any, Tuple
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ESGVariableBuilder:
    """
    Builder for ESG research variables
    
    This class constructs standardized, industry-adjusted ESG variables
    suitable for empirical research in strategic management.
    
    Attributes:
        esg_data: DataFrame with ESG metrics
        financial_data: Optional DataFrame with financial metrics
        company_id: Company identifier column
        year_id: Year identifier column
        variables: Dictionary of constructed variables
    """
    
    def __init__(self,
                 esg_data: pd.DataFrame,
                 financial_data: Optional[pd.DataFrame] = None,
                 company_id: str = 'company',
                 year_id: str = 'year',
                 industry_id: Optional[str] = None):
        """
        Initialize ESG variable builder
        
        Args:
            esg_data: ESG metrics (from CDP, KLD, etc.)
            financial_data: Financial metrics (for normalization)
            company_id: Company identifier column
            year_id: Year identifier column
            industry_id: Industry classification column
        """
        self.esg_data = esg_data.copy()
        self.financial_data = financial_data.copy() if financial_data is not None else None
        self.company_id = company_id
        self.year_id = year_id
        self.industry_id = industry_id
        
        self.variables = pd.DataFrame()
        
        logger.info(f"Initialized ESGVariableBuilder:")
        logger.info(f"  ESG data: {len(esg_data)} observations")
        logger.info(f"  Financial data: {len(financial_data) if financial_data is not None else 0} observations")
        
        # Merge if financial data provided
        if self.financial_data is not None:
            self._merge_financial_data()
    
    def _merge_financial_data(self):
        """Merge financial data with ESG data"""
        self.merged_data = self.esg_data.merge(
            self.financial_data,
            on=[self.company_id, self.year_id],
            how='left'
        )
        logger.info(f"  Merged data: {len(self.merged_data)} observations")
    
    def calculate_carbon_intensity(self,
                                  emission_col: str = 'total_emissions',
                                  revenue_col: Optional[str] = 'revenue') -> pd.Series:
        """
        Calculate carbon intensity (emissions per unit revenue)
        
        Lower carbon intensity indicates better environmental efficiency.
        
        Args:
            emission_col: Emissions column name
            revenue_col: Revenue column name (if available)
        
        Returns:
            Carbon intensity series
        """
        logger.info("Calculating carbon intensity...")
        
        if revenue_col and revenue_col in self.merged_data.columns:
            # Carbon per million dollars of revenue
            intensity = (self.merged_data[emission_col] / 
                        (self.merged_data[revenue_col] / 1e6))
            
            logger.info(f"  Mean intensity: {intensity.mean():.2f} tonnes CO2e per $M revenue")
        else:
            logger.warning("Revenue data not available. Using emissions only.")
            intensity = self.merged_data[emission_col]
        
        return intensity
    
    def standardize_esg_scores(self,
                              score_cols: List[str],
                              method: str = 'zscore') -> pd.DataFrame:
        """
        Standardize ESG scores
        
        Args:
            score_cols: List of score columns to standardize
            method: 'zscore' or 'minmax'
        
        Returns:
            DataFrame with standardized scores
        """
        logger.info(f"Standardizing ESG scores using {method} method...")
        
        standardized = pd.DataFrame()
        
        for col in score_cols:
            if col in self.esg_data.columns:
                if method == 'zscore':
                    # Z-score normalization
                    standardized[f'{col}_std'] = (
                        (self.esg_data[col] - self.esg_data[col].mean()) / 
                        self.esg_data[col].std()
                    )
                elif method == 'minmax':
                    # Min-max normalization [0, 1]
                    standardized[f'{col}_std'] = (
                        (self.esg_data[col] - self.esg_data[col].min()) / 
                        (self.esg_data[col].max() - self.esg_data[col].min())
                    )
                
                logger.info(f"  Standardized: {col}")
        
        return standardized
    
    def calculate_industry_adjusted_metrics(self,
                                          metric_cols: List[str]) -> pd.DataFrame:
        """
        Calculate industry-adjusted ESG metrics
        
        Subtracts industry mean to control for industry effects.
        
        Args:
            metric_cols: List of metric columns to adjust
        
        Returns:
            DataFrame with industry-adjusted metrics
        """
        if self.industry_id is None or self.industry_id not in self.esg_data.columns:
            logger.warning("Industry identifier not available. Skipping industry adjustment.")
            return pd.DataFrame()
        
        logger.info("Calculating industry-adjusted metrics...")
        
        adjusted = pd.DataFrame()
        
        for col in metric_cols:
            if col in self.esg_data.columns:
                # Calculate industry-year means
                industry_means = self.esg_data.groupby([self.industry_id, self.year_id])[col].transform('mean')
                
                # Subtract industry mean
                adjusted[f'{col}_ind_adj'] = self.esg_data[col] - industry_means
                
                logger.info(f"  Industry-adjusted: {col}")
        
        return adjusted
    
    def calculate_temporal_changes(self,
                                  metric_cols: List[str]) -> pd.DataFrame:
        """
        Calculate year-over-year changes in ESG metrics
        
        Args:
            metric_cols: List of metric columns
        
        Returns:
            DataFrame with temporal changes
        """
        logger.info("Calculating temporal changes...")
        
        changes = pd.DataFrame()
        
        # Sort by company and year
        df_sorted = self.esg_data.sort_values([self.company_id, self.year_id])
        
        for col in metric_cols:
            if col in df_sorted.columns:
                # Year-over-year change
                changes[f'{col}_yoy_change'] = df_sorted.groupby(self.company_id)[col].diff()
                
                # Year-over-year percent change
                changes[f'{col}_yoy_pct'] = df_sorted.groupby(self.company_id)[col].pct_change()
                
                logger.info(f"  Temporal change: {col}")
        
        return changes
    
    def calculate_esg_performance_rank(self,
                                      score_col: str,
                                      ascending: bool = False) -> pd.Series:
        """
        Calculate ESG performance percentile rank
        
        Args:
            score_col: ESG score column
            ascending: True if lower scores are better
        
        Returns:
            Percentile rank series (0-100)
        """
        logger.info(f"Calculating ESG performance rank for {score_col}...")
        
        # Rank within each year
        ranks = self.esg_data.groupby(self.year_id)[score_col].rank(
            method='average',
            ascending=ascending,
            pct=True
        ) * 100
        
        logger.info(f"  Mean percentile: {ranks.mean():.1f}")
        
        return ranks
    
    def create_esg_leader_dummy(self,
                               score_col: str,
                               threshold: float = 75,
                               ascending: bool = False) -> pd.Series:
        """
        Create dummy variable for ESG leaders
        
        Args:
            score_col: ESG score column
            threshold: Percentile threshold (default: top 25%)
            ascending: True if lower scores are better
        
        Returns:
            Binary indicator for ESG leaders
        """
        logger.info(f"Creating ESG leader dummy (threshold: {threshold}th percentile)...")
        
        ranks = self.calculate_esg_performance_rank(score_col, ascending)
        
        if ascending:
            leaders = (ranks <= (100 - threshold)).astype(int)
        else:
            leaders = (ranks >= threshold).astype(int)
        
        logger.info(f"  ESG leaders: {leaders.sum()} ({leaders.mean()*100:.1f}%)")
        
        return leaders
    
    def calculate_emissions_reduction_target(self,
                                            emission_col: str = 'total_emissions',
                                            base_year: Optional[int] = None,
                                            target_reduction: float = 0.50) -> pd.Series:
        """
        Calculate if company is on track for emissions reduction target
        
        Args:
            emission_col: Emissions column name
            base_year: Base year for comparison (if None, use first year)
            target_reduction: Target reduction (e.g., 0.50 for 50% reduction)
        
        Returns:
            Series indicating if on track
        """
        logger.info(f"Calculating emissions reduction progress (target: {target_reduction*100:.0f}%)...")
        
        df = self.esg_data.sort_values([self.company_id, self.year_id])
        
        if base_year is None:
            # Use first year as base
            base_emissions = df.groupby(self.company_id)[emission_col].first()
        else:
            # Use specified base year
            base_data = df[df[self.year_id] == base_year]
            base_emissions = base_data.set_index(self.company_id)[emission_col]
        
        # Calculate current reduction from base
        current_emissions = df.set_index(self.company_id)[emission_col]
        reduction_achieved = 1 - (current_emissions / base_emissions)
        
        # On track if achieved >= target
        on_track = (reduction_achieved >= target_reduction).astype(int)
        
        logger.info(f"  Companies on track: {on_track.sum()} ({on_track.mean()*100:.1f}%)")
        
        return on_track
    
    def calculate_esg_volatility(self,
                                score_col: str,
                                window: int = 3) -> pd.Series:
        """
        Calculate rolling volatility of ESG scores
        
        Args:
            score_col: ESG score column
            window: Rolling window size (years)
        
        Returns:
            ESG volatility series
        """
        logger.info(f"Calculating ESG volatility (window: {window} years)...")
        
        df = self.esg_data.sort_values([self.company_id, self.year_id])
        
        volatility = df.groupby(self.company_id)[score_col].rolling(
            window=window,
            min_periods=2
        ).std().reset_index(level=0, drop=True)
        
        logger.info(f"  Mean volatility: {volatility.mean():.3f}")
        
        return volatility
    
    def build_all_variables(self) -> pd.DataFrame:
        """
        Build all ESG variables
        
        Returns:
            Complete dataset with all constructed variables
        """
        logger.info("Building all ESG variables...")
        
        # Start with base data
        result = self.esg_data.copy()
        
        # 1. Carbon intensity
        if 'total_emissions' in result.columns:
            result['carbon_intensity'] = self.calculate_carbon_intensity()
        
        # 2. Standardized scores
        score_cols = [col for col in result.columns if 'score' in col.lower()]
        if score_cols:
            standardized = self.standardize_esg_scores(score_cols)
            result = pd.concat([result, standardized], axis=1)
        
        # 3. Industry adjustment
        if self.industry_id and self.industry_id in result.columns:
            adjusted = self.calculate_industry_adjusted_metrics(score_cols)
            result = pd.concat([result, adjusted], axis=1)
        
        # 4. Temporal changes
        metric_cols = [col for col in result.columns if any(x in col.lower() for x in ['emission', 'score'])]
        if metric_cols:
            changes = self.calculate_temporal_changes(metric_cols)
            result = pd.concat([result, changes], axis=1)
        
        # 5. Performance ranks
        if score_cols:
            for col in score_cols:
                result[f'{col}_percentile'] = self.calculate_esg_performance_rank(col)
        
        # 6. Leader dummies
        if score_cols:
            for col in score_cols:
                result[f'{col}_leader'] = self.create_esg_leader_dummy(col)
        
        # 7. Volatility
        if score_cols:
            for col in score_cols:
                result[f'{col}_volatility'] = self.calculate_esg_volatility(col)
        
        self.variables = result
        
        logger.info(f"✓ Built {len(result.columns)} variables")
        logger.info(f"  Original columns: {len(self.esg_data.columns)}")
        logger.info(f"  New variables: {len(result.columns) - len(self.esg_data.columns)}")
        
        return result
    
    def generate_summary_statistics(self) -> pd.DataFrame:
        """
        Generate summary statistics for all variables
        
        Returns:
            Summary statistics DataFrame
        """
        if self.variables.empty:
            logger.warning("No variables built yet. Run build_all_variables() first.")
            return pd.DataFrame()
        
        # Select numeric columns
        numeric_cols = self.variables.select_dtypes(include=[np.number]).columns
        
        summary = self.variables[numeric_cols].describe().T
        summary['missing'] = self.variables[numeric_cols].isnull().sum()
        summary['missing_pct'] = (summary['missing'] / len(self.variables)) * 100
        
        return summary
    
    def save_variables(self, filepath: Path):
        """
        Save constructed variables to CSV
        
        Args:
            filepath: Output file path
        """
        if self.variables.empty:
            raise ValueError("No variables to save. Run build_all_variables() first.")
        
        self.variables.to_csv(filepath, index=False)
        logger.info(f"✓ Variables saved: {filepath}")
    
    def generate_report(self, output_dir: Path) -> str:
        """
        Generate comprehensive variable construction report
        
        Args:
            output_dir: Directory to save report
        
        Returns:
            Report text
        """
        if self.variables.empty:
            raise ValueError("No variables built. Run build_all_variables() first.")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate summary statistics
        summary = self.generate_summary_statistics()
        summary.to_csv(output_dir / 'variable_summary_statistics.csv')
        
        # Generate report
        report = f"""
# ESG Variable Construction Report

## Dataset Overview
- **Total Observations**: {len(self.variables):,}
- **Companies**: {self.variables[self.company_id].nunique()}
- **Years**: {self.variables[self.year_id].min()} - {self.variables[self.year_id].max()}
- **Total Variables**: {len(self.variables.columns)}

## Variable Categories

### 1. Carbon Metrics
"""
        
        carbon_vars = [col for col in self.variables.columns if 'carbon' in col.lower() or 'emission' in col.lower()]
        for var in carbon_vars:
            report += f"- {var}\n"
        
        report += "\n### 2. ESG Scores\n"
        score_vars = [col for col in self.variables.columns if 'score' in col.lower()]
        for var in score_vars:
            report += f"- {var}\n"
        
        report += "\n### 3. Performance Indicators\n"
        perf_vars = [col for col in self.variables.columns if any(x in col.lower() for x in ['percentile', 'leader', 'rank'])]
        for var in perf_vars:
            report += f"- {var}\n"
        
        report += "\n### 4. Temporal Dynamics\n"
        temp_vars = [col for col in self.variables.columns if any(x in col.lower() for x in ['change', 'volatility', 'yoy'])]
        for var in temp_vars:
            report += f"- {var}\n"
        
        report += f"""
## Data Quality

### Missing Values
Top variables with missing data:
"""
        
        missing = summary.nlargest(5, 'missing_pct')[['missing', 'missing_pct']]
        for idx, row in missing.iterrows():
            report += f"- {idx}: {row['missing']} ({row['missing_pct']:.1f}%)\n"
        
        report += """
## Usage Recommendations

### For ESG Performance Studies
- Use `climate_score_std` or `climate_score_percentile` as main ESG measure
- Control for `carbon_intensity` and `industry`
- Consider `climate_score_leader` for binary treatment

### For Environmental Strategy Studies
- Use `total_emissions` or `carbon_intensity` as outcome
- Analyze `*_yoy_change` for strategic shifts
- Use `*_volatility` for consistency assessment

### For Stakeholder Studies
- Use `climate_score_percentile` for relative performance
- Include `*_ind_adj` for industry comparisons
- Consider `climate_score_leader` for reputation effects

## Files Generated
- `variable_summary_statistics.csv`: Descriptive statistics
- `esg_research_variables.csv`: Complete dataset

"""
        
        # Save report
        report_path = output_dir / 'esg_variable_report.md'
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"✓ Report saved: {report_path}")
        
        return report


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("ESG VARIABLE BUILDER EXAMPLE")
    print("=" * 80)
    
    # Generate sample ESG data
    np.random.seed(42)
    n_companies = 50
    n_years = 5
    
    companies = [f'Company_{i}' for i in range(1, n_companies + 1)]
    years = list(range(2018, 2023))
    
    data = []
    for company in companies:
        for year in years:
            data.append({
                'company': company,
                'year': year,
                'total_emissions': np.random.lognormal(10, 1),
                'climate_score_numeric': np.random.randint(1, 9),
                'industry': np.random.choice(['Tech', 'Manufacturing', 'Services']),
                'revenue': np.random.lognormal(15, 1.5)
            })
    
    esg_data = pd.DataFrame(data)
    financial_data = esg_data[['company', 'year', 'revenue']].copy()
    
    print("\n[Step 1] Initializing builder...")
    builder = ESGVariableBuilder(
        esg_data=esg_data,
        financial_data=financial_data,
        industry_id='industry'
    )
    
    print("\n[Step 2] Building all variables...")
    variables_df = builder.build_all_variables()
    
    print(f"\nVariables built: {len(variables_df.columns)}")
    print(f"Observations: {len(variables_df)}")
    
    print("\n[Step 3] Generating summary statistics...")
    summary = builder.generate_summary_statistics()
    print(summary.head())
    
    print("\n[Step 4] Saving outputs...")
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    builder.save_variables(output_dir / 'esg_variables.csv')
    builder.generate_report(output_dir)
    
    print("\n" + "=" * 80)
    print("ESG VARIABLE CONSTRUCTION COMPLETED")
    print("=" * 80)
