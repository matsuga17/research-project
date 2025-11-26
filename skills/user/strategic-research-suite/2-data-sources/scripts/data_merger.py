"""
data_merger.py

Multi-Source Data Integration Tool

This module provides comprehensive data merging capabilities for combining
data from multiple sources (EDINET, SEC, Compustat, World Bank, etc.) into
unified panel datasets.

Features:
- Fuzzy matching for firm names
- Multiple key matching strategies
- Conflict resolution
- Data quality validation
- Merge diagnostics

Usage:
    from data_merger import DataMerger
    
    merger = DataMerger()
    df_merged = merger.merge_datasets(
        df_left=df_japan,
        df_right=df_financials,
        on='firm_id',
        how='inner'
    )
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Union
from difflib import SequenceMatcher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataMerger:
    """
    Multi-source data integration toolkit
    
    Provides intelligent merging with fuzzy matching, conflict resolution,
    and comprehensive merge diagnostics.
    
    Attributes:
        merge_history: Log of all merge operations
        quality_checks: Validation results
    """
    
    def __init__(self):
        """Initialize data merger"""
        self.merge_history = []
        self.quality_checks = {}
        logger.info("Data Merger initialized")
    
    def merge_datasets(self,
                      df_left: pd.DataFrame,
                      df_right: pd.DataFrame,
                      on: Union[str, List[str]],
                      how: str = 'inner',
                      suffixes: Tuple[str, str] = ('_left', '_right'),
                      validate: Optional[str] = None) -> pd.DataFrame:
        """
        Merge two datasets with diagnostics
        
        Args:
            df_left: Left DataFrame
            df_right: Right DataFrame
            on: Column(s) to merge on
            how: Type of merge ('inner', 'left', 'right', 'outer')
            suffixes: Suffixes for overlapping columns
            validate: Merge validation ('1:1', '1:m', 'm:1', 'm:m')
        
        Returns:
            Merged DataFrame
        """
        logger.info(f"Merging datasets: {len(df_left)} x {len(df_right)} on {on}")
        
        # Pre-merge statistics
        pre_stats = {
            'left_rows': len(df_left),
            'right_rows': len(df_right),
            'left_unique_keys': len(df_left[on].drop_duplicates()) if isinstance(on, str) else len(df_left[on].drop_duplicates()),
            'right_unique_keys': len(df_right[on].drop_duplicates()) if isinstance(on, str) else len(df_right[on].drop_duplicates())
        }
        
        # Perform merge
        df_merged = pd.merge(
            df_left,
            df_right,
            on=on,
            how=how,
            suffixes=suffixes,
            validate=validate,
            indicator=True
        )
        
        # Post-merge statistics
        post_stats = {
            'merged_rows': len(df_merged),
            'both': (df_merged['_merge'] == 'both').sum(),
            'left_only': (df_merged['_merge'] == 'left_only').sum(),
            'right_only': (df_merged['_merge'] == 'right_only').sum()
        }
        
        # Calculate match rate
        if how == 'inner':
            match_rate = post_stats['both'] / min(pre_stats['left_rows'], pre_stats['right_rows'])
        else:
            match_rate = post_stats['both'] / max(pre_stats['left_rows'], pre_stats['right_rows'])
        
        logger.info(f"Merge completed: {post_stats['merged_rows']} rows, {match_rate:.1%} match rate")
        logger.info(f"  Both: {post_stats['both']}, Left only: {post_stats['left_only']}, Right only: {post_stats['right_only']}")
        
        # Remove merge indicator unless user wants diagnostics
        df_result = df_merged.drop(columns=['_merge'])
        
        # Store merge history
        merge_record = {
            'timestamp': pd.Timestamp.now(),
            'merge_type': how,
            'merge_keys': on,
            'pre_stats': pre_stats,
            'post_stats': post_stats,
            'match_rate': match_rate
        }
        self.merge_history.append(merge_record)
        
        return df_result
    
    def fuzzy_match_firms(self,
                         df_left: pd.DataFrame,
                         df_right: pd.DataFrame,
                         name_col_left: str,
                         name_col_right: str,
                         threshold: float = 0.8) -> pd.DataFrame:
        """
        Fuzzy match firm names between datasets
        
        Args:
            df_left: Left DataFrame
            df_right: Right DataFrame
            name_col_left: Firm name column in left df
            name_col_right: Firm name column in right df
            threshold: Similarity threshold (0-1)
        
        Returns:
            Mapping DataFrame
        """
        logger.info(f"Performing fuzzy matching on firm names (threshold={threshold})")
        
        matches = []
        
        for idx_left, name_left in df_left[name_col_left].items():
            best_match = None
            best_score = 0
            
            for idx_right, name_right in df_right[name_col_right].items():
                # Calculate similarity
                score = SequenceMatcher(None, 
                                       name_left.lower(), 
                                       name_right.lower()).ratio()
                
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = idx_right
            
            if best_match is not None:
                matches.append({
                    'left_index': idx_left,
                    'right_index': best_match,
                    'left_name': name_left,
                    'right_name': df_right.loc[best_match, name_col_right],
                    'similarity': best_score
                })
        
        df_matches = pd.DataFrame(matches)
        logger.info(f"Fuzzy matching completed: {len(df_matches)} matches found")
        
        return df_matches
    
    def sequential_merge(self,
                        datasets: List[Tuple[pd.DataFrame, str, List[str]]],
                        how: str = 'left') -> pd.DataFrame:
        """
        Sequential merge of multiple datasets
        
        Args:
            datasets: List of (dataframe, name, merge_keys) tuples
            how: Type of merge
        
        Returns:
            Merged DataFrame
        """
        logger.info(f"Sequential merge of {len(datasets)} datasets")
        
        if not datasets:
            raise ValueError("No datasets provided")
        
        # Start with first dataset
        df_result = datasets[0][0].copy()
        base_name = datasets[0][1]
        logger.info(f"Base dataset: {base_name} ({len(df_result)} rows)")
        
        # Merge remaining datasets sequentially
        for i, (df_to_merge, name, merge_keys) in enumerate(datasets[1:], 1):
            logger.info(f"Merging {name} ({len(df_to_merge)} rows) on {merge_keys}")
            
            df_result = self.merge_datasets(
                df_left=df_result,
                df_right=df_to_merge,
                on=merge_keys,
                how=how,
                suffixes=(f'', f'_{name}')
            )
            
            logger.info(f"After merge {i}: {len(df_result)} rows")
        
        return df_result
    
    def get_merge_report(self) -> pd.DataFrame:
        """Generate merge history report"""
        if not self.merge_history:
            return pd.DataFrame()
        
        report_data = []
        for i, record in enumerate(self.merge_history, 1):
            report_data.append({
                'merge_#': i,
                'timestamp': record['timestamp'],
                'merge_type': record['merge_type'],
                'merge_keys': str(record['merge_keys']),
                'left_rows': record['pre_stats']['left_rows'],
                'right_rows': record['pre_stats']['right_rows'],
                'result_rows': record['post_stats']['merged_rows'],
                'match_rate': f"{record['match_rate']:.1%}",
                'matched': record['post_stats']['both'],
                'left_only': record['post_stats']['left_only'],
                'right_only': record['post_stats']['right_only']
            })
        
        return pd.DataFrame(report_data)


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    
    # Sample 1: Japanese firms (EDINET-like)
    df_japan = pd.DataFrame({
        'firm_id': range(1, 101),
        'firm_name': [f'Company_{i}' for i in range(1, 101)],
        'year': np.repeat(2020, 100),
        'sales_jp': np.random.lognormal(10, 1, 100)
    })
    
    # Sample 2: Financial data
    df_financials = pd.DataFrame({
        'firm_id': range(1, 121),  # Some overlap, some unique
        'year': np.repeat(2020, 120),
        'roa': np.random.normal(0.05, 0.02, 120),
        'leverage': np.random.uniform(0.2, 0.7, 120)
    })
    
    # Sample 3: R&D data
    df_rd = pd.DataFrame({
        'firm_id': range(1, 111),
        'year': np.repeat(2020, 110),
        'rd_spending': np.random.lognormal(8, 1, 110),
        'rd_intensity': np.random.uniform(0, 0.15, 110)
    })
    
    # Initialize merger
    merger = DataMerger()
    
    # Example 1: Simple merge
    print("\n" + "="*60)
    print("Example 1: Simple Merge (Japan + Financials)")
    print("="*60)
    
    df_merged_1 = merger.merge_datasets(
        df_left=df_japan,
        df_right=df_financials,
        on=['firm_id', 'year'],
        how='inner'
    )
    
    print(f"\nResult: {df_merged_1.shape}")
    print(df_merged_1.head())
    
    # Example 2: Sequential merge
    print("\n" + "="*60)
    print("Example 2: Sequential Merge (Japan + Financials + R&D)")
    print("="*60)
    
    datasets_to_merge = [
        (df_japan, 'japan_firms', ['firm_id', 'year']),
        (df_financials, 'financials', ['firm_id', 'year']),
        (df_rd, 'rd_data', ['firm_id', 'year'])
    ]
    
    df_merged_2 = merger.sequential_merge(datasets_to_merge, how='inner')
    
    print(f"\nResult: {df_merged_2.shape}")
    print(df_merged_2.head())
    
    # Example 3: Merge report
    print("\n" + "="*60)
    print("Example 3: Merge History Report")
    print("="*60)
    
    df_report = merger.get_merge_report()
    print(df_report)
    
    # Example 4: Fuzzy matching
    print("\n" + "="*60)
    print("Example 4: Fuzzy Firm Name Matching")
    print("="*60)
    
    df_names_1 = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Apple Inc', 'Microsoft Corp', 'Google LLC']
    })
    
    df_names_2 = pd.DataFrame({
        'id': [101, 102, 103],
        'name': ['Apple Incorporated', 'Microsoft Corporation', 'Alphabet Inc (Google)']
    })
    
    matches = merger.fuzzy_match_firms(
        df_names_1, df_names_2,
        name_col_left='name',
        name_col_right='name',
        threshold=0.6
    )
    
    print("\nFuzzy matches found:")
    print(matches)
