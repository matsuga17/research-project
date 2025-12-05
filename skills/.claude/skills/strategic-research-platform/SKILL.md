---
name: strategic-research-platform
description: |
  戦略経営論・組織論の実証研究のための包括的プラットフォーム。以下の機能を統合：
  (1) 理論的フレームワーク構築（RBV、Dynamic Capabilities、TCE、制度理論等）
  (2) 実証研究デザイン（パネルデータ、イベントスタディ、生存分析等）
  (3) 統計分析実行（記述統計、回帰分析、因果推論）
  (4) データソース探索・収集戦略
  (5) Publication-grade品質保証（ロバストネスチェック、診断テスト）
  (6) トップジャーナル投稿準備（SMJ、AMJ、OS、ASQ対応）
  トリガー：「戦略研究」「組織論研究」「実証研究」「定量分析」「パネルデータ」「回帰分析」「因果推論」「DID」「RDD」
allowed-tools: Bash,Read,Write
---

# Strategic Research Platform - 戦略・組織論実証研究プラットフォーム

## 概要

事業戦略論（Business Strategy）と組織戦略論（Organizational Strategy）分野における定量的実証研究のための統合システム。研究デザインから統計分析の実行、論文執筆まで、研究プロセス全体を体系的に管理し、トップジャーナル掲載基準を満たす研究の実現を支援します。

**統合元スキル**：
- strategic-research-suite
- strategic-management-research-hub
- strategic-organizational-research-hub
- strategic-organizational-empirical
- empirical-research-designer
- statistical-analysis-suite（v2.0.0で統合）

## When to Use This Skill

以下の研究テーマ・タスクに取り組む際に使用：

### 研究テーマ
- 競争戦略研究（持続的競争優位、差別化、プラットフォーム戦略）
- 組織能力・資源ベース研究（Dynamic Capabilities、組織学習）
- 組織デザイン・構造研究
- 制度理論・環境適応研究
- M&A・戦略的提携

### 統計分析タスク
- 記述統計・探索的データ分析
- 回帰分析（OLS、ロジスティック、パネル）
- 因果推論（DID、RDD、IV、PSM）
- 仮説検定・統計的有意性の評価
- 分析結果の解釈・報告

**トリガーキーワード**：
- 「戦略研究」「組織論研究」「実証研究」
- 「統計分析」「回帰分析」「パネルデータ」
- 「因果推論」「DID」「差分の差分」「RDD」「IV」「PSM」
- 「仮説検定」「ロバストネスチェック」

---

# Part 1: 理論的フレームワーク

## 1.1 主要理論

### Resource-Based View (RBV) & Dynamic Capabilities

```
適用研究：
- 企業固有資源と競争優位
- 能力の異質性とパフォーマンス差
- イノベーション能力の測定

必要データ：
- R&D支出、特許データ
- 無形資産（ブランド価値、組織資本）
- 従業員スキル指標

代表的変数：
- R&D intensity = R&D支出 / 売上高
- Patent stock = Σ 特許件数 × 減価償却率
- Human capital intensity = 従業員給与総額 / 従業員数
- Absorptive capacity = R&D intensity × 外部連携数
```

### Transaction Cost Economics (TCE)

```
適用研究：
- Make-or-buy決定
- 垂直統合 vs アウトソーシング
- ガバナンス構造選択

代表的変数：
- Vertical integration = 付加価値 / 売上高
- Asset specificity = 専用設備投資 / 総固定資産
- Environmental uncertainty = 売上変動係数
```

### Institutional Theory

```
適用研究：
- 制度環境と組織行動
- 正当性と生存
- 国際比較研究

代表的変数：
- Rule of law index (World Bank)
- Cultural distance = Σ√[(Hofstede次元差)²]
- Certification adoption rate
```

### Competitive Strategy (Porter Framework)

```
適用研究：
- 産業構造とポジショニング
- Five Forces分析の定量化
- 戦略グループ分析

代表的変数：
- HHI (Herfindahl Index) = Σ(市場シェア²)
- Entry barrier = 固定資産 / 総資産
- Product differentiation = 広告費 / 売上高
```

## 1.2 変数概念化マトリックス

| 変数 | 理論的定義 | 操作的定義 | データソース | 期待符号 |
|------|------------|------------|--------------|----------|
| ROA | 総資産収益率 | 純利益/総資産 | Compustat | DV |
| R&D Intensity | イノベーション投資 | R&D支出/売上高 | Compustat | + |
| Firm Age | 組織慣性 | 設立年からの経過年数 | Compustat | +/- |
| Diversification | 事業多様性 | Entropy index | Segments | +/- |
| Env. Dynamism | 環境不確実性 | 売上変動係数（5年） | Compustat | Mod |

---

# Part 2: 研究デザイン

## 2.1 研究デザインタイプ

### パネルデータ研究
```
特徴：同一企業を複数時点で観測
利点：
- 観察されない異質性の制御（固定効果）
- 因果推論の強化
- 動的関係の分析

標準的設定：
- 企業数：100社以上
- 期間：5年以上
- 観測数：500以上

分析手法：
- 固定効果モデル
- ランダム効果モデル
- 差分の差分法（DID）
- システムGMM（動的パネル）
```

### イベントスタディ
```
適用：M&A発表、CEO交代、規制変更
分析窓：
- 短期：[-5, +5]日
- 長期：[-12, +12]月

手順：
1. イベント日の特定
2. 期待リターンの推定（市場モデル）
3. 異常リターン（AR）の計算
4. 累積異常リターン（CAR）の計算
5. 統計的有意性の検定
```

### 生存分析
```
適用：企業存続、CEO在任期間、製品寿命
手法：
- Kaplan-Meier推定
- Cox比例ハザードモデル
- パラメトリックモデル（Weibull、Exponential）
```

## 2.2 サンプル設計

### 企業選定基準
```
1. 産業範囲
   - 単一産業：深い分析、外的妥当性制限
   - 複数産業：一般化可能、産業固定効果必要

2. 地理的範囲
   - 単一国：制度的均質性
   - 複数国：制度比較可能、国固定効果必要

3. 時間範囲
   - 最低5年（パネルデータ）
   - 構造変化を考慮（金融危機、COVID等）

4. データ完全性
   - 主要変数の欠損率 < 20%
   - 生存バイアスへの対処
```

### 統計的検出力分析
```
必要サンプルサイズの決定：
- 効果量（Cohen's d）：0.2（小）、0.5（中）、0.8（大）
- 有意水準（α）：0.05
- 検出力（1-β）：0.80以上

目安：
- 回帰分析：1変数あたり10-15観測
- パネルデータ：N×T ≥ 500
- イベントスタディ：50-100イベント以上
```

---

# Part 3: 記述統計・探索的データ分析

## 3.1 基本統計量

### Python実装

```python
import pandas as pd
import numpy as np
from scipy import stats

def descriptive_statistics(df, variables=None):
    """
    包括的な記述統計を計算
    """
    if variables is None:
        variables = df.select_dtypes(include=[np.number]).columns.tolist()

    results = []

    for var in variables:
        data = df[var].dropna()

        stats_dict = {
            'Variable': var,
            'N': len(data),
            'Mean': data.mean(),
            'SD': data.std(),
            'Min': data.min(),
            'P25': data.quantile(0.25),
            'Median': data.median(),
            'P75': data.quantile(0.75),
            'Max': data.max(),
            'Skewness': stats.skew(data),
            'Kurtosis': stats.kurtosis(data),
            'Missing': df[var].isna().sum()
        }
        results.append(stats_dict)

    return pd.DataFrame(results)
```

### Stata実装

```stata
* 記述統計
summarize ROA Size Leverage RD_Intensity, detail

* 相関行列
correlate ROA Size Leverage RD_Intensity

* グループ別統計
tabstat ROA Size Leverage, by(Industry) stats(mean sd n)
```

### R実装

```r
library(dplyr)
library(psych)

# 記述統計
descriptive_stats <- df %>%
  select(ROA, Size, Leverage, RD_Intensity) %>%
  describe() %>%
  select(n, mean, sd, min, max, skew, kurtosis)

# 相関行列
cor_matrix <- cor(df[, c("ROA", "Size", "Leverage", "RD_Intensity")],
                  use = "pairwise.complete.obs")
```

## 3.2 相関分析

```python
def correlation_analysis(df, variables, method='pearson'):
    """
    相関分析（有意性検定付き）
    """
    n_vars = len(variables)
    corr_matrix = np.zeros((n_vars, n_vars))
    pval_matrix = np.zeros((n_vars, n_vars))

    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            data1 = df[var1].dropna()
            data2 = df[var2].dropna()
            common_idx = data1.index.intersection(data2.index)

            if method == 'pearson':
                corr, pval = stats.pearsonr(
                    df.loc[common_idx, var1],
                    df.loc[common_idx, var2]
                )
            else:
                corr, pval = stats.spearmanr(
                    df.loc[common_idx, var1],
                    df.loc[common_idx, var2]
                )

            corr_matrix[i, j] = corr
            pval_matrix[i, j] = pval

    return pd.DataFrame(corr_matrix, index=variables, columns=variables)

def format_correlation_table(corr_df, pval_df):
    """
    学術論文用の相関表フォーマット
    * p < .05, ** p < .01, *** p < .001
    """
    formatted = corr_df.copy()

    for i in range(len(corr_df)):
        for j in range(len(corr_df.columns)):
            val = corr_df.iloc[i, j]
            pval = pval_df.iloc[i, j]

            if i == j:
                formatted.iloc[i, j] = "1.00"
            elif i > j:
                stars = ""
                if pval < 0.001:
                    stars = "***"
                elif pval < 0.01:
                    stars = "**"
                elif pval < 0.05:
                    stars = "*"
                formatted.iloc[i, j] = f"{val:.2f}{stars}"
            else:
                formatted.iloc[i, j] = ""

    return formatted
```

## 3.3 分布の確認・正規性検定

```python
import matplotlib.pyplot as plt
import seaborn as sns

def check_distributions(df, variables, output_path=None):
    """
    変数の分布を可視化
    """
    n_vars = len(variables)
    fig, axes = plt.subplots(n_vars, 2, figsize=(12, 4*n_vars))

    for i, var in enumerate(variables):
        data = df[var].dropna()

        # ヒストグラム
        axes[i, 0].hist(data, bins=30, edgecolor='black', alpha=0.7)
        axes[i, 0].set_title(f'{var} - Histogram')
        axes[i, 0].axvline(data.mean(), color='red', linestyle='--', label='Mean')
        axes[i, 0].legend()

        # Q-Qプロット
        stats.probplot(data, dist="norm", plot=axes[i, 1])
        axes[i, 1].set_title(f'{var} - Q-Q Plot')

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
    return fig

def normality_tests(df, variables):
    """正規性検定（Shapiro-Wilk、Kolmogorov-Smirnov）"""
    results = []
    for var in variables:
        data = df[var].dropna()

        if len(data) < 5000:
            sw_stat, sw_pval = stats.shapiro(data)
        else:
            sw_stat, sw_pval = np.nan, np.nan

        ks_stat, ks_pval = stats.kstest(data, 'norm',
                                        args=(data.mean(), data.std()))

        results.append({
            'Variable': var,
            'Shapiro-Wilk': sw_stat,
            'SW p-value': sw_pval,
            'K-S': ks_stat,
            'KS p-value': ks_pval
        })

    return pd.DataFrame(results)
```

---

# Part 4: 回帰分析

## 4.1 OLS回帰

### Python (statsmodels)

```python
import statsmodels.api as sm
import statsmodels.formula.api as smf

def ols_regression(df, formula, robust=True):
    """
    OLS回帰分析
    """
    model = smf.ols(formula, data=df).fit(
        cov_type='HC3' if robust else 'nonrobust'
    )
    return model

def format_regression_table(models, model_names=None):
    """
    複数モデルの回帰結果を学術論文形式でフォーマット
    """
    from statsmodels.iolib.summary2 import summary_col

    if model_names is None:
        model_names = [f"Model {i+1}" for i in range(len(models))]

    result = summary_col(
        models,
        model_names=model_names,
        stars=True,
        float_format='%.3f',
        info_dict={
            'N': lambda x: f"{int(x.nobs)}",
            'R-squared': lambda x: f"{x.rsquared:.3f}",
            'Adj. R-squared': lambda x: f"{x.rsquared_adj:.3f}",
            'F-statistic': lambda x: f"{x.fvalue:.2f}"
        }
    )
    return result

# 使用例
model1 = ols_regression(df, "ROA ~ Size + Leverage")
model2 = ols_regression(df, "ROA ~ Size + Leverage + RD_Intensity")
model3 = ols_regression(df, "ROA ~ Size + Leverage + RD_Intensity + Size:RD_Intensity")

table = format_regression_table([model1, model2, model3],
                                ["Base", "Main", "Interaction"])
```

### Stata

```stata
* 基本OLS
regress ROA Size Leverage, robust

* 交互作用項
regress ROA c.Size##c.RD_Intensity Leverage, robust

* クラスター標準誤差
regress ROA Size Leverage RD_Intensity, cluster(Firm_ID)
```

### R

```r
library(lmtest)
library(sandwich)

# OLS with robust SE
model <- lm(ROA ~ Size + Leverage + RD_Intensity, data = df)
coeftest(model, vcov = vcovHC(model, type = "HC3"))

# 結果テーブル
library(stargazer)
stargazer(model1, model2, model3,
          type = "text",
          se = list(sqrt(diag(vcovHC(model1))),
                   sqrt(diag(vcovHC(model2))),
                   sqrt(diag(vcovHC(model3)))))
```

## 4.2 パネルデータ分析

### 固定効果・ランダム効果モデル

```python
from linearmodels.panel import PanelOLS, RandomEffects, compare

def panel_regression(df, dependent, independents, entity_effects=True,
                    time_effects=False, cluster_entity=True):
    """
    パネルデータ回帰分析
    """
    if not isinstance(df.index, pd.MultiIndex):
        df = df.set_index(['Firm_ID', 'Year'])

    y = df[dependent]
    X = df[independents]

    fe_model = PanelOLS(
        y, X,
        entity_effects=entity_effects,
        time_effects=time_effects,
        drop_absorbed=True
    ).fit(cov_type='clustered', cluster_entity=cluster_entity)

    return fe_model

def hausman_test(df, dependent, independents):
    """
    Hausman検定（固定効果 vs ランダム効果）
    """
    if not isinstance(df.index, pd.MultiIndex):
        df = df.set_index(['Firm_ID', 'Year'])

    y = df[dependent]
    X = sm.add_constant(df[independents])

    fe = PanelOLS(y, X, entity_effects=True).fit()
    re = RandomEffects(y, X).fit()

    b_fe = fe.params
    b_re = re.params
    var_diff = fe.cov - re.cov

    chi2 = (b_fe - b_re).T @ np.linalg.inv(var_diff) @ (b_fe - b_re)
    df_test = len(b_fe)
    p_value = 1 - stats.chi2.cdf(chi2, df_test)

    return {
        'chi2': chi2,
        'df': df_test,
        'p_value': p_value,
        'conclusion': 'Fixed Effects' if p_value < 0.05 else 'Random Effects'
    }
```

### Stata パネルデータ

```stata
* パネル設定
xtset Firm_ID Year

* 固定効果モデル
xtreg ROA Size Leverage RD_Intensity, fe cluster(Firm_ID)

* ランダム効果モデル
xtreg ROA Size Leverage RD_Intensity, re cluster(Firm_ID)

* Hausman検定
hausman fe re

* 時間固定効果を追加
xtreg ROA Size Leverage RD_Intensity i.Year, fe cluster(Firm_ID)
```

## 4.3 ロジスティック回帰・順序回帰

```python
from statsmodels.discrete.discrete_model import Logit, Probit
from statsmodels.miscmodels.ordinal_model import OrderedModel

def logistic_regression(df, formula):
    """ロジスティック回帰"""
    model = smf.logit(formula, data=df).fit()

    odds_ratios = np.exp(model.params)
    conf_int = np.exp(model.conf_int())

    results = pd.DataFrame({
        'Coefficient': model.params,
        'Std. Error': model.bse,
        'z': model.tvalues,
        'P>|z|': model.pvalues,
        'Odds Ratio': odds_ratios,
        'OR 95% CI Lower': conf_int[0],
        'OR 95% CI Upper': conf_int[1]
    })

    return model, results

def ordered_logit(df, dependent, independents):
    """順序ロジット回帰（5段階評価など）"""
    y = df[dependent]
    X = df[independents]
    model = OrderedModel(y, X, distr='logit').fit(method='bfgs')
    return model
```

---

# Part 5: 因果推論手法

## 5.1 差分の差分法（DID）

```python
def difference_in_differences(df, outcome, treatment, post, entity_fe=True,
                             time_fe=True, controls=None):
    """
    差分の差分分析
    """
    df['DID'] = df[treatment] * df[post]

    formula_parts = [outcome, '~', 'DID']

    if not entity_fe:
        formula_parts.append(f'+ {treatment}')
    if not time_fe:
        formula_parts.append(f'+ {post}')
    if controls:
        formula_parts.append('+ ' + ' + '.join(controls))

    formula = ' '.join(formula_parts)

    if entity_fe or time_fe:
        if not isinstance(df.index, pd.MultiIndex):
            df = df.set_index(['Firm_ID', 'Year'])

        y = df[outcome]
        X = df[['DID'] + (controls if controls else [])]

        model = PanelOLS(y, X,
                        entity_effects=entity_fe,
                        time_effects=time_fe).fit(
                            cov_type='clustered', cluster_entity=True
                        )
    else:
        model = smf.ols(formula, data=df).fit(cov_type='HC3')

    return model

def parallel_trends_test(df, outcome, treatment, time_var, pre_periods):
    """平行トレンド検定"""
    results = []

    for t in pre_periods:
        df[f'pre_{t}'] = (df[time_var] == t).astype(int)
        df[f'pre_{t}_treat'] = df[f'pre_{t}'] * df[treatment]

    interactions = [f'pre_{t}_treat' for t in pre_periods]
    formula = f"{outcome} ~ " + " + ".join(interactions)
    model = smf.ols(formula, data=df).fit()

    for var in interactions:
        results.append({
            'Period': var,
            'Coefficient': model.params[var],
            'p-value': model.pvalues[var],
            'Significant': model.pvalues[var] < 0.05
        })

    return pd.DataFrame(results)
```

### Stata DID

```stata
* 基本DID
gen DID = Treatment * Post
regress Y DID Treatment Post, cluster(Firm_ID)

* 固定効果DID
xtreg Y DID i.Year, fe cluster(Firm_ID)

* イベントスタディ形式
gen time_to_treat = Year - Treatment_Year

forvalues t = -5/5 {
    if `t' != -1 {
        gen lead_lag_`=cond(`t'<0, "m", "")'`=abs(`t')' = (time_to_treat == `t') * Treatment
    }
}

xtreg Y lead_lag_* i.Year, fe cluster(Firm_ID)
```

## 5.2 回帰不連続デザイン（RDD）

```python
def regression_discontinuity(df, outcome, running_var, cutoff,
                            bandwidth=None, kernel='triangular'):
    """
    回帰不連続デザイン
    """
    from rdrobust import rdrobust

    df['D'] = (df[running_var] >= cutoff).astype(int)
    df['X_centered'] = df[running_var] - cutoff

    result = rdrobust(
        df[outcome],
        df[running_var],
        c=cutoff,
        kernel=kernel,
        bwselect='mserd' if bandwidth is None else None,
        h=bandwidth
    )

    return result

def rdd_plot(df, outcome, running_var, cutoff, n_bins=20):
    """RDDの可視化"""
    fig, ax = plt.subplots(figsize=(10, 6))

    df['bin'] = pd.cut(df[running_var], bins=n_bins)
    binned = df.groupby('bin')[outcome].mean().reset_index()
    binned['bin_mid'] = binned['bin'].apply(lambda x: x.mid)

    below = binned[binned['bin_mid'] < cutoff]
    above = binned[binned['bin_mid'] >= cutoff]

    ax.scatter(below['bin_mid'], below[outcome], color='blue', label='Below cutoff')
    ax.scatter(above['bin_mid'], above[outcome], color='red', label='Above cutoff')

    for data, color in [(below, 'blue'), (above, 'red')]:
        z = np.polyfit(data['bin_mid'], data[outcome], 1)
        p = np.poly1d(z)
        ax.plot(data['bin_mid'], p(data['bin_mid']), color=color, linestyle='--')

    ax.axvline(x=cutoff, color='black', linestyle='-', label='Cutoff')
    ax.legend()

    return fig
```

## 5.3 操作変数法（IV）

```python
from linearmodels.iv import IV2SLS

def instrumental_variables(df, dependent, endogenous, instruments, exogenous):
    """
    2段階最小二乗法（2SLS）
    """
    formula = f"{dependent} ~ 1 + {' + '.join(exogenous)} + [{endogenous} ~ {' + '.join(instruments)}]"

    model = IV2SLS.from_formula(formula, data=df).fit(
        cov_type='robust'
    )

    return model

def weak_instrument_test(first_stage_model):
    """
    弱操作変数検定（F統計量 > 10 が目安）
    """
    return {
        'F-statistic': first_stage_model.fvalue,
        'p-value': first_stage_model.f_pvalue,
        'Weak Instrument': first_stage_model.fvalue < 10
    }

def overidentification_test(iv_model):
    """過剰識別検定（Sargan-Hansen）"""
    return {
        'J-statistic': iv_model.j_stat.stat,
        'p-value': iv_model.j_stat.pval,
        'Valid Instruments': iv_model.j_stat.pval > 0.05
    }
```

### Stata IV

```stata
* 2SLS
ivregress 2sls Y X1 X2 (Endogenous = Z1 Z2), robust

* 第1段階
ivregress 2sls Y X1 X2 (Endogenous = Z1 Z2), robust first

* 弱操作変数検定
estat firststage

* 過剰識別検定
estat overid
```

## 5.4 傾向スコアマッチング（PSM）

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

def propensity_score_matching(df, treatment, covariates, outcome,
                              n_neighbors=1, caliper=0.1):
    """傾向スコアマッチング"""
    X = df[covariates]
    y = df[treatment]

    ps_model = LogisticRegression(max_iter=1000)
    ps_model.fit(X, y)
    df['propensity_score'] = ps_model.predict_proba(X)[:, 1]

    treated = df[df[treatment] == 1]
    control = df[df[treatment] == 0]

    nn = NearestNeighbors(n_neighbors=n_neighbors)
    nn.fit(control[['propensity_score']])

    distances, indices = nn.kneighbors(treated[['propensity_score']])

    matched_pairs = []
    for i, (dist, idx) in enumerate(zip(distances, indices)):
        if dist[0] <= caliper:
            matched_pairs.append({
                'treated_idx': treated.index[i],
                'control_idx': control.index[idx[0]],
                'distance': dist[0]
            })

    treated_matched = df.loc[[p['treated_idx'] for p in matched_pairs]]
    control_matched = df.loc[[p['control_idx'] for p in matched_pairs]]

    att = treated_matched[outcome].mean() - control_matched[outcome].mean()

    return {
        'ATT': att,
        'n_matched': len(matched_pairs),
        'matched_treated': treated_matched,
        'matched_control': control_matched
    }

def balance_check(treated, control, covariates):
    """マッチング後のバランスチェック（標準化差 < 0.1 が目安）"""
    results = []

    for var in covariates:
        mean_t = treated[var].mean()
        mean_c = control[var].mean()
        sd_pooled = np.sqrt((treated[var].var() + control[var].var()) / 2)

        std_diff = (mean_t - mean_c) / sd_pooled

        results.append({
            'Variable': var,
            'Mean (Treated)': mean_t,
            'Mean (Control)': mean_c,
            'Std. Diff': std_diff,
            'Balanced': abs(std_diff) < 0.1
        })

    return pd.DataFrame(results)
```

---

# Part 6: ロバストネスチェック・診断テスト

## 6.1 標準的ロバストネス検定

```python
def robustness_checks(df, base_model_formula, checks):
    """
    ロバストネスチェックの実行

    checks = {
        'alternative_dv': ['ROE', 'Tobin_Q'],
        'subsamples': [('Large', df['Size'] > df['Size'].median()),
                      ('Small', df['Size'] <= df['Size'].median())],
        'time_periods': [('Pre-crisis', df['Year'] < 2008),
                        ('Post-crisis', df['Year'] >= 2008)]
    }
    """
    results = {'Base Model': smf.ols(base_model_formula, data=df).fit()}

    if 'alternative_dv' in checks:
        for alt_dv in checks['alternative_dv']:
            formula = base_model_formula.replace(
                base_model_formula.split('~')[0].strip(),
                alt_dv
            )
            results[f'Alt DV: {alt_dv}'] = smf.ols(formula, data=df).fit()

    if 'subsamples' in checks:
        for name, condition in checks['subsamples']:
            subset = df[condition]
            results[f'Subsample: {name}'] = smf.ols(
                base_model_formula, data=subset
            ).fit()

    if 'time_periods' in checks:
        for name, condition in checks['time_periods']:
            subset = df[condition]
            results[f'Period: {name}'] = smf.ols(
                base_model_formula, data=subset
            ).fit()

    return results
```

## 6.2 多重共線性チェック

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

def vif_check(df, variables):
    """
    VIF（分散膨張係数）の計算
    VIF > 10 は多重共線性の問題、VIF > 5 は注意
    """
    X = df[variables].dropna()
    X = sm.add_constant(X)

    vif_data = pd.DataFrame()
    vif_data['Variable'] = X.columns
    vif_data['VIF'] = [variance_inflation_factor(X.values, i)
                       for i in range(X.shape[1])]
    vif_data['Problem'] = vif_data['VIF'].apply(
        lambda x: 'High' if x > 10 else ('Moderate' if x > 5 else 'OK')
    )

    return vif_data
```

## 6.3 内生性検定

```python
def endogeneity_test(df, dependent, suspected_endogenous, instruments, exogenous):
    """内生性検定（Durbin-Wu-Hausman検定）"""
    first_stage_formula = f"{suspected_endogenous} ~ {' + '.join(instruments + exogenous)}"
    first_stage = smf.ols(first_stage_formula, data=df).fit()
    df['residual_first'] = first_stage.resid

    augmented_formula = f"{dependent} ~ {suspected_endogenous} + {' + '.join(exogenous)} + residual_first"
    augmented = smf.ols(augmented_formula, data=df).fit()

    return {
        't_statistic': augmented.tvalues['residual_first'],
        'p_value': augmented.pvalues['residual_first'],
        'Endogenous': augmented.pvalues['residual_first'] < 0.05
    }
```

## 6.4 データ品質チェック

### Benford's Law検定

```python
from scipy.stats import chisquare

def benfords_test(data):
    """財務データの信頼性検証"""
    first_digits = [int(str(abs(x))[0]) for x in data if x != 0]
    observed = np.bincount(first_digits, minlength=10)[1:]
    expected = [len(first_digits) * np.log10(1 + 1/d) for d in range(1, 10)]
    stat, p_value = chisquare(observed, expected)
    return p_value > 0.05  # True = データは信頼できる
```

### 外れ値処理

```
- Winsorization：1%/99%でトリミング
- 標準化残差 > 3の除外
- Cook's Distanceによる影響度評価
```

---

# Part 7: データソース

## 7.1 企業財務データ

### 北米
```
Compustat North America（WRDS経由）
- カバレッジ：米国・カナダ上場企業 20,000社以上
- 期間：1950年代〜現在
- 主要テーブル：
  - funda：年次財務データ
  - fundaq：四半期財務データ
  - seg_annual：セグメントデータ（多角化測定）

CRSP（市場データ）
- 株価、リターン、市場価値
- イベントスタディ、Tobin's Q計算
```

### アジア
```
日本：NEEDS-FinancialQUEST
- 日本上場企業3,800社以上
- 系列データ、株式持ち合いデータ

中国：CSMAR
- 中国A株・B株上場企業
- 国有企業vs民間企業分析
```

### グローバル
```
Worldscope (Refinitiv)
- 70カ国、70,000社以上
- 標準化された財務データ

Orbis (BvD)
- 欧州企業に強い
- 所有構造データ
```

## 7.2 イノベーション・特許データ

```
USPTO PatentsView（無料）
- 米国特許全件（1976〜）
- 変数例：
  - 特許ストック = Σ(patents_{t-i} × (1-0.15)^i)
  - 技術多角化 = -Σ(p_i × ln(p_i))
  - 被引用数（影響力指標）

PATSTAT（EPO）
- グローバル特許（90カ国以上）
```

## 7.3 M&A・提携データ

```
SDC Platinum（WRDS経由）
- グローバルM&A、JV、IPO
- 主要変数：取引額、支払方法、関連性

Zephyr (BvD)
- 欧州・アジアのM&Aに強い
```

## 7.4 ガバナンス・ESGデータ

```
ExecuComp（WRDS経由）
- 役員報酬、取締役会構成

MSCI ESG Ratings
- ESGスコア（AAA〜CCC）

CDP（無料申請可）
- 炭素排出データ
```

---

# Part 8: トップジャーナル投稿準備

## 8.1 ジャーナル別要件

### Strategic Management Journal (SMJ)
```
焦点：戦略研究、経営者意思決定
特徴：
- 理論的貢献を重視
- 方法論的厳密性
- 字数：12,000語以内

審査期間：3-6ヶ月
採択率：約8%
```

### Academy of Management Journal (AMJ)
```
焦点：組織・経営全般の実証研究
特徴：
- 高度な実証分析
- 理論と実践の橋渡し
- 字数：12,000語以内

審査期間：3-6ヶ月
採択率：約7%
```

### Organization Science (OS)
```
焦点：組織理論、組織行動
特徴：
- 革新的理論
- 学際的アプローチ
- 字数：制限なし（推奨40ページ）

審査期間：3-6ヶ月
採択率：約8%
```

## 8.2 論文構成テンプレート

```
1. Introduction (2-3ページ)
   - 研究の動機と重要性
   - 理論的ギャップ
   - 主要な貢献のプレビュー

2. Theory & Hypotheses (4-6ページ)
   - 理論的背景
   - 先行研究レビュー
   - 仮説導出

3. Methods (3-4ページ)
   - サンプルとデータ
   - 変数の測定
   - 分析手法

4. Results (3-4ページ)
   - 記述統計と相関
   - 主要分析結果
   - ロバストネスチェック

5. Discussion (2-3ページ)
   - 結果の解釈
   - 理論的含意
   - 実践的含意
   - 限界と将来研究

6. Conclusion (0.5ページ)
```

## 8.3 結果の解釈テンプレート

```
## 主要結果の解釈

### 仮説検証結果

**仮説1**: [仮説の内容]
- 結果: [支持/部分支持/不支持]
- 係数: β = [値], p [</>] [閾値]
- 解釈: [1単位増加に対するY変化の解釈]

**効果量の実質的意義**:
- 標準化係数: [値]
- Cohen's d相当: [小/中/大]
- 実務的含意: [解釈]

### ロバストネス

以下のロバストネスチェックで結果は一貫:
- [ ] 代替的従属変数
- [ ] 代替的独立変数の測定
- [ ] サブサンプル分析
- [ ] 期間別分析
- [ ] 代替的推定方法
```

## 8.4 再現性確保

### AEA準拠のデータ管理
```
必須ファイル：
1. README.md - 再現手順
2. data/ - 生データ（可能な場合）
3. code/ - 分析コード
4. output/ - 結果ファイル

コード要件：
- バージョン管理（Git）
- 環境指定（Docker、requirements.txt）
- 乱数シード固定
- 相対パス使用
```

---

# Part 9: 起動コマンド

## 研究デザインモード
```
Strategic Research Platform起動

目的: 研究デザイン
研究テーマ: [テーマ]
理論的レンズ: [RBV/TCE/Institutional/etc.]
データ要件: [パネル/クロスセクション/イベント]
ターゲットジャーナル: [SMJ/AMJ/OS/ASQ]
```

## 記述統計モード
```
Strategic Research Platform起動

目的: 記述統計
データ: [ファイルパスまたはDataFrame]
変数: [変数リスト]
出力: [統計表/相関行列/分布図]
```

## 回帰分析モード
```
Strategic Research Platform起動

目的: 回帰分析
タイプ: [OLS/パネル/ロジスティック]
式: [Y ~ X1 + X2 + ...]
オプション: [固定効果/ロバストSE/クラスターSE]
出力: [コード/結果テーブル]
```

## 因果推論モード
```
Strategic Research Platform起動

目的: 因果推論
手法: [DID/RDD/IV/PSM]
処置変数: [変数名]
アウトカム: [変数名]
識別戦略: [詳細説明]
出力: [分析コード/結果/診断テスト]
```

## 品質検証モード
```
Strategic Research Platform起動

目的: 品質検証
検証対象: [データ/分析/論文]
チェック項目: [Benford/内生性/ロバストネス/VIF]
出力: [検証レポート]
```

---

## 連携スキル

| スキル名 | 役割 |
|----------|------|
| academic-research-suite | 文献レビュー・論文執筆・引用管理 |
| research-data-hub | データ収集・品質管理 |
| thinking-toolkit | 理論構築・批判的分析 |
| document-design-suite | 結果の可視化・図表作成 |
| code-quality-guardian | コード品質・再現性保証 |

---

**バージョン**: 2.0.0
**統合日**: 2025-11-28
**統合元**: strategic-research-suite, strategic-management-research-hub, strategic-organizational-research-hub, strategic-organizational-empirical, empirical-research-designer, statistical-analysis-suite
