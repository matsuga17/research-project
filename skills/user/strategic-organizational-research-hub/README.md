# Strategic & Organizational Research Hub

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/yourusername/strategic-organizational-research-hub)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

## 概要

事業戦略論・組織戦略論分野の定量分析（実証研究）に特化した包括的データ収集・分析システム。理論構築から論文執筆まで、研究の全ライフサイクルをサポートします。

## 主な機能

### 📚 理論フレームワーク開発
- 10以上の主要理論（RBV、Dynamic Capabilities、TCE、Agency Theory等）
- 仮説構築ガイド
- 変数の操作化

### 🔍 データソース発見
- **70以上のデータベース**を網羅
  - 財務データ：Compustat、CRSP、Orbis、NEEDS等
  - イノベーション：USPTO、PATSTAT、特許データ
  - ESG：CDP、MSCI、Refinitiv ESG
  - ガバナンス：ExecuComp、ISS、13F
- **無料データソースの完全ガイド**（予算ゼロの研究も可能）

### 📊 統計分析ガイド
- OLS回帰、パネルデータ分析（固定効果、変量効果）
- 差分の差分法（DiD）、操作変数法（IV/2SLS）
- イベントスタディ、生存分析
- 調整・媒介分析

### ✍️ 学術論文執筆支援
- トップジャーナル（SMJ、AMJ、OS）への投稿準備
- IMRaD形式の構造化ガイド
- 結果表の作成方法
- よくある却下理由と対策

### 🌏 アジア太平洋地域の特化サポート
- 日本：EDINET、NEEDS、SPEEDA
- 中国：CSMAR
- 韓国：FnGuide、Kis-Value
- 台湾：TEJ
- インド：CMIE Prowess

## 対応研究領域

### 事業戦略
- 競争戦略、企業戦略、国際戦略
- イノベーション戦略、ビジネスモデル
- 戦略的アライアンス、ESG・サステナビリティ

### 組織戦略
- 組織デザイン、組織学習、組織変革
- 組織文化、リーダーシップ・ガバナンス
- 人的資本、組織パフォーマンス

## クイックスタート

### 1. スキルの読み込み

Claudeでこのスキルを使用するには：

```
"strategic-organizational-research-hubスキルを使って、
日本の製造業における取締役会の多様性と企業イノベーションの
関係を研究したい"
```

### 2. 研究プロセス

スキルは以下の8つのフェーズでガイドします：

1. **理論フレームワーク開発**：研究質問の定式化、仮説構築
2. **研究デザイン**：サンプル選択、変数定義
3. **データソース発見**：最適なデータベースの特定
4. **データ収集戦略**：API、ダウンロード、スクレイピング
5. **データクリーニング**：欠損値処理、外れ値対応
6. **統計分析**：回帰分析、パネルデータ、イベントスタディ
7. **論文執筆**：ターゲットジャーナル選定、IMRaD構造
8. **再現性**：レプリケーション資料の準備

### 3. 使用例

#### 例1：新規研究の開始
```
"日本の上場企業におけるR&D投資と企業パフォーマンスの
関係を研究したい。無料のデータソースを使いたい。"
```

**Claudeの応答**：
- 理論：Resource-Based View、Dynamic Capabilities
- 仮説：H1: R&D強度は企業パフォーマンスと正の関係
- データソース：
  - 財務データ：EDINET（無料）
  - 特許データ：USPTO PatentsView（無料）
  - マクロデータ：World Bank、OECD（無料）
- 分析計画：パネルデータ回帰（固定効果モデル）

#### 例2：イベントスタディ
```
"米国のテクノロジー企業におけるCEO交代の
株価への影響を測定したい。"
```

**Claudeの応答**：
- データ：CRSP（株価）、ExecuComp（CEO情報）
- イベントウィンドウ：[-1, +1]日
- 推定ウィンドウ：[-250, -11]日
- 方法：異常リターンの計算、累積異常リターン（CAR）

#### 例3：既存研究の複製
```
"Barney (1991)のRBV研究を現代データで複製し、
新興市場に拡張したい。"
```

**Claudeの応答**：
- サンプル：Orbis（ブラジル、中国、インド）
- VRIN資源の測定方法
- 拡張：制度的要因の追加（World Bank Governance Indicators）
- 貢献：「RBVを新興市場に拡張し、制度的品質が
  資源-パフォーマンスリンクを調整することを示す」

## ディレクトリ構造

```
strategic-organizational-research-hub/
├── SKILL.md                          # メインスキルファイル
├── README.md                         # このファイル
├── QUICKSTART.md                     # クイックスタートガイド
├── FREE_DATA_SOURCES.md             # 無料データソース完全ガイド
├── scripts/
│   ├── data_collection_template.py   # データ収集テンプレート
│   ├── panel_data_analysis.py        # パネルデータ分析
│   ├── event_study_template.py       # イベントスタディ
│   └── data_cleaning_utils.py        # データクリーニングユーティリティ
├── templates/
│   ├── research_proposal.docx        # 研究提案書テンプレート
│   ├── data_dictionary.xlsx          # データ辞書テンプレート
│   └── regression_table.tex          # 回帰表LaTeXテンプレート
└── examples/
    ├── example_japan_rnd_performance.md
    ├── example_board_diversity_innovation.md
    └── example_ma_event_study.md
```

## 統合スキル

### ワークスペース内の関連スキル
- **research-data-collection**：汎用研究ワークフロー管理
- **corporate-research-data-hub**：企業ファイナンス・ガバナンスデータ
- **academic-paper-creation**：日本語学術論文作成（30,000字）

### 公開スキルとの統合
- **docx, pptx, xlsx**：文書・プレゼン・データ作成
- **pdf**：PDFからのデータ抽出
- **csv-data-summarizer-claude-skill**：CSV自動分析

## データソースのカテゴリ

### 無料データソース（予算ゼロ研究）
- **企業レベル**：SEC EDGAR、EDINET、OpenCorporates
- **特許**：USPTO PatentsView、Google Patents、WIPO
- **ESG**：CDP（研究者ライセンス）、GRI Database
- **マクロ・産業**：World Bank、OECD、FRED、IMF

### 有料データソース
- **北米**：Compustat、CRSP、ExecuComp、SDC Platinum
- **欧州**：Orbis、Amadeus、Datastream
- **アジア**：NEEDS、CSMAR、TEJ、CMIE Prowess
- **グローバル**：Worldscope、FactSet、CapitalIQ

## 対象ユーザー

- 経営学・経済学の博士課程学生
- 戦略・組織論の研究者
- 実証研究を行う実務家
- MBA学生（修士論文執筆）

## 前提条件

### 推奨スキル
- 統計学の基礎知識（回帰分析、仮説検定）
- データ分析ツール：Python、R、Stata のいずれか
- 基本的な英語読解力（多くのデータソースは英語）

### オプション
- プログラミング経験（API利用、Webスクレイピング）
- 大学のデータベースへのアクセス（WRDS等）

## よくある質問（FAQ）

### Q1: 予算がない場合でも研究できますか？
**A**: はい。無料データソースの完全ガイド（FREE_DATA_SOURCES.md）を提供しています。SEC EDGAR、EDINET、USPTO、World Bank等を使えば、予算ゼロで高品質な研究が可能です。

### Q2: どのジャーナルを目指すべきですか？
**A**: 研究の貢献度により：
- **トップティア**：SMJ、AMJ、OS（理論的・実証的貢献が高い）
- **フィールドジャーナル**：JIBS（国際戦略）、Research Policy（イノベーション）
- **地域ジャーナル**：Asia Pacific Journal of Management

### Q3: データ収集にどれくらい時間がかかりますか？
**A**: プロジェクトにより異なりますが：
- **パイロット**：1週間
- **フルデータ収集**：2-8週間
- **クリーニング**：2-4週間
- **合計**：研究時間の30-40%をデータ収集に割り当て

### Q4: 内生性の問題にどう対処しますか？
**A**: 複数の手法：
1. ラグ付き独立変数（X(t-1) → Y(t)）
2. 操作変数法（IV/2SLS）
3. 固定効果モデル
4. 差分の差分法（DiD）
5. 限界を認める（それも誠実な対応）

### Q5: 日本語論文にも対応していますか？
**A**: はい。academic-paper-creationスキル（日本語30,000字論文）と統合可能です。日本の学会誌（日本経営学会誌等）への投稿も support します。

## コントリビューション

このスキルの改善提案、バグ報告、新しいデータソースの追加は歓迎です。

## ライセンス

Apache License 2.0

## 免責事項

このスキルは研究計画・実行ツールです。研究者は以下の責任を負います：
1. すべてのデータプロバイダーの利用規約の遵守
2. 必要な機関承認の取得（IRB、倫理審査）
3. データソースと先行研究の適切な引用
4. データの倫理的使用と被験者保護の確保
5. データの正確性と研究への適切性の検証

## サポート

質問・提案は以下まで：
- GitHub Issues: [リンク]
- Email: [メールアドレス]

## 謝辞

このスキルは以下の既存スキルの知見を統合しています：
- research-data-collection
- corporate-research-data-hub
- academic-paper-creation

---

**研究を始めましょう！**

```
"strategic-organizational-research-hubスキルを使って、
[あなたの研究テーマ]を研究したい"
```