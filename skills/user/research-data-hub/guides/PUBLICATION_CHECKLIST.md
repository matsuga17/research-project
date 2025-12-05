# トップジャーナル投稿前チェックリスト
## Publication-Ready Research: Comprehensive Pre-Submission Checklist

**対象ジャーナル**: Journal of Finance (JF), Journal of Financial Economics (JFE), Review of Financial Studies (RFS), Management Science (MS), Strategic Management Journal (SMJ), その他トップジャーナル

**Version**: 2.0  
**最終更新**: 2025-10-31

---

## 使用方法

このチェックリストは、論文投稿の **3-4週間前** から使用することを推奨します。各項目を順番に確認し、すべて完了してから投稿してください。

**進捗管理**:
```
✅ = 完了
🔄 = 作業中
❌ = 未着手
⚠️ = 問題あり（要対応）
```

---

## I. データ品質・再現性（Data Quality & Reproducibility）

### A. データ収集の文書化

- [ ] **A1. データソース完全文書化**
  - すべてのデータソースのURL記載
  - アクセス日付記録
  - APIバージョン記載
  - 使用した検索クエリ・フィルタ記録

- [ ] **A2. Data Lineage完備**
  ```python
  # data_lineage_report.json が存在するか確認
  # 以下の情報を含むか:
  - データソース情報
  - 取得日時
  - 変換履歴
  - 最終データセットへの経路
  ```

- [ ] **A3. Raw Dataの保存**
  - オリジナルの生データを別途保存
  - 変更履歴（diff）を記録
  - SHA-256ハッシュ値を計算・記録

### B. データクリーニングの透明性

- [ ] **B1. サンプル選択基準の明示**
  ```
  明記すべき情報:
  - 母集団定義
  - 包含基準（inclusion criteria）
  - 除外基準（exclusion criteria）
  - 各段階でのサンプルサイズ
  ```

- [ ] **B2. 欠損値処理の文書化**
  - 欠損値の発生パターン分析実施
  - 補完方法の根拠説明
  - 感度分析（欠損値処理方法の変更）実施

- [ ] **B3. 外れ値処理の記録**
  - Winsorization水準の根拠
  - 外れ値の特徴分析
  - 外れ値除外前後の比較

### C. 変数構築の検証

- [ ] **C1. 変数定義の一貫性**
  ```python
  # すべての変数にcodebookエントリがあるか確認
  # 以下を含む:
  - 変数名
  - 定義
  - 単位
  - ソース
  - 構築方法
  ```

- [ ] **C2. 会計恒等式の検証**
  ```python
  # 以下を確認:
  - 総資産 = 総負債 + 純資産（誤差 < 1%）
  - 営業CF + 投資CF + 財務CF = 現金変動
  - 売上 - COGS - 販管費 ≈ 営業利益
  ```

- [ ] **C3. 時系列一貫性の確認**
  - 前年度との増減が異常でないか
  - 構造的ブレイクを検出・説明

### D. 統計的検出力の確認

- [ ] **D1. 事前サンプルサイズ計算**
  ```python
  from data_quality_checker import SampleSizeCalculator
  
  calc = SampleSizeCalculator()
  result = calc.t_test_sample_size(
      effect_size='medium',
      alpha=0.05,
      power=0.80
  )
  # 実際のNが推奨Nを上回るか確認
  ```

- [ ] **D2. 実際の検出力計算（post-hoc）**
  - 主要な検定の達成検出力を計算
  - 検出力が0.80を下回る場合、解釈に注意喚起

- [ ] **D3. 最小検出可能効果（MDE）の報告**
  ```python
  # サンプルサイズが不十分な場合:
  mde = calc.minimum_detectable_effect(
      sample_size=actual_n,
      alpha=0.05,
      power=0.80
  )
  # "Our sample allows us to detect effects of [MDE] or larger."
  ```

---

## II. 分析の厳密性（Analytical Rigor）

### A. 主要分析

- [ ] **A1. 仮説の事前明示**
  - 研究仮説を明確に記載（H1, H2, ...）
  - 予測される符号を明示
  - 理論的根拠を説明

- [ ] **A2. 推定手法の妥当性**
  - 手法選択の根拠説明
  - 前提条件の検証（正規性、等分散性など）
  - 標準誤差の適切な計算（cluster-robust etc）

- [ ] **A3. 多重検定の対処**
  ```python
  # 多数の検定を実施する場合:
  from statsmodels.stats.multitest import multipletests
  
  # Bonferroni correction または FDR control
  reject, pvals_corrected, _, _ = multipletests(
      pvals, alpha=0.05, method='fdr_bh'
  )
  ```

### B. 頑健性検証（必須7カテゴリ）

参照: [ROBUSTNESS_CHECKS_GUIDE.md](ROBUSTNESS_CHECKS_GUIDE.md)

- [ ] **B1. サンプル構成の変更**
  - サブサンプル分析（産業別、時期別、規模別）
  - 極端値の除外

- [ ] **B2. 変数定義の変更**
  - 従属変数の代替定義
  - 独立変数の代替定義

- [ ] **B3. 推定手法の変更**
  - 標準誤差の頑健化
  - パネルデータ推定（FE, RE）

- [ ] **B4. コントロール変数の変更**
  - 段階的追加
  - 固定効果の追加

- [ ] **B5. 内生性への対処**
  - ラグ変数の使用
  - 操作変数法（適切なIVがある場合）

- [ ] **B6. 外れ値処理の変更**
  - 代替的なWinsorization水準
  - Robust regression

- [ ] **B7. 時系列構造への対応**
  - 動学パネルモデル
  - イベントスタディ

### C. 頑健性検証の報告

- [ ] **C1. 本文に簡潔な要約**
  ```
  例文:
  "Our main findings are robust to several alternative specifications, 
  including different measures of [DV], estimation methods, and sample 
  compositions. (See Online Appendix for detailed results.)"
  ```

- [ ] **C2. オンライン付録に完全結果**
  - Table A1-A7: 各カテゴリの頑健性検証
  - Figure A1: 係数安定性プロット

- [ ] **C3. 非有意結果の解釈**
  - 統計的検出力不足の可能性を議論
  - 点推定値の経済的意味を説明

---

## III. 論文執筆の品質（Writing Quality）

### A. 構造・論理

- [ ] **A1. Abstract完成度**
  - 研究課題明示（1文）
  - 手法概要（1-2文）
  - 主要発見（2-3文）
  - 貢献（1-2文）
  - 文字数: 150-200語

- [ ] **A2. Introduction構造**
  ```
  推奨構造:
  1. Research Question & Motivation (1-2段落)
  2. Main Findings (1段落)
  3. Contribution to Literature (2-3段落)
  4. Roadmap (1段落)
  
  ページ数: 3-5ページ
  ```

- [ ] **A3. Literature Review配置**
  - Introductionに統合（2-3段落）
  - または独立セクション（トップジャーナルでは稀）
  - 単なる羅列でなく、ギャップを明確化

- [ ] **A4. 論理的一貫性**
  - 各段落が1つの主張に集中
  - 段落間の接続が明確
  - 仮説 → 分析 → 結果 → 解釈の流れが明瞭

### B. 表・図の品質

- [ ] **B1. 表の完成度**
  ```
  必須要素:
  - タイトル（Table 1: [内容]）
  - 列ヘッダー明確
  - 係数の下に標準誤差（括弧内）
  - 有意水準記号（*, **, ***）
  - 脚注（SE type, controls, FE）
  - N, R², 統計量
  ```

- [ ] **B2. 図の品質**
  - 高解像度（300 dpi以上）
  - 軸ラベル明確
  - 凡例配置適切
  - カラーバリアフリー（色盲対応）

- [ ] **B3. 表・図の番号一貫性**
  - 本文での言及順に番号
  - "Table 1"形式（"table 1"や"Tab. 1"ではない）

### C. 引用・参考文献

- [ ] **C1. 引用形式の統一**
  - ジャーナル指定形式に準拠
  - Author-year形式: (Smith, 2020)
  - または番号形式: [1]

- [ ] **C2. 参考文献リスト完全性**
  - 本文のすべての引用が含まれる
  - 逆に、リストのすべてが本文で引用
  - アルファベット順・年代順

- [ ] **C3. DOI・URL追加**
  - 可能な限りDOI付与
  - Working paperはURL記載

---

## IV. 倫理・透明性（Ethics & Transparency）

### A. データ倫理

参照: [DATA_ETHICS_GUIDE.md](DATA_ETHICS_GUIDE.md)

- [ ] **A1. プライバシー保護**
  - 個人識別情報の匿名化
  - データ使用許諾の確認

- [ ] **A2. 利益相反の開示**
  - 資金提供源の明示
  - 研究対象との関係開示

- [ ] **A3. データ共有計画**
  - 可能な範囲でのデータ公開
  - 再現コードの提供

### B. 研究透明性

- [ ] **B1. Pre-registration実施（推奨）**
  - OSF, AsPredicted, AEA RCT Registry
  - 主要仮説・分析計画を事前登録

- [ ] **B2. すべての分析を報告**
  - 非有意結果も含める（オンライン付録）
  - "すべての仕様を試した"と明記

- [ ] **B3. データ・コード公開準備**
  ```
  Replication Package構成:
  /data/
    - clean_data.csv
    - codebook.json
  /code/
    - 01_data_cleaning.py
    - 02_main_analysis.py
    - 03_robustness_checks.py
  /results/
    - tables/
    - figures/
  README.md (実行手順)
  ```

---

## V. ジャーナル特有要件（Journal-Specific Requirements）

### A. Journal of Finance (JF)

- [ ] **A1. 論文長**
  - 本文: 40ページ以内（double-spaced）
  - オンライン付録: 制限なし

- [ ] **A2. データ・コード要件**
  - Data availability statementを含む
  - コード公開（AEA Data and Code Repository推奨）

- [ ] **A3. 投稿形式**
  - PDF形式（LaTeX推奨）
  - 匿名化（著者情報除去）

### B. Journal of Financial Economics (JFE)

- [ ] **B1. 論文長**
  - 本文: 50ページ以内

- [ ] **B2. 表・図の配置**
  - 本文内に埋め込み（または巻末）

- [ ] **B3. Internet Appendix**
  - すべての頑健性検証を含む
  - データ構築の詳細

### C. Management Science (MS)

- [ ] **C1. 論文長**
  - 本文: 45ページ以内

- [ ] **C2. Online Supplement**
  - すべての証明
  - 追加分析

---

## VI. 技術的チェック（Technical Checks）

### A. ファイル管理

- [ ] **A1. バージョン管理**
  - Git使用（推奨）
  - または日付付きバックアップ

- [ ] **A2. ファイル命名規則**
  ```
  推奨:
  - paper_v2.0_2025-10-31.tex
  - data_final_2025-10-31.csv
  - code_main_analysis_v2.py
  
  避ける:
  - paper_FINAL_FINAL.tex
  - data_new.csv
  ```

- [ ] **A3. バックアップ**
  - 3-2-1ルール遵守
    - 3コピー（本体+2バックアップ）
    - 2種類のメディア（ローカル+クラウド）
    - 1オフサイトコピー（別の物理的場所）

### B. コードの品質

- [ ] **B1. コメント充実**
  ```python
  # 良い例:
  # Step 1: Load and merge datasets
  # Merge financial data (EDINET) with stock price data (JPX)
  # Match key: firm_id + year
  df = pd.merge(df_financial, df_stock, on=['firm_id', 'year'], how='inner')
  ```

- [ ] **B2. コード実行可能性**
  - 他者が実行可能か確認
  - 相対パス使用（絶対パス禁止）
  - requirements.txt提供

- [ ] **B3. 計算効率**
  - 不要なループ削減
  - ベクトル演算活用
  - 実行時間記録

### C. 統計ソフトウェア

- [ ] **C1. パッケージバージョン記録**
  ```python
  # Python
  pip freeze > requirements_frozen.txt
  
  # R
  sessionInfo()
  ```

- [ ] **C2. 乱数シード固定**
  ```python
  import numpy as np
  np.random.seed(42)
  
  import random
  random.seed(42)
  ```

- [ ] **C3. 数値精度確認**
  - 浮動小数点誤差に注意
  - 重要な計算は検証

---

## VII. 投稿前最終確認（Final Pre-Submission Checks）

### A. セルフレビュー

- [ ] **A1. 音読チェック**
  - Abstract、Introduction、Conclusionを音読
  - 不自然な表現を修正

- [ ] **A2. 第三者レビュー**
  - 共著者以外に読んでもらう
  - 理解困難な箇所を特定

- [ ] **A3. 査読者の視点**
  ```
  想定される質問:
  - なぜこの研究が重要か？
  - 内生性の懸念は？
  - 結果は頑健か？
  - 代替的説明はないか？
  - 外的妥当性は？
  ```

### B. チェックリスト完了確認

- [ ] **B1. 全項目完了**
  - ✅がすべての必須項目に付いているか確認
  - ⚠️の項目を解決

- [ ] **B2. ドキュメント整備**
  - Cover letter作成
  - Response to reviewers（revise時）
  - Data availability statement

- [ ] **B3. 投稿準備**
  - 匿名化確認（著者名、所属、謝辞削除）
  - ファイルサイズ確認（ジャーナル制限内）
  - 投稿システムの要件確認

---

## VIII. 投稿後（Post-Submission）

### A. 記録管理

- [ ] **A1. 投稿記録**
  ```
  記録すべき情報:
  - ジャーナル名
  - 投稿日
  - Manuscript ID
  - 対応Editor名
  - 投稿したバージョン（SHA-256ハッシュ）
  ```

- [ ] **A2. バージョン凍結**
  - 投稿版をアーカイブ
  - 変更不可として保存

### B. Revise対応準備

- [ ] **B1. 査読コメント整理**
  ```markdown
  # Reviewer 1
  
  ## Major Comments
  1. [コメント要約]
     - 対応方針: [計画]
     - 完了日: [予定]
  
  ## Minor Comments
  ...
  ```

- [ ] **B2. 追加分析の準備**
  - 予想される追加要求をリスト化
  - 事前に分析実施（時間節約）

---

## IX. 緊急チェック（30分版）

時間がない場合の最小限チェックリスト：

### 絶対に確認すべき5項目

1. **データ品質**
   - [ ] 会計恒等式が成立（誤差<1%）
   - [ ] 外れ値処理を実施・文書化

2. **統計的妥当性**
   - [ ] Cluster-robust標準誤差を使用
   - [ ] 主要な頑健性検証を3つ以上実施

3. **再現性**
   - [ ] コードが実行可能
   - [ ] Data lineage文書化

4. **論文品質**
   - [ ] Abstract、Introduction音読
   - [ ] 表・図の番号一貫性確認

5. **投稿要件**
   - [ ] 匿名化完了
   - [ ] ジャーナル指定形式遵守

---

## X. リソース・ツール

### 推奨ツール

1. **文献管理**: Zotero, Mendeley, EndNote
2. **バージョン管理**: Git + GitHub
3. **LaTeX**: Overleaf (共著に便利)
4. **統計**: Python (pandas, statsmodels), R, Stata
5. **チェック自動化**: [本スキルのツール群]

### 関連ドキュメント

- [ROBUSTNESS_CHECKS_GUIDE.md](ROBUSTNESS_CHECKS_GUIDE.md) - 頑健性検証ガイド
- [DATA_ETHICS_GUIDE.md](DATA_ETHICS_GUIDE.md) - データ倫理
- [COMMON_PITFALLS.md](COMMON_PITFALLS.md) - よくある失敗例
- [TROUBLESHOOTING_FAQ.md](TROUBLESHOOTING_FAQ.md) - トラブルシューティング

---

## チェックリスト進捗管理

```python
# 進捗管理スクリプト
class PublicationChecklist:
    def __init__(self):
        self.items = {
            'data_quality': 13,
            'analytical_rigor': 13,
            'writing_quality': 10,
            'ethics': 6,
            'technical': 9,
            'final_checks': 5
        }
        self.completed = {k: 0 for k in self.items.keys()}
    
    def mark_complete(self, category, count=1):
        self.completed[category] += count
    
    def progress_report(self):
        total_items = sum(self.items.values())
        total_completed = sum(self.completed.values())
        print(f"Overall Progress: {total_completed}/{total_items} ({total_completed/total_items*100:.1f}%)")
        
        for cat in self.items.keys():
            pct = self.completed[cat] / self.items[cat] * 100
            print(f"  {cat}: {self.completed[cat]}/{self.items[cat]} ({pct:.0f}%)")


# 使用例
checklist = PublicationChecklist()
checklist.mark_complete('data_quality', 3)
checklist.progress_report()
```

---

**最終更新**: 2025-10-31  
**Version**: 2.0  
**次回レビュー予定**: 2026-04-30

このチェックリストを使用することで、トップジャーナルの査読基準を満たす論文を効率的に準備できます。
