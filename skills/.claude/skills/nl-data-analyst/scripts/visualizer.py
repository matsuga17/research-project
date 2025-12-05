#!/usr/bin/env python3
"""
visualizer.py - 標準可視化テンプレート
自然言語データ分析スキル用

使用法:
    python visualizer.py <file_path> --type <chart_type> [options]
    
チャートタイプ:
    distribution  - 分布（ヒストグラム/KDE）
    correlation   - 相関ヒートマップ
    timeseries    - 時系列グラフ
    bar           - 棒グラフ
    scatter       - 散布図
    box           - 箱ひげ図
    pie           - 円グラフ
    pair          - ペアプロット
    auto          - 自動選択（複数グラフ生成）
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# スタイル設定
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

# デフォルトカラーパレット
COLORS = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', 
          '#937860', '#DA8BC3', '#8C8C8C', '#CCB974', '#64B5CD']


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


def plot_distribution(df: pd.DataFrame, columns: list = None, 
                      output: str = '/mnt/user-data/outputs/distribution.png',
                      bins: int = 30, kde: bool = True) -> str:
    """分布プロット（ヒストグラム + KDE）"""
    if columns is None:
        columns = df.select_dtypes(include='number').columns[:4].tolist()
    
    n_cols = min(len(columns), 4)
    n_rows = (len(columns) + 1) // 2 if len(columns) > 2 else 1
    
    fig, axes = plt.subplots(n_rows, min(2, n_cols), figsize=(14, 5 * n_rows))
    if n_cols == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_rows > 1 else axes
    
    for idx, col in enumerate(columns[:4]):
        ax = axes[idx] if len(columns) > 1 else axes[0]
        data = df[col].dropna()
        
        sns.histplot(data=data, bins=bins, kde=kde, ax=ax, color=COLORS[idx % len(COLORS)])
        ax.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.2f}')
        ax.axvline(data.median(), color='green', linestyle='--', linewidth=2, label=f'Median: {data.median():.2f}')
        ax.set_title(f'Distribution of {col}', fontsize=12, fontweight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
    
    # 使用しないサブプロットを非表示
    for idx in range(len(columns), len(axes) if hasattr(axes, '__len__') else 1):
        if hasattr(axes, '__len__'):
            axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_correlation(df: pd.DataFrame, output: str = '/mnt/user-data/outputs/correlation.png',
                     method: str = 'pearson', annot: bool = True) -> str:
    """相関ヒートマップ"""
    numeric_cols = df.select_dtypes(include='number').columns
    
    if len(numeric_cols) < 2:
        print("数値列が2つ未満のため相関プロットをスキップ")
        return None
    
    # 列数が多い場合は上位を選択
    if len(numeric_cols) > 15:
        # 分散が大きい列を選択
        variances = df[numeric_cols].var().sort_values(ascending=False)
        numeric_cols = variances.head(15).index.tolist()
    
    corr_matrix = df[numeric_cols].corr(method=method)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(corr_matrix, mask=mask, annot=annot, cmap='coolwarm', 
                center=0, square=True, linewidths=0.5, 
                fmt='.2f', cbar_kws={'shrink': 0.8}, ax=ax,
                vmin=-1, vmax=1)
    
    ax.set_title(f'Correlation Heatmap ({method.capitalize()})', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_timeseries(df: pd.DataFrame, date_col: str, value_cols: list = None,
                    output: str = '/mnt/user-data/outputs/timeseries.png',
                    resample: str = None) -> str:
    """時系列グラフ"""
    df_ts = df.copy()
    
    # 日付列の変換
    df_ts[date_col] = pd.to_datetime(df_ts[date_col], errors='coerce')
    df_ts = df_ts.dropna(subset=[date_col])
    df_ts = df_ts.sort_values(date_col)
    
    if value_cols is None:
        value_cols = df.select_dtypes(include='number').columns[:4].tolist()
    
    n_cols = len(value_cols)
    fig, axes = plt.subplots(n_cols, 1, figsize=(14, 4 * n_cols), sharex=True)
    
    if n_cols == 1:
        axes = [axes]
    
    for idx, col in enumerate(value_cols):
        ax = axes[idx]
        
        if resample:
            plot_data = df_ts.set_index(date_col)[col].resample(resample).mean()
        else:
            plot_data = df_ts.set_index(date_col)[col]
        
        ax.plot(plot_data.index, plot_data.values, linewidth=2, color=COLORS[idx % len(COLORS)])
        
        # トレンドライン
        if len(plot_data) > 2:
            x_numeric = np.arange(len(plot_data))
            valid_mask = ~np.isnan(plot_data.values)
            if valid_mask.sum() > 2:
                z = np.polyfit(x_numeric[valid_mask], plot_data.values[valid_mask], 1)
                p = np.poly1d(z)
                ax.plot(plot_data.index, p(x_numeric), '--', alpha=0.6, color='red', label='Trend')
        
        ax.set_title(f'{col} Over Time', fontsize=12, fontweight='bold')
        ax.set_ylabel(col)
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Date')
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_bar(df: pd.DataFrame, x: str, y: str = None, 
             output: str = '/mnt/user-data/outputs/barplot.png',
             top_n: int = 20, horizontal: bool = False,
             agg: str = 'mean') -> str:
    """棒グラフ"""
    if y is None:
        # カテゴリのカウント
        data = df[x].value_counts().head(top_n)
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if horizontal:
            ax.barh(range(len(data)), data.values, color=COLORS[0])
            ax.set_yticks(range(len(data)))
            ax.set_yticklabels(data.index)
            ax.set_xlabel('Count')
        else:
            ax.bar(range(len(data)), data.values, color=COLORS[0])
            ax.set_xticks(range(len(data)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
            ax.set_ylabel('Count')
        
        ax.set_title(f'Distribution of {x}', fontsize=14, fontweight='bold')
    
    else:
        # グループ集計
        agg_funcs = {'mean': 'mean', 'sum': 'sum', 'count': 'count', 'median': 'median'}
        data = df.groupby(x)[y].agg(agg_funcs.get(agg, 'mean')).sort_values(ascending=False).head(top_n)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if horizontal:
            ax.barh(range(len(data)), data.values, color=COLORS[0])
            ax.set_yticks(range(len(data)))
            ax.set_yticklabels(data.index)
            ax.set_xlabel(f'{y} ({agg})')
        else:
            ax.bar(range(len(data)), data.values, color=COLORS[0])
            ax.set_xticks(range(len(data)))
            ax.set_xticklabels(data.index, rotation=45, ha='right')
            ax.set_ylabel(f'{y} ({agg})')
        
        ax.set_title(f'{y} by {x}', fontsize=14, fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='x' if horizontal else 'y')
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_scatter(df: pd.DataFrame, x: str, y: str, hue: str = None,
                 output: str = '/mnt/user-data/outputs/scatter.png',
                 add_regression: bool = True) -> str:
    """散布図"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if hue and hue in df.columns:
        scatter = sns.scatterplot(data=df, x=x, y=y, hue=hue, alpha=0.6, ax=ax)
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        scatter = ax.scatter(df[x], df[y], alpha=0.6, c=COLORS[0])
    
    if add_regression:
        # 回帰直線
        valid_data = df[[x, y]].dropna()
        if len(valid_data) > 2:
            z = np.polyfit(valid_data[x], valid_data[y], 1)
            p = np.poly1d(z)
            x_line = np.linspace(valid_data[x].min(), valid_data[x].max(), 100)
            ax.plot(x_line, p(x_line), 'r--', alpha=0.8, label=f'Linear fit (slope={z[0]:.3f})')
            ax.legend()
    
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f'{y} vs {x}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_box(df: pd.DataFrame, columns: list = None, by: str = None,
             output: str = '/mnt/user-data/outputs/boxplot.png') -> str:
    """箱ひげ図"""
    if columns is None:
        columns = df.select_dtypes(include='number').columns[:6].tolist()
    
    if by and by in df.columns:
        # グループ別箱ひげ図
        n_cols = len(columns)
        fig, axes = plt.subplots(1, n_cols, figsize=(5 * n_cols, 6))
        
        if n_cols == 1:
            axes = [axes]
        
        for idx, col in enumerate(columns):
            sns.boxplot(data=df, x=by, y=col, ax=axes[idx], palette=COLORS)
            axes[idx].set_title(f'{col} by {by}', fontsize=12, fontweight='bold')
            axes[idx].tick_params(axis='x', rotation=45)
    else:
        # 単純な箱ひげ図
        fig, ax = plt.subplots(figsize=(12, 6))
        df_plot = df[columns].melt(var_name='Variable', value_name='Value')
        sns.boxplot(data=df_plot, x='Variable', y='Value', ax=ax, palette=COLORS)
        ax.set_title('Distribution of Numeric Variables', fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def plot_pie(df: pd.DataFrame, column: str, 
             output: str = '/mnt/user-data/outputs/pie.png',
             top_n: int = 10) -> str:
    """円グラフ"""
    data = df[column].value_counts().head(top_n)
    
    # その他をまとめる
    if len(df[column].value_counts()) > top_n:
        other = df[column].value_counts()[top_n:].sum()
        data['Other'] = other
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    wedges, texts, autotexts = ax.pie(data.values, labels=data.index, autopct='%1.1f%%',
                                       colors=COLORS[:len(data)], startangle=90)
    
    ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    return output


def auto_visualize(df: pd.DataFrame, output_dir: str = '/mnt/user-data/outputs') -> list:
    """自動可視化（複数グラフ生成）"""
    outputs = []
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. 数値列の分布
    if numeric_cols:
        out = plot_distribution(df, columns=numeric_cols[:4],
                               output=f'{output_dir}/distributions.png')
        if out:
            outputs.append(('distribution', out))
    
    # 2. 相関ヒートマップ
    if len(numeric_cols) >= 2:
        out = plot_correlation(df, output=f'{output_dir}/correlation.png')
        if out:
            outputs.append(('correlation', out))
    
    # 3. カテゴリ分布
    if categorical_cols:
        for col in categorical_cols[:2]:
            if df[col].nunique() <= 20:
                out = plot_bar(df, x=col, output=f'{output_dir}/bar_{col}.png')
                if out:
                    outputs.append(('bar', out))
    
    # 4. 箱ひげ図
    if numeric_cols:
        out = plot_box(df, columns=numeric_cols[:6],
                      output=f'{output_dir}/boxplot.png')
        if out:
            outputs.append(('boxplot', out))
    
    # 5. 時系列（日付列がある場合）
    date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
    date_cols = [c for c in df.columns if any(kw in c.lower() for kw in date_keywords)]
    
    if date_cols and numeric_cols:
        try:
            out = plot_timeseries(df, date_col=date_cols[0], value_cols=numeric_cols[:2],
                                 output=f'{output_dir}/timeseries.png')
            if out:
                outputs.append(('timeseries', out))
        except:
            pass
    
    return outputs


def main():
    parser = argparse.ArgumentParser(description='データ可視化')
    parser.add_argument('file_path', help='入力ファイル')
    parser.add_argument('--type', '-t', required=True,
                        choices=['distribution', 'correlation', 'timeseries', 
                                'bar', 'scatter', 'box', 'pie', 'auto'],
                        help='チャートタイプ')
    parser.add_argument('--output', '-o', default='/mnt/user-data/outputs/chart.png',
                        help='出力ファイル')
    parser.add_argument('--columns', '-c', nargs='+', help='対象列')
    parser.add_argument('--x', help='X軸列')
    parser.add_argument('--y', help='Y軸列')
    parser.add_argument('--hue', help='色分け列')
    parser.add_argument('--date-col', help='日付列')
    parser.add_argument('--top-n', type=int, default=20, help='表示する上位N件')
    parser.add_argument('--agg', default='mean', choices=['mean', 'sum', 'count', 'median'],
                        help='集計方法')
    
    args = parser.parse_args()
    
    # データ読み込み
    print(f"📂 ファイル読み込み: {args.file_path}")
    df = load_data(args.file_path)
    print(f"✅ {len(df):,}行 × {len(df.columns)}列")
    
    # 可視化実行
    print(f"📊 {args.type}グラフを作成中...")
    
    if args.type == 'distribution':
        output = plot_distribution(df, columns=args.columns, output=args.output)
    
    elif args.type == 'correlation':
        output = plot_correlation(df, output=args.output)
    
    elif args.type == 'timeseries':
        if not args.date_col:
            # 日付列を自動検出
            date_keywords = ['date', 'time', 'created', 'updated', 'timestamp']
            date_cols = [c for c in df.columns if any(kw in c.lower() for kw in date_keywords)]
            if date_cols:
                args.date_col = date_cols[0]
            else:
                print("❌ 日付列が見つかりません。--date-col で指定してください。")
                return
        output = plot_timeseries(df, date_col=args.date_col, value_cols=args.columns, output=args.output)
    
    elif args.type == 'bar':
        if not args.x:
            # カテゴリ列を自動選択
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            args.x = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
        output = plot_bar(df, x=args.x, y=args.y, output=args.output, top_n=args.top_n, agg=args.agg)
    
    elif args.type == 'scatter':
        if not args.x or not args.y:
            num_cols = df.select_dtypes(include='number').columns.tolist()
            if len(num_cols) >= 2:
                args.x = args.x or num_cols[0]
                args.y = args.y or num_cols[1]
            else:
                print("❌ 数値列が2つ以上必要です。")
                return
        output = plot_scatter(df, x=args.x, y=args.y, hue=args.hue, output=args.output)
    
    elif args.type == 'box':
        output = plot_box(df, columns=args.columns, by=args.x, output=args.output)
    
    elif args.type == 'pie':
        if not args.x:
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            args.x = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
        output = plot_pie(df, column=args.x, output=args.output, top_n=args.top_n)
    
    elif args.type == 'auto':
        outputs = auto_visualize(df, output_dir=Path(args.output).parent)
        print(f"\n📊 生成されたグラフ:")
        for chart_type, path in outputs:
            print(f"  ✓ [{chart_type}] {path}")
        return
    
    if output:
        print(f"\n✅ グラフ保存完了: {output}")


if __name__ == '__main__':
    main()
