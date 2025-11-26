# クイックスタートガイド

このガイドでは、strategic-organizational-research-hubスキルを使って、**15分で最初のデータセットを収集**する方法を説明します。

---

## 目標

日本の製造業上場企業10社の2023年度財務データを収集し、ROA（総資産利益率）を計算する。

**所要時間**: 15分  
**予算**: $0

---

## 必要な準備

### ソフトウェア
- **Python 3.8以上**（[インストール](https://www.python.org/downloads/)）
- **必要なパッケージ**:
  ```bash
  pip install requests pandas openpyxl
  ```

### データソース
- **EDINET**（日本の開示書類システム）：無料、登録不要

---

## ステップ1: EDINETから企業リストを取得（5分）

### 1.1 EDINET APIの基本

EDINETは日本の金融庁が提供する企業開示情報システムです。APIを使って無料でデータ取得できます。

**APIドキュメント**: https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/WZEK0110.html

### 1.2 Pythonスクリプト作成

以下のスクリプトを `step1_get_company_list.py` として保存：

```python
import requests
import pandas as pd
from datetime import datetime

# EDINET API endpoint
base_url = "https://disclosure2.edinet-fsa.go.jp/api/v2"

# 書類一覧取得（2023年度有価証券報告書）
def get_yuho_list(date):
    """
    指定日に提出された有価証券報告書のリストを取得
    """
    url = f"{base_url}/documents.json"
    params = {
        "date": date,  # YYYY-MM-DD形式
        "type": 2      # 2 = 有価証券報告書
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    else:
        print(f"Error: {response.status_code}")
        return []

# 2024年6月（多くの3月決算企業が提出）
date = "2024-06-28"
documents = get_yuho_list(date)

# 製造業（SIC 20-39）のみフィルタ（簡易版：手動リスト）
sample_companies = [
    {"name": "トヨタ自動車", "edinet_code": "E02144"},
    {"name": "ソニーグループ", "edinet_code": "E02683"},
    {"name": "パナソニック", "edinet_code": "E01739"},
    {"name": "日立製作所", "edinet_code": "E01588"},
    {"name": "三菱電機", "edinet_code": "E01759"},
    {"name": "キーエンス", "edinet_code": "E02331"},
    {"name": "ファナック", "edinet_code": "E01506"},
    {"name": "ダイキン工業", "edinet_code": "E01570"},
    {"name": "オムロン", "edinet_code": "E01753"},
    {"name": "村田製作所", "edinet_code": "E01605"}
]

df = pd.DataFrame(sample_companies)
print("企業リスト:")
print(df)

# CSVに保存
df.to_csv("company_list.csv", index=False, encoding="utf-8-sig")
print("\n✅ company_list.csv に保存しました")
```

**実行**:
```bash
python step1_get_company_list.py
```

**出力**: `company_list.csv`（企業リスト）

---

## ステップ2: 財務データを取得（5分）

### 2.1 EDINETから有価証券報告書の財務データを取得

**注意**: 実際のEDINET APIからXBRL形式の財務データを解析するのは複雑です。ここでは簡略化した例を示します。

**実務的アプローチ**:
1. 各企業のIRサイトから決算短信PDFをダウンロード
2. 手動でExcelに入力（10社なら30分程度）
3. または、既存のデータベース（NEEDS、SPEEDAの無料トライアル）を活用

### 2.2 サンプルデータを作成（学習用）

`step2_sample_data.py`:

```python
import pandas as pd

# サンプル財務データ（2023年度、単位：百万円）
data = {
    "company_name": [
        "トヨタ自動車", "ソニーグループ", "パナソニック", 
        "日立製作所", "三菱電機", "キーエンス", 
        "ファナック", "ダイキン工業", "オムロン", "村田製作所"
    ],
    "total_assets": [76588536, 27789469, 9343574, 12825826, 5142700, 
                     2063845, 1356273, 4196574, 934126, 2589437],
    "net_income": [4944672, 970599, 179422, 650729, 268600, 
                   421445, 126581, 311547, 50229, 185694],
    "sales": [45095346, 13005600, 7388896, 10266484, 4995700, 
              816885, 678757, 3838271, 742326, 1992653],
    "rd_expense": [1431230, 654000, 387000, 456000, 198000, 
                   15800, 34000, 79000, 42000, 128000],
    "employees": [394351, 109700, 233128, 322525, 146518, 
                  10423, 8256, 90749, 28006, 78990]
}

df = pd.DataFrame(data)

# 変数を計算
df['roa'] = (df['net_income'] / df['total_assets']) * 100  # %
df['rd_intensity'] = (df['rd_expense'] / df['sales']) * 100  # %
df['log_assets'] = pd.np.log(df['total_assets'])

print("財務データ:")
print(df[['company_name', 'roa', 'rd_intensity', 'log_assets']])

# 保存
df.to_csv("financial_data.csv", index=False, encoding="utf-8-sig")
print("\n✅ financial_data.csv に保存しました")
```

**実行**:
```bash
python step2_sample_data.py
```

**出力**: `financial_data.csv`（財務データ + 計算済み変数）

---

## ステップ3: データ分析（5分）

### 3.1 記述統計

`step3_analysis.py`:

```python
import pandas as pd
import matplotlib.pyplot as plt

# データ読み込み
df = pd.read_csv("financial_data.csv")

# 記述統計
print("=== 記述統計 ===")
print(df[['roa', 'rd_intensity', 'log_assets']].describe())

# 相関行列
print("\n=== 相関行列 ===")
print(df[['roa', 'rd_intensity', 'log_assets']].corr())

# 可視化
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# ROAの分布
axes[0].hist(df['roa'], bins=10, edgecolor='black')
axes[0].set_title('Distribution of ROA')
axes[0].set_xlabel('ROA (%)')
axes[0].set_ylabel('Frequency')

# R&D集約度 vs ROA
axes[1].scatter(df['rd_intensity'], df['roa'])
axes[1].set_title('R&D Intensity vs ROA')
axes[1].set_xlabel('R&D Intensity (%)')
axes[1].set_ylabel('ROA (%)')

# 企業名をラベル表示
for i, txt in enumerate(df['company_name']):
    axes[1].annotate(txt, (df['rd_intensity'][i], df['roa'][i]), 
                     fontsize=8, ha='right')

plt.tight_layout()
plt.savefig('analysis_results.png', dpi=300)
print("\n✅ analysis_results.png に保存しました")
plt.show()
```

**実行**:
```bash
python step3_analysis.py
```

**出力**:
- 記述統計（ターミナル出力）
- 相関行列（ターミナル出力）
- `analysis_results.png`（グラフ）

---

## 次のステップ

おめでとうございます！15分で最初のデータセット収集と分析が完了しました🎉

### より本格的な研究へ

1. **サンプルサイズを拡大**:
   - 10社 → 100社 → 500社
   - EDINETから自動収集（XBRL解析）
   - スクリプト: `scripts/edinet_collector.py` 参照

2. **時系列データ収集**:
   - 1年 → 5年 → 10年
   - パネルデータ構築
   - 固定効果モデルで分析

3. **追加変数の収集**:
   - **特許データ**: USPTO PatentsView
   - **ガバナンスデータ**: EDINETの有価証券報告書（役員の状況）
   - **ESGデータ**: 企業のサステナビリティ報告書

4. **高度な分析手法**:
   - パネルデータ回帰（固定効果、変量効果）
   - 操作変数法（内生性対応）
   - イベントスタディ

---

## トラブルシューティング

### Q1: EDINET APIがエラーを返す
**A**: 
- 日付形式を確認（YYYY-MM-DD）
- 土日祝日は書類提出なし → 平日の日付を使用
- API制限: 1秒に1リクエスト程度に抑える

### Q2: Pythonパッケージがインストールできない
**A**:
```bash
# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# パッケージインストール
pip install --upgrade pip
pip install requests pandas openpyxl matplotlib
```

### Q3: データが欠損している
**A**:
- 企業によってはR&D費用を開示していない → 0として扱うか、除外
- 欠損値処理: `df.fillna(0)` または `df.dropna()`

---

## リソース

### ドキュメント
- [SKILL.md](SKILL.md) - 完全なスキルドキュメント
- [FREE_DATA_SOURCES.md](FREE_DATA_SOURCES.md) - 無料データソース完全ガイド

### スクリプト
- `scripts/data_collection_template.py` - データ収集テンプレート
- `scripts/panel_data_analysis.py` - パネルデータ分析

### 実例
- `examples/example_japan_rnd_performance.md` - 日本企業R&D研究の完全例

---

## 次の学習ステップ

1. **Week 1**: 100社×5年のパネルデータ収集
2. **Week 2**: データクリーニングと記述統計
3. **Week 3**: 回帰分析（OLS、固定効果）
4. **Week 4**: 論文執筆（IMRaD形式）

**目標**: 3ヶ月で最初の研究論文を完成させる！

---

**質問・サポート**:
- GitHub Issues
- Email: [メールアドレス]

頑張ってください！🚀