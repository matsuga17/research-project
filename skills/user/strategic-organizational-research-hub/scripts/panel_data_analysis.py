"""
Panel Data Analysis Template for Strategic & Organizational Research
====================================================================

This script provides comprehensive tools for panel data analysis commonly
used in strategy and organizational research. Includes fixed effects,
random effects, difference-in-differences, and robustness checks.

Author: Strategic & Organizational Research Hub
Version: 1.0
License: Apache 2.0

Requirements:
    pip install pandas numpy statsmodels linearmodels scipy matplotlib seaborn
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
from linearmodels import PanelOLS, RandomEffects
from linearmodels.panel import compare
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Data Preparation for Panel Analysis
# ============================================================================

class PanelDataPrep:
    """
    Prepare data for panel analysis
    """
    
    @staticmethod
    def create_panel_dataset(df, firm_id_col, time_col):
        """
        Convert DataFrame to panel format with MultiIndex
        
        Args:
            df: pandas DataFrame
            firm_id_col: Column name for firm identifier
            time_col: Column name for time period
            
        Returns:
            DataFrame with MultiIndex (firm_id, time)
        """
        # Set multi-index
        df_panel = df.set_index([firm_id_col, time_col])
        
        # Sort by firm and time
        df_panel = df_panel.sort_index()
        
        print(f"✅ Panel dataset created: {df_panel.index.levshape[0]} firms, "
              f"{df_panel.index.levshape[1]} time periods")
        
        # Check balance
        firm_counts = df.groupby(firm_id_col)[time_col].count()
        if firm_counts.std() == 0:
            print("✅ Balanced panel")
        else:
            print(f"⚠️ Unbalanced panel: Firms have {firm_counts.min()}-{firm_counts.max()} observations")
            print(f"   Mean observations per firm: {firm_counts.mean():.1f}")
        
        return df_panel
    
    @staticmethod
    def create_lagged_variables(df, variables, lags=1):
        """
        Create lagged variables for panel data
        
        Args:
            df: Panel DataFrame with MultiIndex (firm_id, time)
            variables: List of variable names to lag
            lags: Number of lags (default: 1)
            
        Returns:
            DataFrame with lagged variables added
        """
        df_lagged = df.copy()
        
        for var in variables:
            if var in df.columns:
                for lag in range(1, lags + 1):
                    lag_name = f"{var}_lag{lag}"
                    df_lagged[lag_name] = df.groupby(level=0)[var].shift(lag)
                    print(f"✅ Created {lag_name}")
        
        return df_lagged
    
    @staticmethod
    def winsorize_variables(df, variables, limits=(0.01, 0.01)):
        """
        Winsorize variables at specified percentiles
        
        Args:
            df: DataFrame
            variables: List of variable names
            limits: Tuple of (lower, upper) percentiles (default: 1%, 99%)
            
        Returns:
            DataFrame with winsorized variables
        """
        from scipy.stats.mstats import winsorize
        
        df_wins = df.copy()
        
        for var in variables:
            if var in df.columns:
                df_wins[f"{var}_wins"] = winsorize(df[var].dropna(), limits=limits)
                print(f"✅ Winsorized {var} at {limits[0]*100}% and {100-limits[1]*100}% percentiles")
        
        return df_wins

# ============================================================================
# Fixed Effects Regression
# ============================================================================

class FixedEffectsAnalysis:
    """
    Fixed effects panel regression
    """
    
    @staticmethod
    def run_fixed_effects(df_panel, dependent_var, independent_vars, 
                         entity_effects=True, time_effects=True,
                         cluster_entity=True):
        """
        Run fixed effects regression
        
        Args:
            df_panel: Panel DataFrame with MultiIndex
            dependent_var: Name of dependent variable
            independent_vars: List of independent variable names
            entity_effects: Include firm fixed effects (default: True)
            time_effects: Include year fixed effects (default: True)
            cluster_entity: Cluster standard errors at firm level (default: True)
            
        Returns:
            PanelOLS results object
        """
        # Prepare variables
        y = df_panel[dependent_var]
        X = df_panel[independent_vars]
        
        # Drop missing values
        data_clean = pd.concat([y, X], axis=1).dropna()
        y_clean = data_clean[dependent_var]
        X_clean = data_clean[independent_vars]
        
        print(f"\n{'='*70}")
        print("FIXED EFFECTS REGRESSION")
        print(f"{'='*70}")
        print(f"Dependent Variable: {dependent_var}")
        print(f"Independent Variables: {', '.join(independent_vars)}")
        print(f"Observations: {len(y_clean)}")
        print(f"Firms: {y_clean.index.get_level_values(0).nunique()}")
        print(f"Entity Effects: {'Yes' if entity_effects else 'No'}")
        print(f"Time Effects: {'Yes' if time_effects else 'No'}")
        
        # Run regression
        model = PanelOLS(y_clean, X_clean, 
                        entity_effects=entity_effects, 
                        time_effects=time_effects)
        
        if cluster_entity:
            results = model.fit(cov_type='clustered', cluster_entity=True)
        else:
            results = model.fit()
        
        return results
    
    @staticmethod
    def compare_models(models_dict, model_names):
        """
        Compare multiple models side by side
        
        Args:
            models_dict: Dictionary of model results
            model_names: List of model names
            
        Returns:
            Comparison table
        """
        comparison = compare(models_dict)
        print("\n" + "="*70)
        print("MODEL COMPARISON")
        print("="*70)
        print(comparison.summary)
        
        return comparison

# ============================================================================
# Random Effects vs Fixed Effects
# ============================================================================

class HausmanTest:
    """
    Hausman test to choose between FE and RE
    """
    
    @staticmethod
    def run_hausman_test(df_panel, dependent_var, independent_vars):
        """
        Run Hausman test and both FE and RE regressions
        
        Returns:
            Dictionary with FE results, RE results, and test statistic
        """
        # Prepare data
        y = df_panel[dependent_var]
        X = df_panel[independent_vars]
        data_clean = pd.concat([y, X], axis=1).dropna()
        
        # Fixed Effects
        fe_model = PanelOLS(data_clean[dependent_var], 
                           data_clean[independent_vars],
                           entity_effects=True, 
                           time_effects=True)
        fe_results = fe_model.fit(cov_type='clustered', cluster_entity=True)
        
        # Random Effects
        re_model = RandomEffects(data_clean[dependent_var], 
                                data_clean[independent_vars])
        re_results = re_model.fit()
        
        print("\n" + "="*70)
        print("HAUSMAN TEST: Fixed Effects vs Random Effects")
        print("="*70)
        print("H0: Random effects is consistent and efficient")
        print("H1: Fixed effects is consistent (reject random effects)")
        
        # Note: Direct Hausman test implementation
        # For simplicity, we compare coefficients manually
        fe_coefs = fe_results.params
        re_coefs = re_results.params
        
        print("\nCoefficient Comparison:")
        comparison = pd.DataFrame({
            'Fixed Effects': fe_coefs,
            'Random Effects': re_coefs,
            'Difference': fe_coefs - re_coefs
        })
        print(comparison)
        
        print("\n⚠️ Note: If differences are large, prefer Fixed Effects.")
        print("   If differences are small, Random Effects is more efficient.")
        
        return {
            'fe_results': fe_results,
            're_results': re_results,
            'coefficient_comparison': comparison
        }

# ============================================================================
# Difference-in-Differences (DiD)
# ============================================================================

class DifferenceInDifferences:
    """
    Difference-in-Differences analysis
    """
    
    @staticmethod
    def prepare_did_data(df, treatment_col, post_col, outcome_col):
        """
        Prepare data for DiD analysis
        
        Args:
            df: DataFrame
            treatment_col: Binary variable (1=treated, 0=control)
            post_col: Binary variable (1=post-treatment, 0=pre-treatment)
            outcome_col: Outcome variable
            
        Returns:
            DataFrame with interaction term
        """
        df_did = df.copy()
        df_did['did_interaction'] = df_did[treatment_col] * df_did[post_col]
        
        # Check parallel trends (simple version)
        print("\n" + "="*70)
        print("PARALLEL TRENDS CHECK")
        print("="*70)
        
        pre_treatment = df_did[df_did[post_col] == 0]
        
        treated_mean = pre_treatment[pre_treatment[treatment_col] == 1][outcome_col].mean()
        control_mean = pre_treatment[pre_treatment[treatment_col] == 0][outcome_col].mean()
        
        print(f"Pre-treatment mean (Treated): {treated_mean:.4f}")
        print(f"Pre-treatment mean (Control): {control_mean:.4f}")
        print(f"Difference: {treated_mean - control_mean:.4f}")
        print("\n⚠️ Ideally, plot trends over time to verify parallel trends assumption")
        
        return df_did
    
    @staticmethod
    def run_did_regression(df_did, outcome_col, treatment_col, post_col, 
                          controls=None):
        """
        Run DiD regression
        
        Model: Y = β0 + β1*Treated + β2*Post + β3*(Treated×Post) + Controls + ε
        
        β3 = DiD estimator (treatment effect)
        """
        # Prepare variables
        X_vars = [treatment_col, post_col, 'did_interaction']
        if controls:
            X_vars.extend(controls)
        
        y = df_did[outcome_col]
        X = df_did[X_vars]
        X = sm.add_constant(X)
        
        # Drop missing
        data_clean = pd.concat([y, X], axis=1).dropna()
        
        # Run OLS
        model = sm.OLS(data_clean[outcome_col], data_clean.drop(columns=[outcome_col]))
        results = model.fit(cov_type='HC1')  # Robust SE
        
        print("\n" + "="*70)
        print("DIFFERENCE-IN-DIFFERENCES REGRESSION")
        print("="*70)
        print(results.summary())
        
        # Highlight DiD coefficient
        did_coef = results.params['did_interaction']
        did_se = results.bse['did_interaction']
        did_pval = results.pvalues['did_interaction']
        
        print("\n" + "="*70)
        print("DiD TREATMENT EFFECT")
        print("="*70)
        print(f"Coefficient: {did_coef:.4f}")
        print(f"Std. Error: {did_se:.4f}")
        print(f"p-value: {did_pval:.4f}")
        print(f"Significance: {'***' if did_pval < 0.001 else '**' if did_pval < 0.01 else '*' if did_pval < 0.05 else 'Not significant'}")
        
        return results

# ============================================================================
# Moderation Analysis (Interaction Effects)
# ============================================================================

class ModerationAnalysis:
    """
    Test moderation (interaction) effects in panel data
    """
    
    @staticmethod
    def create_interaction(df, var1, var2, center=True):
        """
        Create interaction term between two variables
        
        Args:
            df: DataFrame
            var1: First variable name
            var2: Second variable name (moderator)
            center: Mean-center variables before interaction (default: True)
            
        Returns:
            DataFrame with interaction term
        """
        df_interact = df.copy()
        
        if center:
            df_interact[f"{var1}_c"] = df_interact[var1] - df_interact[var1].mean()
            df_interact[f"{var2}_c"] = df_interact[var2] - df_interact[var2].mean()
            df_interact[f"{var1}_x_{var2}"] = df_interact[f"{var1}_c"] * df_interact[f"{var2}_c"]
            print(f"✅ Created mean-centered interaction: {var1}_c × {var2}_c")
        else:
            df_interact[f"{var1}_x_{var2}"] = df_interact[var1] * df_interact[var2]
            print(f"✅ Created interaction: {var1} × {var2}")
        
        return df_interact
    
    @staticmethod
    def plot_simple_slopes(results, var1, var2, moderator_values=None):
        """
        Plot simple slopes for moderation effect
        
        Args:
            results: Regression results with interaction
            var1: Independent variable
            var2: Moderator variable
            moderator_values: Values of moderator to plot (default: ±1 SD)
        """
        if moderator_values is None:
            # Use ±1 SD
            moderator_values = [-1, 0, 1]  # Standardized values
        
        # Extract coefficients (simplified - adjust based on your model)
        # β1 = main effect of var1
        # β3 = interaction coefficient
        
        print("\n⚠️ Simple slopes plot: Implement based on your specific model")
        print("   Use marginal effects or manually calculate slopes at different moderator values")

# ============================================================================
# Robustness Checks
# ============================================================================

class RobustnessChecks:
    """
    Common robustness checks for strategy research
    """
    
    @staticmethod
    def alternative_dv(df_panel, alternative_dv, independent_vars):
        """
        Test with alternative dependent variable
        """
        print("\n" + "="*70)
        print(f"ROBUSTNESS: Alternative DV - {alternative_dv}")
        print("="*70)
        
        fe_analysis = FixedEffectsAnalysis()
        results = fe_analysis.run_fixed_effects(df_panel, alternative_dv, 
                                               independent_vars)
        
        print(results.summary)
        return results
    
    @staticmethod
    def subsample_analysis(df, subsample_condition, dependent_var, independent_vars):
        """
        Run analysis on subsample
        
        Args:
            df: Panel DataFrame
            subsample_condition: Boolean Series for subsample selection
            dependent_var: Dependent variable
            independent_vars: Independent variables
        """
        df_sub = df[subsample_condition]
        
        print("\n" + "="*70)
        print(f"ROBUSTNESS: Subsample Analysis")
        print(f"Subsample size: {len(df_sub)} observations")
        print("="*70)
        
        fe_analysis = FixedEffectsAnalysis()
        results = fe_analysis.run_fixed_effects(df_sub, dependent_var, 
                                               independent_vars)
        
        print(results.summary)
        return results
    
    @staticmethod
    def exclude_crisis_years(df_panel, crisis_years):
        """
        Exclude crisis years (e.g., 2008-2009 financial crisis)
        
        Args:
            df_panel: Panel DataFrame with MultiIndex
            crisis_years: List of years to exclude
            
        Returns:
            Filtered DataFrame
        """
        time_index = df_panel.index.get_level_values(1)
        df_filtered = df_panel[~time_index.isin(crisis_years)]
        
        print(f"✅ Excluded crisis years: {crisis_years}")
        print(f"   Remaining observations: {len(df_filtered)}")
        
        return df_filtered

# ============================================================================
# Descriptive Statistics for Panel Data
# ============================================================================

class PanelDescriptives:
    """
    Generate descriptive statistics for panel data
    """
    
    @staticmethod
    def summary_stats(df, variables):
        """
        Generate summary statistics table
        """
        stats_df = df[variables].describe().T
        stats_df['missing'] = df[variables].isnull().sum()
        stats_df['missing_pct'] = (stats_df['missing'] / len(df)) * 100
        
        print("\n" + "="*70)
        print("DESCRIPTIVE STATISTICS")
        print("="*70)
        print(stats_df.round(3))
        
        return stats_df
    
    @staticmethod
    def correlation_matrix(df, variables):
        """
        Generate correlation matrix with significance stars
        """
        corr = df[variables].corr()
        
        # Calculate p-values
        n = len(df)
        pvals = pd.DataFrame(np.zeros(corr.shape), 
                           columns=corr.columns, 
                           index=corr.index)
        
        for i in range(len(corr)):
            for j in range(i, len(corr)):
                if i != j:
                    r = corr.iloc[i, j]
                    t_stat = r * np.sqrt(n - 2) / np.sqrt(1 - r**2)
                    p = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))
                    pvals.iloc[i, j] = p
                    pvals.iloc[j, i] = p
        
        # Add significance stars
        corr_str = corr.copy().astype(str)
        for i in range(len(corr)):
            for j in range(len(corr)):
                if i != j:
                    p = pvals.iloc[i, j]
                    if p < 0.001:
                        corr_str.iloc[i, j] += '***'
                    elif p < 0.01:
                        corr_str.iloc[i, j] += '**'
                    elif p < 0.05:
                        corr_str.iloc[i, j] += '*'
        
        print("\n" + "="*70)
        print("CORRELATION MATRIX")
        print("="*70)
        print("*** p<0.001, ** p<0.01, * p<0.05")
        print(corr_str)
        
        return corr, pvals
    
    @staticmethod
    def vif_analysis(df, variables):
        """
        Calculate Variance Inflation Factor (VIF) for multicollinearity check
        """
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        
        X = df[variables].dropna()
        
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                          for i in range(len(X.columns))]
        
        print("\n" + "="*70)
        print("MULTICOLLINEARITY CHECK (VIF)")
        print("="*70)
        print("Rule of thumb: VIF > 10 indicates high multicollinearity")
        print(vif_data.round(2))
        
        if (vif_data["VIF"] > 10).any():
            print("\n⚠️ WARNING: High multicollinearity detected!")
            high_vif = vif_data[vif_data["VIF"] > 10]
            print(f"   Variables with VIF > 10: {', '.join(high_vif['Variable'])}")
        
        return vif_data

# ============================================================================
# Example Workflow
# ============================================================================

def example_workflow():
    """
    Demonstrate complete panel data analysis workflow
    """
    print("="*70)
    print("PANEL DATA ANALYSIS - EXAMPLE WORKFLOW")
    print("="*70)
    
    # 1. Generate sample data
    np.random.seed(42)
    n_firms = 100
    n_years = 10
    
    firms = np.repeat(range(n_firms), n_years)
    years = np.tile(range(2014, 2024), n_firms)
    
    df = pd.DataFrame({
        'firm_id': firms,
        'year': years,
        'roa': np.random.normal(0.05, 0.10, n_firms * n_years),
        'log_assets': np.random.normal(8, 2, n_firms * n_years),
        'leverage': np.random.uniform(0, 0.8, n_firms * n_years),
        'rd_intensity': np.random.uniform(0, 0.15, n_firms * n_years),
        'age': np.random.randint(5, 50, n_firms * n_years)
    })
    
    # Add firm fixed effect
    firm_effects = np.random.normal(0, 0.02, n_firms)
    df['roa'] += np.repeat(firm_effects, n_years)
    
    print(f"\n✅ Generated sample data: {n_firms} firms × {n_years} years")
    
    # 2. Convert to panel format
    prep = PanelDataPrep()
    df_panel = prep.create_panel_dataset(df, 'firm_id', 'year')
    
    # 3. Create lagged variables
    df_panel = prep.create_lagged_variables(df_panel, ['rd_intensity'], lags=1)
    
    # 4. Descriptive statistics
    descriptives = PanelDescriptives()
    stats = descriptives.summary_stats(df_panel, 
                                      ['roa', 'log_assets', 'leverage', 'rd_intensity'])
    
    corr, pvals = descriptives.correlation_matrix(df_panel, 
                                                  ['roa', 'log_assets', 'leverage', 'rd_intensity'])
    
    vif = descriptives.vif_analysis(df_panel, 
                                   ['log_assets', 'leverage', 'rd_intensity'])
    
    # 5. Fixed Effects Regression
    fe_analysis = FixedEffectsAnalysis()
    
    # Model 1: Controls only
    model1 = fe_analysis.run_fixed_effects(
        df_panel, 
        dependent_var='roa',
        independent_vars=['log_assets', 'leverage']
    )
    
    # Model 2: Add R&D
    model2 = fe_analysis.run_fixed_effects(
        df_panel,
        dependent_var='roa',
        independent_vars=['log_assets', 'leverage', 'rd_intensity']
    )
    
    # 6. Compare models
    models_dict = {'Model 1': model1, 'Model 2': model2}
    comparison = fe_analysis.compare_models(models_dict, ['Controls', 'Full Model'])
    
    print("\n" + "="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)
    print("Next steps:")
    print("1. Adapt this code to your actual data")
    print("2. Add your specific variables and hypotheses")
    print("3. Run robustness checks")
    print("4. Create regression tables for your paper")
    
    return df_panel, model1, model2

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution
    """
    example_workflow()

if __name__ == "__main__":
    main()
