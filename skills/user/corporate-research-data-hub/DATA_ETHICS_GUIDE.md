# データ倫理ガイド（Data Ethics Guide）
## 責任ある研究実践のための倫理的指針

**Version**: 2.0  
**最終更新**: 2025-10-31

---

## 1. 基本原則

### A. プライバシー保護

**必須対応**:
- [ ] 個人識別情報（PII）の匿名化
- [ ] データアクセスの制限
- [ ] 安全なストレージ使用

**匿名化チェックリスト**:
```python
# 削除・マスキングすべき情報
pii_columns = [
    'name', 'email', 'phone', 'address',
    'social_security_number', 'credit_card',
    'personal_id', 'passport_number'
]

# 匿名化処理
def anonymize_data(df):
    # 直接識別子の削除
    df = df.drop(columns=pii_columns, errors='ignore')
    
    # IDの再割り当て（連番化）
    df['anonymous_id'] = range(len(df))
    
    # 日付の粗視化（年-月のみ）
    df['date'] = pd.to_datetime(df['date']).dt.to_period('M')
    
    return df
```

---

### B. データ使用許諾

**確認事項**:
1. ✅ データソースの利用規約を読む
2. ✅ 学術利用が許可されているか確認
3. ✅ 再配布の可否を確認
4. ✅ 引用要件を満たす

**無料データソースの注意点**:
```
EDINET (日本): 学術利用OK、再配布OK、引用必須
Open DART (韓国): 学術利用OK、商用利用制限あり
Tushare (中国): 個人利用OK、商用ライセンス必要
```

---

### C. 透明性・再現性

**必須対応**:
- [ ] データソースを明記
- [ ] 処理手順を文書化
- [ ] コードを公開（可能な範囲で）
- [ ] Pre-registration実施（推奨）

**Data Availability Statement（例）**:
```
"Financial data were obtained from EDINET (https://disclosure.edinet-fsa.go.jp/), 
a public database maintained by Japan's Financial Services Agency. Stock price 
data were obtained from JPX (https://www.jpx.co.jp/). All data are publicly 
available. Replication code is available at [GitHub URL]."
```

---

## 2. 利益相反の開示

### A. 資金提供

**開示すべき情報**:
```
Funding: This research was supported by [Grant Name] from [Organization].
[Organization] had no role in study design, data collection, analysis, or 
the decision to publish.
```

### B. 企業との関係

**開示が必要なケース**:
- 研究対象企業との雇用関係
- 研究対象企業の株式保有
- コンサルティング契約
- 役員・顧問の兼任

---

## 3. データ共有

### A. 共有すべきもの

- ✅ クリーンデータ（匿名化済み）
- ✅ 分析コード
- ✅ Codebook
- ✅ README（実行手順）

### B. 共有の制約がある場合

```
"Due to data use agreements, we cannot publicly share the raw data. 
However, researchers can obtain the data from [source] by following 
the procedures outlined at [URL]. Our analysis code is available at 
[GitHub URL]."
```

---

## 4. よくある倫理的ジレンマ

### Q1: 非有意の結果を隠してもいい？
**A: いいえ。** Publication bias を防ぐため、すべての結果を報告すべき。

### Q2: データを少し調整して結果を改善してもいい？
**A: いいえ。** Data manipulation は研究不正。

### Q3: 予想と逆の結果が出たら？
**A: 正直に報告。** Negative results も科学的価値あり。

---

## 5. チェックリスト

投稿前に確認：

- [ ] プライバシー保護措置を実施
- [ ] データ使用許諾を確認
- [ ] 利益相反を開示
- [ ] Data Availability Statementを記載
- [ ] 可能な範囲でデータ・コード公開

---

**関連ドキュメント**:
- [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md)
- [COMMON_PITFALLS.md](COMMON_PITFALLS.md)
- AEA Data and Code Availability Policy: https://www.aeaweb.org/journals/data
