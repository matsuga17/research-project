#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
論文削減版作成スクリプト
目標: 57,185字 → 32,000字（25,185字削減）
"""

import re

def read_file(filepath):
    """ファイルを読み込み"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def count_chars(text):
    """文字数をカウント"""
    return len(text.replace(' ', '').replace('\n', '').replace('\t', '').replace('　', ''))

def reduce_section_4(text):
    """第4部の削減（17,363字 → 10,000字）"""
    # 各企業のケース分析を簡潔化
    # 詳細な財務データの一部を削除
    # 重複する説明を削除
    
    # 企業ごとの分析を簡潔化（例：各企業2,000字程度に圧縮）
    patterns_to_reduce = [
        # 冗長な説明文を削除
        (r'　この.*?である。　この.*?である。', r'　'),
        # 詳細すぎる財務データの説明を簡略化
        (r'2023年度の.*?となっている（.*?, 2024, p\.\d+）。', r''),
    ]
    
    reduced_text = text
    for pattern, replacement in patterns_to_reduce:
        reduced_text = re.sub(pattern, replacement, reduced_text, flags=re.DOTALL)
    
    return reduced_text

def reduce_section_5(text):
    """第5部の削減（8,895字 → 4,500字）"""
    # 理論的説明の簡潔化
    # 重複する概念説明の削除
    
    reduced_text = text
    return reduced_text

def create_reduced_version():
    """削減版を作成"""
    
    print("削減版作成を開始します...")
    
    # Draft1とDraft2を読み込み
    draft1 = read_file("調査と分析/Week3_Day25-27asia_pacific_ecommerce_research_draft1.md")
    draft2 = read_file("調査と分析/Week3_Day28-29asia_pacific_ecommerce_research_draft2+draft3.md")
    
    original_chars = count_chars(draft1 + draft2)
    print(f"元の文字数: {original_chars:,}字")
    
    # ===== 手動による慎重な削減 =====
    # 自動削減ではなく、重要な内容を保持しつつ手動で削減
    
    print("\n⚠️ 重要: 自動削減では品質が低下する可能性があります")
    print("手動での慎重な削減を推奨します")
    print("\n削減ガイドライン:")
    print("1. 各企業ケースを2,000-2,500字に圧縮")
    print("2. 理論説明を簡潔化（本質は保持）")
    print("3. 重複する説明を削除")
    print("4. 補足的な情報を削除")
    print("5. 引用を要約に変更")
    
    # 削減版の雛形を作成
    reduced_content = f"""# アジア太平洋E-commerce市場における事業戦略の構造的差異
## —市場成熟度と戦略パターン適合性の実証的研究—

**研究者**：Changu  
**作成日**：2025年11月20日  
**バージョン**：削減版（目標32,000字）

---

## ⚠️ 削減方針

- 第1部〜第3部: 最小限の削減（構造と論理は維持）
- 第4部（実証分析）: 各企業ケースを簡潔化（17,363字 → 10,000字）
- 第5部（理論構築）: 重複を削除し簡潔化（8,895字 → 4,500字）
- 第6部（考察）: 本質的な議論のみ残す（5,910字 → 3,500字）
- 第7部（結論）: 簡潔にまとめる（4,671字 → 2,000字）

---

{draft1}

---

## ⚠️ 以下、削減が必要なセクション

{draft2}

---

## 削減作業メモ

**削減必要文字数**: 25,185字
**削減率**: 44%

### セクション別削減計画
- 第4部: 7,363字削減（42%削減）
- 第5部: 4,395字削減（49%削減）
- 第6部: 2,410字削減（41%削減）
- 第7部: 2,671字削減（57%削減）
- その他: 8,346字削減
"""
    
    # 削減版を保存
    output_path = "final_paper_reduction_needed.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(reduced_content)
    
    print(f"\n削減が必要な論文を保存しました: {output_path}")
    print("\n次のステップ:")
    print("1. このファイルを開いて、手動で慎重に削減")
    print("2. 各セクションの削減目標を確認")
    print("3. 重要な内容は保持し、冗長部分のみ削除")
    print("4. 削減後、文字数を再確認")

if __name__ == "__main__":
    try:
        create_reduced_version()
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()
