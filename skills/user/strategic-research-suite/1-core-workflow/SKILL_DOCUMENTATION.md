---
name: strategic-research-core-workflow
description: Comprehensive Phase 1-8 research workflow for strategic management and organizational studies, covering research design, data collection, panel dataset construction, variable operationalization, statistical analysis, and documentation for top-tier journal publication.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - data-sources: Phase 2 data source discovery and collection
  - statistical-methods: Phase 7 advanced statistical analysis
  - text-analysis: Qualitative data quantification
  - network-analysis: Inter-organizational relationship analysis
  - causal-ml: Causal inference and heterogeneous treatment effects
  - esg-sustainability: ESG/CSR strategy research
  - automation: End-to-end pipeline automation
---

# Strategic Research Core Workflow v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

戦略経営・組織研究のための**Phase 1-8研究ワークフロー**を提供します。Research Question設定からトップジャーナル投稿までの全プロセスをカバーします。

### いつ使うか

- ✅ すべての定量研究プロジェクトの起点
- ✅ 研究設計の全体像を理解したい
- ✅ 初めて戦略研究・組織研究に取り組む
- ✅ Phase別の作業内容と順序を確認したい
- ✅ トップジャーナル（SMJ, AMJ, OS, JOM）基準を満たしたい

### 前提条件

**必須知識**:
- Python基礎（pandas, numpy）
- パネルデータの基本概念
- 統計分析の基礎（回帰分析、p値、信頼区間）

**推奨知識**:
- 戦略経営・組織理論の基礎
- 学術論文の読み方・書き方
- データベース操作（SQL基礎）

### 他スキルとの連携

**Phase別推奨スキル**:
- **Phase 1**: 本スキル + `_shared/THEORY_FRAMEWORKS.md`
- **Phase 2**: `2-data-sources`（データソース探索）
- **Phase 3**: `2-data-sources` + `8-automation`（収集戦略）
- **Phase 4**: 本スキル + `8-automation`（Panel構築）
- **Phase 5**: `_shared/quality-checklist.md`（QA）
- **Phase 6**: `_shared/common-definitions.md` + 専門スキル
  - テキスト変数 → `4-text-analysis`
  - ネットワーク変数 → `5-network-analysis`
  - ESG変数 → `7-esg-sustainability`
- **Phase 7**: `3-statistical-methods`（統計分析）
- **Phase 8**: `8-automation`（再現パッケージ）

---

## 📋 目次

1. [Phase 1: Research Design](#phase-1-research-design)
2. [Phase 2: Data Source Discovery](#phase-2-data-source-discovery)
3. [Phase 3: Data Collection Strategy](#phase-3-data-collection-strategy)
4. [Phase 4: Panel Dataset Construction](#phase-4-panel-dataset-construction)
5. [Phase 5: Quality Assurance](#phase-5-quality-assurance)
6. [Phase 6: Variable Construction](#phase-6-variable-construction)
7. [Phase 7: Statistical Analysis](#phase-7-statistical-analysis)
8. [Phase 8: Documentation & Reproducibility](#phase-8-documentation--reproducibility)
9. [Quick Start Guide](#quick-start-guide)
10. [Common Pitfalls](#common-pitfalls)
11. [FAQ](#faq)

---

## Phase 1: Research Design

### 1.1 Research Question (RQ) 設定

**良いRQの5条件**:

1. **Theoretical Gap**: 既存研究で未解決の問題・矛盾を明確に指摘
2. **Practical Relevance**: 経営実務への示唆が明確
3. **Empirically Testable**: データで検証可能（抽象的概念を回避）
4. **Specific & Focused**: 変数間の関係が明確（「影響する」だけでは不十分）
5. **Boundary Conditions**: どのような状況で成立するかが明確

**悪いRQ例**:
```
❌ 「イノベーションは企業パフォーマンスに影響するか？」

問題点:
- 先行研究で既に確立済み（Theoretical Gapなし）
- 「イノベーション」「パフォーマンス」が曖昧
- 条件・メカニズムが不明確
```

**良いRQ例**:
```
✅ 「環境不確実性が高い状況下で、探索的イノベーション（Exploration）は
短期的パフォーマンスを損なうが、どのような組織的条件（Organizational Slack,
Absorptive Capacity）の下で長期的に回復するか？」

優れている点:
- Theoretical Gap: March (1991)のExploration-Exploitation理論と
  パフォーマンスの時間的ダイナミクスの統合
- 条件付き関係: 環境不確実性という境界条件
- 調整変数: Slack, Absorptive Capacity
- 時間的視点: 短期vs長期
```

### 1.2 理論フレームワーク選択

→ **詳細**: `_shared/THEORY_FRAMEWORKS.md`

**主要理論8つ**:

| 理論 | 適用場面 | 主要文献 |
|------|---------|---------|
| **RBV** | 企業内部資源と競争優位 | Barney (1991) |
| **Dynamic Capabilities** | 環境変化への適応 | Teece et al. (1997) |
| **Institutional Theory** | 組織と環境の同型化 | DiMaggio & Powell (1983) |
| **TCE** | Make-or-buy決定 | Williamson (1985) |
| **Agency Theory** | 経営者-株主利害対立 | Jensen & Meckling (1976) |
| **Stakeholder Theory** | CSR, ESG | Freeman (1984) |
| **IO** | 産業構造と収益性 | Porter (1980) |
| **KBV** | 知識創造・移転 | Grant (1996) |

**選択基準**:
1. **RQ適合性**: RQが説明しようとする現象に最も適した理論
2. **因果メカニズム**: なぜその関係が生じるかを明確に説明できる
3. **トップジャーナル使用頻度**: SMJ, AMJ, OSでの使用実績

**複数理論の統合**:
```python
# 例: RBV + Dynamic Capabilities
# RQが「資源の蓄積（RBV）と環境変化への適応（DC）の相互作用」の場合

理論的論理:
1. RBV: R&D投資は模倣困難な技術資源を蓄積（静的視点）
2. Dynamic Capabilities: 環境変化時にR&D資源を再配置する能力（動的視点）
3. 統合: R&D資源×再配置能力の交互作用がパフォーマンスを決定
```

### 1.3 仮説導出

**仮説構築の3ステップ**:

#### Step 1: 理論的根拠の明示
```
理論: RBV (Resource-Based View)
命題: 模倣困難な資源は持続的競争優位の源泉
適用: R&D投資は技術知識という模倣困難資源を創出
```

#### Step 2: 因果メカニズムの特定
```
R&D投資 → 技術知識蓄積 → 特許取得 → 競争優位 → 超過利潤 → パフォーマンス向上

各ステップの理論的説明:
- R&D→知識: Learning-by-doing (Cohen & Levinthal, 1990)
- 知識→特許: Appropriability mechanisms (Teece, 1986)
- 特許→競争優位: Imitation barriers (Rumelt, 1984)
```

#### Step 3: 境界条件・調整効果の特定
```
H1 (Main Effect): R&D投資強度は企業パフォーマンスに正の影響を与える

H2 (Moderator: Industry Maturity):
産業成熟度が高い場合、H1の正の関係は弱まる

理論的根拠:
- 成熟産業では技術革新の余地が限定的（Klepper, 1996）
- Diminishing returnsが早期に発生
```

**実装例: 仮説リスト**
```markdown
### 仮説

**H1 (Main Effect)**: R&D投資強度は企業パフォーマンス（ROA）に正の影響を与える

**H2 (Moderator)**: 産業成熟度はH1の関係を負に調整する
- H2a: 産業成熟度が低い場合、H1の正の関係は強い
- H2b: 産業成熟度が高い場合、H1の正の関係は弱い

**H3 (Mediator)**: R&D投資強度は特許取得数を媒介してパフォーマンスに影響する
- H3a: R&D投資強度 → 特許取得数（正）
- H3b: 特許取得数 → ROA（正）
- H3c: H3a×H3b: 媒介効果が有意
```

### 1.4 変数定義

→ **詳細**: `_shared/common-definitions.md`

**必須変数タイプ**:

| タイプ | 例 | 測定方法 |
|--------|-----|---------|
| **従属変数 (DV)** | ROA, Tobin's Q, ROE | 財務データから計算 |
| **独立変数 (IV)** | R&D Intensity, Patent Count | 財務・特許データ |
| **調整変数 (Moderator)** | Industry Maturity, Slack | 産業・組織変数 |
| **媒介変数 (Mediator)** | Patent Count, Absorptive Capacity | 中間変数 |
| **統制変数 (CV)** | Firm Size, Leverage, Industry, Year | 交絡因子 |

**Pythonでの変数構築**:
```python
import pandas as pd
import numpy as np

# サンプルデータ読み込み
df = pd.read_csv('compustat_sample.csv')

# 1. 従属変数: ROA
df['roa'] = df['net_income'] / df['total_assets']

# 2. 独立変数: R&D Intensity
df['rd_intensity'] = df['rd_expense'] / df['revenue']

# 欠損値処理: R&D未報告企業は0と仮定（業界標準）
df['rd_intensity'] = df['rd_intensity'].fillna(0)

# 3. 調整変数: Industry Maturity (産業平均年齢)
df['industry_maturity'] = df.groupby('sic_code')['firm_age'].transform('mean')

# 4. 統制変数
# Firm Size (log)
df['firm_size'] = np.log(df['total_assets'])

# Leverage
df['leverage'] = df['total_debt'] / df['total_assets']

# Firm Age (log)
df['firm_age'] = df['year'] - df['founding_year']
df['firm_age_log'] = np.log(df['firm_age'] + 1)  # +1 to avoid log(0)

# 5. ラグ変数（1年ラグ）
df = df.sort_values(['firm_id', 'year'])
df['rd_intensity_lag1'] = df.groupby('firm_id')['rd_intensity'].shift(1)

print(df[['firm_id', 'year', 'roa', 'rd_intensity', 'firm_size']].head(10))
```

### 1.5 サンプル設計

→ **詳細**: `_shared/common-definitions.md#minimum-sample-sizes`

**最小サンプルサイズ**:

| 研究タイプ | 最小 firm-years | 推奨 firm-years | 典型的期間 |
|-----------|----------------|----------------|-----------|
| **基本パネル回帰** | 500 | 1,000+ | 5-10年 |
| **トップジャーナル (SMJ, AMJ, OS)** | 1,500 | 2,000+ | 10-15年 |
| **IV/PSM (内生性対策)** | 1,000 | 2,000+ | 10年+ |
| **Event Study (DiD)** | 100 events | 200+ events | 事象依存 |

**サンプル選択基準**:

```python
# 典型的サンプル選択
sample = df[
    # 1. 期間
    (df['year'] >= 2010) & (df['year'] <= 2020) &
    
    # 2. 産業: 製造業（SIC 2000-3999）
    (df['sic_code'] >= 2000) & (df['sic_code'] <= 3999) &
    
    # 3. データ品質
    (df['total_assets'] > 0) &
    (df['revenue'] > 0) &
    (df['net_income'].notna()) &
    
    # 4. 外れ値除外: Winsorization
    (df['roa'] >= df['roa'].quantile(0.01)) &
    (df['roa'] <= df['roa'].quantile(0.99))
].copy()

print(f"Sample size: {len(sample)} firm-years")
print(f"Unique firms: {sample['firm_id'].nunique()}")
print(f"Years: {sample['year'].min()}-{sample['year'].max()}")
print(f"Industries (SIC2): {sample['sic_code'].apply(lambda x: x//100).nunique()}")

# サンプル記述統計
sample[['roa', 'rd_intensity', 'firm_size', 'leverage']].describe()
```

**Survival Bias対策**:
```python
# 生存バイアスチェック: 全期間存続企業のみか？
full_panel_firms = sample.groupby('firm_id')['year'].count()
expected_years = sample['year'].max() - sample['year'].min() + 1

print(f"Expected years per firm: {expected_years}")
print(f"Mean years per firm: {full_panel_firms.mean():.2f}")
print(f"% of firms with full panel: {(full_panel_firms == expected_years).mean()*100:.1f}%")

# 推奨: Unbalanced panelを許容（生存バイアス軽減）
```

---

## Phase 2: Data Source Discovery

### 2.1 データソース選択

→ **詳細**: `2-data-sources` skill

**地域別主要データソース**:

| 地域 | 財務データ | 株価データ | 役員データ |
|------|----------|----------|-----------|
| **北米** | Compustat ⭐⭐⭐⭐⭐ | CRSP ⭐⭐⭐⭐⭐ | ExecuComp ⭐⭐⭐⭐⭐ |
| **欧州** | Orbis ⭐⭐⭐⭐ | Datastream ⭐⭐⭐⭐ | Orbis ⭐⭐⭐ |
| **日本** | EDINET ⭐⭐⭐⭐⭐ | JPX ⭐⭐⭐⭐ | EDINET ⭐⭐⭐⭐ |
| **韓国** | DART ⭐⭐⭐⭐ | KRX ⭐⭐⭐⭐ | DART ⭐⭐⭐ |
| **中国** | CNINFO ⭐⭐⭐ | Tushare ⭐⭐⭐ | - |

**無料 vs 有料**:

```python
# 北米企業研究
if has_wrds_access:
    # 有料: WRDS（推奨: トップジャーナル水準）
    data_source = "Compustat + CRSP via WRDS"
else:
    # 無料: SEC EDGAR（品質は劣るが可能）
    data_source = "SEC EDGAR 10-K filings"
    print("Warning: Manual extraction required, quality may vary")

# 日本企業研究
data_source = "EDINET API (完全無料)"  # 推奨: 公式API、高品質
```

### 2.2 変数-データソース対応表

| 変数 | データソース | 取得難易度 |
|------|------------|----------|
| **ROA** | Compustat/EDINET | ⭐☆☆☆☆ 容易 |
| **Tobin's Q** | Compustat + CRSP | ⭐⭐☆☆☆ 中 |
| **R&D Intensity** | Compustat | ⭐☆☆☆☆ 容易 |
| **Patent Count** | USPTO/JPO | ⭐⭐⭐☆☆ 中高 |
| **Board Interlock** | Proxy Statement/EDINET | ⭐⭐⭐⭐☆ 高 |
| **MD&A Sentiment** | SEC 10-K | ⭐⭐⭐⭐☆ 高 |
| **ESG Score** | MSCI/CDP | ⭐⭐⭐☆☆ 中高 |

---

## Phase 3: Data Collection Strategy

### 3.1 収集計画立案

**収集プロジェクト構造**:
```
project/
├── data/
│   ├── raw/              # 生データ（変更厳禁）
│   ├── processed/        # 前処理済み
│   └── final/            # 分析用最終版
├── code/
│   ├── 01_collect.py     # データ収集
│   ├── 02_clean.py       # データクリーニング
│   ├── 03_merge.py       # データマージ
│   └── 04_variables.py   # 変数構築
├── docs/
│   └── data_dictionary.md # 変数辞書
└── README.md
```

### 3.2 データ収集実装

→ **詳細実装**: `2-data-sources` skill

**北米企業（WRDS経由）**:
```python
import wrds

# WRDS接続
db = wrds.Connection()

# Compustat財務データ
compustat = db.raw_sql("""
    SELECT gvkey, datadate, fyear, sich, 
           at AS total_assets,
           sale AS revenue,
           ni AS net_income,
           xrd AS rd_expense,
           dltt AS long_term_debt,
           dlc AS current_debt
    FROM comp.funda
    WHERE indfmt='INDL' AND datafmt='STD' AND popsrc='D' AND consol='C'
        AND fyear BETWEEN 2010 AND 2020
        AND sich BETWEEN 2000 AND 3999
""")

# CRSP株価データ
crsp = db.raw_sql("""
    SELECT permno, date, prc, shrout
    FROM crsp.dsf
    WHERE date BETWEEN '2010-01-01' AND '2020-12-31'
""")

db.close()
```

**日本企業（EDINET API）**:
```python
# → 詳細実装は 2-data-sources skill参照
from edinet_collector import EDINETCollector

collector = EDINETCollector()
df_japan = collector.collect_sample(
    start_date='2010-01-01',
    end_date='2020-12-31',
    doc_type='有価証券報告書'
)
```

### 3.3 リスク管理

| リスク | 発生確率 | 対策 |
|--------|---------|------|
| **API制限** | 高 | time.sleep(), バッチ処理 |
| **欠損値** | 高 | 多重代入法, 除外基準明確化 |
| **データ形式不整合** | 中 | 標準化スクリプト |
| **アクセス期限切れ** | 低 | ダウンロード後ローカル保存 |

---

## Phase 4: Panel Dataset Construction

### 4.1 Panel構造の理解

**Panel Data構造**:
```
       firm_id  year  roa  rd_intensity  firm_size
0      1001     2010  0.05  0.03          8.5
1      1001     2011  0.06  0.04          8.6
2      1001     2012  0.04  0.03          8.7
...
1000   2500     2020  0.08  0.05          9.2
```

**特徴**:
- **Cross-sectional dimension**: 複数企業（firm_id）
- **Time-series dimension**: 複数年（year）
- **Balanced vs Unbalanced**: 全企業が全期間存在するか

### 4.2 MultiIndex設定

```python
import pandas as pd

# Panel構造設定
df_panel = df.set_index(['firm_id', 'year']).sort_index()

print(df_panel.head())
print(f"Panel shape: {df_panel.shape}")
print(f"Firms: {df_panel.index.get_level_values('firm_id').nunique()}")
print(f"Years: {df_panel.index.get_level_values('year').nunique()}")

# Balanced panel確認
firms_per_year = df_panel.groupby('year').size()
print("\nObservations per year:")
print(firms_per_year)
```

### 4.3 複数データソースのマージ

**マージ戦略**:

```python
# 1. Compustat財務データ
df_financial = compustat[['gvkey', 'fyear', 'at', 'sale', 'ni', 'xrd']].copy()
df_financial = df_financial.rename(columns={'gvkey': 'firm_id', 'fyear': 'year'})

# 2. CRSP株価データ → 年次平均
df_price = crsp.groupby(['permno', crsp['date'].dt.year])['prc'].mean().reset_index()
df_price = df_price.rename(columns={'permno': 'firm_id', 'date': 'year'})

# 3. Patent データ
df_patent = patents[['assignee_id', 'year', 'patent_count']].copy()
df_patent = df_patent.rename(columns={'assignee_id': 'firm_id'})

# マージ
df_merged = df_financial.merge(
    df_price, on=['firm_id', 'year'], how='left'
).merge(
    df_patent, on=['firm_id', 'year'], how='left'
)

# 欠損値確認
print("Missing values:")
print(df_merged.isnull().sum())
```

**マージ診断**:
```python
# マージ成功率
print(f"Financial data: {len(df_financial)} obs")
print(f"Price data: {len(df_price)} obs")
print(f"Merged data: {len(df_merged)} obs")
print(f"Match rate: {len(df_merged) / len(df_financial) * 100:.1f}%")

# 未マッチ企業の確認
unmatched_firms = set(df_financial['firm_id']) - set(df_merged['firm_id'])
print(f"Unmatched firms: {len(unmatched_firms)}")
```

---

## Phase 5: Quality Assurance

### 5.1 QAチェックリスト

→ **詳細**: `_shared/quality-checklist.md`

**必須チェック**:
- [ ] **欠損値**: 各変数の欠損率 < 10%
- [ ] **外れ値**: Winsorization (1%, 99%)実施
- [ ] **重複**: firm_id × year の一意性確認
- [ ] **変数範囲**: 論理的範囲内か（ROA: -1～1, Leverage: 0～10）
- [ ] **サンプルサイズ**: 最低500 firm-years（推奨: 1000+）
- [ ] **Survival bias**: Unbalanced panel許容or対策

### 5.2 実装: QA自動化

```python
def data_quality_check(df, id_var='firm_id', time_var='year'):
    """データ品質チェック自動化"""
    
    print("="*50)
    print("DATA QUALITY ASSURANCE REPORT")
    print("="*50)
    
    # 1. 基本情報
    print(f"\n1. BASIC INFO")
    print(f"   Shape: {df.shape}")
    print(f"   Firms: {df[id_var].nunique()}")
    print(f"   Years: {df[time_var].min()}-{df[time_var].max()}")
    
    # 2. 欠損値
    print(f"\n2. MISSING VALUES")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_report = pd.DataFrame({
        'Missing': missing,
        'Percentage': missing_pct
    })
    print(missing_report[missing_report['Missing'] > 0])
    
    # 3. 重複
    print(f"\n3. DUPLICATES")
    duplicates = df.duplicated(subset=[id_var, time_var]).sum()
    print(f"   Duplicate rows: {duplicates}")
    
    # 4. 外れ値
    print(f"\n4. OUTLIERS")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outliers = ((df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)).sum()
        print(f"   {col}: {outliers} outliers ({outliers/len(df)*100:.1f}%)")
    
    # 5. Panel balance
    print(f"\n5. PANEL BALANCE")
    firms_per_year = df.groupby(time_var)[id_var].nunique()
    print(f"   Mean firms/year: {firms_per_year.mean():.0f}")
    print(f"   Min firms/year: {firms_per_year.min()}")
    print(f"   Max firms/year: {firms_per_year.max()}")
    
    print("="*50)
    print("QA CHECK COMPLETE")
    print("="*50)

# 実行
data_quality_check(df_panel.reset_index())
```

---

## Phase 6: Variable Construction

### 6.1 標準変数構築

→ **詳細**: `_shared/common-definitions.md`

**Performance Variables**:
```python
# ROA
df['roa'] = df['net_income'] / df['total_assets']

# ROE
df['roe'] = df['net_income'] / df['equity']

# Tobin's Q (Market Value / Book Value)
df['tobin_q'] = (df['market_cap'] + df['total_debt']) / df['total_assets']
```

**Innovation Variables**:
```python
# R&D Intensity
df['rd_intensity'] = df['rd_expense'] / df['revenue']
df['rd_intensity'] = df['rd_intensity'].fillna(0)  # 未報告 = 0

# Patent Count (log+1)
df['patent_count_log'] = np.log(df['patent_count'] + 1)

# Citation-weighted Patents
df['patent_quality'] = df['citation_count'] / df['patent_count']
```

**Control Variables**:
```python
# Firm Size (log of total assets)
df['firm_size'] = np.log(df['total_assets'])

# Leverage
df['leverage'] = df['total_debt'] / df['total_assets']

# Firm Age (log)
df['firm_age_log'] = np.log(df['firm_age'] + 1)

# Cash Ratio
df['cash_ratio'] = df['cash'] / df['total_assets']
```

### 6.2 ラグ変数の作成

```python
# 1年ラグ（独立変数）
df = df.sort_values(['firm_id', 'year'])
df['rd_intensity_lag1'] = df.groupby('firm_id')['rd_intensity'].shift(1)
df['firm_size_lag1'] = df.groupby('firm_id')['firm_size'].shift(1)

# 理由: 内生性軽減（同時性バイアス回避）
# DV: ROA_t を IV: RD_intensity_{t-1} で説明
```

### 6.3 調整変数・交互作用項

```python
# 調整変数の標準化（mean=0, sd=1）
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df['rd_intensity_std'] = scaler.fit_transform(df[['rd_intensity']])
df['industry_maturity_std'] = scaler.fit_transform(df[['industry_maturity']])

# 交互作用項
df['rd_x_maturity'] = df['rd_intensity_std'] * df['industry_maturity_std']
```

---

## Phase 7: Statistical Analysis

### 7.1 記述統計

```python
# 記述統計
desc_stats = df[['roa', 'rd_intensity', 'firm_size', 'leverage']].describe()
print(desc_stats.T)

# 相関行列
corr_matrix = df[['roa', 'rd_intensity', 'firm_size', 'leverage']].corr()
print("\nCorrelation Matrix:")
print(corr_matrix)

# VIF（多重共線性チェック）
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = df[['rd_intensity', 'firm_size', 'leverage']].dropna()
vif = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print("\nVIF (Multicollinearity Check):")
print(vif)
# VIF > 10: 多重共線性あり
```

### 7.2 パネル回帰

→ **詳細**: `3-statistical-methods` skill

**Fixed Effects回帰**:
```python
from linearmodels.panel import PanelOLS

# データ準備
df_panel = df.set_index(['firm_id', 'year'])

# FE回帰
model_fe = PanelOLS.from_formula(
    'roa ~ rd_intensity_lag1 + firm_size_lag1 + leverage + EntityEffects + TimeEffects',
    data=df_panel
)

result_fe = model_fe.fit(cov_type='clustered', cluster_entity=True)
print(result_fe.summary)
```

**Random Effects回帰**:
```python
from linearmodels.panel import RandomEffects

model_re = RandomEffects.from_formula(
    'roa ~ rd_intensity_lag1 + firm_size_lag1 + leverage',
    data=df_panel
)

result_re = model_re.fit()
print(result_re.summary)
```

**Hausman Test (FE vs RE)**:
```python
# Hausman test実装
# H0: RE適切, H1: FE適切
# 実装は 3-statistical-methods skill参照
```

### 7.3 調整効果検証

```python
# 交互作用項を含むモデル
model_interaction = PanelOLS.from_formula(
    'roa ~ rd_intensity_std + industry_maturity_std + rd_x_maturity + '
    'firm_size_lag1 + leverage + EntityEffects + TimeEffects',
    data=df_panel
)

result_int = model_interaction.fit(cov_type='clustered', cluster_entity=True)
print(result_int.summary)

# 交互作用の解釈: rd_x_maturity係数
# 正: 産業成熟度が高いほど、R&Dの効果が強まる
# 負: 産業成熟度が高いほど、R&Dの効果が弱まる
```

---

## Phase 8: Documentation & Reproducibility

### 8.1 再現パッケージ作成

→ **詳細**: `8-automation` skill

**必須要素**:
```
replication_package/
├── README.md              # 実行手順
├── requirements.txt       # Python依存関係
├── data/
│   ├── raw/              # 生データ
│   └── processed/        # 前処理済み
├── code/
│   ├── 01_collect.py
│   ├── 02_clean.py
│   ├── 03_analysis.py
│   └── run_all.sh        # 全スクリプト実行
├── output/
│   ├── tables/           # 回帰結果表
│   └── figures/          # 図
└── docs/
    ├── data_dictionary.md
    └── codebook.pdf
```

### 8.2 Data Dictionary作成

```markdown
# Data Dictionary

## Variables

| Variable | Description | Source | Calculation |
|----------|-------------|--------|-------------|
| roa | Return on Assets | Compustat | net_income / total_assets |
| rd_intensity | R&D Intensity | Compustat | rd_expense / revenue |
| firm_size | Firm Size (log) | Compustat | log(total_assets) |
| leverage | Financial Leverage | Compustat | total_debt / total_assets |

## Sample Selection

- **Data Source**: Compustat North America (WRDS)
- **Period**: 2010-2020
- **Industry**: Manufacturing (SIC 2000-3999)
- **Sample Size**: 12,450 firm-years (1,245 unique firms)
- **Missing Data**: Dropped if ROA or R&D missing
- **Winsorization**: 1% and 99% for all continuous variables
```

---

## Quick Start Guide

### 30分でスタート

**Step 1**: RQを1文で書く（5分）
```
例: 「環境不確実性が高い状況で、探索的イノベーションが短期パフォーマンスに
与える負の影響は、どのような組織的条件で緩和されるか？」
```

**Step 2**: 理論フレームワーク選択（10分）
→ `_shared/THEORY_FRAMEWORKS.md` 参照
```
例: Dynamic Capabilities + Organizational Learning
```

**Step 3**: 仮説を3つ導出（10分）
```
H1: 探索的イノベーション → 短期ROA（負）
H2: Organizational Slack → H1を弱める（調整効果）
H3: Absorptive Capacity → H1を弱める（調整効果）
```

**Step 4**: 必要な変数をリストアップ（5分）
→ `_shared/common-definitions.md` 参照

### 1週間でPhase 1-3完了

**Day 1-2**: Phase 1（Research Design）
- RQ精緻化
- 文献レビュー
- 仮説導出

**Day 3-4**: Phase 2（Data Source Discovery）
→ `2-data-sources` skill使用
- 北米: Compustat選択
- 日本: EDINET選択

**Day 5-7**: Phase 3（Data Collection Strategy）
→ `2-data-sources` + `8-automation` skills
- API実装
- バッチ収集

### 1ヶ月でPhase 1-8完走

**Week 1**: Phase 1-3（設計〜収集戦略）
**Week 2**: Phase 4-5（Panel構築〜QA）
**Week 3**: Phase 6-7（変数構築〜分析）
**Week 4**: Phase 8（Documentation） + 論文執筆開始

---

## Common Pitfalls

### Pitfall 1: 曖昧なRQ

❌ **悪い例**: 「イノベーションと企業パフォーマンスの関係」

**問題**:
- 既存研究で既に確立
- 変数が曖昧（「イノベーション」とは？）
- 条件・メカニズムなし

✅ **良い例**: 「環境不確実性が高い状況で、探索的イノベーション（特許の新規技術クラス比率）が短期ROAに与える負の影響は、組織スラック（現金比率）によってどの程度緩和されるか？」

### Pitfall 2: サンプルサイズ不足

❌ **悪い例**: 100社×3年 = 300 firm-years

**問題**:
- トップジャーナル基準（2000+）に遠く及ばない
- 統計的検出力不足
- Robustness checks実施不可

✅ **解決策**:
- 期間延長: 3年 → 10年
- 産業拡大: 製造業のみ → 全産業
- 地域拡大: 米国のみ → 北米全体

### Pitfall 3: 内生性への無対策

❌ **悪い例**: OLS回帰のみ

**問題**:
- 逆因果: パフォーマンス良好 → R&D投資増加
- 同時性バイアス
- 交絡変数

✅ **解決策**:
→ `3-statistical-methods` skill参照
- ラグ変数使用: IV_{t-1} → DV_t
- Instrumental Variables (IV)
- PSM, Heckman Selection

### Pitfall 4: 理論と分析の乖離

❌ **悪い例**: 理論で「動的プロセス」を主張するが、分析はクロスセクション

**問題**:
- 因果メカニズムが検証されていない
- 時間的順序が不明

✅ **解決策**:
- Panel分析で時間的順序を明示
- ラグ構造で因果の方向性を示す
- 媒介分析でメカニズムを検証

### Pitfall 5: Robustness Checks不足

❌ **悪い例**: メインモデル1つのみ

**問題**:
- 結果の頑健性が不明
- レビュアーから要求される

✅ **解決策**: 最低5つのRobustness Checks
1. 代替DV（ROA → ROE, Tobin's Q）
2. 代替IV測定（R&D Intensity → Patent Count）
3. サブサンプル（大企業のみ、小企業のみ）
4. 代替推定法（FE → GMM）
5. Winsorization水準変更（1%,99% → 5%,95%）

---

## FAQ

### Q1: 初めての定量研究。どこから始めるべきか？

**A**: 以下の3ステップを推奨します：

**Step 1**: 既存研究のレプリケーション（2-3週間）
- トップジャーナル（SMJ, AMJ, OS）から1本選ぶ
- データ収集〜分析を完全再現
- 手法を学ぶ最速の方法

**Step 2**: 小規模プロトタイプ（1-2週間）
- 100社×5年で試行
- Phase 1-8を一通り経験
- 問題点を洗い出す

**Step 3**: 本格研究開始（3-6ヶ月）
- サンプル拡大: 1000+社×10年
- Phase 1から本ロードマップ通りに実行

---

### Q2: トップジャーナル（SMJ, AMJ, OS）に載るには？

**A**: 以下の基準を満たす必要があります：

**理論的貢献**:
- 既存理論の拡張・修正
- 新しい因果メカニズムの発見
- 境界条件（Boundary Conditions）の特定

**方法論的厳密性**:
- サンプルサイズ: **2000+ firm-years**
- 内生性対策: **IV, PSM, Heckman等**
- Robustness checks: **最低5つ**
- Fixed Effects + Clustered SE

**実装ガイド**:
→ `_shared/quality-checklist.md#top-journal-standards`

---

### Q3: データ収集に何日かかるか？

**A**: データソースと規模により異なります：

| データソース | 規模 | 所要時間 |
|-------------|------|---------|
| **Compustat (WRDS)** | 1000社×10年 | **1-2日** |
| **EDINET (日本)** | 1000社×10年 | **3-5日** |
| **SEC EDGAR (手動)** | 100社×10年 | **2-3週間** |
| **Patent (USPTO)** | 1000社×10年 | **1-2週間** |

**時間短縮Tips**:
→ `8-automation` skill（自動化スクリプト）
→ `2-data-sources` skill（API実装例）

---

### Q4: Pythonの知識がない。学ぶべきか？

**A**: **必須です**。以下を習得してください：

**最低限必要なスキル**（習得時間: 2-3週間）:
- **pandas**: データフレーム操作
- **numpy**: 数値計算
- **statsmodels/linearmodels**: 回帰分析
- **matplotlib/seaborn**: 可視化

**学習リソース**:
- [Python for Data Analysis](https://wesmckinney.com/book/) (Wes McKinney)
- [pandas公式チュートリアル](https://pandas.pydata.org/docs/getting_started/index.html)
- `8-automation` skill（実装例が豊富）

**代替案**:
- **Stata**: 学術研究で広く使用、パネル分析に強い
- **R**: 統計分析・可視化に優れる
→ ただし**Pythonが最も汎用性が高い**（データ収集〜分析〜可視化）

---

### Q5: どのスキルをいつ使うべきか？

**A**: Phase別に以下のスキルを参照してください：

| Phase | 主要スキル | 目的 |
|-------|-----------|------|
| **Phase 1-3** | 本スキル（core-workflow） | 研究設計・計画 |
| **Phase 2** | `2-data-sources` | データソース探索 |
| **Phase 3** | `2-data-sources` + `8-automation` | データ収集 |
| **Phase 4** | 本スキル + `8-automation` | Panel構築 |
| **Phase 5** | `_shared/quality-checklist.md` | QA |
| **Phase 6** | `_shared/common-definitions.md` + 専門スキル | 変数構築 |
| **Phase 7** | `3-statistical-methods` | 統計分析 |
| **Phase 8** | `8-automation` | 再現パッケージ |

**専門スキル（Phase 6で必要に応じて）**:
- テキスト変数 → `4-text-analysis`
- ネットワーク変数 → `5-network-analysis`
- ESG変数 → `7-esg-sustainability`
- 因果推論 → `6-causal-ml`

**詳細な選択ガイド**:
→ `SKILL-INDEX.md`（Decision Tree形式）
→ `_shared/cross-references.md`（Phase別参照マップ）

---

### Q6: 内生性問題とは？どう対処するか？

**A**: 内生性の3タイプと対策：

**1. Omitted Variable Bias（欠落変数バイアス）**
```
問題: 重要な変数を統制していない
対策: 理論に基づく統制変数の追加 + Fixed Effects
```

**2. Reverse Causality（逆因果）**
```
問題: Y → X の逆方向の因果関係
対策: ラグ変数（X_{t-1} → Y_t）
     Instrumental Variables (IV)
```

**3. Simultaneity（同時性）**
```
問題: XとYが同時に決定される
対策: 2SLS (Two-Stage Least Squares)
     GMM (Generalized Method of Moments)
```

**詳細実装**:
→ `3-statistical-methods` skill

---

## パッケージインストール

```bash
# 必須パッケージ
pip install pandas numpy scipy statsmodels linearmodels

# データ収集
pip install wrds requests beautifulsoup4

# 可視化
pip install matplotlib seaborn

# WRDS接続（要アカウント）
pip install wrds

# 推奨: 全依存関係
pip install -r requirements.txt
```

---

## 参考文献

### 必読文献

**方法論**:
- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data*. MIT Press.
- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.

**戦略研究**:
- Barney, J. (1991). "Firm resources and sustained competitive advantage." *Journal of Management*, 17(1), 99-120.
- Teece, D. J., Pisano, G., & Shuen, A. (1997). "Dynamic capabilities and strategic management." *Strategic Management Journal*, 18(7), 509-533.

**組織研究**:
- March, J. G. (1991). "Exploration and exploitation in organizational learning." *Organization Science*, 2(1), 71-87.

### トップジャーナル

- **Strategic Management Journal (SMJ)**
- **Academy of Management Journal (AMJ)**
- **Organization Science (OS)**
- **Journal of Management (JOM)**

---

## Quick Reference: Phase-Skill Mapping

| Phase | Duration | Key Skills | Output |
|-------|----------|-----------|--------|
| **1. Research Design** | 1-2週間 | core-workflow, THEORY_FRAMEWORKS | RQ, 仮説 |
| **2. Data Source Discovery** | 3-5日 | data-sources | データソースリスト |
| **3. Data Collection** | 1-3週間 | data-sources, automation | 生データ |
| **4. Panel Construction** | 3-5日 | core-workflow | パネルデータ |
| **5. Quality Assurance** | 2-3日 | quality-checklist | クリーンデータ |
| **6. Variable Construction** | 3-5日 | common-definitions, 専門スキル | 分析変数 |
| **7. Statistical Analysis** | 1-2週間 | statistical-methods | 回帰結果 |
| **8. Documentation** | 3-5日 | automation | 再現パッケージ |

**Total**: 約2-3ヶ月（フルタイム想定）

---

**Version**: 4.0  
**Last Updated**: 2025-11-01  
**Maintainer**: Strategic Research Suite Team  
**License**: MIT

---

**Next Steps**:
1. データソース探索 → `2-data-sources` skill
2. 統計分析手法 → `3-statistical-methods` skill
3. 完全自動化 → `8-automation` skill
**症状**:
```
HTTPError 403: Forbidden
ConnectionError: Failed to establish connection
```

**原因**:
- User-Agent未設定
- API key無効またはexpired
- IP制限・Rate limit
- ネットワーク接続問題

**解決策**:

#### 1. User-Agentを設定:
```python
headers = {
    'User-Agent': 'YourUniversity research@email.edu'
}
response = requests.get(url, headers=headers)
```

#### 2. API keyを確認:
```python
import os
api_key = os.getenv('API_KEY')
if not api_key:
    print("API key not set. Export it: export API_KEY='your_key'")
```

#### 3. Rate limitに対処:
```python
import time
from functools import wraps

def rate_limited(max_calls=10, period=60):
    """Rate limiting decorator"""
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            
            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                print(f"Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
            
            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limited(max_calls=10, period=60)
def call_api(url):
    return requests.get(url)
```

#### 4. リトライロジック:
```python
def fetch_with_retry(url, max_retries=3, backoff=5):
    """Exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = backoff * (2 ** attempt)
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
            else:
                raise
```

---

### 🟠 Problem 2: Memory Error with Large Dataset

**症状**:
```
MemoryError: Unable to allocate array
Killed (OOM)
```

**原因**:
- データを一度に全てメモリにロード
- `float64`の過度な使用
- 不要なカラムの保持
- データのコピーが多い

**解決策**:

#### 1. Chunk processingを使用:
```python
# Instead of:
df = pd.read_csv('large_file.csv')

# Use:
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    # Process each chunk
    processed = process_chunk(chunk)
    chunks.append(processed)

df = pd.concat(chunks, ignore_index=True)
```

#### 2. dtypeを最適化:
```python
# Memory optimization
df['year'] = df['year'].astype('int16')       # int64 → int16 (4x less)
df['firm_id'] = df['firm_id'].astype('category')  # string → category
df['industry'] = df['industry'].astype('category')

# Check memory usage
print(df.memory_usage(deep=True))
```

#### 3. 不要なカラムを削除:
```python
# Only load needed columns
df = pd.read_csv('file.csv', usecols=['col1', 'col2', 'col3'])

# Drop columns after use
df = df.drop(columns=['temp_col1', 'temp_col2'])
```

#### 4. In-place操作を使用:
```python
# Bad: creates copy
df = df.fillna(0)

# Good: in-place
df.fillna(0, inplace=True)
```

#### 5. Daskを使用（超大規模データ）:
```python
import dask.dataframe as dd

# Lazy loading
ddf = dd.read_csv('huge_file.csv')

# Parallel processing
result = ddf.groupby('firm_id').mean().compute()
```

---

### 🟡 Problem 3: Text Encoding Issues

**症状**:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte
UnicodeEncodeError: 'ascii' codec can't encode character
```

**原因**:
- ファイルがUTF-8以外のエンコーディング
- 特殊文字・絵文字の処理
- HTML entities

**解決策**:

#### 1. エンコーディングを検出:
```python
import chardet

# Detect encoding
with open('file.txt', 'rb') as f:
    result = chardet.detect(f.read(10000))
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")

# Read with detected encoding
df = pd.read_csv('file.csv', encoding=encoding)
```

#### 2. エンコーディングエラーを処理:
```python
# Ignore errors
df = pd.read_csv('file.csv', encoding='utf-8', errors='ignore')

# Replace errors
df = pd.read_csv('file.csv', encoding='utf-8', errors='replace')

# Best: specify correct encoding
df = pd.read_csv('file.csv', encoding='shift_jis')  # For Japanese
```

#### 3. テキストをクリーニング:
```python
import unicodedata

def clean_text(text):
    """Remove special characters"""
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ASCII
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text

df['text'] = df['text'].apply(clean_text)
```

---

### 🟢 Problem 4: Missing Data Handling

**症状**:
- モデルが収束しない
- 統計検定で奇妙な結果
- サンプルサイズが大幅に減少

**原因**:
- 欠損値の不適切な処理
- Listwise deletion（完全データのみ使用）
- 欠損パターンの無視

**解決策**:

#### 1. 欠損値を確認:
```python
# Missing value summary
missing_summary = pd.DataFrame({
    'column': df.columns,
    'missing_count': df.isnull().sum(),
    'missing_pct': (df.isnull().sum() / len(df) * 100).round(2)
})

print(missing_summary[missing_summary['missing_count'] > 0])

# Visualize missing pattern
import missingno as msno
msno.matrix(df)
plt.show()
```

#### 2. 適切な補完方法を選択:
```python
# Mean imputation (連続変数)
df['revenue'].fillna(df['revenue'].mean(), inplace=True)

# Median imputation (外れ値がある場合)
df['revenue'].fillna(df['revenue'].median(), inplace=True)

# Forward fill (時系列データ)
df['price'] = df.groupby('firm_id')['price'].fillna(method='ffill')

# Industry mean (グループ別平均)
df['leverage'] = df.groupby('industry')['leverage'].transform(
    lambda x: x.fillna(x.mean())
)
```

#### 3. 欠損フラグを作成:
```python
# Create missing indicator
df['revenue_missing'] = df['revenue'].isnull().astype(int)

# Then impute
df['revenue'].fillna(0, inplace=True)
```

---

### 🔵 Problem 5: Slow Processing / Performance

**症状**:
- コードが数時間かかる
- CPUが100%で固まる
- プログレスバーが動かない

**解決策**:

#### 1. ボトルネックを特定:
```python
import time

# Simple timing
start = time.time()
result = slow_function()
print(f"Elapsed: {time.time() - start:.2f}s")

# Line profiler
%load_ext line_profiler
%lprun -f slow_function slow_function()
```

#### 2. Vectorization を使用:
```python
# Bad: Loop
for i in range(len(df)):
    df.loc[i, 'result'] = df.loc[i, 'a'] * df.loc[i, 'b']

# Good: Vectorized
df['result'] = df['a'] * df['b']
```

#### 3. 並列処理:
```python
from multiprocessing import Pool

def process_firm(firm_id):
    # Heavy computation
    return result

# Parallel processing
with Pool(processes=4) as pool:
    results = pool.map(process_firm, firm_ids)
```

#### 4. プログレスバー:
```python
from tqdm import tqdm

# Add progress bar
for item in tqdm(items, desc="Processing"):
    process(item)
```

---

### 📚 General Debugging Tips

#### 1. データの品質確認:
```python
# Quick data check
def check_data_quality(df):
    print(f"Shape: {df.shape}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nMissing:\n{df.isnull().sum()}")
    print(f"\nDuplicates: {df.duplicated().sum()}")
    print(f"\nSummary:\n{df.describe()}")

check_data_quality(df)
```

#### 2. Small sampleでテスト:
```python
# Test with small sample first
df_sample = df.head(100)
result = your_function(df_sample)

# If works, run on full data
result = your_function(df)
```

#### 3. ログを出力:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("Starting process...")
logger.warning("Missing data detected")
logger.error("API call failed")
```

---

### 🆘 When to Ask for Help

**Stack Overflow前のチェックリスト**:
1. ✅ エラーメッセージを完全に読んだか？
2. ✅ Google検索したか？
3. ✅ 公式ドキュメントを確認したか？
4. ✅ Small exampleで再現できるか？
5. ✅ パッケージバージョンを確認したか？

**質問テンプレート**:
```
【環境】
- OS: macOS 14.0
- Python: 3.11.5
- pandas: 2.0.3

【問題】
[簡潔な説明]

【再現コード】
[最小限の実行可能コード]

【エラーメッセージ】
[完全なトレースバック]

【試したこと】
1. [試した対処法1] → [結果]
2. [試した対処法2] → [結果]
```

---

**Version**: 4.0  
**Last Updated**: 2025-11-01
