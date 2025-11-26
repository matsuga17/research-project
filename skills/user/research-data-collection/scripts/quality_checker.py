"""
Data Quality Checker for Research Data Collection
Performs comprehensive quality assurance checks on collected data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
from pathlib import Path

class DataQualityChecker:
    """Comprehensive data quality checker for empirical research"""
    
    def __init__(self, data: pd.DataFrame, project_name: str = "research_project"):
        self.data = data
        self.project_name = project_name
        self.issues = []
        self.report = {}
        
    def run_all_checks(self) -> Dict:
        """Run all quality checks and generate comprehensive report"""
        print(f"Running quality checks for: {self.project_name}")
        print(f"Dataset: {len(self.data)} rows × {len(self.data.columns)} columns\n")
        
        self.check_completeness()
        self.check_consistency()
        self.check_duplicates()
        self.check_outliers()
        self.check_temporal_consistency()
        
        self.report["summary"] = self._generate_summary()
        self.report["issues"] = self.issues
        self.report["timestamp"] = datetime.now().isoformat()
        
        return self.report
    
    def check_completeness(self) -> Dict:
        """Check data completeness (missing values, expected vs actual records)"""
        print("=" * 60)
        print("COMPLETENESS CHECK")
        print("=" * 60)
        
        total_cells = self.data.shape[0] * self.data.shape[1]
        missing_cells = self.data.isna().sum().sum()
        completeness_rate = ((total_cells - missing_cells) / total_cells) * 100
        
        # Missing values by column
        missing_by_column = self.data.isna().sum()
        missing_pct = (missing_by_column / len(self.data)) * 100
        
        print(f"Overall Completeness: {completeness_rate:.2f}%")
        print(f"Total Missing Cells: {missing_cells:,} / {total_cells:,}\n")
        
        # Report columns with > 5% missing
        high_missing = missing_pct[missing_pct > 5].sort_values(ascending=False)
        if len(high_missing) > 0:
            print("⚠️  Columns with >5% missing data:")
            for col, pct in high_missing.items():
                print(f"   {col}: {pct:.1f}% missing ({int(missing_by_column[col]):,} values)")
                self.issues.append({
                    "type": "high_missing_rate",
                    "column": col,
                    "missing_pct": float(pct),
                    "severity": "high" if pct > 20 else "medium"
                })
        else:
            print("✓ All columns have <5% missing data")
        
        self.report["completeness"] = {
            "overall_rate": float(completeness_rate),
            "total_missing": int(missing_cells),
            "columns_with_high_missing": len(high_missing),
            "missing_by_column": missing_by_column.to_dict()
        }
        
        print()
        return self.report["completeness"]
    
    def check_consistency(self) -> Dict:
        """Check data consistency (types, ranges, logical consistency)"""
        print("=" * 60)
        print("CONSISTENCY CHECK")
        print("=" * 60)
        
        consistency_issues = []
        
        # 1. Check data types
        print("Data Types:")
        for col in self.data.columns:
            dtype = self.data[col].dtype
            print(f"   {col}: {dtype}")
            
            # Check if numeric column has unexpected string values
            if dtype == 'object':
                try:
                    pd.to_numeric(self.data[col], errors='raise')
                    consistency_issues.append({
                        "type": "type_mismatch",
                        "column": col,
                        "issue": "Column appears numeric but stored as object",
                        "severity": "low"
                    })
                except:
                    pass
        
        # 2. Check for negative values in columns that should be positive
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if any(keyword in col.lower() for keyword in ['count', 'size', 'number', 'age']):
                negative_count = (self.data[col] < 0).sum()
                if negative_count > 0:
                    print(f"\n⚠️  {col} has {negative_count} negative values (may be unexpected)")
                    consistency_issues.append({
                        "type": "negative_values",
                        "column": col,
                        "count": int(negative_count),
                        "severity": "medium"
                    })
        
        # 3. Check ranges for percentage columns
        for col in numeric_cols:
            if any(keyword in col.lower() for keyword in ['percent', 'pct', 'rate', 'ratio']):
                out_of_range = ((self.data[col] < 0) | (self.data[col] > 100)).sum()
                if out_of_range > 0:
                    print(f"\n⚠️  {col} has {out_of_range} values outside 0-100 range")
                    consistency_issues.append({
                        "type": "range_violation",
                        "column": col,
                        "count": int(out_of_range),
                        "severity": "high"
                    })
        
        if not consistency_issues:
            print("\n✓ No major consistency issues detected")
        
        self.issues.extend(consistency_issues)
        self.report["consistency"] = {
            "issues_found": len(consistency_issues),
            "details": consistency_issues
        }
        
        print()
        return self.report["consistency"]
    
    def check_duplicates(self) -> Dict:
        """Check for duplicate records"""
        print("=" * 60)
        print("DUPLICATE CHECK")
        print("=" * 60)
        
        # Full row duplicates
        full_duplicates = self.data.duplicated().sum()
        duplicate_pct = (full_duplicates / len(self.data)) * 100
        
        print(f"Full Row Duplicates: {full_duplicates} ({duplicate_pct:.2f}%)")
        
        if full_duplicates > 0:
            self.issues.append({
                "type": "full_duplicates",
                "count": int(full_duplicates),
                "percentage": float(duplicate_pct),
                "severity": "high" if duplicate_pct > 1 else "medium"
            })
            print(f"⚠️  Found {full_duplicates} exact duplicate rows")
        else:
            print("✓ No exact duplicate rows found")
        
        # Check for duplicates in potential ID columns
        id_candidates = [col for col in self.data.columns 
                         if any(keyword in col.lower() for keyword in ['id', 'key', 'code'])]
        
        if id_candidates:
            print(f"\nChecking potential ID columns: {id_candidates}")
            for col in id_candidates:
                dup_count = self.data[col].duplicated().sum()
                if dup_count > 0:
                    print(f"⚠️  {col} has {dup_count} duplicate values")
                    self.issues.append({
                        "type": "id_duplicates",
                        "column": col,
                        "count": int(dup_count),
                        "severity": "high"
                    })
        
        self.report["duplicates"] = {
            "full_row_duplicates": int(full_duplicates),
            "duplicate_percentage": float(duplicate_pct)
        }
        
        print()
        return self.report["duplicates"]
    
    def check_outliers(self, method: str = "iqr", threshold: float = 3.0) -> Dict:
        """
        Detect outliers in numeric columns
        
        Args:
            method: 'iqr' (Interquartile Range) or 'zscore'
            threshold: For IQR: multiplier (default 3.0), for zscore: number of std devs
        """
        print("=" * 60)
        print(f"OUTLIER DETECTION ({method.upper()} method)")
        print("=" * 60)
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outlier_summary = {}
        
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            
            if len(col_data) == 0:
                continue
            
            if method == "iqr":
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers = ((col_data < lower_bound) | (col_data > upper_bound)).sum()
            
            elif method == "zscore":
                z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
                outliers = (z_scores > threshold).sum()
            
            outlier_pct = (outliers / len(col_data)) * 100
            
            if outliers > 0:
                print(f"{col}: {outliers} outliers ({outlier_pct:.2f}%)")
                outlier_summary[col] = {
                    "count": int(outliers),
                    "percentage": float(outlier_pct)
                }
                
                if outlier_pct > 5:
                    self.issues.append({
                        "type": "high_outlier_rate",
                        "column": col,
                        "outlier_pct": float(outlier_pct),
                        "severity": "medium"
                    })
        
        if not outlier_summary:
            print("✓ No significant outliers detected")
        
        self.report["outliers"] = outlier_summary
        
        print()
        return self.report["outliers"]
    
    def check_temporal_consistency(self) -> Dict:
        """Check temporal consistency for date/time columns"""
        print("=" * 60)
        print("TEMPORAL CONSISTENCY CHECK")
        print("=" * 60)
        
        date_cols = self.data.select_dtypes(include=['datetime64']).columns
        
        if len(date_cols) == 0:
            # Try to identify potential date columns
            potential_date_cols = [col for col in self.data.columns 
                                   if any(keyword in col.lower() 
                                         for keyword in ['date', 'time', 'year', 'month'])]
            
            if potential_date_cols:
                print(f"⚠️  Potential date columns not in datetime format: {potential_date_cols}")
                print("    Consider converting to datetime for temporal analysis")
            else:
                print("No date/time columns detected")
        else:
            for col in date_cols:
                col_data = self.data[col].dropna()
                
                if len(col_data) > 0:
                    min_date = col_data.min()
                    max_date = col_data.max()
                    date_range = (max_date - min_date).days
                    
                    print(f"\n{col}:")
                    print(f"   Range: {min_date.date()} to {max_date.date()}")
                    print(f"   Span: {date_range} days")
                    
                    # Check for future dates
                    future_dates = (col_data > pd.Timestamp.now()).sum()
                    if future_dates > 0:
                        print(f"   ⚠️  {future_dates} dates in the future")
                        self.issues.append({
                            "type": "future_dates",
                            "column": col,
                            "count": int(future_dates),
                            "severity": "medium"
                        })
                    
                    # Check for dates before reasonable threshold (e.g., 1900)
                    very_old_dates = (col_data < pd.Timestamp('1900-01-01')).sum()
                    if very_old_dates > 0:
                        print(f"   ⚠️  {very_old_dates} dates before 1900")
                        self.issues.append({
                            "type": "very_old_dates",
                            "column": col,
                            "count": int(very_old_dates),
                            "severity": "low"
                        })
        
        print()
        return {}
    
    def _generate_summary(self) -> Dict:
        """Generate overall quality summary"""
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        for issue in self.issues:
            severity_counts[issue.get("severity", "low")] += 1
        
        total_issues = len(self.issues)
        
        if total_issues == 0:
            quality_score = 100
            status = "EXCELLENT"
        elif severity_counts["high"] == 0 and severity_counts["medium"] <= 2:
            quality_score = 90
            status = "GOOD"
        elif severity_counts["high"] <= 2:
            quality_score = 70
            status = "ACCEPTABLE"
        else:
            quality_score = 50
            status = "NEEDS ATTENTION"
        
        return {
            "quality_score": quality_score,
            "status": status,
            "total_issues": total_issues,
            "issues_by_severity": severity_counts,
            "dataset_size": {
                "rows": len(self.data),
                "columns": len(self.data.columns)
            }
        }
    
    def print_summary(self):
        """Print executive summary"""
        print("\n" + "=" * 60)
        print("QUALITY ASSESSMENT SUMMARY")
        print("=" * 60)
        
        summary = self.report.get("summary", {})
        
        print(f"Quality Score: {summary.get('quality_score', 0)}/100")
        print(f"Status: {summary.get('status', 'UNKNOWN')}")
        print(f"\nTotal Issues: {summary.get('total_issues', 0)}")
        
        severity = summary.get('issues_by_severity', {})
        print(f"   High Severity: {severity.get('high', 0)}")
        print(f"   Medium Severity: {severity.get('medium', 0)}")
        print(f"   Low Severity: {severity.get('low', 0)}")
        
        print("\nRecommendations:")
        if summary.get('quality_score', 0) >= 90:
            print("✓ Data quality is excellent. Proceed with analysis.")
        elif summary.get('quality_score', 0) >= 70:
            print("• Review and address high-severity issues before analysis.")
        else:
            print("⚠️  Significant quality issues detected.")
            print("• Review all issues and consider data cleaning or re-collection.")
        
        print("=" * 60 + "\n")
    
    def save_report(self, output_path: str = "quality_report.json"):
        """Save quality report to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        
        print(f"Quality report saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    # Example with sample data
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 5],  # Note: duplicate ID
        'value': [100, 200, 300, 999999, 250, 260],  # Note: one outlier
        'percentage': [10.5, 20.3, 15.8, 110.0, 18.2, 22.1],  # Note: one > 100
        'date': pd.to_datetime(['2023-01-01', '2023-02-01', None, '2023-04-01', '2023-05-01', '2023-06-01']),
        'category': ['A', 'B', 'A', 'B', 'A', 'B']
    })
    
    # Run quality checks
    checker = DataQualityChecker(sample_data, project_name="example_project")
    report = checker.run_all_checks()
    checker.print_summary()
    
    # Save report
    # checker.save_report("quality_report.json")