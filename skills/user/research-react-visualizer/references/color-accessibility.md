# Color Accessibility Guide - アクセシブルなカラーパレット

学術研究の可視化における色覚多様性対応のガイドライン。

## 1. 推奨カラーパレット

### 1.1 Wong Palette（色覚多様性対応の標準）

Nature誌でも推奨される、色覚多様性に配慮したパレット。

```typescript
const wongPalette = {
  blue: '#0072B2',
  orange: '#E69F00',
  green: '#009E73',
  pink: '#CC79A7',
  yellow: '#F0E442',
  lightBlue: '#56B4E9',
  redOrange: '#D55E00',
  black: '#000000',
};
```

### 1.2 学術研究用パレット

```typescript
// カテゴリカルデータ用（最大8色）
const academicCategorical = [
  '#2563eb',  // Blue
  '#dc2626',  // Red
  '#16a34a',  // Green
  '#f59e0b',  // Amber
  '#8b5cf6',  // Violet
  '#06b6d4',  // Cyan
  '#ec4899',  // Pink
  '#84cc16',  // Lime
];

// 連続データ用（順序付き）
const academicSequential = {
  blue: ['#eff6ff', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8', '#1e40af'],
  green: ['#f0fdf4', '#dcfce7', '#bbf7d0', '#86efac', '#4ade80', '#22c55e', '#16a34a', '#15803d'],
  red: ['#fef2f2', '#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626', '#b91c1c'],
};

// 発散データ用（正負の値）
const academicDiverging = {
  blueRed: ['#1e40af', '#3b82f6', '#93c5fd', '#f5f5f5', '#fca5a5', '#ef4444', '#b91c1c'],
  greenPurple: ['#15803d', '#22c55e', '#86efac', '#f5f5f5', '#c4b5fd', '#8b5cf6', '#6d28d9'],
};
```

## 2. 色覚タイプ別の見え方

### 2.1 主な色覚タイプ

| タイプ | 割合 | 影響を受ける色 | 推奨対策 |
|--------|------|---------------|---------|
| P型（Protanopia） | 男性1% | 赤-緑 | 青-オレンジを使用 |
| D型（Deuteranopia） | 男性6% | 赤-緑 | 青-オレンジを使用 |
| T型（Tritanopia） | 0.01% | 青-黄 | 赤-緑を使用 |

### 2.2 シミュレーション確認

```typescript
// 色覚シミュレーション用の変換関数
const simulateProtanopia = (hex: string): string => {
  // Protanopia変換行列を適用
  // 実装は color-blindness-simulation ライブラリを使用
};

// Recharts での使用例
const colors = academicCategorical;
const protanopiaColors = colors.map(simulateProtanopia);
```

### 2.3 検証ツール

- **Coblis**: https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Sim Daltonism**: macOS用のリアルタイムシミュレーター
- **Chrome DevTools**: Rendering > Emulate vision deficiencies

## 3. 色以外の区別方法

### 3.1 パターン・テクスチャ

```tsx
// SVGパターン定義
const patterns = {
  diagonal: `
    <pattern id="diagonal" patternUnits="userSpaceOnUse" width="10" height="10">
      <path d="M-1,1 l2,-2 M0,10 l10,-10 M9,11 l2,-2" stroke="currentColor" strokeWidth="1"/>
    </pattern>
  `,
  dots: `
    <pattern id="dots" patternUnits="userSpaceOnUse" width="10" height="10">
      <circle cx="5" cy="5" r="2" fill="currentColor"/>
    </pattern>
  `,
  crosshatch: `
    <pattern id="crosshatch" patternUnits="userSpaceOnUse" width="10" height="10">
      <path d="M0,0 L10,10 M10,0 L0,10" stroke="currentColor" strokeWidth="1"/>
    </pattern>
  `,
};
```

### 3.2 形状による区別

```tsx
// Rechartsでの形状指定
const shapes = ['circle', 'square', 'triangle', 'diamond', 'star', 'cross'];

<Line
  dataKey="value"
  stroke="#2563eb"
  dot={{ r: 5, strokeWidth: 2 }}
  activeDot={{ r: 8 }}
  legendType="circle"
/>
```

### 3.3 線種による区別

```tsx
// ダッシュパターン
const lineStyles = {
  solid: undefined,
  dashed: '5 5',
  dotted: '2 2',
  dashDot: '5 2 2 2',
  longDash: '10 5',
};

<Line
  dataKey="valueA"
  stroke="#2563eb"
  strokeDasharray={lineStyles.solid}
/>
<Line
  dataKey="valueB"
  stroke="#dc2626"
  strokeDasharray={lineStyles.dashed}
/>
```

## 4. コントラスト要件

### 4.1 WCAG 2.1 基準

| レベル | テキスト最小コントラスト | 大きいテキスト | グラフィカル要素 |
|--------|------------------------|---------------|----------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | - |

### 4.2 コントラスト計算

```typescript
// 相対輝度を計算
const relativeLuminance = (hex: string): number => {
  const rgb = hexToRgb(hex);
  const [r, g, b] = rgb.map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

// コントラスト比を計算
const contrastRatio = (color1: string, color2: string): number => {
  const l1 = relativeLuminance(color1);
  const l2 = relativeLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
};

// 使用例
const ratio = contrastRatio('#2563eb', '#ffffff'); // 約4.6:1 → AA合格
```

### 4.3 推奨の背景・前景の組み合わせ

```typescript
const accessibleCombinations = {
  lightBackground: {
    background: '#ffffff',
    text: '#1f2937',      // コントラスト比 15.5:1
    secondaryText: '#6b7280', // コントラスト比 5.0:1
    accent: '#2563eb',    // コントラスト比 4.6:1
  },
  darkBackground: {
    background: '#1f2937',
    text: '#f9fafb',      // コントラスト比 14.4:1
    secondaryText: '#d1d5db', // コントラスト比 10.3:1
    accent: '#60a5fa',    // コントラスト比 6.2:1
  },
};
```

## 5. データ可視化の具体的な推奨事項

### 5.1 ラインチャート

```tsx
// 推奨: 色 + 線種 + マーカー形状の組み合わせ
const lineConfigs = [
  { color: '#2563eb', dash: undefined, marker: 'circle' },
  { color: '#dc2626', dash: '5 5', marker: 'square' },
  { color: '#16a34a', dash: '2 2', marker: 'triangle' },
  { color: '#f59e0b', dash: '5 2 2 2', marker: 'diamond' },
];
```

### 5.2 バーチャート

```tsx
// 推奨: 色 + パターンの組み合わせ
const barConfigs = [
  { color: '#2563eb', pattern: null },
  { color: '#dc2626', pattern: 'diagonal' },
  { color: '#16a34a', pattern: 'dots' },
  { color: '#f59e0b', pattern: 'crosshatch' },
];
```

### 5.3 ヒートマップ

```tsx
// 推奨: 単一色相のグラデーション（明度変化）
const heatmapScale = [
  '#eff6ff',  // 最小値
  '#bfdbfe',
  '#93c5fd',
  '#60a5fa',
  '#3b82f6',
  '#2563eb',
  '#1d4ed8',
  '#1e40af',  // 最大値
];

// 発散データ用
const divergingHeatmapScale = [
  '#b91c1c',  // 負の最大
  '#ef4444',
  '#fca5a5',
  '#f5f5f5',  // ゼロ
  '#93c5fd',
  '#3b82f6',
  '#1e40af',  // 正の最大
];
```

## 6. ラベリングとアノテーション

### 6.1 直接ラベリング

凡例に頼らず、データに直接ラベルを配置。

```tsx
// ライン終点にラベルを配置
<LineChart data={data}>
  <Line dataKey="value" stroke="#2563eb" />
  <LabelList dataKey="label" position="right" />
</LineChart>
```

### 6.2 ツールチップの強化

```tsx
// 色だけでなく、形状やラベルも含める
const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload) return null;

  return (
    <div className="bg-white p-3 rounded-lg shadow-lg border">
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-2">
          {/* 形状アイコン */}
          <span className="w-3 h-3" style={{ backgroundColor: entry.color }}>
            {shapes[index]}
          </span>
          {/* テキストラベル */}
          <span className="font-medium">{entry.name}</span>
          <span>{entry.value}</span>
        </div>
      ))}
    </div>
  );
};
```

## 7. テスト・検証チェックリスト

### 7.1 色覚シミュレーション確認

- [ ] P型色覚でも区別可能
- [ ] D型色覚でも区別可能
- [ ] T型色覚でも区別可能
- [ ] グレースケールでも情報が読み取れる

### 7.2 コントラスト確認

- [ ] テキストが背景に対して4.5:1以上
- [ ] グラフィカル要素が3:1以上
- [ ] 隣接する色同士が区別可能

### 7.3 代替手段の確認

- [ ] 色以外の区別方法（形状、パターン、テクスチャ）がある
- [ ] データテーブルなどの代替形式が利用可能
- [ ] 凡例が明確で、直接ラベリングも検討済み

## 8. Reactコンポーネントでの実装例

```tsx
import React from 'react';
import { LineChart, Line, Legend } from 'recharts';

// アクセシブルな設定をまとめたhook
const useAccessibleChartConfig = (dataCount: number) => {
  const configs = [
    { color: '#2563eb', dash: undefined, marker: 'circle' },
    { color: '#dc2626', dash: '5 5', marker: 'square' },
    { color: '#16a34a', dash: '2 2', marker: 'triangle' },
    { color: '#f59e0b', dash: '5 2 2 2', marker: 'diamond' },
    { color: '#8b5cf6', dash: '10 5', marker: 'star' },
    { color: '#06b6d4', dash: '3 3 6 3', marker: 'cross' },
  ];

  return configs.slice(0, dataCount);
};

// 使用例
export const AccessibleLineChart = ({ data, series }) => {
  const configs = useAccessibleChartConfig(series.length);

  return (
    <LineChart data={data}>
      {series.map((s, i) => (
        <Line
          key={s.key}
          dataKey={s.key}
          name={s.label}
          stroke={configs[i].color}
          strokeDasharray={configs[i].dash}
          dot={{ symbol: configs[i].marker }}
        />
      ))}
      <Legend />
    </LineChart>
  );
};
```
