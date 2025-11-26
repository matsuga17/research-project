---
name: strategic-research-statistical-methods
description: Advanced statistical methods for strategic management research including panel regression (Fixed Effects, Random Effects, Pooled OLS), endogeneity solutions (IV, PSM, Heckman, DiD), moderation and mediation analysis, multilevel modeling, survival analysis, and comprehensive robustness checks with implementation examples.
version: 4.0
part_of: strategic-research-suite
related_skills:
  - core-workflow: Phase 7 (Statistical Analysis)
  - data-sources: Data integration for analysis
  - text-analysis: Text-derived variables in regression
  - network-analysis: Network variables in regression
  - causal-ml: Advanced causal inference methods
---

# Statistical Methods Advanced v4.0

**Part of**: [Strategic Research Suite v4.0](../README.md)

---

## 🎯 このスキルについて

戦略経営・組織論研究で使用する**高度な統計手法**を、実装可能なPythonコード付きで提供します。

### カバレッジ

```
統計手法:
├─ パネル回帰: FE, RE, Pooled OLS
├─ 内生性対策: IV, PSM, Heckman, DiD
├─ 調整効果・媒介効果分析
├─ 多階層モデル (MLM)
├─ 生存分析 (Cox Hazard)
├─ Robustness Checks
└─ 診断テスト (VIF, 異分散性等)
```

---

### いつ使うか

✅ **Phase 7: Statistical Analysis**
- 仮説検証のための統計分析
- 内生性問題への対処
- Robustness checksの実施

✅ **論文執筆時**
- トップジャーナル基準の分析
- 査読者コメントへの対応

✅ **研究設計段階**
- 適切な分析手法の選択
- サンプルサイズ計算

---

### 前提条件

**必須知識**:
- 回帰分析の基礎
- パネルデータの概念
- 統計的仮説検定

**推奨知識**:
- 計量経済学の基礎
- 因果推論の概念
- Python/R経験

**技術環境**:
- Python 3.8以上
- statsmodels, linearmodels

---

### 他スキルとの連携

| 用途 | 連携スキル | 目的 |
|------|-----------|------|
| 基本ワークフロー | `1-core-workflow` Phase 7 | 分析の位置づけ |
| テキスト変数 | `4-text-analysis` | センチメント等を説明変数に |
| ネットワーク変数 | `5-network-analysis` | Centrality等を説明変数に |
| 高度因果推論 | `6-causal-ml` | ML+因果推論 |

---

## 📋 目次

1. [パネル回帰](#1-パネル回帰)
2. [内生性対策](#2-内生性対策)
3. [調整効果分析](#3-調整効果分析)
4. [媒介効果分析](#4-媒介効果分析)
5. [多階層モデル](#5-多階層モデルmlm)
6. [生存分析](#6-生存分析)
7. [Robustness Checks](#7-robustness-checks)
8. [診断テスト](#8-診断テスト)

---

## 1. パネル回帰

### 1.1 基本概念

**パネルデータ**: 複数の企業（i）を複数の時点（t）で観測

```
データ構造:
- N: 企業数
- T: 期間
- N × T: 総観測数
```

**3つの主要手法**:
1. **Pooled OLS**: パネル構造を無視
2. **Fixed Effects (FE)**: 企業固有効果を統制
3. **Random Effects (RE)**: 企業固有効果をランダムと仮定

---

### 1.2 Pooled OLS

**モデル**:
```
Y_it = β₀ + β₁X_it + β₂Controls_it + ε_it
```

**特徴**:
- 最もシンプル
- 企業固有効果を無視（バイアスの可能性）

**実装**:

```python
import pandas as pd
import statsmodels.formula.api as smf

# データ準備（既にパネル構造）
# df: (firm_id, year)のMultiIndex

# Pooled OLS
model_pooled = smf.ols('''
roa ~ rd_intensity + firm_size + leverage + firm_age + 
      capital_intensity + C(industry) + C(year)
''', data=df.reset_index()).fit(
    cov_type='cluster',
    cov_kwds={'groups': df.reset_index()['firm_id']}
)

print(model_pooled.summary())

# 結果の保存
results_pooled = {
    'coef_rd': model_pooled.params['rd_intensity'],
    'se_rd': model_pooled.bse['rd_intensity'],
    'pval_rd': model_pooled.pvalues['rd_intensity'],
    'r2': model_pooled.rsquared,
    'n_obs': model_pooled.nobs
}

print(f"R&D係数: {results_pooled['coef_rd']:.4f} (p={results_pooled['pval_rd']:.3f})")
```

---

### 1.3 Fixed Effects (FE)

**モデル**:
```
Y_it = β₁X_it + α_i + λ_t + ε_it

α_i: 企業固定効果（時間不変な企業特性）
λ_t: 時間固定効果（年次トレンド）
```

**特徴**:
- ✅ 企業固有の時間不変な異質性を統制
- ✅ 内生性の一部を対処
- ❌ 時間不変な変数（業界等）の効果を推定不可

**実装**:

```python
from linearmodels.panel import PanelOLS
import pandas as pd

# パネル構造確認
df_panel = df.copy()
df_panel = df_panel.sort_index()  # (firm_id, year)でソート

# Fixed Effects Model
model_fe = PanelOLS.from_formula('''
roa ~ rd_intensity + firm_size + leverage + firm_age + 
      capital_intensity + EntityEffects + TimeEffects
''', data=df_panel).fit(
    cov_type='clustered',
    cluster_entity=True  # 企業レベルでクラスタリング
)

print(model_fe)

# 主要結果
print(f"\nR&D効果:")
print(f"係数: {model_fe.params['rd_intensity']:.4f}")
print(f"標準誤差: {model_fe.std_errors['rd_intensity']:.4f}")
print(f"t統計量: {model_fe.tstats['rd_intensity']:.2f}")
print(f"p値: {model_fe.pvalues['rd_intensity']:.4f}")

# モデル適合度
print(f"\nR²: {model_fe.rsquared:.4f}")
print(f"R² (Within): {model_fe.rsquared_within:.4f}")
print(f"R² (Between): {model_fe.rsquared_between:.4f}")
print(f"R² (Overall): {model_fe.rsquared_overall:.4f}")

# 観測数
print(f"\n観測数: {model_fe.nobs}")
print(f"企業数: {model_fe.entity_info.total}")
print(f"期間: {df_panel.index.get_level_values('year').nunique()}年")
```

---

### 1.4 Random Effects (RE)

**モデル**:
```
Y_it = β₀ + β₁X_it + (u_i + ε_it)

u_i ~ N(0, σ²_u): ランダムな企業効果
```

**特徴**:
- ✅ 時間不変な変数の効果を推定可能
- ❌ 企業効果とXが無相関という強い仮定

**実装**:

```python
from linearmodels.panel import RandomEffects

# Random Effects Model
model_re = RandomEffects.from_formula('''
roa ~ rd_intensity + firm_size + leverage + firm_age + 
      capital_intensity + TimeEffects
''', data=df_panel).fit(
    cov_type='clustered',
    cluster_entity=True
)

print(model_re)

# FEとの比較
print(f"\nFE vs. RE比較:")
print(f"FE R&D係数: {model_fe.params['rd_intensity']:.4f}")
print(f"RE R&D係数: {model_re.params['rd_intensity']:.4f}")
```

---

### 1.5 Hausman Test (FE vs. RE)

**目的**: FEとREのどちらを使うべきか検定

**帰無仮説**: RE適切（企業効果とXが無相関）  
**対立仮説**: FE適切（相関あり）

```python
from linearmodels.panel import compare

# Hausman Test
comparison = compare({'FE': model_fe, 'RE': model_re})
print(comparison)

# 手動計算
hausman_stat = (model_fe.params - model_re.params).T @ \
               np.linalg.inv(model_fe.cov - model_re.cov) @ \
               (model_fe.params - model_re.params)

from scipy.stats import chi2
p_value = 1 - chi2.cdf(hausman_stat, df=len(model_fe.params))

print(f"\nHausman統計量: {hausman_stat:.2f}")
print(f"p値: {p_value:.4f}")

if p_value < 0.05:
    print("→ FE推奨（企業効果とXに相関あり）")
else:
    print("→ RE推奨（無相関の仮定OK）")
```

**実務**: ほぼ常にFEを使用（トップジャーナル標準）

---

## 2. 内生性対策

### 2.1 内生性の種類

**1. Omitted Variable Bias（欠落変数バイアス）**
```
例: 経営者能力（観測不可）がR&D投資と業績の両方に影響
対策: Fixed Effects（時間不変なら）
```

**2. Simultaneity（同時性）**
```
例: 業績良好 → R&D投資増 AND R&D投資 → 業績向上
対策: Instrumental Variables (IV)
```

**3. Measurement Error（測定誤差）**
```
例: R&D支出の報告誤差
対策: IV, Multiple Indicators
```

---

### 2.2 Instrumental Variables (IV)

**基本アイデア**: 
- 内生変数Xと相関するが、誤差項εと無相関な変数Z（操作変数）を使用

**条件**:
1. **Relevance**: Cov(Z, X) ≠ 0（強い相関）
2. **Exogeneity**: Cov(Z, ε) = 0（誤差と無相関）

**2SLS (Two-Stage Least Squares)**:

**Stage 1**: 内生変数をIVで予測
```
X = γ₀ + γ₁Z + γ₂Controls + u
```

**Stage 2**: 予測値X̂を使って回帰
```
Y = β₀ + β₁X̂ + β₂Controls + ε
```

---

### 2.3 IV実装例

**研究例**: R&D投資の効果（R&Dは内生）

**IV候補**: 業界平均R&D強度（他社のR&Dは自社業績に直接影響しない）

```python
from linearmodels.iv import IV2SLS
import pandas as pd

# 業界平均R&D計算（自社除く）
df['industry_avg_rd'] = df.groupby(['industry', 'year'])['rd_intensity'].transform(
    lambda x: (x.sum() - x) / (x.count() - 1)
)

# パネル構造
df_panel = df.set_index(['firm_id', 'year'])

# 2SLS with Fixed Effects
iv_model = IV2SLS.from_formula('''
roa ~ [rd_intensity ~ industry_avg_rd] + 
      firm_size + leverage + firm_age + capital_intensity +
      EntityEffects + TimeEffects
''', data=df_panel).fit(
    cov_type='clustered',
    cluster_entity=True
)

print(iv_model)

# IV妥当性チェック
print(f"\n【Stage 1】")
print(f"F統計量: {iv_model.first_stage.diagnostics['f.stat'].iloc[0]:.2f}")
if iv_model.first_stage.diagnostics['f.stat'].iloc[0] > 10:
    print("✓ Weak IV問題なし（F > 10）")
else:
    print("✗ Weak IV問題あり（F < 10）")

# Stage 1結果
print(f"\nIV → 内生変数の係数: {iv_model.first_stage.params.iloc[0]:.4f}")
print(f"p値: {iv_model.first_stage.pvalues.iloc[0]:.4f}")

# Stage 2結果
print(f"\n【Stage 2】")
print(f"R&D効果（IV）: {iv_model.params['rd_intensity']:.4f}")
print(f"p値: {iv_model.pvalues['rd_intensity']:.4f}")
```

---

### 2.4 Propensity Score Matching (PSM)

**目的**: 処置群と対照群を類似した特性でマッチング

**使用ケース**:
- M&A研究（買収企業 vs. 非買収企業）
- イノベーション採用（採用企業 vs. 非採用企業）

**手順**:
1. Propensity Score推定（処置確率）
2. マッチング（1:1, 1:N, Kernel等）
3. マッチ後のバランスチェック
4. 処置効果推定

**実装**:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Step 1: Propensity Score推定
X_covariates = df[['firm_size', 'leverage', 'firm_age', 'industry_dummy']]
treatment = df['adopted_innovation']  # 1=採用, 0=非採用

# Logistic Regression
lr = LogisticRegression()
lr.fit(X_covariates, treatment)

# Propensity Score
df['propensity_score'] = lr.predict_proba(X_covariates)[:, 1]

# Step 2: 1:1 Nearest Neighbor Matching
treated = df[df['adopted_innovation'] == 1]
control = df[df['adopted_innovation'] == 0]

# KNNマッチング
nn = NearestNeighbors(n_neighbors=1, metric='euclidean')
nn.fit(control[['propensity_score']])

distances, indices = nn.kneighbors(treated[['propensity_score']])

# マッチされた対照群
matched_control_indices = control.index[indices.flatten()]
matched_control = control.loc[matched_control_indices]

# マッチ後データセット
df_matched = pd.concat([treated, matched_control])

print(f"処置群: {len(treated)}")
print(f"マッチされた対照群: {len(matched_control)}")

# Step 3: バランスチェック
from scipy.stats import ttest_ind

print("\n【バランスチェック】")
for var in ['firm_size', 'leverage', 'firm_age']:
    t_stat, p_val = ttest_ind(
        df_matched[df_matched['adopted_innovation']==1][var],
        df_matched[df_matched['adopted_innovation']==0][var]
    )
    print(f"{var}: t={t_stat:.2f}, p={p_val:.3f}")
    if p_val > 0.05:
        print(f"  ✓ バランス良好")
    else:
        print(f"  ✗ 不均衡あり")

# Step 4: 処置効果推定（ATT: Average Treatment effect on the Treated）
outcome_treated = df_matched[df_matched['adopted_innovation']==1]['roa'].mean()
outcome_control = df_matched[df_matched['adopted_innovation']==0]['roa'].mean()

att = outcome_treated - outcome_control

print(f"\n【処置効果】")
print(f"処置群平均ROA: {outcome_treated:.4f}")
print(f"対照群平均ROA: {outcome_control:.4f}")
print(f"ATT: {att:.4f}")

# t検定
t_stat, p_val = ttest_ind(
    df_matched[df_matched['adopted_innovation']==1]['roa'],
    df_matched[df_matched['adopted_innovation']==0]['roa']
)
print(f"t統計量: {t_stat:.2f}, p値: {p_val:.3f}")
```

---

### 2.5 Heckman Selection Model

**目的**: サンプル選択バイアスの補正

**使用ケース**:
- 輸出企業のみを分析（非輸出企業の選択バイアス）
- R&D実施企業のみを分析（非実施企業の選択バイアス）

**2段階**:
1. **Selection Equation**: サンプル選択を予測（Probit）
2. **Outcome Equation**: 選択後の結果を分析（OLS + IMR）

**実装**:

```python
from statsmodels.regression.linear_model import OLS
from statsmodels.discrete.discrete_model import Probit
from scipy.stats import norm

# Step 1: Selection Equation (Probit)
# 従属変数: rd_dummy (R&D実施=1, 非実施=0)

X_selection = df[['firm_size', 'leverage', 'industry_competition']]
X_selection = sm.add_constant(X_selection)

probit_model = Probit(df['rd_dummy'], X_selection).fit()

# Inverse Mills Ratio (IMR)計算
df['z'] = probit_model.predict(X_selection)
df['imr'] = norm.pdf(df['z']) / norm.cdf(df['z'])

# Step 2: Outcome Equation (OLS + IMR)
df_selected = df[df['rd_dummy'] == 1]  # R&D実施企業のみ

X_outcome = df_selected[['rd_intensity', 'firm_size', 'leverage', 'imr']]
X_outcome = sm.add_constant(X_outcome)

ols_model = OLS(df_selected['roa'], X_outcome).fit()

print(ols_model.summary())

# IMRの有意性チェック
print(f"\nIMR係数: {ols_model.params['imr']:.4f}")
print(f"p値: {ols_model.pvalues['imr']:.4f}")

if ols_model.pvalues['imr'] < 0.05:
    print("✓ 選択バイアス有意（Heckman補正必要）")
else:
    print("  選択バイアス非有意")
```

---

### 2.6 Difference-in-Differences (DiD)

**目的**: イベント・政策変更の因果効果推定

**使用ケース**:
- 新規制導入の効果
- M&A announcement効果
- 組織変革の効果

**基本モデル**:
```
Y_it = β₀ + β₁Treated_i + β₂Post_t + β₃(Treated × Post)_it + ε_it

β₃: DiD推定量（処置効果）
```

**実装**:

```python
import pandas as pd
import statsmodels.formula.api as smf

# データ準備
# treated: 処置群=1, 対照群=0
# post: イベント後=1, 前=0

# DiD回帰
did_model = smf.ols('''
roa ~ treated + post + treated:post + 
      firm_size + leverage + C(industry) + C(year)
''', data=df).fit(cov_type='cluster', cov_kwds={'groups': df['firm_id']})

print(did_model.summary())

# DiD効果
did_effect = did_model.params['treated:post']
print(f"\nDiD効果: {did_effect:.4f}")
print(f"p値: {did_model.pvalues['treated:post']:.4f}")

# 平行トレンド仮定チェック（イベント前）
df_pre = df[df['post'] == 0]

# 処置群と対照群のトレンド比較
treated_trend = df_pre[df_pre['treated']==1].groupby('year')['roa'].mean()
control_trend = df_pre[df_pre['treated']==0].groupby('year')['roa'].mean()

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(treated_trend.index, treated_trend.values, label='Treated', marker='o')
plt.plot(control_trend.index, control_trend.values, label='Control', marker='s')
plt.axvline(x=event_year, color='r', linestyle='--', label='Event')
plt.xlabel('Year')
plt.ylabel('ROA')
plt.title('Parallel Trends Check')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 3. 調整効果分析

### 3.1 基本概念

**調整効果（Moderation）**: Xの効果がZによって変化

```
Y = β₀ + β₁X + β₂Z + β₃(X × Z) + ε

β₃: 調整効果
```

**解釈**:
- β₃ > 0: ZがXの効果を強化
- β₃ < 0: ZがXの効果を弱化

---

### 3.2 実装

```python
import statsmodels.formula.api as smf
import numpy as np

# 変数の標準化（交互作用項の多重共線性軽減）
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df['rd_intensity_std'] = scaler.fit_transform(df[['rd_intensity']])
df['env_uncertainty_std'] = scaler.fit_transform(df[['env_uncertainty']])

# 交互作用項
df['rd_x_uncertainty'] = df['rd_intensity_std'] * df['env_uncertainty_std']

# 調整効果モデル
mod_model = smf.ols('''
roa ~ rd_intensity_std + env_uncertainty_std + rd_x_uncertainty +
      firm_size + leverage + firm_age + C(industry) + C(year)
''', data=df).fit(cov_type='cluster', cov_kwds={'groups': df['firm_id']})

print(mod_model.summary())

# 調整効果の解釈
beta_x = mod_model.params['rd_intensity_std']
beta_xz = mod_model.params['rd_x_uncertainty']

print(f"\n【調整効果】")
print(f"R&D主効果（β₁）: {beta_x:.4f}")
print(f"交互作用（β₃）: {beta_xz:.4f}, p={mod_model.pvalues['rd_x_uncertainty']:.3f}")

if mod_model.pvalues['rd_x_uncertainty'] < 0.05:
    if beta_xz > 0:
        print("✓ 環境不確実性がR&D効果を強化")
    else:
        print("✓ 環境不確実性がR&D効果を弱化")
```

---

### 3.3 Simple Slope分析

```python
import matplotlib.pyplot as plt

# 不確実性の高低（±1SD）
uncertainty_low = df['env_uncertainty_std'].mean() - df['env_uncertainty_std'].std()
uncertainty_high = df['env_uncertainty_std'].mean() + df['env_uncertainty_std'].std()

# R&Dの範囲
rd_range = np.linspace(df['rd_intensity_std'].min(), 
                       df['rd_intensity_std'].max(), 100)

# Simple Slopes
slope_low = beta_x + beta_xz * uncertainty_low
slope_high = beta_x + beta_xz * uncertainty_high

roa_low = mod_model.params['Intercept'] + slope_low * rd_range
roa_high = mod_model.params['Intercept'] + slope_high * rd_range

# プロット
plt.figure(figsize=(10, 6))
plt.plot(rd_range, roa_low, label=f'Low Uncertainty (-1SD)', linestyle='--')
plt.plot(rd_range, roa_high, label=f'High Uncertainty (+1SD)', linestyle='-')
plt.xlabel('R&D Intensity (Standardized)')
plt.ylabel('ROA')
plt.title('Moderation Effect: Environmental Uncertainty on R&D→ROA')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Simple Slope検定
from scipy.stats import t as t_dist

se_x = mod_model.bse['rd_intensity_std']
se_xz = mod_model.bse['rd_x_uncertainty']
cov_x_xz = mod_model.cov_params().loc['rd_intensity_std', 'rd_x_uncertainty']

# Low Uncertainty時のSE
se_low = np.sqrt(se_x**2 + (uncertainty_low**2) * se_xz**2 + 
                 2 * uncertainty_low * cov_x_xz)
t_low = slope_low / se_low
p_low = 2 * (1 - t_dist.cdf(abs(t_low), df=mod_model.df_resid))

# High Uncertainty時のSE
se_high = np.sqrt(se_x**2 + (uncertainty_high**2) * se_xz**2 + 
                  2 * uncertainty_high * cov_x_xz)
t_high = slope_high / se_high
p_high = 2 * (1 - t_dist.cdf(abs(t_high), df=mod_model.df_resid))

print(f"\n【Simple Slope検定】")
print(f"Low Uncertainty: Slope={slope_low:.4f}, t={t_low:.2f}, p={p_low:.3f}")
print(f"High Uncertainty: Slope={slope_high:.4f}, t={t_high:.2f}, p={p_high:.3f}")
```

---

## 4. 媒介効果分析

### 4.1 基本概念

**媒介効果（Mediation）**: XがMを通じてYに影響

```
X → M → Y

直接効果: X → Y (c')
間接効果: X → M → Y (a × b)
総効果: c = c' + ab
```

**Baron & Kenny 4ステップ**:
1. X → Y（総効果 c）
2. X → M（パス a）
3. M → Y（パス b）
4. X + M → Y（直接効果 c'）

---

### 4.2 実装

```python
import statsmodels.api as sm
import pandas as pd

# Step 1: X → Y（総効果）
X = sm.add_constant(df[['rd_intensity', 'firm_size', 'leverage']])
y = df['roa']

model_total = sm.OLS(y, X).fit()
c = model_total.params['rd_intensity']
print(f"Step 1（総効果 c）: {c:.4f}, p={model_total.pvalues['rd_intensity']:.3f}")

# Step 2: X → M（パス a）
M = df['organizational_learning']  # 媒介変数
model_a = sm.OLS(M, X).fit()
a = model_a.params['rd_intensity']
print(f"Step 2（パス a）: {a:.4f}, p={model_a.pvalues['rd_intensity']:.3f}")

# Step 3: M → Y（パス b）
X_with_M = sm.add_constant(df[['organizational_learning', 'firm_size', 'leverage']])
model_b = sm.OLS(y, X_with_M).fit()
b = model_b.params['organizational_learning']
print(f"Step 3（パス b）: {b:.4f}, p={model_b.pvalues['organizational_learning']:.3f}")

# Step 4: X + M → Y（直接効果 c'）
X_full = sm.add_constant(df[['rd_intensity', 'organizational_learning', 
                              'firm_size', 'leverage']])
model_direct = sm.OLS(y, X_full).fit()
c_prime = model_direct.params['rd_intensity']
print(f"Step 4（直接効果 c'）: {c_prime:.4f}, p={model_direct.pvalues['rd_intensity']:.3f}")

# 間接効果
indirect_effect = a * b
print(f"\n間接効果（a × b）: {indirect_effect:.4f}")
print(f"媒介割合: {(indirect_effect / c) * 100:.1f}%")

# 媒介タイプ判定
if model_direct.pvalues['rd_intensity'] > 0.05 and indirect_effect != 0:
    print("→ 完全媒介（Full Mediation）")
elif model_direct.pvalues['rd_intensity'] < 0.05 and indirect_effect != 0:
    print("→ 部分媒介（Partial Mediation）")
```

---

### 4.3 Sobel Test（間接効果の有意性検定）

```python
import numpy as np
from scipy.stats import norm

# Sobel Test
se_a = model_a.bse['rd_intensity']
se_b = model_b.bse['organizational_learning']

# Sobel統計量
sobel_stat = indirect_effect / np.sqrt(b**2 * se_a**2 + a**2 * se_b**2)
p_sobel = 2 * (1 - norm.cdf(abs(sobel_stat)))

print(f"\n【Sobel Test】")
print(f"統計量: {sobel_stat:.2f}")
print(f"p値: {p_sobel:.4f}")

if p_sobel < 0.05:
    print("✓ 間接効果有意")
```

---

### 4.4 Bootstrap信頼区間（推奨）

```python
from scipy.stats import bootstrap

def indirect_effect_func(data):
    """Bootstrap用の関数"""
    # X → M
    X_boot = sm.add_constant(data[:, [0, 2, 3]])  # rd, size, lev
    M_boot = data[:, 1]  # org_learning
    model_a_boot = sm.OLS(M_boot, X_boot).fit()
    a_boot = model_a_boot.params[1]  # rd係数
    
    # M → Y
    X_M_boot = sm.add_constant(data[:, [1, 2, 3]])  # org_learning, size, lev
    y_boot = data[:, 4]  # roa
    model_b_boot = sm.OLS(y_boot, X_M_boot).fit()
    b_boot = model_b_boot.params[1]  # org_learning係数
    
    return a_boot * b_boot

# データ準備
boot_data = df[['rd_intensity', 'organizational_learning', 
                'firm_size', 'leverage', 'roa']].dropna().values

# Bootstrap (n=5000)
np.random.seed(42)
n_bootstrap = 5000
indirect_effects = []

for _ in range(n_bootstrap):
    sample_indices = np.random.choice(len(boot_data), size=len(boot_data), replace=True)
    sample = boot_data[sample_indices]
    indirect_effects.append(indirect_effect_func(sample))

# 95%信頼区間
ci_lower = np.percentile(indirect_effects, 2.5)
ci_upper = np.percentile(indirect_effects, 97.5)

print(f"\n【Bootstrap信頼区間】")
print(f"間接効果: {indirect_effect:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

if ci_lower > 0 or ci_upper < 0:
    print("✓ 間接効果有意（CIが0を含まない）")
```

---

## 5. 多階層モデル（MLM）

### 5.1 基本概念

**階層構造**: 個体（Level 1）がグループ（Level 2）にnested

```
例:
- 従業員（L1） nested in 企業（L2）
- 企業（L1） nested in 業界（L2）
- 企業-年（L1） nested in 企業（L2）
```

**基本モデル（Random Intercept）**:
```
Level 1: Y_ij = β₀j + β₁X_ij + ε_ij
Level 2: β₀j = γ₀₀ + u₀j

統合形:
Y_ij = γ₀₀ + β₁X_ij + u₀j + ε_ij
```

---

### 5.2 実装

```python
import statsmodels.formula.api as smf

# Random Intercept Model
# 企業（Level 2）nested in 業界（Level 1）

mlm_model = smf.mixedlm(
    formula='roa ~ rd_intensity + firm_size + leverage',
    data=df,
    groups=df['industry']  # Level 2グループ
).fit()

print(mlm_model.summary())

# Random Effects
print(f"\n【Random Effects】")
print(f"業界分散（τ₀₀）: {mlm_model.cov_re.iloc[0,0]:.4f}")
print(f"残差分散（σ²）: {mlm_model.scale:.4f}")

# ICC (Intraclass Correlation)
icc = mlm_model.cov_re.iloc[0,0] / (mlm_model.cov_re.iloc[0,0] + mlm_model.scale)
print(f"ICC: {icc:.3f}")
print(f"  → 業界が説明する分散: {icc*100:.1f}%")
```

---

## 6. 生存分析

### 6.1 Cox Hazard Model

**使用ケース**:
- 企業存続分析
- M&A後の統合期間
- 提携継続期間

**モデル**:
```
h(t|X) = h₀(t) × exp(β₁X₁ + β₂X₂ + ...)

h(t|X): 時点tでのハザード率
h₀(t): ベースラインハザード
```

---

### 6.2 実装

```python
from lifelines import CoxPHFitter
import pandas as pd

# データ準備
# duration: 存続期間（年数）
# event: 1=廃業, 0=打ち切り（観測終了時点で存続）

df_survival = df[['duration', 'event', 'rd_intensity', 
                   'firm_size', 'leverage', 'firm_age']].dropna()

# Cox PH Model
cph = CoxPHFitter()
cph.fit(df_survival, duration_col='duration', event_col='event')

print(cph.summary)

# Hazard Ratio解釈
print(f"\n【Hazard Ratio】")
for var in ['rd_intensity', 'firm_size']:
    hr = np.exp(cph.params_[var])
    print(f"{var}: HR={hr:.3f}")
    if hr > 1:
        print(f"  → 1単位増加で廃業リスク{(hr-1)*100:.1f}%増")
    else:
        print(f"  → 1単位増加で廃業リスク{(1-hr)*100:.1f}%減")

# Proportional Hazards仮定チェック
from lifelines.statistics import proportional_hazard_test

ph_test = proportional_hazard_test(cph, df_survival, time_transform='rank')
print(f"\nPH仮定検定: p={ph_test.summary['p'].min():.3f}")
if ph_test.summary['p'].min() > 0.05:
    print("✓ PH仮定OK")
```

---

## 7. Robustness Checks

### 7.1 必須チェック（最低3つ）

**1. 代替従属変数**
```python
# ROA → Tobin's Q
model_rob1 = PanelOLS.from_formula('''
tobin_q ~ rd_intensity + controls + EntityEffects + TimeEffects
''', data=df_panel).fit(cov_type='clustered', cluster_entity=True)
```

**2. サブサンプル分析**
```python
# ハイテク業界のみ
df_hightech = df[df['industry'].isin([357, 367, 384])]
model_rob2 = PanelOLS.from_formula('''
roa ~ rd_intensity + controls + EntityEffects + TimeEffects
''', data=df_hightech.set_index(['firm_id', 'year'])).fit(cov_type='clustered', cluster_entity=True)
```

**3. 異なるラグ構造**
```python
# t+1 → t+2
df['roa_lead2'] = df.groupby('firm_id')['roa'].shift(-2)
model_rob3 = PanelOLS.from_formula('''
roa_lead2 ~ rd_intensity + controls + EntityEffects + TimeEffects
''', data=df_panel).fit(cov_type='clustered', cluster_entity=True)
```

---

### 7.2 Robustness結果の報告

```python
# 結果を表形式でまとめ
robustness_results = pd.DataFrame({
    'Model': ['Main', 'Alt DV (Tobin Q)', 'Hightech Only', 'Lag t+2'],
    'Coefficient': [
        model_main.params['rd_intensity'],
        model_rob1.params['rd_intensity'],
        model_rob2.params['rd_intensity'],
        model_rob3.params['rd_intensity']
    ],
    'Std Error': [
        model_main.std_errors['rd_intensity'],
        model_rob1.std_errors['rd_intensity'],
        model_rob2.std_errors['rd_intensity'],
        model_rob3.std_errors['rd_intensity']
    ],
    'P-value': [
        model_main.pvalues['rd_intensity'],
        model_rob1.pvalues['rd_intensity'],
        model_rob2.pvalues['rd_intensity'],
        model_rob3.pvalues['rd_intensity']
    ],
    'N': [
        model_main.nobs,
        model_rob1.nobs,
        model_rob2.nobs,
        model_rob3.nobs
    ]
})

print("\n【Robustness Checks】")
print(robustness_results.to_string(index=False))

# すべてのモデルで有意か確認
all_significant = (robustness_results['P-value'] < 0.05).all()
if all_significant:
    print("\n✓ すべてのRobustness checksで結果頑健")
```

---

## 8. 診断テスト

### 8.1 多重共線性（VIF）

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF計算
X = df[['rd_intensity', 'firm_size', 'leverage', 'firm_age', 'capital_intensity']]
X = X.dropna()

vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print("【多重共線性チェック】")
print(vif_data)

# 判定
max_vif = vif_data["VIF"].max()
if max_vif > 10:
    print(f"\n✗ 警告: 最大VIF={max_vif:.1f} > 10（多重共線性あり）")
elif max_vif > 5:
    print(f"\n⚠ 注意: 最大VIF={max_vif:.1f} > 5（やや高い）")
else:
    print(f"\n✓ 多重共線性問題なし（最大VIF={max_vif:.1f}）")
```

---

### 8.2 異分散性

```python
from statsmodels.stats.diagnostic import het_white

# OLSモデルで実施
model = smf.ols('roa ~ rd_intensity + firm_size + leverage', data=df).fit()

# White test
lm_stat, lm_pval, f_stat, f_pval = het_white(model.resid, model.model.exog)

print(f"【異分散性チェック】")
print(f"White test: LM statistic={lm_stat:.2f}, p={lm_pval:.4f}")

if lm_pval < 0.05:
    print("✗ 異分散性あり → Robust標準誤差使用推奨")
else:
    print("✓ 等分散性OK")
```

---

### 8.3 自己相関

```python
from statsmodels.stats.stattools import durbin_watson

# Durbin-Watson test
dw_stat = durbin_watson(model.resid)

print(f"【自己相関チェック】")
print(f"Durbin-Watson統計量: {dw_stat:.2f}")

if 1.5 < dw_stat < 2.5:
    print("✓ 自己相関問題なし")
else:
    print("⚠ 自己相関の可能性 → クラスタリング標準誤差推奨")
```

---

## 📊 Quick Reference

### 手法選択フローチャート

```
データ構造:
├─ パネルデータ？
│  Yes → Fixed Effects（推奨）
│  No → OLS
│
├─ 内生性の懸念？
│  Yes → IV, PSM, Heckman, DiD
│  No → FE/OLS
│
├─ 調整効果？
│  Yes → 交互作用項 + Simple Slope
│
├─ 媒介効果？
│  Yes → Baron & Kenny + Bootstrap CI
│
└─ 階層構造？
   Yes → Multilevel Model
```

---

### トップジャーナル基準

| ジャーナル | 必須手法 | Robustness | 内生性対策 |
|-----------|---------|-----------|-----------|
| SMJ | FE, Cluster SE | 3つ以上 | 必須 |
| AMJ | FE, Power分析 | 3つ以上 | 必須 |
| OS | FE, 新規手法 | 3つ以上 | 必須 |

---

### Pythonパッケージ

```bash
# 必須
pip install pandas numpy scipy statsmodels linearmodels

# 生存分析
pip install lifelines

# 機械学習（PSM用）
pip install scikit-learn

# 可視化
pip install matplotlib seaborn
```

---

## 参考文献

### 方法論

- Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data*. MIT Press.
- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
- Hayes, A. F. (2017). *Introduction to Mediation, Moderation, and Conditional Process Analysis*. Guilford Press.

---

## 次のステップ

### 基本ワークフロー
→ [`1-core-workflow` skill](../1-core-workflow/SKILL.md) Phase 7

### 高度因果推論
→ [`6-causal-ml` skill](../6-causal-ml/SKILL.md)

### テキスト変数の統合
→ [`4-text-analysis` skill](../4-text-analysis/SKILL.md)

---

**このスキルで、トップジャーナル水準の統計分析を実装できます。**  
**内生性対策からRobustness checksまで、完全な分析フローを実行しましょう。**

---

**最終更新**: 2025-11-01  
**バージョン**: 4.0.0  
**次回メンテナンス予定**: 2025-12-01
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
