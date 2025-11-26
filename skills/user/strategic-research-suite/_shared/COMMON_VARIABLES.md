# Common Variable Definitions

戦略研究で頻繁に使用される変数の標準的な定義と構築方法

---

## 企業パフォーマンス指標

### 会計ベース指標

**ROA (Return on Assets)**
```
ROA = 純利益 / 総資産
```

**ROE (Return on Equity)**  
```
ROE = 純利益 / 株主資本
```

**ROS (Return on Sales)**
```
ROS = 営業利益 / 売上高
```

### 市場ベース指標

**Tobin's Q**
```
Tobin's Q = (時価総額 + 負債の簿価) / 総資産の簿価
```

---

## イノベーション指標

**R&D Intensity**
```
R&D Intensity = R&D支出 / 売上高
```

**Patent Stock**
```
Patent_Stock_t = Σ(i=0 to 4) Patent_i,t-i × (1 - 0.15)^i
```

---

## 組織特性

**Firm Size**
```
ln(Total_Assets)
ln(Sales)
ln(Employees)
```

**Firm Age**
```
Age = Current_Year - Foundation_Year
ln(1 + Age)
```

**Leverage**
```
Leverage = Total_Debt / Total_Assets
```

---

## 競争環境

**Industry Concentration (HHI)**
```
HHI = Σ (Market_Share_i)^2 × 10,000
```

**Industry Growth**
```
Growth = (Sales_t - Sales_t-1) / Sales_t-1
```

---

## 統制変数の標準セット

### 企業レベル
- Firm Size (ln_assets)
- Firm Age (ln_age)  
- Leverage
- ROA (lagged)

### 産業・時間
- Industry HHI
- Industry Growth
- Year Fixed Effects
- Industry Fixed Effects

---

**参照元**: Strategic Research Suite v4.0
