# Strategic Management Research Hub - FAQ

**よくある質問と即座解決ガイド**

最終更新：2025-11-01

---

## 📋 目次

1. [インストール・環境設定](#1-インストール環境設定)
2. [データ収集エラー](#2-データ収集エラー)
3. [データ品質問題](#3-データ品質問題)
4. [分析エラー](#4-分析エラー)
5. [結果の解釈](#5-結果の解釈)
6. [パフォーマンス最適化](#6-パフォーマンス最適化)

---

## 1. インストール・環境設定

### Q1.1: `ModuleNotFoundError: No module named 'XXX'`

**症状：** Pythonスクリプト実行時にライブラリが見つからない

**原因：** 依存ライブラリが未インストール

**解決策：**

```bash
# 全ライブラリを一括インストール
cd /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub
pip install -r requirements.txt

# 特定のライブラリのみ
pip install pandas numpy scipy statsmodels
```

**よくあるケース：**
- `wrds`：WRDS契約者のみ必要 → `pip install wrds`
- `econml`：因果推論用（オプション）→ `pip install econml`
- `transformers`：FinBERT用（大容量）→ `pip install transformers torch`

---

### Q1.2: pip install が遅い・タイムアウトする

**原因：** ネットワーク速度、またはPyPIサーバー混雑

**解決策：**

```bash
# ミラーサイト使用（中国ユーザー向け）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# タイムアウト時間延長
pip install --timeout 300 -r requirements.txt

# 既存ライブラリをスキップ
pip install -r requirements.txt --upgrade --ignore-installed
```

---

### Q1.3: Python仮想環境の作成方法

**推奨理由：** プロジェクトごとに独立した環境、依存関係の衝突回避

**手順：**

```bash
# venv使用（Python標準）
cd /Users/changu/Desktop/研究/skills/user/strategic-management-research-hub
python -m venv venv_strategy

# 仮想環境有効化
# macOS/Linux:
source venv_strategy/bin/activate
# Windows:
venv_strategy\Scripts\activate

# ライブラリインストール
pip install -r requirements.txt

# 無効化
deactivate
```

**conda使用の場合：**

```bash
conda create -n strategy_research python=3.10
conda activate strategy_research
pip install -r requirements.txt
```

---

## 2. データ収集エラー

### Q2.1: WRDS接続エラー「Authentication failed」

**症状：**
```python
wrds.Connection(wrds_username='your_username')
# Error: Authentication failed
```

**原因：**
1. ユーザー名・パスワードが正しくない
2. WRDSアカウントが期限切れ
3. 初回接続時の認証未完了

**解決策：**

```python
# ステップ1：認証情報の確認
# https://wrds-www.wharton.upenn.edu/ でログインテスト

# ステップ2：初回設定（パスワード保存）
import wrds
conn = wrds.Connection(wrds_username='actual_username')
# パスワード入力を求められる → 入力

# ステップ3：接続テスト
test = conn.raw_sql("SELECT * FROM comp.funda LIMIT 5")
print(test)

conn.close()
```

**それでも失敗する場合：**
- WRDS Help Desk連絡：wrds@wharton.upenn.edu
- 大学のWRDS管理者に確認

---

### Q2.2: PatentsView API エラー「429 Too Many Requests」

**症状：**
```
requests.exceptions.HTTPError: 429 Client Error: Too Many Requests
```

**原因：** API Rate Limit超過（45 requests/minute）

**解決策：**

```python
# 方法1：待機時間を追加
import time

for firm in firm_list:
    patents = collector.collect_firm_patents(firm, 2020, 2023)
    time.sleep(2)  # 2秒待機

# 方法2：バッチサイズを減らす
# 一度に取得する企業数を減らす
firm_list_batch1 = firm_list[:50]  # 最初の50社
# 処理後、次のバッチ

# 方法3：rate_limitデコレーターを調整
# data_collectors.pyの@limitsパラメータを変更
# @limits(calls=30, period=60)  # より保守的に
```

---

### Q2.3: EDINET API から空のデータが返される

**症状：**
```python
df = edinet.collect_sample('2023-01-01', '2023-12-31', ['010'])
# 結果: 0行のDataFrame
```

**原因：**
1. 指定日に報告書提出なし
2. 産業コードが間違っている
3. APIリクエストパラメータの誤り

**解決策：**

```python
# デバッグ：特定日のドキュメントリスト確認
docs = edinet.get_document_list('2023-06-30')
print(f"利用可能なドキュメント: {len(docs.get('results', []))}")
print(docs['results'][:3])  # 最初の3件表示

# 産業コード確認
# '010': 製造業（正）
# '001': 金融業
# '004': 運輸業

# 期間を拡大してテスト
df = edinet.collect_sample('2023-06-01', '2023-08-31', None)  # 全産業
print(f"取得: {len(df)}件")
```

---

### Q2.4: 企業名マッチングで一致しない（特許データ）

**症状：**
```python
patents = collector.collect_firm_patents('Sony', 2020, 2023)
# 結果: 0件
```

**原因：** 企業名表記のバリエーション

**解決策：**

```python
# 正式名称を使用
patents = collector.collect_firm_patents('Sony Corporation', 2020, 2023)

# または複数バリエーションで試行
name_variants = [
    'Sony Corporation',
    'Sony Corp',
    'Sony Group Corporation',
    'ソニー株式会社'
]

for name in name_variants:
    patents = collector.collect_firm_patents(name, 2020, 2023)
    if not patents.empty:
        print(f"成功: {name}")
        break

# Fuzzy matchingを使用
from fuzzywuzzy import process

# CompustatとPatentsの企業名マッチング
matched = patents_collector.match_companies_to_compustat(
    patents_df,
    compustat_df,
    threshold=85  # 類似度85%以上
)
```

---

## 3. データ品質問題

### Q3.1: 外れ値が多すぎる（>10%）

**症状：**
```
QA Report: 1,523 outliers detected (15.2%)
```

**原因：**
1. 極端な値が実際に存在（新興企業、特殊イベント）
2. データエラー（入力ミス、単位間違い）
3. Outlier検出のthresholdが厳しすぎる

**解決策：**

```python
# ステップ1：Outlierの詳細確認
high_conf_outliers = df[df['outlier_confidence'] >= 0.67]
print(high_conf_outliers[['firm_name', 'year', 'roa', 'total_assets']].head(20))

# ステップ2：Winsorization（外れ値を調整）
from scipy.stats.mstats import winsorize

df['roa_winsorized'] = winsorize(df['roa'], limits=[0.01, 0.01])
# 上下1%を調整

# ステップ3：業界別に標準化
df['roa_industry_adj'] = df.groupby('industry')['roa'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# ステップ4：Outlierフラグを使った分析
# メイン分析: Outlier除外
df_main = df[df['outlier_flag'] == 0]

# ロバストネスチェック: Outlier含む
df_robust = df  # 全サンプル
```

---

### Q3.2: Benford's Law違反が検出された

**症状：**
```
⚠️  Benford's Law violations detected: ['total_assets', 'sales']
```

**意味：** データに人為的操作の可能性

**対処法：**

```python
# ステップ1：違反の深刻度確認
benford_result = qa_report['benfords_law']
for var, test in benford_result['variable_tests'].items():
    if test['p_value'] < 0.05:
        print(f"{var}: χ² = {test['chi2_statistic']:.2f}, p = {test['p_value']:.4f}")

# ステップ2：データソース再確認
# - 元データに戻って検証
# - 他の変数（net_income, cash）も同様か確認

# ステップ3：既知の例外パターン確認
# Benford違反の正当な理由：
# - 最低資本金規制（例：$10M以上の企業のみ）
# - 産業特有の価格帯（例：航空機は$100M単位）
# - サンプリングバイアス

# ステップ4：論文での報告
# Limitationsセクションで明記：
# "Benford's Law test indicated potential data quality issues 
#  in [variables], possibly due to [regulatory thresholds/
#  industry characteristics]. We conducted robustness checks 
#  excluding these variables, and results remained consistent."
```

---

### Q3.3: パネルデータの高いAttrition Rate（>30%）

**症状：**
```
⚠️  High attrition rate: 35.2%
```

**問題：** Survival biasが分析結果を歪める可能性

**解決策：**

```python
# ステップ1：Attrition原因の特定
attrite_firms = df[df['attrite'] == 1]['firm_id'].unique()
survive_firms = df[df['attrite'] == 0]['firm_id'].unique()

# 特性比較
from scipy.stats import ttest_ind

for var in ['roa', 'firm_size', 'leverage']:
    t, p = ttest_ind(
        df[df['attrite'] == 1][var].dropna(),
        df[df['attrite'] == 0][var].dropna()
    )
    print(f"{var}: t={t:.2f}, p={p:.4f}")

# ステップ2：対処法の選択

# 方法A：Heckman Selection Model
from statsmodels.regression.linear_model import Heckman

# 第1段階：Attrition予測
# 第2段階：Selection補正後の本分析

# 方法B：Inverse Probability Weighting (IPW)
from sklearn.linear_model import LogisticRegression

# Attrition確率推定
lr = LogisticRegression()
lr.fit(df[['firm_size', 'roa', 'leverage']], df['attrite'])
df['prob_attrite'] = lr.predict_proba(df[['firm_size', 'roa', 'leverage']])[:, 1]

# IPW: Attritionしにくい企業に高いウェイトを付与
df['ipw'] = 1 / (1 - df['prob_attrite'])

# 加重回帰
# model = PanelOLS(...).fit(weights=df['ipw'])

# 方法C：Balanced panel onlyでRobustness check
df_balanced = df.groupby('firm_id').filter(
    lambda x: len(x) == df['year'].nunique()
)
```

---

## 4. 分析エラー

### Q4.1: VIF（分散インフレ係数）が10を超える

**症状：**
```
VIF Results:
  firm_size: 12.34
  rd_intensity: 15.67
```

**問題：** 多重共線性により係数推定が不安定

**解決策：**

```python
# ステップ1：相関行列で原因特定
corr_matrix = df[['firm_size', 'rd_intensity', 'leverage', 'firm_age']].corr()
print(corr_matrix)

# ステップ2：対処法

# 方法A：高相関変数の一方を除外
# firm_sizeとrd_intensityが高相関(r>0.7)なら、一方を削除

# 方法B：直交化（Residualizing）
# rd_intensity を firm_size で回帰し、残差を使用
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(df[['firm_size']], df['rd_intensity'])
df['rd_intensity_resid'] = df['rd_intensity'] - lr.predict(df[['firm_size']])

# Model: roa ~ rd_intensity_resid + firm_size + ...

# 方法C：主成分分析（PCA）
from sklearn.decomposition import PCA

pca = PCA(n_components=3)
X_pca = pca.fit_transform(df[['firm_size', 'rd_intensity', 'leverage']])
df['PC1'] = X_pca[:, 0]
df['PC2'] = X_pca[:, 1]

# Model: roa ~ PC1 + PC2 + ...
```

---

### Q4.2: パネル回帰で「Singular matrix」エラー

**症状：**
```python
model = PanelOLS.from_formula('roa ~ rd + size + EntityEffects', data=df_panel).fit()
# LinAlgError: Singular matrix
```

**原因：**
1. 完全共線性（ダミー変数トラップ）
2. 欠損値による自由度不足
3. Fixed effectsと時間不変変数の混在

**解決策：**

```python
# 原因1対処：ダミー変数の確認
# × 間違い: year_2020 + year_2021 + year_2022 + TimeEffects
# ○ 正しい: TimeEffects のみ（自動でダミー生成）

# 原因2対処：欠損値除去
df_panel_clean = df_panel.dropna(subset=['roa', 'rd', 'size'])

# 原因3対処：時間不変変数をFixed effectsから除外
# × 間違い: industry_dummy + EntityEffects（industry不変なら）
# ○ 正しい: industry_dummyを除外、EntityEffectsのみ

# デバッグ：変数の分散を確認
for var in ['rd', 'size', 'leverage']:
    within_var = df_panel.groupby('firm_id')[var].transform(lambda x: x - x.mean()).var()
    print(f"{var} within-variance: {within_var:.4f}")
    # within-variance ≈ 0 なら、Fixed effectsで消失
```

---

### Q4.3: 交互作用項の係数が非有意

**症状：**
```
Model: roa ~ rd * env_dynamism + controls
rd:env_dynamism coefficient: 0.023 (p=0.234)  # 非有意
```

**原因：**
1. 本当に交互作用がない（理論的予測が誤り）
2. サンプルサイズ不足（検出力不足）
3. 測定誤差により効果が希釈

**解決策：**

```python
# ステップ1：Simple slope分析で詳細確認
# env_dynamisが低・中・高のグループ別にrd効果を推定

low_dyn = df[df['env_dynamism'] < df['env_dynamism'].quantile(0.33)]
high_dyn = df[df['env_dynamism'] > df['env_dynamism'].quantile(0.67)]

# 低動態性グループ
model_low = PanelOLS.from_formula('roa ~ rd + controls', data=low_dyn).fit()
print(f"Low dynamism: rd coef = {model_low.params['rd']:.4f}")

# 高動態性グループ
model_high = PanelOLS.from_formula('roa ~ rd + controls', data=high_dyn).fit()
print(f"High dynamism: rd coef = {model_high.params['rd']:.4f}")

# 差が大きければ、交互作用は実質的に存在

# ステップ2：Moderator変数の測定改善
# env_dynamismを複数指標で測定
df['env_dynamism_composite'] = (
    df['sales_volatility'] +
    df['tech_change_rate'] +
    df['competitor_turnover']
) / 3

# ステップ3：検出力分析
from statsmodels.stats.power import TTestIndPower

# 期待される効果量での検出力確認
power_analysis = TTestIndPower()
required_n = power_analysis.solve_power(
    effect_size=0.3,  # 期待される交互作用の効果量
    alpha=0.05,
    power=0.80
)
print(f"Required N: {required_n:.0f}, Current N: {len(df)}")
```

---

## 5. 結果の解釈

### Q5.1: 係数の経済的有意性vs.統計的有意性

**症状：**
```
rd_intensity coefficient: 0.0023 (p=0.001)
```

**質問：** p<0.001で統計的に有意だが、係数0.0023は実務的に意味があるか？

**解答：**

```python
# 経済的有意性の評価

# 方法1：標準化係数（Beta）
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
df[['roa_std', 'rd_std']] = scaler.fit_transform(df[['roa', 'rd_intensity']])

model_std = PanelOLS.from_formula('roa_std ~ rd_std + controls', data=df_panel).fit()
print(f"Standardized coef: {model_std.params['rd_std']:.3f}")
# 解釈：rd_intensityが1SD増加 → ROAが{coef}SD変化

# 方法2：Marginal effect（限界効果）
# rd_intensityを1%ポイント増やすとROAへの影響
coef = 0.0023
rd_increase = 0.01  # 1%ポイント
roa_change = coef * rd_increase
print(f"RD 1pp増加 → ROA {roa_change*100:.2f}pp変化")

# 産業平均ROA=5%なら、0.0023*0.01 = 0.000023 (0.0023pp) の変化
# → 相対的に小さい

# 方法3：実例シミュレーション
mean_rd = df['rd_intensity'].mean()  # 例：0.03 (3%)
new_rd = mean_rd * 1.10  # 10%増加
predicted_roa_change = coef * (new_rd - mean_rd)
print(f"RD 10%増加 → ROA {predicted_roa_change*100:.3f}pp変化")

# 結論：統計的有意でも、経済的インパクトが小さい場合あり
# → Limitationsで議論、または測定精度の改善を検討
```

---

### Q5.2: Fixed effects vs. Random effects 選択

**質問：** どちらのモデルを使うべきか？

**決定プロセス：**

```python
from linearmodels.panel import PanelOLS, RandomEffects

# Model 1: Fixed Effects
model_fe = PanelOLS.from_formula(
    'roa ~ rd + controls + EntityEffects + TimeEffects',
    data=df_panel
).fit(cov_type='clustered', cluster_entity=True)

# Model 2: Random Effects
model_re = RandomEffects.from_formula(
    'roa ~ rd + controls',
    data=df_panel
).fit()

# Hausman Test（FE vs. RE）
from scipy.stats import chi2

# 簡易Hausman test
fe_coef = model_fe.params['rd']
re_coef = model_re.params['rd']
fe_se = model_fe.std_errors['rd']
re_se = model_re.std_errors['rd']

hausman_stat = ((fe_coef - re_coef) ** 2) / (fe_se**2 - re_se**2)
p_value = 1 - chi2.cdf(hausman_stat, df=1)

print(f"Hausman test: χ² = {hausman_stat:.2f}, p = {p_value:.4f}")

# 解釈：
# p < 0.05 → FE推奨（unobserved heterogeneityが相関）
# p > 0.05 → RE可（より効率的）

# 戦略研究の実務的ガイドライン：
# - 企業固有効果が重要な場合（通常） → Fixed Effects
# - クロスセクション変数（時間不変）が重要 → Random Effects
# - 不確かな場合 → 両方報告し、Hausman test結果を記載
```

---

## 6. パフォーマンス最適化

### Q6.1: 大規模データセットの処理が遅い

**症状：**
```python
df = pd.read_csv('large_dataset.csv')  # 10 GB, 100万行
# → メモリ不足、処理に1時間以上
```

**解決策：**

```python
# 方法1：Chunk読み込み
chunks = []
for chunk in pd.read_csv('large_dataset.csv', chunksize=10000):
    # 必要な列のみ選択
    chunk = chunk[['gvkey', 'year', 'roa', 'rd']]
    # フィルタリング
    chunk = chunk[chunk['year'] >= 2010]
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)

# 方法2：Dask使用（並列処理）
import dask.dataframe as dd

ddf = dd.read_csv('large_dataset.csv')
ddf_filtered = ddf[ddf['year'] >= 2010]
df = ddf_filtered.compute()  # Pandas DataFrameに変換

# 方法3：Parquet形式で保存（圧縮+高速）
# 初回
df.to_parquet('dataset.parquet', compression='snappy')

# 以降
df = pd.read_parquet('dataset.parquet')  # CSVより10-100倍高速

# 方法4：データ型最適化
df['year'] = df['year'].astype('int16')  # int64 → int16
df['gvkey'] = df['gvkey'].astype('category')  # objectより高速
```

---

### Q6.2: パネル回帰が遅すぎる（>10分）

**原因：** 大規模パネル（firms × years が大きい）

**解決策：**

```python
# 方法1：Clustered SEの計算を最小限に
model = PanelOLS(...).fit(cov_type='unadjusted')  # 最速
# Robustness checkでのみ clustered SE使用

# 方法2：サンプルサイズ削減（Pilot study）
df_sample = df.groupby('industry').sample(frac=0.1, random_state=42)
# 10%サンプルで高速テスト → 本番は全データ

# 方法3：Julia + FixedEffectModels.jl（最高速）
# Pythonより10-100倍高速
# 詳細：https://github.com/FixedEffects/FixedEffectModels.jl

# 方法4：Parallel processing
from joblib import Parallel, delayed

def run_regression(data_chunk):
    model = PanelOLS(..., data=data_chunk).fit()
    return model.params

results = Parallel(n_jobs=4)(
    delayed(run_regression)(chunk) 
    for chunk in data_chunks
)
```

---

## 追加サポート

### まだ解決しない場合

1. **ログファイル確認：** `./logs/pipeline.log`
2. **SKILL.md参照：** 詳細な技術文書
3. **GitHub Issues：** （公開リポジトリの場合）
4. **メール相談：** research@strategic-hub.edu（架空）

---

## フィードバック

このFAQに追加してほしい質問があれば、ぜひお知らせください。

**最終更新：** 2025-11-01  
**バージョン：** 3.0
