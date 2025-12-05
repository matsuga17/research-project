"""
US Corporate Analytics - データ品質保証モジュール

このモジュールは財務データの品質を検証します。
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import warnings


class BenfordTest:
    """Benford's Lawによるデータ品質検証"""
    
    def __init__(self, confidence_level: float = 0.05):
        """
        初期化
        
        Parameters:
            confidence_level: 有意水準（デフォルト: 0.05）
        """
        self.confidence_level = confidence_level
        
        # Benford's Lawの期待分布（第1桁）
        self.expected_dist = {
            1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079,
            6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
        }
    
    def extract_first_digit(self, number: float) -> Optional[int]:
        """
        数値の第1桁を抽出
        
        Parameters:
            number: 数値
            
        Returns:
            第1桁（1-9）、無効な場合はNone
        """
        if pd.isna(number) or number == 0:
            return None
        
        # 絶対値を取る
        abs_num = abs(number)
        
        # 科学的記数法で表現
        str_num = f"{abs_num:.15e}"
        
        # 第1桁を抽出
        first_digit = int(str_num[0])
        
        return first_digit if 1 <= first_digit <= 9 else None
    
    def test_distribution(self, data: pd.Series) -> Dict:
        """
        データがBenford's Lawに従うかテスト
        
        Parameters:
            data: テストするデータ（Series）
            
        Returns:
            テスト結果の辞書
        """
        # 第1桁を抽出
        first_digits = data.apply(self.extract_first_digit).dropna()
        
        if len(first_digits) < 30:
            warnings.warn("サンプルサイズが小さいため、結果が信頼できない可能性があります")
        
        # 観測分布を計算
        observed_counts = first_digits.value_counts().sort_index()
        total = len(first_digits)
        observed_dist = observed_counts / total
        
        # 期待分布と比較
        expected_counts = pd.Series(self.expected_dist) * total
        
        # カイ二乗検定
        chi_square = 0
        for digit in range(1, 10):
            observed = observed_counts.get(digit, 0)
            expected = expected_counts.get(digit, 0)
            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected
        
        # p値を計算（自由度8）
        p_value = 1 - stats.chi2.cdf(chi_square, df=8)
        
        # 判定
        passes = p_value > self.confidence_level
        
        return {
            'chi_square': chi_square,
            'p_value': p_value,
            'passes': passes,
            'confidence_level': self.confidence_level,
            'sample_size': total,
            'observed_distribution': observed_dist.to_dict(),
            'expected_distribution': self.expected_dist
        }
    
    def test_multiple_variables(self, data: pd.DataFrame,
                               variables: List[str]) -> pd.DataFrame:
        """
        複数の変数をテスト
        
        Parameters:
            data: テストするデータ（DataFrame）
            variables: テストする変数名のリスト
            
        Returns:
            テスト結果のDataFrame
        """
        results = []
        
        for var in variables:
            if var not in data.columns:
                print(f"Warning: {var} not found in data")
                continue
            
            result = self.test_distribution(data[var])
            results.append({
                'variable': var,
                'chi_square': result['chi_square'],
                'p_value': result['p_value'],
                'passes': result['passes'],
                'sample_size': result['sample_size']
            })
        
        return pd.DataFrame(results)


class OutlierDetector:
    """外れ値検出クラス"""
    
    def __init__(self, method: str = 'mahalanobis'):
        """
        初期化
        
        Parameters:
            method: 検出方法（'iqr', 'zscore', 'mahalanobis'）
        """
        self.method = method
    
    def detect_iqr(self, data: pd.Series, 
                   multiplier: float = 1.5) -> pd.Series:
        """
        IQR法で外れ値を検出
        
        Parameters:
            data: データ（Series）
            multiplier: IQRの倍数（デフォルト: 1.5）
            
        Returns:
            外れ値フラグ（True=外れ値）
        """
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        is_outlier = (data < lower_bound) | (data > upper_bound)
        
        return is_outlier
    
    def detect_zscore(self, data: pd.Series,
                     threshold: float = 3.0) -> pd.Series:
        """
        Z-score法で外れ値を検出
        
        Parameters:
            data: データ（Series）
            threshold: 閾値（デフォルト: 3.0標準偏差）
            
        Returns:
            外れ値フラグ（True=外れ値）
        """
        z_scores = np.abs(stats.zscore(data.dropna()))
        is_outlier = pd.Series(False, index=data.index)
        is_outlier[data.notna()] = z_scores > threshold
        
        return is_outlier
    
    def detect_mahalanobis(self, data: pd.DataFrame,
                          threshold: float = 3.0) -> pd.Series:
        """
        Mahalanobis距離で外れ値を検出（多変量）
        
        Parameters:
            data: データ（DataFrame）
            threshold: 閾値（デフォルト: 3.0）
            
        Returns:
            外れ値フラグ（True=外れ値）
        """
        # 欠損値を除外
        clean_data = data.dropna()
        
        if len(clean_data) < data.shape[1] + 1:
            warnings.warn("サンプルサイズが不足しています")
            return pd.Series(False, index=data.index)
        
        # 平均と共分散行列
        mean = clean_data.mean()
        cov = clean_data.cov()
        
        try:
            # 共分散行列の逆行列
            inv_cov = np.linalg.inv(cov)
            
            # Mahalanobis距離を計算
            distances = []
            for idx, row in clean_data.iterrows():
                diff = row - mean
                distance = np.sqrt(diff.dot(inv_cov).dot(diff))
                distances.append(distance)
            
            distances = pd.Series(distances, index=clean_data.index)
            
            # 外れ値判定
            is_outlier = pd.Series(False, index=data.index)
            is_outlier[clean_data.index] = distances > threshold
            
            return is_outlier
            
        except np.linalg.LinAlgError:
            warnings.warn("共分散行列が特異です。IQR法にフォールバック")
            return self.detect_iqr(data.iloc[:, 0])
    
    def detect(self, data: pd.DataFrame,
              variables: Optional[List[str]] = None) -> pd.DataFrame:
        """
        外れ値を検出
        
        Parameters:
            data: データ（DataFrame）
            variables: 検出対象の変数（Noneの場合は全変数）
            
        Returns:
            外れ値フラグのDataFrame
        """
        if variables is None:
            variables = data.select_dtypes(include=[np.number]).columns.tolist()
        
        outlier_flags = pd.DataFrame(index=data.index)
        
        if self.method == 'mahalanobis':
            # 多変量検出
            outlier_flags['is_outlier'] = self.detect_mahalanobis(data[variables])
        else:
            # 単変量検出
            for var in variables:
                if self.method == 'iqr':
                    outlier_flags[f'{var}_outlier'] = self.detect_iqr(data[var])
                elif self.method == 'zscore':
                    outlier_flags[f'{var}_outlier'] = self.detect_zscore(data[var])
            
            # 総合判定（いずれかの変数で外れ値）
            outlier_flags['is_outlier'] = outlier_flags.any(axis=1)
        
        return outlier_flags


class DataQualityChecker:
    """データ品質総合チェッカー"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初期化
        
        Parameters:
            config: 設定辞書
        """
        self.config = config or {}
        self.benford_test = BenfordTest()
        self.outlier_detector = OutlierDetector()
    
    def check_completeness(self, data: pd.DataFrame) -> Dict:
        """
        データの完全性をチェック
        
        Parameters:
            data: チェックするデータ
            
        Returns:
            完全性レポート
        """
        total_cells = data.size
        missing_cells = data.isna().sum().sum()
        missing_ratio = missing_cells / total_cells
        
        # 変数ごとの欠損率
        missing_by_var = data.isna().sum() / len(data)
        
        # 行ごとの欠損率
        missing_by_row = data.isna().sum(axis=1) / len(data.columns)
        
        return {
            'total_cells': total_cells,
            'missing_cells': missing_cells,
            'missing_ratio': missing_ratio,
            'missing_by_variable': missing_by_var.to_dict(),
            'rows_with_missing': (missing_by_row > 0).sum(),
            'complete_rows': (missing_by_row == 0).sum()
        }
    
    def check_consistency(self, data: pd.DataFrame,
                         rules: List[Dict]) -> List[Dict]:
        """
        データの整合性をチェック
        
        Parameters:
            data: チェックするデータ
            rules: 検証ルールのリスト
                例: [{'type': 'balance', 'assets': 'total_assets', 
                      'liabilities': 'total_liabilities', 
                      'equity': 'stockholders_equity'}]
            
        Returns:
            整合性チェック結果のリスト
        """
        results = []
        
        for rule in rules:
            if rule['type'] == 'balance':
                # 貸借対照表の均衡チェック
                assets = data[rule['assets']]
                liabilities = data[rule['liabilities']]
                equity = data[rule['equity']]
                
                diff = assets - (liabilities + equity)
                tolerance = assets * 0.01  # 1%の許容誤差
                
                violations = abs(diff) > tolerance
                
                results.append({
                    'rule_type': 'balance',
                    'violations': violations.sum(),
                    'max_diff': diff.abs().max(),
                    'passed': violations.sum() == 0
                })
            
            elif rule['type'] == 'non_negative':
                # 非負制約チェック
                var = rule['variable']
                violations = data[var] < 0
                
                results.append({
                    'rule_type': 'non_negative',
                    'variable': var,
                    'violations': violations.sum(),
                    'passed': violations.sum() == 0
                })
        
        return results
    
    def check_accuracy(self, data: pd.DataFrame,
                      financial_variables: List[str]) -> Dict:
        """
        データの正確性をチェック（Benford's Law）
        
        Parameters:
            data: チェックするデータ
            financial_variables: 財務変数のリスト
            
        Returns:
            正確性チェック結果
        """
        benford_results = self.benford_test.test_multiple_variables(
            data, financial_variables
        )
        
        pass_rate = benford_results['passes'].mean()
        
        return {
            'benford_test_results': benford_results.to_dict('records'),
            'pass_rate': pass_rate,
            'overall_pass': pass_rate >= 0.8  # 80%以上合格を基準
        }
    
    def check_outliers(self, data: pd.DataFrame,
                      variables: List[str]) -> Dict:
        """
        外れ値をチェック
        
        Parameters:
            data: チェックするデータ
            variables: チェックする変数のリスト
            
        Returns:
            外れ値チェック結果
        """
        outlier_flags = self.outlier_detector.detect(data, variables)
        
        outlier_count = outlier_flags['is_outlier'].sum()
        outlier_ratio = outlier_count / len(data)
        
        return {
            'outlier_count': outlier_count,
            'outlier_ratio': outlier_ratio,
            'outlier_indices': data[outlier_flags['is_outlier']].index.tolist()
        }
    
    def comprehensive_check(self, data: pd.DataFrame,
                           financial_variables: Optional[List[str]] = None,
                           consistency_rules: Optional[List[Dict]] = None) -> Dict:
        """
        包括的なデータ品質チェック
        
        Parameters:
            data: チェックするデータ
            financial_variables: 財務変数のリスト
            consistency_rules: 整合性ルールのリスト
            
        Returns:
            総合的な品質レポート
        """
        report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'data_shape': data.shape
        }
        
        # 完全性チェック
        report['completeness'] = self.check_completeness(data)
        
        # 整合性チェック
        if consistency_rules:
            report['consistency'] = self.check_consistency(data, consistency_rules)
        
        # 正確性チェック（Benford's Law）
        if financial_variables:
            report['accuracy'] = self.check_accuracy(data, financial_variables)
        
        # 外れ値チェック
        if financial_variables:
            report['outliers'] = self.check_outliers(data, financial_variables)
        
        # 総合評価
        scores = []
        
        # 完全性スコア
        completeness_score = 1 - report['completeness']['missing_ratio']
        scores.append(completeness_score)
        
        # 正確性スコア
        if 'accuracy' in report:
            scores.append(1 if report['accuracy']['overall_pass'] else 0.5)
        
        # 外れ値スコア
        if 'outliers' in report:
            outlier_penalty = min(report['outliers']['outlier_ratio'] * 2, 1)
            scores.append(1 - outlier_penalty)
        
        overall_score = np.mean(scores) * 100
        
        report['overall_score'] = overall_score
        
        if overall_score >= 90:
            report['overall_rating'] = "Excellent"
        elif overall_score >= 75:
            report['overall_rating'] = "Good"
        elif overall_score >= 60:
            report['overall_rating'] = "Fair"
        else:
            report['overall_rating'] = "Poor"
        
        return report
