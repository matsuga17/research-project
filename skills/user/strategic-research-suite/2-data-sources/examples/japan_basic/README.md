# Japan Basic Data Collection Example

## 概要

このディレクトリには、**EDINET (Electronic Disclosure for Investors' NETwork)** から日本企業の開示書類を収集する基本的な実行例が含まれています。

### EDINETとは

金融庁が運営する企業の有価証券報告書等の開示システム。上場企業・大企業の財務情報や経営情報が公開されています。

- 公式サイト: https://disclosure.edinet-fsa.go.jp/
- API仕様: https://disclosure.edinet-fsa.go.jp/EKW0EZ0001.html

## 実行内容

1. **ドキュメントリスト取得**: 指定日に提出された開示書類を取得
2. **有価証券報告書フィルタ**: 財務データを含む報告書のみ抽出
3. **企業情報抽出**: ユニークな企業リストを作成
4. **結果保存**: CSV形式で自動保存

## 前提条件

```bash
# 必要なパッケージ
pip install pandas numpy requests
```

## 実行方法

### 基本実行

```bash
cd 2-data-sources/examples/japan_basic/
python collect_japan_data.py
```

### 実行時間

- 単一日: 約5秒
- 1ヶ月（30日）: 約2分（レート制限: 2秒/リクエスト）

## 出力ファイル

実行後、`output/`ディレクトリに以下のファイルが生成されます：

```
output/
├── edinet_documents_20240110.csv       # 全開示書類リスト
├── securities_reports_20240110.csv     # 有価証券報告書のみ
└── firm_list_20240110.csv              # ユニークな企業リスト
```

### ファイル内容

#### edinet_documents_20240110.csv
全開示書類の情報（例：100-200件/日）

| Column | Description |
|--------|-------------|
| edinetCode | EDINET企業コード (E00001等) |
| secCode | 証券コード (4桁) |
| filerName | 提出者名（企業名） |
| docDescription | 書類種別 |
| submitDateTime | 提出日時 |
| docTypeCode | 書類タイプコード |

#### securities_reports_20240110.csv
有価証券報告書のみ（例：10-30件/日）

#### firm_list_20240110.csv
ユニークな企業情報

## 出力例

### コンソール出力

```
================================================================================
JAPAN FIRMS DATA COLLECTION EXAMPLE (EDINET)
================================================================================

[Initialization]
--------------------------------------------------------------------------------
INFO:edinet_collector:EDINETCollector initialized
INFO:edinet_collector:API base URL: https://disclosure.edinet-fsa.go.jp/api/v1
INFO:edinet_collector:Rate limit delay: 2.0s
✓ EDINETCollector initialized (rate limit: 2.0s)

[Step 1] Fetching Document List
--------------------------------------------------------------------------------
Target date: 2024-01-10

INFO:edinet_collector:Fetching document list for 2024-01-10
INFO:edinet_collector:Retrieved 156 documents
✓ Retrieved 156 documents

Sample documents (first 5):
                           filerName                            docDescription
0                   トヨタ自動車株式会社                    四半期報告書－第120期第3四半期
1           ソニーグループ株式会社            有価証券報告書－第78期(2023年4月1日-2024年3月31日)
2                   パナソニック株式会社                      臨時報告書
3               三菱UFJフィナンシャル・グループ              有価証券報告書－第20期
4                       株式会社日立製作所                  内部統制報告書

[Step 2] Filtering for Securities Reports
--------------------------------------------------------------------------------
INFO:edinet_collector:Filtered for securities reports: 156 → 23
✓ Securities reports: 23

[Step 3] Extracting Firm Information
--------------------------------------------------------------------------------
INFO:edinet_collector:Extracted 23 unique firms
✓ Unique firms: 23

Sample firms:
  edinetCode            filerName secCode          JCN
0    E01234    トヨタ自動車株式会社    7203  3180001008844
1    E05678  ソニーグループ株式会社    6758  3010401039466
2    E00012      パナソニック株式会社    6752  1120001077362
3    E03462        三菱UFJフィナンシャル・グループ    8306  2010001040000
4    E01288        株式会社日立製作所    6501  7010001008844

[Step 4] Saving Results
--------------------------------------------------------------------------------
INFO:edinet_collector:Data saved to: output/edinet_documents_20240110.csv
INFO:edinet_collector:  Rows: 156
INFO:edinet_collector:  Columns: 15
✓ Document list saved
INFO:edinet_collector:Data saved to: output/securities_reports_20240110.csv
INFO:edinet_collector:  Rows: 23
INFO:edinet_collector:  Columns: 15
✓ Securities reports saved
INFO:edinet_collector:Data saved to: output/firm_list_20240110.csv
INFO:edinet_collector:  Rows: 23
INFO:edinet_collector:  Columns: 4
✓ Firm list saved

================================================================================
COLLECTION COMPLETED SUCCESSFULLY!
================================================================================

Results saved to: output

Output files:
  - edinet_documents_20240110.csv (156 rows)
  - securities_reports_20240110.csv (23 rows)
  - firm_list_20240110.csv (23 rows)

Next steps:
  1. Review collected data in output/ directory
  2. Extend date range with collect_sample()
  3. Extract EDINET codes for panel dataset construction
  4. Implement XBRL parsing for financial variable extraction
```

## カスタマイズ

### 日付範囲の拡張

```python
# collect_japan_data.py を編集

# 単一日 → 期間収集に変更
df_docs = collector.collect_sample(
    start_date='2024-01-01',
    end_date='2024-01-31',
    doc_type='120'  # 有価証券報告書のみ
)
```

### 業種フィルタの追加

```python
# 製造業のみに絞り込み
df_filtered = collector.filter_by_industry(
    df_reports, 
    industry_codes=['010']  # 製造業コード
)
```

### レート制限の調整

```python
# より保守的な設定（3秒間隔）
collector = EDINETCollector(rate_limit_delay=3.0)
```

## トラブルシューティング

### Error: requests.exceptions.ConnectionError

**原因**: ネットワーク接続の問題

**解決策**:
1. インターネット接続を確認
2. EDINET APIの稼働状況を確認（メンテナンス時間帯を避ける）
3. ファイアウォール/プロキシ設定を確認

### Error: requests.exceptions.Timeout

**原因**: APIリクエストがタイムアウト

**解決策**:
```python
# タイムアウト時間を延長
# edinet_collector.py の get_document_list() 関数で
response = requests.get(url, params=params, timeout=60)  # 30 → 60秒
```

### 日付によってドキュメントが見つからない

**原因**: 土日祝日は開示がない

**解決策**: 平日のみデータ収集するか、期間を広げる

### ModuleNotFoundError: No module named 'edinet_collector'

**原因**: Pythonがscriptsディレクトリを見つけられない

**解決策**:
```bash
# collect_japan_data.py と同じディレクトリから実行
cd 2-data-sources/examples/japan_basic/
python collect_japan_data.py
```

## 制限事項

### XBRL解析未実装

現在のバージョンでは、XBRL（財務データのXML形式）の解析は未実装です。
`get_securities_reports()` はプレースホルダーを返します。

**今後の実装予定**:
- XBRLドキュメントのダウンロード
- 財務諸表データの抽出（売上高、利益、資産等）
- パネルデータ自動構築

### API制限

EDINET APIには利用制限があります（詳細は公式ドキュメント参照）：
- 過度なリクエストを避ける
- デフォルトで2秒間隔のレート制限を設定

## 次のステップ

このBasic Exampleを理解したら：

1. **期間拡張**: 1ヶ月〜1年分のデータ収集
2. **企業選択**: 特定業種・規模の企業に絞り込み
3. **XBRL実装**: 財務データの自動抽出（別途実装）
4. **パネル構築**: Phase 4でパネルデータセット構築

## 関連ドキュメント

- [Data Sources SKILL.md](../../SKILL.md) - データソース詳細
- [EDINET Enhanced Guide](../../EDINET_ENHANCED.md) - EDINET詳細ガイド
- [Core Workflow](../../../1-core-workflow/SKILL.md) - Phase 2-4

## API情報

- **EDINET API仕様**: https://disclosure.edinet-fsa.go.jp/EKW0EZ0001.html
- **メタデータAPI**: `/api/v1/documents.json`
- **ドキュメント取得API**: `/api/v1/documents/{docID}`

---

**作成日**: 2025-11-01  
**最終更新**: 2025-11-01  
**メンテナー**: Strategic Research Suite Team
