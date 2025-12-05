/**
 * Research Dashboard Template
 * 学術研究用のインタラクティブダッシュボードテンプレート
 *
 * このテンプレートは以下のデータタイプに対応：
 * - 財務データ (financial_data.csv)
 * - 市場シェアデータ (market_share_data.csv)
 * - ベンチマークデータ (technical_benchmarks.csv)
 * - ユーザー統計データ (user_statistics.csv)
 */

import React, { useState, useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';

// ============================================
// Types
// ============================================

interface FinancialDataPoint {
  company: string;
  date: string;
  arr?: number;
  revenue?: number;
  valuation?: number;
  funding?: number;
  losses?: number;
  source?: string;
}

interface MarketShareDataPoint {
  company: string;
  segment: 'consumer' | 'enterprise' | 'coding';
  year: number;
  share_percentage: number;
}

interface BenchmarkDataPoint {
  model_name: string;
  benchmark_name: string;
  score: number;
  max_score?: number;
}

// ============================================
// Constants
// ============================================

// 学術的なカラーパレット（色覚多様性対応）
const ACADEMIC_COLORS = {
  primary: ['#2563eb', '#dc2626', '#16a34a', '#f59e0b', '#8b5cf6', '#06b6d4'],
  neutral: ['#1f2937', '#4b5563', '#9ca3af'],
};

// 日本語・英語ラベル
const LABELS = {
  arr: { ja: 'ARR (年間経常収益)', en: 'ARR (Annual Recurring Revenue)' },
  revenue: { ja: '売上高', en: 'Revenue' },
  valuation: { ja: 'バリュエーション', en: 'Valuation' },
  marketShare: { ja: '市場シェア', en: 'Market Share' },
  users: { ja: 'ユーザー数', en: 'Users' },
  benchmark: { ja: 'ベンチマーク', en: 'Benchmark' },
};

// ============================================
// Utility Functions
// ============================================

/**
 * 数値を日本語フォーマットで表示
 */
const formatNumber = (value: number, locale: 'ja' | 'en' = 'ja'): string => {
  if (value >= 1e9) {
    return locale === 'ja'
      ? `${(value / 1e9).toFixed(1)}B`
      : `$${(value / 1e9).toFixed(1)}B`;
  }
  if (value >= 1e6) {
    return locale === 'ja'
      ? `${(value / 1e6).toFixed(1)}M`
      : `$${(value / 1e6).toFixed(1)}M`;
  }
  return value.toLocaleString(locale === 'ja' ? 'ja-JP' : 'en-US');
};

/**
 * CSVデータをパース
 */
const parseCSV = <T extends Record<string, any>>(csv: string): T[] => {
  const lines = csv.trim().split('\n');
  const headers = lines[0].split(',');

  return lines.slice(1).map((line) => {
    const values = line.split(',');
    const obj: Record<string, any> = {};

    headers.forEach((header, index) => {
      const value = values[index];
      // 数値に変換を試みる
      const numValue = parseFloat(value);
      obj[header.trim()] = isNaN(numValue) ? value : numValue;
    });

    return obj as T;
  });
};

// ============================================
// Components
// ============================================

/**
 * 財務ダッシュボードコンポーネント
 */
interface FinancialDashboardProps {
  data: FinancialDataPoint[];
  companies: string[];
  locale?: 'ja' | 'en';
}

export const FinancialDashboard: React.FC<FinancialDashboardProps> = ({
  data,
  companies,
  locale = 'ja',
}) => {
  const [selectedMetric, setSelectedMetric] = useState<'arr' | 'revenue' | 'valuation'>('arr');

  // データを時系列でグループ化
  const timeSeriesData = useMemo(() => {
    const grouped = new Map<string, Record<string, number>>();

    data.forEach((point) => {
      if (!companies.includes(point.company)) return;

      const existing = grouped.get(point.date) || { date: point.date };
      existing[point.company] = point[selectedMetric] || 0;
      grouped.set(point.date, existing);
    });

    return Array.from(grouped.values()).sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );
  }, [data, companies, selectedMetric]);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        {locale === 'ja' ? 'AI企業財務指標比較' : 'AI Company Financial Comparison'}
      </h2>

      {/* メトリック選択 */}
      <div className="flex gap-2 mb-4">
        {(['arr', 'revenue', 'valuation'] as const).map((metric) => (
          <button
            key={metric}
            onClick={() => setSelectedMetric(metric)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
              selectedMetric === metric
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {LABELS[metric][locale]}
          </button>
        ))}
      </div>

      {/* ラインチャート */}
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={timeSeriesData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickLine={{ stroke: '#d1d5db' }}
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickLine={{ stroke: '#d1d5db' }}
            tickFormatter={(value) => formatNumber(value, locale)}
          />
          <Tooltip
            formatter={(value: number) => formatNumber(value, locale)}
            labelStyle={{ color: '#374151' }}
            contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e5e7eb' }}
          />
          <Legend />
          {companies.map((company, index) => (
            <Line
              key={company}
              type="monotone"
              dataKey={company}
              stroke={ACADEMIC_COLORS.primary[index % ACADEMIC_COLORS.primary.length]}
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * 市場シェア推移コンポーネント
 */
interface MarketShareEvolutionProps {
  data: MarketShareDataPoint[];
  segment: 'consumer' | 'enterprise' | 'coding';
  locale?: 'ja' | 'en';
}

export const MarketShareEvolution: React.FC<MarketShareEvolutionProps> = ({
  data,
  segment,
  locale = 'ja',
}) => {
  const segmentLabels = {
    consumer: { ja: '消費者市場', en: 'Consumer Market' },
    enterprise: { ja: 'エンタープライズ市場', en: 'Enterprise Market' },
    coding: { ja: 'コーディング市場', en: 'Coding Market' },
  };

  // セグメントでフィルタリング
  const filteredData = useMemo(() => {
    return data.filter((d) => d.segment === segment);
  }, [data, segment]);

  // 年ごとにグループ化
  const chartData = useMemo(() => {
    const byYear = new Map<number, Record<string, any>>();

    filteredData.forEach((point) => {
      const existing = byYear.get(point.year) || { year: point.year };
      existing[point.company] = point.share_percentage;
      byYear.set(point.year, existing);
    });

    return Array.from(byYear.values()).sort((a, b) => a.year - b.year);
  }, [filteredData]);

  const companies = useMemo(() => {
    return [...new Set(filteredData.map((d) => d.company))];
  }, [filteredData]);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        {segmentLabels[segment][locale]} - {locale === 'ja' ? '市場シェア推移' : 'Market Share Evolution'}
      </h2>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="year" tick={{ fill: '#6b7280', fontSize: 12 }} />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={(value) => `${value}%`}
            domain={[0, 100]}
          />
          <Tooltip
            formatter={(value: number) => `${value.toFixed(1)}%`}
            contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e5e7eb' }}
          />
          <Legend />
          {companies.map((company, index) => (
            <Bar
              key={company}
              dataKey={company}
              stackId="a"
              fill={ACADEMIC_COLORS.primary[index % ACADEMIC_COLORS.primary.length]}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * ベンチマークレーダーチャートコンポーネント
 */
interface BenchmarkRadarProps {
  data: BenchmarkDataPoint[];
  models: string[];
  locale?: 'ja' | 'en';
}

export const BenchmarkRadar: React.FC<BenchmarkRadarProps> = ({
  data,
  models,
  locale = 'ja',
}) => {
  // レーダーチャート用にデータを変換
  const radarData = useMemo(() => {
    const benchmarks = [...new Set(data.map((d) => d.benchmark_name))];

    return benchmarks.map((benchmark) => {
      const point: Record<string, any> = { benchmark };

      models.forEach((model) => {
        const dataPoint = data.find(
          (d) => d.benchmark_name === benchmark && d.model_name === model
        );
        point[model] = dataPoint?.score || 0;
      });

      return point;
    });
  }, [data, models]);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        {locale === 'ja' ? 'AIモデルベンチマーク比較' : 'AI Model Benchmark Comparison'}
      </h2>

      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={radarData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <PolarGrid stroke="#e5e7eb" />
          <PolarAngleAxis
            dataKey="benchmark"
            tick={{ fill: '#6b7280', fontSize: 11 }}
          />
          <PolarRadiusAxis
            angle={30}
            domain={[0, 100]}
            tick={{ fill: '#9ca3af', fontSize: 10 }}
          />
          {models.map((model, index) => (
            <Radar
              key={model}
              name={model}
              dataKey={model}
              stroke={ACADEMIC_COLORS.primary[index % ACADEMIC_COLORS.primary.length]}
              fill={ACADEMIC_COLORS.primary[index % ACADEMIC_COLORS.primary.length]}
              fillOpacity={0.2}
            />
          ))}
          <Legend />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

/**
 * KPIカードコンポーネント
 */
interface KPICardProps {
  title: string;
  value: number;
  unit?: string;
  change?: number;
  locale?: 'ja' | 'en';
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  unit = '',
  change,
  locale = 'ja',
}) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow-md border border-gray-100">
      <p className="text-sm text-gray-500 mb-1">{title}</p>
      <p className="text-2xl font-bold text-gray-800">
        {formatNumber(value, locale)}
        {unit && <span className="text-lg font-normal text-gray-500 ml-1">{unit}</span>}
      </p>
      {change !== undefined && (
        <p className={`text-sm mt-1 ${change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change).toFixed(1)}%
          <span className="text-gray-400 ml-1">
            {locale === 'ja' ? '前年比' : 'YoY'}
          </span>
        </p>
      )}
    </div>
  );
};

/**
 * データフィルターコンポーネント
 */
interface DataFilterProps {
  companies: string[];
  selectedCompanies: string[];
  onSelectionChange: (companies: string[]) => void;
  locale?: 'ja' | 'en';
}

export const DataFilter: React.FC<DataFilterProps> = ({
  companies,
  selectedCompanies,
  onSelectionChange,
  locale = 'ja',
}) => {
  const toggleCompany = (company: string) => {
    if (selectedCompanies.includes(company)) {
      onSelectionChange(selectedCompanies.filter((c) => c !== company));
    } else {
      onSelectionChange([...selectedCompanies, company]);
    }
  };

  return (
    <div className="flex flex-wrap gap-2 p-4 bg-gray-50 rounded-lg">
      <span className="text-sm text-gray-600 self-center mr-2">
        {locale === 'ja' ? '企業選択:' : 'Select Companies:'}
      </span>
      {companies.map((company) => (
        <button
          key={company}
          onClick={() => toggleCompany(company)}
          className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
            selectedCompanies.includes(company)
              ? 'bg-blue-600 text-white'
              : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-100'
          }`}
        >
          {company}
        </button>
      ))}
    </div>
  );
};

// ============================================
// Main App Component
// ============================================

/**
 * メインダッシュボードアプリケーション
 */
const App: React.FC = () => {
  const [locale, setLocale] = useState<'ja' | 'en'>('ja');

  // サンプルデータ（実際の使用時はCSVからインポート）
  const sampleFinancialData: FinancialDataPoint[] = [
    { company: 'OpenAI', date: '2023-Q1', arr: 1300000000, revenue: 1040000000, valuation: 29000000000 },
    { company: 'OpenAI', date: '2023-Q4', arr: 2000000000, revenue: 1600000000, valuation: 86000000000 },
    { company: 'OpenAI', date: '2024-Q4', arr: 4000000000, revenue: 3200000000, valuation: 157000000000 },
    { company: 'Anthropic', date: '2023-Q1', arr: 400000000, revenue: 320000000, valuation: 4100000000 },
    { company: 'Anthropic', date: '2023-Q4', arr: 875000000, revenue: 700000000, valuation: 18000000000 },
    { company: 'Anthropic', date: '2024-Q4', arr: 1500000000, revenue: 1200000000, valuation: 61500000000 },
  ];

  const sampleBenchmarkData: BenchmarkDataPoint[] = [
    { model_name: 'GPT-4o', benchmark_name: 'MMLU', score: 87.2 },
    { model_name: 'GPT-4o', benchmark_name: 'SWE-Bench', score: 33.2 },
    { model_name: 'GPT-4o', benchmark_name: 'GSM8K', score: 94.2 },
    { model_name: 'Claude 3.5 Sonnet', benchmark_name: 'MMLU', score: 88.7 },
    { model_name: 'Claude 3.5 Sonnet', benchmark_name: 'SWE-Bench', score: 49.0 },
    { model_name: 'Claude 3.5 Sonnet', benchmark_name: 'GSM8K', score: 96.4 },
    { model_name: 'Gemini Pro', benchmark_name: 'MMLU', score: 83.7 },
    { model_name: 'Gemini Pro', benchmark_name: 'SWE-Bench', score: 28.5 },
    { model_name: 'Gemini Pro', benchmark_name: 'GSM8K', score: 91.8 },
  ];

  const [selectedCompanies, setSelectedCompanies] = useState<string[]>(['OpenAI', 'Anthropic']);

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* ヘッダー */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            {locale === 'ja' ? 'AI企業研究ダッシュボード' : 'AI Company Research Dashboard'}
          </h1>

          {/* 言語切替 */}
          <div className="flex gap-2">
            <button
              onClick={() => setLocale('ja')}
              className={`px-3 py-1 rounded ${locale === 'ja' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700'}`}
            >
              日本語
            </button>
            <button
              onClick={() => setLocale('en')}
              className={`px-3 py-1 rounded ${locale === 'en' ? 'bg-blue-600 text-white' : 'bg-white text-gray-700'}`}
            >
              English
            </button>
          </div>
        </div>

        {/* KPIカード */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <KPICard
            title={locale === 'ja' ? 'OpenAI ARR' : 'OpenAI ARR'}
            value={4000000000}
            change={100}
            locale={locale}
          />
          <KPICard
            title={locale === 'ja' ? 'Anthropic ARR' : 'Anthropic ARR'}
            value={1500000000}
            change={71.4}
            locale={locale}
          />
          <KPICard
            title={locale === 'ja' ? 'ChatGPT WAU' : 'ChatGPT WAU'}
            value={800000000}
            unit={locale === 'ja' ? '人' : 'users'}
            locale={locale}
          />
          <KPICard
            title={locale === 'ja' ? 'Claude MAU' : 'Claude MAU'}
            value={16000000}
            unit={locale === 'ja' ? '人' : 'users'}
            change={-15}
            locale={locale}
          />
        </div>

        {/* フィルター */}
        <DataFilter
          companies={['OpenAI', 'Anthropic', 'Google']}
          selectedCompanies={selectedCompanies}
          onSelectionChange={setSelectedCompanies}
          locale={locale}
        />

        {/* チャート */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
          <FinancialDashboard
            data={sampleFinancialData}
            companies={selectedCompanies}
            locale={locale}
          />

          <BenchmarkRadar
            data={sampleBenchmarkData}
            models={['GPT-4o', 'Claude 3.5 Sonnet', 'Gemini Pro']}
            locale={locale}
          />
        </div>
      </div>
    </div>
  );
};

export default App;
