# Strategic Management Research Hub v3.1 - 完全統合ガイド
================================================================

**最終更新**: 2025-11-01  
**バージョン**: 3.1  
**ステータス**: Production Ready ✅

---

## 🎉 新機能（v3.1）

### 🔥 本格的データマイニング・機械学習統合

このv3.1アップデートで、以下の最先端機能が追加されました：

1. **Advanced Data Mining Engine**
   - 戦略的グループ分析（クラスタリング）
   - 企業パフォーマンス予測（アンサンブル学習）
   - 特徴量重要度分析（SHAP, Permutation）
   - 異常検知（アウトライア企業特定）
   - 時系列パターン分析

2. **Causal Inference Integration**
   - Causal Forest（異質的処置効果）
   - Double Machine Learning（DML）
   - Synthetic Control Method
   - Propensity Score Matching
   - 内生性問題への完全対応

3. **Explainable AI (XAI)**
   - SHAP値による解釈
   - 特徴量重要度の可視化
   - 予測の透明性確保

---

## 📁 プロジェクト構成（v3.1）

```
strategic-management-research-hub/
├── 📊 データマイニング新機能
│   ├── scripts/
│   │   ├── advanced_strategic_datamining.py      # 🔥 メインエンジン
│   │   ├── ml_causal_inference_integrated.py     # 🔥 因果推論
│   │   ├── datamining_config.yaml                # 設定
│   │   ├── quick_datamining_demo.py              # デモ
│   │   └── test_datamining_integration.py        # テスト
│   ├── DATAMINING_GUIDE.md                        # 📚 詳細ガイド
│   ├── DATAMINING_README.md                       # 📚 クイックガイド
│   └── requirements_datamining.txt                # 依存関係
│
├── 📁 既存機能（Phase 1-8）
│   ├── scripts/
│   │   ├── data_collectors.py                     # データ収集
│   │   ├── data_quality_checker.py                # 品質保証
│   │   ├── panel_data_analysis.py                 # パネル分析
│   │   ├── network_analyzer.py                    # ネットワーク
│   │   ├── text_analyzer.py                       # テキスト分析
│   │   └── complete_pipeline.py                   # 統合パイプライン
│   └── [その他スクリプト]
│
└── 📖 ドキュメント
    ├── SKILL.md                                   # スキル本体
    ├── README.md                                  # プロジェクト概要
    ├── INSTALLATION_GUIDE.md                      # インストール
    ├── QUICKSTART_TUTORIAL.md                     # クイックスタート
    └── FAQ.md                                     # よくある質問
```

---

## 🚀 クイックスタート（3つのステップ）

### ステップ1: インストール

```bash
# 仮想環境作成（推奨）
python -m venv strategic_env
source strategic_env/bin/activate  # Windows: strategic_env\Scripts\activate

# 依存関係インストール
pip install -r requirements_datamining.txt

# 検証
python -c "import pandas, sklearn, econml, xgboost, shap; print('✅ Installation successful')"
```

### ステップ2: デモ実行

```bash
cd scripts

# サンプルデータでデモ（5分）
python quick_datamining_demo.py

# 因果推論も含む完全デモ（10分）
python quick_datamining_demo.py --causal
```

### ステップ3: 自分のデータで分析

```python
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining
import pandas as pd

# データ読み込み
df = pd.read_stata('./data/final/your_data.dta')

# 分析実行
dm = AdvancedStrategicDataMining(
    data=df,
    firm_id='gvkey',
    time_var='year',
    output_dir='./my_analysis/'
)

# 戦略的グループ分析
groups = dm.strategic_group_analysis(
    features=['rd_intensity', 'capital_intensity', 'advertising_intensity'],
    n_clusters=4
)

# パフォーマンス予測
predictions = dm.predict_firm_performance(
    target='roa_lead1',
    features=['rd_intensity', 'firm_size', 'leverage'],
    model_type='ensemble'
)

# レポート生成
report = dm.generate_comprehensive_report()
print(f"📊 レポート: {report}")
```

---

## 📊 主要機能一覧

### 既存機能（Phase 1-8）

| フェーズ | 機能 | ドキュメント |
|---------|------|--------------|
| Phase 1 | 研究設計・理論フレームワーク | SKILL.md |
| Phase 2-3 | データ収集・サンプル構築 | SKILL.md |
| Phase 4-5 | データ統合・変数構築 | SKILL.md |
| Phase 6 | 品質保証（Benford's Law等） | SKILL.md |
| Phase 7 | 統計分析・パネル回帰 | SKILL.md |
| Phase 8 | 文書化・再現パッケージ | SKILL.md |

### 新機能（v3.1）

| カテゴリ | 機能 | ドキュメント |
|---------|------|--------------|
| **データマイニング** | 戦略的グループ分析 | DATAMINING_GUIDE.md §2 |
| | 企業パフォーマンス予測 | DATAMINING_GUIDE.md §3 |
| | 特徴量重要度分析 | DATAMINING_GUIDE.md §4 |
| | 異常検知 | DATAMINING_GUIDE.md §5 |
| | 時系列パターン分析 | DATAMINING_GUIDE.md §7 |
| **因果推論** | Causal Forest | DATAMINING_GUIDE.md §6.1 |
| | Double Machine Learning | DATAMINING_GUIDE.md §6.2 |
| | Synthetic Control | DATAMINING_GUIDE.md §6.3 |
| | Propensity Score Matching | DATAMINING_GUIDE.md §6.4 |
| **説明可能AI** | SHAP値分析 | advanced_datamining.py |
| | 特徴量重要度可視化 | advanced_datamining.py |

---

## 🎯 使用シナリオ別ガイド

### シナリオ1: 初めての戦略研究

**目標**: データ収集から論文執筆まで一貫した研究

```bash
# 1. データ収集（Phase 2-3）
python scripts/data_collectors.py --source compustat --years 2010-2023

# 2. 品質保証（Phase 6）
python scripts/data_quality_checker.py --input ./data/raw/compustat.csv

# 3. データマイニング（新機能）
python scripts/quick_datamining_demo.py --data ./data/final/panel.csv

# 4. 論文執筆（既存機能 + academic-paper-creation skill）
# Claude: "academic-paper-creation skillで論文を作成してください"
```

**所要時間**: 4-6週間

### シナリオ2: 因果推論研究（M&A効果分析）

**目標**: M&Aが企業イノベーションに与える異質的効果を推定

```python
from scripts.ml_causal_inference_integrated import CausalMLIntegration

causal = CausalMLIntegration(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./ma_causal_analysis/'
)

# Causal Forest（異質的処置効果）
cf_results = causal.causal_forest(
    treatment='ma_dummy',
    outcome='patent_count_change',
    controls=['firm_size', 'leverage', 'prior_ma', 'firm_age'],
    heterogeneity_vars=[
        'firm_size',          # 企業規模で効果が異なる？
        'rd_intensity',       # R&D能力で効果が異なる？
        'absorptive_capacity', # 吸収能力で効果が異なる？
        'industry_dynamism'   # 産業動態性で効果が異なる？
    ],
    discrete_treatment=True
)

# 結果の解釈
print(f"平均処置効果（ATE）: {cf_results['ate']:.4f}")
print(f"\n異質性分析:")
for var, analysis in cf_results['heterogeneity_analysis'].items():
    print(f"{var}:")
    print(f"  Low group: {analysis['ate_low']:.4f}")
    print(f"  High group: {analysis['ate_high']:.4f}")
    print(f"  Difference: {analysis['difference']:.4f} (p={analysis['p_value']:.4f})")
```

**論文での報告**:
- Table: Heterogeneous M&A Effects by Firm Characteristics
- Figure: Treatment Effect Distribution
- 理論的解釈: RBV、Dynamic Capabilities、TCE

**所要時間**: 2-3週間

### シナリオ3: 機械学習でパフォーマンス予測

**目標**: 戦略的選択から将来パフォーマンスを予測

```python
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining

dm = AdvancedStrategicDataMining(
    data=df_panel,
    firm_id='gvkey',
    time_var='year',
    output_dir='./performance_prediction/'
)

# 2年後ROAを予測
predictions = dm.predict_firm_performance(
    target='roa_lead2',
    features=[
        'rd_intensity_lag1',
        'advertising_intensity_lag1',
        'capital_intensity_lag1',
        'vertical_integration_lag1',
        'international_ratio_lag1',
        'firm_size_lag1',
        'leverage_lag1',
        'firm_age',
        'industry_concentration',
        'env_dynamism'
    ],
    model_type='ensemble',  # RF + GBM + XGBoost + LightGBM
    tune_hyperparameters=True,
    save_model=True
)

# モデル性能
best_model = predictions['best_model']
test_r2 = predictions['all_results'][best_model]['metrics']['test_r2']
print(f"Best Model: {best_model}, Test R² = {test_r2:.4f}")

# 特徴量重要度
importance = predictions['feature_importance']
print("\nTop 5 Strategic Drivers:")
print(importance.head())
```

**論文での報告**:
- Table: Model Performance Comparison
- Table: Feature Importance Rankings
- 理論的解釈: RBVの実証的検証

**所要時間**: 1-2週間

### シナリオ4: 完全自動化ワークフロー

**目標**: 設定ファイルで全分析を自動実行

```yaml
# datamining_config.yaml を編集

project:
  name: "my_strategy_research"
  output_dir: "./full_analysis_output/"

data:
  firm_id: "gvkey"
  time_var: "year"

strategic_groups:
  enabled: true
  features: ["rd_intensity", "capital_intensity", "advertising_intensity"]
  n_clusters: 4

performance_prediction:
  enabled: true
  target: "roa_lead1"
  features: ["rd_intensity_lag1", "firm_size_lag1", "leverage_lag1"]
  model_type: "ensemble"

causal_inference:
  causal_forest:
    enabled: true
    treatment: "ma_dummy"
    outcome: "roa_change"
```

```python
# 自動実行スクリプト
import yaml
from scripts.advanced_strategic_datamining import AdvancedStrategicDataMining

# 設定読み込み
with open('./scripts/datamining_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 全分析自動実行
# ... （complete_pipeline.py のロジック使用）
```

**所要時間**: 設定30分 + 実行時間（データサイズによる）

---

## 📚 詳細ドキュメント

### 必読ドキュメント

1. **[SKILL.md](./SKILL.md)** - スキル本体（Phase 1-8の詳細）
2. **[DATAMINING_GUIDE.md](./DATAMINING_GUIDE.md)** - データマイニング実践ガイド（70ページ）
3. **[DATAMINING_README.md](./DATAMINING_README.md)** - データマイニングクイックガイド

### 参考ドキュメント

- **INSTALLATION_GUIDE.md** - インストール手順
- **QUICKSTART_TUTORIAL.md** - 初心者向けチュートリアル
- **FAQ.md** - よくある質問
- **USECASE_GUIDE.md** - ユースケース集

### API Documentation

各スクリプトのdocstringを参照：
```python
# Python docstring
help(AdvancedStrategicDataMining)
help(CausalMLIntegration)
```

---

## 🎓 論文投稿チェックリスト

### データマイニング結果の報告

- [ ] **方法論の透明性**
  - [ ] 使用アルゴリズムの明記
  - [ ] ハイパーパラメータの報告
  - [ ] クロスバリデーション手法

- [ ] **モデル性能**
  - [ ] R² (Train/Test)
  - [ ] RMSE, MAE
  - [ ] CV性能

- [ ] **Robustness Checks**
  - [ ] 代替モデル（最低3種類）
  - [ ] 代替サンプル
  - [ ] Outlier除外後

### 因果推論結果の報告

- [ ] **内生性対処**
  - [ ] 内生性源泉の議論
  - [ ] 使用手法の理論的根拠
  - [ ] 識別戦略の説明

- [ ] **処置効果**
  - [ ] ATE/ATT with 95% CI
  - [ ] p値
  - [ ] 効果サイズの解釈

- [ ] **Diagnostics**
  - [ ] Balance diagnostics（PSM）
  - [ ] First-stage F-stat（IV）
  - [ ] Pre-treatment fit（SC）

---

## 💻 システム要件

### 推奨スペック

- **CPU**: 4コア以上
- **RAM**: 16GB以上（32GB推奨）
- **Storage**: 50GB以上の空き容量
- **OS**: macOS 13+, Windows 10+, Ubuntu 20.04+
- **Python**: 3.9, 3.10, 3.11

### 最小スペック

- **CPU**: 2コア
- **RAM**: 8GB
- **Storage**: 20GB
- **Python**: 3.9+

---

## ⚠️ 既知の制約事項

1. **EconML依存**
   - Causal Forest, DMLはEconMLが必須
   - インストールエラー時: `conda install econml`

2. **メモリ使用量**
   - 大規模データ（100万行以上）は要最適化
   - チャンク処理を推奨

3. **計算時間**
   - Causal Forest: 中〜大規模データで10-30分
   - Hyperparameter tuning: さらに時間増

4. **プラットフォーム差異**
   - Windows: Visual C++ Build Tools必要
   - macOS M1/M2: 全パッケージネイティブ対応
   - Linux: 通常問題なし

---

## 🆘 サポート

### 質問・バグ報告

Strategic Management Research Hub skillに問い合わせ：
```
Claude: "strategic-management-research-hub skillで[質問内容]"
```

### コミュニティ

- GitHub Issues（該当する場合）
- 研究コミュニティフォーラム

---

## 📖 引用

このツールを使用した研究では：

```
データ分析は、Strategic Management Research Hub v3.1を使用して実施された。
このシステムは、データマイニング（クラスタリング、機械学習予測、特徴量
重要度分析）および因果推論（Causal Forest, Double Machine Learning, 
Synthetic Control, Propensity Score Matching）の統合フレームワークを
提供し、戦略経営研究における定量分析の再現性と信頼性を確保している。
```

---

## 📄 ライセンス

MIT License - 学術・商用利用可

---

## 🗺️ ロードマップ

### v3.2（予定）

- [ ] 深層学習モデル統合（LSTM, Transformer）
- [ ] リアルタイムデータストリーム対応
- [ ] クラウド統合（AWS, GCP, Azure）
- [ ] 多言語対応（中国語、韓国語論文）

### v4.0（予定）

- [ ] Large Language Model統合（GPT-4, Claude）
- [ ] 自動理論構築支援
- [ ] インタラクティブダッシュボード
- [ ] コラボレーション機能

---

**最終更新**: 2025-11-01  
**バージョン**: 3.1  
**Next Update**: v3.2予定（2025-Q2）

**Happy Researching! 🎓📊🚀**

#戦略経営研究 #データマイニング #機械学習 #因果推論 #トップジャーナル #実証分析
