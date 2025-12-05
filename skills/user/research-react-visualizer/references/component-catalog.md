# Component Catalog - 研究用Reactコンポーネント詳細仕様

このドキュメントは、research-react-visualizerスキルで提供される全コンポーネントの詳細仕様を記載。

## Table of Contents

1. [FinancialDashboard](#1-financialdashboard)
2. [MarketShareEvolution](#2-marketshareevolution)
3. [BenchmarkRadar](#3-benchmarkradar)
4. [GrowthTimeSeries](#4-growthtimeseries)
5. [StrategyMatrix](#5-strategymatrix)
6. [CitationNetwork](#6-citationnetwork)
7. [ResearchDataTable](#7-researchdatatable)
8. [ComparativeAnalysis](#8-comparativeanalysis)
9. [TheoreticalFramework](#9-theoreticalframework)
10. [TimelineVisualization](#10-timelinevisualization)

---

## 1. FinancialDashboard

AI企業の財務指標を包括的に可視化するダッシュボードコンポーネント。

### Props

```typescript
interface FinancialDashboardProps {
  data: FinancialDataPoint[];
  companies: string[];
  metrics: ('arr' | 'revenue' | 'valuation' | 'funding' | 'losses')[];
  dateRange: [string, string]; // ISO date format
  locale: 'ja' | 'en';
  currency: 'USD' | 'JPY';
  onDataPointClick?: (point: FinancialDataPoint) => void;
  showTrendLines?: boolean;
  showYoYGrowth?: boolean;
}

interface FinancialDataPoint {
  company: string;
  date: string;
  metric: string;
  value: number;
  source?: string;
}
```

### Usage

```tsx
import { FinancialDashboard } from '@/components/research';

<FinancialDashboard
  data={financialData}
  companies={['OpenAI', 'Anthropic', 'Google DeepMind']}
  metrics={['arr', 'valuation']}
  dateRange={['2023-01', '2025-12']}
  locale="ja"
  currency="USD"
  showTrendLines={true}
  showYoYGrowth={true}
/>
```

### Chart Types Included

1. **ARR推移ラインチャート**: 複数企業のARR成長を比較
2. **バリュエーションバーチャート**: 資金調達ラウンド別のバリュエーション
3. **収益成長率ヒートマップ**: 四半期ごとの成長率を色で表現
4. **KPIカード**: 主要指標のサマリー表示

### Data Format (CSV)

```csv
company,date,arr,revenue,valuation,funding,losses,source
OpenAI,2024-01,2000000000,1600000000,86000000000,6600000000,5000000000,TechCrunch 2024
Anthropic,2024-01,875000000,700000000,18000000000,4000000000,,Forbes 2024
```

---

## 2. MarketShareEvolution

市場シェアの時系列推移を可視化。アニメーション付き遷移で変化を強調。

### Props

```typescript
interface MarketShareEvolutionProps {
  data: MarketShareDataPoint[];
  segment: 'consumer' | 'enterprise' | 'coding' | 'all';
  companies?: string[]; // フィルタリング用
  yearRange: [number, number];
  chartType: 'stacked-bar' | 'area' | 'treemap' | 'sankey';
  animationDuration?: number;
  showYearComparison?: boolean;
  showPercentageLabels?: boolean;
  locale: 'ja' | 'en';
}

interface MarketShareDataPoint {
  company: string;
  segment: string;
  year: number;
  share_percentage: number;
  absolute_value?: number;
}
```

### Usage

```tsx
import { MarketShareEvolution } from '@/components/research';

<MarketShareEvolution
  data={marketData}
  segment="enterprise"
  chartType="stacked-bar"
  yearRange={[2023, 2025]}
  animationDuration={1000}
  showYearComparison={true}
  locale="ja"
/>
```

### Visualization Options

1. **積み上げ棒グラフ (stacked-bar)**: 年別の市場シェア構成
2. **エリアチャート (area)**: 流動的なシェア推移
3. **ツリーマップ (treemap)**: 階層的なシェア表現
4. **サンキーダイアグラム (sankey)**: シェア移動の流れを可視化

### Data Format (CSV)

```csv
company,segment,year,share_percentage,source
OpenAI,consumer,2023,52.0,Statista
OpenAI,consumer,2025,59.5,Statista
Anthropic,enterprise,2024,32.0,Enterprise Survey
```

---

## 3. BenchmarkRadar

AIモデルの多次元ベンチマーク比較用レーダーチャート。

### Props

```typescript
interface BenchmarkRadarProps {
  data: BenchmarkDataPoint[];
  models: string[];
  benchmarks: string[];
  normalizeScores?: boolean; // 0-100スケールに正規化
  showRawValues?: boolean;
  colorScheme?: 'academic' | 'vibrant' | 'monochrome';
  size?: number;
  locale: 'ja' | 'en';
}

interface BenchmarkDataPoint {
  model_name: string;
  benchmark_name: string;
  score: number;
  max_score?: number;
  date?: string;
}
```

### Usage

```tsx
import { BenchmarkRadar } from '@/components/research';

<BenchmarkRadar
  data={benchmarkData}
  models={['GPT-4o', 'Claude 3.5 Sonnet', 'Gemini Pro']}
  benchmarks={['MMLU', 'SWE-Bench', 'GSM8K', 'HumanEval']}
  normalizeScores={true}
  colorScheme="academic"
  locale="ja"
/>
```

### Supported Benchmarks

| ベンチマーク名 | 説明 | 日本語ラベル |
|--------------|------|------------|
| MMLU | 大規模多領域言語理解 | 多領域言語理解 |
| SWE-Bench | ソフトウェアエンジニアリング | コード生成能力 |
| GSM8K | 数学的推論 | 数学推論 |
| HumanEval | コード生成 | コード評価 |
| GPQA | 大学院レベル質問応答 | 専門家QA |
| hallucination_rate | ハルシネーション率 | 虚偽生成率 |

### Data Format (CSV)

```csv
model_name,benchmark_name,score,max_score,date
GPT-4o,MMLU,87.2,100,2024-05
Claude 3.5 Sonnet,MMLU,88.7,100,2024-06
Claude 3.5 Sonnet,SWE-Bench,49.0,100,2024-06
```

---

## 4. GrowthTimeSeries

ユーザー成長、トラフィック、アクティブユーザー数の時系列分析。

### Props

```typescript
interface GrowthTimeSeriesProps {
  data: GrowthDataPoint[];
  companies: string[];
  metric: 'mau' | 'dau' | 'wau' | 'revenue' | 'downloads';
  dateRange: [string, string];
  granularity: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  showGrowthRate?: boolean;
  showMovingAverage?: boolean;
  movingAverageWindow?: number;
  synchronizedCursor?: boolean;
  locale: 'ja' | 'en';
}

interface GrowthDataPoint {
  company: string;
  date: string;
  metric: string;
  value: number;
  growth_rate?: number;
}
```

### Usage

```tsx
import { GrowthTimeSeries } from '@/components/research';

<GrowthTimeSeries
  data={userStatsData}
  companies={['ChatGPT', 'Claude', 'Gemini']}
  metric="mau"
  dateRange={['2023-01', '2025-06']}
  granularity="monthly"
  showGrowthRate={true}
  synchronizedCursor={true}
  locale="ja"
/>
```

### Features

1. **同期カーソル**: 複数チャート間でホバー位置を同期
2. **成長率オーバーレイ**: 前期比成長率を第2軸で表示
3. **移動平均線**: ノイズを除去したトレンド表示
4. **アノテーション**: 重要イベント（製品リリース等）をマーク

---

## 5. StrategyMatrix

経営戦略フレームワークの2次元/多次元マトリックス可視化。

### Props

```typescript
interface StrategyMatrixProps {
  data: StrategyDataPoint[];
  xAxis: {
    field: string;
    label: { ja: string; en: string };
    categories?: string[];
  };
  yAxis: {
    field: string;
    label: { ja: string; en: string };
    categories?: string[];
  };
  bubbleSize?: string; // データフィールド名
  bubbleColor?: string; // データフィールド名
  showQuadrantLabels?: boolean;
  quadrantLabels?: { ja: string[]; en: string[] };
  showConnections?: boolean;
  locale: 'ja' | 'en';
}

interface StrategyDataPoint {
  id: string;
  name: string;
  [key: string]: any; // 動的フィールド
}
```

### Usage

```tsx
import { StrategyMatrix } from '@/components/research';

// Exploration-Exploitation Matrix
<StrategyMatrix
  data={companyStrategyData}
  xAxis={{
    field: 'tech_evolution_stage',
    label: { ja: '技術進化ステージ', en: 'Tech Evolution Stage' },
    categories: ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
  }}
  yAxis={{
    field: 'funding_pressure',
    label: { ja: '資金調達圧力', en: 'Funding Pressure' },
  }}
  bubbleSize="revenue"
  bubbleColor="exploration_ratio"
  showQuadrantLabels={true}
  locale="ja"
/>
```

### Pre-built Strategy Frameworks

1. **市場成熟度分類マトリックス**
   - X軸: 市場成熟度（超成熟/成熟/急成長/新興）
   - Y軸: 戦略タイプ（差別化/低コスト/集中）

2. **Exploration-Exploitation バランス**
   - X軸: 探索活動比率
   - Y軸: 活用活動比率
   - バブルサイズ: R&D投資額

3. **技術進化×資金圧力マトリックス**
   - OpenAIのSeries F分析用
   - タイミングパラドックスの可視化

---

## 6. CitationNetwork

学術論文の引用ネットワークを力学シミュレーションで可視化。

### Props

```typescript
interface CitationNetworkProps {
  papers: Paper[];
  edges: CitationEdge[];
  nodeSize: 'citations' | 'year' | 'uniform';
  nodeColor: 'cluster' | 'year' | 'journal';
  layout: 'force' | 'hierarchical' | 'radial';
  showLabels?: boolean;
  labelThreshold?: number; // この被引用数以上のノードのみラベル表示
  onNodeClick?: (paper: Paper) => void;
  highlightPaths?: boolean;
  locale: 'ja' | 'en';
}

interface Paper {
  id: string;
  title: string;
  authors: string[];
  year: number;
  journal?: string;
  citations: number;
  abstract?: string;
}

interface CitationEdge {
  source_id: string;
  target_id: string;
  weight?: number;
}
```

### Usage

```tsx
import { CitationNetwork } from '@/components/research';

<CitationNetwork
  papers={papersData}
  edges={citationEdges}
  nodeSize="citations"
  nodeColor="year"
  layout="force"
  showLabels={true}
  labelThreshold={50}
  highlightPaths={true}
  locale="ja"
/>
```

### Features

1. **ズーム・パン**: マウスホイールとドラッグで操作
2. **ノード詳細**: クリックで論文の詳細情報を表示
3. **パス強調**: 特定論文から/への引用パスをハイライト
4. **クラスタリング**: 研究領域ごとに色分け

---

## 7. ResearchDataTable

高機能なデータテーブルコンポーネント。ソート、フィルター、ページネーション対応。

### Props

```typescript
interface ResearchDataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  enableSorting?: boolean;
  enableFiltering?: boolean;
  enablePagination?: boolean;
  pageSize?: number;
  enableExport?: boolean;
  exportFormats?: ('csv' | 'xlsx' | 'json')[];
  stickyHeader?: boolean;
  locale: 'ja' | 'en';
}
```

### Usage

```tsx
import { ResearchDataTable } from '@/components/research';
import { createColumnHelper } from '@tanstack/react-table';

const columnHelper = createColumnHelper<FinancialData>();

const columns = [
  columnHelper.accessor('company', {
    header: '企業名',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('arr', {
    header: 'ARR',
    cell: info => formatCurrency(info.getValue()),
  }),
];

<ResearchDataTable
  data={financialData}
  columns={columns}
  enableSorting={true}
  enableFiltering={true}
  enableExport={true}
  exportFormats={['csv', 'xlsx']}
  locale="ja"
/>
```

---

## 8. ComparativeAnalysis

複数企業・モデルの横断比較用コンポーネント。

### Props

```typescript
interface ComparativeAnalysisProps {
  entities: Entity[];
  metrics: MetricDefinition[];
  comparisonType: 'table' | 'bar' | 'radar' | 'parallel-coordinates';
  normalizeValues?: boolean;
  highlightBest?: boolean;
  showDelta?: boolean;
  baselineEntity?: string;
  locale: 'ja' | 'en';
}

interface Entity {
  id: string;
  name: string;
  [metricKey: string]: any;
}

interface MetricDefinition {
  key: string;
  label: { ja: string; en: string };
  unit?: string;
  higherIsBetter?: boolean;
  format?: (value: number) => string;
}
```

### Usage

```tsx
import { ComparativeAnalysis } from '@/components/research';

<ComparativeAnalysis
  entities={aiCompanies}
  metrics={[
    { key: 'arr', label: { ja: 'ARR', en: 'ARR' }, unit: '$B', higherIsBetter: true },
    { key: 'users', label: { ja: 'ユーザー数', en: 'Users' }, unit: 'M', higherIsBetter: true },
    { key: 'latency', label: { ja: '遅延', en: 'Latency' }, unit: 'ms', higherIsBetter: false },
  ]}
  comparisonType="parallel-coordinates"
  highlightBest={true}
  locale="ja"
/>
```

---

## 9. TheoreticalFramework

理論フレームワークの視覚的表現コンポーネント。

### Props

```typescript
interface TheoreticalFrameworkProps {
  framework: FrameworkDefinition;
  highlightConcepts?: string[];
  showReferences?: boolean;
  interactive?: boolean;
  locale: 'ja' | 'en';
}

interface FrameworkDefinition {
  name: { ja: string; en: string };
  concepts: Concept[];
  relationships: Relationship[];
  references?: Reference[];
}

interface Concept {
  id: string;
  name: { ja: string; en: string };
  description?: { ja: string; en: string };
  category?: string;
}

interface Relationship {
  from: string;
  to: string;
  type: 'causes' | 'moderates' | 'mediates' | 'correlates';
  label?: { ja: string; en: string };
}
```

### Pre-built Frameworks

1. **Organizational Ambidexterity** (March 1991)
2. **Resource Dependence Theory** (Pfeffer & Salancik 1978)
3. **Dynamic Capabilities** (Teece et al. 1997)
4. **Platform Theory** (Rochet & Tirole 2003)
5. **Institutional Distance** (Kostova 1999)

---

## 10. TimelineVisualization

企業・技術の時系列イベントを可視化。

### Props

```typescript
interface TimelineVisualizationProps {
  events: TimelineEvent[];
  tracks?: string[]; // 複数トラック表示用
  dateRange: [string, string];
  granularity: 'year' | 'quarter' | 'month';
  showMilestones?: boolean;
  showConnections?: boolean;
  locale: 'ja' | 'en';
}

interface TimelineEvent {
  id: string;
  title: { ja: string; en: string };
  date: string;
  track?: string;
  type: 'milestone' | 'funding' | 'product' | 'partnership' | 'event';
  description?: { ja: string; en: string };
  value?: number;
  relatedEvents?: string[];
}
```

### Usage

```tsx
import { TimelineVisualization } from '@/components/research';

<TimelineVisualization
  events={openAIEvents}
  tracks={['Funding', 'Products', 'Partnerships']}
  dateRange={['2015-01', '2025-12']}
  granularity="quarter"
  showMilestones={true}
  showConnections={true}
  locale="ja"
/>
```

---

## Utility Functions

### Data Transformation

```typescript
// CSV to component-ready format
import { transformFinancialData, transformMarketShareData } from '@/utils/dataTransform';

const dashboardData = transformFinancialData(rawCSV);
const marketData = transformMarketShareData(rawCSV);
```

### Export Utilities

```typescript
// Export chart as SVG/PNG
import { exportToSVG, exportToPNG, exportToCSV } from '@/utils/export';

exportToSVG(chartRef, 'financial-analysis.svg');
exportToPNG(chartRef, 'market-share.png', { scale: 2 });
exportToCSV(data, 'research-data.csv');
```

### Localization

```typescript
// Format numbers and dates for locale
import { formatNumber, formatDate, formatCurrency } from '@/utils/localization';

formatNumber(1000000, 'ja'); // "1,000,000"
formatDate('2024-01-15', 'ja'); // "2024年1月15日"
formatCurrency(1000000, 'USD', 'ja'); // "$1,000,000"
```

---

## Accessibility Guidelines

全コンポーネントは以下のアクセシビリティ基準を満たす：

1. **色覚多様性対応**: 色だけに依存せず、パターンや形状でも区別可能
2. **キーボードナビゲーション**: Tab/Enter/矢印キーで操作可能
3. **スクリーンリーダー対応**: ARIA属性による適切なラベリング
4. **高コントラスト**: WCAG AA基準を満たすコントラスト比

### Color Palette (Color-blind Safe)

```typescript
const accessiblePalette = {
  categorical: ['#2563eb', '#dc2626', '#16a34a', '#f59e0b', '#8b5cf6', '#06b6d4'],
  sequential: ['#eff6ff', '#bfdbfe', '#60a5fa', '#2563eb', '#1d4ed8', '#1e40af'],
  diverging: ['#dc2626', '#fca5a5', '#ffffff', '#86efac', '#16a34a']
};
```
