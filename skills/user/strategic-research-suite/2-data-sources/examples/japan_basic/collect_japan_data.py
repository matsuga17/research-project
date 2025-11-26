"""
collect_japan_data.py

Japan Firms Data Collection Example

This script demonstrates how to collect Japanese firm data from EDINET.

Steps:
1. Initialize EDINET collector
2. Fetch document list for specific dates
3. Filter for securities reports
4. Extract firm information
5. Save results

Usage:
    cd 2-data-sources/examples/japan_basic/
    python collect_japan_data.py
"""

import sys
from pathlib import Path
import pandas as pd

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'scripts'))
from edinet_collector import EDINETCollector


def main():
    """Execute Japan data collection example"""
    
    print("=" * 80)
    print("JAPAN FIRMS DATA COLLECTION EXAMPLE (EDINET)")
    print("=" * 80)
    print()
    
    # Initialize collector with 2-second delay (be respectful to API)
    print("[Initialization]")
    print("-" * 80)
    collector = EDINETCollector(rate_limit_delay=2.0)
    print("✓ EDINETCollector initialized (rate limit: 2.0s)")
    print()
    
    # Step 1: Fetch document list for a single day
    print("[Step 1] Fetching Document List")
    print("-" * 80)
    print("Target date: 2024-01-10")
    print()
    
    try:
        df_docs = collector.get_document_list('2024-01-10')
        
        if len(df_docs) > 0:
            print(f"✓ Retrieved {len(df_docs)} documents")
            print()
            print("Sample documents (first 5):")
            print(df_docs[['filerName', 'docDescription']].head())
            print()
        else:
            print("⚠ No documents found for this date")
            print()
    
    except Exception as e:
        print(f"✗ Error: {e}")
        print("This may be due to:")
        print("  - Network connection issues")
        print("  - EDINET API being unavailable")
        print("  - Invalid date format")
        return
    
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
    
    # Save document list
    if len(df_docs) > 0:
        collector.save_to_csv(df_docs, output_dir / 'edinet_documents_20240110.csv')
        print(f"✓ Document list saved")
    
    # Save securities reports
    if len(df_reports) > 0:
        collector.save_to_csv(df_reports, output_dir / 'securities_reports_20240110.csv')
        print(f"✓ Securities reports saved")
    
    # Save firm list
    if len(df_firms) > 0:
        collector.save_to_csv(df_firms, output_dir / 'firm_list_20240110.csv')
        print(f"✓ Firm list saved")
    
    print()
    
    # Summary
    print("=" * 80)
    print("COLLECTION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print(f"Results saved to: {output_dir}")
    print()
    print("Output files:")
    print(f"  - edinet_documents_20240110.csv ({len(df_docs)} rows)")
    print(f"  - securities_reports_20240110.csv ({len(df_reports)} rows)")
    print(f"  - firm_list_20240110.csv ({len(df_firms)} rows)")
    print()
    print("Next steps:")
    print("  1. Review collected data in output/ directory")
    print("  2. Extend date range with collect_sample()")
    print("  3. Extract EDINET codes for panel dataset construction")
    print("  4. Implement XBRL parsing for financial variable extraction")
    print()


if __name__ == "__main__":
    main()
