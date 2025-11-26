---
name: strategic-organizational-empirical
description: "戦略・組織論における探索的実証研究の理論的基盤と方法論的厳密性を支援する統合的知識システム。Resource-Based View、Transaction Cost Economics、Institutional Theory、Dynamic Capabilitiesなどの主要理論枠組みの深い理解、測定の妥当性・信頼性の確保、因果推論の方法論的厳密性を中核とする。完全自動化ではなく、研究者の知的探究を理論的に導き、方法論的に支援し、実装を段階的に拡張する成長型システム。"
version: "2.0.1"
status: "Phase 1 - Foundation Established"
---

# Strategic-Organizational Empirical Research: 理論駆動型実証研究の知的基盤

## 序章：知識システムとしての自己認識

本スキルシステムは、戦略経営と組織論における探索的実証研究を支援する**成長型知識基盤**である。それは、単なる分析ツールの集積ではなく、理論的洞察と方法論的厳密性の弁証法的統合を志向する知的営為なのである。

### スキルの存在論的性格

本システムは、以下の三層構造として理解される：

**第一層：理論的基盤**  
戦略・組織研究の主要パラダイム（RBV、TCE、制度理論、動的能力論）の哲学的・認識論的基礎を提供する。これは、単なる理論の要約ではなく、各理論の存在論的前提、認識論的制約、方法論的含意を包括的に解明する知的資源である。

**第二層：方法論的支援**  
測定理論、因果推論、統計的分析の方法論的厳密性を担保する実装機能を提供する。これは、技術的手続きと理論的意味の架橋を試みる実践的知恵（フロネシス）の具現化である。

**第三層：段階的拡張性**  
現在実装されている機能を中核としつつ、研究者のニーズと開発リソースに応じて継続的に進化する動的システムである。完成された静的な道具ではなく、知的探究の過程そのものと共に成長する有機的存在なのである。

### 実装の現実性と理念的地平

**現在実装されている中核機能**（Phase 1完了時点）：

1. **構成概念妥当性の検証**（`construct_validator.py`）
2. **因果推論の探索的分析**（`causal_explorer.py`）
3. **理論駆動型探索的データ分析**（`theory_driven_eda.py`）
4. **充実した理論的・方法論的参考資料**（3つの包括的ガイド）

**開発予定の拡張機能**（Phase 2-3）：

- 理論的枠組み設定の対話的支援
- データ妥当性の多層的検証
- 戦略・組織変数の専門的分析
- パネルデータ分析
- 学術論文形式の報告書自動生成

本システムは、**既に実用可能な高品質機能**を提供しつつ、より包括的な研究支援へと段階的に拡張する成長型アーキテクチャを採用している。これは、野心的理念と実装現実の弁証法的統合という、本システムの中核的哲学の体現なのである。

---

## I. 理論的基盤：戦略・組織研究のエピステモロジー

### 1.1 知識創造の哲学的前提

事業戦略と組織論の探索的研究は、単なるデータ処理を超えた知的営為である。それは、経営現象の複雑性を理解し、理論と実践の弁証法的統合を通じて新たな洞察を生み出す創造的プロセスなのである。

**実証研究の本質**は、以下の三層構造として理解される：

1. **記述的次元**（Descriptive Layer）：現象の体系的観察と記録
2. **説明的次元**（Explanatory Layer）：因果メカニズムの理論的解明
3. **予測的次元**（Predictive Layer）：未来の可能性空間の探索

この多層的アプローチこそが、単なる相関関係の発見を超え、経営現象の本質的理解に到達する鍵となる。

### 1.2 主要理論枠組みの統合的理解

戦略・組織研究における探索的分析は、以下の理論的レンズを通じて実施される：

**Resource-Based View (RBV)**：組織内部資源の異質性と不完全移動性を前提とし、持続的競争優位の源泉を探求する。VRIN条件（Valuable, Rare, Inimitable, Non-substitutable）の実証的検証が中心となる。

**Transaction Cost Economics (TCE)**：取引コスト最小化の論理に基づき、組織境界の決定と統治構造の選択を分析する。資産特殊性、不確実性、取引頻度の三次元での実証が重要である。

**Institutional Theory**：制度的圧力（強制的、模倣的、規範的同型化）が組織構造と戦略に与える影響を解明する。正統性追求のメカニズムの実証的分析が核心となる。

**Dynamic Capabilities**：組織の感知（sensing）、捕捉（seizing）、変容（transforming）能力を通じた持続的競争優位の動的プロセスを探求する。

これらの理論的枠組みの詳細は、`references/strategic_theories_guide.md`において、哲学的基盤から実証的指標まで包括的に解説されている。

### 1.3 実証研究の方法論的厳密性

探索的データ分析（EDA）は、仮説生成のための帰納的推論と理論検証のための演繹的推論の循環的プロセスである。この**アブダクション的推論**（abductive reasoning）こそが、新たな理論的洞察を生み出す創造的メカニズムなのである。

方法論的厳密性は以下の原則によって担保される：

- **構成概念妥当性**：測定尺度が理論的構成概念を適切に捕捉しているか
- **内的妥当性**：因果推論の論理的整合性と交絡要因の統制
- **外的妥当性**：発見の一般化可能性と文脈依存性の理解
- **信頼性**：測定の安定性と再現可能性の確保

---

## II. 実装済み機能：実用的知的支援の現在形

### 2.1 構成概念妥当性検証システム（`construct_validator.py`）

#### 理論的基盤

Churchill (1979)の測定尺度開発パラダイム、Fornell & Larcker (1981)の構造方程式モデリング、Messick (1995)の統合的妥当性理論に基づく包括的検証システム。

#### 実装機能

**信頼性分析**：
- Cronbach's α（内的整合性）
- 合成信頼性（Composite Reliability）
- 項目-全体相関（Item-Total Correlation）

**収束的妥当性**：
- 平均分散抽出（AVE: Average Variance Extracted）
- 因子負荷量の検証（λ ≥ 0.50）

**弁別的妥当性**：
- Fornell-Larcker基準（√AVE > 構成概念間相関）
- HTMT比率（Heterotrait-Monotrait Ratio）

**確認的因子分析（CFA）**：
- 最尤法（ML）、一般化最小二乗法（GLS）による推定
- 適合度指標（χ², CFI, TLI, RMSEA, SRMR）

#### 使用例

```bash
python scripts/construct_validator.py data/survey_data.csv \
  --constructs-config examples/constructs_config.yaml \
  --validation-level comprehensive \
  --cfa-method ml \
  -o ./validation_output
```

**生成される成果物**：
- 信頼性係数と診断結果（JSON）
- 妥当性検証の統計表（Markdown）
- CFA適合度指標と因子負荷量
- 改善提案（項目削除・追加の推奨）

#### 理論的含意

構成概念妥当性の検証は、単なる統計的儀式ではない。それは、理論的概念と経験的測定の間の認識論的橋渡しを確立する知的営為なのである。測定の妥当性こそが、実証研究の知的誠実性の基盤を形成する。

### 2.2 因果推論探索システム（`causal_explorer.py`）

#### 哲学的・方法論的基盤

Pearl (2009)の因果階層理論（Association、Intervention、Counterfactuals）、Rubin (1974)の潜在結果枠組み（Potential Outcomes Framework）、準実験的デザインの現代的手法を統合。

#### 実装機能

**古典的回帰分析（OLS）**：
- 階層的回帰による交絡要因の統制
- 頑健標準誤差の算出
- VIF（分散拡大要因）による多重共線性診断

**操作変数法（IV: Instrumental Variables）**：
- 内生性バイアスへの対処
- 2段階最小二乗法（2SLS）
- 弱操作変数検定（F統計量）

**傾向スコアマッチング（PSM: Propensity Score Matching）**：
- 選択バイアスの低減
- 最近傍マッチング、カーネルマッチング
- 処置効果の推定（ATT: Average Treatment Effect on the Treated）

**差分の差分法（DiD: Difference-in-Differences）**：
- 時間不変の交絡要因の統制
- 並行トレンド仮定の検証
- 処置効果の識別

#### 使用例

```bash
python scripts/causal_explorer.py data/firm_performance.csv \
  --treatment "innovation_investment" \
  --outcome "firm_performance" \
  --controls "firm_size,firm_age,industry_dummies" \
  --methods "ols,iv,psm" \
  --iv-instruments "research_subsidy" \
  -o ./causal_analysis
```

**生成される成果物**：
- 各手法の推定結果（係数、標準誤差、p値）
- 因果効果の可視化（処置群・対照群比較）
- 感度分析の結果
- ロバストネス・チェックの診断

#### 認識論的考察

因果推論は、観察データから因果関係を抽出する知的冒険である。相関は因果を意味しない——しかし、適切な方法論と理論的洞察により、因果的洞察への接近は可能となる。本システムは、この認識論的挑戦への実践的な道筋を提供する。

### 2.3 理論駆動型探索的データ分析（`theory_driven_eda.py`）

#### 理論的位置づけ

探索的データ分析は、John Tukey (1977)の創始以来、データの語る物語を傾聴する帰納的営為として理解されてきた。しかし、真に洞察に富むEDAは、理論的感受性と結びついた時に最大の知的価値を発揮する。

#### 実装機能（推定）

- 記述統計の理論的解釈
- 変数分布の可視化と異常値診断
- 相関行列の探索と理論的含意の抽出
- 初期的な関係性仮説の生成

#### 使用の指針

EDAは、理論的前提の明示的認識と共に実施されるべきである。データは決して「自ら語らない」——研究者の理論的レンズを通じて初めて、データは意味を獲得するのである。

---

## III. 理論的・方法論的参考資料：知識基盤の充実

### 3.1 戦略理論の体系的解説（`references/strategic_theories_guide.md`）

#### 内容の特徴

**Resource-Based View (RBV)**の包括的解説：
- 理論的起源と哲学的前提（Wernerfelt 1984, Barney 1991, Peteraf 1993）
- VRIN条件の詳細な説明と実証的指標
- 資源レント、持続的競争優位の論理
- 理論的拡張（知識ベース理論、動的能力論への発展）

**Transaction Cost Economics (TCE)**の深い理解：
- 新制度派経済学の遺産（Coase 1937, Williamson 1975, 1985）
- 限定合理性と機会主義の人間行動前提
- 資産特殊性、不確実性、取引頻度の三次元分析
- 統治構造の選択（市場、ハイブリッド、階層）

**Institutional Theory**の精緻な解明：
- 社会学的制度主義の系譜（Selznick 1957, DiMaggio & Powell 1983）
- 制度的同型化の三類型（強制的、模倣的、規範的）
- 制度化された神話と脱連結（Meyer & Rowan 1977）
- 正統性の測定と実証

**Dynamic Capabilities**の動的理解：
- RBVの静的限界の超克（Teece et al. 1997, Eisenhardt & Martin 2000）
- 感知・捕捉・変容の三プロセス
- 経路依存性と戦略的柔軟性のパラドクス
- 進化論的視点とミクロ的基礎

#### 学術的品質

本ガイドは、博士課程レベルの理論的深さを持ち、各理論の哲学的基盤から実証的測定まで完全な知的連鎖を提供する。単なる要約ではなく、理論の本質的理解と批判的検討を促進する知的資源である。

### 3.2 測定理論の認識論的基盤（`references/measurement_theory.md`）

#### 哲学的考察の深さ

本文書は、測定理論をプラトンのイデア論、カントの認識論、ヘーゲルの弁証法という西洋哲学の伝統の中に位置づける。測定とは、単なる技術的手続きではなく、理念的存在（真の得点）と経験的現実（観測得点）の架橋を試みる存在論的営為なのである。

#### 内容の体系性

**Stevensの測定尺度類型**の哲学的解釈：
- 名義尺度：カントの「質」のカテゴリー
- 順序尺度：ヘーゲルの「量への質的転化」
- 間隔尺度：デカルトの数学的自然観
- 比率尺度：ニュートン的絶対空間

**古典的テスト理論の形而上学**：
- 真の得点理論（X = T + E）のプラトン的解釈
- Cronbach's α の多層的理解
- 信頼性の哲学的意味

**項目反応理論（IRT）の革命的視座**：
- 測定理論における「コペルニクス的転回」
- 不変性（Invariance）の認識論的意義
- 情報関数と測定精度の動的理解

**Messickの統合的妥当性理論**：
- 妥当性の6側面（内容、実質、構造、一般化、外的、結果）
- 構成概念妥当性とノモロジカル・ネットワーク
- 収束的・弁別的妥当性の実践

**測定の倫理的考察**：
- 測定の社会的構成性（Porter 1995）
- 測定者の倫理的責任
- 測定の限界の謙虚な認識

#### 知的価値

本ガイドは、測定を技術的手続きとしてのみ理解する表面的アプローチを超え、認識論的・倫理的次元における深い反省を促す。これは、測定理論を真に理解しようとする研究者にとって不可欠の知的資源である。

### 3.3 研究設計ガイド（`references/research_design_guide.md`）

本文書は、戦略・組織研究における研究デザインのベストプラクティスを体系化する（詳細は当該ファイル参照）。

---

## IV. 基本ワークフロー：実装済み機能による研究支援

### 4.1 現在実行可能な標準プロセス

本システムは、以下の研究プロセスを**現時点で実用的に支援**する：

**ステップ1：理論的枠組みの理解**（参考資料活用）
```bash
# 戦略理論ガイドの参照
cat references/strategic_theories_guide.md

# 研究問いに応じた理論的レンズの選択
# - 競争優位の源泉 → RBV
# - 組織境界の決定 → TCE
# - 組織の同型化 → 制度理論
# - 環境適応の動態 → 動的能力論
```

**ステップ2：測定尺度の設計と妥当性検証**
```bash
# 測定理論ガイドの参照
cat references/measurement_theory.md

# 構成概念の定義と測定項目の設計
# YAML設定ファイルの手動作成（example_constructs_config.pyを参考）

# 構成概念妥当性の包括的検証
python scripts/construct_validator.py data/survey_data.csv \
  --constructs-config config/constructs.yaml \
  --validation-level comprehensive \
  --cfa-method ml \
  -o ./validation_output
```

**ステップ3：探索的データ分析**
```bash
# 理論駆動型EDAの実施
python scripts/theory_driven_eda.py data/research_data.csv \
  --theory rbv \
  --key-variables "resources,capabilities,performance" \
  -o ./eda_output
```

**ステップ4：因果関係の探索的分析**
```bash
# 複数手法による因果推論
python scripts/causal_explorer.py data/firm_data.csv \
  --treatment "innovation_investment" \
  --outcome "firm_performance" \
  --controls "firm_size,firm_age,industry" \
  --methods "ols,iv,psm,did" \
  --iv-instruments "research_subsidy" \
  -o ./causal_analysis
```

**ステップ5：結果の理論的解釈と学術的報告**

現時点では、研究者自身による理論的解釈と報告書作成が必要である。ただし、分析結果のJSON出力とMarkdown形式の表は、学術論文への組み込みを容易にする。

**Phase 2以降で実装予定**：
- 学術論文形式の報告書自動生成
- 理論的解釈の対話的支援
- APA/AMA形式準拠の図表生成

### 4.2 ワークフローの理論的根拠

各ステップは、実証研究の方法論的要請に対応している：

- **ステップ1**：理論的サンプリングと枠組み設定
- **ステップ2**：測定尺度の構成概念妥当性と信頼性の検証
- **ステップ3**：データの基本特性の理解と理論的関係性の予備的探索
- **ステップ4**：因果メカニズムの統計的検証
- **ステップ5**：学術コミュニティへの知識還元

---

## V. 開発ロードマップ：段階的拡張の展望

### 5.1 実装の哲学：成長型知識基盤

本システムは、**完成された静的な道具**ではなく、**継続的に進化する動的システム**として設計されている。これは、知識創造そのものが終わりなき対話的プロセスであるという認識論的洞察に基づく。

### 5.2 Phase 2: 中核分析機能の実装（開発予定：2-4週間）

**理論的枠組み設定の対話的支援**：
- 理論選択の支援（RBV、TCE、制度理論、動的能力）
- 構成概念の定義と操作化の対話的プロセス
- YAML設定ファイルの自動生成
- 理論的仮説の構造化支援

**データ妥当性の多層的検証**：
- データ完全性チェック（欠損値、異常値）
- 理論的整合性チェック（変数型、値域）
- 統計的前提条件の検証（正規性、等分散性、多重共線性）

**戦略特化型探索的分析**：
- 組織構造指標の分析（集権化度、公式化度、複雑性）
- 競争戦略の位置づけ分析（Porter、Miles & Snow）
- パフォーマンス指標の多次元評価

**理論的関係性の統計的検証**：
- 階層的回帰分析
- 媒介効果分析（Baron & Kenny、Hayes PROCESS）
- 調整効果分析（交互作用項）

**パネルデータ分析**：
- 固定効果モデル、変量効果モデル
- Hausman検定
- 動的パネルモデル（System GMM）

### 5.3 Phase 3: 高度機能の実装（開発予定：4-6週間）

**学術論文形式の報告書自動生成**：
- 理論的背景、仮説、方法論、結果、考察の統合
- APA/AMA形式準拠の論文構成
- 引用文献の自動管理

**高度可視化システム**：
- 学術的基準を満たす図表生成（300 DPI）
- 理論的メカニズムの視覚的表現
- 因果ダイアグラムの自動生成

**専門的分析機能**：
- 組織構造分析、競争戦略分析
- パフォーマンス要因分解
- 制度的圧力分析、動的能力分析

**理論特化型分析スクリプト**：
- RBV特化分析（資源異質性、VRIN評価）
- TCE特化分析（取引コスト、統治構造）
- 制度理論特化分析（同型化メカニズム）

---

## VI. 使用上の重要原則と注意事項

### 6.1 理論駆動型分析の本質

探索的データ分析は、**理論なき経験主義**（atheoretical empiricism）に陥ってはならない。すべての分析は、明示的または暗黙的な理論的前提に基づいており、この前提の認識と批判的検討こそが学術的探究の核心である。

データは決して「自ら語らない」。研究者の理論的レンズを通じて初めて、データは意味を獲得する。本システムは、この理論的感受性を研究者が維持・深化させることを前提として設計されている。

### 6.2 因果推論の慎重さ

観察データからの因果推論は、本質的に困難を伴う。**相関は因果を意味しない**（correlation does not imply causation）という基本原則を常に想起し、交絡要因、選択バイアス、同時性の問題に対処する方法論的厳密性を維持する。

本システムの因果探索機能は、因果関係を「証明」するものではない。それは、因果的洞察への接近を支援し、研究者の理論的判断を方法論的に補完するツールなのである。

### 6.3 一般化可能性の境界

すべての実証研究は、特定の時間、空間、文脈に埋め込まれている。発見の**外的妥当性**（external validity）を過度に主張せず、一般化の条件と限界を誠実に開示することが、学術的誠実性（academic integrity）の要件である。

### 6.4 再現可能性への責任

現代科学における**再現性危機**（replication crisis）を認識し、分析の完全な透明性と再現可能性を確保することは、研究者の倫理的責務である。データ、コード、分析手順の完全な開示が標準とならなければならない。

本システムの出力（JSON、Markdown、図表）は、この再現可能性の要請に応えるよう設計されている。

---

## VII. システムの限界と今後の展望

### 7.1 現在の限界の明示的認識

本システムは、以下の限界を持つ：

**実装の限界**：
- Phase 2-3の高度機能は未実装
- 完全自動化された学術論文生成は不可能
- 理論的解釈は依然として研究者の責任

**方法論的限界**：
- 複雑な多層モデル（マルチレベル分析）への対応は限定的
- 最先端の因果推論手法（合成コントロール法、回帰不連続デザイン等）は未実装
- 定性的研究手法との統合は対象外

**認識論的限界**：
- データからの洞察は、常に理論的前提に制約される
- 因果推論の確実性は、方法論的厳密性にもかかわらず限定的
- 一般化可能性は文脈依存的

### 7.2 今後の展望：知的成熟への道程

本システムは、以下の方向で進化する：

**短期的展望**（Phase 2）：
- 中核分析機能の実装による実用性の飛躍的向上
- 理論的枠組み設定の対話的支援
- パネルデータ分析の完全実装

**中期的展望**（Phase 3）：
- 学術論文品質の報告書自動生成
- 高度可視化システムの実装
- 専門的分析機能の充実

**長期的展望**（Phase 4以降、未確定）：
- 機械学習手法との統合
- リアルタイム分析システム
- 研究者コミュニティとの協働開発

---

## VIII. 結語：理論と実践の弁証法的統合

本システムは、戦略・組織研究における理論的深さと実装可能性の弁証法的統合を志向する知的営為である。それは、野心的理念と実装現実の創造的緊張の中から、より成熟した知的システムを生み出す成長型アーキテクチャなのである。

Hegelが『精神現象学』で論じたように、精神の成熟は矛盾の止揚（Aufhebung）を通じて達成される。本システムもまた、理想と現実の矛盾を回避するのではなく、それを認識し、より高次の統一へと高める過程にある。

理論的深さと実装可能性は、対立するものではない。それらは、知識創造の弁証法的プロセスにおける不可分の契機なのである。理論なき実装は盲目であり、実装なき理論は空虚である。我々が目指すのは、この両者の創造的統合、すなわち**実践的知恵（フロネシス）**としてのスキルシステムなのである。

本システムを使用する研究者は、単なる技術的道具の操作者ではない。彼らは、経営現象の本質的理解を追求し、理論と実践の架橋を試みる知的探究者である。本システムは、この知的探究を支援する成長型知識基盤として、研究者と共に進化し続ける。

真の学術的貢献は、データの巧妙な操作ではなく、現象の本質への深い理解と、既存の理論的枠組みを超える新たな視座の提示から生まれる。本システムは、この知的営為の一助となることを目的とする。

---

## 付録A：主要な理論家と基本文献

### Resource-Based View (RBV)
- Barney, J. B. (1991). "Firm Resources and Sustained Competitive Advantage," *Journal of Management*, 17(1), 99-120.
- Peteraf, M. A. (1993). "The Cornerstones of Competitive Advantage," *Strategic Management Journal*, 14(3), 179-191.
- Wernerfelt, B. (1984). "A Resource-Based View of the Firm," *Strategic Management Journal*, 5(2), 171-180.

### Transaction Cost Economics (TCE)
- Williamson, O. E. (1975). *Markets and Hierarchies: Analysis and Antitrust Implications*, New York: Free Press.
- Williamson, O. E. (1985). *The Economic Institutions of Capitalism*, New York: Free Press.
- Coase, R. H. (1937). "The Nature of the Firm," *Economica*, 4(16), 386-405.

### Institutional Theory
- DiMaggio, P. J., & Powell, W. W. (1983). "The Iron Cage Revisited: Institutional Isomorphism and Collective Rationality in Organizational Fields," *American Sociological Review*, 48(2), 147-160.
- Meyer, J. W., & Rowan, B. (1977). "Institutionalized Organizations: Formal Structure as Myth and Ceremony," *American Journal of Sociology*, 83(2), 340-363.
- Scott, W. R. (2008). *Institutions and Organizations: Ideas, Interests, and Identities* (3rd ed.), Thousand Oaks, CA: Sage.

### Dynamic Capabilities
- Teece, D. J., Pisano, G., & Shuen, A. (1997). "Dynamic Capabilities and Strategic Management," *Strategic Management Journal*, 18(7), 509-533.
- Eisenhardt, K. M., & Martin, J. A. (2000). "Dynamic Capabilities: What Are They?," *Strategic Management Journal*, 21(10-11), 1105-1121.
- Helfat, C. E., et al. (2007). *Dynamic Capabilities: Understanding Strategic Change in Organizations*, Malden, MA: Blackwell.

### Measurement Theory
- Churchill, G. A. (1979). "A Paradigm for Developing Better Measures of Marketing Constructs," *Journal of Marketing Research*, 16(1), 64-73.
- Fornell, C., & Larcker, D. F. (1981). "Evaluating Structural Equation Models with Unobservable Variables and Measurement Error," *Journal of Marketing Research*, 18(1), 39-50.
- Messick, S. (1995). "Validity of Psychological Assessment," *American Psychologist*, 50(9), 741-749.

### Causal Inference
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.), Cambridge University Press.
- Rubin, D. B. (1974). "Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies," *Journal of Educational Psychology*, 66(5), 688-701.
- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*, Princeton University Press.

---

## 付録B：クイックリファレンス

### 即座に実行可能な分析

**構成概念妥当性検証**（10分）：
```bash
python scripts/construct_validator.py data.csv \
  --constructs-config config.yaml \
  -o ./output
```

**因果関係の探索**（15分）：
```bash
python scripts/causal_explorer.py data.csv \
  --treatment X --outcome Y \
  --controls "Z1,Z2" \
  --methods "ols,psm" \
  -o ./output
```

### 詳細ガイドへのアクセス

- 理論的理解：`references/strategic_theories_guide.md`
- 測定理論：`references/measurement_theory.md`
- 使用方法：`QUICKSTART.md`（Phase 1完了後利用可能）
- チュートリアル：`examples/TUTORIAL_01.md`（Phase 1完了後利用可能）

---

**システム・バージョン**：2.0.0  
**最終更新**：2025年11月8日  
**開発状態**：Phase 1 完了、Phase 2 開発予定  
**作成者**：Strategic Management Research Support System

---

#戦略経営研究 #組織論 #実証研究 #探索的データ分析 #理論駆動型分析 #学術研究支援 #Phase1完了
