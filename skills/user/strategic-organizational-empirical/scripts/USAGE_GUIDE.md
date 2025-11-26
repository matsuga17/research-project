# スクリプト使用ガイド：実装済み機能の包括的マニュアル

**作成日**：2025年11月8日  
**バージョン**：1.0  
**対象**：戦略・組織研究の実証分析を行う研究者

---

## 序章：実装機能の哲学と実践

本ガイドは、現在実装されている4つのスクリプトの詳細な使用方法を提供する。それは単なる技術的マニュアルではなく、各スクリプトの背後にある理論的基盤、設計思想、実践的応用を統合的に理解するための知的資源なのである。

**実装済みスクリプト**：
1. `construct_validator.py` - 構成概念妥当性検証システム
2. `causal_explorer.py` - 因果推論探索システム
3. `theory_driven_eda.py` - 理論駆動型探索的データ分析
4. `example_constructs_config.py` - 構成概念設定例

---

## I. 構成概念妥当性検証システム（`construct_validator.py`）

### 1.1 理論的基盤：測定の認識論的営為

構成概念妥当性の検証は、抽象的な理論的概念（組織能力、戦略志向性、組織文化等）を経験的に測定可能な指標へと変換する知的営為である。Churchill (1979)の測定尺度開発パラダイム、Fornell & Larcker (1981)の構造方程式モデリング、Messick (1995)の統合的妥当性理論に基づく本システムは、この認識論的橋渡しを実践的に支援する。

**哲学的考察**：
測定とは、プラトン的イデア（理念的な真の得点）と経験的現実（観測得点）の間の媒介である。我々が観測するのは、常に測定誤差によって歪められた不完全な影に過ぎない。しかし、適切な方法論により、この影から真の姿への接近は可能となる。

### 1.2 基本的な使用方法

#### A. 最小限の実行例

```bash
python scripts/construct_validator.py data/survey_data.csv \
  --constructs-config config/constructs.yaml \
  -o ./output
```

**必須引数**：
- `data/survey_data.csv`：データファイルのパス
- `--constructs-config`：構成概念の定義ファイル（YAML形式）
- `-o`：出力ディレクトリ

**所要時間**：2-5分（データ規模に依存）

#### B. 包括的な実行例

```bash
python scripts/construct_validator.py data/comprehensive_survey.csv \
  --constructs-config config/detailed_constructs.yaml \
  --validation-level comprehensive \
  --cfa-method ml \
  --output ./validation_output \
  --verbose
```

**オプション引数の詳細**：

**`--validation-level` [basic|standard|comprehensive]**（デフォルト：standard）
- `basic`：基本的な信頼性分析のみ（Cronbach's α）
- `standard`：信頼性 + 収束的妥当性
- `comprehensive`：全ての検証（信頼性 + 収束的 + 弁別的 + CFA）

**`--cfa-method` [ml|gls|wls]**（デフォルト：ml）
- `ml`：最尤法（Maximum Likelihood）- 最も一般的
- `gls`：一般化最小二乗法（Generalized Least Squares）
- `wls`：加重最小二乗法（Weighted Least Squares）- 非正規データに適用

**`--verbose`**：詳細な実行ログの出力

### 1.3 構成概念設定ファイル（YAML）の作成

#### A. 基本構造

```yaml
constructs:
  organizational_capability:
    description: "組織能力の測定"
    items:
      - OC1  # R&D投資額（対売上高比）
      - OC2  # 特許出願数
      - OC3  # 新製品開発サイクル（日数）
      - OC4  # 従業員訓練投資額
      - OC5  # プロセス改善提案数
  
  strategic_orientation:
    description: "戦略志向性の測定（7点リッカート尺度）"
    items:
      - SO1  # イノベーション志向
      - SO2  # 市場志向
      - SO3  # 学習志向
      - SO4  # 起業家的志向
  
  firm_performance:
    description: "企業業績の測定"
    items:
      - FP1  # ROA（総資産利益率）
      - FP2  # ROE（自己資本利益率）
      - FP3  # 売上成長率
      - FP4  # 市場シェア

# オプション：理論的関係性の定義（Phase 2以降で活用予定）
theoretical_relationships:
  - from: organizational_capability
    to: firm_performance
    expected_direction: positive
    hypothesis: "H1: 組織能力は企業業績を向上させる"
```

#### B. 設計原則

**1. 構成概念の一次元性**：
各構成概念は、単一の潜在変数を測定すべきである。多次元構成概念の場合は、下位次元ごとに分割する。

**悪い例**（多次元混在）：
```yaml
organizational_capability:
  items:
    - OC1  # 技術的能力
    - OC2  # マーケティング能力
    - OC3  # 財務管理能力
```

**良い例**（次元分離）：
```yaml
technical_capability:
  items: [OC1, OC2, OC3]

marketing_capability:
  items: [OC4, OC5, OC6]

financial_capability:
  items: [OC7, OC8, OC9]
```

**2. 項目数の指針**：
- **最小**：3項目（統計的識別の最低限）
- **推奨**：4-6項目（バランスが良い）
- **注意**：8項目以上（冗長性のリスク）

### 1.4 出力結果の解釈

#### A. 信頼性分析結果（`reliability_analysis.json`）

```json
{
  "organizational_capability": {
    "n_items": 5,
    "cronbach_alpha": 0.847,
    "composite_reliability": 0.862,
    "item_total_correlations": {
      "OC1": 0.68,
      "OC2": 0.71,
      "OC3": 0.52,
      "OC4": 0.76,
      "OC5": 0.69
    },
    "alpha_if_deleted": {
      "OC1": 0.812,
      "OC2": 0.805,
      "OC3": 0.863,  # <- OC3削除で信頼性向上
      "OC4": 0.791,
      "OC5": 0.809
    },
    "interpretation": "良好な内的整合性",
    "recommendations": [
      "OC3の削除を検討（項目-全体相関が低い）",
      "OC3削除後のα = 0.863に向上"
    ]
  }
}
```

**解釈の指針**：

**Cronbach's α**：
- α < 0.60：信頼性不足（使用不可）
- 0.60 ≤ α < 0.70：許容可能（探索的研究）
- 0.70 ≤ α < 0.80：許容可能（確認的研究）
- 0.80 ≤ α < 0.90：良好
- α ≥ 0.90：優秀（ただし冗長性に注意）

**項目-全体相関**：
- r < 0.30：項目の除外を強く推奨
- 0.30 ≤ r < 0.50：項目の修正または除外を検討
- r ≥ 0.50：適切

#### B. 収束的妥当性結果（`convergent_validity.json`）

```json
{
  "organizational_capability": {
    "AVE": 0.562,
    "threshold": 0.50,
    "status": "合格",
    "factor_loadings": {
      "OC1": 0.72,
      "OC2": 0.76,
      "OC3": 0.58,
      "OC4": 0.81,
      "OC5": 0.73
    },
    "interpretation": "測定項目は構成概念を適切に捕捉している"
  }
}
```

**解釈の指針**：

**平均分散抽出（AVE: Average Variance Extracted）**：
```
AVE = (Σλ²) / n
ここで、λは因子負荷量、nは項目数
```

- AVE < 0.50：収束的妥当性不足
- AVE ≥ 0.50：収束的妥当性確保

**因子負荷量（λ）**：
- λ < 0.50：項目の除外を検討
- 0.50 ≤ λ < 0.70：許容可能
- λ ≥ 0.70：望ましい（理想的には ≥ 0.70）

#### C. 弁別的妥当性結果（`discriminant_validity.json`）

```json
{
  "fornell_larcker_criterion": {
    "organizational_capability": {
      "sqrt_AVE": 0.750,
      "correlations_with_others": {
        "strategic_orientation": 0.523,
        "firm_performance": 0.612
      },
      "status": "合格（√AVE > すべての相関）"
    },
    "strategic_orientation": {
      "sqrt_AVE": 0.732,
      "correlations_with_others": {
        "organizational_capability": 0.523,
        "firm_performance": 0.581
      },
      "status": "合格"
    }
  },
  "HTMT_ratios": {
    "OC_SO": 0.687,
    "OC_FP": 0.742,
    "SO_FP": 0.698,
    "threshold": 0.85,
    "interpretation": "すべてのHTMT < 0.85 → 弁別的妥当性確保"
  }
}
```

**解釈の指針**：

**Fornell-Larcker基準**：
√AVE（構成概念A）> 相関係数（A, B）

この条件が満たされれば、構成概念AとBは弁別的妥当性を持つ。

**HTMT比率（Heterotrait-Monotrait Ratio）**：
- HTMT < 0.85：弁別的妥当性確保（保守的基準）
- HTMT < 0.90：弁別的妥当性確保（緩和的基準）
- HTMT ≥ 0.90：弁別的妥当性の懸念

#### D. 確認的因子分析（CFA）結果（`cfa_results.json`）

```json
{
  "model_fit_indices": {
    "chi_square": 156.3,
    "df": 87,
    "p_value": 0.0001,
    "CFI": 0.952,
    "TLI": 0.943,
    "RMSEA": 0.048,
    "SRMR": 0.052,
    "interpretation": "良好な適合度"
  },
  "fit_criteria": {
    "CFI": {"value": 0.952, "threshold": ">0.90", "status": "合格"},
    "TLI": {"value": 0.943, "threshold": ">0.90", "status": "合格"},
    "RMSEA": {"value": 0.048, "threshold": "<0.08", "status": "合格"},
    "SRMR": {"value": 0.052, "threshold": "<0.08", "status": "合格"}
  }
}
```

**適合度指標の判断基準**：

| 指標 | 良好 | 許容可能 | 不適切 |
|-----|------|---------|--------|
| CFI | ≥0.95 | 0.90-0.95 | <0.90 |
| TLI | ≥0.95 | 0.90-0.95 | <0.90 |
| RMSEA | ≤0.06 | 0.06-0.08 | >0.08 |
| SRMR | ≤0.08 | 0.08-0.10 | >0.10 |

**χ²検定の解釈**：
- 有意（p < 0.05）：理論モデルとデータの不一致を示唆
- ただし、サンプルサイズが大きい場合、χ²は容易に有意になる
- 実務的には、CFI、TLI、RMSEA、SRMRを重視

### 1.5 トラブルシューティング

#### エラー1: `semopy not available`

**原因**：確認的因子分析（CFA）に必要なパッケージ未インストール

**解決策**：
```bash
pip install semopy --break-system-packages
# または
conda install -c conda-forge semopy
```

#### エラー2: `Negative AVE calculated`

**原因**：因子負荷量が低すぎる項目の存在

**解決策**：
1. 信頼性分析結果を確認
2. 項目-全体相関が低い項目（r < 0.30）を削除
3. 再分析を実施

#### エラー3: `CFA model did not converge`

**原因**：
- 項目数が少なすぎる（< 3項目）
- 多重共線性（項目間の相関が極めて高い）
- 不適切な初期値

**解決策**：
1. 各構成概念に最低3項目を確保
2. 相関係数 > 0.90の項目ペアを確認し、冗長項目を削除
3. `--cfa-method`を変更（ml → gls）

---

## II. 因果推論探索システム（`causal_explorer.py`）

### 2.1 理論的基盤：因果関係の認識論的挑戦

因果推論は、観察データから因果関係を抽出する認識論的挑戦である。David Hume以来、哲学者たちは因果性の本質について議論してきた。Judea Pearl (2009)の因果階層理論、Donald Rubin (1974)の潜在結果枠組みは、この古典的問題への現代的回答である。

**哲学的考察**：
「相関は因果を意味しない」（correlation does not imply causation）——しかし、適切な方法論と理論的洞察により、因果的洞察への接近は可能となる。本システムは、この認識論的挑戦への実践的な道筋を提供する。

### 2.2 基本的な使用方法

#### A. 最小限の実行例（OLS回帰）

```bash
python scripts/causal_explorer.py data/firm_data.csv \
  --treatment "innovation_investment" \
  --outcome "firm_performance" \
  --controls "firm_size,firm_age" \
  --methods "ols" \
  -o ./causal_output
```

**所要時間**：1-2分

#### B. 包括的な実行例（複数手法）

```bash
python scripts/causal_explorer.py data/longitudinal_firm_data.csv \
  --treatment "innovation_investment" \
  --outcome "firm_performance" \
  --controls "firm_size,firm_age,industry_dummies,year_dummies" \
  --methods "ols,iv,psm,did" \
  --iv-instruments "research_subsidy,industry_rd_intensity" \
  --psm-caliper 0.1 \
  --psm-method nearest \
  --did-time-var "year" \
  --did-treatment-time 2018 \
  --output ./comprehensive_causal_analysis \
  --verbose
```

**所要時間**：5-10分（手法数とデータ規模に依存）

### 2.3 パラメータの詳細

#### A. 必須パラメータ

**`--treatment`**：処置変数（独立変数）
- 例：`innovation_investment`、`strategic_alliance`、`ceo_change`

**`--outcome`**：結果変数（従属変数）
- 例：`firm_performance`、`market_share`、`stock_return`

**`--controls`**：統制変数（カンマ区切り）
- 例：`firm_size,firm_age,industry,year`
- 理論的に重要な交絡要因をすべて含める

#### B. 手法別オプション

**OLS回帰（`--methods ols`）**：

追加オプションなし（統制変数のみで実行）

**操作変数法（`--methods iv`）**：

**`--iv-instruments`**（必須）：操作変数（カンマ区切り）
- 要件1：処置変数と相関（関連性：relevance）
- 要件2：結果変数と直接の因果関係なし（外生性：exogeneity）
- 要件3：結果変数への影響は処置変数を介してのみ（排除制約：exclusion restriction）

例：
```bash
--iv-instruments "research_subsidy"
# 政府研究補助金は、イノベーション投資と相関するが、
# 企業業績への直接的影響は限定的
```

**傾向スコアマッチング（`--methods psm`）**：

**`--psm-caliper`**（デフォルト：0.1）：マッチング許容幅
- 0.05：厳密なマッチング（サンプル減少）
- 0.10：標準的
- 0.20：緩やかなマッチング

**`--psm-method`**（デフォルト：nearest）：マッチング手法
- `nearest`：最近傍マッチング
- `kernel`：カーネルマッチング
- `radius`：半径マッチング

**差分の差分法（`--methods did`）**：

**`--did-time-var`**（必須）：時間変数
- 例：`year`、`quarter`

**`--did-treatment-time`**（必須）：処置開始時点
- 例：`2018`（処置群がイノベーション投資を開始した年）

### 2.4 出力結果の解釈

#### A. OLS回帰結果（`ols_results.json`）

```json
{
  "method": "OLS Regression",
  "dependent_var": "firm_performance",
  "treatment_var": "innovation_investment",
  "results": {
    "coefficient": 0.00015,
    "std_error": 0.00003,
    "t_statistic": 5.0,
    "p_value": 0.0001,
    "confidence_interval": [0.00009, 0.00021]
  },
  "model_statistics": {
    "R_squared": 0.423,
    "adj_R_squared": 0.415,
    "F_statistic": 52.3,
    "n_observations": 450
  },
  "interpretation": "イノベーション投資100万円の増加は、ROAを0.015ポイント向上させる",
  "caution": "OLS推定値は、内生性により偏っている可能性がある"
}
```

**注意点**：
OLS係数は、以下のバイアスを含む可能性：
- 逆因果（reverse causality）：高業績企業がイノベーションに投資
- 同時決定（simultaneity）：第三の要因が両者に影響
- 欠落変数バイアス（omitted variable bias）：未測定の交絡要因

#### B. 操作変数法（IV）結果（`iv_results.json`）

```json
{
  "method": "Instrumental Variables (2SLS)",
  "instruments": ["research_subsidy"],
  "first_stage": {
    "F_statistic": 18.5,
    "threshold": 10.0,
    "status": "強い操作変数（F > 10）"
  },
  "second_stage": {
    "coefficient": 0.00012,
    "std_error": 0.00005,
    "t_statistic": 2.4,
    "p_value": 0.017,
    "confidence_interval": [0.00002, 0.00022]
  },
  "hausman_test": {
    "statistic": 3.2,
    "p_value": 0.074,
    "interpretation": "内生性の証拠は弱い（p > 0.05）"
  },
  "interpretation": "内生性を統制した因果効果の推定"
}
```

**解釈の指針**：

**第一段階（First Stage）**：
- F統計量 > 10：強い操作変数
- F統計量 < 10：弱い操作変数（結果を慎重に解釈）

**Hausman検定**：
- p < 0.05：内生性の証拠あり（IV推定が適切）
- p ≥ 0.05：内生性の証拠弱い（OLS推定でも可）

#### C. 傾向スコアマッチング（PSM）結果（`psm_results.json`）

```json
{
  "method": "Propensity Score Matching",
  "matching_quality": {
    "original_sample": 450,
    "matched_sample": 320,
    "common_support": "89.2%のサンプルが共通支持領域内"
  },
  "balance_check": {
    "firm_size": {"before": 0.45, "after": 0.05, "status": "バランス改善"},
    "firm_age": {"before": 0.38, "after": 0.03, "status": "バランス改善"}
  },
  "treatment_effect": {
    "ATT": 0.012,
    "std_error": 0.004,
    "t_statistic": 3.0,
    "p_value": 0.003,
    "interpretation": "処置群のROAは対照群より1.2ポイント高い"
  }
}
```

**解釈の指針**：

**ATT（Average Treatment Effect on the Treated）**：
処置群における平均処置効果。「イノベーション投資を行った企業が、行わなかった場合と比較してどれだけ業績が向上したか」

**バランス・チェック**：
- 標準化差分 < 0.10：良好なバランス
- マッチング後のバランスが改善していることを確認

#### D. 差分の差分法（DiD）結果（`did_results.json`）

```json
{
  "method": "Difference-in-Differences",
  "treatment_time": 2018,
  "parallel_trends_test": {
    "pre_treatment_periods": [2015, 2016, 2017],
    "test_statistic": 0.85,
    "p_value": 0.47,
    "status": "並行トレンド仮定を支持（p > 0.05）"
  },
  "did_estimate": {
    "coefficient": 0.018,
    "std_error": 0.006,
    "t_statistic": 3.0,
    "p_value": 0.003,
    "interpretation": "処置群の業績向上は対照群より1.8ポイント高い"
  }
}
```

**解釈の指針**：

**並行トレンド仮定（Parallel Trends Assumption）**：
- p > 0.05：仮定を支持（DiD推定は妥当）
- p ≤ 0.05：仮定違反の可能性（結果を慎重に解釈）

### 2.5 手法の選択指針

| 手法 | 適用条件 | 主な対処バイアス | 限界 |
|-----|---------|----------------|------|
| OLS | ベースライン | なし | 内生性に脆弱 |
| IV | 強い操作変数が存在 | 内生性全般 | 弱操作変数問題 |
| PSM | 十分な共変量データ | 選択バイアス | 観測不可能な交絡 |
| DiD | パネルデータ、明確な処置時点 | 時間不変交絡 | 並行トレンド仮定 |

**推奨アプローチ**：
複数手法を併用し、結果の頑健性（robustness）を確認する。

---

## III. 理論駆動型探索的データ分析（`theory_driven_eda.py`）

### 3.1 理論的位置づけ

探索的データ分析（EDA）は、John Tukey (1977)の創始以来、データの語る物語を傾聴する帰納的営為として理解されてきた。しかし、真に洞察に富むEDAは、理論的感受性と結びついた時に最大の知的価値を発揮する。

### 3.2 基本的な使用方法（推定）

```bash
python scripts/theory_driven_eda.py data/research_data.csv \
  --theory rbv \
  --key-variables "resources,capabilities,performance" \
  -o ./eda_output
```

**注記**：本スクリプトの詳細な実装は確認中であるが、理論的枠組みに基づく探索的分析を支援するものと推定される。

---

## IV. 構成概念設定例（`example_constructs_config.py`）

### 4.1 使用方法

```bash
python scripts/example_constructs_config.py -o config/
```

**生成される成果物**：
- `config/example_constructs.yaml`：サンプル設定ファイル

### 4.2 カスタマイズ

生成されたYAMLファイルを編集し、自身の研究に適合させる。

---

## V. 統合的ワークフロー例

### 5.1 完全な分析プロセス

**ステップ1：構成概念の妥当性検証**（10分）
```bash
python scripts/construct_validator.py data/survey.csv \
  --constructs-config config/constructs.yaml \
  --validation-level comprehensive \
  -o ./validation
```

**ステップ2：妥当性確認後、データの準備**（5分）
- 信頼性の低い項目を削除
- 修正したデータセットを作成

**ステップ3：因果関係の探索**（10分）
```bash
python scripts/causal_explorer.py data/cleaned_data.csv \
  --treatment "innovation_investment" \
  --outcome "firm_performance" \
  --controls "firm_size,firm_age,industry" \
  --methods "ols,iv,psm" \
  --iv-instruments "research_subsidy" \
  -o ./causal
```

**ステップ4：結果の理論的解釈**（任意時間）
- 複数手法の結果を比較
- 理論的メカニズムの考察
- 参考資料による深化

---

## 結語：実践的知恵の獲得

本ガイドは、実装済みスクリプトの技術的使用方法を提供するが、真の目的はそれを超える。研究者が方法論的厳密性と理論的洞察を統合し、経営現象の本質的理解へと到達すること——それこそが本システムの究極的目標なのである。

技術的ツールは知識創造の手段であり、目的ではない。研究者の理論的感受性、批判的思考、そして現象への深い洞察が、これらのツールと結びついた時、真に価値ある学術的貢献が生まれる。

---

**作成日**：2025年11月8日  
**バージョン**：1.0  
**次回更新予定**：Phase 2完了時

#使用ガイド #実装機能 #構成概念妥当性 #因果推論 #実践的マニュアル
