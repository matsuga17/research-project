# サンプルプロジェクト: アジア製造業のROA分析

## プロジェクト概要

**研究テーマ**: 日本・韓国・台湾の製造業企業の収益性（ROA）比較分析

**使用データソース**: 完全無料
- 日本: EDINET、JPX
- 韓国: Open DART API
- 台湾: TWSE/MOPS
- マクロデータ: World Bank

**予算**: ¥0

**必要な準備**:
1. APIキー取得（無料）
   - Open DART (韓国): https://opendart.fss.or.kr/
   - World Bank API: 登録不要

## ディレクトリ構造

```
asian_manufacturing_roa/
├── data/
│   ├── raw/                    # 生データ
│   │   ├── japan/
│   │   ├── korea/
│   │   └── taiwan/
│   ├── processed/              # 処理済みデータ
│   └── final/                  # 分析用データセット
├── scripts/
│   ├── 01_collect_japan.py
│   ├── 02_collect_korea.py
│   ├── 03_collect_taiwan.py
│   ├── 04_clean_and_merge.py
│   └── 05_analysis.py
├── output/
│   ├── tables/
│   ├── figures/
│   └── reports/
├── config.py                   # 設定ファイル
├── requirements.txt            # Pythonパッケージ
└── README.md
```

## ステップ1: 環境構築

### 1.1 必要なパッケージのインストール

```bash
# requirements.txt の内容
pandas>=1.3.0
numpy>=1.20.0
requests>=2.26.0
openpyxl>=3.0.0
scipy>=1.7.0
statsmodels>=0.13.0
matplotlib>=3.4.0
seaborn>=0.11.0

# オプション（中国データ用）
tushare>=1.2.0
akshare>=1.7.0

# インストール
pip install -r requirements.txt
```

### 1.2 APIキーの設定

`config.py` を作成:

```python
# config.py
# APIキー（取得後に記入）
DART_API_KEY = "your_dart_api_key_here"  # Open DART（韓国）
TUSHARE_TOKEN = ""  # Tushare（中国、オプション）
FRED_API_KEY = ""   # FRED（為替レート、オプション）

# データパス
RAW_DATA_PATH = "./data/raw"
PROCESSED_DATA_PATH = "./data/processed"
FINAL_DATA_PATH = "./data/final"

# サンプル期間
START_YEAR = 2018
END_YEAR = 2023

# 対象業種（ISIC Rev.4）
TARGET_INDUSTRIES = [
    "C10-C12",  # 食品・飲料・タバコ
    "C13-C15",  # 繊維・衣類
    "C16-C18",  # 木材・紙・印刷
    "C19-C23",  # 化学・ゴム・プラスチック
    "C24-C25",  # 金属製品
    "C26-C28",  # 機械・電気機器
    "C29-C30"   # 輸送機器
]
```

## ステップ2: データ収集

### 2.1 日本データ収集

`scripts/01_collect_japan.py`:

```python
import sys
sys.path.append('..')
from asian_data_collectors import JapanDataCollector
import pandas as pd
from datetime import datetime, timedelta
import config

def collect_japan_data():
    """日本製造業データ収集"""
    
    collector = JapanDataCollector()
    
    # 1. 過去の有価証券報告書リスト取得
    all_documents = []
    
    start_date = datetime(config.START_YEAR, 4, 1)
    end_date = datetime(config.END_YEAR, 12, 31)
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"取得中: {date_str}")
        
        docs = collector.get_edinet_documents(date_str)
        if not docs.empty:
            all_documents.append(docs)
        
        current_date += timedelta(days=1)
    
    # 2. 全書類を結合
    if all_documents:
        df_all = pd.concat(all_documents, ignore_index=True)
        
        # 製造業のみフィルタリング（SICコード2000-3999）
        # ※実際にはEDINETのデータ構造に応じて調整
        df_manufacturing = df_all[df_all['docDescription'].str.contains('有価証券報告書')]
        
        # 保存
        df_manufacturing.to_csv(
            f"{config.RAW_DATA_PATH}/japan/edinet_documents.csv",
            index=False,
            encoding='utf-8-sig'
        )
        
        print(f"保存完了: {len(df_manufacturing)} 件")
        return df_manufacturing
    else:
        print("データ取得失敗")
        return pd.DataFrame()

if __name__ == "__main__":
    collect_japan_data()
```

### 2.2 韓国データ収集

`scripts/02_collect_korea.py`:

```python
import sys
sys.path.append('..')
from asian_data_collectors import KoreaDataCollector
import pandas as pd
import config
import time

def collect_korea_data():
    """韓国製造業データ収集"""
    
    collector = KoreaDataCollector(config.DART_API_KEY)
    
    # 1. 製造業企業リストの読み込み（事前に準備）
    # ※または DART APIで全企業リスト取得
    companies = pd.read_csv(f"{config.RAW_DATA_PATH}/korea/company_list.csv")
    manufacturing = companies[companies['industry'].str.contains('제조업')]
    
    all_financials = []
    
    # 2. 各企業の財務データ取得
    for idx, company in manufacturing.iterrows():
        corp_code = company['corp_code']
        
        print(f"\n進捗: {idx+1}/{len(manufacturing)} - {company['corp_name']}")
        
        for year in range(config.START_YEAR, config.END_YEAR + 1):
            df = collector.get_financial_statements(
                corp_code=corp_code,
                bsns_year=str(year),
                reprt_code='11011'
            )
            
            if not df.empty:
                df['corp_code'] = corp_code
                df['corp_name'] = company['corp_name']
                df['year'] = year
                all_financials.append(df)
            
            time.sleep(1)  # API制限対策
    
    # 3. 保存
    if all_financials:
        df_all = pd.concat(all_financials, ignore_index=True)
        df_all.to_csv(
            f"{config.RAW_DATA_PATH}/korea/financial_statements.csv",
            index=False,
            encoding='utf-8-sig'
        )
        print(f"\n保存完了: {len(df_all)} レコード")
        return df_all
    else:
        print("データ取得失敗")
        return pd.DataFrame()

if __name__ == "__main__":
    collect_korea_data()
```

### 2.3 台湾データ収集

`scripts/03_collect_taiwan.py`:

```python
import sys
sys.path.append('..')
from asian_data_collectors import TaiwanDataCollector
import pandas as pd
from datetime import datetime, timedelta
import config
import time

def collect_taiwan_data():
    """台湾製造業データ収集"""
    
    collector = TaiwanDataCollector()
    
    # 1. 上場企業リスト取得
    companies = collector.get_listed_companies()
    
    if companies.empty:
        print("企業リスト取得失敗")
        return pd.DataFrame()
    
    # 製造業のみフィルタリング（産業分類コードで）
    # ※実際のデータ構造に応じて調整
    manufacturing = companies[companies['產業別'] == '製造業']
    
    # 2. 株価データ取得（サンプル期間）
    all_prices = []
    
    start_date = datetime(config.START_YEAR, 1, 1)
    end_date = datetime(config.END_YEAR, 12, 31)
    current_date = start_date
    
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        print(f"取得中: {date_str}")
        
        df = collector.get_stock_daily(date_str)
        if not df.empty:
            all_prices.append(df)
        
        time.sleep(5)  # TWSE API制限対策
        current_date += timedelta(days=7)  # 週次サンプリング
    
    # 3. 保存
    if all_prices:
        df_all = pd.concat(all_prices, ignore_index=True)
        df_all.to_csv(
            f"{config.RAW_DATA_PATH}/taiwan/stock_prices.csv",
            index=False,
            encoding='utf-8-sig'
        )
        print(f"保存完了: {len(df_all)} レコード")
        return df_all
    else:
        print("データ取得失敗")
        return pd.DataFrame()

if __name__ == "__main__":
    collect_taiwan_data()
```

## ステップ3: データクリーニングと統合

`scripts/04_clean_and_merge.py`:

```python
import pandas as pd
import numpy as np
import config

def clean_japan_data():
    """日本データのクリーニング"""
    
    # ※実際にはXBRLからの財務データ抽出が必要
    # ここではサンプル構造
    df = pd.read_csv(f"{config.RAW_DATA_PATH}/japan/financial_data.csv")
    
    # 1. 必要な変数を抽出
    df_clean = df[['company_code', 'company_name', 'year', 
                   'total_assets', 'net_income', 'sales', 'industry_code']].copy()
    
    # 2. ROA計算
    df_clean['roa'] = df_clean['net_income'] / df_clean['total_assets']
    
    # 3. 異常値処理
    df_clean = df_clean[df_clean['roa'].between(-1, 1)]
    
    # 4. 国識別子追加
    df_clean['country'] = 'Japan'
    
    return df_clean


def clean_korea_data():
    """韓国データのクリーニング"""
    
    df = pd.read_csv(f"{config.RAW_DATA_PATH}/korea/financial_statements.csv")
    
    # 1. 財務諸表から必要項目を抽出
    # ※DART APIの構造に応じて調整
    
    # 資産総額
    assets = df[df['account_nm'].str.contains('자산총계')].copy()
    assets = assets[['corp_code', 'year', 'thstrm_amount']].rename(
        columns={'thstrm_amount': 'total_assets'}
    )
    
    # 当期純利益
    income = df[df['account_nm'].str.contains('당기순이익')].copy()
    income = income[['corp_code', 'year', 'thstrm_amount']].rename(
        columns={'thstrm_amount': 'net_income'}
    )
    
    # 2. マージ
    df_clean = assets.merge(income, on=['corp_code', 'year'])
    
    # 3. ROA計算
    df_clean['roa'] = df_clean['net_income'] / df_clean['total_assets']
    
    # 4. 国識別子追加
    df_clean['country'] = 'Korea'
    
    return df_clean


def clean_taiwan_data():
    """台湾データのクリーニング"""
    
    # ※MOPSから財務データを取得する必要あり
    # ここではサンプル構造
    df = pd.read_csv(f"{config.RAW_DATA_PATH}/taiwan/financial_data.csv")
    
    df_clean = df[['company_code', 'company_name', 'year',
                   'total_assets', 'net_income']].copy()
    
    df_clean['roa'] = df_clean['net_income'] / df_clean['total_assets']
    df_clean['country'] = 'Taiwan'
    
    return df_clean


def merge_all_countries():
    """全データの統合"""
    
    # 1. 各国データのクリーニング
    df_japan = clean_japan_data()
    df_korea = clean_korea_data()
    df_taiwan = clean_taiwan_data()
    
    # 2. 統一フォーマットに変換
    common_columns = ['company_code', 'company_name', 'year', 'country',
                     'total_assets', 'net_income', 'roa']
    
    df_japan = df_japan[common_columns]
    df_korea = df_korea[common_columns]
    df_taiwan = df_taiwan[common_columns]
    
    # 3. 結合
    df_combined = pd.concat([df_japan, df_korea, df_taiwan], ignore_index=True)
    
    # 4. 最終クリーニング
    # 欠損値除去
    df_combined = df_combined.dropna(subset=['roa', 'total_assets'])
    
    # ウィンソライズ（1%/99%）
    from scipy.stats.mstats import winsorize
    df_combined['roa'] = winsorize(df_combined['roa'], limits=[0.01, 0.01])
    
    # 5. 保存
    df_combined.to_csv(
        f"{config.FINAL_DATA_PATH}/asian_manufacturing_panel.csv",
        index=False,
        encoding='utf-8-sig'
    )
    
    print(f"最終データセット保存完了:")
    print(f"  - 総レコード数: {len(df_combined):,}")
    print(f"  - 企業数: {df_combined['company_code'].nunique()}")
    print(f"  - 国別分布:")
    print(df_combined['country'].value_counts())
    
    return df_combined


if __name__ == "__main__":
    df_final = merge_all_countries()
```

## ステップ4: 分析

`scripts/05_analysis.py`:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import config

# 日本語フォント設定（必要に応じて）
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def descriptive_statistics():
    """記述統計"""
    
    df = pd.read_csv(f"{config.FINAL_DATA_PATH}/asian_manufacturing_panel.csv")
    
    # 1. 国別記述統計
    print("=" * 70)
    print("国別記述統計量")
    print("=" * 70)
    
    for country in ['Japan', 'Korea', 'Taiwan']:
        df_country = df[df['country'] == country]
        print(f"\n{country}:")
        print(df_country['roa'].describe())
    
    # 2. 年次推移
    yearly = df.groupby(['country', 'year'])['roa'].mean().reset_index()
    
    plt.figure(figsize=(10, 6))
    for country in ['Japan', 'Korea', 'Taiwan']:
        data = yearly[yearly['country'] == country]
        plt.plot(data['year'], data['roa'], marker='o', label=country)
    
    plt.xlabel('Year')
    plt.ylabel('Average ROA')
    plt.title('ROA Trends: Japan, Korea, Taiwan Manufacturing')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{config.OUTPUT_PATH}/figures/roa_trends.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n図を保存しました: roa_trends.png")


def country_comparison():
    """国間比較分析"""
    
    df = pd.read_csv(f"{config.FINAL_DATA_PATH}/asian_manufacturing_panel.csv")
    
    # 1. ANOVA
    japan = df[df['country'] == 'Japan']['roa'].dropna()
    korea = df[df['country'] == 'Korea']['roa'].dropna()
    taiwan = df[df['country'] == 'Taiwan']['roa'].dropna()
    
    f_stat, p_value = stats.f_oneway(japan, korea, taiwan)
    
    print("\n" + "=" * 70)
    print("ANOVA: 国別ROA比較")
    print("=" * 70)
    print(f"F-statistic: {f_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("結論: 国間で有意な差がある (p < 0.05)")
    else:
        print("結論: 国間で有意な差がない (p >= 0.05)")
    
    # 2. Post-hoc 検定（Tukey's HSD）
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    
    tukey = pairwise_tukeyhsd(df['roa'], df['country'], alpha=0.05)
    print("\nTukey's HSD Post-hoc Test:")
    print(tukey)


def panel_regression():
    """パネル回帰分析"""
    
    df = pd.read_csv(f"{config.FINAL_DATA_PATH}/asian_manufacturing_panel.csv")
    
    # 1. ダミー変数作成
    df = pd.get_dummies(df, columns=['country', 'year'], drop_first=True)
    
    # 2. 説明変数と被説明変数
    y = df['roa']
    X = df[[col for col in df.columns if col.startswith('country_') or col.startswith('year_')]]
    X = sm.add_constant(X)
    
    # 3. OLS回帰
    model = sm.OLS(y, X).fit()
    
    print("\n" + "=" * 70)
    print("パネル回帰分析結果")
    print("=" * 70)
    print(model.summary())
    
    # 4. 結果保存
    with open(f"{config.OUTPUT_PATH}/reports/regression_results.txt", 'w', encoding='utf-8') as f:
        f.write(model.summary().as_text())


if __name__ == "__main__":
    descriptive_statistics()
    country_comparison()
    panel_regression()
    
    print("\n" + "=" * 70)
    print("分析完了！")
    print("結果は output/ フォルダに保存されました。")
    print("=" * 70)
```

## ステップ5: 実行

```bash
# 1. データ収集
python scripts/01_collect_japan.py
python scripts/02_collect_korea.py
python scripts/03_collect_taiwan.py

# 2. データクリーニングと統合
python scripts/04_clean_and_merge.py

# 3. 分析
python scripts/05_analysis.py
```

## 期待される成果物

### 1. データセット
- `data/final/asian_manufacturing_panel.csv`
  - 日韓台製造業企業のパネルデータ
  - 2018-2023年、年次データ
  - 主要変数: ROA、総資産、純利益

### 2. 分析結果
- `output/figures/roa_trends.png`: ROA時系列グラフ
- `output/reports/regression_results.txt`: 回帰分析結果
- `output/tables/descriptive_stats.xlsx`: 記述統計表

### 3. 論文への応用
このデータセットは以下のような研究に使用可能:
- 「東アジア製造業の収益性決定要因」
- 「企業パフォーマンスの国際比較」
- 「制度的環境と企業効率性」

## トラブルシューティング

### Q1: API制限エラーが出る
**A**: スクリプト内の`time.sleep()`の秒数を増やしてください。

### Q2: 韓国語/中国語のエンコードエラー
**A**: 
```python
df.to_csv('file.csv', encoding='utf-8-sig')
```
を使用してください。

### Q3: XBRLファイルの解析方法がわからない
**A**: Python の `arelle` ライブラリを使用:
```bash
pip install arelle
```

## 推定所要時間

- 環境構築: 1時間
- データ収集: 2-3日（API制限による）
- データクリーニング: 1-2日
- 分析: 1日
- **合計**: 約1週間

## 推定費用

**¥0**（完全無料）

ただし、必要なもの:
- インターネット接続
- Python実行環境
- 時間と労力

## さらなる拡張

1. **追加国**: シンガポール、マレーシア、タイを追加
2. **追加変数**: レバレッジ、R&D強度、輸出比率
3. **業種分析**: 業種別の詳細分析
4. **時系列分析**: ARIMAモデルによる予測

---

**このサンプルプロジェクトが、低予算での実証研究の一助となれば幸いです！**

#サンプルプロジェクト #無料データ #アジア製造業 #ROA分析