# データ品質保証基準

**Strategic Research Suite品質基準リファレンス**

このファイルはPublication-ready研究のための品質保証基準を定義します。

## 🎯 品質保証の5つの柱

### 1. Statistical Power（統計的検出力）
### 2. Sample Quality（サンプル品質）
### 3. Data Integrity（データ整合性）
### 4. Measurement Validity（測定妥当性）
### 5. Reproducibility（再現可能性）

---

## 1️⃣ Statistical Power Analysis

### 事前検出力分析（Required）

**目的**: Type II error（偽陰性）を避ける

**基準**:
- Target power: **≥ 0.80** (80%)
- α level: 0.05
- Effect size: 先行研究のメタ分析から推定

**計算式（Two-sample t-test）**:
```
n = 2 × (Z_α/2 + Z_β)² × σ² / δ²

Where:
- Z_α/2 = 1.96 (α = 0.05)
- Z_β = 0.84 (power = 0.80)
- σ = 標準偏差
- δ = 効果量
```

**Python実装**:
```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()
sample_size = analysis.solve_power(
    effect_size=0.35,  # Cohen's d
    alpha=0.05,
    power=0.80,
    alternative='two-sided'
)
```

**報告例**:
```
「先行研究（Smith et al., 2020）に基づき、期待効果量をd=0.35と
推定した。80%検出力（α=0.05）を確保するため、1グループあたり
130社が必要と算出された。本研究のサンプル（N=312社）は十分な
統計的検出力（実現検出力=87%）を有している。」
```

### 事後検出力分析（Post-hoc）

**実施タイミング**: 分析完了後

**目的**: 
- 非有意結果の解釈（検出力不足 vs. 真の効果なし）
- 有意結果の信頼性確認

**Warning**: 
- 事後検出力のみでの判断は不適切
- 必ず事前検出力分析を実施

---

## 2️⃣ Sample Quality Standards

### サバイバルバイアス対策（Critical）

**問題**: 現存企業のみ分析 → パフォーマンス過大評価

**対策**:
1. **Delisted firmsを含める**
   - CRSPのdelisting情報統合
   - デリスト理由の分類（merger, liquidation, etc.）

2. **Attrition分析**
   - デリスト企業 vs. 存続企業の特性比較
   - t-test for systematic differences

**基準**:
- Attrition rate < 30%: 許容範囲
- Attrition rate 30-50%: Selection model必要（Heckman）
- Attrition rate > 50%: 深刻なバイアス

**Python実装**:
```python
# Attrition分析
df_panel['attrite'] = df_panel.groupby('firm_id')['year'].transform(
    lambda x: 1 if x.max() < df_panel['year'].max() else 0
)

from scipy.stats import ttest_ind

attrite_firms = df_panel[df_panel['attrite'] == 1]
survive_firms = df_panel[df_panel['attrite'] == 0]

for var in ['roa', 'total_assets', 'leverage']:
    t, p = ttest_ind(
        attrite_firms[var].dropna(),
        survive_firms[var].dropna()
    )
    if p < 0.05:
        print(f"WARNING: {var} significantly different (p={p:.4f})")
```

### Winsorization（外れ値処理）

**基準**: 1%ile & 99%ile

**対象変数**: すべての連続変数

**理由**: 
- 極端値の影響緩和
- パラメトリック検定の前提改善

**Python実装**:
```python
from scipy.stats.mstats import winsorize

continuous_vars = ['roa', 'leverage', 'tobins_q', 'rd_intensity']

for var in continuous_vars:
    df[f'{var}_winsor'] = winsorize(
        df[var],
        limits=[0.01, 0.01],
        nan_policy='omit'
    )
```

**報告**:
```
「すべての連続変数を1パーセンタイル及び99パーセンタイルで
winsorizeした。」
```

---

## 3️⃣ Data Integrity Checks

### Benford's Law Test

**目的**: データ不正・エラーの検出

**対象**: 自然発生データ（財務データ）

**基準**:
- χ² test: p > 0.05 → 合格
- p < 0.05 → 要調査

**Python実装**:
```python
def benford_test(data):
    """Benford's Law検定"""
    import numpy as np
    from scipy.stats import chisquare
    
    # 先頭桁抽出
    first_digits = [int(str(abs(x))[0]) for x in data if x != 0]
    
    # 観測度数
    observed = np.bincount(first_digits)[1:10]
    
    # Benford's Lawの期待度数
    expected = [np.log10(1 + 1/d) * len(first_digits) for d in range(1, 10)]
    
    # χ² test
    chi2, p_value = chisquare(observed, expected)
    
    return {
        'chi2': chi2,
        'p_value': p_value,
        'conforms': p_value > 0.05
    }
```

**例外**（Benford's Lawが適用されない）:
- ID番号
- 人為的制約（最低資本金要件等）
- 小サンプル（N < 100）

### 会計恒等式検証

**恒等式**:
```
総資産 = 総負債 + 株主資本
```

**許容誤差**: < 1%

**Python実装**:
```python
df['bs_error'] = abs(df['at'] - (df['lt'] + df['ceq']))
df['bs_error_pct'] = df['bs_error'] / df['at']

violations = df[df['bs_error_pct'] > 0.01]

if len(violations) / len(df) > 0.05:
    print("WARNING: >5% balance sheet errors")
```

### 構造変化検定（Chow Test）

**目的**: データの時系列安定性確認

**方法**: 
1. 時系列をsub-periodに分割
2. 各期間で回帰
3. 係数の安定性検定

**基準**:
- F-test: p > 0.05 → 安定
- p < 0.05 → 構造変化あり

**対処**:
- 既知イベント（2008金融危機等）→ Period dummyで統制
- 未知イベント → 原因調査、期間分割分析

---

## 4️⃣ Measurement Validity

### Construct Validity（構成概念妥当性）

**基準**:
1. **Face validity**: 測定が直感的に妥当
2. **Content validity**: 概念の全側面をカバー
3. **Criterion validity**: 他の基準と相関

**Example: Dynamic Capability**

❌ **Poor measurement**:
```
Dynamic Capability = R&D支出のみ
```

✅ **Good measurement**:
```
Dynamic Capability = 
  - R&D intensity
  - 製品開発サイクル時間
  - 市場適応速度
  - 組織柔軟性指標
の統合指標
```

### Reliability（信頼性）

**Internal Consistency**:
- Cronbach's α ≥ 0.70 (許容)
- Cronbach's α ≥ 0.80 (良好)

**適用場面**: 
- 複数項目を統合する場合
- アンケート調査データ

**Python実装**:
```python
def cronbach_alpha(items):
    """Cronbach's α計算"""
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    n_items = items.shape[1]
    
    alpha = (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)
    return alpha
```

### Convergent & Discriminant Validity

**Convergent**: 同一概念の異なる測定が高相関

**Discriminant**: 異なる概念の測定が低相関

**基準**:
- Convergent: r > 0.50
- Discriminant: r < 0.30

---

## 5️⃣ Reproducibility Standards

### AEA (American Economic Association) 基準

**Required Elements**:

1. **Data Availability Statement**
   ```
   「データは[ソース名]から[アクセス方法]で入手可能。
   本研究で使用したデータセットは[URL]で公開している。」
   ```

2. **Code Availability**
   ```
   「すべての分析コードは[GitHub URL]で公開している。」
   ```

3. **Computational Requirements**
   ```
   - Python 3.9+
   - RAM: 16GB minimum
   - Runtime: 約2時間
   ```

4. **Random Seed Documentation**
   ```python
   np.random.seed(42)
   random.seed(42)
   ```

### Replication Package Checklist

- [ ] README.md with execution instructions
- [ ] Data sources documented
- [ ] All scripts numbered sequentially
- [ ] Requirements.txt / environment.yml
- [ ] Expected output described
- [ ] Known limitations documented
- [ ] Contact information provided

### Docker Environment（推奨）

**利点**:
- 環境の完全再現
- OS依存性の排除
- バージョン固定

**Dockerfile example**:
```dockerfile
FROM python:3.9-slim

WORKDIR /research

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_all.py"]
```

---

## 📊 Quality Score Matrix

各基準に対してスコアを付与：

| 基準 | Weight | Score (0-10) | Weighted |
|------|--------|--------------|----------|
| Statistical Power | 20% | 8 | 1.6 |
| Sample Quality | 20% | 7 | 1.4 |
| Data Integrity | 20% | 9 | 1.8 |
| Measurement Validity | 20% | 8 | 1.6 |
| Reproducibility | 20% | 10 | 2.0 |
| **Total** | 100% | - | **8.4** |

**解釈**:
- Score ≥ 8.0: Publication-ready (Top journals)
- Score 6.0-7.9: Revision needed
- Score < 6.0: Major revision required

---

## 🚨 Critical Failures (即座に対処)

以下のいずれかが検出された場合、分析を中断して対処：

1. **Power < 0.50**: サンプル不足
2. **Benford p < 0.001**: データ不正の可能性
3. **BS error > 10%**: 深刻なデータ品質問題
4. **VIF > 20**: 極端な多重共線性
5. **Attrition > 50%**: Selection biasが深刻

---

## 📈 Reporting Template

### Methods Section

```markdown
## 3.3 Data Quality Assurance

We conducted comprehensive quality assurance following best practices 
(Smith & Jones, 2020).

**Statistical Power**: A priori power analysis indicated that our sample 
(N=312 firms) provides 87% power to detect a medium effect (d=0.35) 
at α=0.05.

**Survivor Bias**: We included delisted firms using CRSP delisting data, 
resulting in an attrition rate of 18%. t-tests revealed no significant 
differences in key variables between surviving and delisted firms.

**Outlier Treatment**: All continuous variables were winsorized at the 
1st and 99th percentiles to mitigate extreme value influence.

**Data Integrity**: Benford's Law tests (χ²=12.3, p=0.14) and balance 
sheet identity checks (error rate <1%) confirmed data integrity.

**Structural Stability**: Chow tests revealed no significant structural 
breaks across the study period (F=1.8, p=0.12).
```

---

## 🔗 関連スキル

この品質基準は以下のスキルで実装されています：

- **1-core-workflow**: Phase 6で品質保証を実行
- **3-statistical-methods**: 統計的検出力分析の詳細
- **8-automation**: 自動品質チェックパイプライン

---

**このファイルは全スキルから参照されます**

Publication-ready研究のために、これらの基準を必ず満たしてください。

最終更新: 2025-11-01
Version: 4.0
