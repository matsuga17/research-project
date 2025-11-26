# Strategic Research Suite - インストールガイド

## 📋 目次

1. [システム要件](#システム要件)
2. [基本インストール](#基本インストール)
3. [依存ライブラリの詳細](#依存ライブラリの詳細)
4. [トラブルシューティング](#トラブルシューティング)
5. [環境別の注意事項](#環境別の注意事項)
6. [動作確認](#動作確認)

---

## システム要件

### Python バージョン
- **推奨**: Python 3.10 以上
- **対応**: Python 3.9, 3.10, 3.11
- Python 3.12 は一部ライブラリの互換性に注意

### オペレーティングシステム
- macOS 10.15 以上
- Linux (Ubuntu 20.04+, CentOS 8+)
- Windows 10/11 (一部ツールで制約あり)

### ハードウェア
- **メモリ**: 最低 8GB、推奨 16GB 以上
- **ストレージ**: 5GB 以上の空き容量
- **CPU**: マルチコア推奨（並列処理対応）

---

## 基本インストール

### ステップ 1: Python 環境の確認

```bash
# Python バージョン確認
python3 --version

# pip の更新
python3 -m pip install --upgrade pip
```

### ステップ 2: 仮想環境の作成（推奨）

```bash
# プロジェクトディレクトリに移動
cd /path/to/strategic-research-suite

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### ステップ 3: 基本ライブラリのインストール

```bash
# requirements.txt から一括インストール
pip install -r requirements.txt

# または、主要ライブラリを個別インストール
pip install pandas numpy scipy statsmodels scikit-learn
pip install linearmodels econml doubleml
pip install matplotlib seaborn plotly
pip install networkx nltk spacy
```

### ステップ 4: 追加設定

```bash
# spaCy の英語モデルをダウンロード
python -m spacy download en_core_web_sm

# NLTK データのダウンロード
python -m nltk.downloader punkt vader_lexicon stopwords
```

---

## 依存ライブラリの詳細

### 🔴 重要: `linear_model` エラーの解決

**問題**: 「`linear_model` が見つからない」というエラーが発生する場合

**原因**: 以下の2つのライブラリを混同している可能性があります：
1. `sklearn.linear_model` (scikit-learn)
2. `linearmodels` (パネルデータ分析用の別ライブラリ)

**解決策**:

```bash
# 両方のライブラリをインストール
pip install scikit-learn>=1.3.0
pip install linearmodels>=5.3
```

**インポート方法の違い**:

```python
# scikit-learn の場合
from sklearn.linear_model import LinearRegression, Lasso, Ridge

# linearmodels の場合（パネルデータ分析）
from linearmodels.panel import PanelOLS, RandomEffects
```

### 📊 統計・計量経済学ライブラリ

```bash
# パネルデータ分析
pip install linearmodels>=5.3

# 因果推論
pip install econml>=0.14.0
pip install doubleml>=0.7.0

# 統計モデリング
pip install statsmodels>=0.14.0
```

### 🤖 機械学習ライブラリ

```bash
pip install scikit-learn>=1.3.0
pip install xgboost>=2.0.0  # オプション: 高度な機械学習
```

### 📝 テキスト分析ライブラリ

```bash
pip install nltk>=3.8
pip install spacy>=3.6.0
pip install vaderSentiment>=3.3.2
pip install gensim>=4.3.0
pip install textblob>=0.17.1

# spaCy の言語モデル
python -m spacy download en_core_web_sm

# 日本語テキスト処理（オプション）
pip install mecab-python3>=1.0.6
pip install fugashi>=1.3.0

# 中国語テキスト処理（オプション）
pip install jieba>=0.42.1
```

### 🌐 ネットワーク分析ライブラリ

```bash
pip install networkx>=3.1
pip install python-louvain>=0.16
```

### 📊 データ収集ライブラリ

```bash
# Web スクレイピング
pip install requests>=2.31.0
pip install beautifulsoup4>=4.12.0
pip install selenium>=4.11.0

# データベース API
pip install wrds>=3.1.0      # WRDS データ（要アカウント）
pip install fredapi>=0.5.0   # FRED データ
pip install yfinance>=0.2.28 # Yahoo Finance
```

### 📈 可視化ライブラリ

```bash
pip install matplotlib>=3.7.0
pip install seaborn>=0.12.0
pip install plotly>=5.15.0
```

---

## トラブルシューティング

### 問題 1: `linearmodels` のインストールエラー

**症状**:
```
ERROR: Could not build wheels for linearmodels
```

**解決策（macOS）**:
```bash
# Xcode Command Line Tools をインストール
xcode-select --install

# Homebrew で必要なライブラリをインストール
brew install gcc

# 再インストール
pip install linearmodels
```

**解決策（Linux）**:
```bash
# ビルドツールをインストール
sudo apt-get install build-essential
sudo apt-get install python3-dev

# 再インストール
pip install linearmodels
```

### 問題 2: `econml` のインストールエラー

**症状**:
```
ERROR: Failed building wheel for econml
```

**解決策**:
```bash
# numpy と scipy を先にインストール
pip install numpy scipy

# scikit-learn のバージョンを確認
pip install scikit-learn>=1.3.0

# econml を再インストール
pip install econml
```

### 問題 3: `wrds` ライブラリの認証エラー

**症状**:
```
Connection failed: Authentication error
```

**解決策**:
1. WRDS アカウントの作成・確認
2. `.pgpass` ファイルの設定（macOS/Linux）:

```bash
# ホームディレクトリに .pgpass を作成
echo "wrds-pgdata.wharton.upenn.edu:9737:wrds:YOUR_USERNAME:YOUR_PASSWORD" > ~/.pgpass

# パーミッション変更
chmod 600 ~/.pgpass
```

3. Windows の場合:
```
C:\Users\YourName\AppData\Roaming\postgresql\pgpass.conf
に同様の内容を記述
```

### 問題 4: spaCy モデルのダウンロードエラー

**症状**:
```
OSError: Can't find model 'en_core_web_sm'
```

**解決策**:
```bash
# 直接ダウンロード
python -m spacy download en_core_web_sm

# または URL から直接インストール
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz
```

### 問題 5: メモリ不足エラー

**症状**:
```
MemoryError: Unable to allocate array
```

**解決策**:
1. データのチャンク処理:
```python
# 大規模データは分割して処理
chunk_size = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

2. データ型の最適化:
```python
# 不要な精度を削減
df['column'] = df['column'].astype('float32')  # float64 → float32
```

3. 不要な変数の削除:
```python
import gc
del large_dataframe
gc.collect()
```

---

## 環境別の注意事項

### macOS

#### Homebrew のインストール（推奨）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 日本語テキスト処理（mecab）
```bash
brew install mecab mecab-ipadic
pip install mecab-python3
```

#### Apple Silicon (M1/M2/M3) の場合
```bash
# Rosetta 経由での実行が必要な場合がある
arch -x86_64 pip install [package]
```

### Linux (Ubuntu/Debian)

#### 必要なシステムパッケージ
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev
```

### Windows

#### Visual C++ Build Tools
一部のライブラリのビルドに必要:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### 長いパス名の問題
```powershell
# レジストリエディタで長いパス名を有効化
# または、短いディレクトリ名を使用
```

---

## 動作確認

### テストスクリプトの実行

```bash
# テストケースの実行
pytest 1-core-workflow/tests/ -v
pytest 3-statistical-methods/tests/ -v

# すべてのテストを実行
pytest . -v
```

### 個別モジュールの動作確認

```python
# panel_regression.py の確認
python -c "from linearmodels.panel import PanelOLS; print('✓ linearmodels OK')"

# econml の確認
python -c "from econml.dml import LinearDML; print('✓ econml OK')"

# networkx の確認
python -c "import networkx as nx; print('✓ networkx OK')"

# テキスト分析の確認
python -c "import nltk, spacy; print('✓ Text analysis OK')"
```

### 実行例の動作確認

```bash
# 基本ワークフローの実行
cd 1-core-workflow/examples/basic_workflow
python run_example.py

# パネル回帰の実行
cd 3-statistical-methods/examples/panel_did_example
python run_panel_did_analysis.py

# ネットワーク分析の実行
cd 5-network-analysis/examples/alliance_network_example
python analyze_alliance_networks.py
```

---

## 📞 サポート

### 問題が解決しない場合

1. **ログの確認**: エラーメッセージ全体をコピー
2. **環境情報の収集**:
```bash
python --version
pip list
uname -a  # macOS/Linux
systeminfo  # Windows
```

3. **GitHub Issues**: プロジェクトの Issue を検索・投稿
4. **ドキュメント**: 各スキルの `SKILL.md` を参照

---

## 🎓 次のステップ

インストールが完了したら：

1. **README.md** でプロジェクト構造を確認
2. **SKILL-INDEX.md** で各スキルの概要を確認
3. **examples/** ディレクトリで実行例を試す
4. 自分の研究に応用開始！

---

**最終更新日**: 2025-11-02  
**バージョン**: v4.0  
**対象 Python**: 3.9, 3.10, 3.11
