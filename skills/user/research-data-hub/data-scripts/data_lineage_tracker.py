"""
データ系譜追跡システム (Data Lineage Tracker)
===========================================
データ収集から最終データセットまでの完全な系譜を記録し、再現性を担保

トップジャーナル（JF, JFE, RFS）の再現性要件に準拠

Author: Corporate Research Data Hub
Version: 2.0
Date: 2025-10-31
"""

import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, List, Any
import pandas as pd
import numpy as np


class DataLineageTracker:
    """
    データ収集から最終データセットまでの完全な系譜を記録
    
    **再現性担保のための必須要素**:
    1. データソース情報（URL、バージョン、アクセス日時）
    2. 変換処理の完全な記録（コード、パラメータ）
    3. 品質チェック結果
    4. 最終データセットのメタデータ
    
    American Economic Association (AEA) Data and Code Availability Policy準拠
    """
    
    def __init__(self, project_name: str, project_id: Optional[str] = None):
        """
        Parameters:
        -----------
        project_name : str
            プロジェクト名
        project_id : str, optional
            プロジェクト識別子（自動生成可能）
        """
        self.project_name = project_name
        self.project_id = project_id or self._generate_project_id()
        
        self.lineage = {
            'project_name': project_name,
            'project_id': self.project_id,
            'created_at': datetime.now().isoformat(),
            'data_sources': [],
            'transformations': [],
            'quality_checks': [],
            'final_dataset': {},
            'environment': self._capture_environment()
        }
    
    def _generate_project_id(self) -> str:
        """プロジェクト識別子を自動生成"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.project_name.replace(' ', '_')}_{timestamp}"
    
    def _capture_environment(self) -> dict:
        """実行環境情報を記録"""
        import platform
        import sys
        
        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'processor': platform.processor(),
            'pandas_version': pd.__version__,
            'numpy_version': np.__version__
        }
    
    def log_data_source(self, source_name: str, url: str, access_date: str,
                       version: Optional[str] = None, 
                       credentials_hash: Optional[str] = None,
                       file_hash: Optional[str] = None,
                       notes: Optional[str] = None) -> None:
        """
        データソース情報を記録
        
        Parameters:
        -----------
        source_name : str
            データソース名（例: "Open DART", "EDINET"）
        url : str
            データソースURL
        access_date : str
            アクセス日時（ISO 8601形式推奨）
        version : str, optional
            データソースバージョン
        credentials_hash : str, optional
            認証情報のハッシュ（セキュリティ: 平文保存禁止）
        file_hash : str, optional
            ダウンロードファイルのSHA256ハッシュ
        notes : str, optional
            追加メモ
        
        Examples:
        ---------
        >>> tracker = DataLineageTracker('my_research')
        >>> tracker.log_data_source(
        ...     source_name='Open DART',
        ...     url='https://opendart.fss.or.kr/api/corpCode.xml',
        ...     access_date='2024-10-31T14:30:00',
        ...     version='2024-Q4',
        ...     notes='企業コード一覧取得'
        ... )
        """
        source_entry = {
            'source_name': source_name,
            'url': url,
            'access_date': access_date,
            'version': version,
            'credentials_hash': credentials_hash,
            'file_hash': file_hash,
            'notes': notes,
            'logged_at': datetime.now().isoformat()
        }
        
        self.lineage['data_sources'].append(source_entry)
        print(f"✓ データソース記録: {source_name}")
    
    def log_transformation(self, transformation_name: str, 
                          input_vars: List[str],
                          output_vars: List[str],
                          code_snippet: str,
                          parameters: Optional[Dict[str, Any]] = None,
                          notes: Optional[str] = None) -> None:
        """
        データ変換処理を記録
        
        Parameters:
        -----------
        transformation_name : str
            変換処理名（例: "winsorization", "currency_conversion"）
        input_vars : list of str
            入力変数名リスト
        output_vars : list of str
            出力変数名リスト
        code_snippet : str
            実際に実行したコード（関数呼び出し含む）
        parameters : dict, optional
            パラメータ（例: {'limits': [0.01, 0.99]}）
        notes : str, optional
            処理の説明
        
        Examples:
        ---------
        >>> tracker.log_transformation(
        ...     transformation_name='winsorization',
        ...     input_vars=['roa', 'leverage'],
        ...     output_vars=['roa_winsorized', 'leverage_winsorized'],
        ...     code_snippet='winsorize(df, limits=[0.01, 0.99])',
        ...     parameters={'limits': [0.01, 0.99]}
        ... )
        """
        transformation_entry = {
            'name': transformation_name,
            'inputs': input_vars,
            'outputs': output_vars,
            'code': code_snippet,
            'parameters': parameters or {},
            'notes': notes,
            'logged_at': datetime.now().isoformat()
        }
        
        self.lineage['transformations'].append(transformation_entry)
        print(f"✓ 変換処理記録: {transformation_name}")
    
    def log_quality_check(self, check_name: str, result: Dict[str, Any],
                         passed: bool, notes: Optional[str] = None) -> None:
        """
        品質チェック結果を記録
        
        Parameters:
        -----------
        check_name : str
            チェック名（例: "outlier_detection", "accounting_identity"）
        result : dict
            チェック結果の詳細
        passed : bool
            合格/不合格
        notes : str, optional
            追加メモ
        
        Examples:
        ---------
        >>> tracker.log_quality_check(
        ...     check_name='outlier_detection',
        ...     result={'outliers_found': 23, 'outlier_rate': 1.2},
        ...     passed=True,
        ...     notes='許容範囲内'
        ... )
        """
        quality_check_entry = {
            'check_name': check_name,
            'result': result,
            'passed': passed,
            'notes': notes,
            'logged_at': datetime.now().isoformat()
        }
        
        self.lineage['quality_checks'].append(quality_check_entry)
        status = "✓ 合格" if passed else "✗ 不合格"
        print(f"{status}: {check_name}")
    
    def generate_codebook(self, df: pd.DataFrame, output_path: str,
                         variable_descriptions: Optional[Dict[str, str]] = None) -> dict:
        """
        完全なコードブック生成（AEA準拠）
        
        American Economic Association (AEA) Data and Code Availability Policy準拠
        
        Parameters:
        -----------
        df : DataFrame
            最終データセット
        output_path : str
            コードブック保存先パス（JSON形式）
        variable_descriptions : dict, optional
            変数説明の辞書 {変数名: 説明}
        
        Returns:
        --------
        codebook : dict
            生成されたコードブック
        
        Examples:
        ---------
        >>> descriptions = {
        ...     'roa': 'Return on Assets (純利益 / 総資産)',
        ...     'log_assets': '総資産の自然対数'
        ... }
        >>> tracker.generate_codebook(
        ...     df=final_df,
        ...     output_path='codebook.json',
        ...     variable_descriptions=descriptions
        ... )
        """
        codebook = {
            'project_name': self.project_name,
            'project_id': self.project_id,
            'generated_at': datetime.now().isoformat(),
            'sample_size': len(df),
            'num_variables': len(df.columns),
            'variables': {}
        }
        
        var_desc = variable_descriptions or {}
        
        for col in df.columns:
            var_info = {
                'name': col,
                'type': str(df[col].dtype),
                'description': var_desc.get(col, ''),
                'missing_values': int(df[col].isna().sum()),
                'missing_percentage': float(df[col].isna().sum() / len(df) * 100),
                'unique_values': int(df[col].nunique())
            }
            
            # 数値変数の統計量
            if df[col].dtype in ['float64', 'int64']:
                var_info.update({
                    'mean': float(df[col].mean()) if pd.notna(df[col].mean()) else None,
                    'std': float(df[col].std()) if pd.notna(df[col].std()) else None,
                    'min': float(df[col].min()) if pd.notna(df[col].min()) else None,
                    'max': float(df[col].max()) if pd.notna(df[col].max()) else None,
                    'median': float(df[col].median()) if pd.notna(df[col].median()) else None,
                    'q25': float(df[col].quantile(0.25)) if pd.notna(df[col].quantile(0.25)) else None,
                    'q75': float(df[col].quantile(0.75)) if pd.notna(df[col].quantile(0.75)) else None
                })
            
            codebook['variables'][col] = var_info
        
        # JSON保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(codebook, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ コードブック生成: {output_path}")
        print(f"  サンプルサイズ: {codebook['sample_size']:,}")
        print(f"  変数数: {codebook['num_variables']}")
        
        return codebook
    
    def set_final_dataset_info(self, file_path: str, file_hash: str,
                              sample_size: int, time_period: str,
                              notes: Optional[str] = None) -> None:
        """
        最終データセット情報を設定
        
        Parameters:
        -----------
        file_path : str
            最終データセットのパス
        file_hash : str
            ファイルのSHA256ハッシュ
        sample_size : int
            サンプルサイズ
        time_period : str
            対象期間（例: "2015-2023"）
        notes : str, optional
            追加メモ
        """
        self.lineage['final_dataset'] = {
            'file_path': file_path,
            'file_hash': file_hash,
            'sample_size': sample_size,
            'time_period': time_period,
            'notes': notes,
            'finalized_at': datetime.now().isoformat()
        }
        
        print(f"✓ 最終データセット情報記録: {file_path}")
    
    def export_lineage_report(self, output_path: str) -> None:
        """
        完全な系譜レポートをJSON形式で出力
        
        Parameters:
        -----------
        output_path : str
            出力先パス
        
        Examples:
        ---------
        >>> tracker.export_lineage_report('data_lineage_report.json')
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.lineage, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*70}")
        print(f"データ系譜レポート生成完了")
        print(f"{'='*70}")
        print(f"プロジェクト: {self.project_name}")
        print(f"データソース数: {len(self.lineage['data_sources'])}")
        print(f"変換処理数: {len(self.lineage['transformations'])}")
        print(f"品質チェック数: {len(self.lineage['quality_checks'])}")
        print(f"出力先: {output_path}")
        print(f"{'='*70}\n")
    
    def compute_file_hash(self, file_path: str, algorithm: str = 'sha256') -> str:
        """
        ファイルのハッシュ値を計算
        
        Parameters:
        -----------
        file_path : str
            ファイルパス
        algorithm : str
            ハッシュアルゴリズム（'sha256', 'md5'）
        
        Returns:
        --------
        hash_value : str
            ハッシュ値（16進数文字列）
        
        Examples:
        ---------
        >>> hash_val = tracker.compute_file_hash('data.csv')
        >>> print(f"SHA256: {hash_val}")
        """
        if algorithm == 'sha256':
            hasher = hashlib.sha256()
        elif algorithm == 'md5':
            hasher = hashlib.md5()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        with open(file_path, 'rb') as f:
            # メモリ効率的な読み込み
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        
        return hasher.hexdigest()


# ============================================================================
# 使用例
# ============================================================================

if __name__ == "__main__":
    # デモンストレーション
    print("=" * 70)
    print("Data Lineage Tracker - デモンストレーション")
    print("=" * 70)
    
    # トラッカー初期化
    tracker = DataLineageTracker('asian_roa_determinants')
    
    # データソース記録
    tracker.log_data_source(
        source_name='Open DART',
        url='https://opendart.fss.or.kr/api/list.json',
        access_date='2024-10-31T10:00:00',
        version='2024-Q4'
    )
    
    # 変換処理記録
    tracker.log_transformation(
        transformation_name='通貨換算',
        input_vars=['sales_krw', 'exchange_rate'],
        output_vars=['sales_usd'],
        code_snippet='sales_usd = sales_krw / exchange_rate',
        parameters={'exchange_rate_source': 'Bank of Korea'}
    )
    
    # 品質チェック記録
    tracker.log_quality_check(
        check_name='欠損値チェック',
        result={'missing_rate': 2.3},
        passed=True,
        notes='許容範囲内（<5%）'
    )
    
    # サンプルデータでコードブック生成
    sample_df = pd.DataFrame({
        'roa': np.random.normal(0.05, 0.03, 1000),
        'log_assets': np.random.normal(10, 2, 1000),
        'leverage': np.random.uniform(0, 0.8, 1000)
    })
    
    codebook = tracker.generate_codebook(
        df=sample_df,
        output_path='demo_codebook.json',
        variable_descriptions={
            'roa': 'Return on Assets',
            'log_assets': '総資産の自然対数',
            'leverage': 'レバレッジ比率'
        }
    )
    
    # 最終データセット情報
    tracker.set_final_dataset_info(
        file_path='final_dataset.csv',
        file_hash='abc123...',
        sample_size=1000,
        time_period='2015-2023'
    )
    
    # 系譜レポート出力
    tracker.export_lineage_report('demo_lineage_report.json')
    
    print("\n✓ デモ完了！")
    print("生成ファイル:")
    print("  - demo_codebook.json")
    print("  - demo_lineage_report.json")
