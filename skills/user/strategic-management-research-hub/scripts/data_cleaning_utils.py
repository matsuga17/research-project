"""
Data Cleaning Utilities for Strategic & Organizational Research
================================================================

Comprehensive data cleaning and preprocessing functions:
- Missing data handling
- Outlier detection and treatment
- Variable transformation
- Data quality diagnostics
- Consistency checks

Author: Strategic & Organizational Research Hub
License: Apache 2.0
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import StandardScaler, RobustScaler
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

CLEANING_CONFIG = {
    "missing_threshold": 0.5,  # Drop variables with >50% missing
    "outlier_method": "iqr",   # 'iqr', 'zscore', or 'percentile'
    "outlier_threshold": 3,    # Standard deviations or IQR multiplier
    "winsorize_percentiles": (0.01, 0.99)
}

# ============================================================================
# Missing Data Analysis
# ============================================================================

class MissingDataAnalyzer:
    """
    Analyze and visualize missing data patterns
    """
    
    @staticmethod
    def analyze_missing(df: pd.DataFrame) -> pd.DataFrame:
        """
        Comprehensive missing data analysis
        
        Args:
            df: Input DataFrame
        
        Returns:
            DataFrame with missing data statistics
        """
        missing_stats = pd.DataFrame({
            'column': df.columns,
            'missing_count': df.isnull().sum().values,
            'missing_pct': (df.isnull().sum() / len(df) * 100).values,
            'dtype': df.dtypes.values,
            'n_unique': [df[col].nunique() for col in df.columns]
        })
        
        missing_stats = missing_stats.sort_values('missing_pct', ascending=False)
        missing_stats = missing_stats[missing_stats['missing_count'] > 0]
        
        print("="*70)
        print("MISSING DATA ANALYSIS")
        print("="*70)
        
        if len(missing_stats) == 0:
            print("✅ No missing data detected")
        else:
            print(f"⚠️  {len(missing_stats)} columns with missing data:\n")
            print(missing_stats.to_string(index=False))
            
            # Classification
            severe = missing_stats[missing_stats['missing_pct'] > 50]
            moderate = missing_stats[(missing_stats['missing_pct'] > 20) & (missing_stats['missing_pct'] <= 50)]
            minor = missing_stats[missing_stats['missing_pct'] <= 20]
            
            print(f"\n📊 Summary:")
            print(f"   - Severe (>50%): {len(severe)} columns")
            print(f"   - Moderate (20-50%): {len(moderate)} columns")
            print(f"   - Minor (<20%): {len(minor)} columns")
        
        return missing_stats
    
    @staticmethod
    def plot_missing_pattern(df: pd.DataFrame, save_path: Optional[str] = None):
        """
        Visualize missing data pattern
        """
        # Calculate missing percentage
        missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
        missing_pct = missing_pct[missing_pct > 0]
        
        if len(missing_pct) == 0:
            print("✅ No missing data to visualize")
            return
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, max(6, len(missing_pct) * 0.3)))
        
        bars = ax.barh(range(len(missing_pct)), missing_pct.values, color='coral')
        ax.set_yticks(range(len(missing_pct)))
        ax.set_yticklabels(missing_pct.index)
        ax.set_xlabel("Missing Data (%)", fontsize=12)
        ax.set_title("Missing Data by Variable", fontsize=14, fontweight='bold')
        ax.axvline(x=20, color='orange', linestyle='--', alpha=0.5, label='20% threshold')
        ax.axvline(x=50, color='red', linestyle='--', alpha=0.5, label='50% threshold')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Missing data plot saved: {save_path}")
        
        plt.show()
    
    @staticmethod
    def missing_indicator_method(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Create missing indicators and fill with appropriate values
        
        Strategy for R&D data: "If R&D is missing, create indicator and fill with 0"
        
        Args:
            df: Input DataFrame
            columns: Columns to apply indicator method
        
        Returns:
            DataFrame with missing indicators
        """
        df_clean = df.copy()
        
        for col in columns:
            if col in df.columns:
                # Create missing indicator
                indicator_name = f"{col}_missing"
                df_clean[indicator_name] = df[col].isnull().astype(int)
                
                # Fill missing with 0
                df_clean[col] = df_clean[col].fillna(0)
                
                missing_count = df_clean[indicator_name].sum()
                print(f"   ✓ {col}: Created indicator ({missing_count} missing, {missing_count/len(df)*100:.1f}%)")
        
        return df_clean

# ============================================================================
# Outlier Detection and Treatment
# ============================================================================

class OutlierHandler:
    """
    Detect and treat outliers in continuous variables
    """
    
    @staticmethod
    def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
        """
        Detect outliers using IQR method
        
        Args:
            series: Input series
            multiplier: IQR multiplier (1.5 = mild, 3.0 = extreme)
        
        Returns:
            Boolean series indicating outliers
        """
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outliers = (series < lower_bound) | (series > upper_bound)
        
        return outliers
    
    @staticmethod
    def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
        """
        Detect outliers using Z-score method
        
        Args:
            series: Input series
            threshold: Z-score threshold (typically 3.0)
        
        Returns:
            Boolean series indicating outliers
        """
        z_scores = np.abs(stats.zscore(series, nan_policy='omit'))
        outliers = z_scores > threshold
        
        return outliers
    
    @staticmethod
    def winsorize(df: pd.DataFrame, columns: List[str], 
                  lower: float = 0.01, upper: float = 0.99) -> pd.DataFrame:
        """
        Winsorize variables to reduce outlier impact
        
        Args:
            df: Input DataFrame
            columns: Columns to winsorize
            lower: Lower percentile (default 1%)
            upper: Upper percentile (default 99%)
        
        Returns:
            DataFrame with winsorized variables
        """
        df_winsorized = df.copy()
        
        print("\n" + "="*70)
        print("WINSORIZATION")
        print("="*70)
        print(f"Percentiles: {lower*100}% - {upper*100}%\n")
        
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                lower_bound = df[col].quantile(lower)
                upper_bound = df[col].quantile(upper)
                
                # Count observations affected
                n_below = (df[col] < lower_bound).sum()
                n_above = (df[col] > upper_bound).sum()
                
                # Winsorize
                df_winsorized[col] = df[col].clip(lower_bound, upper_bound)
                
                print(f"   ✓ {col}:")
                print(f"      - Bounds: [{lower_bound:.4f}, {upper_bound:.4f}]")
                print(f"      - Affected: {n_below} below, {n_above} above")
        
        return df_winsorized
    
    @staticmethod
    def analyze_outliers(df: pd.DataFrame, columns: List[str], 
                        method: str = 'iqr') -> Dict:
        """
        Comprehensive outlier analysis
        
        Args:
            df: Input DataFrame
            columns: Columns to analyze
            method: 'iqr' or 'zscore'
        
        Returns:
            Dictionary with outlier statistics
        """
        print("\n" + "="*70)
        print(f"OUTLIER ANALYSIS ({method.upper()} method)")
        print("="*70)
        
        outlier_stats = {}
        
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                if method == 'iqr':
                    outliers = OutlierHandler.detect_outliers_iqr(df[col].dropna())
                elif method == 'zscore':
                    outliers = OutlierHandler.detect_outliers_zscore(df[col].dropna())
                else:
                    raise ValueError("Method must be 'iqr' or 'zscore'")
                
                n_outliers = outliers.sum()
                pct_outliers = n_outliers / len(df[col].dropna()) * 100
                
                outlier_stats[col] = {
                    'n_outliers': n_outliers,
                    'pct_outliers': pct_outliers
                }
                
                print(f"   {col}: {n_outliers} outliers ({pct_outliers:.2f}%)")
        
        return outlier_stats

# ============================================================================
# Variable Transformation
# ============================================================================

class VariableTransformer:
    """
    Transform variables for regression analysis
    """
    
    @staticmethod
    def log_transform(df: pd.DataFrame, columns: List[str], 
                     add_one: bool = True) -> pd.DataFrame:
        """
        Apply logarithmic transformation
        
        Args:
            df: Input DataFrame
            columns: Columns to transform
            add_one: If True, use log(x+1) to handle zeros
        
        Returns:
            DataFrame with log-transformed variables
        """
        df_transformed = df.copy()
        
        print("\n" + "="*70)
        print("LOGARITHMIC TRANSFORMATION")
        print("="*70)
        
        for col in columns:
            if col in df.columns:
                new_col_name = f"log_{col}"
                
                if add_one:
                    df_transformed[new_col_name] = np.log(df[col] + 1)
                    print(f"   ✓ {col} → {new_col_name} [log(x+1)]")
                else:
                    # Check for non-positive values
                    if (df[col] <= 0).any():
                        print(f"   ⚠️  {col} contains non-positive values, using log(x+1)")
                        df_transformed[new_col_name] = np.log(df[col] + 1)
                    else:
                        df_transformed[new_col_name] = np.log(df[col])
                        print(f"   ✓ {col} → {new_col_name} [log(x)]")
        
        return df_transformed
    
    @staticmethod
    def standardize(df: pd.DataFrame, columns: List[str], 
                   method: str = 'zscore') -> pd.DataFrame:
        """
        Standardize variables
        
        Args:
            df: Input DataFrame
            columns: Columns to standardize
            method: 'zscore' (mean=0, std=1) or 'robust' (median-based)
        
        Returns:
            DataFrame with standardized variables
        """
        df_standardized = df.copy()
        
        print("\n" + "="*70)
        print(f"STANDARDIZATION ({method.upper()})")
        print("="*70)
        
        if method == 'zscore':
            scaler = StandardScaler()
        elif method == 'robust':
            scaler = RobustScaler()
        else:
            raise ValueError("Method must be 'zscore' or 'robust'")
        
        for col in columns:
            if col in df.columns:
                new_col_name = f"std_{col}"
                df_standardized[new_col_name] = scaler.fit_transform(df[[col]])
                print(f"   ✓ {col} → {new_col_name}")
        
        return df_standardized
    
    @staticmethod
    def create_interaction(df: pd.DataFrame, var1: str, var2: str) -> pd.DataFrame:
        """
        Create interaction term
        
        Args:
            df: Input DataFrame
            var1: First variable
            var2: Second variable
        
        Returns:
            DataFrame with interaction term
        """
        df_interaction = df.copy()
        interaction_name = f"{var1}_x_{var2}"
        df_interaction[interaction_name] = df[var1] * df[var2]
        
        print(f"✅ Interaction term created: {interaction_name}")
        
        return df_interaction
    
    @staticmethod
    def create_polynomial(df: pd.DataFrame, column: str, degree: int = 2) -> pd.DataFrame:
        """
        Create polynomial terms (for testing curvilinear relationships)
        
        Args:
            df: Input DataFrame
            column: Column to transform
            degree: Polynomial degree
        
        Returns:
            DataFrame with polynomial terms
        """
        df_poly = df.copy()
        
        for d in range(2, degree + 1):
            poly_name = f"{column}_pow{d}"
            df_poly[poly_name] = df[column] ** d
            print(f"   ✓ Created {poly_name}")
        
        return df_poly

# ============================================================================
# Data Quality Diagnostics
# ============================================================================

class DataQualityChecker:
    """
    Comprehensive data quality diagnostics
    """
    
    @staticmethod
    def check_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict:
        """
        Check for duplicate observations
        
        Args:
            df: Input DataFrame
            subset: Columns to check for duplicates (e.g., ['firm_id', 'year'])
        
        Returns:
            Dictionary with duplicate statistics
        """
        if subset:
            duplicates = df.duplicated(subset=subset, keep=False)
        else:
            duplicates = df.duplicated(keep=False)
        
        n_duplicates = duplicates.sum()
        
        print("\n" + "="*70)
        print("DUPLICATE CHECK")
        print("="*70)
        
        if n_duplicates == 0:
            print("✅ No duplicates found")
        else:
            print(f"⚠️  {n_duplicates} duplicate observations detected")
            if subset:
                print(f"   (Based on columns: {subset})")
            
            # Show example duplicates
            print("\nExample duplicates:")
            print(df[duplicates].head(10))
        
        return {
            'n_duplicates': n_duplicates,
            'pct_duplicates': n_duplicates / len(df) * 100
        }
    
    @staticmethod
    def check_consistency(df: pd.DataFrame, rules: Dict[str, str]) -> Dict:
        """
        Check logical consistency rules
        
        Args:
            df: Input DataFrame
            rules: Dictionary of rules (name: condition)
                   Example: {'positive_assets': 'total_assets > 0'}
        
        Returns:
            Dictionary with rule violations
        """
        print("\n" + "="*70)
        print("CONSISTENCY CHECKS")
        print("="*70)
        
        violations = {}
        
        for rule_name, condition in rules.items():
            try:
                valid = df.eval(condition)
                n_violations = (~valid).sum()
                
                violations[rule_name] = {
                    'condition': condition,
                    'n_violations': n_violations,
                    'pct_violations': n_violations / len(df) * 100
                }
                
                if n_violations == 0:
                    print(f"   ✅ {rule_name}: All observations valid")
                else:
                    print(f"   ⚠️  {rule_name}: {n_violations} violations ({n_violations/len(df)*100:.2f}%)")
                    
            except Exception as e:
                print(f"   ❌ {rule_name}: Error evaluating condition - {e}")
        
        return violations
    
    @staticmethod
    def summary_statistics(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """
        Generate comprehensive summary statistics
        
        Args:
            df: Input DataFrame
            columns: Columns to summarize
        
        Returns:
            DataFrame with summary statistics
        """
        summary = df[columns].describe().T
        summary['missing'] = df[columns].isnull().sum()
        summary['missing_pct'] = (df[columns].isnull().sum() / len(df) * 100)
        summary['n_unique'] = df[columns].nunique()
        
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        print(summary.to_string())
        
        return summary
    
    @staticmethod
    def correlation_analysis(df: pd.DataFrame, columns: List[str], 
                           threshold: float = 0.8) -> pd.DataFrame:
        """
        Analyze correlations and flag high correlations
        
        Args:
            df: Input DataFrame
            columns: Columns to analyze
            threshold: Correlation threshold for flagging
        
        Returns:
            DataFrame with high correlations
        """
        corr_matrix = df[columns].corr()
        
        # Extract upper triangle (avoid duplicates)
        upper_tri = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        corr_pairs = corr_matrix.where(upper_tri).stack().reset_index()
        corr_pairs.columns = ['Variable 1', 'Variable 2', 'Correlation']
        
        # Flag high correlations
        high_corr = corr_pairs[np.abs(corr_pairs['Correlation']) > threshold]
        high_corr = high_corr.sort_values('Correlation', key=abs, ascending=False)
        
        print("\n" + "="*70)
        print(f"HIGH CORRELATIONS (|r| > {threshold})")
        print("="*70)
        
        if len(high_corr) == 0:
            print("✅ No high correlations detected")
        else:
            print(f"⚠️  {len(high_corr)} pairs with high correlation:\n")
            print(high_corr.to_string(index=False))
            print("\n⚠️  High correlations may indicate multicollinearity")
        
        return high_corr

# ============================================================================
# Complete Data Cleaning Pipeline
# ============================================================================

class DataCleaningPipeline:
    """
    Execute complete data cleaning workflow
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize pipeline with raw data
        """
        self.df_raw = df.copy()
        self.df_clean = df.copy()
        self.cleaning_log = []
    
    def run_pipeline(self, 
                    continuous_vars: List[str],
                    winsorize_vars: Optional[List[str]] = None,
                    log_transform_vars: Optional[List[str]] = None,
                    missing_indicator_vars: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Run complete cleaning pipeline
        
        Args:
            continuous_vars: List of continuous variables
            winsorize_vars: Variables to winsorize
            log_transform_vars: Variables to log-transform
            missing_indicator_vars: Variables to apply missing indicator method
        
        Returns:
            Cleaned DataFrame
        """
        print("="*70)
        print("DATA CLEANING PIPELINE")
        print("="*70)
        print(f"Input: {len(self.df_clean)} observations, {len(self.df_clean.columns)} variables\n")
        
        # 1. Missing data analysis
        missing_analyzer = MissingDataAnalyzer()
        missing_stats = missing_analyzer.analyze_missing(self.df_clean)
        
        # 2. Handle missing data with indicator method
        if missing_indicator_vars:
            print("\n" + "="*70)
            print("MISSING INDICATOR METHOD")
            print("="*70)
            self.df_clean = missing_analyzer.missing_indicator_method(
                self.df_clean, missing_indicator_vars
            )
        
        # 3. Outlier analysis
        outlier_handler = OutlierHandler()
        outlier_stats = outlier_handler.analyze_outliers(self.df_clean, continuous_vars)
        
        # 4. Winsorization
        if winsorize_vars:
            self.df_clean = outlier_handler.winsorize(
                self.df_clean, winsorize_vars,
                lower=CLEANING_CONFIG['winsorize_percentiles'][0],
                upper=CLEANING_CONFIG['winsorize_percentiles'][1]
            )
        
        # 5. Variable transformation
        if log_transform_vars:
            transformer = VariableTransformer()
            self.df_clean = transformer.log_transform(self.df_clean, log_transform_vars)
        
        # 6. Data quality checks
        quality_checker = DataQualityChecker()
        quality_checker.summary_statistics(self.df_clean, continuous_vars)
        
        print("\n" + "="*70)
        print("CLEANING COMPLETE")
        print("="*70)
        print(f"Output: {len(self.df_clean)} observations, {len(self.df_clean.columns)} variables")
        print(f"Variables added: {len(self.df_clean.columns) - len(self.df_raw.columns)}")
        
        return self.df_clean
    
    def export_cleaning_report(self, filename: str):
        """
        Export data cleaning report
        """
        report = {
            'raw_shape': self.df_raw.shape,
            'clean_shape': self.df_clean.shape,
            'variables_added': len(self.df_clean.columns) - len(self.df_raw.columns),
            'cleaning_steps': self.cleaning_log
        }
        
        with open(filename, 'w') as f:
            f.write("DATA CLEANING REPORT\n")
            f.write("="*70 + "\n\n")
            for key, value in report.items():
                f.write(f"{key}: {value}\n")
        
        print(f"✅ Cleaning report exported: {filename}")

# ============================================================================
# Example Workflow
# ============================================================================

def example_cleaning():
    """
    Example data cleaning workflow
    """
    print("="*70)
    print("DATA CLEANING EXAMPLE")
    print("="*70)
    
    # Generate synthetic firm-level data
    np.random.seed(42)
    n = 1000
    
    df = pd.DataFrame({
        'firm_id': range(n),
        'year': np.random.choice([2020, 2021, 2022], n),
        'total_assets': np.random.lognormal(10, 2, n),
        'sales': np.random.lognormal(9, 1.5, n),
        'rnd': np.random.lognormal(5, 1, int(n * 0.7)),  # 30% missing
        'employees': np.random.poisson(500, n),
        'roa': np.random.normal(0.05, 0.1, n)
    })
    
    # Add some outliers
    df.loc[np.random.choice(n, 10), 'roa'] = np.random.uniform(-0.5, 0.5, 10)
    
    # Pad R&D with NaN for missing values
    df['rnd'] = pd.concat([pd.Series(df['rnd'].values), 
                           pd.Series([np.nan] * int(n * 0.3))], ignore_index=True).values[:n]
    
    print(f"\n✅ Synthetic data generated: {len(df)} observations\n")
    
    # Run cleaning pipeline
    pipeline = DataCleaningPipeline(df)
    
    df_clean = pipeline.run_pipeline(
        continuous_vars=['total_assets', 'sales', 'rnd', 'employees', 'roa'],
        winsorize_vars=['total_assets', 'sales', 'roa'],
        log_transform_vars=['total_assets', 'sales'],
        missing_indicator_vars=['rnd']
    )
    
    # Export
    df_clean.to_csv('cleaned_data.csv', index=False)
    pipeline.export_cleaning_report('cleaning_report.txt')
    
    print(f"\n✅ Cleaned data exported: cleaned_data.csv")

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution function
    """
    example_cleaning()

if __name__ == "__main__":
    main()
