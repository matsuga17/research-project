# Chart Patterns for Research - 研究用途別チャートパターン

このドキュメントは、研究目的に応じた最適なチャートパターンを提供する。

## 1. 企業比較分析パターン

### 1.1 財務指標比較

**目的**: 複数AI企業の財務パフォーマンスを比較

**推奨チャート**:
- **複数軸ラインチャート**: ARRと成長率を同時表示
- **グループ棒グラフ**: 四半期別の収益比較
- **ウォーターフォールチャート**: 資金調達の累積効果

```tsx
// 複数軸ラインチャートの実装例
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function DualAxisFinancialChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis yAxisId="left" label={{ value: 'ARR ($B)', angle: -90 }} />
        <YAxis yAxisId="right" orientation="right" label={{ value: '成長率 (%)', angle: 90 }} />
        <Tooltip />
        <Legend />
        <Line yAxisId="left" type="monotone" dataKey="arr" stroke="#2563eb" name="ARR" />
        <Line yAxisId="right" type="monotone" dataKey="growthRate" stroke="#dc2626" name="成長率" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### 1.2 市場ポジショニング

**目的**: 競合他社との市場位置関係を可視化

**推奨チャート**:
- **バブルチャート**: 市場シェア × 成長率 × 売上規模
- **マトリックスチャート**: BCGマトリックス風の4象限分析

```tsx
// バブルチャートの実装例
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export function MarketPositionBubble({ data }) {
  const colors = ['#2563eb', '#dc2626', '#16a34a', '#f59e0b'];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
        <XAxis type="number" dataKey="marketShare" name="市場シェア" unit="%" />
        <YAxis type="number" dataKey="growthRate" name="成長率" unit="%" />
        <ZAxis type="number" dataKey="revenue" range={[100, 1000]} name="売上" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter data={data}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  );
}
```

## 2. 時系列分析パターン

### 2.1 成長トレンド分析

**目的**: ユーザー数・収益の長期トレンドを把握

**推奨チャート**:
- **エリアチャート**: 累積的な成長を強調
- **ステップチャート**: 段階的な成長フェーズを表現
- **同期ラインチャート**: 複数指標のトレンド比較

```tsx
// 同期カーソル付きチャートグループ
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useState } from 'react';

export function SynchronizedCharts({ mauData, revenueData }) {
  const [activeIndex, setActiveIndex] = useState(null);

  const handleMouseMove = (e) => {
    if (e && e.activeTooltipIndex !== undefined) {
      setActiveIndex(e.activeTooltipIndex);
    }
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={mauData} onMouseMove={handleMouseMove}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="mau" stroke="#2563eb" />
          {activeIndex !== null && (
            <ReferenceLine x={mauData[activeIndex]?.date} stroke="#999" />
          )}
        </LineChart>
      </ResponsiveContainer>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={revenueData} onMouseMove={handleMouseMove}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#dc2626" />
          {activeIndex !== null && (
            <ReferenceLine x={revenueData[activeIndex]?.date} stroke="#999" />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

### 2.2 イベントタイムライン

**目的**: 企業の重要イベント（資金調達、製品リリース）を時系列で表示

**推奨チャート**:
- **ガントチャート風タイムライン**: 複数トラックでイベントを分類
- **スパークライン付きタイムライン**: 各イベントに関連指標を添付

```tsx
// イベントタイムラインの実装例
export function EventTimeline({ events }) {
  const trackColors = {
    funding: '#16a34a',
    product: '#2563eb',
    partnership: '#f59e0b',
    event: '#8b5cf6'
  };

  return (
    <div className="relative">
      {/* タイムライン軸 */}
      <div className="absolute left-0 right-0 h-0.5 bg-gray-300 top-1/2" />

      {/* イベントマーカー */}
      {events.map((event, index) => (
        <div
          key={event.id}
          className="absolute transform -translate-x-1/2"
          style={{ left: `${calculatePosition(event.date)}%` }}
        >
          <div
            className="w-4 h-4 rounded-full border-2 border-white"
            style={{ backgroundColor: trackColors[event.type] }}
          />
          <div className="mt-2 text-xs text-center whitespace-nowrap">
            {event.title.ja}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## 3. ベンチマーク分析パターン

### 3.1 多次元比較

**目的**: AIモデルの複数ベンチマークを同時比較

**推奨チャート**:
- **レーダーチャート**: 5-8次元の能力比較
- **平行座標プロット**: 多数の指標を一度に比較
- **ヒートマップ**: モデル×ベンチマークのスコアマトリックス

```tsx
// レーダーチャートの実装例
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend, ResponsiveContainer } from 'recharts';

export function BenchmarkRadarChart({ data, models }) {
  const colors = ['#2563eb', '#dc2626', '#16a34a'];

  return (
    <ResponsiveContainer width="100%" height={400}>
      <RadarChart data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="benchmark" />
        <PolarRadiusAxis angle={30} domain={[0, 100]} />
        {models.map((model, index) => (
          <Radar
            key={model}
            name={model}
            dataKey={model}
            stroke={colors[index]}
            fill={colors[index]}
            fillOpacity={0.2}
          />
        ))}
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );
}
```

### 3.2 コスト対性能分析

**目的**: 価格と性能のトレードオフを可視化

**推奨チャート**:
- **散布図**: 価格 × 性能スコア
- **パレートフロンティア**: 最適な選択肢を強調

```tsx
// コスト対性能散布図
export function CostPerformanceScatter({ data }) {
  // パレートフロンティアを計算
  const paretoFrontier = calculateParetoFrontier(data);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ScatterChart>
        <XAxis type="number" dataKey="cost" name="コスト" unit="$/1M tokens" />
        <YAxis type="number" dataKey="performance" name="性能スコア" />
        <Tooltip />
        <Scatter data={data} fill="#2563eb" />
        <Line
          type="stepAfter"
          data={paretoFrontier}
          dataKey="performance"
          stroke="#dc2626"
          strokeDasharray="5 5"
          name="パレートフロンティア"
        />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
```

## 4. 戦略フレームワークパターン

### 4.1 マトリックス分析

**目的**: 2軸の戦略的ポジショニングを可視化

**推奨チャート**:
- **4象限マトリックス**: 明確なカテゴリ分類
- **連続軸マトリックス**: グラデーションで位置を表現

```tsx
// 4象限戦略マトリックス
export function StrategyQuadrantMatrix({ data, xAxis, yAxis, quadrantLabels }) {
  return (
    <div className="relative w-full h-96 border border-gray-300">
      {/* 象限ラベル */}
      <div className="absolute top-2 left-2 text-sm text-gray-500">{quadrantLabels[0]}</div>
      <div className="absolute top-2 right-2 text-sm text-gray-500">{quadrantLabels[1]}</div>
      <div className="absolute bottom-2 left-2 text-sm text-gray-500">{quadrantLabels[2]}</div>
      <div className="absolute bottom-2 right-2 text-sm text-gray-500">{quadrantLabels[3]}</div>

      {/* 軸線 */}
      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-gray-300" />
      <div className="absolute top-1/2 left-0 right-0 h-px bg-gray-300" />

      {/* データポイント */}
      {data.map((point) => (
        <div
          key={point.id}
          className="absolute w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs transform -translate-x-1/2 -translate-y-1/2"
          style={{
            left: `${normalizeValue(point[xAxis.field], xAxis.min, xAxis.max) * 100}%`,
            top: `${(1 - normalizeValue(point[yAxis.field], yAxis.min, yAxis.max)) * 100}%`
          }}
        >
          {point.name.substring(0, 2)}
        </div>
      ))}

      {/* 軸ラベル */}
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-full mt-2">
        {xAxis.label.ja}
      </div>
      <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-full -rotate-90 mr-2">
        {yAxis.label.ja}
      </div>
    </div>
  );
}
```

### 4.2 フロー・プロセス図

**目的**: 戦略的意思決定プロセスやバリューチェーンを可視化

**推奨チャート**:
- **サンキーダイアグラム**: 資源・価値の流れ
- **フローチャート**: 意思決定プロセス

```tsx
// サンキーダイアグラム（D3.jsベース）
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';

export function StrategySankey({ nodes, links }) {
  const { nodes: layoutNodes, links: layoutLinks } = sankey()
    .nodeWidth(15)
    .nodePadding(10)
    .extent([[1, 1], [width - 1, height - 1]])
    ({ nodes, links });

  return (
    <svg width={width} height={height}>
      {/* リンク */}
      {layoutLinks.map((link, i) => (
        <path
          key={i}
          d={sankeyLinkHorizontal()(link)}
          fill="none"
          stroke="#cbd5e1"
          strokeOpacity={0.5}
          strokeWidth={Math.max(1, link.width)}
        />
      ))}

      {/* ノード */}
      {layoutNodes.map((node, i) => (
        <rect
          key={i}
          x={node.x0}
          y={node.y0}
          width={node.x1 - node.x0}
          height={node.y1 - node.y0}
          fill="#2563eb"
        />
      ))}
    </svg>
  );
}
```

## 5. ネットワーク分析パターン

### 5.1 引用ネットワーク

**目的**: 論文間の引用関係を可視化

**推奨チャート**:
- **Force-directed グラフ**: 自然なクラスタリング
- **階層グラフ**: 時系列での引用関係

```tsx
// D3 Force-directed Network
import { forceSimulation, forceLink, forceManyBody, forceCenter } from 'd3-force';
import { useEffect, useRef } from 'react';

export function CitationNetworkGraph({ papers, citations }) {
  const svgRef = useRef();

  useEffect(() => {
    const simulation = forceSimulation(papers)
      .force('link', forceLink(citations).id(d => d.id).distance(100))
      .force('charge', forceManyBody().strength(-300))
      .force('center', forceCenter(width / 2, height / 2));

    simulation.on('tick', () => {
      // ノードとリンクの位置を更新
    });

    return () => simulation.stop();
  }, [papers, citations]);

  return (
    <svg ref={svgRef} width={width} height={height}>
      {/* リンク */}
      <g className="links">
        {citations.map((link, i) => (
          <line key={i} stroke="#999" strokeOpacity={0.6} />
        ))}
      </g>

      {/* ノード */}
      <g className="nodes">
        {papers.map((paper) => (
          <circle
            key={paper.id}
            r={Math.sqrt(paper.citations) * 2}
            fill={getColorByYear(paper.year)}
          />
        ))}
      </g>
    </svg>
  );
}
```

### 5.2 組織間関係ネットワーク

**目的**: 企業間の提携・投資関係を可視化

**推奨チャート**:
- **双方向グラフ**: 投資元と投資先
- **クラスター図**: 企業グループの関係性

## 6. 地理的分析パターン

### 6.1 地域別市場分析

**目的**: アジア太平洋E-commerce市場など地域別データを可視化

**推奨チャート**:
- **コロプレスマップ**: 地域ごとの指標を色で表現
- **バブルマップ**: 都市・国ごとの規模を表現

```tsx
// 地域別バブルマップ（簡易版）
export function RegionalBubbleMap({ data }) {
  const regionPositions = {
    'Japan': { x: 80, y: 35 },
    'China': { x: 60, y: 40 },
    'India': { x: 45, y: 50 },
    'Indonesia': { x: 65, y: 60 },
    'Korea': { x: 75, y: 38 },
  };

  return (
    <svg viewBox="0 0 100 80" className="w-full h-auto">
      {/* 背景地図（簡易） */}
      <rect fill="#e5e7eb" width="100" height="80" />

      {/* データバブル */}
      {data.map((region) => {
        const pos = regionPositions[region.name];
        if (!pos) return null;

        return (
          <g key={region.name}>
            <circle
              cx={pos.x}
              cy={pos.y}
              r={Math.sqrt(region.value) / 10}
              fill="#2563eb"
              fillOpacity={0.6}
            />
            <text
              x={pos.x}
              y={pos.y + Math.sqrt(region.value) / 10 + 5}
              textAnchor="middle"
              fontSize="3"
              fill="#374151"
            >
              {region.name}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
```

## 7. データエクスポートパターン

### 7.1 学術論文用SVG出力

**目的**: 高品質な図表を学術論文に挿入

```tsx
// SVGエクスポート機能
export function ExportableSVGChart({ children, filename }) {
  const chartRef = useRef();

  const handleExport = () => {
    const svg = chartRef.current.querySelector('svg');
    const svgData = new XMLSerializer().serializeToString(svg);

    // 日本語フォントを埋め込み
    const svgWithFonts = svgData.replace(
      '<svg',
      `<svg xmlns="http://www.w3.org/2000/svg">
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
          text { font-family: 'Noto Sans JP', sans-serif; }
        </style`
    );

    const blob = new Blob([svgWithFonts], { type: 'image/svg+xml' });
    saveAs(blob, `${filename}.svg`);
  };

  return (
    <div ref={chartRef}>
      {children}
      <button onClick={handleExport} className="mt-2 px-4 py-2 bg-blue-600 text-white rounded">
        SVGでエクスポート
      </button>
    </div>
  );
}
```

### 7.2 インタラクティブHTML出力

**目的**: プレゼンテーションやWebサイトで使用

```bash
# artifacts-builderを使用してバンドル
bash scripts/bundle-artifact.sh

# 生成されたbundle.htmlをそのまま共有可能
```

## 8. アクセシビリティパターン

### 8.1 色覚多様性対応

```tsx
// カラーブラインド対応パレット
const colorBlindSafePalette = {
  // Wong palette (色覚多様性対応として広く推奨)
  primary: '#0072B2',    // Blue
  secondary: '#E69F00',  // Orange
  tertiary: '#009E73',   // Green
  quaternary: '#CC79A7', // Pink
  quinary: '#F0E442',    // Yellow
  senary: '#56B4E9',     // Light blue
  septenary: '#D55E00',  // Red-orange
};

// パターンで区別
const patterns = {
  solid: null,
  dashed: '5,5',
  dotted: '2,2',
  dashDot: '5,2,2,2',
};
```

### 8.2 キーボードナビゲーション

```tsx
// キーボード操作可能なチャートコンポーネント
export function KeyboardAccessibleChart({ data }) {
  const [focusedIndex, setFocusedIndex] = useState(0);

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowRight':
        setFocusedIndex(prev => Math.min(prev + 1, data.length - 1));
        break;
      case 'ArrowLeft':
        setFocusedIndex(prev => Math.max(prev - 1, 0));
        break;
    }
  };

  return (
    <div tabIndex={0} onKeyDown={handleKeyDown} role="img" aria-label="データチャート">
      {/* チャート実装 */}
      <div aria-live="polite" className="sr-only">
        現在のデータポイント: {data[focusedIndex].label}, 値: {data[focusedIndex].value}
      </div>
    </div>
  );
}
```
