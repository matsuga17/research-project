"""
Corporate Data Processing Toolkit
==================================
A collection of utility functions for processing corporate financial data
in empirical research.

Author: Corporate Research Data Hub
Version: 1.0
Date: 2025-10-31

Dependencies:
    - pandas>=1.3.0
    - numpy>=1.21.0
    - scipy>=1.7.0

Usage:
    from corporate_data_utils import *
    
    # Load data
    df = pd.read_csv('raw_data.csv')
    
    # Clean and standardize
    df = standardize_financial_variables(df)
    df = winsorize_variables(df, ['roa', 'leverage'], limits=[0.01, 0.01])
    
    # Create variables
    df = create_financial_ratios(df)
    df = create_lagged_variables(df, firm_id='gvkey', time_var='year')
    
    # Quality checks
    report = run_quality_checks(df)
    print(report)
"""

import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
from scipy.spatial import distance
import warnings

# ============================================================================
# 1. DATA LOADING & INITIAL PROCESSING
# ============================================================================

def load_compustat_data(filepath, key_vars=None):
    """
    Load Compustat data with standard preprocessing.
    
    Parameters:
    -----------
    filepath : str
        Path to Compustat data file (CSV, Stata, etc.)
    key_vars : list, optional
        List of essential variables. Records with missing key_vars will be dropped.
    
    Returns:
    --------
    df : DataFrame
        Loaded and initially processed data
    """
    # Detect file type and load
    if filepath.endswith('.dta'):
        df = pd.read_stata(filepath)
    elif filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)
    else:
        raise ValueError("Unsupported file format. Use .dta, .csv, or .parquet")
    
    print(f"Loaded {len(df):,} observations with {len(df.columns)} variables")
    
    # Convert date variables
    if 'datadate' in df.columns:
        df['datadate'] = pd.to_datetime(df['datadate'])
        df['year'] = df['datadate'].dt.year
    
    # Handle missing data codes (Compustat specific)
    # Some fields use specific negative values for missing
    missing_codes = [-9999, -99.99]
    for col in df.select_dtypes(include=[np.number]).columns:
        df.loc[df[col].isin(missing_codes), col] = np.nan
    
    # Drop records with missing key variables
    if key_vars:
        initial_count = len(df)
        df = df.dropna(subset=key_vars)
        dropped = initial_count - len(df)
        if dropped > 0:
            print(f"Dropped {dropped:,} records with missing key variables")
    
    return df


def merge_compustat_crsp(df_compustat, df_crsp, link_table_path=None):
    """
    Merge Compustat and CRSP data using CCM link table.
    
    Parameters:
    -----------
    df_compustat : DataFrame
        Compustat data with 'gvkey' and 'datadate'
    df_crsp : DataFrame
        CRSP data with 'permno' and 'date'
    link_table_path : str, optional
        Path to CRSP-Compustat merged link table (ccmxpf_linktable)
        If None, assumes df_compustat already has 'lpermno'
    
    Returns:
    --------
    df_merged : DataFrame
        Merged dataset
    """
    if link_table_path:
        # Load link table
        ccm = pd.read_stata(link_table_path) if link_table_path.endswith('.dta') \
              else pd.read_csv(link_table_path)
        
        # Keep only primary links
        ccm = ccm[ccm['linktype'].isin(['LC', 'LU'])]
        ccm = ccm[ccm['linkprim'].isin(['P', 'C'])]
        
        # Merge Compustat with link table
        df_compustat = df_compustat.merge(
            ccm[['gvkey', 'lpermno', 'linkdt', 'linkenddt']], 
            on='gvkey', 
            how='left'
        )
        
        # Keep only valid links (datadate within link period)
        df_compustat = df_compustat[
            (df_compustat['datadate'] >= df_compustat['linkdt']) &
            (df_compustat['datadate'] <= df_compustat['linkenddt'])
        ]
    
    # Merge with CRSP
    df_merged = df_compustat.merge(
        df_crsp,
        left_on=['lpermno', 'datadate'],
        right_on=['permno', 'date'],
        how='inner',
        validate='one_to_one',
        indicator=True
    )
    
    # Report merge statistics
    print(f"\nMerge Statistics:")
    print(f"Compustat records: {len(df_compustat):,}")
    print(f"CRSP records: {len(df_crsp):,}")
    print(f"Matched records: {len(df_merged):,}")
    print(f"Match rate: {len(df_merged)/len(df_compustat)*100:.1f}%")
    
    return df_merged


# ============================================================================
# 2. VARIABLE STANDARDIZATION & CLEANING
# ============================================================================

def standardize_financial_variables(df, currency_scale='millions'):
    """
    Standardize financial variables to consistent units.
    
    Parameters:
    -----------
    df : DataFrame
        Raw financial data
    currency_scale : str
        Target scale: 'thousands', 'millions', or 'billions'
    
    Returns:
    --------
    df : DataFrame
        Standardized data
    """
    # Compustat reports in millions by default
    # Define scale factors
    scale_factors = {
        'thousands': 1000,
        'millions': 1,
        'billions': 0.001
    }
    
    scale = scale_factors.get(currency_scale, 1)
    
    # Financial variables typically in millions in Compustat
    financial_vars = ['at', 'sale', 'ni', 'ceq', 'dltt', 'dlc', 'che', 
                      'capx', 'xrd', 'lt', 'act', 'lct']
    
    for var in financial_vars:
        if var in df.columns:
            df[var] = df[var] * scale
    
    print(f"Financial variables standardized to {currency_scale}")
    
    return df


def handle_special_values(df):
    """
    Handle special cases in financial data:
    - R&D: Missing often means zero (not all firms report)
    - Dividends: Missing means zero
    - But distinguish from true missing (firm-years that should have data)
    
    Parameters:
    -----------
    df : DataFrame
        Financial data
    
    Returns:
    --------
    df : DataFrame
        Data with special values handled
    """
    # R&D expenditure (xrd)
    if 'xrd' in df.columns:
        df['xrd_missing'] = df['xrd'].isna().astype(int)
        df['xrd'] = df['xrd'].fillna(0)
        print(f"R&D: {df['xrd_missing'].sum():,} missing values set to 0 with indicator")
    
    # Dividends (dvc)
    if 'dvc' in df.columns:
        df['dvc'] = df['dvc'].fillna(0)
    
    # Negative values in some variables are data errors
    if 'at' in df.columns:  # Total assets cannot be negative
        neg_assets = (df['at'] < 0).sum()
        if neg_assets > 0:
            print(f"Warning: {neg_assets} observations with negative assets set to NaN")
            df.loc[df['at'] < 0, 'at'] = np.nan
    
    return df


def winsorize_variables(df, variables, limits=[0.01, 0.01]):
    """
    Winsorize continuous variables at specified percentiles.
    
    Parameters:
    -----------
    df : DataFrame
        Data to winsorize
    variables : list
        List of variable names to winsorize
    limits : list
        [lower_percentile, upper_percentile], e.g., [0.01, 0.01] for 1%/99%
    
    Returns:
    --------
    df : DataFrame
        Data with winsorized variables
    """
    for var in variables:
        if var in df.columns:
            original_mean = df[var].mean()
            df[var] = winsorize(df[var].dropna(), limits=limits)
            new_mean = df[var].mean()
            print(f"Winsorized {var}: mean changed from {original_mean:.4f} to {new_mean:.4f}")
        else:
            print(f"Warning: Variable '{var}' not found in DataFrame")
    
    return df


# ============================================================================
# 3. FINANCIAL RATIO CONSTRUCTION
# ============================================================================

def create_financial_ratios(df):
    """
    Create standard financial ratios used in corporate research.
    
    Parameters:
    -----------
    df : DataFrame
        Data with raw financial variables
    
    Returns:
    --------
    df : DataFrame
        Data with financial ratios added
    """
    # Return on Assets (ROA)
    if 'ni' in df.columns and 'at' in df.columns:
        df['roa'] = df['ni'] / df['at']
        print("Created: roa = ni / at")
    
    # Return on Equity (ROE)
    if 'ni' in df.columns and 'ceq' in df.columns:
        df['roe'] = df['ni'] / df['ceq']
        # Handle negative equity
        df.loc[df['ceq'] <= 0, 'roe'] = np.nan
        print("Created: roe = ni / ceq")
    
    # Leverage
    if 'dltt' in df.columns and 'dlc' in df.columns and 'at' in df.columns:
        df['leverage'] = (df['dltt'] + df['dlc']) / df['at']
        print("Created: leverage = (dltt + dlc) / at")
    
    # Current Ratio
    if 'act' in df.columns and 'lct' in df.columns:
        df['current_ratio'] = df['act'] / df['lct']
        df.loc[df['lct'] == 0, 'current_ratio'] = np.nan
        print("Created: current_ratio = act / lct")
    
    # Cash Ratio
    if 'che' in df.columns and 'at' in df.columns:
        df['cash_ratio'] = df['che'] / df['at']
        print("Created: cash_ratio = che / at")
    
    # R&D Intensity
    if 'xrd' in df.columns and 'sale' in df.columns:
        df['rd_intensity'] = df['xrd'] / df['sale']
        df.loc[df['sale'] == 0, 'rd_intensity'] = np.nan
        print("Created: rd_intensity = xrd / sale")
    
    # Capital Intensity
    if 'ppent' in df.columns and 'sale' in df.columns:
        df['capital_intensity'] = df['ppent'] / df['sale']
        df.loc[df['sale'] == 0, 'capital_intensity'] = np.nan
        print("Created: capital_intensity = ppent / sale")
    
    # Sales Growth
    if 'sale' in df.columns and 'gvkey' in df.columns:
        df = df.sort_values(['gvkey', 'year'])
        df['sales_growth'] = df.groupby('gvkey')['sale'].pct_change()
        print("Created: sales_growth (year-over-year)")
    
    # Tobin's Q (approximation)
    # (Market Value of Equity + Book Value of Debt) / Total Assets
    if 'mkvalt' in df.columns and 'dltt' in df.columns and 'dlc' in df.columns and 'at' in df.columns:
        df['tobins_q'] = (df['mkvalt'] + df['dltt'] + df['dlc']) / df['at']
        print("Created: tobins_q (approximation)")
    
    return df


def create_log_variables(df, variables):
    """
    Create log-transformed variables.
    
    Parameters:
    -----------
    df : DataFrame
        Data
    variables : list
        Variables to log-transform
    
    Returns:
    --------
    df : DataFrame
        Data with log variables added
    """
    for var in variables:
        if var in df.columns:
            # Check for zeros and negatives
            zeros = (df[var] == 0).sum()
            negatives = (df[var] < 0).sum()
            
            if zeros > 0 or negatives > 0:
                # Use log(x+1) transformation
                df[f'log_{var}'] = np.log(df[var] + 1)
                print(f"Created: log_{var} using log(x+1) due to {zeros} zeros and {negatives} negatives")
            else:
                df[f'log_{var}'] = np.log(df[var])
                print(f"Created: log_{var}")
        else:
            print(f"Warning: Variable '{var}' not found")
    
    return df


# ============================================================================
# 4. PANEL DATA OPERATIONS
# ============================================================================

def create_lagged_variables(df, variables, lags=[1], firm_id='gvkey', time_var='year'):
    """
    Create lagged variables for panel data analysis.
    
    Parameters:
    -----------
    df : DataFrame
        Panel data
    variables : list
        Variables to lag
    lags : list
        Number of periods to lag
    firm_id : str
        Firm identifier variable
    time_var : str
        Time variable
    
    Returns:
    --------
    df : DataFrame
        Data with lagged variables
    """
    df = df.sort_values([firm_id, time_var])
    
    for var in variables:
        if var in df.columns:
            for lag in lags:
                lagged_var = f'lag{lag}_{var}'
                df[lagged_var] = df.groupby(firm_id)[var].shift(lag)
                print(f"Created: {lagged_var}")
        else:
            print(f"Warning: Variable '{var}' not found")
    
    return df


def create_lead_variables(df, variables, leads=[1], firm_id='gvkey', time_var='year'):
    """
    Create lead (forward) variables for panel data.
    
    Parameters:
    -----------
    df : DataFrame
        Panel data
    variables : list
        Variables to lead
    leads : list
        Number of periods to lead
    firm_id : str
        Firm identifier variable
    time_var : str
        Time variable
    
    Returns:
    --------
    df : DataFrame
        Data with lead variables
    """
    df = df.sort_values([firm_id, time_var])
    
    for var in variables:
        if var in df.columns:
            for lead in leads:
                lead_var = f'lead{lead}_{var}'
                df[lead_var] = df.groupby(firm_id)[var].shift(-lead)
                print(f"Created: {lead_var}")
        else:
            print(f"Warning: Variable '{var}' not found")
    
    return df


def calculate_industry_means(df, variables, industry_var='sic2', time_var='year'):
    """
    Calculate industry-year means (for industry-adjusted performance measures).
    
    Parameters:
    -----------
    df : DataFrame
        Data
    variables : list
        Variables to calculate industry means for
    industry_var : str
        Industry classification variable
    time_var : str
        Time variable
    
    Returns:
    --------
    df : DataFrame
        Data with industry-adjusted variables
    """
    for var in variables:
        if var in df.columns:
            # Calculate industry-year mean
            ind_mean = df.groupby([industry_var, time_var])[var].transform('mean')
            df[f'{var}_ind_adj'] = df[var] - ind_mean
            print(f"Created: {var}_ind_adj (industry-adjusted)")
        else:
            print(f"Warning: Variable '{var}' not found")
    
    return df


# ============================================================================
# 5. INDUSTRY CLASSIFICATION
# ============================================================================

def fama_french_12_industry(sic):
    """
    Map SIC code to Fama-French 12 industry classification.
    
    Parameters:
    -----------
    sic : int
        4-digit SIC code
    
    Returns:
    --------
    industry : int
        Fama-French 12 industry code (1-12)
    """
    if pd.isna(sic):
        return np.nan
    
    sic = int(sic)
    
    if 100 <= sic <= 999:  # Consumer NonDurables
        return 1
    elif 2000 <= sic <= 2399 or 2700 <= sic <= 2749 or 2770 <= sic <= 2799 or 3100 <= sic <= 3199 or 3940 <= sic <= 3989:
        return 2  # Consumer Durables
    elif 2500 <= sic <= 2519 or 2590 <= sic <= 2599 or 3630 <= sic <= 3659 or 3710 <= sic <= 3711 or 3714 <= sic <= 3714 or 3716 <= sic <= 3716 or 3750 <= sic <= 3751 or 3792 <= sic <= 3792 or 3900 <= sic <= 3939 or 3990 <= sic <= 3999:
        return 3  # Manufacturing
    elif 1200 <= sic <= 1399 or 2900 <= sic <= 2999:
        return 4  # Energy
    elif 2520 <= sic <= 2589 or 2600 <= sic <= 2699 or 2750 <= sic <= 2769 or 3000 <= sic <= 3099 or 3200 <= sic <= 3569 or 3580 <= sic <= 3629 or 3700 <= sic <= 3709 or 3712 <= sic <= 3713 or 3715 <= sic <= 3715 or 3717 <= sic <= 3749 or 3752 <= sic <= 3791 or 3793 <= sic <= 3799 or 3830 <= sic <= 3839 or 3860 <= sic <= 3899:
        return 5  # Chemicals and Allied Products
    elif 3570 <= sic <= 3579 or 3660 <= sic <= 3692 or 3694 <= sic <= 3699 or 3810 <= sic <= 3829 or 7370 <= sic <= 7379:
        return 6  # Business Equipment (Computers, Software, Electronic Equipment)
    elif 4800 <= sic <= 4899:
        return 7  # Telecom
    elif 4900 <= sic <= 4949:
        return 8  # Utilities
    elif 5000 <= sic <= 5999:
        return 9  # Shops (Wholesale, Retail, Some Services)
    elif 7000 <= sic <= 7200 or 7210 <= sic <= 7299 or 7395 <= sic <= 7500 or 7520 <= sic <= 7549 or 7600 <= sic <= 7699 or 7800 <= sic <= 7999 or 8000 <= sic <= 8099 or 8200 <= sic <= 8299 or 8400 <= sic <= 8499 or 8600 <= sic <= 8699 or 8800 <= sic <= 8899:
        return 10  # Healthcare, Medical Equipment, and Drugs
    elif 6000 <= sic <= 6999:
        return 11  # Finance
    else:
        return 12  # Other


def add_fama_french_industries(df, sic_var='sich'):
    """
    Add Fama-French industry classifications to dataset.
    
    Parameters:
    -----------
    df : DataFrame
        Data with SIC codes
    sic_var : str
        Name of SIC variable
    
    Returns:
    --------
    df : DataFrame
        Data with FF industry variables
    """
    if sic_var in df.columns:
        df['ff12_ind'] = df[sic_var].apply(fama_french_12_industry)
        print(f"Created: ff12_ind (Fama-French 12 industry classification)")
        
        # Create 2-digit SIC for industry fixed effects
        df['sic2'] = (df[sic_var] / 100).astype(int)
        print(f"Created: sic2 (2-digit SIC code)")
    else:
        print(f"Warning: SIC variable '{sic_var}' not found")
    
    return df


# ============================================================================
# 6. QUALITY CHECKS
# ============================================================================

def check_accounting_identities(df, tolerance=0.01):
    """
    Verify basic accounting identities: Assets = Liabilities + Equity.
    
    Parameters:
    -----------
    df : DataFrame
        Financial data
    tolerance : float
        Acceptable error as fraction of total assets
    
    Returns:
    --------
    report : dict
        Summary of accounting errors
    """
    if 'at' in df.columns and 'lt' in df.columns and 'ceq' in df.columns:
        df['accounting_error'] = abs(df['at'] - (df['lt'] + df['ceq']))
        df['accounting_error_pct'] = df['accounting_error'] / df['at']
        
        errors = df[df['accounting_error_pct'] > tolerance]
        
        report = {
            'total_observations': len(df),
            'observations_with_errors': len(errors),
            'error_rate': len(errors) / len(df) * 100,
            'mean_error_pct': errors['accounting_error_pct'].mean() if len(errors) > 0 else 0,
            'max_error_pct': errors['accounting_error_pct'].max() if len(errors) > 0 else 0
        }
        
        print(f"\nAccounting Identity Check:")
        print(f"Observations with errors >{tolerance*100}%: {report['observations_with_errors']:,} ({report['error_rate']:.2f}%)")
        
        return report
    else:
        print("Warning: Required variables (at, lt, ceq) not found for accounting check")
        return None


def detect_outliers(df, variables, method='mahalanobis', threshold=0.99):
    """
    Detect multivariate outliers in the dataset.
    
    Parameters:
    -----------
    df : DataFrame
        Data
    variables : list
        Variables to use for outlier detection
    method : str
        'mahalanobis' or 'iqr'
    threshold : float
        Quantile threshold for outlier detection (0-1)
    
    Returns:
    --------
    outlier_indices : Index
        Indices of detected outliers
    """
    # Select and clean data
    X = df[variables].dropna()
    
    if method == 'mahalanobis':
        # Calculate Mahalanobis distance
        mean = X.mean()
        cov = X.cov()
        cov_inv = np.linalg.inv(cov)
        
        distances = []
        for idx, row in X.iterrows():
            dist = distance.mahalanobis(row, mean, cov_inv)
            distances.append((idx, dist))
        
        distances = pd.DataFrame(distances, columns=['index', 'mahalanobis'])
        distances = distances.set_index('index')
        
        # Identify outliers
        cutoff = distances['mahalanobis'].quantile(threshold)
        outliers = distances[distances['mahalanobis'] > cutoff]
        
        print(f"\nOutlier Detection (Mahalanobis, {threshold*100}th percentile):")
        print(f"Outliers detected: {len(outliers):,} ({len(outliers)/len(X)*100:.2f}%)")
        
        return outliers.index
    
    elif method == 'iqr':
        # IQR method (univariate for each variable)
        outlier_mask = pd.Series(False, index=X.index)
        
        for var in variables:
            Q1 = X[var].quantile(0.25)
            Q3 = X[var].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outlier_mask |= (X[var] < lower) | (X[var] > upper)
        
        outliers = X[outlier_mask]
        
        print(f"\nOutlier Detection (IQR method):")
        print(f"Outliers detected: {len(outliers):,} ({len(outliers)/len(X)*100:.2f}%)")
        
        return outliers.index


def check_temporal_consistency(df, variable, firm_id='gvkey', time_var='year', 
                                growth_threshold=5.0):
    """
    Check for extreme year-over-year changes in variables.
    
    Parameters:
    -----------
    df : DataFrame
        Panel data
    variable : str
        Variable to check
    firm_id : str
        Firm identifier
    time_var : str
        Time variable
    growth_threshold : float
        Flag growth rates exceeding this (as multiple, e.g., 5 = 500%)
    
    Returns:
    --------
    extreme_changes : DataFrame
        Observations with extreme changes
    """
    df = df.sort_values([firm_id, time_var])
    df[f'{variable}_growth'] = df.groupby(firm_id)[variable].pct_change()
    
    extreme = df[
        (df[f'{variable}_growth'].abs() > growth_threshold) | 
        (df[f'{variable}_growth'].abs() == np.inf)
    ]
    
    print(f"\nTemporal Consistency Check for {variable}:")
    print(f"Observations with extreme growth (>|{growth_threshold*100}%|): {len(extreme):,}")
    
    if len(extreme) > 0:
        print("\nSample of extreme changes:")
        print(extreme[[firm_id, time_var, variable, f'{variable}_growth']].head(10))
    
    return extreme


def run_quality_checks(df, firm_id='gvkey', time_var='year'):
    """
    Run comprehensive quality checks on corporate dataset.
    
    Parameters:
    -----------
    df : DataFrame
        Corporate panel data
    firm_id : str
        Firm identifier
    time_var : str
        Time variable
    
    Returns:
    --------
    report : dict
        Comprehensive quality report
    """
    print("="*70)
    print("CORPORATE DATA QUALITY ASSURANCE REPORT")
    print("="*70)
    
    report = {}
    
    # 1. Sample composition
    report['total_observations'] = len(df)
    report['unique_firms'] = df[firm_id].nunique()
    report['time_coverage'] = (df[time_var].min(), df[time_var].max())
    report['avg_obs_per_firm'] = len(df) / report['unique_firms']
    
    print(f"\n1. SAMPLE COMPOSITION:")
    print(f"   Total observations: {report['total_observations']:,}")
    print(f"   Unique firms: {report['unique_firms']:,}")
    print(f"   Time coverage: {report['time_coverage'][0]} to {report['time_coverage'][1]}")
    print(f"   Average observations per firm: {report['avg_obs_per_firm']:.1f}")
    
    # 2. Missing data analysis
    print(f"\n2. MISSING DATA ANALYSIS:")
    missing = df.isnull().sum() / len(df) * 100
    missing = missing[missing > 0].sort_values(ascending=False)
    print(f"   Variables with >20% missing:")
    for var, pct in missing[missing > 20].items():
        print(f"   - {var}: {pct:.1f}%")
    report['missing_data'] = missing.to_dict()
    
    # 3. Accounting identities
    accounting_report = check_accounting_identities(df)
    report['accounting_check'] = accounting_report
    
    # 4. Temporal consistency
    if 'sale' in df.columns:
        extreme_sales = check_temporal_consistency(df, 'sale', firm_id, time_var)
        report['extreme_sales_growth'] = len(extreme_sales)
    
    # 5. Summary statistics
    print(f"\n5. SUMMARY STATISTICS:")
    numeric_vars = ['at', 'sale', 'ni', 'roa', 'leverage']
    existing_vars = [v for v in numeric_vars if v in df.columns]
    if existing_vars:
        summary = df[existing_vars].describe()
        print(summary)
        report['summary_stats'] = summary.to_dict()
    
    print("="*70)
    print("END OF QUALITY REPORT")
    print("="*70)
    
    return report


# ============================================================================
# 7. EXPORT & DOCUMENTATION
# ============================================================================

def save_dataset_multiple_formats(df, base_filename, formats=['dta', 'csv', 'parquet']):
    """
    Save dataset in multiple formats for different users.
    
    Parameters:
    -----------
    df : DataFrame
        Final dataset
    base_filename : str
        Base filename without extension
    formats : list
        List of formats to save: 'dta', 'csv', 'parquet', 'xlsx'
    """
    for fmt in formats:
        if fmt == 'dta':
            df.to_stata(f'{base_filename}.dta', write_index=False, version=117)
            print(f"Saved: {base_filename}.dta")
        elif fmt == 'csv':
            df.to_csv(f'{base_filename}.csv', index=False)
            print(f"Saved: {base_filename}.csv")
        elif fmt == 'parquet':
            df.to_parquet(f'{base_filename}.parquet', index=False, compression='gzip')
            print(f"Saved: {base_filename}.parquet")
        elif fmt == 'xlsx':
            df.to_excel(f'{base_filename}.xlsx', index=False, sheet_name='Data')
            print(f"Saved: {base_filename}.xlsx")


def create_data_dictionary(df, output_file='data_dictionary.xlsx'):
    """
    Create a data dictionary documenting all variables.
    
    Parameters:
    -----------
    df : DataFrame
        Dataset
    output_file : str
        Output file path
    """
    # Variable information
    var_info = []
    for col in df.columns:
        dtype = df[col].dtype
        missing_pct = df[col].isnull().sum() / len(df) * 100
        unique_vals = df[col].nunique()
        
        if dtype in [np.float64, np.int64]:
            var_min = df[col].min()
            var_max = df[col].max()
            var_mean = df[col].mean()
            var_std = df[col].std()
        else:
            var_min = var_max = var_mean = var_std = np.nan
        
        var_info.append({
            'Variable': col,
            'Type': str(dtype),
            'Missing %': f"{missing_pct:.2f}",
            'Unique Values': unique_vals,
            'Min': var_min,
            'Max': var_max,
            'Mean': var_mean,
            'Std Dev': var_std
        })
    
    dict_df = pd.DataFrame(var_info)
    dict_df.to_excel(output_file, index=False, sheet_name='Data Dictionary')
    print(f"Data dictionary saved to: {output_file}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example workflow for processing corporate financial data.
    """
    
    # 1. Load data
    # df = load_compustat_data('compustat_raw.dta', key_vars=['gvkey', 'at', 'sale'])
    
    # 2. Standardize and clean
    # df = standardize_financial_variables(df, currency_scale='millions')
    # df = handle_special_values(df)
    
    # 3. Create variables
    # df = create_financial_ratios(df)
    # df = create_log_variables(df, ['at', 'sale'])
    # df = add_fama_french_industries(df, sic_var='sich')
    
    # 4. Create panel variables
    # df = create_lagged_variables(df, ['roa', 'leverage'], lags=[1])
    
    # 5. Winsorize
    # df = winsorize_variables(df, ['roa', 'leverage', 'tobins_q'])
    
    # 6. Quality checks
    # report = run_quality_checks(df)
    
    # 7. Save
    # save_dataset_multiple_formats(df, 'final_dataset')
    # create_data_dictionary(df, 'data_dictionary.xlsx')
    
    print("Corporate Data Processing Toolkit loaded successfully!")
    print("Import this module and use the functions for your data processing workflow.")