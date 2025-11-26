"""
US Corporate Analytics - 統合テストスクリプト

すべての主要機能が正しく動作するかテストします。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from datetime import datetime


class IntegrationTester:
    """統合テストクラス"""
    
    def __init__(self, config_path: str):
        """
        初期化
        
        Parameters:
            config_path: 設定ファイルのパス
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name: str, test_func) -> bool:
        """
        テストを実行
        
        Parameters:
            test_name: テスト名
            test_func: テスト関数
            
        Returns:
            テストの成功/失敗
        """
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"{'='*60}")
        
        try:
            test_func()
            print(f"\n✓ {test_name} - PASSED")
            self.test_results.append((test_name, True, None))
            self.passed += 1
            return True
        except Exception as e:
            print(f"\n✗ {test_name} - FAILED")
            print(f"Error: {e}")
            self.test_results.append((test_name, False, str(e)))
            self.failed += 1
            return False
    
    def test_sec_client(self):
        """SEC APIクライアントのテスト"""
        from utils.sec_client import SECEdgarClient
        
        client = SECEdgarClient(
            api_key=self.config['sec_edgar']['api_key'],
            user_agent=self.config['sec_edgar']['user_agent']
        )
        
        # CIK取得テスト
        print("  - Testing CIK retrieval...")
        cik = client.get_company_cik("AAPL")
        assert cik is not None, "Failed to retrieve CIK"
        print(f"    Apple CIK: {cik}")
        
        # Company Facts取得テスト
        print("  - Testing Company Facts retrieval...")
        facts = client.get_company_facts(cik)
        assert 'facts' in facts, "Failed to retrieve company facts"
        print(f"    Facts retrieved: {len(facts['facts'])} categories")
        
        print("  ✓ SEC Client tests passed")
    
    def test_worldbank_client(self):
        """World Bank APIクライアントのテスト"""
        from utils.worldbank_client import WorldBankClient
        
        client = WorldBankClient()
        
        # GDP データ取得テスト
        print("  - Testing GDP data retrieval...")
        gdp_data = client.get_gdp_data("USA", 2020, 2023)
        assert not gdp_data.empty, "Failed to retrieve GDP data"
        print(f"    GDP data points: {len(gdp_data)}")
        
        print("  ✓ World Bank Client tests passed")
    
    def test_imf_client(self):
        """IMF APIクライアントのテスト"""
        from utils.imf_client import IMFClient
        
        client = IMFClient()
        
        # GDP指標取得テスト
        print("  - Testing IMF GDP indicators...")
        gdp_data = client.get_gdp_indicators(["USA"], 2020, 2023)
        assert not gdp_data.empty, "Failed to retrieve IMF data"
        print(f"    IMF data points: {len(gdp_data)}")
        
        print("  ✓ IMF Client tests passed")
    
    def test_financial_ratios(self):
        """財務比率計算のテスト"""
        from utils.financial_ratios import FinancialRatioCalculator
        import pandas as pd
        
        # サンプルデータ作成
        data = pd.DataFrame({
            'revenue': [1000000, 1100000, 1200000],
            'net_income': [100000, 110000, 120000],
            'total_assets': [500000, 550000, 600000],
            'stockholders_equity': [300000, 330000, 360000],
            'current_assets': [200000, 220000, 240000],
            'current_liabilities': [100000, 110000, 120000],
            'total_liabilities': [200000, 220000, 240000],
        }, index=[2021, 2022, 2023])
        
        # 財務比率計算
        print("  - Testing financial ratio calculations...")
        calculator = FinancialRatioCalculator(data)
        ratios = calculator.calculate_all_ratios()
        
        assert not ratios.empty, "Failed to calculate ratios"
        assert 'ROA' in ratios.columns, "ROA not calculated"
        assert 'ROE' in ratios.columns, "ROE not calculated"
        
        print(f"    Calculated ratios: {len(ratios.columns)} types")
        print("  ✓ Financial Ratios tests passed")
    
    def test_company_analyzer(self):
        """企業分析器のテスト"""
        from scripts.company_analyzer import CompanyAnalyzer
        
        # 小規模テスト（1年分のみ）
        print("  - Testing Company Analyzer...")
        analyzer = CompanyAnalyzer("AAPL", self.config)
        
        # CIK取得
        cik = analyzer.sec_client.get_company_cik("AAPL")
        assert cik is not None, "Failed to retrieve CIK in analyzer"
        analyzer.cik = cik
        
        print(f"    Analyzer initialized with CIK: {cik}")
        print("  ✓ Company Analyzer tests passed")
    
    def test_visualizer(self):
        """可視化機能のテスト"""
        from scripts.visualizer import FinancialVisualizer
        import pandas as pd
        import tempfile
        
        # サンプルデータ作成
        data = pd.DataFrame({
            'ROA': [15.2, 16.1, 17.3],
            'ROE': [45.3, 48.2, 52.1],
        }, index=[2021, 2022, 2023])
        
        print("  - Testing visualization...")
        visualizer = FinancialVisualizer()
        
        # テンポラリファイルに保存
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            visualizer.plot_trend(data, ['ROA', 'ROE'], save_path=tmp.name)
            assert os.path.exists(tmp.name), "Failed to save visualization"
            os.unlink(tmp.name)
        
        print("  ✓ Visualizer tests passed")
    
    def print_summary(self):
        """テスト結果のサマリーを表示"""
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"\nTotal tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print(f"\n{'-'*60}")
            print("FAILED TESTS:")
            print(f"{'-'*60}")
            for test_name, passed, error in self.test_results:
                if not passed:
                    print(f"\n✗ {test_name}")
                    print(f"  Error: {error}")
        
        print(f"\n{'='*60}\n")
        
        return self.failed == 0


def main():
    """メイン実行関数"""
    print(f"\n{'#'*60}")
    print(f"# US Corporate Analytics - Integration Tests")
    print(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'#'*60}\n")
    
    # 設定ファイルのパス
    config_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'config.yaml'
    )
    
    if not os.path.exists(config_path):
        print(f"✗ Configuration file not found: {config_path}")
        print("  Please create config.yaml first.")
        sys.exit(1)
    
    # テスター初期化
    tester = IntegrationTester(config_path)
    
    # テスト実行
    tests = [
        ("SEC EDGAR Client", tester.test_sec_client),
        ("World Bank Client", tester.test_worldbank_client),
        ("IMF Client", tester.test_imf_client),
        ("Financial Ratios Calculator", tester.test_financial_ratios),
        ("Company Analyzer", tester.test_company_analyzer),
        ("Visualizer", tester.test_visualizer),
    ]
    
    for test_name, test_func in tests:
        tester.run_test(test_name, test_func)
    
    # サマリー表示
    success = tester.print_summary()
    
    if success:
        print("✓ All tests passed successfully!")
        print("\nYour US Corporate Analytics skill is ready to use.")
        print("\nNext steps:")
        print("  1. Run quickstart.py for a guided tour")
        print("  2. Check notebooks/01_getting_started.ipynb")
        print("  3. Read SKILL.md for detailed documentation")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
