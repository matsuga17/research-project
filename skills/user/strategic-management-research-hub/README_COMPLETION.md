# Strategic Organizational Research Hub - 補完ファイルパッケージ

## 📦 パッケージ概要

このディレクトリには、`strategic-organizational-research-hub`スキルを完璧に機能させるために不足していた**8つの重要ファイル**が含まれています。

**作成日**: 2025-10-31

---

## 📂 ディレクトリ構造

```
strategic-organizational-research-hub/
│
├── sample_scripts/                    # 実装例スクリプト
│   ├── complete_pipeline.py          # 研究プロジェクト全自動化パイプライン（1200行）
│   ├── japanese_firms_roa.py         # 日本企業R&D研究の完全実装（600行）
│   └── asian_comparison.py           # アジア3カ国比較研究（500行）
│
├── templates/                         # テンプレートファイル
│   ├── research_plan.md              # 研究計画書テンプレート（包括的）
│   ├── data_dictionary.xlsx          # データ辞書テンプレート（Excel）
│   └── replication_readme.md         # 再現性READMEテンプレート
│
└── tests/                             # テストファイル
    ├── test_data_integrity.py        # データ品質検証テスト（19テスト）
    └── test_qa_system.py             # 品質保証システム統合テスト（20テスト）
```

---

## ✨ 各ファイルの詳細

### 1. **complete_pipeline.py**（研究プロジェクト全自動化）

**目的**: データ収集から論文執筆まで、研究の全ライフサイクルを自動化

**機能**:
- **8フェーズの自動実行**:
  1. データ収集（API/手動/スクレイピング）
  2. データクリーニング（欠損値・外れ値処理）
  3. データ統合（複数ソースのマージ）
  4. 記述統計（Table 1-3）
  5. 回帰分析（OLS/Panel/IV/DiD）
  6. 頑健性チェック
  7. 可視化（Figure 1-3）
  8. 結果エクスポート（LaTeX/DOCX/Excel）

**使用方法**:
```bash
python complete_pipeline.py --config config.yaml
```

**設定ファイル例** (`config.yaml`):
```yaml
data_sources:
  - name: compustat
    type: database
    query: "SELECT * FROM comp.funda WHERE ..."
  
sample_criteria:
  industry: [20, 21, 22]  # SIC codes
  years: [2010, 2023]
  
variables:
  dependent: roa
  independent: [rd_intensity, log_assets]
  controls: [leverage, firm_age]
  
analysis:
  models:
    - name: "Model 1"
      type: panel_fe
      formula: "roa ~ rd_intensity + log_assets + leverage"
```

**出力**:
- `data_final.csv`: 最終データセット
- `output/tables/`: 回帰表
- `output/figures/`: 図表
- `output/logs/`: 実行ログ

---

### 2. **japanese_firms_roa.py**（日本企業R&D研究）

**研究テーマ**: 日本製造業におけるR&D投資と企業パフォーマンス

**仮説**:
- H1: R&D集約度はROAと正の関係
- H2: 高技術産業でより強い効果
- H3: 企業規模が調整効果を持つ

**データソース**（すべて無料）:
- EDINET: 財務データ
- USPTO PatentsView: 特許データ
- World Bank: マクロデータ

**サンプル**: 日本製造業15社 × 14年 = 210観測値（シミュレート版）

**実行方法**:
```bash
python japanese_firms_roa.py
```

**出力**:
```
output_japanese_firms_roa/
├── data_raw.csv
├── data_cleaned.csv
├── table1_sample_composition.csv
├── table2_descriptive_stats.csv
├── table3_correlation.csv
├── table4_regression_results.txt
└── figures/
    ├── figure1_roa_distribution.png
    ├── figure2_rd_roa_scatter.png
    └── figure3_rd_trend.png
```

**所要時間**: 約5分

---

### 3. **asian_comparison.py**（アジア3カ国比較研究）

**研究テーマ**: 日本・韓国・台湾における取締役会の多様性とESGパフォーマンス

**仮説**:
- H1: 女性役員比率はESGスコアと正の関係
- H2: ガバナンス品質が高い国で効果が強い
- H3: 産業により効果が異なる

**データソース**（すべて無料）:
- EDINET（日本）: 役員データ
- DART（韓国）: 役員データ
- MOPS（台湾）: 役員データ
- CDP: ESGデータ
- World Bank WGI: ガバナンス指標

**サンプル**: 3カ国 × 10社/国 × 9年 = 270観測値

**実行方法**:
```bash
python asian_comparison.py
```

**出力**:
```
output_asian_comparison/
├── data_final.csv
├── regression_results.txt
└── figures/
    ├── figure1_female_ratio_trend.png
    └── figure2_esg_by_country.png
```

---

### 4. **research_plan.md**（研究計画書テンプレート）

**内容**（16セクション）:
1. Research Question & Motivation
2. Theoretical Framework（理論・仮説）
3. Research Design（研究デザイン）
4. Data Sources（データソース評価）
5. Data Collection Plan（収集計画）
6. Data Cleaning Plan（クリーニング計画）
7. Statistical Analysis Plan（分析計画）
8. Expected Results & Contributions
9. Timeline（22週間スケジュール）
10. Resources & Budget
11. Risk Management（リスク管理）
12. Ethical Considerations
13. Replication & Transparency
14. Target Journal
15. References
16. Approval & Sign-off

**使用方法**:
1. テンプレートを開く
2. [ ] の項目を埋める
3. アドバイザーと共有
4. 承認後、データ収集開始

---

### 5. **data_dictionary.xlsx**（データ辞書テンプレート）

**構成**:
- **Sheet 1**: Data Dictionary
  - Variable Name
  - Description
  - Data Type
  - Unit/Scale
  - Source
  - Source Variables
  - Missing Count/Percentage
  - Mean, SD, Min, Max
  - Notes

- **Sheet 2**: Instructions
  - 使用方法の詳細説明
  - ベストプラクティス
  - 記入例

**用途**:
- 変数の定義と出典を明確化
- 共同研究者との情報共有
- 査読者への透明性提供

---

### 6. **replication_readme.md**（再現性READMEテンプレート）

**内容**（20セクション）:
1. Overview
2. Contents（ファイル構造）
3. System Requirements
4. Installation & Setup
5. Data Access
6. Replication Instructions
7. Expected Results
8. Troubleshooting
9. Data Sources
10. Sample Selection
11. Variable Definitions
12. Statistical Methods
13. Computational Environment
14. Citation
15. License
16. Contact
17. Acknowledgments
18. Version History
19. Additional Resources
20. FAQ

**用途**:
- 研究の再現性を確保
- 他の研究者がコードを実行できるようサポート
- ジャーナル投稿時の必須資料

---

### 7. **test_data_integrity.py**（データ品質検証テスト）

**19個のテスト**:

**カテゴリ1: データ構造**
- データロード成功
- 必須列の存在確認
- 完全に空の列の検出

**カテゴリ2: 欠損データ**
- 欠損率が許容範囲内か
- キー変数の欠損最小化

**カテゴリ3: 外れ値**
- 極端な外れ値検出
- 財務比率の妥当性

**カテゴリ4: 論理的整合性**
- 年の値が妥当か
- 企業年齢が非負か
- Log変数の妥当性

**カテゴリ5: 時系列整合性（パネルデータ）**
- パネル構造の確認
- 重複企業-年の検出
- 時系列ギャップの検出

**カテゴリ6: データ型**
- 数値変数が数値型か
- カテゴリ変数が文字列型か

**カテゴリ7: 統計的性質**
- 分散がゼロでないか
- 相関行列が計算可能か

**カテゴリ8: サンプルサイズ**
- 回帰に十分なサンプルサイズか
- グループごとに十分な観測値か

**実行方法**:
```bash
python test_data_integrity.py --data data_final.csv
```

**出力例**:
```
✓ Test 1.1 PASSED: Data loaded successfully (5000 rows)
✓ Test 2.1 PASSED: Missing data within acceptable limits
⚠ Warning: rd_intensity has 20% missing data
✓ Test 3.1 PASSED: No extreme outliers detected
...
Tests run: 19
Failures: 0
Errors: 0
```

---

### 8. **test_qa_system.py**（品質保証システム統合テスト）

**20個のQAチェック**:

**カテゴリ1: データ収集QA**
- データソースの文書化
- 収集ログの存在
- 生データの保存

**カテゴリ2: データクリーニングQA**
- データ辞書の完全性
- クリーニング手順の文書化
- 整合性テストの合格

**カテゴリ3: 分析QA**
- 記述統計表の作成
- 回帰診断の文書化
- 頑健性チェックの実施
- 結果表の出版可能性

**カテゴリ4: 出力QA**
- 図表の高解像度
- 図表のラベル
- READMEの包括性

**カテゴリ5: 再現性QA**
- コードの実行可能性
- 要件の文書化
- 再現手順の提供
- サンプルデータの提供

**カテゴリ6: 研究倫理QA**
- 利用規約の遵守
- 引用の正確性
- 機密データ漏洩の防止

**実行方法**:
```bash
python test_qa_system.py --project-dir ./my_research_project/
```

**出力**:
```
✓ QA 1.1 PASSED: Data sources documented
✓ QA 2.1 PASSED: Data dictionary complete
✓ QA 3.1 PASSED: Descriptive statistics generated
⚠ QA 4.1 SKIPPED: No figures/ directory found
...
Tests run: 20
Passed: 15
Skipped: 5
```

---

## 🚀 クイックスタート

### ステップ1: ファイルの配置

```bash
# ダウンロードしたファイルを適切な場所に配置
cp sample_scripts/* /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub/sample_scripts/
cp templates/* /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub/templates/
cp tests/* /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub/tests/
```

### ステップ2: 依存関係のインストール

```bash
pip install pandas numpy scipy statsmodels linearmodels matplotlib seaborn openpyxl --break-system-packages
```

### ステップ3: サンプルスクリプトの実行

```bash
cd sample_scripts
python japanese_firms_roa.py
```

### ステップ4: データ品質テストの実行

```bash
cd tests
python test_data_integrity.py --data ../output_japanese_firms_roa/data_cleaned.csv
```

---

## 📖 使用シナリオ

### シナリオ1: 新規研究プロジェクトの開始

1. `research_plan.md`をコピーして記入
2. `complete_pipeline.py`の`config.yaml`を作成
3. パイロットデータ収集（10-20企業）
4. `test_data_integrity.py`で品質確認
5. フルデータ収集
6. `complete_pipeline.py`を実行
7. `test_qa_system.py`で品質保証

### シナリオ2: 既存研究の再現

1. `replication_readme.md`を参考に環境構築
2. データソースへのアクセスを取得
3. 提供されたスクリプトを実行
4. 結果が元論文と一致するか確認

### シナリオ3: 日本企業研究の実施

1. `japanese_firms_roa.py`をベースに修正
2. EDINET APIを使用して実データ収集
3. USPTOから特許データ取得
4. 分析実行
5. 結果をSMJ/AMJスタイルで執筆

### シナリオ4: アジア比較研究

1. `asian_comparison.py`をベースに修正
2. 各国の開示システムからデータ収集
   - 日本: EDINET
   - 韓国: DART
   - 台湾: MOPS
3. CDPからESGデータ取得
4. 分析実行
5. 国際経営ジャーナルに投稿

---

## ⚙️ カスタマイズ方法

### complete_pipeline.pyのカスタマイズ

**データソースの追加**:
```python
class MyDataCollector(DataCollector):
    def _collect_my_source(self, source: Dict) -> pd.DataFrame:
        # カスタムデータ収集ロジック
        return df
```

**新しい分析手法の追加**:
```python
class RegressionAnalyzer:
    def _run_my_method(self, df: pd.DataFrame, spec: Dict):
        # カスタム分析ロジック
        return result
```

### テストのカスタマイズ

**新しいテストの追加**:
```python
def test_21_my_custom_check(self):
    """
    Custom QA check for my specific needs.
    """
    # テストロジック
    self.assertTrue(condition, "Error message")
```

---

## 🔧 トラブルシューティング

### 問題1: パッケージのインストールエラー

**エラー**: `error: externally-managed-environment`

**解決策**:
```bash
pip install [package] --break-system-packages
# または
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 問題2: EDINET APIエラー

**エラー**: `HTTP 404 Not Found`

**解決策**:
- 日付形式を確認（YYYY-MM-DD）
- 平日の日付を使用（土日祝は書類提出なし）
- APIレート制限を遵守（1秒に1リクエスト）

### 問題3: メモリ不足

**エラー**: `MemoryError`

**解決策**:
- データをチャンクで処理
- 不要な変数を削除 (`del df; gc.collect()`)
- より強力なマシンを使用

---

## 📊 期待される成果物

### 研究プロジェクト完了時に得られるもの:

1. **データ**:
   - `data_raw.csv`: 生データ
   - `data_cleaned.csv`: クリーニング済みデータ
   - `data_dictionary.xlsx`: 変数定義

2. **分析結果**:
   - `table1-3.csv`: 記述統計
   - `table4.tex`: 回帰結果（LaTeX）
   - `table5.tex`: 頑健性チェック

3. **可視化**:
   - `figure1-3.png`: 高解像度図表

4. **文書**:
   - `research_plan.md`: 研究計画
   - `REPLICATION.md`: 再現手順
   - `qa_report.json`: 品質保証レポート

5. **コード**:
   - 実行可能なPythonスクリプト
   - コメント付きで理解しやすい
   - テスト済みで信頼性高い

---

## 🎓 学術基準への準拠

### トップジャーナル要件

**Strategic Management Journal (SMJ)**:
- ✓ 理論に基づく仮説
- ✓ パネルデータ分析
- ✓ 頑健性チェック
- ✓ 再現性材料

**Academy of Management Journal (AMJ)**:
- ✓ 厳密な理論構築
- ✓ 複数の分析手法
- ✓ 内生性への対応
- ✓ 代替説明の検討

**Organization Science (OS)**:
- ✓ 新しい理論的洞察
- ✓ 精緻な統計分析
- ✓ データの透明性
- ✓ 限界の明示

---

## 📝 引用

このスキルパッケージを使用した場合、以下のように引用してください：

```
データ収集、理論フレームワーク開発、統計分析は、
business strategy and organizational strategy empirical research
のための体系的プロトコル（strategic-organizational-research-hub
skill v1.0）に従い、研究プロセス全体の再現性と方法論的厳密性を
確保した。
```

---

## 📞 サポート

### 質問・バグ報告

- **GitHub Issues**: [リンク]
- **Email**: [メールアドレス]

### 改善提案

新しいデータソースの追加、分析手法の追加、テストの追加など、
改善提案を歓迎します。

---

## 📜 ライセンス

**コード**: MIT License  
**テンプレート**: CC BY 4.0  
**データ**: 各データプロバイダーの利用規約に従う

---

## 🎉 おめでとうございます！

これで、`strategic-organizational-research-hub`スキルが**完全に機能**します。

**次のステップ**:
1. サンプルスクリプトを実行してみる
2. 自分の研究テーマに合わせてカスタマイズ
3. 高品質な研究を実施
4. トップジャーナルに投稿

**研究の成功を祈っています！🚀**

---

**作成者**: Strategic Management Research Hub  
**バージョン**: 1.0  
**最終更新**: 2025-10-31
