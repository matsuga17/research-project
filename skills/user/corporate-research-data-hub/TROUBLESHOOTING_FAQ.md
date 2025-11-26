# トラブルシューティングFAQ
## よくある問題と解決策

**Version**: 2.0  
**最終更新**: 2025-10-31

---

## データ収集の問題

### Q1: APIエラー「429 Too Many Requests」が出る

**原因**: レート制限超過

**解決策**:
```python
import time

# リトライ機能付き実装
def collect_with_rate_limit(ids, delay=2):
    results = []
    for i, id in enumerate(ids):
        try:
            data = api.get(id)
            results.append(data)
            
            # 進捗表示
            if (i+1) % 10 == 0:
                print(f"Progress: {i+1}/{len(ids)}")
            
            # レート制限対策
            time.sleep(delay)
            
        except Exception as e:
            if '429' in str(e):
                print(f"Rate limit hit. Waiting 60s...")
                time.sleep(60)
                data = api.get(id)  # リトライ
                results.append(data)
    
    return results
```

---

### Q2: データが文字化けする

**原因**: エンコーディングの不一致

**解決策**:
```python
# 日本語データ
df = pd.read_csv('data.csv', encoding='utf-8-sig')  # BOM付きUTF-8
# または
df = pd.read_csv('data.csv', encoding='shift_jis')  # Shift-JIS

# 中国語データ
df = pd.read_csv('data.csv', encoding='gb18030')

# エンコーディング自動検出
import chardet
with open('data.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result['encoding'])

df = pd.read_csv('data.csv', encoding=result['encoding'])
```

---

### Q3: マージ後にデータが激減した

**診断**:
```python
# マージ診断ツール使用
from corporate_data_utils import diagnostic_merge

merged = diagnostic_merge(df1, df2, key='firm_id', how='inner')
# 自動的にマッチ率を表示し、アンマッチをCSVに出力
```

**よくある原因**:
1. IDの形式不一致（全角/半角、大文字/小文字）
2. 欠損値
3. 時期のずれ

---

## データクリーニングの問題

### Q4: 欠損値が多すぎる（>50%）

**対処法**:
```python
# 1. 欠損パターンを分析
import missingno as msno
msno.matrix(df)
msno.heatmap(df)

# 2. 欠損のランダム性を検定
from scipy import stats
# Little's MCAR test実装
# H0: Missing Completely At Random

# 3. 対応方針
if missing_rate < 5%:
    strategy = 'Listwise deletion'
elif missing_pattern == 'MCAR':
    strategy = 'Multiple imputation'
else:
    strategy = 'Model-based imputation or exclude variable'
```

---

### Q5: 会計恒等式が成立しない

**確認手順**:
```python
# 総資産 = 総負債 + 純資産
df['accounting_check'] = abs(
    df['total_assets'] - (df['total_liabilities'] + df['equity'])
) / df['total_assets']

# 許容誤差: 1%
problematic = df[df['accounting_check'] > 0.01]
print(f"Problematic observations: {len(problematic)}")

# 原因を調査
problematic[['firm_id', 'year', 'total_assets', 
            'total_liabilities', 'equity']].to_csv('accounting_errors.csv')
```

**対処**:
1. 元データを確認（転記ミス？）
2. 単位の不一致を確認（百万 vs. 十億）
3. 誤差が大きい観測は除外を検討

---

## 統計分析の問題

### Q6: 回帰結果が不安定（係数の符号が変わる）

**原因**: 多重共線性

**診断**:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF計算
X = df[['rd_intensity', 'log_assets', 'leverage', 'age']]
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print(vif_data)
# VIF > 10 は問題あり
```

**対処**:
1. 高相関変数の除去
2. 主成分分析（PCA）
3. 正則化回帰（Ridge, Lasso）

---

### Q7: 「ConvergenceWarning」が出る

**原因**: 最適化アルゴリズムが収束しない

**解決策**:
```python
# 1. 変数のスケーリング
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. イテレーション数を増やす
model = LogisticRegression(max_iter=1000)

# 3. ソルバーを変更
model = LogisticRegression(solver='saga')
```

---

## コンピューティングの問題

### Q8: メモリ不足エラー

**解決策**:
```python
# 1. チャンク処理
chunksize = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunksize):
    process(chunk)

# 2. データ型の最適化
df['firm_id'] = df['firm_id'].astype('category')
df['year'] = df['year'].astype('int16')

# 3. 不要な列を削除
df = df[required_columns]

# 4. Daskを使用（大規模データ）
import dask.dataframe as dd
ddf = dd.read_csv('large_file.csv')
```

---

### Q9: 処理が遅すぎる

**最適化**:
```python
# 1. ベクトル演算を使用
# 悪い例
for i in range(len(df)):
    df.loc[i, 'new_var'] = df.loc[i, 'x'] * df.loc[i, 'y']

# 良い例
df['new_var'] = df['x'] * df['y']

# 2. apply()ではなくベクトル演算
# 遅い
df['log_assets'] = df['assets'].apply(lambda x: np.log(x))

# 速い
df['log_assets'] = np.log(df['assets'])

# 3. 並列処理
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(process_firm, firm_ids)
```

---

## 論文執筆の問題

### Q10: LaTeXがコンパイルできない

**よくあるエラー**:
```latex
% 1. パッケージ不足
% → インストール: tlmgr install [package]

% 2. 特殊文字エスケープ
% 悪い例
R^2 is 0.358
% 良い例
R\textsuperscript{2} is 0.358

% 3. 参考文献エラー
% → bibtex実行を忘れずに
% pdflatex → bibtex → pdflatex → pdflatex
```

---

### Q11: 表が入らない（too wide）

**解決策**:
```latex
% 1. フォントサイズ縮小
\begin{table}
\small  % または \footnotesize
\begin{tabular}{...}
...
\end{tabular}
\end{table}

% 2. 横置き
\begin{sidewaystable}
...
\end{sidewaystable}

% 3. 列幅調整
\begin{tabular}{p{3cm}p{2cm}p{2cm}}
...
\end{tabular}
```

---

## 投稿・査読の問題

### Q12: Desk rejectされた

**次のステップ**:
1. エディターレターを熟読
2. 改善可能な点を特定
3. 必要に応じて大幅改訂
4. 他ジャーナルへ投稿

**Desk rejectの主な理由**:
- ジャーナルのスコープ外
- 貢献が不明確
- 方法論に重大な欠陥
- 文章の質が低い

---

### Q13: 査読が厳しすぎる

**対応**:
```markdown
# 建設的な対応例

We appreciate the reviewer's thorough and constructive feedback. 
We have addressed all concerns as follows:

**Major Concern 1**: Endogeneity issue
Response: We have added [3 new analyses]...

**Major Concern 2**: Sample selection bias
Response: We now include [Heckman correction]...

While we have made substantial revisions, we acknowledge that 
[limitation X] remains. We have added discussion of this 
limitation on page [Y].
```

---

## 緊急時の対応

### データ消失
1. ✅ 最新バックアップを確認
2. ✅ クラウド同期をチェック
3. ✅ データソースから再取得
4. ✅ 今後の防止策実施

### 締切直前のエラー
1. ✅ 優先順位を明確化
2. ✅ 最小限の修正に集中
3. ✅ 延長可能か確認
4. ✅ 共著者に連絡

---

## サポート情報

### コミュニティ
- Stack Overflow（プログラミング）
- Cross Validated（統計）
- ResearchGate（学術全般）

### 推奨リソース
- Python: pandas documentation
- 統計: UCLA IDRE Statistical Consulting
- LaTeX: Overleaf documentation

---

**それでも解決しない場合**:

1. GitHub Issuesに報告
2. 詳細なエラーメッセージを含める
3. 再現可能な最小例を提供

---

**関連ドキュメント**:
- [COMMON_PITFALLS.md](COMMON_PITFALLS.md) - よくある失敗例
- [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) - 投稿前チェックリスト

**Version履歴**:
- v1.0 (2024-01-15): 初版
- v2.0 (2025-10-31): FAQを40問から13問に厳選、実用的な解決策を追加
