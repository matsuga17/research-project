"""
自動データ品質チェックツール
============================
収集したデータの品質を自動的にチェックし、詳細なレポートを生成

使用方法:
    python data_quality_checker.py --input data.csv --output qa_report.html

Author: Corporate Research Data Hub
Version: 1.0
Date: 2025-10-31
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataQualityChecker:
    """データ品質チェッカー"""
    
    def __init__(self, df: pd.DataFrame, firm_id: str = 'firm_id', 
                 time_var: str = 'year', country_var: str = 'country'):
        """
        Parameters:
        -----------
        df : DataFrame
            チェック対象データ
        firm_id : str
            企業識別子カラム名
        time_var : str
            時間変数カラム名
        country_var : str
            国識別子カラム名（クロスカントリー研究の場合）
        """
        self.df = df
        self.firm_id = firm_id
        self.time_var = time_var
        self.country_var = country_var
        self.report = {}
        
    def check_all(self) -> dict:
        """全チェックを実行"""
        
        print("=" * 70)
        print("データ品質チェック開始")
        print("=" * 70)
        
        # 1. 基本情報
        self.check_basic_info()
        
        # 2. 欠損値分析
        self.check_missing_values()
        
        # 3. パネル構造
        self.check_panel_structure()
        
        # 4. 数値変数の分布
        self.check_numeric_distributions()
        
        # 5. 異常値検出
        self.check_outliers()
        
        # 6. 時系列一貫性
        self.check_temporal_consistency()
        
        # 7. 会計恒等式（該当する場合）
        self.check_accounting_identities()
        
        # 8. クロスセクション妥当性
        self.check_cross_sectional_reasonableness()
        
        print("\n" + "=" * 70)
        print("データ品質チェック完了")
        print("=" * 70)
        
        return self.report
    
    def check_basic_info(self):
        """基本情報のチェック"""
        
        print("\n[1/8] 基本情報チェック")
        
        info = {
            'total_observations': len(self.df),
            'total_variables': len(self.df.columns),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        if self.firm_id in self.df.columns:
            info['unique_firms'] = self.df[self.firm_id].nunique()
            info['avg_obs_per_firm'] = len(self.df) / info['unique_firms']
        
        if self.time_var in self.df.columns:
            info['time_coverage'] = (
                int(self.df[self.time_var].min()), 
                int(self.df[self.time_var].max())
            )
            info['time_periods'] = self.df[self.time_var].nunique()
        
        if self.country_var in self.df.columns:
            info['countries'] = self.df[self.country_var].nunique()
            info['country_distribution'] = self.df[self.country_var].value_counts().to_dict()
        
        self.report['basic_info'] = info
        
        # 表示
        print(f"  総観測数: {info['total_observations']:,}")
        print(f"  変数数: {info['total_variables']}")
        print(f"  メモリ使用量: {info['memory_usage_mb']:.2f} MB")
        if 'unique_firms' in info:
            print(f"  ユニーク企業数: {info['unique_firms']:,}")
            print(f"  企業あたり平均観測数: {info['avg_obs_per_firm']:.2f}")
        if 'time_coverage' in info:
            print(f"  時系列カバレッジ: {info['time_coverage'][0]} - {info['time_coverage'][1]}")
        if 'countries' in info:
            print(f"  国数: {info['countries']}")
    
    def check_missing_values(self):
        """欠損値分析"""
        
        print("\n[2/8] 欠損値分析")
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'missing_count': missing,
            'missing_percentage': missing_pct
        })
        missing_df = missing_df[missing_df['missing_count'] > 0].sort_values(
            'missing_percentage', ascending=False
        )
        
        self.report['missing_values'] = missing_df.to_dict('index')
        
        # 表示
        if len(missing_df) > 0:
            print(f"  欠損値のある変数: {len(missing_df)}")
            print("\n  欠損率トップ10:")
            for var, row in list(missing_df.iterrows())[:10]:
                print(f"    - {var}: {row['missing_percentage']:.1f}% ({int(row['missing_count'])} obs)")
            
            # 警告
            high_missing = missing_df[missing_df['missing_percentage'] > 50]
            if len(high_missing) > 0:
                print(f"\n  ⚠️  警告: {len(high_missing)} 変数が50%以上欠損")
        else:
            print("  ✓ 欠損値なし")
    
    def check_panel_structure(self):
        """パネル構造のチェック"""
        
        print("\n[3/8] パネル構造チェック")
        
        if self.firm_id not in self.df.columns or self.time_var not in self.df.columns:
            print("  スキップ: firm_id または time_var が見つかりません")
            return
        
        # 企業ごとの観測数
        obs_per_firm = self.df.groupby(self.firm_id)[self.time_var].count()
        
        structure = {
            'min_obs_per_firm': int(obs_per_firm.min()),
            'max_obs_per_firm': int(obs_per_firm.max()),
            'mean_obs_per_firm': float(obs_per_firm.mean()),
            'median_obs_per_firm': float(obs_per_firm.median())
        }
        
        # バランス度
        time_periods = self.df[self.time_var].nunique()
        perfectly_balanced = (obs_per_firm == time_periods).sum()
        structure['perfectly_balanced_firms'] = int(perfectly_balanced)
        structure['balance_percentage'] = float(perfectly_balanced / len(obs_per_firm) * 100)
        
        # 観測数が少ない企業
        insufficient = obs_per_firm[obs_per_firm < 3]
        structure['firms_with_less_than_3_obs'] = len(insufficient)
        
        self.report['panel_structure'] = structure
        
        # 表示
        print(f"  最小観測数: {structure['min_obs_per_firm']}")
        print(f"  最大観測数: {structure['max_obs_per_firm']}")
        print(f"  平均観測数: {structure['mean_obs_per_firm']:.2f}")
        print(f"  完全バランスド企業: {structure['perfectly_balanced_firms']} ({structure['balance_percentage']:.1f}%)")
        
        if structure['firms_with_less_than_3_obs'] > 0:
            print(f"  ⚠️  警告: {structure['firms_with_less_than_3_obs']} 企業が3年未満のデータ")
    
    def check_numeric_distributions(self):
        """数値変数の分布チェック"""
        
        print("\n[4/8] 数値変数の分布チェック")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        distributions = {}
        
        for col in numeric_cols:
            if col in [self.firm_id, self.time_var]:
                continue
            
            data = self.df[col].dropna()
            
            if len(data) == 0:
                continue
            
            dist = {
                'mean': float(data.mean()),
                'std': float(data.std()),
                'min': float(data.min()),
                'max': float(data.max()),
                'q25': float(data.quantile(0.25)),
                'median': float(data.median()),
                'q75': float(data.quantile(0.75)),
                'skewness': float(stats.skew(data)),
                'kurtosis': float(stats.kurtosis(data))
            }
            
            distributions[col] = dist
        
        self.report['distributions'] = distributions
        
        # 表示（主要変数のみ）
        key_vars = [col for col in ['roa', 'roe', 'leverage', 'sales', 'assets'] 
                    if col in distributions]
        
        if key_vars:
            print("  主要変数の分布:")
            for var in key_vars[:5]:
                dist = distributions[var]
                print(f"\n    {var}:")
                print(f"      平均: {dist['mean']:.4f}, 標準偏差: {dist['std']:.4f}")
                print(f"      範囲: [{dist['min']:.4f}, {dist['max']:.4f}]")
                print(f"      歪度: {dist['skewness']:.2f}, 尖度: {dist['kurtosis']:.2f}")
        
        print(f"\n  分析した数値変数: {len(distributions)}")
    
    def check_outliers(self):
        """異常値検出"""
        
        print("\n[5/8] 異常値検出")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        key_vars = [col for col in numeric_cols 
                   if col not in [self.firm_id, self.time_var] and 
                   self.df[col].notna().sum() > 100]
        
        if len(key_vars) == 0:
            print("  スキップ: 分析可能な数値変数がありません")
            return
        
        outliers_summary = {}
        
        for col in key_vars[:10]:  # 最初の10変数のみ
            data = self.df[col].dropna()
            
            # IQR法
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            
            outliers = data[(data < lower) | (data > upper)]
            
            outliers_summary[col] = {
                'count': len(outliers),
                'percentage': len(outliers) / len(data) * 100,
                'lower_bound': float(lower),
                'upper_bound': float(upper)
            }
        
        self.report['outliers'] = outliers_summary
        
        # 表示
        print("  IQR法による異常値検出（上位5変数）:")
        sorted_outliers = sorted(outliers_summary.items(), 
                                key=lambda x: x[1]['percentage'], 
                                reverse=True)
        
        for var, info in sorted_outliers[:5]:
            print(f"    {var}: {info['count']} ({info['percentage']:.2f}%)")
    
    def check_temporal_consistency(self):
        """時系列一貫性チェック"""
        
        print("\n[6/8] 時系列一貫性チェック")
        
        if self.firm_id not in self.df.columns or self.time_var not in self.df.columns:
            print("  スキップ: パネル構造が必要")
            return
        
        # 主要変数の成長率をチェック
        key_vars = [col for col in ['sales', 'assets', 'roa'] 
                   if col in self.df.columns]
        
        if len(key_vars) == 0:
            print("  スキップ: チェック対象変数がありません")
            return
        
        consistency = {}
        
        for var in key_vars:
            # 年次成長率
            df_sorted = self.df.sort_values([self.firm_id, self.time_var])
            df_sorted[f'{var}_growth'] = df_sorted.groupby(self.firm_id)[var].pct_change()
            
            growth = df_sorted[f'{var}_growth'].dropna()
            
            # 極端な変化を検出
            extreme_positive = (growth > 5).sum()  # 500%以上の成長
            extreme_negative = (growth < -0.9).sum()  # 90%以上の減少
            
            consistency[var] = {
                'extreme_positive_count': int(extreme_positive),
                'extreme_negative_count': int(extreme_negative),
                'extreme_total': int(extreme_positive + extreme_negative),
                'extreme_percentage': float((extreme_positive + extreme_negative) / len(growth) * 100)
            }
        
        self.report['temporal_consistency'] = consistency
        
        # 表示
        print("  極端な年次変化の検出:")
        for var, info in consistency.items():
            print(f"    {var}: {info['extreme_total']} 観測値 ({info['extreme_percentage']:.2f}%)")
            print(f"      - 極端な増加: {info['extreme_positive_count']}")
            print(f"      - 極端な減少: {info['extreme_negative_count']}")
    
    def check_accounting_identities(self):
        """会計恒等式チェック"""
        
        print("\n[7/8] 会計恒等式チェック")
        
        # 資産 = 負債 + 純資産
        required_vars = ['total_assets', 'total_liabilities', 'equity']
        alternative_vars = ['assets', 'liabilities', 'shareholders_equity']
        
        # 変数名のマッピングを試行
        var_map = {}
        for req, alt in zip(required_vars, alternative_vars):
            if req in self.df.columns:
                var_map[req] = req
            elif alt in self.df.columns:
                var_map[req] = alt
        
        if len(var_map) < 3:
            print("  スキップ: 必要な変数が見つかりません")
            print(f"    必要: total_assets, total_liabilities, equity")
            return
        
        # 計算
        df_check = self.df[[var_map[v] for v in required_vars]].dropna()
        
        if len(df_check) == 0:
            print("  スキップ: データがありません")
            return
        
        df_check['error'] = abs(
            df_check[var_map['total_assets']] - 
            (df_check[var_map['total_liabilities']] + df_check[var_map['equity']])
        )
        df_check['error_pct'] = df_check['error'] / df_check[var_map['total_assets']]
        
        # 統計
        errors = df_check[df_check['error_pct'] > 0.01]  # 1%以上のエラー
        
        accounting = {
            'observations_checked': len(df_check),
            'errors_above_1pct': len(errors),
            'error_rate': float(len(errors) / len(df_check) * 100),
            'mean_error_pct': float(errors['error_pct'].mean()) if len(errors) > 0 else 0,
            'max_error_pct': float(errors['error_pct'].max()) if len(errors) > 0 else 0
        }
        
        self.report['accounting_identities'] = accounting
        
        # 表示
        print(f"  チェック対象: {accounting['observations_checked']} 観測値")
        print(f"  エラー（>1%）: {accounting['errors_above_1pct']} ({accounting['error_rate']:.2f}%)")
        
        if accounting['errors_above_1pct'] > 0:
            print(f"  ⚠️  警告: 会計恒等式エラーが検出されました")
            print(f"    平均エラー: {accounting['mean_error_pct']*100:.2f}%")
            print(f"    最大エラー: {accounting['max_error_pct']*100:.2f}%")
        else:
            print("  ✓ 会計恒等式エラーなし")
    
    def check_cross_sectional_reasonableness(self):
        """横断的妥当性チェック"""
        
        print("\n[8/8] 横断的妥当性チェック")
        
        # 国別・年別の平均値をチェック
        if self.country_var in self.df.columns and self.time_var in self.df.columns:
            key_vars = [col for col in ['roa', 'leverage'] if col in self.df.columns]
            
            if len(key_vars) == 0:
                print("  スキップ: チェック対象変数がありません")
                return
            
            reasonableness = {}
            
            for var in key_vars:
                # 国別平均
                country_means = self.df.groupby(self.country_var)[var].mean()
                
                reasonableness[var] = {
                    'country_means': country_means.to_dict(),
                    'min_country_mean': float(country_means.min()),
                    'max_country_mean': float(country_means.max()),
                    'range': float(country_means.max() - country_means.min())
                }
            
            self.report['cross_sectional_reasonableness'] = reasonableness
            
            # 表示
            print("  国別平均値:")
            for var in key_vars:
                print(f"\n    {var}:")
                for country, mean in reasonableness[var]['country_means'].items():
                    print(f"      {country}: {mean:.4f}")
        else:
            print("  スキップ: country または year 変数が必要")
    
    def generate_html_report(self, output_path: str):
        """HTML形式のレポート生成"""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>データ品質レポート</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .warning {{ color: #e74c3c; font-weight: bold; }}
                .success {{ color: #27ae60; font-weight: bold; }}
                .metric {{ background-color: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .timestamp {{ color: #7f8c8d; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>データ品質チェックレポート</h1>
                <p class="timestamp">生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>1. 基本情報</h2>
                <div class="metric">
                    <p><strong>総観測数:</strong> {self.report['basic_info']['total_observations']:,}</p>
                    <p><strong>変数数:</strong> {self.report['basic_info']['total_variables']}</p>
        """
        
        if 'unique_firms' in self.report['basic_info']:
            html += f"""
                    <p><strong>ユニーク企業数:</strong> {self.report['basic_info']['unique_firms']:,}</p>
                    <p><strong>企業あたり平均観測数:</strong> {self.report['basic_info']['avg_obs_per_firm']:.2f}</p>
            """
        
        html += "</div>"
        
        # 欠損値
        if 'missing_values' in self.report and self.report['missing_values']:
            html += """
                <h2>2. 欠損値分析</h2>
                <table>
                    <tr><th>変数</th><th>欠損数</th><th>欠損率(%)</th></tr>
            """
            
            for var, info in list(self.report['missing_values'].items())[:20]:
                html += f"""
                    <tr>
                        <td>{var}</td>
                        <td>{int(info['missing_count']):,}</td>
                        <td>{info['missing_percentage']:.2f}%</td>
                    </tr>
                """
            
            html += "</table>"
        
        # パネル構造
        if 'panel_structure' in self.report:
            ps = self.report['panel_structure']
            html += f"""
                <h2>3. パネル構造</h2>
                <div class="metric">
                    <p><strong>最小観測数:</strong> {ps['min_obs_per_firm']}</p>
                    <p><strong>最大観測数:</strong> {ps['max_obs_per_firm']}</p>
                    <p><strong>平均観測数:</strong> {ps['mean_obs_per_firm']:.2f}</p>
                    <p><strong>完全バランスド企業率:</strong> {ps['balance_percentage']:.1f}%</p>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"\nHTMLレポート生成: {output_path}")


# ============================================================================
# 高度な品質保証機能（v2.0で追加）
# ============================================================================

class AdvancedQualityAssurance:
    """
    Publication-grade data quality assurance
    
    トップジャーナル（JF, JFE, RFS, MS, SMJ）の基準に準拠した
    統計的に厳密な品質保証フレームワーク
    
    References:
    - Button et al. (2013). Power failure in neuroscience. Nature Reviews Neuroscience.
    - Ioannidis (2005). Why most published research findings are false. PLoS Medicine.
    - Simmons et al. (2011). False-positive psychology. Psychological Science.
    """
    
    def __init__(self, df: pd.DataFrame, firm_id: str = 'firm_id', 
                 time_var: str = 'year', verbose: bool = True):
        self.df = df
        self.firm_id = firm_id
        self.time_var = time_var
        self.verbose = verbose
        self.qa_report = {}
    
    def run_comprehensive_qa(self) -> dict:
        """包括的品質保証チェックを実行"""
        
        if self.verbose:
            print("=" * 70)
            print("ADVANCED QUALITY ASSURANCE (v2.0)")
            print("=" * 70)
        
        # 1. Multivariate outlier detection
        self.qa_report['outliers'] = self.detect_multivariate_outliers()
        
        # 2. Benford's Law test
        self.qa_report['benfords_law'] = self.test_benfords_law()
        
        # 3. Regression-based anomaly detection
        self.qa_report['anomalies'] = self.detect_regression_anomalies()
        
        # 4. Time-series structural breaks
        self.qa_report['structural_breaks'] = self.detect_structural_breaks()
        
        # 5. Influential observations
        self.qa_report['influential_obs'] = self.detect_influential_observations()
        
        # 6. Sample selection bias
        self.qa_report['selection_bias'] = self.test_sample_selection_bias()
        
        return self.qa_report
    
    def detect_multivariate_outliers(self, variables: list = None,
                                    contamination: float = 0.01) -> dict:
        """
        アンサンブル手法による多変量異常値検出
        
        3手法を使用:
        1. Mahalanobis distance
        2. Isolation Forest
        3. Local Outlier Factor
        
        合意ルール: 3手法中2手法以上で検出 → 異常値
        """
        from sklearn.ensemble import IsolationForest
        from sklearn.neighbors import LocalOutlierFactor
        from sklearn.covariance import EllipticEnvelope
        
        if variables is None:
            variables = self.df.select_dtypes(include=[np.number]).columns.tolist()
            variables = [v for v in variables if v not in [self.firm_id, self.time_var]]
        
        X = self.df[variables].dropna()
        
        if len(X) < 30:
            warnings.warn("Sample size too small for reliable outlier detection")
            return {'error': 'Insufficient data'}
        
        # Method 1: Mahalanobis distance
        mean = X.mean()
        cov = X.cov()
        
        try:
            cov_inv = np.linalg.inv(cov)
            mahal_distances = []
            
            for idx, row in X.iterrows():
                dist = distance.mahalanobis(row, mean, cov_inv)
                mahal_distances.append(dist)
            
            mahal_distances = np.array(mahal_distances)
            threshold = stats.chi2.ppf(0.999, df=len(variables))
            mahal_outliers = mahal_distances > threshold
            
        except np.linalg.LinAlgError:
            warnings.warn("Covariance matrix is singular. Using robust covariance.")
            robust_cov = EllipticEnvelope(contamination=contamination)
            mahal_outliers = robust_cov.fit_predict(X) == -1
        
        # Method 2: Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
        iso_outliers = iso_forest.fit_predict(X) == -1
        
        # Method 3: Local Outlier Factor
        lof = LocalOutlierFactor(n_neighbors=min(20, len(X) // 10), contamination=contamination)
        lof_outliers = lof.fit_predict(X) == -1
        
        # Ensemble: 2/3 methods agree
        votes = mahal_outliers.astype(int) + iso_outliers.astype(int) + lof_outliers.astype(int)
        ensemble_outliers = votes >= 2
        
        # Add to DataFrame
        self.df['outlier_flag'] = 0
        self.df.loc[X.index, 'outlier_flag'] = ensemble_outliers.astype(int)
        self.df['outlier_confidence'] = 0.0
        self.df.loc[X.index, 'outlier_confidence'] = votes / 3
        
        result = {
            'total_outliers': int(ensemble_outliers.sum()),
            'outlier_rate': float(ensemble_outliers.sum() / len(X) * 100),
            'mahalanobis_outliers': int(mahal_outliers.sum()),
            'isolation_forest_outliers': int(iso_outliers.sum()),
            'lof_outliers': int(lof_outliers.sum()),
            'high_confidence_outliers': int((votes == 3).sum())
        }
        
        if self.verbose:
            print("\n[1/6] Multivariate Outlier Detection")
            print(f"  Total outliers: {result['total_outliers']} ({result['outlier_rate']:.2f}%)")
            print(f"  High confidence (3/3 methods): {result['high_confidence_outliers']}")
        
        return result
    
    def test_benfords_law(self, variable: str = 'sales') -> dict:
        """
        Benford's Law Test for fraud detection
        
        自然発生データの第1桁は特定の分布に従う: P(d) = log10(1 + 1/d)
        この分布からの逸脱はデータ操作の可能性を示唆
        """
        if variable not in self.df.columns:
            return {'error': f'Variable {variable} not found'}
        
        data = self.df[variable].dropna()
        data = data[data > 0]
        
        if len(data) == 0:
            return {'error': 'No valid data for Benford test'}
        
        # Extract first digit
        first_digits = data.apply(lambda x: int(str(abs(x)).replace('.', '')[0]) if str(abs(x)).replace('.', '')[0] != '0' else int(str(abs(x)).replace('.', '')[1]))
        
        # Observed frequencies
        observed = first_digits.value_counts().sort_index()
        
        # Expected frequencies (Benford's Law)
        expected_probs = {d: np.log10(1 + 1/d) for d in range(1, 10)}
        expected = pd.Series({d: expected_probs[d] * len(first_digits) for d in range(1, 10)})
        
        # Chi-square test
        chi2_stat, p_value = stats.chisquare(observed, expected[observed.index])
        
        result = {
            'chi2_statistic': float(chi2_stat),
            'p_value': float(p_value),
            'conforms_to_benford': p_value > 0.05,
            'observed': observed.to_dict(),
            'expected': expected.to_dict()
        }
        
        if self.verbose:
            print(f"\n[2/6] Benford's Law Test ({variable})")
            print(f"  χ² = {chi2_stat:.2f}, p = {p_value:.4f}")
            if p_value < 0.05:
                print("  ⚠️  WARNING: Significant deviation from Benford's Law")
            else:
                print("  ✓ Data conforms to Benford's Law")
        
        return result
    
    def detect_regression_anomalies(self, dependent_var: str = 'roa',
                                   predictors: list = None) -> dict:
        """回帰ベースの異常検出"""
        from sklearn.linear_model import LinearRegression
        
        if dependent_var not in self.df.columns:
            return {'error': f'Dependent variable {dependent_var} not found'}
        
        if predictors is None:
            predictors = ['log_assets', 'leverage', 'age']
            predictors = [p for p in predictors if p in self.df.columns]
        
        if not predictors:
            return {'error': 'No valid predictors found'}
        
        data = self.df[[dependent_var] + predictors].dropna()
        
        if len(data) < 50:
            return {'error': 'Insufficient observations'}
        
        y = data[dependent_var]
        X = data[predictors].copy()
        X['const'] = 1
        
        model = LinearRegression()
        model.fit(X, y)
        
        predictions = model.predict(X)
        residuals = y - predictions
        std_residuals = (residuals - residuals.mean()) / residuals.std()
        
        anomalies = np.abs(std_residuals) > 3
        
        self.df['regression_residual'] = np.nan
        self.df.loc[data.index, 'regression_residual'] = residuals
        self.df['anomaly_flag'] = 0
        self.df.loc[data.index[anomalies], 'anomaly_flag'] = 1
        
        result = {
            'total_anomalies': int(anomalies.sum()),
            'anomaly_rate': float(anomalies.sum() / len(data) * 100),
            'r_squared': float(model.score(X, y)),
            'max_residual': float(np.abs(residuals).max())
        }
        
        if self.verbose:
            print(f"\n[3/6] Regression-based Anomaly Detection")
            print(f"  Model R² = {result['r_squared']:.3f}")
            print(f"  Anomalies: {result['total_anomalies']} ({result['anomaly_rate']:.2f}%)")
        
        return result
    
    def detect_structural_breaks(self, variable: str = 'roa',
                                 min_segment_size: int = 30) -> dict:
        """構造的ブレークの検出（Chow test）"""
        
        if variable not in self.df.columns or self.time_var not in self.df.columns:
            return {'error': 'Required variables not found'}
        
        data = self.df[[self.time_var, variable]].dropna().sort_values(self.time_var)
        
        if len(data) < min_segment_size * 2:
            return {'error': 'Insufficient data'}
        
        breaks_detected = []
        
        for t in range(min_segment_size, len(data) - min_segment_size):
            segment1 = data.iloc[:t]
            segment2 = data.iloc[t:]
            
            f_stat, p_value = stats.f_oneway(segment1[variable], segment2[variable])
            
            if p_value < 0.01:
                breaks_detected.append({
                    'time': int(data.iloc[t][self.time_var]),
                    'f_statistic': float(f_stat),
                    'p_value': float(p_value)
                })
        
        result = {
            'breaks_detected': len(breaks_detected),
            'break_points': breaks_detected
        }
        
        if self.verbose:
            print(f"\n[4/6] Structural Break Detection ({variable})")
            if breaks_detected:
                print(f"  ⚠️  {len(breaks_detected)} structural breaks detected")
            else:
                print("  ✓ No significant structural breaks")
        
        return result
    
    def detect_influential_observations(self, dependent_var: str = 'roa',
                                       predictors: list = None) -> dict:
        """影響力の大きい観測値の検出（Cook's distance）"""
        
        try:
            import statsmodels.api as sm
            from statsmodels.stats.outliers_influence import OLSInfluence
        except ImportError:
            return {'error': 'statsmodels not installed'}
        
        if dependent_var not in self.df.columns:
            return {'error': f'Dependent variable not found'}
        
        if predictors is None:
            predictors = ['log_assets', 'leverage']
            predictors = [p for p in predictors if p in self.df.columns]
        
        data = self.df[[dependent_var] + predictors].dropna()
        
        if len(data) < 30:
            return {'error': 'Insufficient data'}
        
        y = data[dependent_var]
        X = sm.add_constant(data[predictors])
        
        model = sm.OLS(y, X).fit()
        influence = OLSInfluence(model)
        cooks_d = influence.cooks_distance[0]
        
        threshold = 4 / len(data)
        influential = cooks_d > threshold
        
        self.df['cooks_distance'] = np.nan
        self.df.loc[data.index, 'cooks_distance'] = cooks_d
        self.df['influential_flag'] = 0
        self.df.loc[data.index[influential], 'influential_flag'] = 1
        
        result = {
            'total_influential': int(influential.sum()),
            'influence_rate': float(influential.sum() / len(data) * 100),
            'threshold': float(threshold),
            'max_cooks_d': float(cooks_d.max())
        }
        
        if self.verbose:
            print(f"\n[5/6] Influential Observations Detection")
            print(f"  Influential: {result['total_influential']} ({result['influence_rate']:.2f}%)")
        
        return result
    
    def test_sample_selection_bias(self) -> dict:
        """サンプル選択バイアステスト"""
        
        if self.firm_id not in self.df.columns or self.time_var not in self.df.columns:
            return {'error': 'Panel structure required'}
        
        firms_by_year = self.df.groupby(self.time_var)[self.firm_id].nunique()
        
        max_firms = firms_by_year.max()
        min_firms = firms_by_year.min()
        attrition_rate = (max_firms - min_firms) / max_firms * 100
        
        all_years = self.df[self.time_var].unique()
        firm_year_counts = self.df.groupby(self.firm_id)[self.time_var].nunique()
        balanced_firms = (firm_year_counts == len(all_years)).sum()
        balance_rate = balanced_firms / len(firm_year_counts) * 100
        
        result = {
            'total_firms': int(self.df[self.firm_id].nunique()),
            'balanced_firms': int(balanced_firms),
            'balance_rate': float(balance_rate),
            'attrition_rate': float(attrition_rate),
            'warning': attrition_rate > 30
        }
        
        if self.verbose:
            print(f"\n[6/6] Sample Selection Bias Test")
            print(f"  Balanced firms: {balanced_firms} ({balance_rate:.1f}%)")
            print(f"  Attrition rate: {attrition_rate:.1f}%")
            if attrition_rate > 30:
                print("  ⚠️  WARNING: High attrition rate")
        
        return result


class SampleSizeCalculator:
    """
    統計的検出力に基づくサンプルサイズ設計
    
    References:
    - Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences.
    - Button, K. S., et al. (2013). Power failure in neuroscience. Nature Reviews Neuroscience.
    """
    
    def __init__(self):
        self.effect_size_benchmarks = {
            'small': 0.2,
            'medium': 0.5,
            'large': 0.8
        }
    
    def t_test_sample_size(self, effect_size, alpha=0.05, power=0.80, 
                          two_sided=True):
        """t検定のサンプルサイズ計算"""
        try:
            from statsmodels.stats.power import TTestIndPower
        except ImportError:
            return {'error': 'statsmodels not installed'}
        
        if isinstance(effect_size, str):
            effect_size = self.effect_size_benchmarks[effect_size]
        
        analysis = TTestIndPower()
        n_per_group = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative='two-sided' if two_sided else 'larger'
        )
        
        return {
            'n_per_group': int(np.ceil(n_per_group)),
            'total_n': int(np.ceil(n_per_group * 2)),
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power
        }
    
    def regression_sample_size(self, num_predictors, expected_r2, 
                               alpha=0.05, power=0.80):
        """重回帰分析のサンプルサイズ計算"""
        try:
            from statsmodels.stats.power import FTestPower
        except ImportError:
            return {'error': 'statsmodels not installed'}
        
        # Green (1991) の経験則
        rule_of_thumb_n = 104 + num_predictors
        
        # 統計的検出力に基づく計算
        f2 = expected_r2 / (1 - expected_r2)
        
        power_analysis = FTestPower()
        statistical_n = power_analysis.solve_power(
            effect_size=f2,
            df_num=num_predictors,
            alpha=alpha,
            power=power
        )
        
        recommended_n = max(rule_of_thumb_n, int(np.ceil(statistical_n)))
        
        return {
            'rule_of_thumb_n': rule_of_thumb_n,
            'statistical_power_n': int(np.ceil(statistical_n)),
            'recommended_n': recommended_n,
            'num_predictors': num_predictors,
            'expected_r2': expected_r2
        }
    
    def panel_data_sample_size(self, num_firms, num_periods, 
                              effect_size, alpha=0.05, power=0.80):
        """パネルデータ分析のサンプルサイズ設計"""
        
        base_result = self.t_test_sample_size(effect_size, alpha, power)
        base_n = base_result['total_n']
        
        # Design effect（クラスタリングによる増幅）
        avg_cluster_size = num_periods
        icc = 0.05  # Intraclass correlation（仮定）
        design_effect = 1 + (avg_cluster_size - 1) * icc
        
        adjusted_firms = int(np.ceil(base_n / num_periods * design_effect))
        
        return {
            'required_firms': adjusted_firms,
            'required_periods': num_periods,
            'total_observations': adjusted_firms * num_periods,
            'design_effect': design_effect
        }


# ============================================================================
# コマンドライン実行
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='データ品質チェックツール')
    parser.add_argument('--input', required=True, help='入力CSVファイルパス')
    parser.add_argument('--output', default='qa_report.html', help='出力HTMLファイルパス')
    parser.add_argument('--firm-id', default='firm_id', help='企業識別子カラム名')
    parser.add_argument('--time-var', default='year', help='時間変数カラム名')
    parser.add_argument('--country-var', default='country', help='国変数カラム名')
    
    args = parser.parse_args()
    
    # データ読み込み
    print(f"データ読み込み: {args.input}")
    df = pd.read_csv(args.input)
    
    # 品質チェック実行
    checker = DataQualityChecker(
        df, 
        firm_id=args.firm_id,
        time_var=args.time_var,
        country_var=args.country_var
    )
    
    report = checker.check_all()
    
    # HTMLレポート生成
    checker.generate_html_report(args.output)
    
    print("\n完了！")
    print(f"HTMLレポート: {args.output}")

# ============================================================================
# Advanced Quality Assurance (Publication-Grade)
# ============================================================================

class AdvancedQualityAssurance:
    """
    Publication-grade data quality assurance
    
    トップジャーナル（JF, JFE, RFS, MS, SMJ）の基準に準拠した
    統計的に厳密な品質保証フレームワーク
    
    References:
    - Button et al. (2013). Power failure in neuroscience. Nature Reviews Neuroscience.
    - Ioannidis (2005). Why most published research findings are false. PLoS Medicine.
    - Simmons et al. (2011). False-positive psychology. Psychological Science.
    """
    
    def __init__(self, df: pd.DataFrame, firm_id: str = 'firm_id', 
                 time_var: str = 'year', verbose: bool = True):
        """
        Parameters:
        -----------
        df : DataFrame
            チェック対象データ
        firm_id : str
            企業識別子カラム名
        time_var : str
            時間変数カラム名
        verbose : bool
            詳細出力の有無
        """
        self.df = df
        self.firm_id = firm_id
        self.time_var = time_var
        self.verbose = verbose
        self.qa_report = {}
    
    def run_comprehensive_qa(self) -> dict:
        """
        包括的品質保証チェックを実行
        
        Returns:
        --------
        report : dict
            詳細な品質レポート
        """
        if self.verbose:
            print("=" * 70)
            print("ADVANCED QUALITY ASSURANCE")
            print("=" * 70)
        
        # 1. Multivariate outlier detection
        self.qa_report['outliers'] = self.detect_multivariate_outliers()
        
        # 2. Benford's Law test
        self.qa_report['benfords_law'] = self.test_benfords_law()
        
        # 3. Regression-based anomaly detection
        self.qa_report['anomalies'] = self.detect_regression_anomalies()
        
        # 4. Time-series structural breaks
        self.qa_report['structural_breaks'] = self.detect_structural_breaks()
        
        # 5. Influential observations
        self.qa_report['influential_obs'] = self.detect_influential_observations()
        
        # 6. Sample selection bias
        self.qa_report['selection_bias'] = self.test_sample_selection_bias()
        
        return self.qa_report
    
    def detect_multivariate_outliers(self, variables: Optional[List[str]] = None,
                                    contamination: float = 0.01) -> dict:
        """
        アンサンブル手法による多変量異常値検出
        
        3手法を使用:
        1. Mahalanobis distance
        2. Isolation Forest
        3. Local Outlier Factor
        
        合意ルール: 3手法中2手法以上で検出 → 異常値
        
        Parameters:
        -----------
        variables : list of str, optional
            チェック対象変数リスト（デフォルト: 全数値変数）
        contamination : float
            想定される異常値の割合
        
        Returns:
        --------
        result : dict
            異常値検出結果
        """
        if variables is None:
            # デフォルト: 数値変数を使用
            variables = self.df.select_dtypes(include=[np.number]).columns.tolist()
            variables = [v for v in variables if v not in [self.firm_id, self.time_var]]
        
        X = self.df[variables].dropna()
        
        if len(X) < 30:
            warnings.warn("Sample size too small for reliable outlier detection")
            return {'error': 'Insufficient data'}
        
        # Method 1: Mahalanobis distance
        mean = X.mean()
        cov = X.cov()
        
        try:
            cov_inv = np.linalg.inv(cov)
            mahal_distances = []
            
            for idx, row in X.iterrows():
                dist = distance.mahalanobis(row, mean, cov_inv)
                mahal_distances.append(dist)
            
            mahal_distances = np.array(mahal_distances)
            # Chi-square threshold (p=0.001)
            threshold = stats.chi2.ppf(0.999, df=len(variables))
            mahal_outliers = mahal_distances > threshold
            
        except np.linalg.LinAlgError:
            warnings.warn("Covariance matrix is singular. Using robust covariance.")
            # Use Minimum Covariance Determinant (MCD) estimator
            from sklearn.covariance import EllipticEnvelope
            robust_cov = EllipticEnvelope(contamination=contamination)
            mahal_outliers = robust_cov.fit_predict(X) == -1
        
        # Method 2: Isolation Forest
        from sklearn.ensemble import IsolationForest
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        iso_outliers = iso_forest.fit_predict(X) == -1
        
        # Method 3: Local Outlier Factor
        from sklearn.neighbors import LocalOutlierFactor
        lof = LocalOutlierFactor(
            n_neighbors=min(20, len(X) // 10),
            contamination=contamination
        )
        lof_outliers = lof.fit_predict(X) == -1
        
        # Ensemble: 2/3 methods agree
        votes = mahal_outliers.astype(int) + iso_outliers.astype(int) + lof_outliers.astype(int)
        ensemble_outliers = votes >= 2
        
        # Add to DataFrame
        self.df['outlier_flag'] = 0
        self.df.loc[X.index, 'outlier_flag'] = ensemble_outliers.astype(int)
        self.df['outlier_confidence'] = 0.0
        self.df.loc[X.index, 'outlier_confidence'] = votes / 3
        
        result = {
            'total_outliers': int(ensemble_outliers.sum()),
            'outlier_rate': float(ensemble_outliers.sum() / len(X) * 100),
            'mahalanobis_outliers': int(mahal_outliers.sum()),
            'isolation_forest_outliers': int(iso_outliers.sum()),
            'lof_outliers': int(lof_outliers.sum()),
            'high_confidence_outliers': int((votes == 3).sum())
        }
        
        if self.verbose:
            print("\n[1/6] Multivariate Outlier Detection")
            print(f"  Total outliers detected: {result['total_outliers']} ({result['outlier_rate']:.2f}%)")
            print(f"  High confidence (3/3 methods): {result['high_confidence_outliers']}")
        
        return result
    
    def test_benfords_law(self, variable: str = 'sales') -> dict:
        """
        Benford's Law Test for fraud detection
        
        Benford's Law: 自然発生データの第1桁は特定の分布に従う
        P(d) = log10(1 + 1/d)
        
        この分布からの逸脱はデータ操作の可能性を示唆
        
        Parameters:
        -----------
        variable : str
            テスト対象変数（デフォルト: 'sales'）
        
        Returns:
        --------
        result : dict
            カイ二乗検定結果と観測・期待度数
        """
        if variable not in self.df.columns:
            return {'error': f'Variable {variable} not found'}
        
        data = self.df[variable].dropna()
        data = data[data > 0]  # 正の値のみ
        
        if len(data) < 100:
            return {'error': 'Insufficient data for Benford\'s Law test'}
        
        # 第1桁を抽出
        first_digits = data.apply(lambda x: int(str(abs(x)).replace('.', '')[0]))
        
        # 観測度数
        observed = first_digits.value_counts().sort_index()
        
        # 期待度数（Benford's Law）
        expected_probs = {d: np.log10(1 + 1/d) for d in range(1, 10)}
        expected = pd.Series({d: expected_probs[d] * len(first_digits) for d in range(1, 10)})
        
        # カイ二乗検定
        chi2_stat, p_value = stats.chisquare(observed, expected[observed.index])
        
        result = {
            'chi2_statistic': float(chi2_stat),
            'p_value': float(p_value),
            'conforms_to_benford': p_value > 0.05,
            'observed': observed.to_dict(),
            'expected': expected.to_dict()
        }
        
        if self.verbose:
            print(f"\n[2/6] Benford's Law Test ({variable})")
            print(f"  χ² = {chi2_stat:.2f}, p = {p_value:.4f}")
            if p_value < 0.05:
                print("  ⚠️  WARNING: Significant deviation from Benford's Law")
                print("     This may indicate data manipulation or unusual data generation process")
            else:
                print("  ✓ Data conforms to Benford's Law")
        
        return result
    
    def detect_regression_anomalies(self, dependent_var: str = 'roa',
                                   predictors: Optional[List[str]] = None) -> dict:
        """
        回帰ベースの異常検出
        
        期待値から大きく外れる観測値を検出
        
        Parameters:
        -----------
        dependent_var : str
            従属変数
        predictors : list of str, optional
            予測変数リスト
        
        Returns:
        --------
        result : dict
            異常検出結果
        """
        if dependent_var not in self.df.columns:
            return {'error': f'Dependent variable {dependent_var} not found'}
        
        if predictors is None:
            # デフォルト予測変数
            predictors = ['log_assets', 'leverage', 'age']
            predictors = [p for p in predictors if p in self.df.columns]
        
        if not predictors:
            return {'error': 'No valid predictors found'}
        
        # Prepare data
        data = self.df[[dependent_var] + predictors].dropna()
        
        if len(data) < 50:
            return {'error': 'Insufficient observations for regression'}
        
        y = data[dependent_var]
        X = data[predictors]
        
        # Add constant
        X = X.copy()
        X['const'] = 1
        
        # OLS regression
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predictions and residuals
        predictions = model.predict(X)
        residuals = y - predictions
        
        # Standardized residuals
        std_residuals = (residuals - residuals.mean()) / residuals.std()
        
        # Anomalies: |standardized residual| > 3
        anomalies = np.abs(std_residuals) > 3
        
        self.df['regression_residual'] = np.nan
        self.df.loc[data.index, 'regression_residual'] = residuals
        self.df['anomaly_flag'] = 0
        self.df.loc[data.index[anomalies], 'anomaly_flag'] = 1
        
        result = {
            'total_anomalies': int(anomalies.sum()),
            'anomaly_rate': float(anomalies.sum() / len(data) * 100),
            'r_squared': float(model.score(X, y)),
            'max_residual': float(np.abs(residuals).max())
        }
        
        if self.verbose:
            print(f"\n[3/6] Regression-based Anomaly Detection")
            print(f"  Model R² = {result['r_squared']:.3f}")
            print(f"  Anomalies detected: {result['total_anomalies']} ({result['anomaly_rate']:.2f}%)")
        
        return result
    
    def detect_structural_breaks(self, variable: str = 'roa',
                                 min_segment_size: int = 30) -> dict:
        """
        構造的ブレークの検出（Chow test）
        
        時系列データにおける構造的変化を検出
        
        Parameters:
        -----------
        variable : str
            テスト対象変数
        min_segment_size : int
            最小セグメントサイズ
        
        Returns:
        --------
        result : dict
            構造的ブレーク検出結果
        """
        if variable not in self.df.columns:
            return {'error': f'Variable {variable} not found'}
        
        if self.time_var not in self.df.columns:
            return {'error': 'Time variable not found'}
        
        # Sort by time
        data = self.df[[self.time_var, variable]].dropna().sort_values(self.time_var)
        
        if len(data) < min_segment_size * 2:
            return {'error': 'Insufficient data for structural break detection'}
        
        # Test for break at each potential breakpoint
        breaks_detected = []
        
        for t in range(min_segment_size, len(data) - min_segment_size):
            # Split sample
            segment1 = data.iloc[:t]
            segment2 = data.iloc[t:]
            
            # F-test for equality of means
            f_stat, p_value = stats.f_oneway(
                segment1[variable],
                segment2[variable]
            )
            
            if p_value < 0.01:  # Bonferroni correction recommended
                breaks_detected.append({
                    'time': int(data.iloc[t][self.time_var]),
                    'f_statistic': float(f_stat),
                    'p_value': float(p_value)
                })
        
        result = {
            'breaks_detected': len(breaks_detected),
            'break_points': breaks_detected
        }
        
        if self.verbose:
            print(f"\n[4/6] Structural Break Detection ({variable})")
            if breaks_detected:
                print(f"  ⚠️  {len(breaks_detected)} structural breaks detected")
                for bp in breaks_detected[:3]:  # Show first 3
                    print(f"     Year {bp['time']}: F={bp['f_statistic']:.2f}, p={bp['p_value']:.4f}")
            else:
                print("  ✓ No significant structural breaks detected")
        
        return result
    
    def detect_influential_observations(self, dependent_var: str = 'roa',
                                       predictors: Optional[List[str]] = None) -> dict:
        """
        影響力の大きい観測値の検出（Cook's distance）
        
        Parameters:
        -----------
        dependent_var : str
            従属変数
        predictors : list of str, optional
            予測変数リスト
        
        Returns:
        --------
        result : dict
            影響力のある観測値の検出結果
        """
        if dependent_var not in self.df.columns:
            return {'error': f'Dependent variable {dependent_var} not found'}
        
        if predictors is None:
            predictors = ['log_assets', 'leverage']
            predictors = [p for p in predictors if p in self.df.columns]
        
        if not predictors:
            return {'error': 'No valid predictors found'}
        
        # Prepare data
        data = self.df[[dependent_var] + predictors].dropna()
        
        if len(data) < 30:
            return {'error': 'Insufficient data'}
        
        # Import statsmodels for Cook's distance
        try:
            import statsmodels.api as sm
            from statsmodels.stats.outliers_influence import OLSInfluence
        except ImportError:
            return {'error': 'statsmodels not installed'}
        
        y = data[dependent_var]
        X = sm.add_constant(data[predictors])
        
        # Fit model
        model = sm.OLS(y, X).fit()
        influence = OLSInfluence(model)
        
        # Cook's distance
        cooks_d = influence.cooks_distance[0]
        
        # Threshold: 4/n (common rule of thumb)
        threshold = 4 / len(data)
        influential = cooks_d > threshold
        
        self.df['cooks_distance'] = np.nan
        self.df.loc[data.index, 'cooks_distance'] = cooks_d
        self.df['influential_flag'] = 0
        self.df.loc[data.index[influential], 'influential_flag'] = 1
        
        result = {
            'total_influential': int(influential.sum()),
            'influence_rate': float(influential.sum() / len(data) * 100),
            'threshold': float(threshold),
            'max_cooks_d': float(cooks_d.max())
        }
        
        if self.verbose:
            print(f"\n[5/6] Influential Observations Detection")
            print(f"  Influential observations: {result['total_influential']} ({result['influence_rate']:.2f}%)")
            print(f"  Cook's D threshold: {result['threshold']:.4f}")
        
        return result
    
    def test_sample_selection_bias(self) -> dict:
        """
        Sample selection bias test
        
        生存バイアス、脱落バイアスの検出
        
        Returns:
        --------
        result : dict
            サンプル選択バイアステスト結果
        """
        if self.firm_id not in self.df.columns or self.time_var not in self.df.columns:
            return {'error': 'Panel structure required'}
        
        # Firms by year
        firms_by_year = self.df.groupby(self.time_var)[self.firm_id].nunique()
        
        # Attrition rate
        max_firms = firms_by_year.max()
        min_firms = firms_by_year.min()
        attrition_rate = (max_firms - min_firms) / max_firms * 100
        
        # Firms present in all years (balanced)
        all_years = self.df[self.time_var].unique()
        firm_year_counts = self.df.groupby(self.firm_id)[self.time_var].nunique()
        balanced_firms = (firm_year_counts == len(all_years)).sum()
        balance_rate = balanced_firms / len(firm_year_counts) * 100
        
        result = {
            'total_firms': int(self.df[self.firm_id].nunique()),
            'balanced_firms': int(balanced_firms),
            'balance_rate': float(balance_rate),
            'attrition_rate': float(attrition_rate),
            'firms_by_year': firms_by_year.to_dict(),
            'warning': attrition_rate > 30
        }
        
        if self.verbose:
            print(f"\n[6/6] Sample Selection Bias Test")
            print(f"  Balanced panel firms: {balanced_firms} ({balance_rate:.1f}%)")
            print(f"  Attrition rate: {attrition_rate:.1f}%")
            if attrition_rate > 30:
                print("  ⚠️  WARNING: High attrition rate may indicate selection bias")
        
        return result
    
    def generate_advanced_qa_report(self, output_path: str = 'advanced_qa_report.html'):
        """
        詳細なHTMLレポートを生成
        
        Parameters:
        -----------
        output_path : str
            出力ファイルパス
        """
        html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Quality Assurance Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; border-left: 4px solid #3498db; padding-left: 10px; }}
        .metric {{ background-color: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .warning {{ background-color: #ffe6e6; border-left: 4px solid #e74c3c; }}
        .success {{ background-color: #e6f7e6; border-left: 4px solid #27ae60; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #3498db; color: white; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .footer {{ margin-top: 30px; text-align: center; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Advanced Quality Assurance Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Dataset Size:</strong> {len(self.df):,} observations</p>
        
        <h2>1. Multivariate Outlier Detection</h2>
        <div class="metric {'warning' if self.qa_report.get('outliers', {}).get('outlier_rate', 0) > 5 else 'success'}">
            <p><strong>Total Outliers:</strong> {self.qa_report.get('outliers', {}).get('total_outliers', 'N/A')} ({self.qa_report.get('outliers', {}).get('outlier_rate', 0):.2f}%)</p>
            <p><strong>High Confidence Outliers (3/3 methods):</strong> {self.qa_report.get('outliers', {}).get('high_confidence_outliers', 'N/A')}</p>
        </div>
        
        <h2>2. Benford's Law Test</h2>
        <div class="metric {'success' if self.qa_report.get('benfords_law', {}).get('conforms_to_benford', False) else 'warning'}">
            <p><strong>Chi-square statistic:</strong> {self.qa_report.get('benfords_law', {}).get('chi2_statistic', 'N/A'):.2f}</p>
            <p><strong>p-value:</strong> {self.qa_report.get('benfords_law', {}).get('p_value', 'N/A'):.4f}</p>
            <p><strong>Conforms to Benford's Law:</strong> {'✓ Yes' if self.qa_report.get('benfords_law', {}).get('conforms_to_benford', False) else '⚠️ No'}</p>
        </div>
        
        <h2>3. Regression-based Anomaly Detection</h2>
        <div class="metric">
            <p><strong>Anomalies Detected:</strong> {self.qa_report.get('anomalies', {}).get('total_anomalies', 'N/A')} ({self.qa_report.get('anomalies', {}).get('anomaly_rate', 0):.2f}%)</p>
            <p><strong>Model R²:</strong> {self.qa_report.get('anomalies', {}).get('r_squared', 'N/A'):.3f}</p>
        </div>
        
        <h2>4. Structural Breaks</h2>
        <div class="metric {'warning' if self.qa_report.get('structural_breaks', {}).get('breaks_detected', 0) > 0 else 'success'}">
            <p><strong>Breaks Detected:</strong> {self.qa_report.get('structural_breaks', {}).get('breaks_detected', 'N/A')}</p>
        </div>
        
        <h2>5. Influential Observations</h2>
        <div class="metric">
            <p><strong>Influential Observations:</strong> {self.qa_report.get('influential_obs', {}).get('total_influential', 'N/A')} ({self.qa_report.get('influential_obs', {}).get('influence_rate', 0):.2f}%)</p>
        </div>
        
        <h2>6. Sample Selection Bias</h2>
        <div class="metric {'warning' if self.qa_report.get('selection_bias', {}).get('warning', False) else 'success'}">
            <p><strong>Total Firms:</strong> {self.qa_report.get('selection_bias', {}).get('total_firms', 'N/A')}</p>
            <p><strong>Balanced Panel Firms:</strong> {self.qa_report.get('selection_bias', {}).get('balanced_firms', 'N/A')} ({self.qa_report.get('selection_bias', {}).get('balance_rate', 0):.1f}%)</p>
            <p><strong>Attrition Rate:</strong> {self.qa_report.get('selection_bias', {}).get('attrition_rate', 0):.1f}%</p>
        </div>
        
        <div class="footer">
            <p>Corporate Research Data Hub - Advanced Quality Assurance v2.0</p>
            <p>Generated with AdvancedQualityAssurance class</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✓ Advanced QA Report saved: {output_path}")




# ============================================================================
# Advanced Quality Assurance Module (v2.0)
# ============================================================================
"""
Publication-Grade Data Quality Assurance
=========================================
統計的に厳密な品質保証フレームワーク

References:
- Button et al. (2013). Power failure in neuroscience. Nature Reviews Neuroscience.
- Ioannidis (2005). Why most published research findings are false. PLoS Medicine.
- Simmons et al. (2011). False-positive psychology. Psychological Science.
"""

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from typing import Dict, List, Tuple, Optional

class AdvancedQualityAssurance:
    """
    Publication-grade data quality assurance
    
    7つの相補的テスト:
    1. 多変量異常値検出（アンサンブル）
    2. Benford's Law テスト（不正検出）
    3. 回帰ベース異常検出
    4. 構造的ブレーク検出
    5. 影響力の大きい観測値検出
    6. 出版バイアステスト
    7. サンプル選択バイアステスト
    """
    
    def __init__(self, df: pd.DataFrame, firm_id: str = 'firm_id', 
                 time_var: str = 'year', verbose: bool = True):
        """
        Parameters:
        -----------
        df : DataFrame
            分析対象データ
        firm_id : str
            企業識別子
        time_var : str
            時間変数
        verbose : bool
            進捗表示
        """
        self.df = df.copy()
        self.firm_id = firm_id
        self.time_var = time_var
        self.verbose = verbose
        self.qa_report = {}
    
    def run_comprehensive_qa(self) -> Dict:
        """
        包括的品質保証チェックを実行
        
        Returns:
        --------
        report : dict
            詳細な品質レポート
        """
        if self.verbose:
            print("=" * 70)
            print("ADVANCED QUALITY ASSURANCE - Publication Grade")
            print("=" * 70)
        
        # 1. Multivariate outlier detection
        self.qa_report['outliers'] = self.detect_multivariate_outliers()
        
        # 2. Benford's Law test
        self.qa_report['benfords_law'] = self.test_benfords_law()
        
        # 3. Regression-based anomaly detection
        self.qa_report['anomalies'] = self.detect_regression_anomalies()
        
        # 4. Time-series structural breaks
        self.qa_report['structural_breaks'] = self.detect_structural_breaks()
        
        # 5. Influential observations
        self.qa_report['influential_obs'] = self.detect_influential_observations()
        
        # 6. Publication bias tests
        if 'effect_size' in self.df.columns and 'standard_error' in self.df.columns:
            self.qa_report['publication_bias'] = self.test_publication_bias()
        
        # 7. Sample selection bias
        self.qa_report['selection_bias'] = self.test_sample_selection_bias()
        
        if self.verbose:
            print("\n" + "=" * 70)
            print("QUALITY ASSURANCE COMPLETE")
            print("=" * 70)
        
        return self.qa_report
    
    def detect_multivariate_outliers(self, variables: Optional[List[str]] = None,
                                    contamination: float = 0.01) -> Dict:
        """
        アンサンブル手法による多変量異常値検出
        
        3手法を使用:
        1. Mahalanobis distance (α=0.001)
        2. Isolation Forest (contamination=0.01)
        3. Local Outlier Factor (n_neighbors=20)
        
        合意ルール: 3手法中2手法以上で検出 → 異常値
        
        Parameters:
        -----------
        variables : list of str, optional
            検出対象変数（デフォルト: 全数値変数）
        contamination : float
            異常値の予想割合
        
        Returns:
        --------
        result : dict
            検出結果とメトリクス
        """
        if variables is None:
            # デフォルト: 数値変数を使用
            variables = self.df.select_dtypes(include=[np.number]).columns.tolist()
            variables = [v for v in variables if v not in [self.firm_id, self.time_var]]
        
        X = self.df[variables].dropna()
        
        if len(X) < 30:
            warnings.warn("Sample size too small for reliable outlier detection")
            return {'error': 'Insufficient data'}
        
        # Method 1: Mahalanobis distance
        mean = X.mean()
        cov = X.cov()
        
        try:
            cov_inv = np.linalg.inv(cov)
            mahal_distances = []
            
            for idx, row in X.iterrows():
                dist = distance.mahalanobis(row, mean, cov_inv)
                mahal_distances.append(dist)
            
            mahal_distances = np.array(mahal_distances)
            # Chi-square threshold (p=0.001)
            threshold = stats.chi2.ppf(0.999, df=len(variables))
            mahal_outliers = mahal_distances > threshold
            
        except np.linalg.LinAlgError:
            warnings.warn("Covariance matrix is singular. Using robust covariance.")
            # Use Minimum Covariance Determinant (MCD) estimator
            robust_cov = EllipticEnvelope(contamination=contamination)
            mahal_outliers = robust_cov.fit_predict(X) == -1
        
        # Method 2: Isolation Forest
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        iso_outliers = iso_forest.fit_predict(X) == -1
        
        # Method 3: Local Outlier Factor
        lof = LocalOutlierFactor(
            n_neighbors=min(20, len(X) // 10),
            contamination=contamination
        )
        lof_outliers = lof.fit_predict(X) == -1
        
        # Ensemble: 2/3 methods agree
        votes = mahal_outliers.astype(int) + iso_outliers.astype(int) + lof_outliers.astype(int)
        ensemble_outliers = votes >= 2
        
        # Add to DataFrame
        self.df['outlier_flag'] = 0
        self.df.loc[X.index, 'outlier_flag'] = ensemble_outliers.astype(int)
        self.df['outlier_confidence'] = 0.0
        self.df.loc[X.index, 'outlier_confidence'] = votes / 3
        
        result = {
            'total_outliers': int(ensemble_outliers.sum()),
            'outlier_rate': float(ensemble_outliers.sum() / len(X) * 100),
            'mahalanobis_outliers': int(mahal_outliers.sum()),
            'isolation_forest_outliers': int(iso_outliers.sum()),
            'lof_outliers': int(lof_outliers.sum()),
            'high_confidence_outliers': int((votes == 3).sum())
        }
        
        if self.verbose:
            print("\n[1/7] Multivariate Outlier Detection (Ensemble)")
            print(f"  Total outliers: {result['total_outliers']} ({result['outlier_rate']:.2f}%)")
            print(f"  High confidence (3/3 methods): {result['high_confidence_outliers']}")
            if result['outlier_rate'] > 3.0:
                print("  ⚠️  WARNING: Outlier rate >3% - check data source")
        
        return result
    
    def test_benfords_law(self, variable: str = 'sales') -> Dict:
        """
        Benford's Law Test for fraud detection
        
        理論: 自然発生データでは、先頭桁が特定の分布に従う:
        P(first digit = d) = log₁₀(1 + 1/d)
        
        この分布からの逸脱はデータ操作を示唆する可能性がある
        
        Parameters:
        -----------
        variable : str
            テスト対象変数（デフォルト: sales）
        
        Returns:
        --------
        result : dict
            カイ二乗検定結果と観測/期待頻度
        """
        # 変数候補を探索
        possible_vars = ['sales', 'sale', 'total_assets', 'at', 'revenue', 'assets']
        test_var = None
        
        for var in possible_vars:
            if var in self.df.columns:
                test_var = var
                break
        
        if test_var is None:
            return {'error': f'No suitable variable found for Benford test'}
        
        data = self.df[test_var].dropna()
        data = data[data > 0]  # Positive values only
        
        if len(data) < 100:
            return {'error': 'Sample too small for Benford test (n<100)'}
        
        # Extract first digit
        first_digits = data.apply(lambda x: int(str(abs(x)).replace('.', '')[0]))
        
        # Observed frequencies
        observed = first_digits.value_counts().sort_index()
        
        # Expected frequencies (Benford's Law)
        expected_probs = {d: np.log10(1 + 1/d) for d in range(1, 10)}
        expected = pd.Series({d: expected_probs[d] * len(first_digits) for d in range(1, 10)})
        
        # Chi-square test
        chi2_stat, p_value = stats.chisquare(observed, expected[observed.index])
        
        result = {
            'variable_tested': test_var,
            'sample_size': len(first_digits),
            'chi2_statistic': float(chi2_stat),
            'p_value': float(p_value),
            'conforms_to_benford': p_value > 0.05,
            'observed': observed.to_dict(),
            'expected': {k: round(v, 1) for k, v in expected.to_dict().items()}
        }
        
        if self.verbose:
            print(f"\n[2/7] Benford's Law Test ({test_var})")
            print(f"  χ² = {chi2_stat:.2f}, p = {p_value:.4f}")
            if p_value < 0.05:
                print("  ⚠️  WARNING: Significant deviation from Benford's Law")
                print("     Possible data manipulation or unusual generation process")
            else:
                print("  ✓ Data conforms to Benford's Law")
        
        return result
    
    def detect_regression_anomalies(self, dependent_var: str = 'roa',
                                   predictors: Optional[List[str]] = None) -> Dict:
        """
        回帰ベースの異常検出
        
        期待値から大きく外れる観測値を検出
        
        Parameters:
        -----------
        dependent_var : str
            従属変数
        predictors : list of str, optional
            予測変数（デフォルト: log_assets, leverage, age）
        
        Returns:
        --------
        result : dict
            異常検出結果
        """
        # 変数候補
        dep_candidates = ['roa', 'roe', 'return_on_assets', 'profit_margin']
        dep_var = None
        for var in dep_candidates:
            if var in self.df.columns:
                dep_var = var
                break
        
        if dep_var is None:
            return {'error': 'No suitable dependent variable found'}
        
        if predictors is None:
            # デフォルト予測変数
            pred_candidates = [
                ['log_assets', 'leverage', 'age'],
                ['log_assets', 'leverage'],
                ['log_assets'],
                ['total_assets']
            ]
            
            for pred_set in pred_candidates:
                if all(p in self.df.columns for p in pred_set):
                    predictors = pred_set
                    break
        
        if predictors is None or not predictors:
            return {'error': 'No valid predictors found'}
        
        # Prepare data
        data = self.df[[dep_var] + predictors].dropna()
        
        if len(data) < 50:
            return {'error': 'Insufficient observations for regression (n<50)'}
        
        y = data[dep_var]
        X = data[predictors]
        
        # Add constant
        X = X.copy()
        X['const'] = 1
        
        # OLS regression
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predictions and residuals
        predictions = model.predict(X)
        residuals = y - predictions
        
        # Standardized residuals
        std_residuals = (residuals - residuals.mean()) / residuals.std()
        
        # Anomalies: |standardized residual| > 3
        anomalies = np.abs(std_residuals) > 3
        
        self.df['regression_residual'] = np.nan
        self.df.loc[data.index, 'regression_residual'] = residuals
        self.df['anomaly_flag'] = 0
        self.df.loc[data.index[anomalies], 'anomaly_flag'] = 1
        
        result = {
            'dependent_variable': dep_var,
            'predictors': predictors,
            'total_anomalies': int(anomalies.sum()),
            'anomaly_rate': float(anomalies.sum() / len(data) * 100),
            'r_squared': float(model.score(X, y)),
            'max_residual': float(np.abs(residuals).max())
        }
        
        if self.verbose:
            print(f"\n[3/7] Regression-based Anomaly Detection")
            print(f"  Model: {dep_var} ~ {' + '.join(predictors)}")
            print(f"  R² = {result['r_squared']:.3f}")
            print(f"  Anomalies: {result['total_anomalies']} ({result['anomaly_rate']:.2f}%)")
        
        return result
    
    def detect_structural_breaks(self, variable: str = 'roa',
                                 min_segment_size: int = 30) -> Dict:
        """
        構造的ブレークの検出（Chow test）
        
        時系列データにおける構造的変化を検出
        
        Parameters:
        -----------
        variable : str
            テスト対象変数
        min_segment_size : int
            最小セグメントサイズ
        
        Returns:
        --------
        result : dict
            検出されたブレーク
        """
        # 変数候補
        var_candidates = ['roa', 'roe', 'sales', 'sale', 'total_assets']
        test_var = None
        for var in var_candidates:
            if var in self.df.columns:
                test_var = var
                break
        
        if test_var is None:
            return {'error': 'No suitable variable found'}
        
        if self.time_var not in self.df.columns:
            return {'error': 'Time variable not found'}
        
        # Sort by time
        data = self.df[[self.time_var, test_var]].dropna().sort_values(self.time_var)
        
        if len(data) < min_segment_size * 2:
            return {'error': 'Insufficient data for structural break detection'}
        
        # Test for break at each potential breakpoint
        breaks_detected = []
        
        for t in range(min_segment_size, len(data) - min_segment_size):
            # Split sample
            segment1 = data.iloc[:t]
            segment2 = data.iloc[t:]
            
            # F-test for equality of means
            try:
                f_stat, p_value = stats.f_oneway(
                    segment1[test_var],
                    segment2[test_var]
                )
                
                if p_value < 0.01:  # Bonferroni correction recommended
                    breaks_detected.append({
                        'time': int(data.iloc[t][self.time_var]),
                        'f_statistic': float(f_stat),
                        'p_value': float(p_value)
                    })
            except:
                continue
        
        result = {
            'variable_tested': test_var,
            'breaks_detected': len(breaks_detected),
            'break_points': breaks_detected[:5]  # Top 5
        }
        
        if self.verbose:
            print(f"\n[4/7] Structural Break Detection ({test_var})")
            if breaks_detected:
                print(f"  ⚠️  {len(breaks_detected)} structural breaks detected")
                for bp in breaks_detected[:3]:
                    print(f"     Year {bp['time']}: F={bp['f_statistic']:.2f}, p={bp['p_value']:.4f}")
            else:
                print("  ✓ No significant structural breaks detected")
        
        return result
    
    def detect_influential_observations(self, dependent_var: str = 'roa',
                                       predictors: Optional[List[str]] = None) -> Dict:
        """
        影響力の大きい観測値の検出（Cook's distance）
        
        Parameters:
        -----------
        dependent_var : str
            従属変数
        predictors : list of str, optional
            予測変数
        
        Returns:
        --------
        result : dict
            影響力のある観測値の情報
        """
        # 変数候補
        dep_candidates = ['roa', 'roe', 'return_on_assets']
        dep_var = None
        for var in dep_candidates:
            if var in self.df.columns:
                dep_var = var
                break
        
        if dep_var is None:
            return {'error': 'No suitable dependent variable found'}
        
        if predictors is None:
            pred_candidates = [
                ['log_assets', 'leverage'],
                ['log_assets'],
                ['total_assets']
            ]
            
            for pred_set in pred_candidates:
                if all(p in self.df.columns for p in pred_set):
                    predictors = pred_set
                    break
        
        if not predictors:
            return {'error': 'No valid predictors found'}
        
        # Prepare data
        data = self.df[[dep_var] + predictors].dropna()
        
        if len(data) < 30:
            return {'error': 'Insufficient data (n<30)'}
        
        # Import statsmodels for Cook's distance
        try:
            import statsmodels.api as sm
            from statsmodels.stats.outliers_influence import OLSInfluence
        except ImportError:
            return {'error': 'statsmodels not installed'}
        
        y = data[dep_var]
        X = sm.add_constant(data[predictors])
        
        # Fit model
        try:
            model = sm.OLS(y, X).fit()
            influence = OLSInfluence(model)
            
            # Cook's distance
            cooks_d = influence.cooks_distance[0]
            
            # Threshold: 4/n
            threshold = 4 / len(data)
            influential = cooks_d > threshold
            
            self.df['cooks_distance'] = np.nan
            self.df.loc[data.index, 'cooks_distance'] = cooks_d
            self.df['influential_flag'] = 0
            self.df.loc[data.index[influential], 'influential_flag'] = 1
            
            result = {
                'total_influential': int(influential.sum()),
                'influence_rate': float(influential.sum() / len(data) * 100),
                'threshold': float(threshold),
                'max_cooks_d': float(cooks_d.max())
            }
            
            if self.verbose:
                print(f"\n[5/7] Influential Observations Detection")
                print(f"  Influential obs: {result['total_influential']} ({result['influence_rate']:.2f}%)")
                print(f"  Cook's D threshold: {result['threshold']:.4f}")
            
            return result
            
        except Exception as e:
            return {'error': f'Cook\'s distance calculation failed: {str(e)}'}
    
    def test_publication_bias(self, effect_var: str = 'effect_size',
                             se_var: str = 'standard_error') -> Dict:
        """
        Publication bias test (Egger's test)
        
        メタ分析や複数研究の統合時に使用
        
        Parameters:
        -----------
        effect_var : str
            効果サイズ変数
        se_var : str
            標準誤差変数
        
        Returns:
        --------
        result : dict
            出版バイアステスト結果
        """
        if effect_var not in self.df.columns or se_var not in self.df.columns:
            return {'error': 'Effect size or standard error variable not found'}
        
        data = self.df[[effect_var, se_var]].dropna()
        
        if len(data) < 10:
            return {'error': 'Insufficient data for publication bias test (n<10)'}
        
        # Egger's test
        precision = 1 / data[se_var]
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            precision, data[effect_var]
        )
        
        result = {
            'intercept': float(intercept),
            'p_value': float(p_value),
            'bias_detected': p_value < 0.10,
            'interpretation': 'Publication bias likely' if p_value < 0.10 else 'No evidence of publication bias'
        }
        
        if self.verbose:
            print(f"\n[6/7] Publication Bias Test (Egger's test)")
            print(f"  Intercept = {intercept:.4f}, p = {p_value:.4f}")
            if p_value < 0.10:
                print("  ⚠️  WARNING: Publication bias detected")
            else:
                print("  ✓ No evidence of publication bias")
        
        return result
    
    def test_sample_selection_bias(self) -> Dict:
        """
        Sample selection bias test
        
        生存バイアス、脱落バイアスの検出
        
        Returns:
        --------
        result : dict
            サンプル選択バイアスの評価
        """
        if self.firm_id not in self.df.columns or self.time_var not in self.df.columns:
            return {'error': 'Panel structure required'}
        
        # Firms by year
        firms_by_year = self.df.groupby(self.time_var)[self.firm_id].nunique()
        
        # Attrition rate
        max_firms = firms_by_year.max()
        min_firms = firms_by_year.min()
        attrition_rate = (max_firms - min_firms) / max_firms * 100
        
        # Firms present in all years (balanced)
        all_years = self.df[self.time_var].unique()
        firm_year_counts = self.df.groupby(self.firm_id)[self.time_var].nunique()
        balanced_firms = (firm_year_counts == len(all_years)).sum()
        balance_rate = balanced_firms / len(firm_year_counts) * 100
        
        result = {
            'total_firms': int(self.df[self.firm_id].nunique()),
            'balanced_firms': int(balanced_firms),
            'balance_rate': float(balance_rate),
            'attrition_rate': float(attrition_rate),
            'firms_by_year': firms_by_year.to_dict(),
            'warning': attrition_rate > 30
        }
        
        if self.verbose:
            print(f"\n[7/7] Sample Selection Bias Test")
            print(f"  Balanced panel firms: {balanced_firms} ({balance_rate:.1f}%)")
            print(f"  Attrition rate: {attrition_rate:.1f}%")
            if attrition_rate > 30:
                print("  ⚠️  WARNING: High attrition rate may indicate selection bias")
        
        return result
    
    def generate_html_report(self, output_path: str = 'qa_report_advanced.html'):
        """
        詳細なHTMLレポートを生成
        
        Parameters:
        -----------
        output_path : str
            出力ファイルパス
        """
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Advanced Quality Assurance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
                .metric {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .warning {{ background: #ffebee; border-left: 4px solid #f44336; }}
                .success {{ background: #e8f5e9; border-left: 4px solid #4caf50; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
            </style>
        </head>
        <body>
            <h1>Advanced Quality Assurance Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <h2>1. Multivariate Outlier Detection</h2>
            <div class="metric">
                <p><strong>Total Outliers:</strong> {self.qa_report.get('outliers', {}).get('total_outliers', 'N/A')}</p>
                <p><strong>Outlier Rate:</strong> {self.qa_report.get('outliers', {}).get('outlier_rate', 'N/A'):.2f}%</p>
                <p><strong>High Confidence:</strong> {self.qa_report.get('outliers', {}).get('high_confidence_outliers', 'N/A')}</p>
            </div>
            
            <h2>2. Benford's Law Test</h2>
            <div class="metric {'success' if self.qa_report.get('benfords_law', {}).get('conforms_to_benford', False) else 'warning'}">
                <p><strong>Chi-square:</strong> {self.qa_report.get('benfords_law', {}).get('chi2_statistic', 'N/A'):.2f}</p>
                <p><strong>P-value:</strong> {self.qa_report.get('benfords_law', {}).get('p_value', 'N/A'):.4f}</p>
                <p><strong>Result:</strong> {'PASS' if self.qa_report.get('benfords_law', {}).get('conforms_to_benford', False) else 'WARNING'}</p>
            </div>
            
            <h2>3. Regression Anomalies</h2>
            <div class="metric">
                <p><strong>Anomalies Detected:</strong> {self.qa_report.get('anomalies', {}).get('total_anomalies', 'N/A')}</p>
                <p><strong>Model R²:</strong> {self.qa_report.get('anomalies', {}).get('r_squared', 'N/A'):.3f}</p>
            </div>
            
            <h2>4. Structural Breaks</h2>
            <div class="metric {'warning' if self.qa_report.get('structural_breaks', {}).get('breaks_detected', 0) > 0 else 'success'}">
                <p><strong>Breaks Detected:</strong> {self.qa_report.get('structural_breaks', {}).get('breaks_detected', 'N/A')}</p>
            </div>
            
            <h2>5. Influential Observations</h2>
            <div class="metric">
                <p><strong>Influential Observations:</strong> {self.qa_report.get('influential_obs', {}).get('total_influential', 'N/A')}</p>
                <p><strong>Influence Rate:</strong> {self.qa_report.get('influential_obs', {}).get('influence_rate', 'N/A'):.2f}%</p>
            </div>
            
            <h2>6. Sample Selection Bias</h2>
            <div class="metric {'warning' if self.qa_report.get('selection_bias', {}).get('warning', False) else 'success'}">
                <p><strong>Total Firms:</strong> {self.qa_report.get('selection_bias', {}).get('total_firms', 'N/A')}</p>
                <p><strong>Balanced Panel:</strong> {self.qa_report.get('selection_bias', {}).get('balance_rate', 'N/A'):.1f}%</p>
                <p><strong>Attrition Rate:</strong> {self.qa_report.get('selection_bias', {}).get('attrition_rate', 'N/A'):.1f}%</p>
            </div>
            
            <h2>Summary</h2>
            <div class="metric">
                <p>Quality assurance checks completed successfully.</p>
                <p>Review warnings and investigate flagged observations.</p>
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        if self.verbose:
            print(f"\n✓ HTML report saved: {output_path}")


# ============================================================================
# Statistical Power Analysis & Sample Size Design
# ============================================================================

class SampleSizeCalculator:
    """
    統計的検出力に基づくサンプルサイズ設計
    
    References:
    - Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences.
    - Button, K. S., et al. (2013). Power failure: why small sample size 
      undermines the reliability of neuroscience. Nature Reviews Neuroscience.
    """
    
    def __init__(self):
        self.effect_size_benchmarks = {
            'small': 0.2,      # Cohen's d = 0.2
            'medium': 0.5,     # Cohen's d = 0.5
            'large': 0.8       # Cohen's d = 0.8
        }
    
    def t_test_sample_size(self, effect_size, alpha=0.05, power=0.80, 
                          two_sided=True):
        """
        t検定のサンプルサイズ計算
        
        Parameters:
        -----------
        effect_size : float or str
            効果サイズ（Cohen's d）または 'small'/'medium'/'large'
        alpha : float
            有意水準（デフォルト: 0.05）
        power : float
            検出力（デフォルト: 0.80 = 80%）
        two_sided : bool
            両側検定か片側検定か
        
        Returns:
        --------
        dict : サンプルサイズと詳細情報
        """
        try:
            from statsmodels.stats.power import TTestIndPower
        except ImportError:
            return {'error': 'statsmodels required for power analysis'}
        
        if isinstance(effect_size, str):
            effect_size = self.effect_size_benchmarks[effect_size]
        
        analysis = TTestIndPower()
        n_per_group = analysis.solve_power(
            effect_size=effect_size,
            alpha=alpha,
            power=power,
            alternative='two-sided' if two_sided else 'one-sided'
        )
        
        return {
            'n_per_group': int(np.ceil(n_per_group)),
            'total_n': int(np.ceil(n_per_group * 2)),
            'effect_size': effect_size,
            'alpha': alpha,
            'power': power,
            'interpretation': self._interpret_sample_size(n_per_group)
        }
    
    def regression_sample_size(self, num_predictors, expected_r2, 
                               alpha=0.05, power=0.80):
        """
        重回帰分析のサンプルサイズ計算
        
        Rule of thumb: N ≥ 104 + k (Green, 1991)
        Statistical power approach: より厳密な計算
        
        Parameters:
        -----------
        num_predictors : int
            独立変数の数
        expected_r2 : float
            予想されるR² (0-1)
        alpha : float
            有意水準
        power : float
            検出力
        
        Returns:
        --------
        dict : 必要サンプルサイズ
        """
        # Green (1991) の経験則
        rule_of_thumb_n = 104 + num_predictors
        
        # 統計的検出力に基づく計算
        # f² = R² / (1 - R²)
        f2 = expected_r2 / (1 - expected_r2)
        
        try:
            from statsmodels.stats.power import FTestPower
            power_analysis = FTestPower()
            
            statistical_n = power_analysis.solve_power(
                effect_size=f2,
                df_num=num_predictors,
                alpha=alpha,
                power=power
            )
            
            recommended_n = max(rule_of_thumb_n, int(np.ceil(statistical_n)))
            
            return {
                'rule_of_thumb_n': rule_of_thumb_n,
                'statistical_power_n': int(np.ceil(statistical_n)),
                'recommended_n': recommended_n,
                'num_predictors': num_predictors,
                'expected_r2': expected_r2,
                'notes': f"Green's rule: N≥104+k={rule_of_thumb_n}, Statistical power: {int(np.ceil(statistical_n))}"
            }
        except ImportError:
            return {
                'rule_of_thumb_n': rule_of_thumb_n,
                'recommended_n': rule_of_thumb_n,
                'notes': 'Using rule of thumb only (statsmodels not available)'
            }
    
    def panel_data_sample_size(self, num_firms, num_periods, 
                              effect_size, alpha=0.05, power=0.80):
        """
        パネルデータ分析のサンプルサイズ設計
        
        考慮事項:
        - Cluster-robust標準誤差による検出力低下
        - 固定効果モデルの自由度調整
        """
        # 基本的なサンプルサイズ（クラスタリングなし）
        base_result = self.t_test_sample_size(effect_size, alpha, power)
        base_n = base_result['total_n']
        
        # Design effect（クラスタリングによる増幅）
        # Moulton (1990) の近似
        avg_cluster_size = num_periods
        icc = 0.05  # Intraclass correlation（仮定）
        design_effect = 1 + (avg_cluster_size - 1) * icc
        
        adjusted_firms = int(np.ceil(base_n / num_periods * design_effect))
        
        return {
            'required_firms': adjusted_firms,
            'required_periods': num_periods,
            'total_observations': adjusted_firms * num_periods,
            'design_effect': design_effect,
            'notes': f"Cluster (firm) count adjusted by {design_effect:.2f}x"
        }
    
    def _interpret_sample_size(self, n):
        """サンプルサイズの解釈"""
        if n < 30:
            return "Very small - pilot only"
        elif n < 100:
            return "Small - check robustness"
        elif n < 500:
            return "Medium - adequate for most analyses"
        else:
            return "Large - high statistical power"


# ============================================================================
# Main execution
# ============================================================================

if __name__ == '__main__':
    print("Advanced Quality Assurance Module")
    print("=" * 70)
    print("Available classes:")
    print("  - AdvancedQualityAssurance")
    print("  - SampleSizeCalculator")
    print("\nImport these classes in your analysis scripts.")
