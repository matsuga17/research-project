# 分析パターン集

自然言語クエリから適切な分析コードへの変換パターン。

## 1. データ探索パターン

### 1.1 基本情報確認

```python
# データの形状
df.shape  # (行数, 列数)

# 先頭/末尾の確認
df.head(10)
df.tail(10)

# 列情報
df.info()
df.dtypes

# 基本統計
df.describe(include='all')
```

### 1.2 欠損値分析

```python
# 欠損数と欠損率
missing = pd.DataFrame({
    'missing': df.isnull().sum(),
    'missing_pct': df.isnull().mean() * 100
}).sort_values('missing', ascending=False)

# 欠損パターンの可視化
import missingno as msno
msno.matrix(df)
```

### 1.3 ユニーク値分析

```python
# 各列のユニーク値数
df.nunique()

# 特定列の値分布
df['column'].value_counts()
df['column'].value_counts(normalize=True)  # 割合
```

## 2. データクレンジングパターン

### 2.1 欠損値処理

```python
# 削除
df.dropna()                           # 全欠損行削除
df.dropna(subset=['col1', 'col2'])    # 特定列で判定
df.dropna(thresh=3)                   # 3つ以上の非欠損値がある行のみ保持

# 補完
df['col'].fillna(0)                   # 定数
df['col'].fillna(df['col'].mean())    # 平均
df['col'].fillna(df['col'].median())  # 中央値
df['col'].fillna(df['col'].mode()[0]) # 最頻値
df['col'].fillna(method='ffill')      # 前方補完
df['col'].fillna(method='bfill')      # 後方補完

# グループ別補完
df['col'] = df.groupby('group')['col'].transform(lambda x: x.fillna(x.median()))
```

### 2.2 重複処理

```python
# 重複確認
df.duplicated().sum()
df[df.duplicated(keep=False)]  # 重複行を全て表示

# 重複削除
df.drop_duplicates()
df.drop_duplicates(subset=['key_col'], keep='first')
```

### 2.3 外れ値処理

```python
# IQR法
Q1, Q3 = df['col'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR

# 外れ値の検出
outliers = df[(df['col'] < lower) | (df['col'] > upper)]

# 外れ値の除去
df_clean = df[(df['col'] >= lower) & (df['col'] <= upper)]

# キャッピング
df['col'] = df['col'].clip(lower, upper)

# Zスコア法
from scipy import stats
z_scores = np.abs(stats.zscore(df['col'].dropna()))
df_clean = df[z_scores < 3]
```

### 2.4 型変換

```python
# 日時変換
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# 数値変換
df['num'] = pd.to_numeric(df['num'], errors='coerce')

# カテゴリ変換
df['cat'] = df['cat'].astype('category')

# 文字列変換
df['str'] = df['str'].astype(str)
```

## 3. 集計・分析パターン

### 3.1 グループ集計

```python
# 基本集計
df.groupby('category')['value'].mean()
df.groupby('category')['value'].agg(['mean', 'sum', 'count', 'std'])

# 複数列でグループ化
df.groupby(['cat1', 'cat2'])['value'].mean()

# 複数の集計関数
df.groupby('category').agg({
    'value1': ['mean', 'sum'],
    'value2': ['min', 'max'],
    'value3': 'count'
})

# 名前付き集計（pandas >= 0.25）
df.groupby('category').agg(
    total=('value', 'sum'),
    average=('value', 'mean'),
    count=('id', 'nunique')
)
```

### 3.2 クロス集計

```python
# 基本
pd.crosstab(df['row'], df['col'])

# マージンあり
pd.crosstab(df['row'], df['col'], margins=True)

# 正規化
pd.crosstab(df['row'], df['col'], normalize='all')  # 全体
pd.crosstab(df['row'], df['col'], normalize='index')  # 行方向
pd.crosstab(df['row'], df['col'], normalize='columns')  # 列方向

# ピボットテーブル
df.pivot_table(values='value', index='row', columns='col', aggfunc='mean')
```

### 3.3 ランキング

```python
# 上位N件
df.nlargest(10, 'value')
df.nsmallest(10, 'value')

# グループ内ランキング
df['rank'] = df.groupby('category')['value'].rank(ascending=False)

# 累積
df['cumsum'] = df['value'].cumsum()
df['cumsum_pct'] = df['value'].cumsum() / df['value'].sum()
```

### 3.4 時系列分析

```python
# リサンプリング
df.set_index('date').resample('D').mean()   # 日次
df.set_index('date').resample('W').sum()    # 週次
df.set_index('date').resample('M').mean()   # 月次
df.set_index('date').resample('Q').sum()    # 四半期

# ローリング
df['rolling_mean'] = df['value'].rolling(window=7).mean()
df['rolling_std'] = df['value'].rolling(window=7).std()

# 前期比
df['pct_change'] = df['value'].pct_change()
df['diff'] = df['value'].diff()

# シフト
df['lag1'] = df['value'].shift(1)
df['lead1'] = df['value'].shift(-1)
```

## 4. 統計分析パターン

### 4.1 相関分析

```python
# ピアソン相関
df.corr()
df.corr(method='pearson')

# スピアマン相関
df.corr(method='spearman')

# 特定のペア
df['col1'].corr(df['col2'])

# 高相関ペアの抽出
corr_matrix = df.corr()
high_corr = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
high_corr_pairs = high_corr.stack().reset_index()
high_corr_pairs.columns = ['var1', 'var2', 'correlation']
high_corr_pairs = high_corr_pairs[abs(high_corr_pairs['correlation']) > 0.7]
```

### 4.2 仮説検定

```python
from scipy import stats

# t検定（2群比較）
group1 = df[df['group'] == 'A']['value']
group2 = df[df['group'] == 'B']['value']
t_stat, p_value = stats.ttest_ind(group1, group2)

# カイ二乗検定（独立性）
contingency = pd.crosstab(df['cat1'], df['cat2'])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

# 正規性検定
stat, p_value = stats.shapiro(df['value'])

# ANOVA（多群比較）
groups = [df[df['group'] == g]['value'] for g in df['group'].unique()]
f_stat, p_value = stats.f_oneway(*groups)
```

### 4.3 回帰分析

```python
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

# 単回帰
X = df[['x']]
y = df['y']
model = LinearRegression()
model.fit(X, y)
print(f"係数: {model.coef_[0]:.4f}, 切片: {model.intercept_:.4f}")

# 重回帰（statsmodels）
X = sm.add_constant(df[['x1', 'x2', 'x3']])
y = df['y']
model = sm.OLS(y, X).fit()
print(model.summary())
```

## 5. 自然言語→コードマッピング

| 自然言語表現 | 対応コード |
|------------|----------|
| 「〜の平均」「〜の平均値」 | `.mean()` |
| 「〜の合計」「〜の総計」 | `.sum()` |
| 「〜の件数」「〜の数」 | `.count()`, `len()` |
| 「〜の最大」「最も高い」 | `.max()`, `.idxmax()` |
| 「〜の最小」「最も低い」 | `.min()`, `.idxmin()` |
| 「〜の中央値」 | `.median()` |
| 「〜の標準偏差」 | `.std()` |
| 「上位N件」「トップN」 | `.nlargest(N, col)`, `.head(N)` |
| 「下位N件」「ワーストN」 | `.nsmallest(N, col)`, `.tail(N)` |
| 「〜別の」「〜ごとの」 | `.groupby(col)` |
| 「〜の分布」 | `.value_counts()`, `histplot` |
| 「〜と〜の関係」「〜と〜の相関」 | `.corr()`, `scatterplot` |
| 「〜の傾向」「〜の推移」 | 時系列プロット |
| 「〜を除外」「〜以外」 | `df[df['col'] != value]` |
| 「〜以上」「〜を超える」 | `df[df['col'] >= value]` |
| 「〜以下」「〜未満」 | `df[df['col'] <= value]` |
| 「〜を含む」「〜がある」 | `df[df['col'].str.contains(pattern)]` |
| 「欠損を削除」 | `.dropna()` |
| 「欠損を補完」 | `.fillna()` |
| 「重複を削除」 | `.drop_duplicates()` |
| 「ソート」「並び替え」 | `.sort_values()` |

## 6. エラー対処パターン

### メモリエラー

```python
# チャンクで読み込み
chunks = pd.read_csv(path, chunksize=100000)
df = pd.concat(chunks)

# 型の最適化
df['int_col'] = df['int_col'].astype('int32')
df['float_col'] = df['float_col'].astype('float32')
df['cat_col'] = df['cat_col'].astype('category')
```

### 日付パースエラー

```python
# フォーマット指定
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d', errors='coerce')

# 複数フォーマット対応
def parse_date(x):
    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y']:
        try:
            return pd.to_datetime(x, format=fmt)
        except:
            continue
    return pd.NaT

df['date'] = df['date_str'].apply(parse_date)
```

### 文字コードエラー

```python
# エンコーディング指定
df = pd.read_csv(path, encoding='utf-8')
df = pd.read_csv(path, encoding='shift-jis')
df = pd.read_csv(path, encoding='cp932')

# 自動検出
import chardet
with open(path, 'rb') as f:
    result = chardet.detect(f.read())
df = pd.read_csv(path, encoding=result['encoding'])
```
