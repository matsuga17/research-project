# Phase 1実装ガイド：基礎的統合の確立

**期間**: 1-2ヶ月（8週間）  
**総工数**: 76時間（外部ツール40時間、内部スキル36時間）  
**目標**: 理論構築の全プロセスを経験し、基本的な外部-内部統合を実現

---

## 実装の哲学的原理

Phase 1の本質は、「理解（understanding）」から「実践（practice）」への移行である。理論的知識を単に「知る」のではなく、それを自分の研究文脈に「適用」し、その過程で生じる認知的緊張を「統合」する――この三段階のプロセスを通じて、真の理論的感受性（theoretical sensitivity）が育まれる。

---

## Week 1-2：理論的基盤の習得

### 目標
3大方法論（Eisenhardt、Gioia、Glaser-Strauss）の認識論的差異を理解し、自分の研究に最適なアプローチを理論的根拠とともに選択できるようになる。

### 実施内容

#### Day 1-3：Eisenhardt (1989) 精読（8時間）

**Step 1：初回精読（3時間）**
- 論文全体を通読し、8ステッププロセスの全体像を把握
- 各ステップの目的と方法をメモ
- 実例（コンピュータ企業の戦略研究）の分析プロセスを追跡

**Step 2：批判的再読（3時間）**
- 認識論的前提を特定：
  - 実証主義的アプローチとは何か？
  - 「検証可能な命題」とは何を意味するか？
  - 理論的サンプリングの論理は？
- 限界と批判を文献から収集（後続研究での批判的議論）

**Step 3：自己研究への適用思考実験（2時間）**
- 自分の研究テーマに8ステップを当てはめたらどうなるか？
- どのステップが最も困難か？なぜか？
- このアプローチの適合性を評価

**成果物**：
- `eisenhardt_analysis.md`：分析メモ（1,000-1,500字）

#### Day 4-6：Gioia et al. (2013) 精読（6時間）

**Step 1：初回精読（2時間）**
- Gioiaアプローチの中核概念を理解：
  - 1st order concepts（インフォーマント中心）
  - 2nd order themes（研究者の理論的解釈）
  - Aggregate dimensions（高次抽象化）
- データ構造図（data structure）の読み方を学習

**Step 2：実例分析（2時間）**
- 論文中の具体例（identity change研究等）を詳細分析
- 1st → 2nd → Aggregate の抽象化プロセスを追跡
- データ構造図の作成方法を理解

**Step 3：Eisenhardtとの比較（2時間）**
- 両アプローチの哲学的差異を明確化
- どのような研究質問に各々が適しているか？
- 統合的活用の可能性を探索

**成果物**：
- `gioia_analysis.md`：分析メモ（1,000-1,500字）

#### Day 7-9：Glaser & Strauss (1967) 精読（4時間）

**注意**：この古典は読みにくいため、以下の補助文献も併用を推奨：
- Charmaz (2006): "Constructing Grounded Theory"（より実践的）
- Corbin & Strauss (2014): "Basics of Qualitative Research"（手順書的）

**Step 1：中核概念の理解（2時間）**
- 理論的感受性（theoretical sensitivity）とは？
- 理論的サンプリングと理論的飽和の論理
- オープン→アクシャル→選択的コーディングの段階

**Step 2：3アプローチの統合比較（2時間）**
- 比較表の作成（添付のテンプレート使用）
- 各アプローチが生成する理論の性質の違い
- 自分の研究に最適なアプローチの暫定選択

**成果物**：
- `three_approaches_comparison.md`：比較表（1,500-2,000字）

#### Day 10-14：統合レポート執筆（6時間）

**レポート構成**：

1. **序論**（500字）
   - 探索的理論構築における方法論選択の重要性
   - 本レポートの目的

2. **3大アプローチの比較分析**（1,000字）
   - 認識論的前提の違い
   - 理論の性質（命題 vs 概念枠組み vs プロセス理論）
   - データ分析手法の違い

3. **自己研究への適用**（500字）
   - 研究質問の性質分析
   - 最適アプローチの選択と理由
   - 予想される困難とその対応策

4. **結論**（300字）
   - Week 1-2で得られた洞察
   - 次のステップ（Week 3-4）への準備

**成果物**：
- `phase1_week1-2_methodology_comparison.md`：統合レポート（2,000-3,000字）

### 評価基準

- [ ] Eisenhardt、Gioia、Glaser-Straussの哲学的差異を説明できる
- [ ] 各アプローチが生成する理論の性質の違いを理解している
- [ ] 自分の研究に最適なアプローチを理論的根拠とともに選択できる
- [ ] 統合レポート（2,000-3,000字）が完成している

---

## Week 3-4：基本ツールのセットアップと初歩的活用

### 目標
研究の再現性を確保するための基本ツール（Git、Python/R、DoWhy）をセットアップし、因果推論の基礎を習得する。

### 実施内容

#### Day 15-16：Git/GitHub基本（4時間）

**前提知識**：なし（完全初心者から開始可能）

**Step 1：Git基礎理解（1時間）**
- バージョン管理の概念と重要性
- Git vs GitHub の違い
- 基本用語：repository、commit、branch、merge

**学習リソース**：
- Git公式チュートリアル：https://git-scm.com/book/ja/v2
- GitHub Learning Lab：https://lab.github.com/

**Step 2：環境セットアップ（1時間）**
```bash
# Gitインストール確認
git --version

# 初期設定
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# GitHubアカウント作成（まだの場合）
# https://github.com
```

**Step 3：研究リポジトリ作成（2時間）**
```bash
# ローカルリポジトリ作成
mkdir ~/research-project
cd ~/research-project
git init

# 基本構造作成
mkdir -p literature/{papers,notes}
mkdir -p data/{raw,processed,codebooks}
mkdir -p analysis/{notebooks,scripts,results}
mkdir -p theory/{hypotheses,frameworks,models}
mkdir -p writing/{drafts,figures,tables}

# README作成
echo "# My Research Project" > README.md
echo "## Purpose" >> README.md
echo "Exploratory theory building in strategic management" >> README.md

# 初回コミット
git add .
git commit -m "Initial project structure"

# GitHubリモートリポジトリ作成と接続
# （GitHub上で新しいリポジトリを作成後）
git remote add origin https://github.com/yourusername/research-project.git
git push -u origin main
```

**成果物**：
- Git管理された研究リポジトリ
- `README.md`：プロジェクト概要

#### Day 17-20：Python/R環境構築（6時間）

**選択基準**：
- Python推奨：因果推論（DoWhy、EconML）、機械学習統合
- R推奨：SEM（lavaan）、伝統的統計、学術的正統性

**理想**：両方習得し、タスクに応じて使い分け

**Python環境構築（3時間）**：

```bash
# Miniconda/Anacondaインストール（まだの場合）
# https://docs.conda.io/en/latest/miniconda.html

# 仮想環境作成
conda create -n theory_building python=3.10
conda activate theory_building

# 基本パッケージインストール
pip install jupyter numpy pandas matplotlib seaborn
pip install scikit-learn statsmodels scipy

# 因果推論ライブラリ
pip install dowhy econml causalml

# 環境のエクスポート（再現性確保）
conda env export > environment.yml

# Git管理下に追加
git add environment.yml
git commit -m "Add Python environment configuration"
```

**R環境構築（3時間）**（オプション）：

```r
# renvで環境管理
install.packages("renv")
renv::init()

# 基本パッケージ
install.packages(c("tidyverse", "ggplot2"))
install.packages(c("lavaan", "semTools", "semPlot"))

# スナップショット作成
renv::snapshot()

# Git管理下に追加
# renv.lock ファイルが自動生成される
```

**Step 3：Jupyter Notebook / R Markdown セットアップ（1時間）**

```bash
# Jupyter起動確認
jupyter notebook

# 初回ノートブック作成
# analysis/notebooks/00_setup_test.ipynb
```

**成果物**：
- `environment.yml`（Python）または`renv.lock`（R）
- `analysis/notebooks/00_setup_test.ipynb`：環境テスト

#### Day 21-28：DoWhy入門（8時間）

**前提知識**：Python基礎、因果推論の概念（学習しながら習得）

**Step 1：因果推論の基礎理解（2時間）**

**必読資料**：
- Pearl, J. (2009). "Causality: Models, Reasoning, and Inference"（第1章のみ）
- Hernán & Robins (2020). "Causal Inference: What If"（無料公開）

**中核概念**：
- 因果推論 vs 相関分析
- 交絡因子（confounders）の問題
- do演算子と介入（intervention）
- 因果グラフ（DAG: Directed Acyclic Graph）

**Step 2：DoWhy公式チュートリアル（4時間）**

**実施順序**：
1. DoWhyの4ステッププロセス理解
   - Model: 因果仮定をグラフで表現
   - Identify: 因果効果が識別可能か判定
   - Estimate: 因果効果を推定
   - Refute: 反駁テストで頑健性確認

2. lalonde datasetでの実践
```python
import dowhy
from dowhy import CausalModel
import pandas as pd

# データ読み込み（DoWhy付属のlalonde dataset）
data = dowhy.datasets.linear_dataset(
    beta=10,
    num_common_causes=5,
    num_instruments=2,
    num_samples=10000
)

# 因果モデル構築
model = CausalModel(
    data=data["df"],
    treatment=data["treatment_name"],
    outcome=data["outcome_name"],
    common_causes=data["common_causes_names"]
)

# グラフ可視化
model.view_model()

# 因果効果の識別
identified_estimand = model.identify_effect()

# 因果効果の推定
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_matching"
)
print(estimate)

# 反駁テスト
refute_results = model.refute_estimate(
    identified_estimand,
    estimate,
    method_name="random_common_cause"
)
print(refute_results)
```

3. 自分のデータへの適用準備
   - 研究テーマの因果関係を因果グラフで表現
   - 潜在的交絡因子をリストアップ

**Step 3：因果推論実践ノートブック作成（2時間）**

**ノートブック構成**：
1. 研究背景と因果質問の明確化
2. 因果グラフの構築と可視化
3. DoWhyでの因果効果推定
4. 反駁テストによる頑健性確認
5. 理論的解釈と次のステップ

**成果物**：
- `analysis/notebooks/01_dowhy_practice.ipynb`：DoWhy実践ノートブック
- 因果グラフ図（.png形式で保存）

### Week 3-4完了時の統合実践

**Git管理の習慣化**：
```bash
# 毎日の作業後にコミット
git add .
git commit -m "Day XX: [作業内容の簡潔な説明]"
git push origin main
```

**理論的メモの記録**：
各ツール使用時に、以下を記録：
- なぜこのツール/手法を選んだか？
- 他にどんな選択肢があったか？
- この選択の理論的・方法論的根拠は？

**成果物の完全性チェック**：
- [ ] Gitリポジトリが適切に構造化されている
- [ ] Python/R環境が再現可能な形で記録されている
- [ ] DoWhy実践ノートブックが完成している
- [ ] 毎日のコミット履歴が存在する

---

## Week 5-6：複数競合仮説生成の実践

### 目標
自分の研究テーマについて、複数の理論レンズから3-5つの競合仮説を生成し、文献レビューを通じて理論的ギャップを特定する。

### 実施内容

#### Day 29-30：Zotero導入と文献管理（2時間）

**Step 1：Zoteroセットアップ（30分）**
- Zotero本体とブラウザ拡張機能のインストール
- Zoteroアカウント作成（クラウド同期用）
- Better BibTeX for Zoteroプラグイン導入（BibTeX出力用）

**ダウンロード**：
- Zotero：https://www.zotero.org/
- Better BibTeX：https://retorque.re/zotero-better-bibtex/

**Step 2：文献管理の基本操作（1時間）**
- 論文のインポート（PDF、DOI、Webページから）
- コレクションとタグの整理
- メモとアノテーション機能
- BibTeX形式でのエクスポート

**Step 3：Git統合（30分）**
```bash
# Zoteroライブラリをエクスポート
# File → Export Library → Better BibTeX
# literature/references.bib に保存

git add literature/references.bib
git commit -m "Add Zotero bibliography"
```

#### Day 31-45：文献レビュー（20時間）

**目標文献数**：10-15本（精読）+ 30-50本（斜め読み）

**検索戦略**：

**Step 1：キーワード設定（1時間）**
研究テーマから抽出：
- 核心概念（例：digital transformation, competitive advantage）
- 理論的視点（例：resource-based view, dynamic capabilities）
- 文脈（例：manufacturing firms, emerging economies）

**検索式例**：
```
("digital transformation" OR "digitalization")
AND ("competitive advantage" OR "sustained competitive advantage")
AND ("resource-based view" OR "dynamic capabilities")
AND ("2015" OR "2016" OR ... OR "2025")
```

**Step 2：データベース検索（3時間）**
推奨データベース：
- ABI/INFORM（ビジネス研究）
- JSTOR（学際的）
- Web of Science（引用追跡）
- Scopus（引用追跡）
- Google Scholar（補完的）

**検索順序**：
1. Backward search：セミナル論文から引用文献を遡る
2. Forward search：Google Scholarで被引用論文を追跡
3. 系統的検索：複数データベースでの網羅的検索

**Step 3：文献選別（2時間）**
選別基準：
- 研究質問との関連性（高・中・低）
- 理論的貢献度（概念開発、理論検証、実証分析）
- 方法論的厳密性（査読誌、引用数）
- 出版時期（最新研究を優先、ただし古典も含む）

**Step 4：文献精読とメモ作成（14時間）**

**1論文あたり1-1.5時間**を目安：
- 30分：初回精読（全体像把握）
- 30分：批判的再読（理論的貢献の特定）
- 30分：メモ作成とZoteroへの記録

**メモの構造**（Zoteroのノート機能を使用）：
1. **研究質問**：著者は何を問うているか？
2. **理論的視点**：どの理論レンズを採用しているか？
3. **主要命題・発見**：中核的な主張は何か？
4. **方法論**：どのようにデータを収集・分析したか？
5. **理論的貢献**：既存知識に何を付加したか？
6. **限界**：著者自身が認める限界は？批判的に見た限界は？
7. **自己研究への示唆**：この研究から何を学べるか？

#### Day 46-49：文献レビュー表の作成（4時間）

**Step 1：Excel/Notionでの表作成（2時間）**

**列構成**：
- 著者（年）
- 論文タイトル
- 掲載誌
- 理論レンズ
- 研究質問
- 方法論（定性/定量/混合）
- 主要発見
- 理論的貢献
- 限界
- 引用数
- 自己研究との関連性（高/中/低）

**Step 2：理論的パターンの発見（2時間）**
表を作成後、以下を分析：
- どの理論レンズが最も頻繁に使用されているか？
- 研究間で矛盾する発見はあるか？
- 未検討の理論的組み合わせはあるか？
- 境界条件が不明確なテーマはあるか？

**理論的ギャップの類型**：
1. **未探索現象**：新しい現象で既存理論が未適用
2. **理論的矛盾**：研究間で結論が不一致
3. **境界条件不明**：理論の適用範囲が不明確
4. **メカニズム不明**：「なぜ・どのように」が未解明

**成果物**：
- `literature/review_matrix.xlsx`：文献レビュー表
- `literature/theoretical_gaps.md`：理論的ギャップのメモ（1,000字）

#### Day 50-56：複数競合仮説の生成（6時間）

**Step 1：理論レンズの選択（1時間）**

自分の研究テーマに適用可能な4-5つの理論レンズを選択：
- Resource-Based View (RBV)
- Transaction Cost Economics (TCE)
- Institutional Theory
- Dynamic Capabilities
- Agency Theory
- Organizational Learning Theory
- など

**選択基準**：
- 研究質問との理論的適合性
- 既存文献での使用頻度
- 説明力の潜在性

**Step 2：各レンズからの仮説生成（3時間）**

**仮説生成テンプレート**（各レンズごとに）：

```markdown
### 説明X（理論レンズ名）

**中核的主張**：
[1-2文で、このレンズから見た現象の本質的説明]

**因果メカニズム**：
[A → B → C という因果の連鎖を明示]

**キー概念**：
- 概念1：[定義]
- 概念2：[定義]

**予測（検証可能な命題）**：
1. もし～ならば、～が観察されるはずである
2. ～の条件下では、～の効果が強まるはずである

**境界条件**：
- この説明が適用される状況：～
- 適用されない状況：～

**理論的品質評価**：
- Testability（検証可能性）：★★★★☆
- Explanatory Power（説明力）：★★★★★
- Parsimony（簡潔性）：★★★☆☆
- Consistency（整合性）：★★★★☆
- Novelty（新規性）：★★★☆☆

**既存研究との関係**：
- この説明を支持する研究：[著者, 年]
- 矛盾する研究：[著者, 年]
```

**Step 3：統合的枠組みの構築（2時間）**

複数の競合説明を統合：
1. 各説明の強みと限界を比較
2. 相互補完的な側面を特定
3. 適用境界条件を明確化
4. 統合的理論枠組みの提案

**統合的枠組みの例**：
```markdown
### 統合的理論枠組み

**基本命題**：
デジタル変革の成否は、初期段階では制度的圧力（Institutional Theory）が
支配的だが、成熟段階では企業固有の能力（RBV）と動的能力が重要になる。
ただし、産業の不確実性が高い場合、全段階で動的能力の影響が大きい。

**理論的貢献**：
既存研究の多くは単一の理論レンズを採用しているが、本枠組みは複数レンズの
統合により、状況依存的な理論モデルを提供する。

**境界条件マトリクス**：

| 段階/不確実性 | 低不確実性 | 高不確実性 |
|--------------|-----------|-----------|
| 初期段階 | 制度理論 | 制度理論 + 動的能力 |
| 成熟段階 | RBV | RBV + 動的能力 |
```

**成果物**：
- `theory/hypotheses/competing_hypotheses.md`：複数競合仮説（3,000-5,000字）

### Week 5-6完了時の評価基準

- [ ] 10-15本の文献を精読し、文献レビュー表を作成した
- [ ] 理論的ギャップを4類型（未探索、矛盾、境界不明、メカニズム不明）から特定できた
- [ ] 3-5つの競合仮説を異なる理論レンズから生成できた
- [ ] 各仮説の理論的品質を5基準で評価できた
- [ ] 統合的理論枠組みを提案できた

---

## Week 7-8：最初の理論的枠組み構築

### 目標
Claudeとの対話的理論開発を通じて、複数競合仮説を統合的理論枠組みへと昇華させ、視覚的な理論モデルを作成する。

### 実施内容

#### Day 57-60：Claudeとの対話的理論開発（8時間）

**対話セッション1：理解（Understanding）（2時間）**

**目的**：研究者の暗黙的前提を顕在化し、理論的視点を明確化

**対話プロンプト例**：
```
私の研究テーマは「[テーマ]」です。Week 5-6で以下の複数競合仮説を
生成しました：

【仮説1（RBV視点）】：[要約]
【仮説2（TCE視点）】：[要約]
【仮説3（制度理論視点）】：[要約]
【仮説4（動的能力視点）】：[要約]

以下の点について、批判的質問をしてください：
1. どの仮説が最も説得力があると思いますか？なぜですか？
2. 各仮説の理論的前提は何ですか？
3. 仮説間の矛盾点はありますか？
4. この現象の本質的特徴は何だと思いますか？
```

**記録すべき内容**：
- Claudeからの質問とそれに対する自分の回答
- 質問を通じて顕在化した暗黙的前提
- 自分が見落としていた視点

**対話セッション2：発散（Divergent Exploration）（3時間）**

**目的**：固定観念を打破し、新規な理論的視点を生成

**対話プロンプト例**：
```
私の仮説を以下の創造的技法で再解釈してください：

1. 学際的類推：この現象は他の学問分野（生物学、物理学、心理学など）の
   どのような概念に似ていますか？

2. 前提の反転：もし主要な前提（例：「資源は稀少である」）を逆転させたら、
   理論はどう変わりますか？

3. スケールシフト：個人レベルの現象を組織レベル、または産業レベルに
   拡張したらどうなりますか？

4. 理論的融合：2つの異なる理論（例：RBVと制度理論）を統合したら、
   どのような新しい洞察が得られますか？
```

**記録すべき内容**：
- 各創造的技法から得られた新しいアイデア
- 特に印象的だった類推や視点転換
- 既存理論では説明できない側面の発見

**対話セッション3：統合（Connection Making）（2時間）**

**目的**：発散的探索で生成されたアイデアを統合

**対話プロンプト例**：
```
セッション1と2で得られた洞察を統合し、以下を作成してください：

1. 中核命題（3-5個）：理論枠組みの基礎となる主張
2. 理論的メカニズム：各命題がどのように相互作用するか
3. 境界条件：理論が適用される/されない条件
4. 理論モデルの概念図（テキストベースの図）

特に、以下の点を重視してください：
- 論理的一貫性：命題間に矛盾はないか？
- 簡潔性：最小限の前提で最大限を説明しているか？
- 新規性：既存理論に何を付加しているか？
```

**対話セッション4：批判的評価（Critical Evaluation）（1時間）**

**目的**：構築された理論枠組みを厳密に評価

**対話プロンプト例**：
```
私の理論枠組みを以下の基準で批判的に評価してください：

1. 理論的妥当性：
   - 概念定義は明確か？
   - 論理的一貫性はあるか？
   - 因果推論は妥当か？

2. 検証可能性：
   - 実証研究で検証可能か？
   - どのようなデータが必要か？
   - 反証可能な予測を含んでいるか？

3. 理論的貢献：
   - 既存理論を単に組み合わせただけではないか？
   - 新規な洞察を提供しているか？
   - どのような学術的インパクトが期待できるか？

4. 限界と境界条件：
   - 理論が適用されない状況は何か？
   - 前提が破られるとどうなるか？
```

#### Day 61-63：理論モデル図の作成（6時間）

**Step 1：手書きスケッチ（2時間）**
- 中核概念を四角形（変数）で表現
- 因果関係を矢印で表現
- 調整効果を破線矢印で表現
- 媒介効果を複数矢印の連鎖で表現

**スケッチのポイント**：
- 複雑すぎない（概念は5-10個程度）
- 因果の方向性が明確
- 境界条件を明示（「高不確実性の場合」など）

**Step 2：デジタル化（4時間）**

**推奨ツール**：
- PowerPoint：最も手軽、学術的に標準
- Draw.io：無料、柔軟性高い
- Adobe Illustrator：プロフェッショナル品質（有料）

**作成手順（PowerPoint例）**：

1. 基本図形の配置
```
挿入 → 図形 → 四角形/楕円形
- 変数：四角形
- 構成概念：楕円形
```

2. 矢印の追加
```
挿入 → 図形 → 矢印
- 因果関係：実線矢印
- 調整効果：破線矢印
- 記号：+（正の関係）、-（負の関係）
```

3. ラベルとキャプション
```
各変数に明確な名称
矢印に仮説番号（H1、H2など）
図のタイトルと出典（「筆者作成」）
```

**理論モデル図の例**：
```
[図1. デジタル変革と持続的競争優位の統合的理論モデル]

           制度的圧力
               |
               ↓ (H1)
        デジタル変革戦略 ───(H2)──→ 持続的競争優位
               ↑                        ↑
               |                        |
          (H3) |                   (H5) |
               |                        |
        組織的能力              動的能力
                                       
                         (H4：調整効果)
                    産業の不確実性
```

**成果物**：
- `theory/models/theoretical_framework_v1.png`：理論モデル図

#### Day 64-70：統合レポートの執筆（8時間）

**レポート構成**（5,000-8,000字）：

**1. 序論**（1,000字）
- 研究背景と動機
- 研究質問の明確化
- 理論的貢献の予告

**2. 文献レビューと理論的ギャップ**（1,500字）
- 既存研究の体系的レビュー（Week 5-6の文献レビュー表を活用）
- 理論的ギャップの特定
- 本研究の位置づけ

**3. 複数競合仮説の提示**（1,500字）
- 各理論レンズからの説明（Week 5-6の競合仮説を精緻化）
- 各説明の理論的品質評価
- 説明間の比較

**4. 統合的理論枠組みの構築**（2,000字）
- 中核命題（3-5個）
- 理論的メカニズムの詳細説明
- 境界条件の明確化
- 理論モデル図の説明

**5. 理論的貢献と実証的示唆**（1,000字）
- 既存理論への貢献
- 実証研究への示唆（どのようなデータが必要か？）
- 実務的示唆

**6. 限界と今後の研究方向**（500字）
- 理論的限界の自覚的認識
- 次のステップ（Phase 2での実証研究計画）

**7. 結論**（500字）
- Phase 1で得られた主要な洞察
- 理論構築プロセスの振り返り

**執筆のポイント**：
- Week 1-2、5-6の成果物を統合
- Claudeとの対話から得られた洞察を反映
- 理論的一貫性を確保（論理的飛躍がないか常に確認）
- 学術的文体（断定的ではなく、慎重な表現）

**成果物**：
- `theory/frameworks/phase1_integrated_framework.md`：統合的理論枠組み（5,000-8,000字）

### Week 7-8完了時の評価基準

- [ ] Claudeとの対話を通じて、暗黙的前提を顕在化できた
- [ ] 創造的技法（類推、前提反転等）から新しい洞察を得た
- [ ] 理論モデル図を作成し、因果関係を視覚化できた
- [ ] 統合的理論枠組みのレポート（5,000-8,000字）が完成した
- [ ] 理論的一貫性と新規性を確保できた

---

## Phase 1全体の統合評価

### 最終成果物チェックリスト

**Week 1-2：理論的基盤**
- [ ] `phase1_week1-2_methodology_comparison.md`（2,000-3,000字）

**Week 3-4：基本ツール**
- [ ] Git管理された研究リポジトリ
- [ ] `environment.yml`（Python環境）
- [ ] `analysis/notebooks/01_dowhy_practice.ipynb`

**Week 5-6：文献レビューと仮説生成**
- [ ] `literature/review_matrix.xlsx`（10-15論文）
- [ ] `theory/hypotheses/competing_hypotheses.md`（3,000-5,000字）

**Week 7-8：理論枠組み構築**
- [ ] `theory/models/theoretical_framework_v1.png`
- [ ] `theory/frameworks/phase1_integrated_framework.md`（5,000-8,000字）

### 能力評価（自己評価）

**知識・理解**（5段階評価）
- [ ] Eisenhardt、Gioia、Glaser-Straussの哲学的差異を説明できる：1 2 3 4 5
- [ ] 因果グラフの基本的な読み書きができる：1 2 3 4 5
- [ ] 複数の理論レンズを使い分けられる：1 2 3 4 5

**スキル・実践**（5段階評価）
- [ ] Git/GitHubで研究プロジェクトを管理できる：1 2 3 4 5
- [ ] DoWhyで因果推論を実行できる：1 2 3 4 5
- [ ] 複数競合仮説を独力で生成できる：1 2 3 4 5
- [ ] 文献レビューから理論的ギャップを特定できる：1 2 3 4 5

**統合的能力**（5段階評価）
- [ ] 外部ツールと内部思考を統合的に使用できる：1 2 3 4 5
- [ ] 理論的一貫性を保ちながら創造的に考えられる：1 2 3 4 5

**総合評価**：
すべての項目で3以上ならPhase 1完了とみなす。
2以下の項目がある場合、該当Weekを再実施。

---

## Phase 2への移行準備

Phase 1完了後、以下を実施してからPhase 2へ：

### 1. 成果物の整理とアーカイブ
```bash
# Phase 1成果物を専用ディレクトリにコピー
mkdir phase1_archive
cp -r theory/ literature/ analysis/ phase1_archive/

# タグ付き
git tag -a v1.0-phase1-complete -m "Phase 1: Basic integration complete"
git push origin v1.0-phase1-complete
```

### 2. Phase 1の振り返りレポート作成

**レポート構成**（2,000字）：
1. 最も困難だった課題とその克服方法
2. 最も重要な学びと洞察
3. Phase 2での注力ポイント
4. タイムライン実績と計画との差異分析

**成果物**：
- `phase1_retrospective.md`

### 3. Phase 2実装計画の確認

Phase 2の主要活動を確認：
- Week 9-12：CAQDAS導入とコーディング
- Week 13-16：理論モデル可視化と論文執筆開始
- Week 17-20：SEM導入
- Week 21-24：Snakemakeワークフロー構築

---

## トラブルシューティング

### よくある問題と解決策

**問題1：文献レビューで何を読めばいいかわからない**
- 解決策：セミナル論文（引用数上位）から開始し、backward/forward searchで拡大

**問題2：複数競合仮説が思いつかない**
- 解決策：まず2つの対立する理論レンズ（例：RBV vs 制度理論）から開始。その後、第3の視点を追加。

**問題3：理論モデルが複雑になりすぎる**
- 解決策：中核概念を5-7個に絞る。詳細は本文で説明し、図はシンプルに。

**問題4：Gitの使い方がわからなくなった**
- 解決策：基本コマンドのチートシートを作成。`git status`、`git add .`、`git commit -m "message"`、`git push`の4つで80%のケースに対応可能。

**問題5：時間が足りない**
- 解決策：最小実行可能戦略（MVS）に切り替え。文献10本→5本、仮説5個→3個など、質を維持しつつ量を減らす。

---

## 補足資料

### 推奨学習リソース

**方法論**：
- Gehman et al. (2018): Finding theory-method fit（アプローチ選択のガイド）
- Langley (1999): Strategies for theorizing from process data（プロセス理論構築）

**因果推論**：
- Hernán & Robins (2020): "Causal Inference: What If"（無料公開、最良の入門書）
- Pearl & Mackenzie (2018): "The Book of Why"（一般読者向け、概念理解に最適）

**ツール**：
- DoWhy Documentation：https://www.pywhy.org/dowhy
- Git Book（日本語版）：https://git-scm.com/book/ja/v2

### テンプレートファイル

以下のテンプレートは`templates/`ディレクトリに配置：
- `methodology_comparison_template.md`
- `literature_review_matrix_template.xlsx`
- `competing_hypotheses_template.md`
- `theoretical_framework_template.md`

---

## Phase 1の哲学的意義

Phase 1は単なる「準備段階」ではない。それは、研究者が理論構築の**全体的リズム**を体得する重要な時期である。

外部ツール（Git、DoWhy、Zotero）は思考を外部化し、可視化する。内部スキル（複数競合仮説生成、批判的評価）は外部化された思考に方向性と意味を与える。この往復運動―外化と内化の弁証法―こそが、理論構築の本質的プロセスである。

Phase 1を完了した研究者は、もはや「初学者」ではない。理論構築の全景を見渡し、自分の立ち位置を理解し、次のステップへの明確な方向性を持つ「見習い理論構築者」となる。

Phase 2では、この基礎の上に、より高度なツール（CAQDAS、SEM）と深化したスキル（データ構造図作成、理論的厳密性評価）を統合していく。しかし、その核心にあるのは、Phase 1で体得した「外部と内部の往復運動」という基本的リズムである。

**次なるステップ**：
Week 1の理論的基盤習得から、今日、開始しよう。

---

**文書情報**

- **作成日**：2025-11-08
- **対象**：Phase 1実装者
- **前提**：SKILL.mdを読了済み
- **次の文書**：テンプレートファイル集

**更新履歴**：
- v1.0（2025-11-08）：初版作成
