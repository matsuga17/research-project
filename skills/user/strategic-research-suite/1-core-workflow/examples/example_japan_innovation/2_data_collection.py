"""
2_data_collection.py

Data Collection for Japan Innovation Study

This script demonstrates data collection from Japanese sources.
For demonstration, it generates synthetic data that mimics EDINET structure.
In production, this would connect to actual EDINET API.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / 'scripts'
sys.path.append(str(scripts_dir))


def collect_japan_firm_data():
    """
    Collect Japanese firm data (demo version)
    
    In production, this would:
    1. Connect to EDINET API
    2. Download 有価証券報告書
    3. Extract financial data from XBRL
    """
    print("\n📡 Collecting data from Japanese sources...")
    print("   Source: EDINET (demo data)")
    
    # Generate synthetic data that mimics Japanese firms
    np.random.seed(42)
    
    # Japanese firm IDs (E-codes)
    n_firms = 500
    firm_codes = [f"E{1000+i:05d}" for i in range(n_firms)]
    
    # Years
    years = range(2010, 2024)
    
    data = []
    for firm_code in firm_codes:
        # Firm characteristics
        firm_industry = np.random.choice(['電気機器', '機械', '化学', '自動車', '医薬品'], 
                                        p=[0.25, 0.20, 0.20, 0.20, 0.15])
        base_size = np.random.lognormal(17, 2)  # Larger firms in yen
        base_roa = np.random.normal(0.04, 0.02)
        
        for year in years:
            # Time trends
            growth = (year - 2010) * 0.01
            
            data.append({
                'firm_code': firm_code,
                'firm_name': f'株式会社{firm_code}',
                'year': year,
                'industry': firm_industry,
                'sales_yen': base_size * (1 + growth) * np.random.lognormal(0, 0.3),  # 売上高（億円）
                'operating_income_yen': base_size * base_roa * (1 + growth) * np.random.lognormal(0, 0.5),  # 営業利益
                'net_income_yen': base_size * base_roa * 0.7 * (1 + growth) * np.random.lognormal(0, 0.6),  # 当期純利益
                'total_assets_yen': base_size * 2 * (1 + growth) * np.random.lognormal(0, 0.2),  # 総資産
                'total_equity_yen': base_size * 0.8 * (1 + growth) * np.random.lognormal(0, 0.25),  # 純資産
                'rd_expenditure_yen': base_size * np.random.uniform(0.01, 0.15),  # R&D支出
                'num_employees': int(base_size / 10 * np.random.uniform(0.8, 1.2)),  # 従業員数
                'num_patents': np.random.poisson(base_size / 100),  # 特許出願数
                'listing_market': np.random.choice(['東証プライム', '東証スタンダード'], p=[0.7, 0.3])
            })
    
    df = pd.DataFrame(data)
    
    # Calculate financial ratios
    df['roa'] = df['net_income_yen'] / df['total_assets_yen']
    df['roe'] = df['net_income_yen'] / df['total_equity_yen']
    df['rd_intensity'] = df['rd_expenditure_yen'] / df['sales_yen']
    df['leverage'] = (df['total_assets_yen'] - df['total_equity_yen']) / df['total_assets_yen']
    df['log_sales'] = np.log(df['sales_yen'] + 1)
    df['log_assets'] = np.log(df['total_assets_yen'] + 1)
    df['firm_age'] = df['year'] - 1990  # Assume all firms founded around 1990
    
    print(f"   ✓ Collected data for {n_firms} firms")
    print(f"   ✓ Time period: {df['year'].min()}-{df['year'].max()}")
    print(f"   ✓ Total observations: {len(df):,}")
    
    return df


def main():
    """
    Execute data collection
    """
    print("=" * 70)
    print("Japan Innovation Research - Data Collection")
    print("=" * 70)
    
    # Create output directory
    output_dir = Path("./output/")
    output_dir.mkdir(exist_ok=True)
    
    # Collect data
    df = collect_japan_firm_data()
    
    # Save raw data
    raw_file = output_dir / 'japan_firms_raw.csv'
    df.to_csv(raw_file, index=False, encoding='utf-8-sig')  # UTF-8 with BOM for Excel
    
    print("\n" + "=" * 70)
    print("Data Collection Completed!")
    print("=" * 70)
    
    print("\n📊 Sample Statistics:")
    print(f"  Firms: {df['firm_code'].nunique():,}")
    print(f"  Observations: {len(df):,}")
    print(f"  Years: {df['year'].min()}-{df['year'].max()}")
    
    print("\n🏭 Industry Distribution:")
    industry_dist = df.groupby('industry')['firm_code'].nunique()
    for industry, count in industry_dist.items():
        print(f"  {industry}: {count}社")
    
    print("\n📈 Key Variables (Mean):")
    print(f"  ROA: {df['roa'].mean():.3f}")
    print(f"  R&D Intensity: {df['rd_intensity'].mean():.3f}")
    print(f"  Sales (億円): {df['sales_yen'].mean():,.0f}")
    print(f"  Patents/firm/year: {df['num_patents'].mean():.1f}")
    
    print(f"\n💾 Data saved to:")
    print(f"  {raw_file}")
    
    print("\n📝 Next Step:")
    print("  Run 3_full_pipeline.py to execute complete analysis")
    print("=" * 70)


if __name__ == "__main__":
    main()
