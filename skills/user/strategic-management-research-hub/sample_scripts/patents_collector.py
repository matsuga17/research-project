"""
PatentsView Data Collector for Strategic Management Research
特許データ収集と戦略変数構築

使用例：
    collector = PatentsCollector()
    patents_df = collector.collect_firm_patents('Apple Inc', 2010, 2023)
    metrics = collector.calculate_innovation_metrics(patents_df)
"""

import requests
import pandas as pd
import numpy as np
from typing import Dict, List
import time
from collections import Counter


class PatentsCollector:
    """PatentsView APIを使用した特許データ収集"""
    
    def __init__(self):
        self.api_url = "https://api.patentsview.org/patents/query"
        self.rate_limit_delay = 0.5  # Respectful scraping
        
    def collect_firm_patents(self, 
                            firm_name: str, 
                            start_year: int, 
                            end_year: int,
                            max_results: int = 10000) -> pd.DataFrame:
        """
        企業の特許データを収集
        
        Args:
            firm_name: 企業名（例：'Apple Inc', 'Samsung Electronics'）
            start_year: 開始年
            end_year: 終了年
            max_results: 最大取得件数
            
        Returns:
            特許データフレーム
        """
        query = {
            "q": {
                "_and": [
                    {"assignee_organization": firm_name},
                    {"_gte": {"patent_date": f"{start_year}-01-01"}},
                    {"_lte": {"patent_date": f"{end_year}-12-31"}}
                ]
            },
            "f": [
                "patent_number",
                "patent_date",
                "patent_title",
                "patent_abstract",
                "cited_patent_number",
                "citedby_patent_number",
                "uspc_mainclass_id",
                "cpc_subgroup_id",
                "inventor_id",
                "inventor_city",
                "inventor_country"
            ],
            "o": {
                "page": 1,
                "per_page": 1000
            },
            "s": [{"patent_date": "asc"}]
        }
        
        all_patents = []
        page = 1
        
        while True:
            query["o"]["page"] = page
            
            try:
                response = requests.post(self.api_url, json=query)
                response.raise_for_status()
                data = response.json()
                
                patents = data.get('patents', [])
                if not patents:
                    break
                    
                all_patents.extend(patents)
                print(f"  Retrieved {len(all_patents)} patents...")
                
                if len(all_patents) >= max_results:
                    break
                if len(patents) < 1000:  # Last page
                    break
                    
                page += 1
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                break
        
        df = pd.DataFrame(all_patents)
        print(f"Total patents collected: {len(df)}")
        
        return df
    
    def calculate_innovation_metrics(self, patents_df: pd.DataFrame) -> Dict:
        """
        イノベーション指標を計算
        
        Strategic variables:
        - Patent count: イノベーション量
        - Citation count: イノベーション影響力
        - Tech diversity: 技術多角化
        - Generality: 技術汎用性
        - Originality: 技術新規性
        
        Returns:
            指標の辞書
        """
        metrics = {}
        
        # 1. 特許数（基本指標）
        metrics['patent_count'] = len(patents_df)
        
        if metrics['patent_count'] == 0:
            return metrics
        
        # 2. Forward Citations（影響力）
        citations = patents_df['citedby_patent_number'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )
        metrics['avg_citations'] = citations.mean()
        metrics['citation_std'] = citations.std()
        metrics['total_citations'] = citations.sum()
        
        # 3. Technology Diversity (Entropy Index)
        tech_classes = []
        for classes in patents_df['uspc_mainclass_id']:
            if isinstance(classes, list):
                tech_classes.extend(classes)
        
        if tech_classes:
            class_counts = Counter(tech_classes)
            total = sum(class_counts.values())
            probs = np.array([count/total for count in class_counts.values()])
            metrics['tech_diversity'] = -np.sum(probs * np.log(probs))
        else:
            metrics['tech_diversity'] = 0
        
        # 4. Generality Index（汎用性）
        # 被引用特許の技術クラス分散度
        generality_scores = []
        for cited_by in patents_df['citedby_patent_number']:
            if isinstance(cited_by, list) and len(cited_by) > 0:
                # 簡略版：被引用数の多様性
                generality = 1 - (1 / len(set(cited_by))) if cited_by else 0
                generality_scores.append(generality)
        
        metrics['avg_generality'] = np.mean(generality_scores) if generality_scores else 0
        
        # 5. Originality Index（新規性）
        # 引用特許の技術クラス分散度
        originality_scores = []
        for cited in patents_df['cited_patent_number']:
            if isinstance(cited, list) and len(cited) > 0:
                originality = 1 - (1 / len(set(cited))) if cited else 0
                originality_scores.append(originality)
        
        metrics['avg_originality'] = np.mean(originality_scores) if originality_scores else 0
        
        # 6. 発明者多様性
        all_inventors = []
        for inventors in patents_df['inventor_id']:
            if isinstance(inventors, list):
                all_inventors.extend(inventors)
        
        metrics['unique_inventors'] = len(set(all_inventors))
        metrics['inventors_per_patent'] = len(all_inventors) / metrics['patent_count']
        
        return metrics
    
    def construct_patent_stock(self, 
                              annual_patents: pd.DataFrame,
                              depreciation_rate: float = 0.15,
                              max_lag: int = 10) -> pd.DataFrame:
        """
        特許ストックを構築（減価償却考慮）
        
        Args:
            annual_patents: 年次特許数データ（'year', 'patent_count'列必須）
            depreciation_rate: 年次減価償却率（デフォルト15%）
            max_lag: 考慮する最大ラグ期間
            
        Returns:
            特許ストックを含むデータフレーム
        """
        annual_patents = annual_patents.sort_values('year').copy()
        annual_patents['patent_stock'] = 0.0
        
        for idx, row in annual_patents.iterrows():
            current_year = row['year']
            stock = 0
            
            for lag in range(max_lag):
                lag_year = current_year - lag
                lag_patents = annual_patents[
                    annual_patents['year'] == lag_year
                ]['patent_count']
                
                if len(lag_patents) > 0:
                    stock += lag_patents.iloc[0] * ((1 - depreciation_rate) ** lag)
            
            annual_patents.loc[idx, 'patent_stock'] = stock
        
        return annual_patents
    
    def match_to_compustat(self,
                          patents_df: pd.DataFrame,
                          compustat_df: pd.DataFrame,
                          name_col: str = 'conm') -> pd.DataFrame:
        """
        PatentsデータとCompustatをマッチング
        
        Args:
            patents_df: 特許データ（'assignee_organization'列必須）
            compustat_df: Compustatデータ（企業名列必須）
            name_col: Compustatの企業名列名
            
        Returns:
            マッチング結果（'gvkey'列付き特許データ）
        """
        from fuzzywuzzy import fuzz, process
        import re
        
        def clean_name(name):
            """企業名の標準化"""
            if pd.isna(name):
                return ''
            name = str(name).lower()
            # 法人格削除
            suffixes = ['inc', 'corp', 'corporation', 'company', 'co',
                       'ltd', 'limited', 'llc', 'plc']
            for suffix in suffixes:
                name = re.sub(rf'\b{suffix}\b\.?', '', name)
            name = re.sub(r'[^\w\s]', '', name)
            name = re.sub(r'\s+', ' ', name).strip()
            return name
        
        # 名前クリーニング
        patents_df['clean_name'] = patents_df['assignee_organization'].apply(clean_name)
        compustat_df['clean_name'] = compustat_df[name_col].apply(clean_name)
        
        # Fuzzy matching
        compustat_names = compustat_df['clean_name'].unique()
        matches = []
        
        for idx, row in patents_df.iterrows():
            patent_name = row['clean_name']
            if not patent_name:
                continue
                
            best_match, score = process.extractOne(
                patent_name,
                compustat_names,
                scorer=fuzz.token_sort_ratio
            )
            
            if score >= 85:  # マッチング閾値
                gvkey = compustat_df[
                    compustat_df['clean_name'] == best_match
                ]['gvkey'].iloc[0]
                
                matches.append({
                    'patent_id': idx,
                    'gvkey': gvkey,
                    'match_score': score
                })
        
        match_df = pd.DataFrame(matches)
        patents_matched = patents_df.merge(
            match_df, 
            left_index=True, 
            right_on='patent_id',
            how='left'
        )
        
        match_rate = (patents_matched['gvkey'].notna().sum() / 
                     len(patents_matched) * 100)
        print(f"Match rate: {match_rate:.1f}%")
        
        return patents_matched


# 使用例
if __name__ == "__main__":
    # 初期化
    collector = PatentsCollector()
    
    # Example 1: Apple Inc.の特許収集
    print("Collecting Apple patents...")
    apple_patents = collector.collect_firm_patents(
        'Apple Inc',
        2015,
        2023
    )
    
    # イノベーション指標計算
    apple_metrics = collector.calculate_innovation_metrics(apple_patents)
    print("\nApple Innovation Metrics:")
    for key, value in apple_metrics.items():
        print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Example 2: 複数企業の年次特許数
    firms = ['Apple Inc', 'Samsung Electronics', 'Microsoft Corporation']
    all_annual = []
    
    for firm in firms:
        print(f"\nProcessing {firm}...")
        patents = collector.collect_firm_patents(firm, 2015, 2023)
        
        # 年次集計
        patents['year'] = pd.to_datetime(patents['patent_date']).dt.year
        annual = patents.groupby('year').size().reset_index(name='patent_count')
        annual['firm'] = firm
        
        # 特許ストック計算
        annual = collector.construct_patent_stock(annual)
        
        all_annual.append(annual)
    
    # 結合
    combined = pd.concat(all_annual, ignore_index=True)
    print("\nCombined annual patents:")
    print(combined)
    
    # CSV保存
    combined.to_csv('patent_data_sample.csv', index=False)
    print("\nData saved to: patent_data_sample.csv")
