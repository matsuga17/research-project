# 頑健性検証ガイド（Robustness Checks Guide）
## トップジャーナル投稿に向けた体系的検証手順

**対象読者**: 学術論文執筆者、特にトップジャーナル（JF, JFE, RFS, MS, SMJ等）への投稿を目指す研究者  
**目的**: 査読で求められる頑健性検証を網羅的に実施し、結果の信頼性を確立  
**Version**: 2.0  
**最終更新**: 2025-10-31

---

## 目次

1. [頑健性検証の重要性](#importance)
2. [必須の頑健性検証（7カテゴリ）](#mandatory)
3. [推奨される追加検証](#optional)
4. [頑健性検証の報告方法](#reporting)
5. [よくある失敗例と対策](#pitfalls)

---

<a name="importance"></a>
## 1. 頑健性検証の重要性

### なぜ頑健性検証が必須なのか

**トップジャーナル査読の現実**:
- 平均2-3回のreviseが要求される
- 各reviseで新たな頑健性検証が追加要求される
- **初回投稿時に主要な検証を済ませることで、revise期間を大幅短縮**

**頑健性検証の3つの目的**:
1. **内的妥当性の確認**: 結果が真の効果を捉えているか
2. **外的妥当性の検証**: 結果が一般化可能か
3. **測定誤差の影響評価**: データの不完全性が結論を変えないか

---

<a name="mandatory"></a>
## 2. 必須の頑健性検証（7カテゴリ）

### A. サンプル構成の変更（Sample Composition）

**目的**: 特定のサブサンプルに結果が依存していないことを示す

#### A1. サブサンプル分析

```python
# 1. 産業別
for industry in df['industry'].unique():
    subsample = df[df['industry'] == industry]
    result = run_regression(subsample)
    print(f"{industry}: β={result.params['rd_intensity']:.3f}, p={result.pvalues['rd_intensity']:.3f}")

# 2. 時期別（前半・後半）
df_early = df[df['year'] <= 2019]
df_late = df[df['year'] > 2019]

# 3. 企業規模別（四分位）
df['size_quartile'] = pd.qcut(df['log_assets'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
for q in ['Q1', 'Q2', 'Q3', 'Q4']:
    subsample = df[df['size_quartile'] == q]
    result = run_regression(subsample)
```

**報告方法**:
```
Table A1: Results by Subsamples

                    Full Sample    High-Tech    Traditional    Small Firms    Large Firms
rd_intensity        0.045***       0.062***     0.031**       0.038**        0.051***
                    (0.012)        (0.018)      (0.015)       (0.017)        (0.014)
```

#### A2. 極端値の除外

```python
# 1. 上下1%をトリム
df_trimmed = df[(df['roa'] > df['roa'].quantile(0.01)) & 
                (df['roa'] < df['roa'].quantile(0.99))]

# 2. 異常値フラグ観測を除外
df_no_outliers = df[df['outlier_flag'] == 0]

# 3. 影響力の大きい観測を除外（Cook's distance > 4/n）
df_no_influential = df[df['influential_flag'] == 0]
```

**期待される結果**: 係数の符号と有意性が維持される（多少の変動は許容）

---

### B. 変数定義の変更（Variable Definition）

**目的**: 特定の変数定義に結果が依存していないことを示す

#### B1. 従属変数の代替定義

```python
# ROAの代替定義
df['roa_alt1'] = df['ebit'] / df['total_assets']  # EBIT-based
df['roa_alt2'] = df['net_income'] / df['avg_assets']  # 平均資産
df['roa_alt3'] = df['operating_income'] / df['total_assets']  # 営業利益

# 各定義で回帰を再実行
for roa_var in ['roa', 'roa_alt1', 'roa_alt2', 'roa_alt3']:
    result = run_regression(df, dependent_var=roa_var)
```

#### B2. 独立変数の代替定義

```python
# R&D intensityの代替定義
df['rd_alt1'] = df['rd_expenditure'] / df['total_assets']  # 資産比
df['rd_alt2'] = np.log(df['rd_expenditure'] + 1)  # 対数変換
df['rd_alt3'] = df['rd_expenditure'] / df['market_value']  # 時価総額比
```

**報告方法**:
```
Table A2: Alternative Variable Definitions

Dependent Variable:    ROA        ROA (EBIT)    ROA (Avg)    Operating ROA
rd_intensity          0.045***    0.048***      0.043***     0.046***
                      (0.012)     (0.013)       (0.011)      (0.012)
```

---

### C. 推定手法の変更（Estimation Method）

**目的**: 特定の推定手法に結果が依存していないことを示す

#### C1. 標準誤差の頑健化

```python
import statsmodels.formula.api as smf

# 1. OLS with heteroskedasticity-robust SE
model1 = smf.ols('roa ~ rd_intensity + controls', data=df).fit(cov_type='HC3')

# 2. Cluster-robust SE (firm level)
model2 = smf.ols('roa ~ rd_intensity + controls', data=df).fit(
    cov_type='cluster', cov_kwds={'groups': df['firm_id']}
)

# 3. Two-way clustering (firm + year)
# Requires: linearmodels package
from linearmodels import PanelOLS
model3 = PanelOLS.from_formula(
    'roa ~ rd_intensity + controls + EntityEffects + TimeEffects',
    data=df
).fit(cov_type='clustered', clusters=df[['firm_id', 'year']])
```

#### C2. パネルデータ推定

```python
from linearmodels import PanelOLS, RandomEffects

# 固定効果モデル
fe_model = PanelOLS.from_formula(
    'roa ~ rd_intensity + controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit()

# ランダム効果モデル
re_model = RandomEffects.from_formula(
    'roa ~ rd_intensity + controls',
    data=df.set_index(['firm_id', 'year'])
).fit()

# Hausman test
# H0: Random effects is consistent (preferred)
hausman_stat = calculate_hausman_test(fe_model, re_model)
```

**報告方法**:
```
Table A3: Alternative Estimation Methods

                    OLS         Robust SE    Cluster SE    Fixed Effects
rd_intensity       0.045***     0.045***     0.045**       0.042**
                   (0.010)      (0.012)      (0.018)       (0.020)
R²                  0.358        0.358        0.358         0.421
```

---

### D. コントロール変数の変更（Control Variables）

**目的**: オミッテッド・バイアス（欠落変数バイアス）がないことを示す

#### D1. 段階的追加

```python
# Model 1: 基本モデル（最小限のコントロール）
model1 = smf.ols('roa ~ rd_intensity + log_assets + leverage', data=df).fit()

# Model 2: 産業特性追加
model2 = smf.ols('roa ~ rd_intensity + log_assets + leverage + hhi + industry_growth', 
                 data=df).fit()

# Model 3: 企業特性追加
model3 = smf.ols('roa ~ rd_intensity + log_assets + leverage + hhi + industry_growth + age + diversification', 
                 data=df).fit()

# Model 4: ガバナンス変数追加
model4 = smf.ols('roa ~ rd_intensity + log_assets + leverage + hhi + industry_growth + age + diversification + board_size + ceo_duality', 
                 data=df).fit()
```

**期待される結果**: 主要な独立変数（rd_intensity）の係数が安定

#### D2. 固定効果の追加

```python
# 1. 産業固定効果
model_ind = smf.ols('roa ~ rd_intensity + controls + C(industry)', data=df).fit()

# 2. 年固定効果
model_year = smf.ols('roa ~ rd_intensity + controls + C(year)', data=df).fit()

# 3. 両方（two-way fixed effects）
model_both = smf.ols('roa ~ rd_intensity + controls + C(industry) + C(year)', 
                     data=df).fit()

# 4. 企業固定効果（パネル）
model_firm = PanelOLS.from_formula(
    'roa ~ rd_intensity + time_varying_controls + EntityEffects',
    data=df.set_index(['firm_id', 'year'])
).fit()
```

---

### E. 内生性への対処（Endogeneity）

**目的**: 逆因果性・同時決定バイアスがないことを示す

#### E1. ラグ変数の使用

```python
# 独立変数を1期ラグ
df['lag_rd_intensity'] = df.groupby('firm_id')['rd_intensity'].shift(1)

# ラグ変数で回帰
model_lag = smf.ols('roa ~ lag_rd_intensity + controls', data=df).fit()
```

**解釈**: RD投資の効果が1期後のROAに現れる → 逆因果性の可能性低下

#### E2. 操作変数法（IV/2SLS）

```python
from linearmodels.iv import IV2SLS

# 適切な操作変数が必要（例: industry_avg_rd, tax_credit）
model_iv = IV2SLS.from_formula(
    'roa ~ [rd_intensity ~ industry_avg_rd + tax_credit] + controls',
    data=df
).fit()

# 第1段階の検証
print(f"First-stage F-statistic: {model_iv.first_stage.diagnostics['f.stat']:.2f}")
# Rule of thumb: F > 10
```

**注意**: 操作変数の妥当性（relevance & exclusion）を丁寧に議論

#### E3. Heckman 2段階推定（サンプル選択バイアス）

```python
# 生存している企業のみが観測される問題に対処
from statsmodels.regression.linear_model import Heckman

# Selection equation
df['selected'] = (df['exit_flag'] == 0).astype(int)

# Outcome equation
heckman = Heckman(
    endog=df['roa'],
    exog=df[['rd_intensity'] + controls],
    exog_select=df[['log_assets', 'leverage', 'industry_growth'] + controls]
).fit()

print(heckman.summary())
# Check: lambda (inverse Mills ratio) が有意 → selection bias存在
```

---

### F. 外れ値処理の変更（Outlier Treatment）

**目的**: 結果が外れ値処理方法に依存していないことを示す

#### F1. 代替的なWinsorization

```python
# 1. 1%/99% (ベースライン)
df_w1 = df.copy()
df_w1['roa'] = df_w1['roa'].clip(
    lower=df['roa'].quantile(0.01),
    upper=df['roa'].quantile(0.99)
)

# 2. 5%/95% (より保守的)
df_w5 = df.copy()
df_w5['roa'] = df_w5['roa'].clip(
    lower=df['roa'].quantile(0.05),
    upper=df['roa'].quantile(0.95)
)

# 3. Winsorization なし
df_raw = df.copy()

# 各データで回帰
results = []
for name, data in [('1%/99%', df_w1), ('5%/95%', df_w5), ('No Winsor', df_raw)]:
    model = smf.ols('roa ~ rd_intensity + controls', data=data).fit()
    results.append({'method': name, 'coef': model.params['rd_intensity'], 
                   'pval': model.pvalues['rd_intensity']})
```

#### F2. 頑健な推定法（Robust Regression）

```python
from statsmodels.robust.robust_linear_model import RLM

# M-estimator (Huber)
model_robust = RLM.from_formula('roa ~ rd_intensity + controls', 
                                data=df, M=sm.robust.norms.HuberT()).fit()

print(f"Robust regression: β={model_robust.params['rd_intensity']:.3f}")
```

---

### G. 時系列構造への対応（Time-Series Structure）

**目的**: 時系列相関・動学的関係を考慮

#### G1. 動学パネルモデル（Dynamic Panel）

```python
# Arellano-Bond estimator
from linearmodels.panel import PanelOLS

df['lag_roa'] = df.groupby('firm_id')['roa'].shift(1)

model_dynamic = smf.ols('roa ~ lag_roa + rd_intensity + controls', 
                        data=df).fit(cov_type='cluster', 
                                    cov_kwds={'groups': df['firm_id']})
```

#### G2. イベントスタディ分析

```python
# R&D急増のイベント前後でROA変化を観察
df['rd_spike'] = (df['rd_growth'] > df['rd_growth'].quantile(0.90)).astype(int)

# t-3からt+3までの動学効果
for t in range(-3, 4):
    df[f'period_{t}'] = ((df['year'] - df['event_year']) == t).astype(int)

model_event = smf.ols('roa ~ ' + ' + '.join([f'period_{t}' for t in range(-3, 4)]) + ' + controls', 
                     data=df).fit()
```

---

<a name="optional"></a>
## 3. 推奨される追加検証

### H. プラセボテスト（Placebo Tests）

**目的**: 効果が偶然でないことを示す

```python
# 1. ランダムな処置割り当て
np.random.seed(42)
df['placebo_treatment'] = np.random.permutation(df['rd_intensity'])

model_placebo = smf.ols('roa ~ placebo_treatment + controls', data=df).fit()
# 期待: 係数が非有意

# 2. 将来の処置を使用（forward placebo）
df['future_rd'] = df.groupby('firm_id')['rd_intensity'].shift(-1)
model_future = smf.ols('roa ~ future_rd + controls', data=df).fit()
# 期待: 非有意（因果関係なし）
```

### I. サブサンプル分析（より詳細）

```python
# 1. 上場年数別
df['listing_age'] = df['year'] - df['listing_year']
df['mature'] = (df['listing_age'] > 5).astype(int)

model_interact = smf.ols('roa ~ rd_intensity + rd_intensity:mature + mature + controls', 
                         data=df).fit()

# 2. 国別（クロスカントリー研究）
for country in df['country'].unique():
    subsample = df[df['country'] == country]
    model = smf.ols('roa ~ rd_intensity + controls', data=subsample).fit()
    print(f"{country}: β={model.params['rd_intensity']:.3f}")
```

### J. 代替的なサンプル期間

```python
# 1. 金融危機を除外（2008-2009）
df_no_crisis = df[~df['year'].isin([2008, 2009])]

# 2. COVID-19を除外（2020-2021）
df_no_covid = df[~df['year'].isin([2020, 2021])]

# 3. ローリングウィンドウ分析
for start_year in range(2010, 2018):
    end_year = start_year + 5
    window_df = df[(df['year'] >= start_year) & (df['year'] <= end_year)]
    model = smf.ols('roa ~ rd_intensity + controls', data=window_df).fit()
    print(f"{start_year}-{end_year}: β={model.params['rd_intensity']:.3f}")
```

---

<a name="reporting"></a>
## 4. 頑健性検証の報告方法

### 論文本文での記載

**簡潔な要約文（結果セクション）**:
```
"Our main findings are robust to several alternative specifications. 
Results remain qualitatively similar when we (i) use alternative measures 
of performance (EBIT/assets, operating ROA), (ii) employ different 
estimation methods (cluster-robust standard errors, fixed effects), 
(iii) exclude outliers using various criteria, and (iv) control for 
additional firm and industry characteristics. (See Online Appendix Tables 
A1-A5 for detailed results.)"
```

### オンライン付録での完全報告

**推奨構成**:

```
Online Appendix: Robustness Checks

Table A1: Alternative Dependent Variable Definitions
Table A2: Alternative Independent Variable Definitions
Table A3: Alternative Estimation Methods
Table A4: Subsample Analyses
Table A5: Additional Control Variables
Table A6: Endogeneity Tests (IV, Lagged variables)
Table A7: Outlier Treatment Alternatives
Table A8: Placebo Tests

Figure A1: Coefficient Stability Plot (varying control sets)
Figure A2: Event Study Plot (dynamic effects)
```

### 係数安定性プロット

```python
import matplotlib.pyplot as plt

# 異なる仕様での係数推定値をプロット
specs = ['Baseline', 'Alt Dep', 'Alt Indep', 'Robust SE', 
         'FE', 'No Outliers', 'Extra Controls']
coefs = [0.045, 0.048, 0.043, 0.045, 0.042, 0.046, 0.044]
ses = [0.012, 0.013, 0.011, 0.012, 0.020, 0.014, 0.013]

plt.figure(figsize=(10, 6))
plt.errorbar(range(len(specs)), coefs, yerr=[1.96*se for se in ses], 
             fmt='o', capsize=5, capthick=2)
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.xticks(range(len(specs)), specs, rotation=45, ha='right')
plt.ylabel('Coefficient on R&D Intensity')
plt.title('Robustness: Coefficient Stability Across Specifications')
plt.tight_layout()
plt.savefig('results/robustness_stability.pdf')
```

---

<a name="pitfalls"></a>
## 5. よくある失敗例と対策

### 失敗例1: 「頑健性検証で結果が消える」

**症状**: メイン結果は有意だが、いくつかの頑健性検証で非有意に

**原因**:
- サンプルサイズ不足（統計的検出力の問題）
- 本当に頑健でない（特定条件下のみで成立）
- 多重検定問題（何度も検証すると偶然非有意になる）

**対策**:
1. **事前にサンプルサイズを設計**（Phase 3.5参照）
2. **主要な検証を事前登録**（OSF, AsPredicted）
3. **非有意になった検証の解釈を丁寧に議論**

```
"While the effect becomes statistically insignificant in the smallest 
subsample (n=87, bottom quartile), this likely reflects reduced 
statistical power rather than a true null effect. The point estimate 
(β=0.034) remains positive and economically meaningful."
```

### 失敗例2: 「p-hacking」の疑い

**症状**: 査読者から「データマイニング」「cherry-picking」と指摘

**原因**:
- 有意になるまで仕様を変え続けた
- 非有意の結果を報告していない
- 理論的根拠なく多数の交互作用項を試した

**対策**:
1. **Pre-analysis plan作成**
   ```markdown
   # Pre-Analysis Plan
   
   ## Primary Hypothesis
   H1: R&D intensity positively affects ROA (β > 0)
   
   ## Primary Specification
   ROA = β₀ + β₁·RD_intensity + β₂·Log_assets + β₃·Leverage + ε
   
   ## Pre-specified Robustness Checks
   1. Alternative dependent variable: EBIT/assets
   2. Cluster-robust standard errors
   3. Exclude top/bottom 1% of ROA
   
   Registered: 2024-10-31
   ```

2. **すべての検証結果を報告**（有意・非有意問わず）

3. **理論的動機を明確に**
   ```
   "We test whether the effect varies by firm size because [theory X] 
   predicts that [mechanism Y] should be stronger for larger firms."
   ```

### 失敗例3: 操作変数の妥当性が疑わしい

**症状**: 査読者から「exclusion restrictionが成立しない」と指摘

**典型的な問題のある操作変数**:
- Industry average R&D → 産業レベルの他の要因と相関の可能性
- Firm age → 直接ROAに影響する可能性
- CEO characteristics → 企業選択と相関

**良い操作変数の例**:
- 外生的ショック（自然災害、規制変更）
- ランダム割り当て（実験）
- 地理的・制度的変数（距離、法制度）

**対策**:
1. **第1段階の強さを確認**（F統計量 > 10）
2. **Exclusion restrictionを丁寧に議論**
3. **過剰識別検定**（複数の操作変数）

```python
# Sargan-Hansen test (overidentification)
from linearmodels.iv import IV2SLS

model_iv = IV2SLS.from_formula(
    'roa ~ [rd_intensity ~ instrument1 + instrument2] + controls',
    data=df
).fit()

print(f"Sargan test p-value: {model_iv.sargan:.4f}")
# H0: All instruments are valid
# p > 0.10 → instruments likely valid
```

---

## 6. 頑健性検証の優先順位

### 最優先（必須）

1. ✅ **クラスター頑健標準誤差**
2. ✅ **代替的な従属変数定義**
3. ✅ **外れ値処理の変更**
4. ✅ **固定効果の追加**
5. ✅ **サブサンプル分析（産業別、時期別）**

### 高優先（強く推奨）

6. ✅ **代替的な独立変数定義**
7. ✅ **追加コントロール変数**
8. ✅ **ラグ変数の使用**
9. ✅ **動学パネルモデル**

### 中優先（トップジャーナルでは推奨）

10. ⭕ **操作変数法**（適切なIVがある場合）
11. ⭕ **プラセボテスト**
12. ⭕ **Heckman補正**（サンプル選択バイアスが疑われる場合）

---

## 7. 実装チェックリスト

### 分析実施前

- [ ] Pre-analysis planを作成・登録
- [ ] サンプルサイズ計算を実施（Phase 3.5）
- [ ] 主要な仕様を事前決定

### 分析実施中

- [ ] 全7カテゴリの必須検証を実施
- [ ] 各検証の結果を記録（有意・非有意問わず）
- [ ] コード・データを整理（再現可能性）

### 論文執筆時

- [ ] 本文に簡潔な要約を記載
- [ ] オンライン付録に完全な結果を掲載
- [ ] 係数安定性プロットを作成
- [ ] 非有意結果の解釈を議論

### 投稿前

- [ ] すべての検証が再現可能か確認
- [ ] データ・コードをアーカイブ
- [ ] Replication packageを整備

---

## 8. 参考文献

### 頑健性検証の方法論

- Angrist, J. D., & Pischke, J. S. (2008). *Mostly Harmless Econometrics*. Princeton University Press.
- Cameron, A. C., & Miller, D. L. (2015). A practitioner's guide to cluster-robust inference. *Journal of Human Resources*, 50(2), 317-372.
- Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference*. Cambridge University Press.

### トップジャーナルの実践例

- Angrist, J. D., & Lavy, V. (1999). Using Maimonides' rule to estimate the effect of class size on scholastic achievement. *Quarterly Journal of Economics*, 114(2), 533-575.
- Bertrand, M., Duflo, E., & Mullainathan, S. (2004). How much should we trust differences-in-differences estimates? *Quarterly Journal of Economics*, 119(1), 249-275.

### データ品質・p-hacking

- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science*, 22(11), 1359-1366.
- Ioannidis, J. P. (2005). Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

---

## 付録: Pythonコード実装例

### 完全な頑健性検証パイプライン

```python
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS
import numpy as np

class RobustnessChecker:
    """頑健性検証の自動化"""
    
    def __init__(self, df, formula, firm_id='firm_id', time_var='year'):
        self.df = df
        self.formula = formula
        self.firm_id = firm_id
        self.time_var = time_var
        self.results = {}
    
    def run_all_checks(self):
        """すべての頑健性検証を実行"""
        
        print("=" * 70)
        print("COMPREHENSIVE ROBUSTNESS CHECKS")
        print("=" * 70)
        
        # A. サンプル構成
        self.check_subsamples()
        
        # B. 変数定義
        self.check_variable_definitions()
        
        # C. 推定手法
        self.check_estimation_methods()
        
        # D. コントロール変数
        self.check_control_variables()
        
        # E. 外れ値処理
        self.check_outlier_treatment()
        
        # F. 時系列構造
        self.check_dynamic_specification()
        
        # G. プラセボテスト
        self.check_placebo()
        
        return self.results
    
    def check_subsamples(self):
        """サブサンプル分析"""
        print("\n[1/7] Subsample Analysis")
        
        # 産業別
        for ind in self.df['industry'].unique():
            subsample = self.df[self.df['industry'] == ind]
            if len(subsample) > 30:
                model = smf.ols(self.formula, data=subsample).fit()
                self.results[f'subsample_{ind}'] = model
                print(f"  {ind}: n={len(subsample)}, β={model.params[1]:.3f}, p={model.pvalues[1]:.3f}")
    
    def check_variable_definitions(self):
        """変数定義の変更"""
        print("\n[2/7] Alternative Variable Definitions")
        
        # 従属変数の代替定義を試行
        alt_dep_vars = [col for col in self.df.columns if 'alt' in col.lower() and 'roa' in col.lower()]
        for var in alt_dep_vars:
            alt_formula = self.formula.replace('roa', var)
            model = smf.ols(alt_formula, data=self.df).fit()
            self.results[f'alt_dep_{var}'] = model
            print(f"  {var}: β={model.params[1]:.3f}, p={model.pvalues[1]:.3f}")
    
    # ... 他の検証メソッド ...
    
    def generate_report(self, output_path='robustness_report.html'):
        """HTMLレポート生成"""
        # 実装: すべての結果を整理したレポート作成
        pass


# 使用例
df = pd.read_csv('data/clean/final_dataset.csv')

checker = RobustnessChecker(
    df,
    formula='roa ~ rd_intensity + log_assets + leverage + C(year) + C(industry)',
    firm_id='firm_id',
    time_var='year'
)

results = checker.run_all_checks()
checker.generate_report('reports/robustness_checks.html')
```

---

**Version履歴**:
- v1.0 (2024-01-15): 初版作成
- v2.0 (2025-10-31): 実装コード追加、失敗例・対策拡充

---

**関連ドキュメント**:
- [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) - 投稿前チェックリスト
- [DATA_ETHICS_GUIDE.md](DATA_ETHICS_GUIDE.md) - データ倫理ガイド
- [TROUBLESHOOTING_FAQ.md](TROUBLESHOOTING_FAQ.md) - よくある問題と解決策
