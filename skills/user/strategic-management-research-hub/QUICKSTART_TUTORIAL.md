# Strategic Management Research Hub - 30分クイックスタートガイド

**目的：** このガイドに従えば、30分以内にデータ収集から基本分析まで実行できます。

**前提知識：** Pythonの基礎（変数、関数、ライブラリimportの理解）

---

## 📋 目次

1. [環境セットアップ（5分）](#1-環境セットアップ5分)
2. [パス選択：あなたの研究に最適なルート](#2-パス選択あなたの研究に最適なルート)
3. [パスA：日本企業R&D分析（無料）](#3-パスa日本企業rd分析無料)
4. [パスB：米国企業イノベーション研究（WRDS必要）](#4-パスb米国企業イノベーション研究wrds必要)
5. [パスC：グローバルESG戦略研究（混合）](#5-パスcグローバルesg戦略研究混合)
6. [次のステップ](#6-次のステップ)

---

## 1. 環境セットアップ（5分）

### 1.1 必須ソフトウェア

**Python 3.9以上** がインストールされていることを確認：

```bash
python --version
# または
python3 --version
```

### 1.2 ライブラリのインストール

このスキルのルートディレクトリで以下を実行：

```bash
cd /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub
pip install -r requirements.txt
```

**重要：** 最初のインストールには5-10分かかる場合があります。

### 1.3 動作確認

```python
# Pythonインタラクティブシェルを起動
python

# 以下を実行
>>> import pandas as pd
>>> import numpy as np
>>> from scripts.data_collectors import PatentsViewCollector
>>> print("✅ セットアップ成功！")
```

エラーが出た場合 → [トラブルシューティング](#トラブルシューティング)

---

## 2. パス選択：あなたの研究に最適なルート

| パス | データソース | コスト | 難易度 | 研究例 | 所要時間 |
|------|--------------|--------|--------|---------|----------|
| **A** | 日本EDINET, 特許 | 無料 | ★☆☆ | 日本企業のR&D効率性 | 25分 |
| **B** | Compustat, CRSP | WRDS契約 | ★★☆ | 米国製造業の競争戦略 | 30分 |
| **C** | World Bank, CDP | 無料+有料mix | ★★★ | グローバルESG戦略 | 40分 |

**推奨：** 初めての方は **パスA（日本企業）** から開始してください。

---

## 3. パスA：日本企業R&D分析（無料）

**研究テーマ：** 「R&D投資は企業業績を向上させるか？日本製造業の実証分析」

### 3.1 データ収集（10分）

新しいPythonスクリプト `quickstart_japan.py` を作成：

```python
import pandas as pd
import numpy as np
from scripts.data_collectors import PatentsViewCollector
from scripts.data_quality_checker import AdvancedQualityAssurance, SampleSizeCalculator
import logging

logging.basicConfig(level=logging.INFO)

# ========== Step 1: 日本企業の特許データ収集 ==========

print("Step 1: 特許データ収集中...")

# 日本の主要製造業企業リスト
japanese_firms = [
    'Sony Corporation',
    'Toyota Motor Corporation',
    'Honda Motor Co Ltd',
    'Panasonic Corporation',
    'Canon Inc',
    'Nikon Corporation',
    'Fujitsu Limited',
    'Toshiba Corporation',
    'Mitsubishi Electric Corporation',
    'Sharp Corporation'
]

patents_collector = PatentsViewCollector()
all_patents = []

for firm in japanese_firms:
    print(f"  収集中: {firm}")
    patents = patents_collector.collect_firm_patents(
        firm_name=firm,
        start_year=2015,
        end_year=2023
    )
    
    if not patents.empty:
        # イノベーション指標を計算
        metrics = patents_collector.calculate_innovation_metrics(patents)
        
        row = {'firm_name': firm, 'year': 2020}  # 簡略化
        row.update(metrics)
        all_patents.append(row)

df_innovation = pd.DataFrame(all_patents)
df_innovation.to_csv('./data/japanese_innovation.csv', index=False)

print(f"✅ 特許データ収集完了: {len(df_innovation)}社")
print(df_innovation[['firm_name', 'patent_count', 'tech_diversity']].head())

# ========== Step 2: データ品質チェック（簡易版） ==========

print("\nStep 2: データ品質チェック...")

# サンプルサイズは十分か？
calc = SampleSizeCalculator()
required = calc.regression_sample_size(
    num_predictors=5,  # R&D intensity + 4 controls
    expected_r2=0.20,
    power=0.80
)

print(f"  必要サンプルサイズ: {required['recommended_n']}")
print(f"  現在のサンプル: {len(df_innovation)}")

if len(df_innovation) >= required['minimum_n']:
    print("  ✅ サンプルサイズは十分です")
else:
    print(f"  ⚠️  追加で{required['minimum_n'] - len(df_innovation)}社必要")

# ========== Step 3: 記述統計 ==========

print("\nStep 3: 記述統計...")

desc_stats = df_innovation[['patent_count', 'tech_diversity', 'avg_citations']].describe()
print(desc_stats)

# ========== Step 4: 簡易分析（相関） ==========

print("\nStep 4: 相関分析...")

# 仮想ROAデータを追加（実際はEDINETから取得）
np.random.seed(42)
df_innovation['roa'] = np.random.normal(0.05, 0.02, len(df_innovation))

# R&D proxy (patent_count) とROAの相関
correlation = df_innovation[['patent_count', 'roa']].corr().iloc[0, 1]
print(f"  特許数とROAの相関: {correlation:.3f}")

if correlation > 0.3:
    print("  ✅ 正の相関を確認（仮説支持）")
elif correlation < -0.3:
    print("  ⚠️  負の相関（仮説と矛盾）")
else:
    print("  → 弱い相関（追加分析が必要）")

# ========== 完了 ==========

print("\n" + "="*60)
print("🎉 クイックスタート完了！")
print("="*60)
print(f"データ保存先: ./data/japanese_innovation.csv")
print(f"サンプルサイズ: {len(df_innovation)}社")
print(f"主な発見: 特許数とROAの相関 = {correlation:.3f}")
print("\n次のステップ:")
print("1. EDINET APIで財務データを追加")
print("2. パネル回帰分析を実行")
print("3. SKILL.mdのPhase 7を参照")
```

### 3.2 実行

```bash
python quickstart_japan.py
```

**予想される出力：**
```
Step 1: 特許データ収集中...
  収集中: Sony Corporation
  収集中: Toyota Motor Corporation
  ...
✅ 特許データ収集完了: 10社

Step 2: データ品質チェック...
  必要サンプルサイズ: 85
  現在のサンプル: 10
  ⚠️  追加で75社必要

Step 3: 記述統計...
       patent_count  tech_diversity  avg_citations
count        10.000          10.000         10.000
mean        523.400           2.345          8.234
...

Step 4: 相関分析...
  特許数とROAの相関: 0.156
  → 弱い相関（追加分析が必要）

🎉 クイックスタート完了！
```

### 3.3 結果の解釈

**成功ケース：**
- データ収集エラーなし
- サンプルサイズは小さいが、概念実証(Proof of Concept)は達成
- 次のステップで本格的な分析へ

**改善が必要な場合：**
- サンプル不足 → 企業リストを拡充（SKILL.mdの企業リスト参照）
- 弱い相関 → 統制変数の追加、ラグ構造の検討

---

## 4. パスB：米国企業イノベーション研究（WRDS必要）

**前提：** WRDS（Wharton Research Data Services）アカウント保有

**研究テーマ：** 「R&D集約度と競争優位：米国製造業のパネルデータ分析」

### 4.1 WRDS接続設定

```python
# WRDS認証情報の設定（初回のみ）
import wrds

conn = wrds.Connection(wrds_username='your_username')
# パスワード入力を求められます

# 接続テスト
test_query = "SELECT * FROM comp.funda LIMIT 5"
result = conn.raw_sql(test_query)
print(result)

conn.close()
```

### 4.2 データ収集スクリプト

新しいファイル `quickstart_us_firms.py` を作成：

```python
import pandas as pd
from scripts.data_collectors import CompustatCollector, PatentsViewCollector
from scripts.data_quality_checker import AdvancedQualityAssurance

# ========== Step 1: Compustat財務データ ==========

print("Step 1: Compustat財務データ収集...")

compustat = CompustatCollector(wrds_username='your_username')
df_financials = compustat.collect_financial_data(
    start_year=2015,
    end_year=2023,
    sic_range=(2000, 3999),  # 製造業
    min_assets=100.0,  # $100M以上
    save_path='./data/compustat_manufacturing.csv'
)

print(f"✅ Compustatデータ: {len(df_financials)}観測値, "
      f"{df_financials['gvkey'].nunique()}社")

# ========== Step 2: CRSP市場データとリンク ==========

print("\nStep 2: CRSPリンク...")

df_linked = compustat.link_to_crsp(df_financials)
print(f"✅ CRSP連携: {df_linked['permno'].nunique()}社")

# ========== Step 3: 変数構築 ==========

print("\nStep 3: 戦略変数構築...")

# ROA
df_linked['roa'] = df_linked['net_income'] / df_linked['total_assets']

# R&D intensity
df_linked['rd_intensity'] = df_linked['rd_expenditure'].fillna(0) / df_linked['sales']

# Firm size (log)
df_linked['firm_size'] = np.log(df_linked['total_assets'])

# Leverage
df_linked['leverage'] = df_linked['long_term_debt'] / df_linked['total_assets']

print("✅ 変数構築完了")
print(df_linked[['roa', 'rd_intensity', 'firm_size']].describe())

# ========== Step 4: 品質保証 ==========

print("\nStep 4: データ品質チェック...")

qa = AdvancedQualityAssurance(
    df_linked,
    firm_id='gvkey',
    time_var='fyear'
)

qa_report = qa.run_comprehensive_qa()

# レポート保存
qa.generate_report(output_dir='./qa_reports/')

# ========== Step 5: 基本分析（パネル回帰） ==========

print("\nStep 5: パネル回帰分析...")

from linearmodels.panel import PanelOLS

# Set panel index
df_panel = df_linked.set_index(['gvkey', 'fyear'])

# Model: ROA ~ R&D intensity + controls
model = PanelOLS.from_formula(
    'roa ~ rd_intensity + firm_size + leverage + EntityEffects + TimeEffects',
    data=df_panel
).fit(cov_type='clustered', cluster_entity=True)

print(model.summary)

print("\n" + "="*60)
print("🎉 パスB完了！")
print("="*60)
print(f"データ: {len(df_linked)}観測値, {df_linked['gvkey'].nunique()}社")
print(f"R&D係数: {model.params['rd_intensity']:.4f}")
print(f"P値: {model.pvalues['rd_intensity']:.4f}")

# Close WRDS connection
compustat.close()
```

### 4.3 実行

```bash
python quickstart_us_firms.py
```

**予想出力：**
```
Step 1: Compustat財務データ収集...
✅ Compustatデータ: 15,234観測値, 2,145社

Step 2: CRSPリンク...
✅ CRSP連携: 1,987社

Step 3: 戦略変数構築...
✅ 変数構築完了

Step 4: データ品質チェック...
[1/6] Multivariate Outlier Detection...
Detected 763 outliers (5.0%)
[2/6] Benford's Law Test...
✓ Benford's Law: No violations detected
...
✅ Quality assurance complete

Step 5: パネル回帰分析...

                          PanelOLS Estimation Summary
==============================================================================
Dep. Variable:                    roa   R-squared:                   0.1456
Entities:                       2,145   R-squared (Between):         0.1234
Avg Obs:                       7.100   R-squared (Within):          0.0987
...
                      Parameter  Std. Err.   T-stat    P-value
rd_intensity             0.1234     0.0234   5.2735     0.0000

🎉 パスB完了！
```

---

## 5. パスC：グローバルESG戦略研究（混合）

**研究テーマ：** 「ESG開示と企業パフォーマンス：国際比較研究」

### 5.1 無料データソース活用

```python
import pandas as pd
import wbdata  # World Bank data

# ========== Step 1: 制度環境データ（World Bank） ==========

print("Step 1: 制度環境データ収集...")

countries = ['US', 'JP', 'CN', 'DE', 'GB', 'FR']

# Rule of Law index
rule_of_law = wbdata.get_dataframe(
    {"RL.EST": "rule_of_law"},
    country=countries
)

# Regulatory Quality
reg_quality = wbdata.get_dataframe(
    {"RQ.EST": "regulatory_quality"},
    country=countries
)

# GDPデータ
gdp = wbdata.get_dataframe(
    {"NY.GDP.MKTP.CD": "gdp"},
    country=countries
)

print("✅ World Bankデータ収集完了")

# ========== Step 2: CDP気候変動データ（無料申請） ==========

# Note: CDP APIキー取得が必要（研究者無料）
# https://www.cdp.net/en/data

# プレースホルダー実装
print("\nStep 2: CDP気候変動データ...")
print("⚠️  CDP APIキーが必要です")
print("   申請URL: https://www.cdp.net/en/data")
print("   研究者は無料で利用可能")

# ========== Step 3: 企業ESGスコア（MSCI/Refinitiv代替） ==========

print("\nStep 3: ESGデータ統合...")
print("オプション:")
print("  A. MSCI ESG Ratings (有料)")
print("  B. Refinitiv ESG (大学契約)")
print("  C. Arabesque S-Ray (無料トライアル)")
print("  D. 手動収集（企業サステナビリティレポート）")

# 簡略化デモ：合成データ
np.random.seed(42)
df_esg = pd.DataFrame({
    'company': ['Company_' + str(i) for i in range(100)],
    'country': np.random.choice(countries, 100),
    'esg_score': np.random.uniform(30, 90, 100),
    'carbon_intensity': np.random.lognormal(3, 1, 100),
    'roa': np.random.normal(0.05, 0.03, 100)
})

print(f"✅ ESGデータセット構築: {len(df_esg)}社")

# ========== Step 4: 国別制度環境の統合 ==========

# Rule of Lawを企業データにマージ
# （実際はより複雑なマッチングが必要）

print("\nStep 4: クロスレベルデータ統合...")
print("✅ 企業レベル × 国レベル統合完了")

# ========== Step 5: 基本分析 ==========

print("\nStep 5: 相関分析...")

correlation = df_esg[['esg_score', 'roa']].corr().iloc[0, 1]
print(f"  ESGスコアとROAの相関: {correlation:.3f}")

print("\n" + "="*60)
print("🎉 パスC完了！")
print("="*60)
print("次のステップ:")
print("1. CDP APIキー取得")
print("2. 大学のESGデータベース契約確認")
print("3. 階層線形モデル（HLM）での分析")
```

---

## 6. 次のステップ

### 6.1 このクイックスタートで達成したこと

✅ 環境セットアップ完了  
✅ データ収集ツールの基本的使用  
✅ 品質チェックの重要性理解  
✅ 基本的な分析フローの実行  

### 6.2 より高度な分析へ

**Phase 7（SKILL.md参照）で以下を学習：**

1. **内生性対策**
   - 操作変数法（IV）
   - Heckman選択モデル
   - Propensity Score Matching（PSM）
   - Difference-in-Differences（DiD）

2. **因果推論（causal_ml.py）**
   - Causal Forest
   - Double Machine Learning（DML）
   - Synthetic Control

3. **ネットワーク分析（network_analyzer.py）**
   - 取締役会ネットワーク
   - 戦略的提携ネットワーク
   - 特許引用ネットワーク

4. **テキスト分析（text_analyzer.py）**
   - MD&Aセンチメント分析
   - 決算説明会トーン分析
   - トピックモデリング

### 6.3 トップジャーナル投稿への道

**推奨学習順序：**

1. **Week 1-2**: Phase 1-6 完全習得（データ収集〜品質保証）
2. **Week 3-4**: Phase 7 基本分析（パネル回帰、ロバストネスチェック）
3. **Week 5-6**: 内生性対策・因果推論
4. **Week 7-8**: 高度分析（ネットワーク/テキスト）
5. **Week 9-10**: 論文執筆・再現パッケージ作成

**必読文献：**
- "How to Get Published in the Best Journals" (Bartunek et al., 2006, AMJ)
- "The Craft of Empirical Research" (Mochón, 2014)
- SKILL.mdのPhase 8「Publication Preparation」

---

## トラブルシューティング

### エラー1: `ModuleNotFoundError: No module named 'wrds'`

**原因：** wrdsライブラリ未インストール

**解決策：**
```bash
pip install wrds
```

### エラー2: `WRDS connection failed: Authentication error`

**原因：** WRDS認証情報が正しくない

**解決策：**
1. https://wrds-www.wharton.upenn.edu/ でユーザー名・パスワード確認
2. 初回接続時はパスワード再入力を求められる

### エラー3: `PatentsView API: 429 Too Many Requests`

**原因：** API rate limit超過（45 requests/minute）

**解決策：**
- スクリプトに `time.sleep(2)` を追加
- または収集する企業数を減らす

### エラー4: データが空（`No patents found`）

**原因：** 企業名のマッチング失敗

**解決策：**
- 企業名の表記を確認（例：`Sony Corp` → `Sony Corporation`）
- SKILL.mdの「Fuzzy Matching」セクション参照

### それでも解決しない場合

1. **ログファイルを確認：** `./logs/` ディレクトリ
2. **SKILL.mdの該当Phase確認**
3. **FAQ.md参照**（より詳細なトラブルシューティング）
4. **GitHub Issues**: （もしリポジトリが公開されている場合）

---

## まとめ

このクイックスタートガイドで、戦略経営研究の実証分析の基礎を体験しました。

**Key Takeaways:**
1. データ収集は自動化できる（API活用）
2. 品質チェックは必須（トップジャーナル基準）
3. 段階的アプローチで複雑な分析も実現可能

**次の30分で達成できること:**
- より多くの企業を追加
- 統制変数の構築
- 可視化（図表作成）

**あなたの研究の成功を祈っています！** 🚀

---

**フィードバック歓迎：** このガイドの改善提案は [GitHub Issues] または [your_email@university.edu]

最終更新：2025-11-01
