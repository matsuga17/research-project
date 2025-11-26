# US Corporate Analytics - 使用例集

このドキュメントでは、US Corporate Analyticsスキルの実践的な使用例を紹介します。

---

## 例1: 単一企業の財務分析（基本）

### 目的
Apple Inc.の過去5年間の財務パフォーマンスを分析

### 手順

**ステップ1: データ取得**

```python
from scripts.company_analyzer import CompanyAnalyzer
import yaml

# 設定読み込み
with open('config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# アナライザー初期化
analyzer = CompanyAnalyzer("AAPL", config)

# データ取得（5年分）
analyzer.fetch_all_data(years=5)
```

**ステップ2: 財務比率計算**

```python
# 財務比率は自動計算済み
print(analyzer.financial_ratios)
```

**ステップ3: パフォーマンス分析**

```python
analysis = analyzer.analyze_performance()

print(f"企業評価: {analysis['performance_rating']}")
print(f"最新ROA: {analysis['latest_ratios']['ROA']:.2f}%")
print(f"最新ROE: {analysis['latest_ratios']['ROE']:.2f}%")
```

**ステップ4: レポート生成**

```python
report = analyzer.generate_summary_report()
print(report)

# データをエクスポート
analyzer.export_data("./reports/apple_analysis")
```

**期待される出力**:
```
企業財務分析レポート
-------------------------------
ティッカー: AAPL
財務パフォーマンス評価: AAA

主要財務比率（最新年度）
ROA: 27.34 (平均: 25.12, トレンド: ↑)
ROE: 147.36 (平均: 142.08, トレンド: ↑)
net_margin: 25.31 (平均: 23.45, トレンド: ↑)
```

---

## 例2: 業界比較分析

### 目的
テクノロジー大手5社（FAANG）の財務パフォーマンスを比較

### 手順

```python
from scripts.industry_comparison import IndustryComparison

# 比較対象企業
tickers = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]

# 比較分析初期化
comparison = IndustryComparison(tickers, config)

# データ取得
comparison.fetch_all_companies(years=5)

# 財務比率比較
ratio_names = ['ROA', 'ROE', 'net_margin', 'current_ratio', 'debt_ratio']
comparison.compare_ratios(ratio_names)

# ランキング生成
ranking_roe = comparison.generate_ranking('ROE')
print("ROEランキング:")
print(ranking_roe)

# 業界統計
stats = comparison.calculate_industry_statistics(ratio_names)
print("\n業界統計:")
print(stats)

# 可視化
comparison.visualize_comparison(ratio_names, "./reports/faang_comparison.png")
comparison.generate_heatmap(ratio_names, "./reports/faang_heatmap.png")

# レポートエクスポート
comparison.export_comparison("./reports/faang_analysis")
```

**出力例（ROEランキング）**:
```
      ROE  rank
META  30.5     1
AAPL  28.9     2
GOOGL 23.1     3
AMZN  12.8     4
NFLX  11.2     5
```

---

## 例3: マクロ経済統合分析

### 目的
企業業績とマクロ経済指標の相関分析

### 手順

```python
from scripts.company_analyzer import CompanyAnalyzer
from scipy.stats import pearsonr

# データ取得
analyzer = CompanyAnalyzer("AMZN", config)
analyzer.fetch_all_data(years=10)

# 財務データとマクロデータをマージ
financial = analyzer.financial_ratios
macro = analyzer.macro_data

# 年度でマージ
merged = financial.merge(
    macro, 
    left_index=True, 
    right_on='year',
    how='inner'
)

# 相関分析
if 'revenue_growth' in merged.columns and 'NY.GDP.MKTP.KD.ZG' in merged.columns:
    corr, pval = pearsonr(
        merged['revenue_growth'].dropna(),
        merged['NY.GDP.MKTP.KD.ZG'].dropna()
    )
    print(f"売上成長率とGDP成長率の相関: {corr:.3f} (p={pval:.4f})")

# 回帰分析
import statsmodels.api as sm

X = merged[['NY.GDP.MKTP.KD.ZG', 'SL.UEM.TOTL.ZS']].dropna()
y = merged.loc[X.index, 'revenue_growth'].dropna()

X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())
```

**出力例**:
```
売上成長率とGDP成長率の相関: 0.685 (p=0.0023)

回帰分析結果:
                 coef    std err          t      P>|t|
const          5.234      2.145      2.440      0.035
GDP_growth     1.823      0.456      3.998      0.003
Unemployment  -0.912      0.334     -2.731      0.021

R-squared: 0.647
```

---

## 例4: CEO交代の影響分析

### 目的
CEO交代が企業業績に与える影響を定量化

### 手順

```python
from utils.sec_client import SECEdgarClient
import pandas as pd

# 8-KからCEO交代イベントを抽出
client = SECEdgarClient(
    api_key=config['sec_edgar']['api_key'],
    user_agent=config['sec_edgar']['user_agent']
)

# 対象企業リスト
companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
ceo_changes = []

for ticker in companies:
    cik = client.get_company_cik(ticker)
    
    # 8-K取得（2018-2023年）
    filings = client.get_filing_urls(
        cik, "8-K", 
        start_date="2018-01-01",
        end_date="2023-12-31"
    )
    
    # Item 5.02（役員の異動）を含むファイリングを検索
    # 注: 実際の実装では8-Kの内容をパースする必要があります
    
    for filing in filings:
        # ここで8-Kの内容を解析し、CEO交代を検出
        # 簡略化のため省略
        pass

# 交代前後の業績変化を分析
def analyze_ceo_change(ticker, change_date, analyzer):
    """CEO交代前後の業績を比較"""
    
    # 交代年を取得
    change_year = pd.to_datetime(change_date).year
    
    # 前2年と後2年のデータを取得
    pre_years = [change_year - 2, change_year - 1]
    post_years = [change_year + 1, change_year + 2]
    
    ratios = analyzer.financial_ratios
    
    # 交代前の平均
    pre_roa = ratios.loc[pre_years, 'ROA'].mean()
    
    # 交代後の平均
    post_roa = ratios.loc[post_years, 'ROA'].mean()
    
    # 変化率
    change = ((post_roa - pre_roa) / pre_roa) * 100
    
    return {
        'ticker': ticker,
        'change_date': change_date,
        'pre_roa': pre_roa,
        'post_roa': post_roa,
        'change_pct': change
    }

# 結果を集計
results = []
for event in ceo_changes:
    analyzer = CompanyAnalyzer(event['ticker'], config)
    analyzer.fetch_all_data(years=10)
    
    result = analyze_ceo_change(
        event['ticker'],
        event['date'],
        analyzer
    )
    results.append(result)

# 統計分析
results_df = pd.DataFrame(results)
avg_change = results_df['change_pct'].mean()

print(f"CEO交代によるROA平均変化: {avg_change:.2f}%")
```

---

## 例5: ガバナンス評価

### 目的
企業のコーポレートガバナンス体制を評価

### 手順

```python
from utils.sec_client import SECEdgarClient
import re

def analyze_governance(ticker, year, config):
    """ガバナンス分析"""
    
    client = SECEdgarClient(
        api_key=config['sec_edgar']['api_key'],
        user_agent=config['sec_edgar']['user_agent']
    )
    
    cik = client.get_company_cik(ticker)
    
    # DEF 14A（委任状説明書）を取得
    filings = client.get_filing_urls(
        cik, "DEF 14A",
        start_date=f"{year}-01-01",
        end_date=f"{year}-12-31"
    )
    
    if not filings:
        return None
    
    # 最新のDEF 14Aを取得
    filing_url = filings[0]['url']
    
    # ファイリングの内容を取得（簡略化）
    # 実際にはHTMLパース等が必要
    
    governance_metrics = {
        'ticker': ticker,
        'year': year,
        # 以下は実際にDEF 14Aから抽出
        'board_size': 10,  # 取締役会の人数
        'independent_directors': 7,  # 独立取締役の人数
        'independent_ratio': 0.70,  # 独立取締役比率
        'female_directors': 3,  # 女性取締役の人数
        'diversity_score': 0.30,  # 多様性スコア
        'ceo_total_compensation': 14800000,  # CEO報酬（ドル）
        'board_meetings': 8  # 取締役会開催回数
    }
    
    # スコアリング
    score = 0
    
    # 独立性（最大25点）
    if governance_metrics['independent_ratio'] >= 0.75:
        score += 25
    elif governance_metrics['independent_ratio'] >= 0.50:
        score += 15
    else:
        score += 5
    
    # 多様性（最大25点）
    if governance_metrics['diversity_score'] >= 0.30:
        score += 25
    elif governance_metrics['diversity_score'] >= 0.20:
        score += 15
    else:
        score += 5
    
    # 取締役会活動（最大25点）
    if governance_metrics['board_meetings'] >= 8:
        score += 25
    elif governance_metrics['board_meetings'] >= 6:
        score += 15
    else:
        score += 5
    
    # 報酬の適切性（最大25点）
    # 業界平均との比較が必要（ここでは簡略化）
    score += 20
    
    governance_metrics['total_score'] = score
    
    # 評価
    if score >= 90:
        governance_metrics['rating'] = "Excellent"
    elif score >= 75:
        governance_metrics['rating'] = "Good"
    elif score >= 60:
        governance_metrics['rating'] = "Fair"
    else:
        governance_metrics['rating'] = "Poor"
    
    return governance_metrics

# 実行例
governance = analyze_governance("AAPL", 2023, config)
print(f"ガバナンススコア: {governance['total_score']}/100")
print(f"評価: {governance['rating']}")
```

---

## 例6: 業界トレンド分析

### 目的
特定業界（例：半導体）の財務トレンドを分析

### 手順

```python
from scripts.industry_comparison import IndustryComparison
import matplotlib.pyplot as plt

# 半導体企業
semiconductor_companies = [
    "NVDA",  # NVIDIA
    "INTC",  # Intel
    "AMD",   # AMD
    "TSM",   # TSMC
    "QCOM"   # Qualcomm
]

# 業界分析
industry = IndustryComparison(semiconductor_companies, config)
industry.fetch_all_companies(years=10)

# 全企業のR&D支出トレンド
rd_spending = {}

for ticker, analyzer in industry.analyzers.items():
    if 'rd_expense' in analyzer.financial_data.columns:
        rd_spending[ticker] = analyzer.financial_data['rd_expense']

# プロット
plt.figure(figsize=(12, 6))
for ticker, data in rd_spending.items():
    plt.plot(data.index, data.values, marker='o', label=ticker)

plt.title('R&D Spending Trend - Semiconductor Industry', fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('R&D Spending (USD)', fontsize=12)
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('./reports/semiconductor_rd_trend.png', dpi=300)

# 業界平均の成長率
ratio_names = ['revenue_growth', 'rd_intensity', 'ROA']
stats = industry.calculate_industry_statistics(ratio_names)

print("業界平均指標:")
print(stats)
```

---

## 例7: ポートフォリオ分析

### 目的
投資ポートフォリオの財務健全性を評価

### 手順

```python
from scripts.company_analyzer import CompanyAnalyzer
import pandas as pd

# ポートフォリオ（企業と保有比率）
portfolio = {
    "AAPL": 0.30,
    "MSFT": 0.25,
    "GOOGL": 0.20,
    "AMZN": 0.15,
    "TSLA": 0.10
}

# 各企業を分析
portfolio_analysis = {}

for ticker, weight in portfolio.items():
    analyzer = CompanyAnalyzer(ticker, config)
    analyzer.fetch_all_data(years=5)
    
    analysis = analyzer.analyze_performance()
    
    portfolio_analysis[ticker] = {
        'weight': weight,
        'rating': analysis['performance_rating'],
        'roa': analysis['latest_ratios'].get('ROA', 0),
        'roe': analysis['latest_ratios'].get('ROE', 0),
        'debt_ratio': analysis['latest_ratios'].get('debt_ratio', 0)
    }

# ポートフォリオ全体の加重平均
portfolio_df = pd.DataFrame(portfolio_analysis).T

weighted_roa = (portfolio_df['roa'] * portfolio_df['weight']).sum()
weighted_roe = (portfolio_df['roe'] * portfolio_df['weight']).sum()
weighted_debt = (portfolio_df['debt_ratio'] * portfolio_df['weight']).sum()

print("ポートフォリオ分析結果:")
print(f"加重平均ROA: {weighted_roa:.2f}%")
print(f"加重平均ROE: {weighted_roe:.2f}%")
print(f"加重平均負債比率: {weighted_debt:.2f}")

# 各企業の評価
print("\n個別企業評価:")
for ticker, data in portfolio_analysis.items():
    print(f"{ticker}: {data['rating']} (ウェイト: {data['weight']*100:.0f}%)")
```

---

## 例8: 自動レポート生成

### 目的
定期的な財務レポートを自動生成

### 手順

```python
from datetime import datetime
import os

def generate_monthly_report(tickers, config, output_dir):
    """月次レポートを自動生成"""
    
    # 日付
    today = datetime.now()
    report_date = today.strftime("%Y-%m")
    
    # 出力ディレクトリ作成
    monthly_dir = f"{output_dir}/{report_date}"
    os.makedirs(monthly_dir, exist_ok=True)
    
    # サマリーレポート初期化
    summary = {
        'report_date': report_date,
        'companies': []
    }
    
    # 各企業を分析
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        
        try:
            analyzer = CompanyAnalyzer(ticker, config)
            analyzer.fetch_all_data(years=5)
            
            # 個別レポート生成
            company_dir = f"{monthly_dir}/{ticker}"
            analyzer.export_data(company_dir)
            
            # サマリーに追加
            analysis = analyzer.analyze_performance()
            summary['companies'].append({
                'ticker': ticker,
                'rating': analysis['performance_rating'],
                'latest_roa': analysis['latest_ratios'].get('ROA', 'N/A'),
                'latest_roe': analysis['latest_ratios'].get('ROE', 'N/A')
            })
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            summary['companies'].append({
                'ticker': ticker,
                'error': str(e)
            })
    
    # 統合サマリーレポート
    summary_text = f"""
月次財務レポート
================
レポート日: {summary['report_date']}

企業別サマリー:
"""
    
    for company in summary['companies']:
        ticker = company['ticker']
        if 'error' in company:
            summary_text += f"\n{ticker}: エラー - {company['error']}"
        else:
            summary_text += f"""
{ticker}:
  評価: {company['rating']}
  ROA: {company['latest_roa']:.2f}%
  ROE: {company['latest_roe']:.2f}%
"""
    
    # サマリー保存
    with open(f"{monthly_dir}/monthly_summary.txt", 'w') as f:
        f.write(summary_text)
    
    print(f"\nMonthly report generated: {monthly_dir}")
    return monthly_dir

# 実行例
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
report_dir = generate_monthly_report(tickers, config, "./reports")
```

---

## 次のステップ

これらの例を参考に、独自の分析ワークフローを構築してください。

**推奨学習リソース**:
1. `SKILL.md` - 全機能の詳細説明
2. `TEMPLATES_GUIDE.md` - テンプレートの使用方法
3. `scripts/` - 各スクリプトのソースコード

**カスタマイズのヒント**:
- 業界特有の指標を追加
- 独自のスコアリングロジックを実装
- 可視化スタイルのカスタマイズ
- 自動化スケジュールの設定

---

**最終更新**: 2025-11-02
