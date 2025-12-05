---
name: research-react-visualizer
description: Create interactive React-based data visualizations for academic research, including financial dashboards, market share analysis, benchmark comparisons, citation networks, and strategic framework visualizations. This skill should be used when researchers need to create publication-ready interactive visualizations from research data (CSV, databases), or when building exploratory data analysis tools for management/strategy research.
license: MIT
---

# Research React Visualizer

学術研究者向けのインタラクティブなReactベースのデータ可視化スキル。経営戦略研究、AI企業分析、組織論研究に最適化されたコンポーネント群を提供。

## Overview

このスキルは以下の目的で使用する：
- 研究データ（CSV、SQLite）からインタラクティブなダッシュボードを作成
- 学術論文用の出版品質の可視化を生成
- 比較分析ツール（企業比較、ベンチマーク比較）を構築
- 時系列分析、市場シェア推移、財務指標の可視化
- 引用ネットワーク、理論フレームワークの視覚的表現

## Quick Start

### Step 1: Initialize Project

```bash
# artifacts-builderスキルのスクリプトを使用してReactプロジェクトを初期化
bash /path/to/skills/Anthropic/artifacts-builder/scripts/init-artifact.sh research-dashboard
cd research-dashboard

# 追加の可視化ライブラリをインストール
npm install recharts d3 @tanstack/react-table
```

### Step 2: Select Visualization Type

研究目的に応じて適切なコンポーネントタイプを選択：

| 研究目的 | 推奨コンポーネント | ライブラリ |
|---------|------------------|-----------|
| 財務指標比較 | FinancialDashboard | Recharts |
| 市場シェア推移 | MarketShareEvolution | Recharts + D3 |
| AIベンチマーク | BenchmarkRadar | Recharts |
| ユーザー成長分析 | GrowthTimeSeries | TanStack Charts |
| 戦略フレームワーク | StrategyMatrix | Custom SVG |
| 引用ネットワーク | CitationNetwork | D3 Force |
| データテーブル | ResearchDataTable | TanStack Table |

### Step 3: Import Research Data

```typescript
// CSVデータをインポート
import { parseCSV } from './utils/dataParser';

// SQLiteからデータを取得（Node.js環境の場合）
import Database from 'better-sqlite3';
const db = new Database('research.db');
```

### Step 4: Bundle and Export

```bash
# 学術出版用のHTML/SVGをエクスポート
bash scripts/bundle-artifact.sh
```

## Component Catalog

詳細は `references/component-catalog.md` を参照。

### 1. Financial Dashboard（財務ダッシュボード）

AI企業の財務指標を比較・分析するためのコンポーネント。

**データ要件**:
- company: 企業名
- year/quarter: 時期
- arr, revenue, valuation, funding: 財務指標

**主要機能**:
- 複数企業のARR推移比較
- バリュエーション成長トラッキング
- 資金調達ラウンドの時系列表示

### 2. Market Share Evolution（市場シェア推移）

消費者市場、エンタープライズ市場、コーディング市場のシェア推移を可視化。

**データ要件**:
- segment: 市場セグメント（consumer, enterprise, coding）
- company: 企業名
- share_percentage: シェア率
- year: 年度

**主要機能**:
- 積み上げ棒グラフによるシェア推移
- セグメント間比較
- アニメーション付き遷移

### 3. Benchmark Radar（ベンチマーク比較）

AIモデルの多次元ベンチマーク比較。

**データ要件**:
- model_name: モデル名
- benchmark_name: ベンチマーク名（MMLU, SWE-Bench等）
- score: スコア

**主要機能**:
- レーダーチャートによる多次元比較
- ベンチマーク選択フィルター
- コスト対性能マトリックス

### 4. Strategy Matrix（戦略マトリックス）

経営戦略フレームワークの視覚的表現。

**用途**:
- 市場成熟度分類（超成熟/成熟/急成長/新興）
- 戦略パターン分析
- Exploration-Exploitation バランス
- 技術進化ステージ × 資金調達圧力マトリックス

### 5. Citation Network（引用ネットワーク）

学術論文の引用関係を可視化。

**データ要件**:
- papers: 論文リスト（id, title, year, citations）
- edges: 引用関係（source_id, target_id）

**主要機能**:
- D3 Force-directedレイアウト
- ノードサイズ = 被引用数
- クリックで論文詳細表示

## Academic Design Guidelines

### 出版品質の可視化

学術論文・プレゼンテーション用の可視化には以下のガイドラインを遵守：

1. **カラーパレット**: アクセシビリティを考慮（色覚多様性対応）
   ```typescript
   const academicPalette = {
     primary: ['#2563eb', '#dc2626', '#16a34a', '#9333ea'],
     neutral: ['#1f2937', '#4b5563', '#9ca3af'],
     background: '#ffffff'
   };
   ```

2. **フォント**: 学術的な読みやすさを優先
   ```css
   font-family: 'Noto Sans JP', 'Inter', sans-serif;
   ```

3. **軸ラベル・凡例**: 必ず日本語と英語の両方に対応
   ```typescript
   const labels = {
     revenue: { ja: '売上高', en: 'Revenue' },
     marketShare: { ja: '市場シェア', en: 'Market Share' }
   };
   ```

4. **エクスポート機能**: SVG/PNGでの出力対応
   ```typescript
   import { saveAs } from 'file-saver';

   const exportToSVG = (chartRef: RefObject<SVGElement>) => {
     const svgData = new XMLSerializer().serializeToString(chartRef.current);
     const blob = new Blob([svgData], { type: 'image/svg+xml' });
     saveAs(blob, 'chart.svg');
   };
   ```

### インタラクティブ機能

研究者が探索的データ分析を行うための機能：

- **フィルタリング**: 企業、期間、セグメントの選択
- **ドリルダウン**: 集計から個別データへの深掘り
- **ツールチップ**: 詳細情報のホバー表示
- **同期カーソル**: 複数チャート間でのカーソル同期

## Usage Examples

### Example 1: AI企業財務比較ダッシュボード

```typescript
import { FinancialDashboard } from '@/components/research';
import financialData from '@/data/financial_data.csv';

export function AICompanyFinancials() {
  return (
    <FinancialDashboard
      data={financialData}
      companies={['OpenAI', 'Anthropic', 'Google']}
      metrics={['arr', 'valuation', 'funding']}
      dateRange={['2023-01', '2025-12']}
      locale="ja"
    />
  );
}
```

### Example 2: 市場シェア推移アニメーション

```typescript
import { MarketShareEvolution } from '@/components/research';
import marketData from '@/data/market_share_data.csv';

export function MarketShareAnalysis() {
  return (
    <MarketShareEvolution
      data={marketData}
      segment="enterprise"
      animationDuration={1000}
      showYearComparison={true}
    />
  );
}
```

### Example 3: 戦略フレームワーク可視化

```typescript
import { StrategyMatrix } from '@/components/research';

const marketMaturityData = [
  { market: 'Japan', maturity: 'super-mature', strategy: 'differentiation' },
  { market: 'India', maturity: 'emerging', strategy: 'market-penetration' },
  // ...
];

export function StrategyFramework() {
  return (
    <StrategyMatrix
      data={marketMaturityData}
      xAxis="maturity"
      yAxis="strategy"
      bubbleSize="revenue"
      labels={{ ja: true, en: true }}
    />
  );
}
```

## Data Integration

### CSVデータの読み込み

```typescript
// Viteを使用したCSVインポート
import financialData from './data/financial_data.csv?raw';
import Papa from 'papaparse';

const parsed = Papa.parse(financialData, {
  header: true,
  dynamicTyping: true
});
```

### SQLiteデータの利用（Node.js環境）

```typescript
import Database from 'better-sqlite3';

const db = new Database('./databases/corporate_research.db');
const companies = db.prepare(`
  SELECT * FROM companies
  WHERE industry = 'AI'
`).all();
```

## Export Options

### 1. 学術論文用SVG

```typescript
const exportForPublication = () => {
  // 高解像度SVGをエクスポート
  exportToSVG(chartRef, {
    width: 1200,
    height: 800,
    fontEmbed: true
  });
};
```

### 2. インタラクティブHTML

```bash
# bundle-artifact.shを使用して単一HTMLにバンドル
bash scripts/bundle-artifact.sh
# → bundle.html が生成される
```

### 3. プレゼンテーション用PNG

```typescript
import html2canvas from 'html2canvas';

const exportToPNG = async (element: HTMLElement) => {
  const canvas = await html2canvas(element, { scale: 2 });
  canvas.toBlob(blob => saveAs(blob, 'chart.png'));
};
```

## Best Practices for Researchers

### データの品質確保

1. **欠損値の処理**: 可視化前にデータクリーニング
2. **外れ値の表示**: 研究では外れ値も重要な情報
3. **データソースの明記**: 凡例にデータ出典を含める

### 再現性の確保

1. **シード値の固定**: アニメーションやランダム配置で使用
2. **設定のエクスポート**: フィルター設定をJSON保存
3. **バージョン管理**: コンポーネントのバージョンを記録

### 日本語対応

1. **フォント**: Noto Sans JPを優先使用
2. **ラベル**: 日英両方のラベルを用意
3. **数値フォーマット**: 日本式（3桁カンマ）と英語式に対応

## Reference Files

- `references/component-catalog.md` - 全コンポーネントの詳細仕様
- `references/chart-patterns.md` - 研究用途別チャートパターン
- `references/color-accessibility.md` - アクセシブルなカラーパレット
- `templates/dashboard-template/` - ダッシュボードのベーステンプレート
