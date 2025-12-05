import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


def detect_and_construct_date_column(df):
    """
    Detects existing date columns or constructs one from year/month/quarter components.
    
    Returns:
        tuple: (date_series, date_column_name, construction_method)
               date_series: pandas Series with datetime values
               date_column_name: str name of the column
               construction_method: str description of how date was obtained
    """
    # Month name to number mapping
    month_mapping = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'sept': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }
    
    # Quarter to month mapping (start of quarter)
    quarter_mapping = {
        'q1': 1, 'Q1': 1, 'quarter 1': 1,
        'q2': 4, 'Q2': 4, 'quarter 2': 4,
        'q3': 7, 'Q3': 7, 'quarter 3': 7,
        'q4': 10, 'Q4': 10, 'quarter 4': 10
    }
    
    # Priority 1: Look for explicit date columns (must be object/string type)
    date_keywords = ['date', 'time', 'datetime', 'timestamp']
    for col in df.columns:
        if any(keyword in col.lower() for keyword in date_keywords):
            # Only process if column is string/object type (not numeric)
            if df[col].dtype == 'object':
                try:
                    date_series = pd.to_datetime(df[col], errors='coerce')
                    if date_series.notna().sum() > len(df) * 0.5:  # At least 50% valid dates
                        return date_series, col, "existing_column"
                except:
                    continue
    
    # Priority 2: Construct from year + month + day
    year_cols = [c for c in df.columns if c.lower() in ['year', 'yr', 'yyyy']]
    month_cols = [c for c in df.columns if c.lower() in ['month', 'mon', 'mm', 'mnth']]
    day_cols = [c for c in df.columns if c.lower() in ['day', 'dd', 'date', 'dt']]
    
    if year_cols and month_cols and day_cols:
        try:
            year_col = year_cols[0]
            month_col = month_cols[0]
            day_col = day_cols[0]
            
            # Convert month names to numbers if needed
            month_series = df[month_col].copy()
            if month_series.dtype == 'object':
                month_series = month_series.str.lower().map(month_mapping)
            
            date_series = pd.to_datetime({
                'year': df[year_col],
                'month': month_series,
                'day': df[day_col]
            }, errors='coerce')
            
            if date_series.notna().sum() > len(df) * 0.5:
                return date_series, 'constructed_date', "year_month_day"
        except:
            pass
    
    # Priority 3: Construct from year + month (day = 1)
    if year_cols and month_cols:
        try:
            year_col = year_cols[0]
            month_col = month_cols[0]
            
            # Convert month names to numbers if needed
            month_series = df[month_col].copy()
            if month_series.dtype == 'object':
                month_series = month_series.str.lower().map(month_mapping)
            
            date_series = pd.to_datetime({
                'year': df[year_col],
                'month': month_series,
                'day': 1
            }, errors='coerce')
            
            if date_series.notna().sum() > len(df) * 0.5:
                return date_series, 'constructed_date', "year_month"
        except:
            pass
    
    # Priority 4: Construct from year + quarter
    quarter_cols = [c for c in df.columns if c.lower() in ['quarter', 'q', 'qtr', 'quarters']]
    
    if year_cols and quarter_cols:
        try:
            year_col = year_cols[0]
            quarter_col = quarter_cols[0]
            
            # Convert quarter to month (start of quarter)
            quarter_series = df[quarter_col].copy()
            if quarter_series.dtype == 'object':
                quarter_series = quarter_series.str.lower().map(quarter_mapping)
            else:
                # If numeric, assume 1-4 mapping to months 1, 4, 7, 10
                quarter_series = quarter_series.map({1: 1, 2: 4, 3: 7, 4: 10})
            
            date_series = pd.to_datetime({
                'year': df[year_col],
                'month': quarter_series,
                'day': 1
            }, errors='coerce')
            
            if date_series.notna().sum() > len(df) * 0.5:
                return date_series, 'constructed_date', "year_quarter"
        except:
            pass
    
    return None, None, None


def select_important_categorical_columns(df, max_cols=8):
    """
    Selects the most important categorical columns for analysis.
    
    Criteria:
    - Unique value count between 2 and 50
    - Not an ID column
    - Prioritizes columns with higher information content
    """
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Filter out ID columns and columns with too many/few unique values
    candidates = []
    for col in categorical_cols:
        if 'id' in col.lower():
            continue
        unique_count = df[col].nunique()
        if 2 <= unique_count <= 50:
            # Calculate "information score" as uniqueness ratio
            info_score = unique_count / len(df)
            candidates.append((col, unique_count, info_score))
    
    # Sort by information score (prefer moderate uniqueness)
    # Optimal is around 5-20 unique values
    candidates.sort(key=lambda x: abs(x[2] - 0.1), reverse=False)
    
    # Return top max_cols
    return [col for col, _, _ in candidates[:max_cols]]


def select_important_numeric_columns(df, max_cols=8, exclude_cols=None):
    """
    Selects the most important numeric columns for visualization.
    
    Criteria:
    - Higher coefficient of variation (CV)
    - Excludes highly correlated duplicates
    """
    if exclude_cols is None:
        exclude_cols = []
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in exclude_cols]
    
    if len(numeric_cols) <= max_cols:
        return numeric_cols
    
    # Calculate coefficient of variation (CV) for each column
    cv_scores = {}
    for col in numeric_cols:
        data = df[col].dropna()
        if len(data) > 0 and data.mean() != 0:
            cv = data.std() / abs(data.mean())
            cv_scores[col] = cv
        else:
            cv_scores[col] = 0
    
    # Sort by CV (higher variation is more interesting)
    sorted_cols = sorted(cv_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select top columns, avoiding highly correlated pairs
    selected = []
    for col, _ in sorted_cols:
        if len(selected) >= max_cols:
            break
        
        # Check correlation with already selected columns
        add_column = True
        for selected_col in selected:
            try:
                corr = df[[col, selected_col]].corr().iloc[0, 1]
                if abs(corr) > 0.95:  # Too highly correlated
                    add_column = False
                    break
            except:
                pass
        
        if add_column:
            selected.append(col)
    
    return selected


def summarize_csv(file_path):
    """
    Comprehensively analyzes a CSV file and generates multiple visualizations.
    
    IMPROVEMENTS:
    1. Flexible date detection (from year/month/quarter components)
    2. Smart column selection for large datasets
    3. Robust error handling
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        str: Formatted comprehensive analysis of the dataset
    """
    summary = []
    charts_created = []
    warnings_list = []
    
    # Load CSV with error handling
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return f"❌ ERROR: Could not load CSV file.\nDetails: {str(e)}"
    
    # Basic info
    summary.append("=" * 60)
    summary.append("📊 DATA OVERVIEW")
    summary.append("=" * 60)
    summary.append(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")
    summary.append(f"\nColumns: {', '.join(df.columns.tolist())}")
    
    # Data types
    summary.append(f"\n📋 DATA TYPES:")
    for col, dtype in df.dtypes.items():
        summary.append(f"  • {col}: {dtype}")
    
    # Missing data analysis
    missing = df.isnull().sum().sum()
    missing_pct = (missing / (df.shape[0] * df.shape[1])) * 100 if df.shape[0] * df.shape[1] > 0 else 0
    summary.append(f"\n🔍 DATA QUALITY:")
    if missing:
        summary.append(f"Missing values: {missing:,} ({missing_pct:.2f}% of total data)")
        summary.append("Missing by column:")
        for col in df.columns:
            col_missing = df[col].isnull().sum()
            if col_missing > 0:
                col_pct = (col_missing / len(df)) * 100
                summary.append(f"  • {col}: {col_missing:,} ({col_pct:.1f}%)")
    else:
        summary.append("✓ No missing values - dataset is complete!")
    
    # Numeric analysis with error handling
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        try:
            summary.append(f"\n📈 NUMERICAL ANALYSIS:")
            summary.append(str(df[numeric_cols].describe()))
            
            # Correlations if multiple numeric columns
            if len(numeric_cols) > 1:
                summary.append(f"\n🔗 CORRELATIONS:")
                corr_matrix = df[numeric_cols].corr()
                
                # Show top correlations
                summary.append("Top correlations (absolute value):")
                corr_pairs = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        corr_pairs.append((
                            corr_matrix.columns[i],
                            corr_matrix.columns[j],
                            corr_matrix.iloc[i, j]
                        ))
                corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
                for col1, col2, corr_val in corr_pairs[:10]:
                    summary.append(f"  • {col1} ↔ {col2}: {corr_val:.3f}")
                
                # Create correlation heatmap
                try:
                    plt.figure(figsize=(12, 10))
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                               square=True, linewidths=1, fmt='.2f', cbar_kws={'shrink': 0.8})
                    plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
                    plt.tight_layout()
                    plt.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
                    plt.close()
                    charts_created.append('correlation_heatmap.png')
                except Exception as e:
                    warnings_list.append(f"Could not create correlation heatmap: {str(e)}")
        
        except Exception as e:
            warnings_list.append(f"Numeric analysis error: {str(e)}")
    
    # Categorical analysis with smart column selection
    try:
        categorical_cols = select_important_categorical_columns(df, max_cols=8)
        
        if categorical_cols:
            summary.append(f"\n📊 CATEGORICAL ANALYSIS:")
            summary.append(f"Showing {len(categorical_cols)} most informative categorical columns")
            
            for col in categorical_cols:
                value_counts = df[col].value_counts()
                summary.append(f"\n{col}:")
                for val, count in value_counts.head(10).items():
                    pct = (count / len(df)) * 100
                    summary.append(f"  • {val}: {count:,} ({pct:.1f}%)")
                if len(value_counts) > 10:
                    summary.append(f"  ... and {len(value_counts) - 10} more values")
            
            # Categorical distributions visualization
            if categorical_cols:
                try:
                    n_cols_to_plot = min(4, len(categorical_cols))
                    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
                    axes = axes.flatten()
                    
                    for idx, col in enumerate(categorical_cols[:4]):
                        value_counts = df[col].value_counts().head(10)
                        axes[idx].barh(range(len(value_counts)), value_counts.values, color='steelblue')
                        axes[idx].set_yticks(range(len(value_counts)))
                        axes[idx].set_yticklabels(value_counts.index)
                        axes[idx].set_title(f'Top Values in {col}', fontweight='bold')
                        axes[idx].set_xlabel('Count')
                        axes[idx].grid(True, alpha=0.3, axis='x')
                    
                    # Hide unused subplots
                    for idx in range(len(categorical_cols[:4]), 4):
                        axes[idx].set_visible(False)
                    
                    plt.tight_layout()
                    plt.savefig('categorical_distributions.png', dpi=150, bbox_inches='tight')
                    plt.close()
                    charts_created.append('categorical_distributions.png')
                except Exception as e:
                    warnings_list.append(f"Could not create categorical distribution plots: {str(e)}")
    
    except Exception as e:
        warnings_list.append(f"Categorical analysis error: {str(e)}")
    
    # Time series analysis with flexible date detection
    try:
        date_series, date_col_name, construction_method = detect_and_construct_date_column(df)
        
        if date_series is not None and date_series.notna().sum() > 0:
            summary.append(f"\n📅 TIME SERIES ANALYSIS:")
            summary.append(f"Date column: {date_col_name} ({construction_method})")
            
            valid_dates = date_series.dropna()
            if len(valid_dates) > 0:
                date_range = valid_dates.max() - valid_dates.min()
                summary.append(f"Date range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
                summary.append(f"Span: {date_range.days} days")
                
                # Select important numeric columns for time series
                ts_numeric_cols = select_important_numeric_columns(df, max_cols=8)
                
                if ts_numeric_cols:
                    try:
                        n_plots = min(4, len(ts_numeric_cols))
                        fig, axes = plt.subplots(n_plots, 1, figsize=(14, 4 * n_plots))
                        if n_plots == 1:
                            axes = [axes]
                        
                        # Create temporary dataframe with date
                        temp_df = df.copy()
                        temp_df['_date_'] = date_series
                        temp_df = temp_df.dropna(subset=['_date_'])
                        temp_df = temp_df.sort_values('_date_')
                        
                        for idx, num_col in enumerate(ts_numeric_cols[:4]):
                            ax = axes[idx]
                            
                            # Group by date and aggregate
                            daily_data = temp_df.groupby('_date_')[num_col].agg(['mean', 'sum', 'count'])
                            
                            # Plot mean trend
                            daily_data['mean'].plot(ax=ax, label='Average', linewidth=2, color='steelblue')
                            
                            # Add trend line
                            if len(daily_data) > 2:
                                z = np.polyfit(range(len(daily_data)), daily_data['mean'].values, 1)
                                p = np.poly1d(z)
                                ax.plot(daily_data.index, p(range(len(daily_data))), 
                                       "--", alpha=0.6, color='red', label='Trend')
                            
                            ax.set_title(f'{num_col} Over Time', fontweight='bold', fontsize=12)
                            ax.set_xlabel('Date')
                            ax.set_ylabel(num_col)
                            ax.legend()
                            ax.grid(True, alpha=0.3)
                        
                        plt.tight_layout()
                        plt.savefig('time_series_analysis.png', dpi=150, bbox_inches='tight')
                        plt.close()
                        charts_created.append('time_series_analysis.png')
                    except Exception as e:
                        warnings_list.append(f"Could not create time series plots: {str(e)}")
        else:
            summary.append(f"\n📅 TIME SERIES ANALYSIS:")
            summary.append("⚠️  No date columns found or could not construct date from available columns")
    
    except Exception as e:
        warnings_list.append(f"Time series analysis error: {str(e)}")
    
    # Distribution plots for selected numeric columns
    if numeric_cols:
        try:
            dist_cols = select_important_numeric_columns(df, max_cols=8)
            n_cols_to_plot = min(4, len(dist_cols))
            
            if n_cols_to_plot > 0:
                fig, axes = plt.subplots(2, 2, figsize=(12, 10))
                axes = axes.flatten()
                
                for idx, col in enumerate(dist_cols[:4]):
                    data = df[col].dropna()
                    axes[idx].hist(data, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
                    axes[idx].set_title(f'Distribution of {col}', fontweight='bold')
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
                    axes[idx].grid(True, alpha=0.3)
                    
                    # Add mean and median lines
                    axes[idx].axvline(data.mean(), color='red', linestyle='--', 
                                     linewidth=2, label=f'Mean: {data.mean():.2f}')
                    axes[idx].axvline(data.median(), color='green', linestyle='--', 
                                     linewidth=2, label=f'Median: {data.median():.2f}')
                    axes[idx].legend()
                
                # Hide unused subplots
                for idx in range(n_cols_to_plot, 4):
                    axes[idx].set_visible(False)
                
                plt.tight_layout()
                plt.savefig('distributions.png', dpi=150, bbox_inches='tight')
                plt.close()
                charts_created.append('distributions.png')
        except Exception as e:
            warnings_list.append(f"Could not create distribution plots: {str(e)}")
    
    # Summary of visualizations
    if charts_created:
        summary.append(f"\n📊 VISUALIZATIONS CREATED:")
        for chart in charts_created:
            summary.append(f"  ✓ {chart}")
    
    # Warnings section
    if warnings_list:
        summary.append(f"\n⚠️  WARNINGS:")
        for warning in warnings_list:
            summary.append(f"  • {warning}")
    
    summary.append("\n" + "=" * 60)
    summary.append("✅ COMPREHENSIVE ANALYSIS COMPLETE")
    summary.append("=" * 60)
    
    return "\n".join(summary)


if __name__ == "__main__":
    # Test with sample data
    import sys
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "resources/sample.csv"
    
    print(summarize_csv(file_path))
