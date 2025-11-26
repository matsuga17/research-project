# よくある失敗例と対策（Common Pitfalls and Solutions）
## 実証研究で陥りやすい罠とその回避方法

**対象読者**: 実証研究を行うすべての研究者、特に初めてトップジャーナルに投稿する方  
**目的**: 先人の失敗から学び、同じ轍を踏まないための実践的ガイド  
**Version**: 2.0  
**最終更新**: 2025-10-31

---

## 目次

1. [データ収集・処理での失敗](#data-collection)
2. [統計分析での失敗](#statistical-analysis)
3. [論文執筆での失敗](#writing)
4. [査読対応での失敗](#peer-review)
5. [時間管理での失敗](#time-management)

---

<a name="data-collection"></a>
## 1. データ収集・処理での失敗

### 失敗例1: 「データが突然消えた」

**状況**:
```
研究者: 「3ヶ月かけて集めたデータが、PCクラッシュで全て消えました...」
原因: バックアップなし、クラウド同期なし
```

**影響**: 研究が数ヶ月遅延、最悪の場合プロジェクト中止

**対策**: **3-2-1バックアップルール** を徹底

```python
# 自動バックアップスクリプト
import shutil
import datetime
from pathlib import Path

def backup_data():
    """データを複数箇所にバックアップ"""
    
    # ソースディレクトリ
    source = Path('/Users/research/data')
    
    # バックアップ1: ローカル外付けHDD
    backup1 = Path('/Volumes/Backup_Drive/research_backup')
    
    # バックアップ2: クラウド（Dropbox/Google Drive/OneDrive）
    backup2 = Path('/Users/research/Dropbox/research_backup')
    
    # タイムスタンプ付きバックアップ
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    for backup_dir in [backup1, backup2]:
        destination = backup_dir / f'backup_{timestamp}'
        shutil.copytree(source, destination)
        print(f"Backup created: {destination}")

# 毎日自動実行（crontabやTask Schedulerで設定）
if __name__ == '__main__':
    backup_data()
```

**ベストプラクティス**:
- ✅ Git + GitHub/GitLabでコード管理
- ✅ データはDropbox/Google Driveで自動同期
- ✅ 重要なマイルストーンでZIPアーカイブ作成
- ✅ 外付けHDDに週1回バックアップ

---

### 失敗例2: 「どのデータが最新版かわからない」

**状況**:
```
フォルダ構成:
/data/
  - final_data.csv
  - final_data_v2.csv
  - final_data_FINAL.csv
  - final_data_FINAL_REALLY.csv
  - final_data_20231015.csv
  - final_data_new.csv

研究者: 「どれが本当の最終版？」
```

**影響**: 誤ったデータで分析、結果の信頼性喪失

**対策**: **Git + バージョン番号 + 日付** の体系的管理

```bash
# Git管理の例
git init
git add data/corporate_data_v1.0_2025-10-31.csv
git commit -m "Initial dataset: n=1,234, 2015-2023"

# 変更時
git add data/corporate_data_v1.1_2025-11-05.csv
git commit -m "Added R&D variables, removed outliers >3σ"

# タグ付け（重要なバージョン）
git tag -a v1.0 -m "Version submitted to JF"
```

**命名規則**:
```
推奨: [project]_[content]_v[major].[minor]_[YYYY-MM-DD].[extension]
例: asian_roa_data_v2.1_2025-10-31.csv

禁止: final.csv, new.csv, data_FINAL_FINAL.csv
```

---

### 失敗例3: 「このデータ、どこから取ったんだっけ？」

**状況**:
```
査読者: 「データソースのURLを教えてください」
研究者: 「え、記録してない...」
```

**影響**: 
- 再現不可能（致命的）
- 査読者の信頼喪失
- リジェクトの可能性大

**対策**: **Data Lineage Trackerの使用**

```python
from data_lineage_tracker import DataLineageTracker

# プロジェクト開始時に初期化
tracker = DataLineageTracker('asian_roa_study')

# データソース記録（収集時）
tracker.log_data_source(
    source_name='EDINET',
    url='https://disclosure.edinet-fsa.go.jp/api/v1/documents.json',
    access_date='2025-10-31',
    version='API v1.0',
    query_parameters={'date': '2023-03-31', 'type': '2'}
)

# 変換記録
tracker.log_transformation(
    transformation_name='Winsorization',
    input_vars=['roa'],
    output_vars=['roa_winsorized'],
    code_snippet="df['roa'].clip(lower=p01, upper=p99)",
    params={'lower_percentile': 0.01, 'upper_percentile': 0.99}
)

# 最終レポート出力
tracker.export_lineage_report('data_lineage_report.json')
```

**必ず記録すべき情報**:
- データソースURL
- アクセス日時
- 使用したAPI/クエリ
- ダウンロードしたファイル名
- データ加工の全手順

---

### 失敗例4: 「マージしたら観測数が激減した」

**状況**:
```
df1 = pd.read_csv('financial_data.csv')  # n=10,000
df2 = pd.read_csv('stock_data.csv')      # n=8,500

merged = pd.merge(df1, df2, on='firm_id', how='inner')
print(len(merged))  # 2,134 ← えっ、なぜこんなに少ない？
```

**原因**: 
- IDの不一致（大文字小文字、全角半角）
- 時期のずれ
- 欠損値

**対策**: **段階的マージ + 診断**

```python
def diagnostic_merge(df1, df2, key, how='inner'):
    """診断情報付きマージ"""
    
    print(f"Before merge: df1={len(df1)}, df2={len(df2)}")
    
    # マージ前にキーの重複確認
    dup1 = df1[key].duplicated().sum()
    dup2 = df2[key].duplicated().sum()
    if dup1 > 0 or dup2 > 0:
        print(f"⚠️  WARNING: Duplicates found (df1={dup1}, df2={dup2})")
    
    # 共通キーの確認
    common_keys = set(df1[key]) & set(df2[key])
    print(f"Common keys: {len(common_keys)}")
    print(f"Only in df1: {len(set(df1[key]) - set(df2[key]))}")
    print(f"Only in df2: {len(set(df2[key]) - set(df1[key]))}")
    
    # マージ
    merged = pd.merge(df1, df2, on=key, how=how, indicator=True)
    
    # マージ結果の診断
    print(f"\nMerge results:")
    print(merged['_merge'].value_counts())
    print(f"Final n: {len(merged)}")
    
    # マッチしなかったケースをレポート
    unmatched_df1 = df1[~df1[key].isin(merged[key])]
    unmatched_df2 = df2[~df2[key].isin(merged[key])]
    
    unmatched_df1.to_csv('unmatched_from_df1.csv', index=False)
    unmatched_df2.to_csv('unmatched_from_df2.csv', index=False)
    
    return merged.drop('_merge', axis=1)

# 使用例
merged = diagnostic_merge(df_financial, df_stock, key='firm_id')
```

**ベストプラクティス**:
- ✅ マージ前にキーの整合性確認
- ✅ 段階的マージ（一度に複数データソースをマージしない）
- ✅ マッチ率を記録（90%以上が望ましい）
- ✅ アンマッチの原因を調査

---

<a name="statistical-analysis"></a>
## 2. 統計分析での失敗

### 失敗例5: 「p値が0.051で非有意...あと少しなのに！」

**状況**:
```python
result = model.fit()
print(f"p-value: {result.pvalues['rd_intensity']:.3f}")
# 0.051

研究者の心の声: 「0.05以下にならないかな...」
→ 様々な仕様を試す
→ p < 0.05になる仕様を発見
→ 「この仕様が正しい」と主張
```

**問題**: **p-hacking（データマイニング）**

**影響**:
- 偽陽性の結果
- 再現不可能
- 研究の信頼性喪失

**対策**: **Pre-registration + 透明性**

```python
# Pre-analysis Plan（分析前に作成・登録）
"""
Primary Hypothesis:
H1: R&D intensity positively affects ROA (β > 0)

Primary Specification:
ROA = β₀ + β₁·RD_intensity + β₂·Log_assets + β₃·Leverage + ε

Clustering: Firm-level
Sample: Manufacturing firms, 2015-2023
N (expected): >200 firms

Pre-specified Robustness Checks:
1. Alternative DV: Operating ROA
2. Winsorization: 5%/95% (vs. 1%/99%)
3. Subsample: High-tech vs. Traditional

Registered: 2025-10-31 on OSF.io
"""

# すべての仕様を報告（有意・非有意問わず）
all_results = []

# Spec 1: Baseline
model1 = run_regression(df, spec='baseline')
all_results.append({'spec': 'Baseline', 'coef': model1.params[1], 
                   'pval': model1.pvalues[1]})

# Spec 2: Alternative DV
model2 = run_regression(df, dependent_var='operating_roa')
all_results.append({'spec': 'Alt DV', 'coef': model2.params[1], 
                   'pval': model2.pvalues[1]})

# ...すべての仕様を記録

# 結果テーブル作成
results_df = pd.DataFrame(all_results)
print(results_df)
```

**重要な原則**:
- ✅ 分析計画を事前登録
- ✅ すべての結果を報告
- ✅ 非有意の理由を議論（検出力不足 vs. 真のゼロ効果）
- ❌ 有意になるまで仕様変更を繰り返さない

---

### 失敗例6: 「標準誤差、どれ使えばいいの？」

**状況**:
```python
# OLS回帰
model = smf.ols('roa ~ rd_intensity + controls', data=df).fit()

# 標準誤差の選択肢
se_default = model.bse['rd_intensity']         # 0.010
se_robust = model.get_robustcov_results(cov_type='HC3').bse['rd_intensity']  # 0.012
se_cluster = model.get_robustcov_results(cov_type='cluster', 
                                         groups=df['firm_id']).bse['rd_intensity']  # 0.018

# どれが正しい？
```

**問題**: 標準誤差の選択で有意性が変わる

**対策**: **パネルデータの性質に応じて選択**

```python
def choose_standard_error(df, firm_id='firm_id', time_var='year'):
    """
    適切な標準誤差の選択ガイド
    """
    
    # パネル構造の確認
    n_firms = df[firm_id].nunique()
    n_periods = df[time_var].nunique()
    avg_obs_per_firm = len(df) / n_firms
    
    print(f"Panel structure: {n_firms} firms, {n_periods} periods")
    print(f"Average observations per firm: {avg_obs_per_firm:.1f}")
    
    # 推奨事項
    if n_firms < 50:
        print("⚠️  WARNING: Few clusters. Bootstrap or wild cluster bootstrap recommended.")
        return 'bootstrap'
    
    if avg_obs_per_firm > 1:
        print("✅ Cluster-robust SE recommended (firm level)")
        return 'cluster_firm'
    
    if n_periods > 1 and avg_obs_per_firm > 1:
        print("✅ Two-way clustering recommended (firm + year)")
        return 'cluster_twoway'
    
    print("✅ Heteroskedasticity-robust SE (HC3) recommended")
    return 'HC3'

# 使用例
se_type = choose_standard_error(df)
```

**決定木**:
```
パネルデータ？
  Yes → 企業レベルのクラスタリング必須
    → クラスタ数 < 50？
      Yes → Bootstrap SE
      No → Cluster-robust SE
  No → Heteroskedasticity-robust SE (HC3)
```

---

### 失敗例7: 「サンプルサイズ、これで十分だよね？」

**状況**:
```
研究者: 「n=85でt検定したら非有意だった。効果なしと結論」
統計家: 「検出力は？」
研究者: 「？」
```

**問題**: **Type II error（偽陰性）** の見落とし

**対策**: **事前にサンプルサイズ計算**

```python
from data_quality_checker import SampleSizeCalculator

calc = SampleSizeCalculator()

# 期待される効果サイズ（文献レビューから推定）
expected_d = 0.3  # Small-to-medium effect

# 必要サンプルサイズ
result = calc.t_test_sample_size(
    effect_size=expected_d,
    alpha=0.05,
    power=0.80  # 80%の検出力
)

print(f"Required n per group: {result['n_per_group']}")
print(f"Total n required: {result['total_n']}")

# 現在のサンプルで検出可能な効果サイズ
actual_n = 85
min_detectable = calc.minimum_detectable_effect(
    sample_size=actual_n,
    alpha=0.05,
    power=0.80
)

print(f"With n={actual_n}, MDE = {min_detectable:.3f}")
```

**正しい報告**:
```
"We find no significant effect of R&D intensity on ROA (β=0.023, p=0.12). 
However, our sample size (n=85) provides 80% power to detect effects of 
d=0.6 or larger. The observed effect size (d=0.3) falls below this 
threshold, suggesting the null result may reflect insufficient statistical 
power rather than a true absence of effect."
```

---

<a name="writing"></a>
## 3. 論文執筆での失敗

### 失敗例8: 「査読者が理解してくれない」

**状況**:
```
査読コメント:
"The paper's contribution is unclear. What exactly is new here?"
"The writing is confusing. I couldn't follow the logic."
```

**原因**: 
- Contribution statementが曖昧
- 論理的飛躍
- 専門用語の過度な使用

**対策**: **明確なContribution Statement**

```markdown
# 良い例（明確）

Our study makes three contributions to the R&D-performance literature:

1. **Novel Context**: We are the first to examine R&D effects in East Asian 
   manufacturing firms, where institutional differences (e.g., bank-centered 
   finance, patient capital) may alter R&D incentives.

2. **Mechanism**: We identify firm size as a key moderator, showing that 
   R&D benefits are concentrated in larger firms (>$1B assets) due to 
   economies of scale in R&D.

3. **Data**: We construct a unique panel of 245 firms across Japan, Korea, 
   and China (2015-2023) using only free data sources, demonstrating that 
   high-quality research is possible without expensive databases.

# 悪い例（曖昧）

This study contributes to the literature on R&D and firm performance.
```

**テンプレート**:
```
We contribute to [literature X] by [action]:

1. [Empirical contribution]: We document [new fact/pattern]
2. [Theoretical contribution]: We show that [mechanism/theory]
3. [Methodological contribution]: We introduce [method/data]
```

---

### 失敗例9: 「表が見づらい」

**状況**:
```
Table 1: Regression Results
                          (1)        (2)        (3)
────────────────────────────────────────────────
rd_intensity             0.045123   0.046789   0.044321
                        (0.012345) (0.013456) (0.011234)
log_assets              0.012345   0.013456   0.014567
                        (0.003456) (0.004567) (0.003456)
[50 more variables...]
```

**問題**: 情報過多、重要な結果が埋もれる

**対策**: **選択的報告 + 段階的開示**

```python
# 本文の表：コアの結果のみ
core_vars = ['rd_intensity', 'log_assets', 'leverage']

# オンライン付録の表：すべてのコントロール変数

def create_publication_table(results, core_vars):
    """出版用の整理された表を作成"""
    
    table = []
    
    # ヘッダー
    table.append(['', 'Model 1', 'Model 2', 'Model 3'])
    
    # コア変数
    for var in core_vars:
        row = [var]
        for model in results:
            coef = f"{model.params[var]:.3f}"
            se = f"({model.bse[var]:.3f})"
            stars = get_significance_stars(model.pvalues[var])
            row.append(f"{coef}{stars}")
        table.append(row)
        
        # 標準誤差行
        row_se = ['']
        for model in results:
            row_se.append(f"({model.bse[var]:.3f})")
        table.append(row_se)
    
    # コントロール変数（Yes/No表示）
    control_vars = [v for v in results[0].params.index if v not in core_vars]
    table.append(['Controls', 'Yes', 'Yes', 'Yes'])
    table.append(['Firm FE', 'No', 'Yes', 'Yes'])
    table.append(['Year FE', 'No', 'No', 'Yes'])
    
    # 統計量
    table.append(['Observations', 
                 str(len(results[0].model.data.orig_endog)),
                 str(len(results[1].model.data.orig_endog)),
                 str(len(results[2].model.data.orig_endog))])
    table.append(['R²', 
                 f"{results[0].rsquared:.3f}",
                 f"{results[1].rsquared:.3f}",
                 f"{results[2].rsquared:.3f}"])
    
    return pd.DataFrame(table)
```

**ベストプラクティス**:
- ✅ 主要変数のみ本文に掲載（3-5変数）
- ✅ コントロール変数はYes/No表示
- ✅ 詳細はオンライン付録
- ✅ 有意水準を明確に（*, **, ***）

---

<a name="peer-review"></a>
## 4. 査読対応での失敗

### 失敗例10: 「査読者と論争になった」

**状況**:
```
Reviewer: "The endogeneity concern is serious. You need IV."

著者の（悪い）応答:
"We disagree. Our approach is correct. Reviewer misunderstands."

結果: Reject
```

**問題**: 防御的・攻撃的な返答

**対策**: **建設的・協力的な対応**

```markdown
# 良い応答例

We thank the reviewer for raising this important concern about endogeneity. 
We agree that reverse causality is a potential issue.

We have addressed this concern in three ways:

1. **Lagged Variables**: We now use t-1 R&D intensity to predict t ROA, 
   reducing simultaneity bias (new Table 3, Column 3).

2. **Instrumental Variables**: We instrument for R&D using industry-average 
   R&D intensity, which strongly predicts firm-level R&D (F=28.4) but is 
   plausibly exogenous to individual firm ROA (new Table A5).

3. **Granger Causality Test**: We show that past R&D predicts future ROA, 
   but past ROA does not predict future R&D, consistent with our causal 
   interpretation (new Table A6).

While no approach perfectly eliminates endogeneity concerns, these three 
complementary analyses substantially strengthen our causal claims.

[New results on page 23, Online Appendix pp. A12-A15]
```

**テンプレート**:
```
1. 査読者に感謝
2. 懸念を認める
3. 対応策を具体的に説明
4. 新しい分析を追加
5. 限界を正直に認める（必要に応じて）
```

---

<a name="time-management"></a>
## 5. 時間管理での失敗

### 失敗例11: 「締切直前にパニック」

**状況**:
```
Day -30: 「まだ1ヶ月ある。余裕」
Day -14: 「そろそろ始めるか」
Day -7:  「やばい、間に合わない」
Day -1:  「徹夜で何とか...」
締切日:  「提出したけど、誤字脱字だらけ、分析も不完全」

結果: Desk reject
```

**対策**: **逆算スケジュール + バッファ**

```python
from datetime import datetime, timedelta

class ResearchScheduler:
    """研究プロジェクトのスケジュール管理"""
    
    def __init__(self, deadline, project_name):
        self.deadline = datetime.strptime(deadline, '%Y-%m-%d')
        self.project_name = project_name
        self.tasks = []
    
    def add_task(self, task_name, duration_days, dependencies=[]):
        """タスク追加"""
        self.tasks.append({
            'name': task_name,
            'duration': duration_days,
            'dependencies': dependencies
        })
    
    def generate_schedule(self):
        """スケジュール生成（逆算）"""
        current_date = self.deadline
        schedule = []
        
        # 逆順でタスク配置
        for task in reversed(self.tasks):
            end_date = current_date
            start_date = current_date - timedelta(days=task['duration'])
            
            schedule.append({
                'task': task['name'],
                'start': start_date.strftime('%Y-%m-%d'),
                'end': end_date.strftime('%Y-%m-%d'),
                'duration': task['duration']
            })
            
            current_date = start_date
        
        return pd.DataFrame(reversed(schedule))
    
# 使用例
scheduler = ResearchScheduler(deadline='2025-12-31', project_name='Asian ROA Study')

# タスク登録
scheduler.add_task('Final proofreading', 2)
scheduler.add_task('Co-author review', 5)
scheduler.add_task('Robustness checks', 7)
scheduler.add_task('Main analysis', 10)
scheduler.add_task('Data cleaning', 10)
scheduler.add_task('Data collection', 14)

# スケジュール出力
schedule = scheduler.generate_schedule()
print(schedule)
```

**推奨スケジュール（投稿まで3ヶ月の場合）**:
```
Week 1-2:  データ収集
Week 3-4:  データクリーニング
Week 5-6:  主要分析
Week 7-8:  頑健性検証
Week 9:    論文執筆
Week 10:   共著者レビュー
Week 11:   修正・改訂
Week 12:   最終校正・投稿

バッファ: 各フェーズに20%の余裕を持たせる
```

---

## 6. 失敗を防ぐ10のチェックポイント

### 日次チェック
1. ✅ データのバックアップ実施
2. ✅ 作業ログを記録
3. ✅ 進捗をトラッキング

### 週次チェック
4. ✅ 共著者とのコミュニケーション
5. ✅ スケジュールの見直し
6. ✅ 技術的問題の早期発見

### 月次チェック
7. ✅ 全体進捗の評価
8. ✅ 代替計画の準備
9. ✅ 文献レビューの更新

### マイルストーンチェック
10. ✅ 外部レビュー依頼（投稿前）

---

## 7. リカバリープラン

### 「データが消えた」場合
1. 冷静になる（パニックは禁物）
2. 最後のバックアップを確認
3. クラウド同期をチェック
4. データソースから再取得
5. 今後の防止策を実施

### 「締切に間に合わない」場合
1. 優先順位を明確化
2. 最小限の成果を定義
3. 延長可能か確認
4. 協力者に助けを求める
5. 次回のための教訓を記録

### 「分析結果が予想と逆」の場合
1. コードの検証
2. データの再確認
3. 理論の再検討
4. 代替的説明の探索
5. 正直に報告（negative results も価値あり）

---

**Version履歴**:
- v1.0 (2024-01-15): 初版
- v2.0 (2025-10-31): 実装コード追加、リカバリープラン拡充

**関連ドキュメント**:
- [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md)
- [TROUBLESHOOTING_FAQ.md](TROUBLESHOOTING_FAQ.md)
- [DATA_ETHICS_GUIDE.md](DATA_ETHICS_GUIDE.md)
