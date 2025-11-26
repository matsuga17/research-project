# Strategic Management Research Hub v3.1

**事業戦略論・組織戦略論分野における定量的実証研究のための統合システム**

[![Version](https://img.shields.io/badge/version-3.1-blue.svg)](https://github.com/yourusername/strategic-management-research-hub)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 概要

このスキルは、戦略経営研究者のためのエンドツーエンドの実証研究支援システムです。データ発見から論文執筆まで、研究プロセス全体を体系的に管理し、トップジャーナル（SMJ, AMJ, OS, ASQ）掲載基準を満たす研究の実現を支援します。

### 主要特徴

- ✅ **8フェーズ統合ワークフロー**: 構想→データ探索→収集→品質保証→分析→理論構築→執筆→投稿準備
- ✅ **戦略論特化データソース**: 競争戦略、組織能力、制度環境、産業構造分析（70+ソース）
- ✅ **Publication-Ready QA**: 統計的検出力分析、Benford's Law、構造変化検定
- ✅ **完全再現性**: AEA準拠のデータ系譜追跡、Docker環境、pytest検証
- ✅ **理論構築支援**: RBV、Dynamic Capabilities、Institutional Theory統合
- ✅ **国際データカバレッジ**: 北米・欧州・アジア11カ国+グローバル無料ソース
- ✅ **高度な分析手法**: テキスト分析、ネットワーク分析、機械学習×因果推論

## 📚 使用可能な研究テーマ

### 【優先度：最高】
- **競争戦略研究**: 持続的競争優位、差別化戦略、プラットフォーム戦略
- **組織能力・資源ベース研究**: Dynamic Capabilities、組織学習、イノベーション能力
- **組織デザイン・構造研究**: 組織構造と業績、集権化vs.分権化

### 【優先度：高】
- **制度理論・環境適応研究**: 制度的同型化、正当性獲得戦略
- **多角化・国際化戦略**: 関連多角化vs.非関連多角化、新興市場参入
- **M&A・戦略的提携**: M&Aパフォーマンス、アライアンスポートフォリオ

## 🚀 クイックスタート

### 初心者向け（5分で開始）

```
「strategic-management-research-hub skillを使用して、
 日本の製造業企業におけるR&D投資とパフォーマンスの関係を研究したい」
```

Claude が以下を自動実行：
1. Phase 1: 理論的フレームワーク提案、変数リスト提示
2. Phase 2: 無料データソース（EDINET）を推奨
3. Phase 3-5: データ収集・統合スクリプト生成
4. Phase 6: 自動品質チェック実行
5. Phase 7: パネル回帰分析
6. Phase 8: 再現パッケージ作成

### 中級者向け（効率的ワークフロー）

```python
# 完全自動化パイプライン
from complete_pipeline import StrategicResearchPipeline

pipeline = StrategicResearchPipeline(
    research_question="Does R&D intensity improve firm performance?",
    sample_criteria={
        'industry': 'manufacturing',
        'years': (2010, 2023),
        'include_text': True  # MD&A分析を含む
    },
    output_dir='./output/'
)

# Phase 1-8を一括実行（2-4時間）
results = pipeline.run_full_pipeline()
```

### 上級者向け（論文投稿準備）

```
「SMJ投稿準備：Phase 6のPublication-Ready QAを実行し、
 Phase 7で5種類のrobustness checksを追加、
 Phase 8でAEA準拠のreplication packageを作成」
```

## 📊 データソースカバレッジ

### 無料データソース（¥0予算研究が可能）

#### アジア11カ国
| 国 | データソース | 内容 | アクセス |
|---|------------|------|---------|
| 🇯🇵 日本 | EDINET | 財務諸表、有価証券報告書 | API無料 |
| 🇰🇷 韓国 | DART | 財務諸表、governance | API無料 |
| 🇨🇳 中国 | CNINFO, AKShare | 財務・株価 | 無料 |
| 🇹🇼 台湾 | TWSE, MOPS | 株価・財務 | 無料 |
| 🇸🇬 シンガポール | SGX | 上場企業情報 | 一部無料 |
| 🇲🇾 マレーシア | Bursa Malaysia | 財務データ | 無料 |
| 🇹🇭 タイ | SET | 株価・財務 | 無料 |
| 🇻🇳 ベトナム | HOSE/HNX | 株価 | 無料 |
| 🇮🇩 インドネシア | IDX | 上場企業情報 | 無料 |
| 🇵🇭 フィリピン | PSE | 企業情報 | 無料 |
| 🇮🇳 インド | BSE/NSE | 株価データ | 一部無料 |

#### グローバル
- **USPTO PatentsView**: 全米国特許（無料、API）
- **World Bank**: 200カ国マクロ指標（無料、API）
- **SEC EDGAR**: 米国上場企業開示（無料、API）
- **CDP**: 13,000企業ESGデータ（研究者無料）

### 有料データソース（大学契約）

- **Compustat** (WRDS): 北米企業財務データ
- **CRSP** (WRDS): 株価・リターンデータ
- **Orbis** (BvD): 欧州企業データ
- **SDC Platinum**: M&A・提携データ
- **ISS**: コーポレートガバナンスデータ

## 🛠️ 主要機能

### 1. 高度な品質保証（Phase 6）

```python
from data_quality_checker import AdvancedQualityAssurance

qa = AdvancedQualityAssurance(df_panel, firm_id='gvkey', time_var='year')
qa_report = qa.run_comprehensive_qa()

# 自動チェック項目：
# - Multivariate outlier detection (3手法統合)
# - Benford's Law test (不正検出)
# - Structural break detection (Chow test)
# - Accounting identity verification
# - Panel balance & attrition analysis
# - Statistical power analysis (post-hoc)
```

### 2. テキストデータ分析（Appendix F）

```python
from text_analyzer import MDAAnalyzer, EarningsCallAnalyzer

# 10-K MD&A分析
mda_analyzer = MDAAnalyzer()
sentiment = mda_analyzer.analyze_sentiment(mda_text)
topics = mda_analyzer.extract_topics(mda_text)
forward_looking = mda_analyzer.measure_forward_looking(mda_text)

# 決算説明会分析
call_analyzer = EarningsCallAnalyzer()
strategy_mentions = call_analyzer.analyze_strategy_discussion(transcript)
qa_tone = call_analyzer.analyze_qa_tone(transcript)
```

### 3. ネットワーク分析（Appendix G）

```python
from network_analyzer import BoardNetworkAnalyzer

# 取締役ネットワーク構築
board_network = BoardNetworkAnalyzer()
G = board_network.build_network(director_data)
metrics = board_network.calculate_centrality(G, firm_id='AAPL')

# 戦略的示唆：
# - Degree centrality → 情報アクセス
# - Betweenness → ブリッジ役割
# - Clustering → 三者関係密度
```

### 4. 機械学習×因果推論（Appendix H）

```python
from causal_ml import CausalForestEstimator, DMLEstimator

# 異質的処置効果推定（Causal Forest）
cf = CausalForestEstimator()
heterogeneous_effects = cf.estimate(
    treatment='ma_dummy',
    outcome='roa_change',
    heterogeneity_vars=['firm_size', 'rd_intensity']
)

# Double Machine Learning
dml = DMLEstimator()
ate = dml.estimate(
    treatment='rd_intensity',
    outcome='roa_lead2',
    controls=high_dimensional_controls
)
```

### 5. ESG/サステナビリティ研究（Appendix I）

```python
from esg_analyzer import ESGDataCollector

# CDP データ取得（無料）
cdp = ESGDataCollector(source='cdp')
carbon_data = cdp.collect_carbon_emissions(firms=['AAPL', 'MSFT'])

# EPA Toxic Release Inventory
epa = ESGDataCollector(source='epa')
emissions = epa.collect_toxic_emissions(state='CA', year=2023)
```

## 📖 ドキュメント構成

```
strategic-management-research-hub/
├── SKILL.md                    # メインスキルファイル（5782行）
├── README.md                   # このファイル
├── QUICKSTART.md              # 5分で始めるガイド
├── sample_scripts/
│   ├── complete_pipeline.py   # 全自動パイプライン
│   ├── japanese_firms_roa.py  # 日本企業研究サンプル
│   └── asian_comparison.py    # アジア横断比較サンプル
├── templates/
│   ├── research_plan.md       # 研究計画テンプレート
│   ├── data_dictionary.xlsx   # データ辞書テンプレート
│   └── replication_readme.md  # 再現ガイドテンプレート
└── tests/
    ├── test_data_integrity.py
    └── test_qa_system.py
```

## 🎓 学習リソース

### チュートリアル

1. **初心者向け**：[はじめての戦略研究](tutorials/beginner_guide.md)
   - データソース選択
   - 基本的な変数構築
   - 記述統計とパネル回帰

2. **中級者向け**：[効率的ワークフロー](tutorials/intermediate_workflow.md)
   - 複数データソース統合
   - 内生性への対処
   - Robustness checks

3. **上級者向け**：[トップジャーナル投稿準備](tutorials/advanced_publication.md)
   - Publication-grade QA
   - 理論的貢献の明確化
   - 完全再現パッケージ

### サンプルプロジェクト

#### プロジェクト1：日本製造業のイノベーション戦略（¥0予算）
```yaml
研究テーマ：R&D投資とパフォーマンス：環境動態性の調整効果
データソース：EDINET + JPX + PatentsView（全て無料）
期間：8週間
成果：SMJ投稿可能なデータセット
```
👉 [完全実装を見る](sample_scripts/japanese_firms_roa.py)

#### プロジェクト2：韓国財閥の多角化戦略（¥0予算）
```yaml
研究テーマ：財閥所属と多角化：制度的視点
データソース：DART + KRX + World Bank（全て無料）
期間：10週間
理論的貢献：制度理論の新興市場への拡張
```
👉 [完全実装を見る](sample_scripts/korean_chaebol.py)

#### プロジェクト3：中国国有企業改革の効果（¥0予算）
```yaml
研究テーマ：所有形態とイノベーション：制度変化の影響
データソース：CNINFO + AKShare + PatentsView（全て無料）
分析手法：Difference-in-Differences
期間：12週間
```
👉 [完全実装を見る](sample_scripts/china_soe_reform.py)

## 🔧 インストール

### 必要環境

- Python 3.9以上
- 16GB RAM以上推奨
- 50GB以上の空きストレージ

### インストール手順

```bash
# リポジトリクローン
git clone https://github.com/yourusername/strategic-management-research-hub.git
cd strategic-management-research-hub

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージインストール
pip install -r requirements.txt

# テスト実行
pytest tests/
```

### Docker環境（推奨）

```bash
# Docker image ビルド
docker build -t strategic-research:v3.1 .

# コンテナ起動
docker run -it -v $(pwd):/workspace strategic-research:v3.1

# Jupyter Notebook起動
jupyter notebook --ip=0.0.0.0 --allow-root
```

## 💡 使用例

### 例1：基本的な研究（Claudeに依頼）

```
「strategic-management-research-hub skillを使用して、
 日本企業のダイナミック・ケイパビリティとパフォーマンスの関係を
 研究したい。無料データソースのみ使用。」
```

### 例2：高度な分析（Pythonスクリプト）

```python
from complete_pipeline import StrategicResearchPipeline

pipeline = StrategicResearchPipeline(
    research_question="Dynamic Capabilities → Performance (Japan)",
    sample_criteria={
        'country': 'Japan',
        'industry': 'manufacturing',
        'years': (2010, 2023),
        'data_sources': ['edinet', 'jpx', 'patents'],
        'include_text': True,
        'include_network': True
    },
    output_dir='./japan_dc_research/'
)

results = pipeline.run_full_pipeline()
```

### 例3：特定フェーズのみ実行

```python
# Phase 6の品質保証のみ
from data_quality_checker import AdvancedQualityAssurance

qa = AdvancedQualityAssurance(df_panel, firm_id='gvkey', time_var='year')
qa_report = qa.run_comprehensive_qa()
qa.generate_report(output_formats=['html', 'pdf'], output_dir='./qa/')
```

## 📊 成果物

このスキルを使用して生成される成果物：

### データ成果物
- ✅ クリーニング済みパネルデータセット（.dta, .csv, .parquet）
- ✅ 変数定義データ辞書（.xlsx）
- ✅ データ系譜トラッキングファイル（.json）

### 分析成果物
- ✅ 記述統計テーブル（LaTeX/Excel）
- ✅ 相関行列（LaTeX/Excel）
- ✅ 回帰分析結果（LaTeX/Excel）
- ✅ Robustness checks（LaTeX/Excel）
- ✅ 図表（高解像度PNG/PDF）

### 品質保証成果物
- ✅ QAレポート（HTML/PDF）
- ✅ Benford's Law検定結果
- ✅ 構造変化検定結果
- ✅ 検出力分析レポート

### 再現性成果物
- ✅ 完全な再現スクリプト（Python）
- ✅ Docker環境定義（Dockerfile, docker-compose.yml）
- ✅ 依存パッケージリスト（requirements.txt）
- ✅ Pytest test suite
- ✅ REPLICATIONガイド（Markdown）

## 📈 トップジャーナル基準

このスキルは以下のトップジャーナル基準に完全対応：

### Strategic Management Journal (SMJ)
- [x] サバイバルバイアス対策
- [x] 統計的検出力分析
- [x] 5種類以上のrobustness checks
- [x] 内生性への対処
- [x] 完全なreplication package

### Academy of Management Journal (AMJ)
- [x] 理論的貢献の明確化
- [x] 組織レベル現象の分析
- [x] マイクロファンデーション
- [x] プロセスメカニズムの説明

### Organization Science (OS)
- [x] 縦断データ分析
- [x] 組織学習・ルーティン研究
- [x] 計算論的手法対応

### Administrative Science Quarterly (ASQ)
- [x] 新規理論的貢献
- [x] 豊富な文脈理解
- [x] プロセス分析

## 🤝 貢献

このスキルへの貢献を歓迎します！

### 貢献方法

1. このリポジトリをFork
2. 新しいブランチ作成 (`git checkout -b feature/amazing-feature`)
3. 変更をCommit (`git commit -m 'Add amazing feature'`)
4. ブランチにPush (`git push origin feature/amazing-feature`)
5. Pull Request作成

### 貢献の種類

- 🐛 バグ修正
- ✨ 新機能追加
- 📝 ドキュメント改善
- 🌐 新しいデータソース追加
- 🔬 新しい分析手法追加
- 🎓 チュートリアル作成

## 📞 サポート

### 質問・相談

- **GitHub Issues**: [問題報告・機能要望](https://github.com/yourusername/strategic-management-research-hub/issues)
- **Discussions**: [Q&A・アイデア交換](https://github.com/yourusername/strategic-management-research-hub/discussions)
- **Email**: research-support@example.com

### よくある質問

👉 [FAQ.md](FAQ.md)を参照してください

## 📜 ライセンス

MIT License - 学術・商用利用可

詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🙏 謝辞

このスキルは以下の既存スキルとリソースを参考にしています：

- [research-data-collection](https://github.com/anthropics/skills/research-data-collection)
- [corporate-research-data-hub](https://github.com/anthropics/skills/corporate-research-data-hub)
- [academic-paper-creation](https://github.com/anthropics/skills/academic-paper-creation)
- [K-Dense-AI scientific-skills](https://github.com/K-Dense-AI/skills)

## 📚 引用

このスキルを研究で使用した場合、以下のように謝辞に記載してください：

```
データ収集と品質保証は、strategic-management-research-hub skill v3.1
(https://github.com/yourusername/strategic-management-research-hub)に
基づく体系的手順に従って実施された。このアプローチにより、研究の
再現性とデータの信頼性が確保された。
```

## 🗓️ バージョン履歴

- **v3.1** (2025-10-31): テキスト分析、ネットワーク分析、ML×因果推論、ESG拡充、アジア拡張、完全自動化
- **v3.0** (2025-10-31): 戦略論特化、統計的検出力分析、Publication-grade QA、理論構築フレームワーク
- **v2.0** (2025-10-30): Advanced QA、Data lineage tracking、Research checklist manager
- **v1.0** (2025-10-29): 基本6フェーズワークフロー

## 🚀 次のステップ

1. **インストール**: 上記のインストール手順に従ってください
2. **クイックスタート**: [QUICKSTART.md](QUICKSTART.md)で5分で開始
3. **チュートリアル**: [tutorials/](tutorials/)でステップバイステップ学習
4. **サンプルプロジェクト**: [sample_scripts/](sample_scripts/)で実践例を参照

---

**🎓 本格的な戦略経営研究を、今すぐ始めましょう！**

```
「strategic-management-research-hub skillを使用して、
 [あなたの研究テーマ]の実証研究を開始したい」
```

と言うだけで、Claudeが完全サポートします。

**Good luck with your research! 📊🚀🎓**
