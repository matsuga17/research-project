#!/usr/bin/env python3
"""
cleaner.py - データクレンジングユーティリティ
自然言語データ分析スキル用

使用法:
    python cleaner.py <file_path> --action <action> [options]
    
アクション:
    missing     - 欠損値処理
    duplicates  - 重複削除
    outliers    - 外れ値処理
    dtypes      - 型変換
    normalize   - 正規化
    all         - 全自動クレンジング
"""

import pandas as pd
import numpy as np
import argparse
import json
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


def load_data(path: str) -> pd.DataFrame:
    """ファイル読み込み"""
    suffix = Path(path).suffix.lower()
    if suffix == '.csv':
        return pd.read_csv(path, low_memory=False)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(path)
    elif suffix == '.json':
        return pd.read_json(path)
    elif suffix in ['.parquet', '.pq']:
        return pd.read_parquet(path)
    else:
        return pd.read_csv(path, low_memory=False)


def save_data(df: pd.DataFrame, path: str, original_path: str = None):
    """ファイル保存"""
    suffix = Path(path).suffix.lower()
    if suffix == '.csv':
        df.to_csv(path, index=False)
    elif suffix in ['.xlsx', '.xls']:
        df.to_excel(path, index=False)
    elif suffix == '.json':
        df.to_json(path, orient='records', force_ascii=False)
    elif suffix in ['.parquet', '.pq']:
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False)


def handle_missing(df: pd.DataFrame, strategy: str = 'auto', 
                   columns: list = None, fill_value=None) -> tuple:
    """
    欠損値処理
    
    strategy:
        auto     - 型に応じて自動選択
        drop     - 欠損行を削除
        mean     - 平均値で補完
        median   - 中央値で補完
        mode     - 最頻値で補完
        ffill    - 前方補完
        bfill    - 後方補完
        constant - 指定値で補完
    """
    df_clean = df.copy()
    changes = []
    
    if columns is None:
        columns = df.columns[df.isnull().any()].tolist()
    
    for col in columns:
        if col not in df.columns:
            continue
        
        missing_before = df_clean[col].isnull().sum()
        if missing_before == 0:
            continue
        
        if strategy == 'drop':
            df_clean = df_clean.dropna(subset=[col])
            changes.append({
                'column': col,
                'action': 'drop',
                'rows_removed': missing_before
            })
        
        elif strategy == 'auto':
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                fill_val = df_clean[col].median()
                df_clean[col].fillna(fill_val, inplace=True)
                changes.append({
                    'column': col,
                    'action': 'fill_median',
                    'fill_value': fill_val,
                    'filled': missing_before
                })
            else:
                fill_val = df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else ''
                df_clean[col].fillna(fill_val, inplace=True)
                changes.append({
                    'column': col,
                    'action': 'fill_mode',
                    'fill_value': str(fill_val),
                    'filled': missing_before
                })
        
        elif strategy == 'mean':
            fill_val = df_clean[col].mean()
            df_clean[col].fillna(fill_val, inplace=True)
            changes.append({'column': col, 'action': 'fill_mean', 'fill_value': fill_val, 'filled': missing_before})
        
        elif strategy == 'median':
            fill_val = df_clean[col].median()
            df_clean[col].fillna(fill_val, inplace=True)
            changes.append({'column': col, 'action': 'fill_median', 'fill_value': fill_val, 'filled': missing_before})
        
        elif strategy == 'mode':
            fill_val = df_clean[col].mode()[0] if len(df_clean[col].mode()) > 0 else None
            df_clean[col].fillna(fill_val, inplace=True)
            changes.append({'column': col, 'action': 'fill_mode', 'fill_value': str(fill_val), 'filled': missing_before})
        
        elif strategy == 'ffill':
            df_clean[col].fillna(method='ffill', inplace=True)
            changes.append({'column': col, 'action': 'ffill', 'filled': missing_before})
        
        elif strategy == 'bfill':
            df_clean[col].fillna(method='bfill', inplace=True)
            changes.append({'column': col, 'action': 'bfill', 'filled': missing_before})
        
        elif strategy == 'constant':
            df_clean[col].fillna(fill_value, inplace=True)
            changes.append({'column': col, 'action': 'fill_constant', 'fill_value': str(fill_value), 'filled': missing_before})
    
    return df_clean, changes


def handle_duplicates(df: pd.DataFrame, subset: list = None, 
                      keep: str = 'first') -> tuple:
    """重複削除"""
    df_clean = df.copy()
    dup_count = df_clean.duplicated(subset=subset, keep=False).sum()
    
    if dup_count > 0:
        df_clean = df_clean.drop_duplicates(subset=subset, keep=keep)
        removed = len(df) - len(df_clean)
        changes = [{
            'action': 'remove_duplicates',
            'subset': subset,
            'keep': keep,
            'duplicates_found': dup_count,
            'rows_removed': removed
        }]
    else:
        changes = [{'action': 'remove_duplicates', 'message': 'No duplicates found'}]
    
    return df_clean, changes


def handle_outliers(df: pd.DataFrame, columns: list = None, 
                    method: str = 'iqr', action: str = 'remove',
                    threshold: float = 1.5) -> tuple:
    """
    外れ値処理
    
    method:
        iqr     - IQR法（四分位範囲）
        zscore  - Zスコア法
    
    action:
        remove  - 外れ値を含む行を削除
        cap     - 境界値でキャップ
        nan     - NaNに置換
    """
    df_clean = df.copy()
    changes = []
    
    if columns is None:
        columns = df.select_dtypes(include='number').columns.tolist()
    
    for col in columns:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df_clean[col]):
            continue
        
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - threshold * IQR
            upper = Q3 + threshold * IQR
        
        elif method == 'zscore':
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            lower = mean - threshold * std
            upper = mean + threshold * std
        
        outliers_mask = (df_clean[col] < lower) | (df_clean[col] > upper)
        outlier_count = outliers_mask.sum()
        
        if outlier_count == 0:
            continue
        
        if action == 'remove':
            df_clean = df_clean[~outliers_mask]
            changes.append({
                'column': col,
                'action': 'remove_outliers',
                'method': method,
                'bounds': [lower, upper],
                'outliers_removed': int(outlier_count)
            })
        
        elif action == 'cap':
            df_clean.loc[df_clean[col] < lower, col] = lower
            df_clean.loc[df_clean[col] > upper, col] = upper
            changes.append({
                'column': col,
                'action': 'cap_outliers',
                'method': method,
                'bounds': [lower, upper],
                'outliers_capped': int(outlier_count)
            })
        
        elif action == 'nan':
            df_clean.loc[outliers_mask, col] = np.nan
            changes.append({
                'column': col,
                'action': 'nan_outliers',
                'method': method,
                'bounds': [lower, upper],
                'outliers_replaced': int(outlier_count)
            })
    
    return df_clean, changes


def handle_dtypes(df: pd.DataFrame, conversions: dict = None,
                  auto_detect: bool = True) -> tuple:
    """
    型変換
    
    conversions: {'column_name': 'target_type'}
    target_type: datetime, numeric, category, string
    """
    df_clean = df.copy()
    changes = []
    
    if auto_detect:
        # 日付列の自動検出と変換
        date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
        for col in df_clean.select_dtypes(include=['object']).columns:
            if any(kw in col.lower() for kw in date_keywords):
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    changes.append({
                        'column': col,
                        'action': 'convert_datetime',
                        'from': 'object',
                        'to': 'datetime64'
                    })
                except:
                    pass
        
        # 数値として解釈可能な文字列列
        for col in df_clean.select_dtypes(include=['object']).columns:
            try:
                numeric_col = pd.to_numeric(df_clean[col], errors='coerce')
                if numeric_col.notna().sum() / len(df_clean) > 0.9:
                    df_clean[col] = numeric_col
                    changes.append({
                        'column': col,
                        'action': 'convert_numeric',
                        'from': 'object',
                        'to': str(numeric_col.dtype)
                    })
            except:
                pass
    
    if conversions:
        for col, target_type in conversions.items():
            if col not in df_clean.columns:
                continue
            
            original_type = str(df_clean[col].dtype)
            
            if target_type == 'datetime':
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            elif target_type == 'numeric':
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            elif target_type == 'category':
                df_clean[col] = df_clean[col].astype('category')
            elif target_type == 'string':
                df_clean[col] = df_clean[col].astype(str)
            
            changes.append({
                'column': col,
                'action': f'convert_{target_type}',
                'from': original_type,
                'to': str(df_clean[col].dtype)
            })
    
    return df_clean, changes


def auto_clean(df: pd.DataFrame, config: dict = None) -> tuple:
    """
    自動クレンジング
    デフォルト設定で全処理を実行
    """
    if config is None:
        config = {
            'missing_strategy': 'auto',
            'remove_duplicates': True,
            'handle_outliers': False,  # デフォルトでは無効
            'auto_dtypes': True
        }
    
    all_changes = []
    df_clean = df.copy()
    
    # 1. 型変換
    if config.get('auto_dtypes', True):
        df_clean, changes = handle_dtypes(df_clean, auto_detect=True)
        all_changes.extend(changes)
    
    # 2. 重複削除
    if config.get('remove_duplicates', True):
        df_clean, changes = handle_duplicates(df_clean)
        all_changes.extend(changes)
    
    # 3. 欠損値処理
    if config.get('missing_strategy'):
        df_clean, changes = handle_missing(df_clean, strategy=config['missing_strategy'])
        all_changes.extend(changes)
    
    # 4. 外れ値処理
    if config.get('handle_outliers', False):
        df_clean, changes = handle_outliers(df_clean, action='cap')
        all_changes.extend(changes)
    
    return df_clean, all_changes


def print_summary(original_df: pd.DataFrame, clean_df: pd.DataFrame, changes: list):
    """クレンジング結果のサマリー出力"""
    print("=" * 60)
    print("🧹 データクレンジング結果")
    print("=" * 60)
    print(f"\n📊 データサイズ変化")
    print(f"  行: {len(original_df):,} → {len(clean_df):,} ({len(clean_df) - len(original_df):+,})")
    print(f"  列: {len(original_df.columns)} → {len(clean_df.columns)}")
    
    print(f"\n🔧 実行された処理")
    for change in changes:
        action = change.get('action', 'unknown')
        col = change.get('column', 'all')
        
        if 'fill' in action:
            print(f"  ✓ [{col}] {action}: {change.get('filled', 0)}件を補完")
        elif 'remove' in action or 'drop' in action:
            removed = change.get('rows_removed', change.get('outliers_removed', 0))
            print(f"  ✓ [{col}] {action}: {removed}件を削除")
        elif 'convert' in action:
            print(f"  ✓ [{col}] {action}: {change.get('from')} → {change.get('to')}")
        elif 'cap' in action:
            print(f"  ✓ [{col}] {action}: {change.get('outliers_capped', 0)}件をキャップ")
        else:
            print(f"  ✓ {action}")
    
    print(f"\n📈 欠損値変化")
    print(f"  クレンジング前: {original_df.isnull().sum().sum():,}")
    print(f"  クレンジング後: {clean_df.isnull().sum().sum():,}")
    
    print("\n" + "=" * 60)
    print("✅ クレンジング完了")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description='データクレンジング')
    parser.add_argument('file_path', help='入力ファイル')
    parser.add_argument('--action', '-a', required=True,
                        choices=['missing', 'duplicates', 'outliers', 'dtypes', 'all'],
                        help='実行アクション')
    parser.add_argument('--output', '-o', help='出力ファイル')
    parser.add_argument('--strategy', '-s', default='auto',
                        help='欠損値処理戦略')
    parser.add_argument('--columns', '-c', nargs='+', help='対象列')
    parser.add_argument('--keep', default='first', choices=['first', 'last', False],
                        help='重複処理時の保持方法')
    parser.add_argument('--method', '-m', default='iqr', choices=['iqr', 'zscore'],
                        help='外れ値検出方法')
    parser.add_argument('--outlier-action', default='remove', choices=['remove', 'cap', 'nan'],
                        help='外れ値処理方法')
    parser.add_argument('--json', action='store_true', help='JSON形式で出力')
    
    args = parser.parse_args()
    
    # データ読み込み
    print(f"📂 ファイル読み込み: {args.file_path}")
    df_original = load_data(args.file_path)
    print(f"✅ {len(df_original):,}行 × {len(df_original.columns)}列")
    
    # アクション実行
    if args.action == 'missing':
        df_clean, changes = handle_missing(df_original, strategy=args.strategy, columns=args.columns)
    elif args.action == 'duplicates':
        df_clean, changes = handle_duplicates(df_original, subset=args.columns, keep=args.keep)
    elif args.action == 'outliers':
        df_clean, changes = handle_outliers(df_original, columns=args.columns, 
                                           method=args.method, action=args.outlier_action)
    elif args.action == 'dtypes':
        df_clean, changes = handle_dtypes(df_original, auto_detect=True)
    elif args.action == 'all':
        df_clean, changes = auto_clean(df_original)
    
    # 結果出力
    if args.json:
        result = {
            'original_shape': list(df_original.shape),
            'clean_shape': list(df_clean.shape),
            'changes': changes
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_summary(df_original, df_clean, changes)
    
    # ファイル保存
    if args.output:
        save_data(df_clean, args.output)
        print(f"\n📄 保存完了: {args.output}")
    
    return df_clean


if __name__ == '__main__':
    main()
