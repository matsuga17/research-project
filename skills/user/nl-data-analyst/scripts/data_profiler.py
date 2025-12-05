#!/usr/bin/env python3
"""
data_profiler.py - 自動データプロファイリングスクリプト
自然言語データ分析スキル用

使用法:
    python data_profiler.py <file_path> [--output <output_path>] [--format json|text]
"""

import pandas as pd
import numpy as np
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


def detect_file_type(path: str) -> str:
    """ファイル形式を検出"""
    suffix = Path(path).suffix.lower()
    type_map = {
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.xlsx': 'excel',
        '.xls': 'excel',
        '.json': 'json',
        '.parquet': 'parquet',
        '.pq': 'parquet',
    }
    return type_map.get(suffix, 'csv')


def load_data(path: str) -> pd.DataFrame:
    """ファイルを読み込み"""
    file_type = detect_file_type(path)
    
    loaders = {
        'csv': lambda p: pd.read_csv(p, low_memory=False),
        'tsv': lambda p: pd.read_csv(p, sep='\t', low_memory=False),
        'excel': lambda p: pd.read_excel(p),
        'json': lambda p: pd.read_json(p),
        'parquet': lambda p: pd.read_parquet(p),
    }
    
    return loaders[file_type](path)


def analyze_column(series: pd.Series) -> dict:
    """個別列の分析"""
    result = {
        'dtype': str(series.dtype),
        'count': int(len(series)),
        'missing': int(series.isnull().sum()),
        'missing_pct': round(series.isnull().sum() / len(series) * 100, 2),
        'unique': int(series.nunique()),
        'unique_pct': round(series.nunique() / len(series) * 100, 2),
    }
    
    # 数値列の分析
    if pd.api.types.is_numeric_dtype(series):
        non_null = series.dropna()
        if len(non_null) > 0:
            result['stats'] = {
                'mean': round(non_null.mean(), 4),
                'std': round(non_null.std(), 4),
                'min': round(non_null.min(), 4),
                'q25': round(non_null.quantile(0.25), 4),
                'median': round(non_null.median(), 4),
                'q75': round(non_null.quantile(0.75), 4),
                'max': round(non_null.max(), 4),
            }
            # 外れ値検出
            Q1, Q3 = non_null.quantile([0.25, 0.75])
            IQR = Q3 - Q1
            outliers = ((non_null < Q1 - 1.5*IQR) | (non_null > Q3 + 1.5*IQR)).sum()
            result['outliers'] = int(outliers)
            result['outliers_pct'] = round(outliers / len(non_null) * 100, 2)
    
    # カテゴリ/文字列列の分析
    elif pd.api.types.is_object_dtype(series) or pd.api.types.is_categorical_dtype(series):
        value_counts = series.value_counts().head(10)
        result['top_values'] = {
            str(k): int(v) for k, v in value_counts.items()
        }
        # 空文字列検出
        if series.dtype == 'object':
            empty_strings = (series == '').sum()
            if empty_strings > 0:
                result['empty_strings'] = int(empty_strings)
    
    # 日時列の分析
    elif pd.api.types.is_datetime64_any_dtype(series):
        non_null = series.dropna()
        if len(non_null) > 0:
            result['date_range'] = {
                'min': str(non_null.min()),
                'max': str(non_null.max()),
                'span_days': int((non_null.max() - non_null.min()).days)
            }
    
    return result


def detect_potential_dates(df: pd.DataFrame) -> list:
    """日付に変換可能な列を検出"""
    potential_dates = []
    date_keywords = ['date', 'time', 'created', 'updated', 'timestamp', 'dt', 'day', 'month', 'year']
    
    for col in df.select_dtypes(include=['object']).columns:
        # 列名による検出
        if any(kw in col.lower() for kw in date_keywords):
            potential_dates.append(col)
            continue
        
        # サンプルによる検出
        sample = df[col].dropna().head(100)
        if len(sample) > 0:
            try:
                pd.to_datetime(sample, errors='raise')
                potential_dates.append(col)
            except:
                pass
    
    return potential_dates


def detect_quality_issues(df: pd.DataFrame) -> list:
    """データ品質問題を検出"""
    issues = []
    
    # 高欠損率列
    high_missing = df.columns[df.isnull().mean() > 0.5].tolist()
    if high_missing:
        issues.append({
            'type': 'high_missing',
            'severity': 'warning',
            'columns': high_missing,
            'message': f'{len(high_missing)}列で欠損率が50%を超えています'
        })
    
    # 重複行
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        issues.append({
            'type': 'duplicates',
            'severity': 'info',
            'count': int(dup_count),
            'message': f'{dup_count}件の重複行が検出されました'
        })
    
    # 定数列（単一値のみ）
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        issues.append({
            'type': 'constant_columns',
            'severity': 'info',
            'columns': constant_cols,
            'message': f'{len(constant_cols)}列が定数（単一値）です'
        })
    
    # 高カーディナリティ列
    high_cardinality = []
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) > 0.9:
            high_cardinality.append(col)
    if high_cardinality:
        issues.append({
            'type': 'high_cardinality',
            'severity': 'info',
            'columns': high_cardinality,
            'message': f'{len(high_cardinality)}列でユニーク値率が90%を超えています（ID列の可能性）'
        })
    
    return issues


def profile_dataframe(df: pd.DataFrame) -> dict:
    """データフレーム全体のプロファイリング"""
    profile = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'rows': len(df),
            'columns': len(df.columns),
            'memory_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        },
        'dtypes_summary': df.dtypes.astype(str).value_counts().to_dict(),
        'columns': {},
        'quality_issues': [],
        'potential_date_columns': [],
    }
    
    # 各列の分析
    for col in df.columns:
        profile['columns'][col] = analyze_column(df[col])
    
    # 品質問題検出
    profile['quality_issues'] = detect_quality_issues(df)
    
    # 日付候補列
    profile['potential_date_columns'] = detect_potential_dates(df)
    
    # 数値列間の相関（上位）
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        high_corr = []
        for i in range(len(numeric_cols)):
            for j in range(i+1, len(numeric_cols)):
                c = corr.iloc[i, j]
                if abs(c) > 0.7:
                    high_corr.append({
                        'col1': numeric_cols[i],
                        'col2': numeric_cols[j],
                        'correlation': round(c, 3)
                    })
        if high_corr:
            profile['high_correlations'] = sorted(high_corr, key=lambda x: abs(x['correlation']), reverse=True)[:10]
    
    return profile


def format_text_report(profile: dict) -> str:
    """テキスト形式のレポート生成"""
    lines = []
    lines.append("=" * 60)
    lines.append("📊 データプロファイリングレポート")
    lines.append("=" * 60)
    
    # 基本情報
    meta = profile['metadata']
    lines.append(f"\n📋 基本情報")
    lines.append(f"  行数: {meta['rows']:,}")
    lines.append(f"  列数: {meta['columns']}")
    lines.append(f"  メモリ使用量: {meta['memory_mb']:.2f} MB")
    
    # 型サマリー
    lines.append(f"\n📐 データ型分布")
    for dtype, count in profile['dtypes_summary'].items():
        lines.append(f"  {dtype}: {count}列")
    
    # 品質問題
    if profile['quality_issues']:
        lines.append(f"\n⚠️ 検出された品質問題")
        for issue in profile['quality_issues']:
            severity_icon = '🔴' if issue['severity'] == 'warning' else '🟡'
            lines.append(f"  {severity_icon} {issue['message']}")
    
    # 日付候補列
    if profile['potential_date_columns']:
        lines.append(f"\n📅 日付型に変換可能な列")
        lines.append(f"  {', '.join(profile['potential_date_columns'])}")
    
    # 高相関
    if 'high_correlations' in profile:
        lines.append(f"\n🔗 高相関ペア（|r| > 0.7）")
        for hc in profile['high_correlations'][:5]:
            lines.append(f"  {hc['col1']} ↔ {hc['col2']}: {hc['correlation']}")
    
    # 各列の詳細
    lines.append(f"\n📊 列詳細")
    lines.append("-" * 60)
    
    for col_name, col_info in profile['columns'].items():
        lines.append(f"\n【{col_name}】")
        lines.append(f"  型: {col_info['dtype']}")
        lines.append(f"  欠損: {col_info['missing']:,} ({col_info['missing_pct']}%)")
        lines.append(f"  ユニーク: {col_info['unique']:,} ({col_info['unique_pct']}%)")
        
        if 'stats' in col_info:
            s = col_info['stats']
            lines.append(f"  統計: 平均={s['mean']}, 中央値={s['median']}, 標準偏差={s['std']}")
            lines.append(f"        範囲=[{s['min']}, {s['max']}], IQR=[{s['q25']}, {s['q75']}]")
            if col_info.get('outliers', 0) > 0:
                lines.append(f"  外れ値: {col_info['outliers']} ({col_info['outliers_pct']}%)")
        
        if 'top_values' in col_info:
            lines.append(f"  上位値:")
            for val, cnt in list(col_info['top_values'].items())[:5]:
                lines.append(f"    - {val}: {cnt}")
        
        if 'date_range' in col_info:
            dr = col_info['date_range']
            lines.append(f"  日付範囲: {dr['min']} ~ {dr['max']} ({dr['span_days']}日)")
    
    lines.append("\n" + "=" * 60)
    lines.append("✅ プロファイリング完了")
    lines.append("=" * 60)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='データプロファイリング')
    parser.add_argument('file_path', help='分析対象ファイル')
    parser.add_argument('--output', '-o', help='出力ファイルパス')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='text', help='出力形式')
    args = parser.parse_args()
    
    # データ読み込み
    print(f"📂 ファイル読み込み中: {args.file_path}")
    df = load_data(args.file_path)
    print(f"✅ {len(df):,}行 × {len(df.columns)}列 を読み込みました")
    
    # プロファイリング実行
    print("🔍 プロファイリング中...")
    profile = profile_dataframe(df)
    
    # 出力
    if args.format == 'json':
        output = json.dumps(profile, ensure_ascii=False, indent=2)
    else:
        output = format_text_report(profile)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"📄 レポート保存: {args.output}")
    else:
        print(output)
    
    return profile


if __name__ == '__main__':
    main()
