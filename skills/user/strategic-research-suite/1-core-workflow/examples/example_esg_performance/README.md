# ESG Performance Research Example

## 研究テーマ
企業のESGパフォーマンスと財務パフォーマンスの関係

## Research Question
**"Does ESG performance affect financial performance?"**

## 概要
このプロジェクトは、ESG（環境・社会・ガバナンス）パフォーマンスが企業の財務パフォーマンスに与える影響を実証分析する実行例です。

## データソース
- **MSCI ESG Ratings**: ESG総合スコア（デモデータ）
- **CDP**: 気候変動データ（デモデータ）
- **Compustat**: 財務データ（デモデータ）
- **EPA TRI**: 環境規制データ（デモデータ）

## 実行手順

### 簡易実行（推奨）
```bash
python run_esg_study.py
```

このスクリプトは完全なパイプライン（Phase 1-8）を実行します。

## 期待される結果

### サンプル特性
- **企業数**: 約300社（S&P 500企業のサブセット）
- **期間**: 2015-2023年
- **観測値**: 約2,700件

### 仮説
- **H1**: ESG総合スコアは財務パフォーマンス（ROA）に正の影響を与える
- **H2**: 環境スコア（E）が最も強い影響を持つ
- **H3**: 業種によってESG-パフォーマンス関係が異なる

### 主要変数
- **従属変数**: ROA, Tobin's Q
- **独立変数**: ESG総合スコア, E/S/Gスコア
- **統制変数**: 企業規模、レバレッジ、業種、年次

## ディレクトリ構成

```
example_esg_performance/
├── README.md                    # このファイル
├── run_esg_study.py             # メイン実行スクリプト
└── output/                      # 結果出力ディレクトリ
```

## 所要時間
- 約2-3分（デモデータ使用時）

## 技術要件
- Python 3.8+
- pandas, numpy
- pyyaml

## インストール
```bash
pip install pandas numpy pyyaml
```

## 実行例
```bash
cd /Users/changu/Desktop/研究/skills/user/strategic-research-suite/1-core-workflow/examples/example_esg_performance
python run_esg_study.py
```

## 次のステップ
1. 結果の確認: `output/phase8_final_report.md`
2. ESG詳細分析: `esg-sustainability-data` skill を使用
3. 因果推論: `causal-ml-toolkit` skill でCATEを推定
4. 論文執筆: 結果を学術論文にまとめる

## 関連Skills
- **core-workflow**: Phase 1-8の基本フレームワーク
- **esg-sustainability-data**: ESGデータソース詳細
- **causal-ml-toolkit**: 因果推論（処置効果の異質性）
- **statistical-methods-advanced**: パネル回帰分析

---

**作成日**: 2025-11-01  
**バージョン**: 1.0  
**Part of**: Strategic Research Suite v4.0
