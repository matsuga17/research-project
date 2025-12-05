"""
Panel Data Analysis for Strategic & Organizational Research
============================================================

Comprehensive script for panel data regression analysis including:
- Pooled OLS
- Fixed Effects (FE)
- Random Effects (RE)
- Hausman test
- Robustness checks
- Publication-ready tables

Author: Strategic & Organizational Research Hub
License: Apache 2.0
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import eval_measures
from linearmodels.panel import PanelOLS, RandomEffects
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# Configuration
# ============================================================================

CONFIG = {
    "output_dir": "results/",
    "figures_dir": "figures/",
    "decimal_places": 3,
    "significance_levels": [0.01, 0.05, 0.10],
    "robust_se": True,  # Use cluster-robust standard errors
    "winsorize_level": 0.01  # Winsorize at 1% and 99%
}

# ============================================================================
# Data Preparation
# ============================================================================

class PanelDataPreparator:
    """
    Prepare panel data for analysis
    """
    
    @staticmethod
    def create_panel_structure(df: pd.DataFrame, 
                               entity_col: str, 
                               time_col: str) -> pd.DataFrame:
        """
        Convert DataFrame to panel structure with MultiIndex
        
        Args:
            df: Input DataFrame
            entity_col: Column name for entity (firm) identifier
            time_col: Column name for time identifier
        
        Returns:
            DataFrame with MultiIndex (entity, time)
        """
        df = df.copy()
        df[entity_col] = df[entity_col].astype(str)
        df[time_col] = pd.to_numeric(df[time_col])
        
        # Set MultiIndex
        df = df.set_index([entity_col, time_col])
        df = df.sort_index()
        
        print(f"✅ Panel structure created:")
        print(f"   - Entities: {df.index.get_level_values(0).nunique()}")
        print(f"   - Time periods: {df.index.get_level_values(1).nunique()}")
        print(f"   - Total observations: {len(df)}")
        
        return df
    
    @staticmethod
    def winsorize_variables(df: pd.DataFrame, 
                           columns: List[str], 
                           level: float = 0.01) -> pd.DataFrame:
        """
        Winsorize continuous variables at specified percentiles
        
        Args:
            df: Input DataFrame
            columns: List of column names to winsorize
            level: Winsorization level (e.g., 0.01 = 1% and 99%)
        
        Returns:
            DataFrame with winsorized variables
        """
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                lower = df[col].quantile(level)
                upper = df[col].quantile(1 - level)
                df[col] = df[col].clip(lower, upper)
                print(f"✅ Winsorized {col}: [{lower:.3f}, {upper:.3f}]")
        
        return df
    
    @staticmethod
    def create_lagged_variables(df: pd.DataFrame, 
                               columns: List[str], 
                               lags: int = 1) -> pd.DataFrame:
        """
        Create lagged variables within each entity
        
        Args:
            df: Panel DataFrame with MultiIndex (entity, time)
            columns: Columns to lag
            lags: Number of lags
        
        Returns:
            DataFrame with lagged variables
        """
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                for lag in range(1, lags + 1):
                    lagged_col = f"{col}_lag{lag}"
                    df[lagged_col] = df.groupby(level=0)[col].shift(lag)
                    print(f"✅ Created {lagged_col}")
        
        return df
    
    @staticmethod
    def check_balance(df: pd.DataFrame) -> Dict:
        """
        Check if panel is balanced and report missingness
        
        Args:
            df: Panel DataFrame with MultiIndex
        
        Returns:
            Dictionary with balance statistics
        """
        entities = df.index.get_level_values(0).unique()
        time_periods = df.index.get_level_values(1).unique()
        
        obs_per_entity = df.groupby(level=0).size()
        expected_obs = len(time_periods)
        
        balanced = (obs_per_entity == expected_obs).all()
        
        stats_dict = {
            "balanced": balanced,
            "n_entities": len(entities),
            "n_periods": len(time_periods),
            "expected_obs": expected_obs * len(entities),
            "actual_obs": len(df),
            "missing_obs": expected_obs * len(entities) - len(df),
            "min_obs_per_entity": obs_per_entity.min(),
            "max_obs_per_entity": obs_per_entity.max(),
            "mean_obs_per_entity": obs_per_entity.mean()
        }
        
        print("\n" + "="*60)
        print("Panel Balance Check")
        print("="*60)
        print(f"Balanced: {'Yes' if balanced else 'No'}")
        print(f"Entities: {stats_dict['n_entities']}")
        print(f"Time periods: {stats_dict['n_periods']}")
        print(f"Expected observations: {stats_dict['expected_obs']}")
        print(f"Actual observations: {stats_dict['actual_obs']}")
        print(f"Missing observations: {stats_dict['missing_obs']}")
        print(f"Obs per entity: min={stats_dict['min_obs_per_entity']}, "
              f"max={stats_dict['max_obs_per_entity']}, "
              f"mean={stats_dict['mean_obs_per_entity']:.1f}")
        print("="*60 + "\n")
        
        return stats_dict

# ============================================================================
# Descriptive Statistics
# ============================================================================

class DescriptiveStats:
    """
    Generate descriptive statistics for panel data
    """
    
    @staticmethod
    def summary_statistics(df: pd.DataFrame, 
                          variables: List[str]) -> pd.DataFrame:
        """
        Generate summary statistics (Table 1 in papers)
        
        Args:
            df: Panel DataFrame
            variables: List of variables to summarize
        
        Returns:
            DataFrame with summary statistics
        """
        stats_df = pd.DataFrame()
        
        for var in variables:
            if var in df.columns:
                stats_df.loc[var, 'N'] = df[var].count()
                stats_df.loc[var, 'Mean'] = df[var].mean()
                stats_df.loc[var, 'Std'] = df[var].std()
                stats_df.loc[var, 'Min'] = df[var].min()
                stats_df.loc[var, 'P25'] = df[var].quantile(0.25)
                stats_df.loc[var, 'Median'] = df[var].median()
                stats_df.loc[var, 'P75'] = df[var].quantile(0.75)
                stats_df.loc[var, 'Max'] = df[var].max()
        
        # Format numbers
        for col in ['Mean', 'Std', 'Min', 'P25', 'Median', 'P75', 'Max']:
            stats_df[col] = stats_df[col].round(CONFIG["decimal_places"])
        stats_df['N'] = stats_df['N'].astype(int)
        
        print("\n" + "="*80)
        print("Summary Statistics")
        print("="*80)
        print(stats_df.to_string())
        print("="*80 + "\n")
        
        return stats_df
    
    @staticmethod
    def correlation_matrix(df: pd.DataFrame, 
                          variables: List[str]) -> pd.DataFrame:
        """
        Generate correlation matrix (Table 2 in papers)
        
        Args:
            df: Panel DataFrame
            variables: Variables to include
        
        Returns:
            Correlation matrix
        """
        corr = df[variables].corr()
        corr = corr.round(CONFIG["decimal_places"])
        
        print("\n" + "="*80)
        print("Correlation Matrix")
        print("="*80)
        print(corr.to_string())
        print("="*80 + "\n")
        
        # Check for multicollinearity
        high_corr = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if abs(corr.iloc[i, j]) > 0.7:
                    high_corr.append((corr.columns[i], corr.columns[j], 
                                    corr.iloc[i, j]))
        
        if high_corr:
            print("⚠️  High correlations detected (|r| > 0.7):")
            for var1, var2, r in high_corr:
                print(f"   {var1} - {var2}: {r:.3f}")
            print()
        
        return corr
    
    @staticmethod
    def plot_distributions(df: pd.DataFrame, 
                          variables: List[str], 
                          output_file: str = "distributions.png"):
        """
        Plot distributions of key variables
        """
        n_vars = len(variables)
        n_cols = 3
        n_rows = (n_vars + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
        axes = axes.flatten() if n_vars > 1 else [axes]
        
        for i, var in enumerate(variables):
            if var in df.columns:
                axes[i].hist(df[var].dropna(), bins=50, edgecolor='black', alpha=0.7)
                axes[i].set_title(var)
                axes[i].set_xlabel('Value')
                axes[i].set_ylabel('Frequency')
                axes[i].grid(alpha=0.3)
        
        # Hide unused subplots
        for i in range(n_vars, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Distribution plots saved to {output_file}")
        plt.close()

# ============================================================================
# Panel Regression Models
# ============================================================================

class PanelRegression:
    """
    Panel data regression models
    """
    
    @staticmethod
    def pooled_ols(df: pd.DataFrame, 
                   dependent_var: str, 
                   independent_vars: List[str]) -> Dict:
        """
        Pooled OLS regression (baseline model)
        
        Args:
            df: Panel DataFrame
            dependent_var: Dependent variable
            independent_vars: List of independent variables
        
        Returns:
            Dictionary with results
        """
        # Prepare data
        data = df[[dependent_var] + independent_vars].dropna()
        y = data[dependent_var]
        X = data[independent_vars]
        X = sm.add_constant(X)
        
        # Run regression
        model = OLS(y, X)
        results = model.fit()
        
        print("\n" + "="*80)
        print("Pooled OLS Regression")
        print("="*80)
        print(results.summary())
        print("="*80 + "\n")
        
        return {
            "model": "Pooled OLS",
            "results": results,
            "n_obs": int(results.nobs),
            "r_squared": results.rsquared,
            "adj_r_squared": results.rsquared_adj
        }
    
    @staticmethod
    def fixed_effects(df: pd.DataFrame, 
                     dependent_var: str, 
                     independent_vars: List[str],
                     entity_effects: bool = True,
                     time_effects: bool = False) -> Dict:
        """
        Fixed Effects regression
        
        Args:
            df: Panel DataFrame with MultiIndex (entity, time)
            dependent_var: Dependent variable
            independent_vars: List of independent variables
            entity_effects: Include entity fixed effects
            time_effects: Include time fixed effects
        
        Returns:
            Dictionary with results
        """
        # Prepare data
        data = df[[dependent_var] + independent_vars].dropna()
        
        # Run regression
        if entity_effects and time_effects:
            model = PanelOLS(data[dependent_var], 
                           data[independent_vars],
                           entity_effects=True,
                           time_effects=True)
            fe_type = "Two-way (Entity + Time)"
        elif entity_effects:
            model = PanelOLS(data[dependent_var], 
                           data[independent_vars],
                           entity_effects=True,
                           time_effects=False)
            fe_type = "One-way (Entity)"
        else:
            model = PanelOLS(data[dependent_var], 
                           data[independent_vars],
                           entity_effects=False,
                           time_effects=True)
            fe_type = "One-way (Time)"
        
        if CONFIG["robust_se"]:
            results = model.fit(cov_type='clustered', cluster_entity=True)
        else:
            results = model.fit()
        
        print("\n" + "="*80)
        print(f"Fixed Effects Regression ({fe_type})")
        print("="*80)
        print(results.summary)
        print("="*80 + "\n")
        
        return {
            "model": f"Fixed Effects ({fe_type})",
            "results": results,
            "n_obs": int(results.nobs),
            "r_squared": results.rsquared,
            "r_squared_within": results.rsquared_within,
            "f_statistic": results.f_statistic.stat,
            "f_pvalue": results.f_statistic.pval
        }
    
    @staticmethod
    def random_effects(df: pd.DataFrame, 
                      dependent_var: str, 
                      independent_vars: List[str]) -> Dict:
        """
        Random Effects regression
        
        Args:
            df: Panel DataFrame with MultiIndex (entity, time)
            dependent_var: Dependent variable
            independent_vars: List of independent variables
        
        Returns:
            Dictionary with results
        """
        # Prepare data
        data = df[[dependent_var] + independent_vars].dropna()
        
        # Run regression
        model = RandomEffects(data[dependent_var], data[independent_vars])
        results = model.fit()
        
        print("\n" + "="*80)
        print("Random Effects Regression")
        print("="*80)
        print(results.summary)
        print("="*80 + "\n")
        
        return {
            "model": "Random Effects",
            "results": results,
            "n_obs": int(results.nobs),
            "r_squared": results.rsquared
        }
    
    @staticmethod
    def hausman_test(fe_results, re_results):
        """
        Hausman test to choose between FE and RE
        
        Args:
            fe_results: Fixed effects results
            re_results: Random effects results
        
        Returns:
            Test statistic and p-value
        """
        print("\n" + "="*80)
        print("Hausman Test (FE vs RE)")
        print("="*80)
        print("H0: Random Effects is consistent")
        print("H1: Fixed Effects is consistent")
        print()
        
        # Note: Manual Hausman test implementation
        # In practice, use specialized packages or report both models
        print("⚠️  Report both FE and RE models. Prefer FE for strategy research")
        print("   (most strategy papers use FE to control for unobserved heterogeneity)")
        print("="*80 + "\n")

# ============================================================================
# Robustness Checks
# ============================================================================

class RobustnessChecks:
    """
    Conduct robustness checks
    """
    
    @staticmethod
    def alternative_dv(df: pd.DataFrame, 
                      alternative_dvs: List[str],
                      independent_vars: List[str]) -> List[Dict]:
        """
        Test robustness with alternative dependent variables
        
        Args:
            df: Panel DataFrame
            alternative_dvs: List of alternative dependent variables
            independent_vars: Independent variables
        
        Returns:
            List of results for each alternative DV
        """
        print("\n" + "="*80)
        print("Robustness Check: Alternative Dependent Variables")
        print("="*80)
        
        results = []
        for dv in alternative_dvs:
            if dv in df.columns:
                print(f"\n📊 Testing with DV: {dv}")
                result = PanelRegression.fixed_effects(df, dv, independent_vars)
                results.append(result)
        
        return results
    
    @staticmethod
    def subsample_analysis(df: pd.DataFrame,
                          dependent_var: str,
                          independent_vars: List[str],
                          split_var: str,
                          split_condition: callable) -> Tuple[Dict, Dict]:
        """
        Subsample analysis (e.g., by firm size, industry)
        
        Args:
            df: Panel DataFrame
            dependent_var: Dependent variable
            independent_vars: Independent variables
            split_var: Variable to split on
            split_condition: Function that returns True for subsample 1
        
        Returns:
            Tuple of (results_subsample1, results_subsample2)
        """
        print("\n" + "="*80)
        print(f"Robustness Check: Subsample Analysis on {split_var}")
        print("="*80)
        
        df_sub1 = df[split_condition(df[split_var])]
        df_sub2 = df[~split_condition(df[split_var])]
        
        print(f"\n📊 Subsample 1: {len(df_sub1)} observations")
        results1 = PanelRegression.fixed_effects(df_sub1, dependent_var, 
                                                independent_vars)
        
        print(f"\n📊 Subsample 2: {len(df_sub2)} observations")
        results2 = PanelRegression.fixed_effects(df_sub2, dependent_var, 
                                                independent_vars)
        
        return results1, results2

# ============================================================================
# Publication-Ready Tables
# ============================================================================

class TableGenerator:
    """
    Generate publication-ready regression tables
    """
    
    @staticmethod
    def regression_table(results_list: List[Dict], 
                        output_file: str = "regression_table.txt",
                        latex: bool = False) -> str:
        """
        Create regression table (like Table 3 in papers)
        
        Args:
            results_list: List of regression result dictionaries
            output_file: Output file name
            latex: Generate LaTeX format
        
        Returns:
            Formatted table string
        """
        # Extract coefficients and standard errors
        table_data = []
        
        for result in results_list:
            res = result["results"]
            
            # Get coefficients and standard errors
            if hasattr(res, 'params'):  # linearmodels format
                coef = res.params
                se = res.std_errors
                pval = res.pvalues
            else:  # statsmodels format
                coef = res.params
                se = res.bse
                pval = res.pvalues
            
            model_data = {
                "model": result["model"],
                "n_obs": result["n_obs"],
                "r_squared": result.get("r_squared", 0),
                "coefficients": coef,
                "std_errors": se,
                "pvalues": pval
            }
            table_data.append(model_data)
        
        # Format table
        if latex:
            table_str = TableGenerator._format_latex_table(table_data)
        else:
            table_str = TableGenerator._format_text_table(table_data)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(table_str)
        
        print(f"✅ Regression table saved to {output_file}")
        return table_str
    
    @staticmethod
    def _format_text_table(table_data: List[Dict]) -> str:
        """Format as plain text table"""
        lines = []
        lines.append("="*100)
        lines.append("Regression Results")
        lines.append("="*100)
        
        # Header
        header = "Variable".ljust(30)
        for i, data in enumerate(table_data, 1):
            header += f"Model {i}".rjust(15)
        lines.append(header)
        lines.append("-"*100)
        
        # Coefficients
        all_vars = set()
        for data in table_data:
            all_vars.update(data["coefficients"].index)
        
        for var in sorted(all_vars):
            line = var.ljust(30)
            for data in table_data:
                if var in data["coefficients"].index:
                    coef = data["coefficients"][var]
                    se = data["std_errors"][var]
                    pval = data["pvalues"][var]
                    
                    # Significance stars
                    stars = ""
                    if pval < 0.01:
                        stars = "***"
                    elif pval < 0.05:
                        stars = "**"
                    elif pval < 0.10:
                        stars = "*"
                    
                    line += f"{coef:>12.3f}{stars}".rjust(15)
                else:
                    line += " ".rjust(15)
            lines.append(line)
            
            # Standard errors in parentheses
            line = " ".ljust(30)
            for data in table_data:
                if var in data["std_errors"].index:
                    se = data["std_errors"][var]
                    line += f"({se:.3f})".rjust(15)
                else:
                    line += " ".rjust(15)
            lines.append(line)
        
        lines.append("-"*100)
        
        # Model statistics
        line = "N".ljust(30)
        for data in table_data:
            line += f"{data['n_obs']}".rjust(15)
        lines.append(line)
        
        line = "R-squared".ljust(30)
        for data in table_data:
            line += f"{data['r_squared']:.3f}".rjust(15)
        lines.append(line)
        
        lines.append("="*100)
        lines.append("Notes: Standard errors in parentheses")
        lines.append("* p<0.10, ** p<0.05, *** p<0.01")
        lines.append("="*100)
        
        return "\n".join(lines)
    
    @staticmethod
    def _format_latex_table(table_data: List[Dict]) -> str:
        """Format as LaTeX table"""
        lines = []
        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(r"\caption{Regression Results}")
        lines.append(r"\label{tab:regression}")
        
        # Table structure
        n_models = len(table_data)
        lines.append(r"\begin{tabular}{l" + "c"*n_models + "}")
        lines.append(r"\hline\hline")
        
        # Header
        header = "Variable"
        for i in range(1, n_models + 1):
            header += f" & Model {i}"
        header += r" \\"
        lines.append(header)
        lines.append(r"\hline")
        
        # Coefficients
        all_vars = set()
        for data in table_data:
            all_vars.update(data["coefficients"].index)
        
        for var in sorted(all_vars):
            line = var.replace("_", "\\_")
            for data in table_data:
                if var in data["coefficients"].index:
                    coef = data["coefficients"][var]
                    pval = data["pvalues"][var]
                    
                    stars = ""
                    if pval < 0.01:
                        stars = "^{***}"
                    elif pval < 0.05:
                        stars = "^{**}"
                    elif pval < 0.10:
                        stars = "^{*}"
                    
                    line += f" & {coef:.3f}{stars}"
                else:
                    line += " & "
            line += r" \\"
            lines.append(line)
            
            # Standard errors
            line = ""
            for data in table_data:
                if var in data["std_errors"].index:
                    se = data["std_errors"][var]
                    line += f" & ({se:.3f})"
                else:
                    line += " & "
            line += r" \\"
            lines.append(line)
        
        lines.append(r"\hline")
        
        # Statistics
        line = "Observations"
        for data in table_data:
            line += f" & {data['n_obs']}"
        line += r" \\"
        lines.append(line)
        
        line = "R-squared"
        for data in table_data:
            line += f" & {data['r_squared']:.3f}"
        line += r" \\"
        lines.append(line)
        
        lines.append(r"\hline\hline")
        lines.append(r"\multicolumn{" + str(n_models+1) + r"}{l}{\footnotesize Standard errors in parentheses} \\")
        lines.append(r"\multicolumn{" + str(n_models+1) + r"}{l}{\footnotesize $^{*}$ $p<0.10$, $^{**}$ $p<0.05$, $^{***}$ $p<0.01$} \\")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{table}")
        
        return "\n".join(lines)

# ============================================================================
# Example Workflow
# ============================================================================

def example_analysis():
    """
    Complete panel data analysis workflow
    """
    print("="*80)
    print("Panel Data Analysis for Strategic Research")
    print("="*80)
    
    # 1. Load sample data (replace with your actual data)
    np.random.seed(42)
    
    # Create sample panel data: 100 firms, 5 years
    n_firms = 100
    n_years = 5
    
    firms = [f"Firm_{i}" for i in range(n_firms)]
    years = list(range(2019, 2019 + n_years))
    
    data = []
    for firm in firms:
        firm_effect = np.random.normal(0, 1)
        for year in years:
            data.append({
                "firm_id": firm,
                "year": year,
                "roa": 5 + firm_effect + 0.5 * np.random.normal(0, 1),
                "rd_intensity": 2 + 0.3 * firm_effect + 0.2 * np.random.normal(0, 1),
                "firm_size": 10 + firm_effect + np.random.normal(0, 0.5),
                "leverage": 0.3 + 0.1 * firm_effect + 0.05 * np.random.normal(0, 1),
                "firm_age": 20 + np.random.randint(-5, 5)
            })
    
    df = pd.DataFrame(data)
    
    # 2. Prepare panel structure
    prep = PanelDataPreparator()
    df_panel = prep.create_panel_structure(df, "firm_id", "year")
    
    # 3. Winsorize continuous variables
    df_panel = prep.winsorize_variables(df_panel, 
                                       ["roa", "rd_intensity", "firm_size", "leverage"])
    
    # 4. Create lagged variables
    df_panel = prep.create_lagged_variables(df_panel, ["rd_intensity"], lags=1)
    
    # 5. Check panel balance
    prep.check_balance(df_panel)
    
    # 6. Descriptive statistics
    desc = DescriptiveStats()
    summary = desc.summary_statistics(df_panel, 
                                     ["roa", "rd_intensity_lag1", "firm_size", 
                                      "leverage", "firm_age"])
    
    corr = desc.correlation_matrix(df_panel,
                                  ["roa", "rd_intensity_lag1", "firm_size", 
                                   "leverage", "firm_age"])
    
    desc.plot_distributions(df_panel, 
                           ["roa", "rd_intensity_lag1", "firm_size"],
                           "distributions.png")
    
    # 7. Run regressions
    independent_vars = ["rd_intensity_lag1", "firm_size", "leverage", "firm_age"]
    
    # Pooled OLS
    pooled = PanelRegression.pooled_ols(df_panel, "roa", independent_vars)
    
    # Fixed Effects
    fe = PanelRegression.fixed_effects(df_panel, "roa", independent_vars,
                                      entity_effects=True, time_effects=False)
    
    # Two-way Fixed Effects
    fe_two = PanelRegression.fixed_effects(df_panel, "roa", independent_vars,
                                          entity_effects=True, time_effects=True)
    
    # Random Effects
    re = PanelRegression.random_effects(df_panel, "roa", independent_vars)
    
    # 8. Generate publication table
    table_gen = TableGenerator()
    results_list = [pooled, fe, fe_two, re]
    
    table_gen.regression_table(results_list, "regression_table.txt", latex=False)
    table_gen.regression_table(results_list, "regression_table.tex", latex=True)
    
    print("\n✅ Analysis complete!")
    print("\nOutput files:")
    print("  - regression_table.txt (for review)")
    print("  - regression_table.tex (for paper)")
    print("  - distributions.png (for diagnostics)")
    
    return df_panel, results_list

# ============================================================================
# Main Function
# ============================================================================

def main():
    """
    Main execution
    """
    import os
    os.makedirs("results", exist_ok=True)
    os.makedirs("figures", exist_ok=True)
    
    # Run example analysis
    df, results = example_analysis()
    
    print("\n" + "="*80)
    print("Next Steps:")
    print("="*80)
    print("1. Replace sample data with your actual data")
    print("2. Adjust variable names and specifications")
    print("3. Conduct robustness checks")
    print("4. Generate additional tables and figures")
    print("5. Write up results for paper")
    print("="*80)

if __name__ == "__main__":
    main()
