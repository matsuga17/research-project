# Japan Innovation Research Example

## 研究テーマ
日本企業のイノベーション投資（R&D）と企業パフォーマンスの関係

## Research Question
**"How does R&D intensity affect firm performance in Japanese manufacturing firms?"**

## 概要
このプロジェクトは、日本の製造業企業を対象に、R&D投資強度が企業パフォーマンスに与える影響を実証分析する完全な実行例です。

## データソース
- **EDINET**: 日本企業の財務データ（有価証券報告書）
- **特許庁**: 特許出願データ（イノベーション指標）
- **e-Stat**: 産業別統計データ（統制変数）

## 実行手順

### ステップ1: 研究設計
```bash
python 1_research_design.py
```

このスクリプトは以下を実行します：
- 研究課題の明確化
- 仮説の定式化
- 変数の定義
- サンプル基準の設定

**出力**: `output/phase1_research_design.json`

### ステップ2: データ収集
```bash
python 2_data_collection.py
```

このスクリプトは以下を実行します：
- EDINETから日本企業の財務データを収集
- 特許データの取得（プレースホルダー）
- 産業統計データの収集（プレースホルダー）

**注意**: 実際のEDINET API利用には申請が必要です。このexampleではデモデータを使用します。

**出力**: `output/japan_firms_raw.csv`

### ステップ3: 完全パイプライン実行
```bash
python 3_full_pipeline.py
```

このスクリプトは Phase 1-8 を一括実行します：
- Phase 1: 研究設計
- Phase 2: データソース特定
- Phase 3: サンプル構築
- Phase 4: データ収集
- Phase 5: データクリーニング
- Phase 6: 変数構築
- Phase 7: 統計分析
- Phase 8: レポート生成

**出力**: `output/` ディレクトリ内に全Phase の結果

## 期待される結果

### サンプル特性
- **企業数**: 約500社（日本の上場製造業企業）
- **期間**: 2010-2023年
- **観測値**: 約6,000件

### 仮説
- **H1**: R&D intensity は ROA に正の影響を与える
- **H2**: 企業規模が R&D-パフォーマンス関係を調整する
- **H3**: 産業競争度が R&D-パフォーマンス関係を調整する

### 主要変数
- **従属変数**: ROA (Return on Assets)
- **独立変数**: R&D intensity (R&D支出 / 売上高)
- **統制変数**: 企業規模、企業年齢、レバレッジ、産業、年次

## ディレクトリ構成

```
example_japan_innovation/
├── README.md                    # このファイル
├── 1_research_design.py         # Phase 1 実行スクリプト
├── 2_data_collection.py         # データ収集スクリプト
├── 3_full_pipeline.py           # 完全パイプライン実行
├── config.yaml                  # 設定ファイル
└── output/                      # 結果出力ディレクトリ
    ├── phase1_research_design.json
    ├── phase2_data_sources.json
    ├── phase3_sample.csv
    ├── ...
    └── phase8_final_report.md
```

## 所要時間
- **ステップ1**: 約1分
- **ステップ2**: 約5分（デモデータ使用時）
- **ステップ3**: 約2-3分

## 技術要件
- Python 3.8+
- pandas, numpy
- matplotlib, seaborn (可視化用)
- pytest (テスト実行用)

## インストール
```bash
pip install pandas numpy matplotlib seaborn pyyaml
```

## 実行例
```bash
# 完全パイプライン実行
cd /Users/changu/Desktop/研究/skills/user/strategic-research-suite/1-core-workflow/examples/example_japan_innovation
python 3_full_pipeline.py

# 個別Phase実行
python 1_research_design.py
python 2_data_collection.py
```

## トラブルシューティング

### エラー: ModuleNotFoundError
```bash
# パスが通っていない場合
export PYTHONPATH="${PYTHONPATH}:/Users/changu/Desktop/研究/skills/user/strategic-research-suite/1-core-workflow"
```

### データ収集エラー
実際のEDINET APIを使用する場合は、`2_data_collection.py`内のAPI keyを設定してください。

## 次のステップ
1. 結果の確認: `output/phase8_final_report.md`
2. ロバストネスチェック: `statistical-methods` skill を使用
3. 追加分析: `text-analysis` skill でMD&A分析
4. 論文執筆: 結果を学術論文にまとめる

## 関連Skills
- **core-workflow**: Phase 1-8の基本フレームワーク
- **data-sources-catalog**: EDINET等のデータソース詳細
- **statistical-methods-advanced**: 高度な統計分析手法
- **text-analysis-toolkit**: MD&A・決算説明会分析

## 参考文献
- 日本の実証研究における慣例: [参考文献を追加]
- EDINET利用ガイド: https://disclosure.edinet-fsa.go.jp/
- 特許庁データベース: https://www.jpo.go.jp/

---

**作成日**: 2025-11-01  
**バージョン**: 1.0  
**Part of**: Strategic Research Suite v4.0
