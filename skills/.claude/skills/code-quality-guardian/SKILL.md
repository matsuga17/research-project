---
name: code-quality-guardian
description: |
  研究コードの品質保証・再現性確保のための統合スキル。以下の機能を包括：
  (1) コードレビュー・品質チェック（Python/R/Stata）
  (2) 再現性パッケージング（AEA準拠）
  (3) バージョン管理・ドキュメント生成
  (4) テスト・検証フレームワーク
  (5) 依存関係管理・環境構築
  トリガー：「コードレビュー」「再現性」「reproducibility」「コード品質」「テスト」
allowed-tools: Bash,Read,Write
---

# Code Quality Guardian - 研究コード品質保証スキル

## 概要

学術研究における分析コードの品質保証と再現性確保を支援するスキルです。トップジャーナルのデータ・コード共有ポリシー（AEA、Management Science等）に準拠した再現性パッケージの作成を支援します。

## When to Use This Skill

以下の場合にこのスキルを使用：

- 分析コードの品質レビュー
- 再現性パッケージの作成
- コードのドキュメント生成
- テストスクリプトの作成
- 研究環境の構築・共有

**トリガーキーワード**：
- 「コードレビュー」「品質チェック」「Code Review」
- 「再現性」「Reproducibility」「Replication Package」
- 「テスト」「検証」「Validation」
- 「ドキュメント」「README」

---

# Part 1: コードレビュー・品質チェック

## 1.1 レビューチェックリスト

### 全般的品質基準

```
□ 読みやすさ・保守性
├── [ ] 意味のある変数名・関数名
├── [ ] 適切なコメント（なぜを説明）
├── [ ] 一貫したコーディングスタイル
├── [ ] 適切な関数分割（1関数1責任）
└── [ ] マジックナンバーの回避

□ 堅牢性
├── [ ] エラーハンドリング
├── [ ] 入力値の検証
├── [ ] エッジケースの処理
├── [ ] 欠損値の明示的処理
└── [ ] 適切なログ出力

□ 効率性
├── [ ] 不要な繰り返し計算の回避
├── [ ] 適切なデータ構造の使用
├── [ ] メモリ効率（大規模データ）
└── [ ] ベクトル化演算の活用

□ 再現性
├── [ ] 乱数シードの固定
├── [ ] 相対パスの使用
├── [ ] 依存関係の明示
└── [ ] バージョン指定
```

## 1.2 Python コード品質チェック

### 自動チェックスクリプト

```python
#!/usr/bin/env python3
"""
研究コード品質チェッカー
"""
import ast
import os
import re
from pathlib import Path

class ResearchCodeChecker:
    """研究用Pythonコードの品質チェック"""

    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.code = f.read()
        self.issues = []

    def check_all(self):
        """全チェックを実行"""
        self.check_random_seed()
        self.check_absolute_paths()
        self.check_magic_numbers()
        self.check_docstrings()
        self.check_error_handling()
        self.check_pandas_best_practices()
        return self.issues

    def check_random_seed(self):
        """乱数シードの固定確認"""
        seed_patterns = [
            r'np\.random\.seed\(',
            r'random\.seed\(',
            r'torch\.manual_seed\(',
            r'set_random_seed\(',
        ]

        has_random = any([
            'np.random' in self.code,
            'random.' in self.code,
            'torch.' in self.code,
            'sklearn' in self.code
        ])

        has_seed = any(re.search(p, self.code) for p in seed_patterns)

        if has_random and not has_seed:
            self.issues.append({
                'type': 'reproducibility',
                'severity': 'high',
                'message': '乱数を使用していますが、シードが設定されていません',
                'suggestion': 'np.random.seed(42) などでシードを固定してください'
            })

    def check_absolute_paths(self):
        """絶対パスの使用確認"""
        # Windowsパス
        windows_paths = re.findall(r'["\'][A-Z]:\\[^"\']+["\']', self.code)
        # Unixパス
        unix_paths = re.findall(r'["\']\/(?:Users|home|mnt)[^"\']+["\']', self.code)

        for path in windows_paths + unix_paths:
            self.issues.append({
                'type': 'reproducibility',
                'severity': 'high',
                'message': f'絶対パスが使用されています: {path}',
                'suggestion': 'Path(__file__).parent や os.path.join() で相対パスを使用してください'
            })

    def check_magic_numbers(self):
        """マジックナンバーの検出"""
        tree = ast.parse(self.code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Num):
                # 0, 1, 2, 100 などの一般的な数値は除外
                if node.n not in [0, 1, 2, 10, 100, 1000]:
                    if isinstance(node.n, (int, float)) and node.n > 10:
                        self.issues.append({
                            'type': 'maintainability',
                            'severity': 'low',
                            'message': f'マジックナンバー {node.n} が検出されました',
                            'suggestion': '意味のある定数名を定義してください'
                        })

    def check_docstrings(self):
        """Docstringの確認"""
        tree = ast.parse(self.code)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    self.issues.append({
                        'type': 'documentation',
                        'severity': 'medium',
                        'message': f'関数 {node.name} にdocstringがありません',
                        'suggestion': '関数の目的、引数、戻り値を説明するdocstringを追加してください'
                    })

    def check_error_handling(self):
        """エラーハンドリングの確認"""
        tree = ast.parse(self.code)

        # ファイル操作
        file_ops = ['open(', 'pd.read_', 'np.load', 'pickle.load']
        has_file_ops = any(op in self.code for op in file_ops)

        # try-except
        has_try = 'try:' in self.code

        if has_file_ops and not has_try:
            self.issues.append({
                'type': 'robustness',
                'severity': 'medium',
                'message': 'ファイル操作がありますが、エラーハンドリングがありません',
                'suggestion': 'try-except でファイルが見つからない場合の処理を追加してください'
            })

    def check_pandas_best_practices(self):
        """Pandasのベストプラクティス確認"""
        # inplace=True の使用
        if 'inplace=True' in self.code:
            self.issues.append({
                'type': 'best_practice',
                'severity': 'low',
                'message': 'inplace=True が使用されています',
                'suggestion': 'inplace=True は非推奨です。代入形式 df = df.method() を使用してください'
            })

        # チェーンインデックス
        if re.search(r'df\[[^\]]+\]\[[^\]]+\]', self.code):
            self.issues.append({
                'type': 'correctness',
                'severity': 'high',
                'message': 'チェーンインデックスが検出されました',
                'suggestion': '.loc[] または .iloc[] を使用してください'
            })

    def generate_report(self):
        """レポート生成"""
        issues = self.check_all()

        report = f"""
# コード品質レポート

**ファイル**: {self.file_path}
**検出された問題**: {len(issues)}

## サマリー

| 重要度 | 件数 |
|--------|------|
| High | {sum(1 for i in issues if i['severity'] == 'high')} |
| Medium | {sum(1 for i in issues if i['severity'] == 'medium')} |
| Low | {sum(1 for i in issues if i['severity'] == 'low')} |

## 詳細

"""
        for i, issue in enumerate(issues, 1):
            report += f"""
### {i}. [{issue['severity'].upper()}] {issue['type']}

**問題**: {issue['message']}

**推奨**: {issue['suggestion']}

---
"""
        return report


# 使用例
if __name__ == '__main__':
    checker = ResearchCodeChecker('analysis.py')
    print(checker.generate_report())
```

## 1.3 R コード品質チェック

```r
# R コード品質チェッカー
library(lintr)
library(styler)

check_r_code <- function(file_path) {
  issues <- list()

  # lintrによる静的解析
  lint_results <- lint(file_path)

  # 乱数シードの確認
  code <- readLines(file_path)
  code_text <- paste(code, collapse = "\n")

  if (grepl("sample\\(|rnorm\\(|runif\\(|rbinom\\(", code_text)) {
    if (!grepl("set\\.seed\\(", code_text)) {
      issues <- append(issues, list(
        type = "reproducibility",
        severity = "high",
        message = "乱数を使用していますが、set.seed()がありません"
      ))
    }
  }

  # 絶対パスの確認
  abs_paths <- gregexpr("[\"\']/(Users|home|mnt)/[^\"\']+[\"\']", code_text)
  if (length(abs_paths[[1]]) > 0 && abs_paths[[1]][1] != -1) {
    issues <- append(issues, list(
      type = "reproducibility",
      severity = "high",
      message = "絶対パスが使用されています"
    ))
  }

  return(list(
    lint_issues = lint_results,
    custom_issues = issues
  ))
}

# スタイル修正
style_r_file <- function(file_path) {
  styler::style_file(file_path)
}
```

## 1.4 Stata コード品質チェック

```stata
* Stata コード品質チェックリスト

/*
□ 基本設定
  - [ ] clear all で開始
  - [ ] set seed で乱数固定
  - [ ] version 指定
  - [ ] memory設定（必要な場合）

□ パス管理
  - [ ] global でルートパス定義
  - [ ] 相対パス使用
  - [ ] cd は最小限

□ ログ管理
  - [ ] log using でログ開始
  - [ ] log close でログ終了

□ データ管理
  - [ ] 元データは読み取り専用
  - [ ] tempfile/tempvar の活用
  - [ ] label の適切な使用
*/

* 推奨テンプレート
version 17.0
clear all
set more off
set seed 12345

* パス設定
global root "."
global data "$root/data"
global output "$root/output"
global code "$root/code"

* ログ開始
cap log close
log using "$output/analysis_log.txt", replace text

* メイン分析
do "$code/01_data_cleaning.do"
do "$code/02_analysis.do"
do "$code/03_robustness.do"

* ログ終了
log close
```

---

# Part 2: 再現性パッケージング（AEA準拠）

## 2.1 ディレクトリ構造

```
replication_package/
├── README.md                 # 必須：再現手順
├── LICENSE                   # ライセンス
├── data/
│   ├── raw/                  # 生データ（利用可能な場合）
│   │   └── .gitkeep
│   ├── processed/            # 処理済みデータ
│   │   └── analysis_data.csv
│   └── codebook.md          # 変数説明
├── code/
│   ├── 00_master.py         # マスタースクリプト
│   ├── 01_data_cleaning.py
│   ├── 02_analysis.py
│   ├── 03_tables.py
│   └── 04_figures.py
├── output/
│   ├── tables/              # 表の出力
│   ├── figures/             # 図の出力
│   └── logs/                # ログファイル
├── docs/
│   └── variable_definitions.md
├── requirements.txt          # Python依存関係
├── environment.yml           # Conda環境
└── Dockerfile               # Docker設定（オプション）
```

## 2.2 README テンプレート

```markdown
# Replication Package

**論文タイトル**: [論文タイトル]
**著者**: [著者名]
**ジャーナル**: [ジャーナル名]
**DOI**: [DOI]

## 概要

このリポジトリには、上記論文の分析結果を再現するために必要な
コードとデータが含まれています。

## データ利用可能性

### 含まれるデータ
- `data/processed/analysis_data.csv`: 分析用データセット

### 外部データソース
| データ | ソース | アクセス方法 | 利用条件 |
|--------|--------|-------------|---------|
| [データ名] | [ソース] | [URL/連絡先] | [条件] |

## 計算環境

### ソフトウェア要件
- Python 3.9+
- 必要パッケージ: `requirements.txt` 参照

### 環境構築

```bash
# venv使用の場合
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# conda使用の場合
conda env create -f environment.yml
conda activate replication

# Docker使用の場合
docker build -t replication .
docker run -it replication
```

## 再現手順

### クイックスタート

```bash
python code/00_master.py
```

### 個別実行

1. データ前処理: `python code/01_data_cleaning.py`
2. 主要分析: `python code/02_analysis.py`
3. 表の生成: `python code/03_tables.py`
4. 図の生成: `python code/04_figures.py`

### 出力ファイルと論文の対応

| 出力ファイル | 論文での位置 |
|-------------|-------------|
| `output/tables/table1.tex` | Table 1 (p.XX) |
| `output/tables/table2.tex` | Table 2 (p.XX) |
| `output/figures/figure1.pdf` | Figure 1 (p.XX) |

## 実行時間

| スクリプト | 推定実行時間 |
|-----------|-------------|
| 01_data_cleaning.py | 約5分 |
| 02_analysis.py | 約30分 |
| 全体 | 約1時間 |

テスト環境: [CPU], [RAM], [OS]

## 連絡先

質問がある場合は [email] までご連絡ください。
```

## 2.3 マスタースクリプト

```python
#!/usr/bin/env python3
"""
マスタースクリプト: 全分析を順次実行

Usage:
    python 00_master.py [--skip-cleaning] [--tables-only]
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# 設定
SCRIPTS = [
    ('01_data_cleaning.py', 'データクリーニング'),
    ('02_analysis.py', '主要分析'),
    ('03_tables.py', '表の生成'),
    ('04_figures.py', '図の生成'),
]

def setup_logging():
    """ログディレクトリの設定"""
    log_dir = Path('output/logs')
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'master_log_{timestamp}.txt'

    return log_file

def run_script(script_name, description, log_file):
    """個別スクリプトの実行"""
    print(f"\n{'='*60}")
    print(f"実行中: {description} ({script_name})")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, f'code/{script_name}'],
            capture_output=True,
            text=True,
            check=True
        )

        elapsed = time.time() - start_time

        # ログに記録
        with open(log_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Script: {script_name}\n")
            f.write(f"Status: SUCCESS\n")
            f.write(f"Time: {elapsed:.2f} seconds\n")
            f.write(f"Output:\n{result.stdout}\n")

        print(f"✓ 完了 ({elapsed:.2f}秒)")
        return True

    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time

        with open(log_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Script: {script_name}\n")
            f.write(f"Status: FAILED\n")
            f.write(f"Time: {elapsed:.2f} seconds\n")
            f.write(f"Error:\n{e.stderr}\n")

        print(f"✗ エラー: {e.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description='再現パッケージの実行')
    parser.add_argument('--skip-cleaning', action='store_true',
                        help='データクリーニングをスキップ')
    parser.add_argument('--tables-only', action='store_true',
                        help='表の生成のみ実行')
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════╗
║           Replication Package - Master Script            ║
║                                                          ║
║  論文タイトル: [論文タイトル]                              ║
╚══════════════════════════════════════════════════════════╝
""")

    log_file = setup_logging()
    print(f"ログファイル: {log_file}")

    # 実行するスクリプトの決定
    scripts_to_run = SCRIPTS.copy()

    if args.skip_cleaning:
        scripts_to_run = [s for s in scripts_to_run
                         if 'cleaning' not in s[0]]

    if args.tables_only:
        scripts_to_run = [s for s in scripts_to_run
                         if 'table' in s[0]]

    # 実行
    total_start = time.time()
    results = []

    for script, desc in scripts_to_run:
        success = run_script(script, desc, log_file)
        results.append((script, success))

        if not success:
            print(f"\n⚠ {script} でエラーが発生したため、処理を中断します")
            break

    # サマリー
    total_time = time.time() - total_start

    print(f"""
╔══════════════════════════════════════════════════════════╗
║                      実行サマリー                          ║
╚══════════════════════════════════════════════════════════╝
""")

    for script, success in results:
        status = "✓ 成功" if success else "✗ 失敗"
        print(f"  {status}: {script}")

    print(f"\n総実行時間: {total_time:.2f}秒 ({total_time/60:.1f}分)")

    # 成功した場合のみ
    if all(s for _, s in results):
        print("""
╔══════════════════════════════════════════════════════════╗
║              全スクリプトが正常に完了しました               ║
║                                                          ║
║  出力ファイル:                                            ║
║    - output/tables/ に表                                  ║
║    - output/figures/ に図                                 ║
╚══════════════════════════════════════════════════════════╝
""")

if __name__ == '__main__':
    main()
```

## 2.4 環境設定ファイル

### requirements.txt

```
# Core
numpy>=1.21.0
pandas>=1.3.0
scipy>=1.7.0

# Statistics
statsmodels>=0.13.0
linearmodels>=4.25

# Visualization
matplotlib>=3.4.0
seaborn>=0.11.0

# Data
openpyxl>=3.0.0
xlrd>=2.0.0

# Utilities
tqdm>=4.62.0
python-dotenv>=0.19.0

# Reproducibility
# pip freeze > requirements_full.txt でフル版を生成
```

### environment.yml (Conda)

```yaml
name: replication
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy>=1.21
  - pandas>=1.3
  - scipy>=1.7
  - statsmodels>=0.13
  - matplotlib>=3.4
  - seaborn>=0.11
  - jupyter
  - pip
  - pip:
    - linearmodels>=4.25
```

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /replication

# システム依存関係
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# コードとデータ
COPY . .

# 実行
CMD ["python", "code/00_master.py"]
```

---

# Part 3: テスト・検証フレームワーク

## 3.1 ユニットテスト

```python
"""
tests/test_analysis.py
分析コードのユニットテスト
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# テスト対象のインポート
import sys
sys.path.append('code')
from analysis_functions import (
    winsorize,
    calculate_roa,
    run_regression
)

class TestDataProcessing:
    """データ処理関数のテスト"""

    def test_winsorize_basic(self):
        """Winsorizeの基本テスト"""
        data = pd.Series([1, 2, 3, 4, 5, 100])
        result = winsorize(data, limits=(0.1, 0.1))

        # 外れ値が処理されていることを確認
        assert result.max() < 100
        assert len(result) == len(data)

    def test_winsorize_preserves_median(self):
        """Winsorizeが中央値を保持するか"""
        data = pd.Series(np.random.randn(1000))
        result = winsorize(data, limits=(0.01, 0.01))

        # 中央値はほぼ同じはず
        assert abs(data.median() - result.median()) < 0.1

    def test_calculate_roa(self):
        """ROA計算のテスト"""
        df = pd.DataFrame({
            'net_income': [100, 200, -50],
            'total_assets': [1000, 2000, 500]
        })

        result = calculate_roa(df)

        expected = pd.Series([0.1, 0.1, -0.1])
        pd.testing.assert_series_equal(result, expected)

    def test_calculate_roa_zero_assets(self):
        """総資産ゼロの場合のROA"""
        df = pd.DataFrame({
            'net_income': [100],
            'total_assets': [0]
        })

        result = calculate_roa(df)

        # ゼロ除算はNaNになるべき
        assert pd.isna(result.iloc[0])


class TestRegression:
    """回帰分析のテスト"""

    @pytest.fixture
    def sample_data(self):
        """テスト用サンプルデータ"""
        np.random.seed(42)
        n = 100

        return pd.DataFrame({
            'Y': np.random.randn(n),
            'X1': np.random.randn(n),
            'X2': np.random.randn(n),
            'firm_id': np.repeat(range(20), 5),
            'year': np.tile(range(5), 20)
        })

    def test_regression_output_structure(self, sample_data):
        """回帰結果の構造確認"""
        result = run_regression(sample_data, 'Y ~ X1 + X2')

        # 必要な属性の確認
        assert hasattr(result, 'params')
        assert hasattr(result, 'pvalues')
        assert hasattr(result, 'rsquared')

    def test_regression_known_relationship(self):
        """既知の関係でのテスト"""
        np.random.seed(42)
        n = 1000

        X = np.random.randn(n)
        Y = 2 * X + np.random.randn(n) * 0.1  # Y = 2X + noise

        df = pd.DataFrame({'Y': Y, 'X': X})
        result = run_regression(df, 'Y ~ X')

        # 係数は約2であるべき
        assert abs(result.params['X'] - 2) < 0.1


class TestReproducibility:
    """再現性のテスト"""

    def test_random_seed_consistency(self):
        """乱数シードの一貫性"""
        np.random.seed(42)
        result1 = np.random.randn(100)

        np.random.seed(42)
        result2 = np.random.randn(100)

        np.testing.assert_array_equal(result1, result2)

    def test_output_files_exist(self):
        """出力ファイルの存在確認"""
        expected_files = [
            'output/tables/table1.tex',
            'output/tables/table2.tex',
            'output/figures/figure1.pdf',
        ]

        for file_path in expected_files:
            assert Path(file_path).exists(), f"{file_path} が見つかりません"


# pytestの実行
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

## 3.2 結果の検証

```python
"""
tests/test_results.py
論文の結果の再現性検証
"""
import pandas as pd
import numpy as np

class TestPaperResults:
    """論文に報告された結果との比較"""

    # 論文の報告値（手動で入力）
    PAPER_RESULTS = {
        'table1': {
            'main_effect': 0.123,
            'main_effect_se': 0.045,
            'n_obs': 5000,
            'r_squared': 0.234
        },
        'table2': {
            'interaction': 0.056,
            'interaction_se': 0.021
        }
    }

    def test_table1_main_effect(self):
        """Table 1の主効果の再現"""
        # 再現結果の読み込み
        results = pd.read_csv('output/tables/table1_results.csv')

        paper_value = self.PAPER_RESULTS['table1']['main_effect']
        reproduced_value = results.loc[
            results['variable'] == 'main_effect', 'coefficient'
        ].values[0]

        # 許容誤差: 0.001
        assert abs(paper_value - reproduced_value) < 0.001, \
            f"主効果が一致しません: 論文={paper_value}, 再現={reproduced_value}"

    def test_sample_size(self):
        """サンプルサイズの確認"""
        results = pd.read_csv('output/tables/table1_results.csv')

        paper_n = self.PAPER_RESULTS['table1']['n_obs']
        reproduced_n = results['n_obs'].values[0]

        assert paper_n == reproduced_n, \
            f"サンプルサイズが一致しません: 論文={paper_n}, 再現={reproduced_n}"
```

## 3.3 データ整合性チェック

```python
"""
code/data_validation.py
データの整合性検証
"""
import pandas as pd
import numpy as np

class DataValidator:
    """データ検証クラス"""

    def __init__(self, df):
        self.df = df
        self.errors = []
        self.warnings = []

    def validate_all(self):
        """全検証を実行"""
        self.check_missing_values()
        self.check_duplicates()
        self.check_value_ranges()
        self.check_accounting_identities()
        return self.errors, self.warnings

    def check_missing_values(self):
        """欠損値チェック"""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100

        for col, pct in missing_pct.items():
            if pct > 50:
                self.errors.append(f"{col}: 欠損率が50%を超えています ({pct:.1f}%)")
            elif pct > 20:
                self.warnings.append(f"{col}: 欠損率が20%を超えています ({pct:.1f}%)")

    def check_duplicates(self):
        """重複チェック"""
        if 'firm_id' in self.df.columns and 'year' in self.df.columns:
            duplicates = self.df.duplicated(subset=['firm_id', 'year'], keep=False)
            if duplicates.any():
                n_dups = duplicates.sum()
                self.errors.append(f"firm_id-year で {n_dups} 件の重複があります")

    def check_value_ranges(self):
        """値の範囲チェック"""
        checks = {
            'ROA': (-1, 1),
            'Leverage': (0, 10),
            'Size': (0, None),
        }

        for col, (min_val, max_val) in checks.items():
            if col in self.df.columns:
                if min_val is not None:
                    below_min = (self.df[col] < min_val).sum()
                    if below_min > 0:
                        self.warnings.append(
                            f"{col}: {below_min}件が下限値({min_val})を下回っています"
                        )
                if max_val is not None:
                    above_max = (self.df[col] > max_val).sum()
                    if above_max > 0:
                        self.warnings.append(
                            f"{col}: {above_max}件が上限値({max_val})を超えています"
                        )

    def check_accounting_identities(self):
        """会計恒等式のチェック"""
        if all(col in self.df.columns for col in ['assets', 'liabilities', 'equity']):
            # 資産 = 負債 + 資本
            diff = abs(self.df['assets'] - self.df['liabilities'] - self.df['equity'])
            violations = (diff > 1).sum()  # 許容誤差: 1

            if violations > 0:
                self.errors.append(
                    f"会計恒等式に {violations} 件の違反があります"
                )

    def generate_report(self):
        """検証レポート生成"""
        self.validate_all()

        report = f"""
# データ検証レポート

## サマリー
- **総レコード数**: {len(self.df):,}
- **エラー**: {len(self.errors)}件
- **警告**: {len(self.warnings)}件

## エラー
"""
        for error in self.errors:
            report += f"- ❌ {error}\n"

        report += "\n## 警告\n"
        for warning in self.warnings:
            report += f"- ⚠️ {warning}\n"

        return report
```

---

# Part 4: 起動コマンド

## コードレビューモード
```
Code Quality Guardian起動

目的: コードレビュー
対象: [ファイルパス または ディレクトリ]
言語: [Python/R/Stata]
出力: [レビューレポート]
```

## 再現性パッケージモード
```
Code Quality Guardian起動

目的: 再現性パッケージ作成
プロジェクト: [プロジェクトルート]
準拠基準: [AEA/Management Science/カスタム]
出力: [パッケージ構造/README/設定ファイル]
```

## テスト作成モード
```
Code Quality Guardian起動

目的: テスト作成
対象コード: [ファイルパス]
テストタイプ: [ユニット/統合/結果検証]
出力: [テストスクリプト]
```

## 検証モード
```
Code Quality Guardian起動

目的: データ検証
データファイル: [CSVパス]
検証項目: [欠損値/範囲/重複/恒等式]
出力: [検証レポート]
```

---

## 連携スキル

| スキル名 | 役割 |
|----------|------|
| strategic-research-platform | 研究デザイン・統計分析コードの生成 |
| research-data-hub | データ収集・品質管理 |
| academic-research-suite | 文献レビュー・論文執筆・引用管理 |
| document-design-suite | 結果の可視化・図表作成 |
| thinking-toolkit | 理論構築・批判的分析 |

---

## 参考基準

- AEA Data and Code Availability Policy
- Journal of Finance Replication Policy
- Management Science Code and Data Policy
- TIER Protocol (Teaching Integrity in Empirical Research)

---

**バージョン**: 1.0.0
**作成日**: 2025-11-28
