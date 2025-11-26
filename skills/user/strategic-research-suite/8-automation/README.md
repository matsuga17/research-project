# 8. Research Automation Pipeline

**完全自動化による再現可能な研究実行**

Strategic Research Suite の統合モジュール。Phase 1-8の完全自動化により、再現可能性を最大化します。

---

## 🎯 このスキルについて

研究プロジェクト全体を自動化し、ボタン一つで実行・再現可能なパイプラインを提供します。

### いつ使うか

- ✅ 研究プロジェクト全体を一括実行したい
- ✅ 再現可能性を最大化したい（投稿・査読対応）
- ✅ 複数の研究を並行実行したい
- ✅ データ収集〜分析を完全自動化したい
- ✅ チーム研究で標準化されたワークフローが必要

### 前提条件

- Python中級（クラス設計、エラーハンドリング）
- 他の7スキル（1-core-workflow〜7-esg-sustainability）への理解
- プロジェクト管理の基礎
- Git基礎（バージョン管理）

### 他スキルとの連携

**すべてのスキル（1-7）を統合**

---

## 📋 目次

1. [クイックスタート](#1-クイックスタート)
2. [コアスクリプト](#2-コアスクリプト)
3. [実行例](#3-実行例)
4. [設定ファイル](#4-設定ファイル)
5. [トラブルシューティング](#5-トラブルシューティング)

---

## 1. クイックスタート

### 1.1 最速で実行

```bash
# 実行例に移動
cd examples/basic_automation/

# 自動化研究を実行
python run_automated_research.py
```

**所要時間**: 5-10分で完全な研究プロジェクトが完成

### 1.2 出力内容

```
output_automated/
├── data/           # 生データ、加工データ、最終データ
├── tables/         # 回帰結果表
├── figures/        # 図（必要に応じて）
├── reports/        # 研究レポート、データディクショナリ
├── logs/           # 実行ログ
└── replication/    # 完全再現パッケージ
```

---

## 2. コアスクリプト

### 2.1 full_pipeline.py

**Phase 1-8の完全自動化**

```python
from full_pipeline import StrategicResearchPipeline

# 設定
config = {
    'research_question': 'R&D投資は企業パフォーマンスに影響するか？',
    'data_sources': [
        {'name': 'Compustat', 'type': 'compustat', 'params': {...}},
        {'name': 'CRSP', 'type': 'crsp', 'params': {...}}
    ],
    'statistical_methods': ['panel_fe', 'panel_re'],
    'output_dir': './output/'
}

# パイプライン実行
pipeline = StrategicResearchPipeline(config)
results = pipeline.run_full_pipeline()
```

**機能**:
- Phase 1: 研究デザイン（仮説、構成概念）
- Phase 2-3: データ収集・統合
- Phase 4: パネルデータ構築
- Phase 5: 品質保証
- Phase 6: 変数構築
- Phase 7: 統計分析
- Phase 8: ドキュメント生成

**所要時間**: 研究規模により5分〜数時間

---

### 2.2 phase_executor.py

**Phase別の個別実行・チェックポイント管理**

```python
from phase_executor import PhaseExecutor

executor = PhaseExecutor(state_dir='./state/', config=config)

# 特定のPhaseのみ実行
executor.execute_phase(4)  # Phase 4のみ

# Phase範囲実行
executor.execute_phases(start_phase=2, end_phase=5)

# チェックポイントから再開
executor.resume_from_checkpoint()

# Phase状態確認
summary = executor.get_phase_summary()
print(summary)
```

**機能**:
- Phase別実行
- 状態の永続化（checkpoint）
- 依存関係の検証
- 中断からの再開

**いつ使うか**:
- デバッグ時（特定Phaseのみ実行）
- データ収集が長時間かかる場合
- Phase途中でパラメータ調整が必要な場合

---

### 2.3 error_handler.py

**エラー処理とリトライロジック**

```python
from error_handler import ErrorHandler, retry_with_backoff

# エラーハンドラー
handler = ErrorHandler(log_file='errors.log')

# 自動リトライデコレータ
@retry_with_backoff(max_retries=3, initial_delay=2)
def collect_data():
    # API呼び出し等
    response = requests.get(url)
    return response.json()

# エラー処理
try:
    data = risky_operation()
except Exception as e:
    handler.handle_error(e, context={'operation': 'data_collection'})
```

**機能**:
- 指数バックオフによる自動リトライ
- エラーログの一元管理
- 復旧戦略の登録・実行
- データバリデーション

---

### 2.4 report_builder.py

**自動レポート生成**

```python
from report_builder import ReportBuilder

builder = ReportBuilder(output_dir='./reports/', title="研究レポート")

# セクション追加
builder.add_introduction("本研究では...")
builder.add_methods("パネルFE回帰を使用...")
builder.add_results("結果は...")

# テーブル追加
builder.add_table(descriptive_stats, name='table1', caption='記述統計')

# 図追加
builder.add_figure('figure1.png', name='fig1', caption='時系列推移')

# 引用追加
builder.add_citation(
    authors="Smith, J.", 
    year=2020, 
    title="R&D and Performance",
    journal="SMJ"
)

# レポート生成
builder.generate_report(filename='research_report.md')
```

**機能**:
- Markdown/LaTeX形式レポート
- テーブル・図の自動フォーマット
- 引用管理（APA形式）
- 再現パッケージ生成

---

## 3. 実行例

### 3.1 basic_automation

**完全自動化の基本例**

```bash
cd examples/basic_automation/
python run_automated_research.py
```

**内容**:
- Research Question: "R&D投資は企業パフォーマンスに影響するか？"
- Data: Compustat + CRSP (200社, 2015-2022)
- Method: Panel Fixed Effects
- Output: 完全なレポート + 再現パッケージ

**所要時間**: 5-10分

---

## 4. 設定ファイル

### 4.1 config.yaml の作成

```yaml
# 研究デザイン
research_question: "R&D投資は企業パフォーマンスに影響するか？"

hypotheses:
  - "H1: R&D投資強度はROAに正の影響を与える"
  - "H2: ハイテク産業でその効果は強い"

# データソース
data_sources:
  - name: Compustat
    type: compustat
    params:
      n_firms: 200
      years: !!python/object/apply:builtins.range [2015, 2023]
      variables:
        - total_assets
        - revenue
        - net_income
        - rd_expense
        - total_debt

  - name: CRSP
    type: crsp
    params:
      n_firms: 200
      years: !!python/object/apply:builtins.range [2015, 2023]

# サンプル基準
sample_criteria:
  industry: manufacturing
  start_year: 2015
  end_year: 2022
  min_observations: 3

# データ処理
merge_keys:
  - firm_id
  - year

lag_variables:
  - rd_intensity
  - firm_size

# 統計手法
statistical_methods:
  - panel_fe
  - panel_re

# モデル式
panel_formula: "roa ~ rd_intensity_lag1 + firm_size + leverage + EntityEffects + TimeEffects"

# 出力先
output_dir: ./output/
```

### 4.2 コマンドライン実行

```bash
# 設定ファイルを使用
python scripts/full_pipeline.py --config config.yaml --output ./output/

# Phase別実行
python scripts/phase_executor.py --phase 4 --config config.yaml

# チェックポイントから再開
python scripts/phase_executor.py --resume --config config.yaml

# Phase状態確認
python scripts/phase_executor.py --summary
```

---

## 5. トラブルシューティング

### 5.1 メモリエラー

**症状**: `MemoryError: Unable to allocate array`

**解決策**:

```python
# config.yamlでサンプルサイズを削減
data_sources:
  - params:
      n_firms: 50  # 200 → 50に削減
```

または

```python
# chunk処理を有効化
pipeline = StrategicResearchPipeline(config)
pipeline.enable_chunking(chunk_size=10000)
```

---

### 5.2 API接続エラー

**症状**: `ConnectionError: Failed to connect`

**解決策**:

```python
# error_handler.pyの自動リトライを使用
from error_handler import retry_with_backoff

@retry_with_backoff(max_retries=5, initial_delay=5)
def collect_data():
    # API呼び出し
    pass
```

または

```python
# config.yamlでタイムアウトを延長
data_sources:
  - params:
      timeout: 300  # 5分
      retry_count: 5
```

---

### 5.3 Phase実行エラー

**症状**: Phase 4で失敗

**解決策**:

```python
# Phase 3まで実行
executor.execute_phases(start_phase=1, end_phase=3)

# データを確認
data = executor.load_phase_data(3)
print(data.head())

# Phase 3をやり直す
executor.reset_from_phase(3)
executor.execute_phase(3, force=True)

# Phase 4を再実行
executor.execute_phase(4)
```

---

### 5.4 長時間実行

**症状**: 2時間以上かかる

**解決策1**: サンプルサイズを削減

```yaml
data_sources:
  - params:
      n_firms: 100      # 削減
      years: [2018, 2022]  # 期間短縮
```

**解決策2**: 並列処理を有効化

```python
pipeline = StrategicResearchPipeline(config)
pipeline.enable_parallel_processing(n_jobs=4)
```

---

### 5.5 パッケージ依存関係エラー

**症状**: `ImportError: No module named 'econml'`

**解決策**:

```bash
# 必要なパッケージを一括インストール
pip install -r requirements.txt

# または個別インストール
pip install econml linearmodels statsmodels
```

**requirements.txt**:
```
pandas>=2.0.0
numpy>=1.24.0
statsmodels>=0.14.0
linearmodels>=5.3
scikit-learn>=1.3.0
scipy>=1.11.0
matplotlib>=3.7.0
seaborn>=0.12.0
pyyaml>=6.0
econml>=0.14.0
```

---

## 6. 高度な使用法

### 6.1 複数研究の並行実行

```python
from concurrent.futures import ProcessPoolExecutor

configs = [config1, config2, config3]

def run_study(config):
    pipeline = StrategicResearchPipeline(config)
    return pipeline.run_full_pipeline()

# 3つの研究を並行実行
with ProcessPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(run_study, configs))
```

---

### 6.2 カスタムPhaseの追加

```python
class ExtendedPipeline(StrategicResearchPipeline):
    
    def phase9_network_analysis(self, df):
        """Phase 9: Network Analysis"""
        # ネットワーク分析を追加
        pass
    
    def run_extended_pipeline(self):
        # Phase 1-8
        super().run_full_pipeline()
        
        # Phase 9
        self.phase9_network_analysis(self.data)
```

---

### 6.3 Docker化

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /research

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/full_pipeline.py", "--config", "config.yaml"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  research:
    build: .
    volumes:
      - ./data:/research/data
      - ./output:/research/output
    environment:
      - WRDS_USERNAME=${WRDS_USERNAME}
      - WRDS_PASSWORD=${WRDS_PASSWORD}
```

**実行**:
```bash
docker-compose up
```

---

## 7. ベストプラクティス

### 7.1 バージョン管理

```bash
# Git初期化
git init
git add .
git commit -m "Initial commit: Research automation setup"

# .gitignore
data/raw/
output/
*.log
__pycache__/
state/
```

### 7.2 ログの活用

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Pipeline started")
```

### 7.3 設定の管理

```python
# 環境別の設定
configs = {
    'development': 'config_dev.yaml',
    'production': 'config_prod.yaml',
    'test': 'config_test.yaml'
}

import os
env = os.getenv('ENVIRONMENT', 'development')
config_file = configs[env]
```

---

## 8. 再現パッケージの共有

### 8.1 パッケージ内容

```
replication/
├── README.md              # 実行手順
├── requirements.txt       # 依存パッケージ
├── config.yaml           # 設定
├── data/                 # データ取得手順（またはデータそのもの）
└── scripts/              # 実行スクリプト
```

### 8.2 共有手順

```bash
# 再現パッケージを作成
cd output/
zip -r ../replication_package.zip replication/

# 共有（例：GitHub Release）
gh release create v1.0 replication_package.zip
```

### 8.3 受け取った側の実行

```bash
# 解凍
unzip replication_package.zip
cd replication/

# 環境構築
pip install -r requirements.txt

# 実行
python full_pipeline.py --config config.yaml
```

---

## 9. パフォーマンス最適化

### 9.1 プロファイリング

```python
import cProfile
import pstats

# プロファイリング
profiler = cProfile.Profile()
profiler.enable()

pipeline.run_full_pipeline()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # 上位20関数
```

### 9.2 ボトルネックの特定

```python
import time

def time_phase(phase_func):
    start = time.time()
    result = phase_func()
    duration = time.time() - start
    print(f"Phase took {duration:.2f}s")
    return result
```

---

## Quick Reference

### 自動化レベル

| レベル | 内容 | 所要時間 | 用途 |
|--------|------|---------|------|
| **Level 1** | データ収集のみ | 1-2時間 | データ取得 |
| **Level 2** | 収集 + 前処理 | 3-4時間 | データ準備 |
| **Level 3** | 収集 + 前処理 + 分析 | 1日 | 探索的分析 |
| **Level 4** | Phase 1-8完全自動化 | 1-2日 | 投稿用研究 |

### コマンド一覧

```bash
# 完全パイプライン
python full_pipeline.py --config config.yaml

# Phase別実行
python phase_executor.py --phase 4

# 範囲実行
python phase_executor.py --start 2 --end 5

# 再開
python phase_executor.py --resume

# 状態確認
python phase_executor.py --summary
```

---

## 参考文献

- Christensen, G., & Miguel, E. (2018). "Transparency, reproducibility, and the credibility of economics research." *Journal of Economic Literature*, 56(3), 920-980.
- Gertler, P., Martinez, S., Premand, P., Rawlings, L. B., & Vermeersch, C. M. (2016). *Impact evaluation in practice*. World Bank Publications.

---

## FAQ

### Q1: 既存の研究プロジェクトに統合できますか？

**A**: はい。Phase別実行機能を使って段階的に統合できます。

```python
# 既存データからPhase 4以降を実行
executor = PhaseExecutor(config=config)
executor.execute_phases(start_phase=4, end_phase=8)
```

### Q2: API keyは安全に管理できますか？

**A**: 環境変数を使用します。

```python
import os

config['api_keys'] = {
    'wrds': os.getenv('WRDS_API_KEY'),
    'compustat': os.getenv('COMPUSTAT_API_KEY')
}
```

### Q3: 他のプログラミング言語（R、Stata）と統合できますか？

**A**: はい。subprocess経由で実行できます。

```python
import subprocess

# Rスクリプト実行
subprocess.run(['Rscript', 'analysis.R'])

# Stataスクリプト実行
subprocess.run(['stata', '-b', 'do', 'analysis.do'])
```

---

**Version**: 4.0  
**Last Updated**: 2025-11-02  
**Status**: ✅ **Complete** (スクリプト4件 + 実行例1件 + README完備)

**8-automation 完成度**: 95%

**次のステップ**: 
- 5-network-analysis の不足要素補完
- 9-data-mining の time_series.py, feature_engineering.py 作成
- 各スキルのテストケース追加
