"""
collect_japan_data_demo.py

Japan Firms Data Collection - DEMO VERSION

This demo version generates sample data to demonstrate the workflow
without requiring actual EDINET API access.

Usage:
    cd 2-data-sources/examples/japan_basic/
    python collect_japan_data_demo.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from edinet_collector import EDINETCollector


def generate_sample_edinet_data(n_docs: int = 50) -> pd.DataFrame:
    """
    Generate sample EDINET document data for demonstration
    
    Args:
        n_docs: Number of sample documents to generate
    
    Returns:
        DataFrame mimicking EDINET API response structure
    """
    np.random.seed(42)
    
    # Sample Japanese company names
    company_names = [
        'トヨタ自動車株式会社', 'ソニーグループ株式会社', 
        'パナソニック株式会社', '本田技研工業株式会社',
        '日産自動車株式会社', 'キヤノン株式会社',
        '富士フイルムホールディングス株式会社', '株式会社日立製作所',
        '三菱電機株式会社', '株式会社東芝',
        '任天堂株式会社', 'ソフトバンクグループ株式会社',
        '株式会社NTTドコモ', 'KDDI株式会社',
        '三菱UFJフィナンシャル・グループ', '株式会社三井住友フィナンシャルグループ'
    ]
    
    doc_types = [
        '有価証券報告書', '四半期報告書', '半期報告書', 
        '臨時報告書', '訂正有価証券報告書', '内部統制報告書'
    ]
    
    data = []
    for i in range(n_docs):
        company = np.random.choice(company_names)
        doc_type = np.random.choice(doc_types)
        
        data.append({
            'edinetCode': f'E{10000 + i:05d}',
            'secCode': f'{1000 + np.random.randint(0, 9000):04d}',
            'filerName': company,
            'docDescription': doc_type,
            'submitDateTime': '2024-01-10 09:00',
            'docTypeCode': '120' if '有価証券報告書' in doc_type else '140',
            'industryCode': f'{np.random.randint(1, 20):03d}',
            'JCN': f'{1000000000000 + i:013d}',
            'retrieval_date': '2024-01-10'
        })
    
    return pd.DataFrame(data)


def main():
    """Execute demo data collection"""
    
    print("=" * 80)
    print("JAPAN FIRMS DATA COLLECTION - DEMO VERSION")
    print("(Using sample data - no actual API calls)")
    print("=" * 80)
    print()
    
    # Initialize collector
    print("[Initialization]")
    print("-" * 80)
    collector = EDINETCollector(rate_limit_delay=0.1)  # Faster for demo
    print("✓ EDINETCollector initialized")
    print()
    
    # Generate sample data
    print("[Step 1] Generating Sample EDINET Data")
    print("-" * 80)
    print("Note: This demo uses generated data instead of real API calls")
    print()
    
    df_docs = generate_sample_edinet_data(n_docs=50)
    print(f"✓ Generated {len(df_docs)} sample documents")
    print()
    print("Sample documents (first 5):")
    print(df_docs[['filerName', 'docDescription']].head())
    print()
    
    # Step 2: Filter for securities reports
    print("[Step 2] Filtering for Securities Reports")
    print("-" * 80)
    
    df_reports = collector.filter_securities_reports(df_docs)
    print(f"✓ Securities reports: {len(df_reports)}")
    print()
    
    # Step 3: Extract firm information
    print("[Step 3] Extracting Firm Information")
    print("-" * 80)
    
    df_firms = collector.extract_firm_list(df_reports)
    print(f"✓ Unique firms: {len(df_firms)}")
    
    if len(df_firms) > 0:
        print()
        print("Sample firms:")
        print(df_firms.head())
    print()
    
    # Step 4: Save results
    print("[Step 4] Saving Results")
    print("-" * 80)
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    collector.save_to_csv(df_docs, output_dir / 'edinet_documents_demo.csv')
    print(f"✓ Document list saved")
    
    collector.save_to_csv(df_reports, output_dir / 'securities_reports_demo.csv')
    print(f"✓ Securities reports saved")
    
    collector.save_to_csv(df_firms, output_dir / 'firm_list_demo.csv')
    print(f"✓ Firm list saved")
    
    print()
    
    # Summary
    print("=" * 80)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("Output files (demo data):")
    print(f"  - edinet_documents_demo.csv ({len(df_docs)} rows)")
    print(f"  - securities_reports_demo.csv ({len(df_reports)} rows)")
    print(f"  - firm_list_demo.csv ({len(df_firms)} rows)")
    print()
    print("This demo demonstrates the workflow:")
    print("  1. Fetch documents from EDINET (simulated)")
    print("  2. Filter for securities reports")
    print("  3. Extract unique firm list")
    print("  4. Save results for analysis")
    print()
    print("For real data collection:")
    print("  - Use collect_japan_data.py with valid EDINET API access")
    print("  - Check EDINET API documentation for access requirements")
    print("  - Consider using date ranges with collect_sample()")
    print()


if __name__ == "__main__":
    main()
