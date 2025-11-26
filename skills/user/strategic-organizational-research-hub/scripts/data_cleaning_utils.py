"""
Data Cleaning Utilities for Strategic & Organizational Research
================================================================

Comprehensive tools for cleaning and preparing firm-level data
for strategy and organizational research.

Author: Strategic & Organizational Research Hub
Version: 1.0
License: Apache 2.0

Requirements:
    pip install pandas numpy scipy fuzzywuzzy python-Levenshtein
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats.mstats import winsorize
import re
from fuzzywuzzy import fuzz, process
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Missing Data Handler
# ============================================================================

class MissingDataHandler:
    """
    Handle missing data in panel datasets
    """
    
    @staticmethod
    def analyze_missing(df, variables=None):
        """
        Analyze missing data patterns
        
        Args:
            df: DataFrame
            variables: List of variables to analyze (default: all columns)
            
        Returns:
            DataFrame with missing data statistics
        """
        if variables is None:
            variables = df.columns.tolist()
        
        missing_stats = pd.DataFrame({
            'variable': variables,
            'n_missing': [df[var].isnull().sum() for var in variables],
            'pct_missing': [df[var].isnull().sum() / len(df) * 100 for var in variables],
            'n_present': [df[var].notna().sum() for var in variables]
        })
        
        missing_stats = missing_stats.sort_values('pct_missing', ascending=False)
        
        print("="*70)
        print("MISSING DATA ANALYSIS")
        print("="*70)
        print(missing_stats.to_string(index=False))
        
        # Flag high missingness
        high_missing = missing_stats[missing_stats['pct_missing'] > 30]
        if len(high_missing) > 0:
            print("\n⚠️ WARNING: Variables with >30% missing:")
            print(high_missing[['variable', 'pct_missing']].to_string(index=False))
        
        return missing_stats
    
    @staticmethod
    def impute_rd_spending(df, rd_col='xrd', sales_col='sale', 
                          create_indicator=True):
        """
        Impute R&D spending (common issue: firms don't report if zero)
        
        Strategy: Assume missing R&D = 0, but create indicator variable
        
        Args:
            df: DataFrame
            rd_col: R&D expenditure column name
            sales_col: Sales column name (for validation)
            create_indicator: Create dummy = 1 if R&D was missing
            
        Returns:
            DataFrame with imputed R&D
        """
        df_imputed = df.copy()
        
        n_missing = df_imputed[rd_col].isnull().sum()
        pct_missing = n_missing / len(df_imputed) * 100
        
        print("="*70)
        print(f"R&D IMPUTATION: {rd_col}")
        print("="*70)
        print(f"Missing R&D values: {n_missing} ({pct_missing:.1f}%)")
        
        # Create indicator before imputation
        if create_indicator:
            df_imputed[f'{rd_col}_missing'] = df_imputed[rd_col].isnull().astype(int)
            print(f"✅ Created indicator: {rd_col}_missing")
        
        # Impute with 0
        df_imputed[rd_col].fillna(0, inplace=True)
        
        # Validate: R&D should not exceed sales
        if sales_col in df_imputed.columns:
            invalid = (df_imputed[rd_col] > df_imputed[sales_col])
            if invalid.sum() > 0:
                print(f"⚠️ WARNING: {invalid.sum()} observations have R&D > Sales")
                print("   Consider setting these to missing or rechecking data source")
        
        print(f"✅ Imputed {n_missing} missing R&D values with 0")
        
        return df_imputed
    
    @staticmethod
    def forward_fill_firmyear(df, firm_id_col, year_col, fill_vars):
        """
        Forward fill missing values within firm (carry forward last known value)
        
        Use for: Slowly-changing variables (industry, headquarters location)
        
        Args:
            df: DataFrame
            firm_id_col: Firm identifier column
            year_col: Year column
            fill_vars: List of variables to forward fill
            
        Returns:
            DataFrame with forward-filled values
        """
        df_filled = df.copy()
        df_filled = df_filled.sort_values([firm_id_col, year_col])
        
        for var in fill_vars:
            if var in df_filled.columns:
                df_filled[var] = df_filled.groupby(firm_id_col)[var].ffill()
                filled_count = df[var].isnull().sum() - df_filled[var].isnull().sum()
                print(f"✅ Forward-filled {filled_count} missing values in {var}")
        
        return df_filled

# ============================================================================
# Outlier Handler
# ============================================================================

class OutlierHandler:
    """
    Detect and treat outliers
    """
    
    @staticmethod
    def detect_outliers(df, variable, method='zscore', threshold=3):
        """
        Detect outliers using various methods
        
        Args:
            df: DataFrame
            variable: Variable name
            method: 'zscore', 'iqr', or 'percentile'
            threshold: Threshold for z-score (default: 3)
            
        Returns:
            Boolean Series indicating outliers
        """
        data = df[variable].dropna()
        
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outliers = z_scores > threshold
            
        elif method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = (data < lower_bound) | (data > upper_bound)
            
        elif method == 'percentile':
            lower_bound = data.quantile(0.01)
            upper_bound = data.quantile(0.99)
            outliers = (data < lower_bound) | (data > upper_bound)
        
        else:
            raise ValueError("method must be 'zscore', 'iqr', or 'percentile'")
        
        n_outliers = outliers.sum()
        pct_outliers = n_outliers / len(data) * 100
        
        print(f"\n{variable}: Detected {n_outliers} outliers ({pct_outliers:.2f}%) using {method}")
        
        return outliers
    
    @staticmethod
    def winsorize_variable(df, variable, limits=(0.01, 0.01)):
        """
        Winsorize variable at specified percentiles
        
        This caps extreme values at the specified percentile thresholds.
        
        Args:
            df: DataFrame
            variable: Variable name
            limits: Tuple of (lower_pct, upper_pct) as decimals (default: 1%, 99%)
            
        Returns:
            Series with winsorized values
        """
        data = df[variable].copy()
        
        # Get original extremes
        original_min = data.min()
        original_max = data.max()
        
        # Winsorize
        data_winsorized = winsorize(data.dropna(), limits=limits)
        
        # Get new extremes
        new_min = data_winsorized.min()
        new_max = data_winsorized.max()
        
        print(f"\n✅ Winsorized {variable} at {limits[0]*100}% and {100-limits[1]*100}%")
        print(f"   Original range: [{original_min:.4f}, {original_max:.4f}]")
        print(f"   New range: [{new_min:.4f}, {new_max:.4f}]")
        
        # Create winsorized variable in original df index
        df[f"{variable}_wins"] = np.nan
        df.loc[data.notna(), f"{variable}_wins"] = data_winsorized
        
        return df[f"{variable}_wins"]
    
    @staticmethod
    def trim_outliers(df, variable, lower_pct=0.01, upper_pct=0.99):
        """
        Trim (remove) extreme values
        
        Args:
            df: DataFrame
            variable: Variable name
            lower_pct: Lower percentile threshold (default: 1%)
            upper_pct: Upper percentile threshold (default: 99%)
            
        Returns:
            Filtered DataFrame
        """
        lower_bound = df[variable].quantile(lower_pct)
        upper_bound = df[variable].quantile(upper_pct)
        
        df_trimmed = df[
            (df[variable] >= lower_bound) & 
            (df[variable] <= upper_bound)
        ].copy()
        
        removed = len(df) - len(df_trimmed)
        pct_removed = removed / len(df) * 100
        
        print(f"\n✅ Trimmed {variable}")
        print(f"   Bounds: [{lower_bound:.4f}, {upper_bound:.4f}]")
        print(f"   Removed: {removed} observations ({pct_removed:.2f}%)")
        print(f"   Remaining: {len(df_trimmed)} observations")
        
        return df_trimmed

# ============================================================================
# Variable Constructor
# ============================================================================

class VariableConstructor:
    """
    Construct common variables used in strategy research
    """
    
    @staticmethod
    def calculate_roa(df, net_income_col='ni', total_assets_col='at'):
        """
        Calculate Return on Assets (ROA)
        
        ROA = Net Income / Total Assets
        """
        df['roa'] = df[net_income_col] / df[total_assets_col]
        
        print(f"✅ Calculated ROA: {net_income_col} / {total_assets_col}")
        print(f"   Mean ROA: {df['roa'].mean():.4f}")
        print(f"   Median ROA: {df['roa'].median():.4f}")
        
        return df
    
    @staticmethod
    def calculate_roe(df, net_income_col='ni', equity_col='seq'):
        """
        Calculate Return on Equity (ROE)
        
        ROE = Net Income / Shareholders' Equity
        """
        df['roe'] = df[net_income_col] / df[equity_col]
        
        print(f"✅ Calculated ROE: {net_income_col} / {equity_col}")
        print(f"   Mean ROE: {df['roe'].mean():.4f}")
        
        return df
    
    @staticmethod
    def calculate_tobins_q(df, market_value_col='mkvalt', total_assets_col='at',
                          total_liabilities_col='lt'):
        """
        Calculate Tobin's Q
        
        Q = (Market Value of Equity + Book Value of Debt) / Total Assets
        """
        df['tobins_q'] = (df[market_value_col] + df[total_liabilities_col]) / df[total_assets_col]
        
        print(f"✅ Calculated Tobin's Q")
        print(f"   Mean Q: {df['tobins_q'].mean():.4f}")
        
        return df
    
    @staticmethod
    def calculate_leverage(df, total_debt_col='dltt', total_assets_col='at'):
        """
        Calculate Leverage
        
        Leverage = Total Debt / Total Assets
        """
        df['leverage'] = df[total_debt_col] / df[total_assets_col]
        
        print(f"✅ Calculated Leverage: {total_debt_col} / {total_assets_col}")
        print(f"   Mean Leverage: {df['leverage'].mean():.4f}")
        
        return df
    
    @staticmethod
    def calculate_rd_intensity(df, rd_col='xrd', sales_col='sale'):
        """
        Calculate R&D Intensity
        
        R&D Intensity = R&D Expenditure / Sales
        """
        df['rd_intensity'] = df[rd_col] / df[sales_col]
        
        # Cap at 1.0 (100%) - values > 1 likely data errors
        df.loc[df['rd_intensity'] > 1, 'rd_intensity'] = np.nan
        
        print(f"✅ Calculated R&D Intensity: {rd_col} / {sales_col}")
        print(f"   Mean R&D Intensity: {df['rd_intensity'].mean():.4f}")
        print(f"   ⚠️ Capped values > 1.0 (likely errors)")
        
        return df
    
    @staticmethod
    def log_transform(df, variables):
        """
        Apply log transformation to variables
        
        Common for: Firm size, age, employees
        
        Args:
            df: DataFrame
            variables: List of variables to transform
            
        Returns:
            DataFrame with log-transformed variables
        """
        for var in variables:
            if var in df.columns:
                # Check for non-positive values
                if (df[var] <= 0).any():
                    print(f"⚠️ {var} has non-positive values. Using log(x + 1)")
                    df[f'log_{var}'] = np.log(df[var] + 1)
                else:
                    df[f'log_{var}'] = np.log(df[var])
                
                print(f"✅ Created log_{var}")
        
        return df

# ============================================================================
# Firm Name Matching
# ============================================================================

class FirmNameMatcher:
    """
    Match firm names across datasets (fuzzy matching)
    """
    
    @staticmethod
    def standardize_name(name):
        """
        Standardize firm name for matching
        
        - Remove punctuation
        - Convert to lowercase
        - Remove common suffixes (Inc, Corp, Ltd)
        - Remove extra spaces
        """
        if pd.isnull(name):
            return ""
        
        name = str(name).lower()
        
        # Remove punctuation
        name = re.sub(r'[^\w\s]', '', name)
        
        # Remove common suffixes
        suffixes = ['inc', 'corp', 'corporation', 'company', 'co', 'ltd', 
                   'limited', 'llc', 'plc', 'sa', 'nv', 'ag', 'gmbh']
        for suffix in suffixes:
            name = re.sub(r'\b' + suffix + r'\b', '', name)
        
        # Remove extra spaces
        name = ' '.join(name.split())
        
        return name.strip()
    
    @staticmethod
    def fuzzy_match(name, candidates, threshold=80):
        """
        Find best match for a name from a list of candidates
        
        Args:
            name: Name to match
            candidates: List of candidate names
            threshold: Minimum similarity score (0-100)
            
        Returns:
            Best match and similarity score
        """
        name_std = FirmNameMatcher.standardize_name(name)
        candidates_std = [FirmNameMatcher.standardize_name(c) for c in candidates]
        
        # Use fuzzywuzzy for matching
        best_match, score = process.extractOne(name_std, candidates_std, 
                                               scorer=fuzz.token_sort_ratio)
        
        if score >= threshold:
            # Return original candidate name (not standardized)
            match_idx = candidates_std.index(best_match)
            return candidates[match_idx], score
        else:
            return None, score
    
    @staticmethod
    def match_dataframes(df1, df2, name_col1, name_col2, threshold=80):
        """
        Match firms between two dataframes
        
        Args:
            df1: First DataFrame
            df2: Second DataFrame
            name_col1: Firm name column in df1
            name_col2: Firm name column in df2
            threshold: Matching threshold (default: 80)
            
        Returns:
            DataFrame with matches
        """
        print("="*70)
        print("FUZZY FIRM NAME MATCHING")
        print("="*70)
        
        matches = []
        
        for idx1, name1 in df1[name_col1].items():
            best_match, score = FirmNameMatcher.fuzzy_match(
                name1, 
                df2[name_col2].tolist(), 
                threshold=threshold
            )
            
            if best_match:
                matches.append({
                    'name_df1': name1,
                    'name_df2': best_match,
                    'match_score': score
                })
        
        matches_df = pd.DataFrame(matches)
        
        print(f"✅ Matched {len(matches)} out of {len(df1)} firms (threshold={threshold})")
        print(f"   Mean match score: {matches_df['match_score'].mean():.1f}")
        
        # Flag low-confidence matches
        low_confidence = matches_df[matches_df['match_score'] < 90]
        if len(low_confidence) > 0:
            print(f"\n⚠️ {len(low_confidence)} low-confidence matches (score < 90):")
            print(low_confidence.head(10))
        
        return matches_df

# ============================================================================
# Data Validation
# ============================================================================

class DataValidator:
    """
    Validate data quality
    """
    
    @staticmethod
    def check_accounting_equation(df, assets_col='at', liabilities_col='lt', 
                                  equity_col='seq', tolerance=0.01):
        """
        Check if Assets = Liabilities + Equity
        
        Args:
            df: DataFrame
            assets_col: Total assets column
            liabilities_col: Total liabilities column
            equity_col: Shareholders' equity column
            tolerance: Acceptable deviation (as fraction of assets)
            
        Returns:
            Boolean Series indicating violations
        """
        df['accounting_check'] = df[assets_col] - (df[liabilities_col] + df[equity_col])
        df['accounting_check_pct'] = df['accounting_check'] / df[assets_col]
        
        violations = abs(df['accounting_check_pct']) > tolerance
        
        print("="*70)
        print("ACCOUNTING EQUATION VALIDATION")
        print("="*70)
        print(f"Assets = Liabilities + Equity")
        print(f"Tolerance: ±{tolerance*100}% of assets")
        print(f"\n✅ Valid: {(~violations).sum()} observations")
        print(f"⚠️ Violations: {violations.sum()} observations ({violations.sum()/len(df)*100:.2f}%)")
        
        if violations.sum() > 0:
            print("\nSample violations:")
            print(df[violations][['accounting_check', 'accounting_check_pct']].head())
        
        return violations
    
    @staticmethod
    def check_date_consistency(df, firm_id_col, year_col):
        """
        Check for duplicate firm-year observations
        
        Args:
            df: DataFrame
            firm_id_col: Firm identifier column
            year_col: Year column
            
        Returns:
            DataFrame with duplicates
        """
        duplicates = df.duplicated(subset=[firm_id_col, year_col], keep=False)
        
        print("="*70)
        print("DATE CONSISTENCY CHECK")
        print("="*70)
        
        if duplicates.sum() == 0:
            print("✅ No duplicate firm-year observations")
        else:
            print(f"⚠️ WARNING: {duplicates.sum()} duplicate firm-year observations")
            print("\nSample duplicates:")
            print(df[duplicates][[firm_id_col, year_col]].head(10))
        
        return df[duplicates]
    
    @staticmethod
    def check_negative_values(df, variables):
        """
        Check for negative values in variables that should be non-negative
        
        Args:
            df: DataFrame
            variables: List of variables (should be non-negative)
            
        Returns:
            Dictionary with counts of negative values
        """
        print("="*70)
        print("NEGATIVE VALUE CHECK")
        print("="*70)
        
        negative_counts = {}
        
        for var in variables:
            if var in df.columns:
                negative = (df[var] < 0).sum()
                pct_negative = negative / df[var].notna().sum() * 100
                
                negative_counts[var] = negative
                
                if negative > 0:
                    print(f"⚠️ {var}: {negative} negative values ({pct_negative:.2f}%)")
                else:
                    print(f"✅ {var}: No negative values")
        
        return negative_counts

# ============================================================================
# Pipeline: Complete Data Cleaning Workflow
# ============================================================================

class DataCleaningPipeline:
    """
    End-to-end data cleaning pipeline
    """
    
    @staticmethod
    def run_pipeline(df, config):
        """
        Run complete data cleaning pipeline
        
        Args:
            df: Raw DataFrame
            config: Dictionary with cleaning configuration
            
        Example config:
        {
            'firm_id_col': 'gvkey',
            'year_col': 'fyear',
            'winsorize_vars': ['roa', 'leverage'],
            'rd_col': 'xrd',
            'construct_vars': ['roa', 'leverage', 'rd_intensity'],
            'log_vars': ['at', 'sale']
        }
        
        Returns:
            Cleaned DataFrame
        """
        print("="*70)
        print("DATA CLEANING PIPELINE")
        print("="*70)
        print(f"Initial observations: {len(df)}")
        
        df_clean = df.copy()
        
        # 1. Missing data analysis
        print("\n" + "="*70)
        print("STEP 1: MISSING DATA ANALYSIS")
        print("="*70)
        missing_handler = MissingDataHandler()
        missing_handler.analyze_missing(df_clean)
        
        # 2. R&D imputation
        if 'rd_col' in config:
            print("\n" + "="*70)
            print("STEP 2: R&D IMPUTATION")
            print("="*70)
            df_clean = missing_handler.impute_rd_spending(df_clean, rd_col=config['rd_col'])
        
        # 3. Variable construction
        if 'construct_vars' in config:
            print("\n" + "="*70)
            print("STEP 3: VARIABLE CONSTRUCTION")
            print("="*70)
            constructor = VariableConstructor()
            
            if 'roa' in config['construct_vars']:
                df_clean = constructor.calculate_roa(df_clean)
            if 'leverage' in config['construct_vars']:
                df_clean = constructor.calculate_leverage(df_clean)
            if 'rd_intensity' in config['construct_vars']:
                df_clean = constructor.calculate_rd_intensity(df_clean)
        
        # 4. Log transformations
        if 'log_vars' in config:
            print("\n" + "="*70)
            print("STEP 4: LOG TRANSFORMATIONS")
            print("="*70)
            df_clean = constructor.log_transform(df_clean, config['log_vars'])
        
        # 5. Outlier treatment
        if 'winsorize_vars' in config:
            print("\n" + "="*70)
            print("STEP 5: OUTLIER TREATMENT (WINSORIZATION)")
            print("="*70)
            outlier_handler = OutlierHandler()
            for var in config['winsorize_vars']:
                if var in df_clean.columns:
                    outlier_handler.winsorize_variable(df_clean, var)
        
        # 6. Data validation
        print("\n" + "="*70)
        print("STEP 6: DATA VALIDATION")
        print("="*70)
        validator = DataValidator()
        
        if 'firm_id_col' in config and 'year_col' in config:
            validator.check_date_consistency(df_clean, 
                                            config['firm_id_col'], 
                                            config['year_col'])
        
        print("\n" + "="*70)
        print("PIPELINE COMPLETE")
        print("="*70)
        print(f"Final observations: {len(df_clean)}")
        print(f"Variables: {len(df_clean.columns)}")
        
        return df_clean

# ============================================================================
# Example Usage
# ============================================================================

def example_usage():
    """
    Demonstrate data cleaning pipeline
    """
    # Generate sample data
    np.random.seed(42)
    n = 1000
    
    df_raw = pd.DataFrame({
        'gvkey': np.repeat(range(100), 10),
        'fyear': np.tile(range(2014, 2024), 100),
        'at': np.random.lognormal(8, 2, n),  # Total assets
        'sale': np.random.lognormal(7.5, 2, n),  # Sales
        'ni': np.random.normal(50, 200, n),  # Net income
        'lt': np.random.lognormal(7.5, 2, n),  # Total liabilities
        'xrd': np.random.uniform(0, 100, n)  # R&D
    })
    
    # Add some missing R&D
    df_raw.loc[df_raw.sample(frac=0.3).index, 'xrd'] = np.nan
    
    # Add some extreme outliers
    df_raw.loc[df_raw.sample(n=10).index, 'ni'] = np.random.uniform(-1000, 1000, 10)
    
    print("Sample raw data generated")
    
    # Configure pipeline
    config = {
        'firm_id_col': 'gvkey',
        'year_col': 'fyear',
        'rd_col': 'xrd',
        'construct_vars': ['roa', 'leverage', 'rd_intensity'],
        'log_vars': ['at', 'sale'],
        'winsorize_vars': ['roa', 'rd_intensity']
    }
    
    # Run pipeline
    pipeline = DataCleaningPipeline()
    df_clean = pipeline.run_pipeline(df_raw, config)
    
    print("\n✅ Cleaned data ready for analysis")
    print("\nCleaned variables:")
    print(df_clean.columns.tolist())
    
    return df_clean

# ============================================================================
# Main
# ============================================================================

def main():
    """
    Main execution
    """
    example_usage()

if __name__ == "__main__":
    main()
