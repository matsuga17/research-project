#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
論文の文字数分析と削減戦略の策定
"""

import re
from pathlib import Path

def count_chars(text):
    """文字数をカウント（空白・改行を除く）"""
    return len(text.replace(' ', '').replace('\n', '').replace('\t', '').replace('　', ''))

def analyze_markdown_file(filepath):
    """Markdownファイルを分析"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # セクションごとに分割
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    
    print(f"\n{'='*80}")
    print(f"ファイル分析: {Path(filepath).name}")
    print(f"{'='*80}\n")
    
    total_chars = 0
    section_info = []
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
        
        # セクション名を取得
        lines = section.split('\n')
        section_name = lines[0] if lines else f"セクション{i}"
        section_text = '\n'.join(lines[1:]) if len(lines) > 1 else ''
        
        char_count = count_chars(section_text)
        total_chars += char_count
        
        section_info.append({
            'name': section_name,
            'chars': char_count,
            'text': section_text
        })
    
    # 結果を表示
    print(f"総文字数: {total_chars:,}字\n")
    print(f"{'セクション名':<40} {'文字数':>10}")
    print('-' * 80)
    
    for info in sorted(section_info, key=lambda x: x['chars'], reverse=True):
        print(f"{info['name'][:38]:<40} {info['chars']:>10,}字")
    
    return total_chars, section_info

def main():
    # Draft1とDraft2+Draft3を分析
    draft1_path = "調査と分析/Week3_Day25-27asia_pacific_ecommerce_research_draft1.md"
    draft2_path = "調査と分析/Week3_Day28-29asia_pacific_ecommerce_research_draft2+draft3.md"
    
    print("\n" + "="*80)
    print("論文文字数分析レポート")
    print("="*80)
    
    # Draft1の分析
    draft1_chars, draft1_sections = analyze_markdown_file(draft1_path)
    
    # Draft2+Draft3の分析
    draft2_chars, draft2_sections = analyze_markdown_file(draft2_path)
    
    # 合計
    total_chars = draft1_chars + draft2_chars
    
    print(f"\n{'='*80}")
    print(f"合計文字数: {total_chars:,}字")
    print(f"目標範囲: 28,000-32,000字")
    print(f"超過: {total_chars - 32000:,}字 ({(total_chars/32000-1)*100:.1f}%)")
    print(f"{'='*80}\n")
    
    # 削減戦略の提案
    print("\n削減戦略の提案:")
    print("-" * 80)
    
    excess = total_chars - 32000
    
    if excess > 0:
        print(f"削減が必要な文字数: {excess:,}字\n")
        
        # 各セクションからの削減目標
        reduction_targets = {
            '実証分析': 0.20,  # 20%削減
            '理論構築': 0.15,  # 15%削減
            '考察': 0.15,      # 15%削減
            '先行研究': 0.10,  # 10%削減
            '方法論': 0.10     # 10%削減
        }
        
        print("セクション別削減目標:")
        for section_name, reduction_rate in reduction_targets.items():
            print(f"  {section_name}: {reduction_rate*100:.0f}%削減")
        
        print("\n具体的な削減方法:")
        print("  1. 冗長な説明文の簡潔化")
        print("  2. 重複する記述の削除")
        print("  3. 事例の詳細度を調整（本質を保ちつつ簡潔に）")
        print("  4. 長い引用を要約に変更")
        print("  5. 補足的な説明を削除")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
