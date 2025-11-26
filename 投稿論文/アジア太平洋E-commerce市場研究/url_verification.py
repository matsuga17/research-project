#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL検証スクリプト
参考文献リスト内のすべてのURLの接続性を検証
"""

import re
import requests
from urllib.parse import urlparse
from datetime import datetime
import time

def extract_urls_from_file(filename):
    """ファイルからURLを抽出"""
    urls = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # URLパターンを検索
            url_pattern = r'https?://[^\s\)」】\]\>]+'
            found_urls = re.findall(url_pattern, content)
            urls = list(set(found_urls))  # 重複を除去
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
    return urls

def verify_url(url, timeout=10):
    """URLの接続性を検証"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        if status_code < 400:
            return True, status_code, "OK"
        else:
            return False, status_code, f"HTTP Error {status_code}"
    except requests.exceptions.Timeout:
        return False, None, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, None, "Connection Error"
    except requests.exceptions.TooManyRedirects:
        return False, None, "Too Many Redirects"
    except Exception as e:
        return False, None, str(e)

def generate_verification_report(urls):
    """URL検証レポートを生成"""
    report = []
    report.append("=" * 80)
    report.append("URL検証レポート")
    report.append(f"生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    report.append(f"検証URL数: {len(urls)}")
    report.append("=" * 80)
    report.append("")
    
    success_count = 0
    failure_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"検証中 ({i}/{len(urls)}): {url[:60]}...")
        is_valid, status_code, message = verify_url(url)
        
        if is_valid:
            success_count += 1
            report.append(f"✓ OK  [{status_code}] {url}")
        else:
            failure_count += 1
            report.append(f"✗ FAIL [{message}] {url}")
        
        # レート制限を避けるため、少し待機
        time.sleep(0.5)
    
    report.append("")
    report.append("=" * 80)
    report.append(f"検証結果サマリー")
    report.append(f"成功: {success_count} / 失敗: {failure_count} / 合計: {len(urls)}")
    report.append(f"成功率: {success_count/len(urls)*100:.1f}%")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    """メイン処理"""
    # 参考文献リストファイル
    refs_file = "references.txt"
    
    # 最終論文ファイル（Markdown版）
    paper_files = [
        "調査と分析/Week3_Day25-27asia_pacific_ecommerce_research_draft1.md",
        "調査と分析/Week3_Day28-29asia_pacific_ecommerce_research_draft2+draft3.md"
    ]
    
    all_urls = []
    
    # 参考文献リストからURL抽出
    print(f"\n参考文献リストからURL抽出中: {refs_file}")
    all_urls.extend(extract_urls_from_file(refs_file))
    
    # 論文ファイルからURL抽出
    for paper_file in paper_files:
        print(f"論文ファイルからURL抽出中: {paper_file}")
        all_urls.extend(extract_urls_from_file(paper_file))
    
    # 重複を除去
    all_urls = list(set(all_urls))
    print(f"\n抽出されたユニークURL数: {len(all_urls)}")
    
    # URL検証
    print("\nURL検証を開始します...\n")
    report = generate_verification_report(all_urls)
    
    # レポートを表示
    print("\n" + report)
    
    # レポートをファイルに保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f"url_verification_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nレポートを保存しました: {report_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
