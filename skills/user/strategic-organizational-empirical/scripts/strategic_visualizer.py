#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategic Visualizer: 戦略研究特化型可視化システム

Philosophical and Aesthetic Foundation:
========================================
Tufte (1983, 2001)の情報デザイン哲学に基づき、「データインク比」を最大化し、
「チャートジャンク」を最小化する。学術的可視化は単なる装飾ではなく、
理論的洞察の視覚的具現化である。Bertin (1967)のセミオロジー理論が示すように、
視覚変数（位置、サイズ、色、形状）は意味的関係を正確に表現しなければならない。

Core Design Principles:
- Clarity (明瞭性): 複雑な関係性を直感的に理解可能に
- Accuracy (正確性): データの忠実な表現、歪曲の排除
- Elegance (優雅性): 学術的品位と美的洗練の両立
- Context (文脈性): 理論的枠組みとの整合性

Visualization Types:
====================
1. 理論的フレームワーク図（Conceptual Framework Diagrams）
2. 因果関係図（Causal Path Diagrams）
3. 調整効果可視化（Interaction Plots）
4. 媒介効果図（Mediation Diagrams）
5. パネルデータ可視化（Panel Data Visualization）
6. 組織構造図（Organizational Structure Charts）
7. 戦略ポジショニング図（Strategic Position Maps）
8. パフォーマンス分解図（Performance Decomposition）

Technical Stack:
- matplotlib (基盤ライブラリ)
- seaborn (統計的可視化)
- plotly (インタラクティブ可視化)
- networkx (ネットワーク図)
- graphviz (概念図)

Usage:
======
    python strategic_visualizer.py \\
        --type framework \\
        --config visualization_config.yaml \\
        --output figures/

Author: Strategic Management Research Lab
Version: 1.0.0
License: MIT
Date: 2025-11-08

References:
-----------
- Tufte, E. R. (1983). The Visual Display of Quantitative Information. Graphics Press.
- Tufte, E. R. (2001). The Visual Display of Quantitative Information (2nd ed.). Graphics Press.
- Bertin, J. (1967). Sémiologie graphique. Mouton.
- Wilkinson, L. (2005). The Grammar of Graphics (2nd ed.). Springer.
"""

import argparse
import yaml
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib import cm
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
import sys
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# ==============================================================================
# Academic Color Palettes (学術的カラーパレット)
# ==============================================================================

# Colorblind-friendly palette based on Wong (2011)
WONG_PALETTE = {
    'black': '#000000',
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'purple': '#CC79A7'
}

# Grayscale palette for print journals
GRAYSCALE_PALETTE = {
    'dark_gray': '#2E2E2E',
    'medium_gray': '#6E6E6E',
    'light_gray': '#AEAEAE',
    'very_light_gray': '#D3D3D3',
    'black': '#000000',
    'white': '#FFFFFF'
}

# Theory-specific color schemes
THEORY_COLORS = {
    'RBV': '#0072B2',  # Blue - resources
    'TCE': '#D55E00',  # Vermillion - transactions
    'Institutional': '#009E73',  # Green - legitimacy
    'Dynamic_Capabilities': '#CC79A7'  # Purple - change
}

# ==============================================================================
# Visualization Configuration
# ==============================================================================

@dataclass
class VisualizationConfig:
    """可視化設定の構造化"""
    figure_size: Tuple[float, float] = (10, 6)
    dpi: int = 300
    font_family: str = 'serif'
    font_size: int = 11
    title_size: int = 14
    label_size: int = 12
    legend_size: int = 10
    color_palette: str = 'wong'
    style: str = 'seaborn-v0_8-whitegrid'
    output_format: str = 'png'
    transparent_background: bool = False
    
    def apply(self):
        """設定を適用"""
        plt.rcParams['figure.figsize'] = self.figure_size
        plt.rcParams['figure.dpi'] = self.dpi
        plt.rcParams['font.family'] = self.font_family
        plt.rcParams['font.size'] = self.font_size
        plt.rcParams['axes.titlesize'] = self.title_size
        plt.rcParams['axes.labelsize'] = self.label_size
        plt.rcParams['legend.fontsize'] = self.legend_size
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False

# ==============================================================================
# Core Visualizer Class
# ==============================================================================

class StrategicVisualizer:
    """
    戦略研究特化型可視化の中核クラス
    
    Philosophical Approach:
    ----------------------
    視覚化は単なるデータの表示ではなく、理論的理解の視覚的具現化である。
    Gestalt心理学の原則（近接、類似、閉合、連続）を活用し、
    認知的負荷を最小化しながら複雑な関係性を伝達する。
    """
    
    def __init__(self, config: Optional[VisualizationConfig] = None):
        """
        初期化
        
        Parameters:
        -----------
        config : VisualizationConfig, optional
            可視化設定
        """
        self.config = config or VisualizationConfig()
        self.config.apply()
        self.figures: Dict[str, plt.Figure] = {}
    
    def create_theoretical_framework(self, 
                                    constructs: List[Dict[str, Any]],
                                    relationships: List[Dict[str, Any]],
                                    title: str = "理論的フレームワーク",
                                    output_path: Optional[str] = None) -> plt.Figure:
        """
        理論的フレームワーク図の作成
        
        Creates a conceptual diagram showing relationships between theoretical constructs.
        
        Parameters:
        -----------
        constructs : List[Dict]
            構成概念のリスト [{'name': str, 'type': str, 'x': float, 'y': float}]
        relationships : List[Dict]
            関係性のリスト [{'from': str, 'to': str, 'type': str, 'label': str}]
        title : str
            図のタイトル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Draw constructs as boxes
        construct_positions = {}
        for construct in constructs:
            name = construct['name']
            x = construct.get('x', 0.5)
            y = construct.get('y', 0.5)
            construct_type = construct.get('type', 'independent')
            
            # Determine box color based on type
            if construct_type == 'independent':
                color = WONG_PALETTE['blue']
            elif construct_type == 'dependent':
                color = WONG_PALETTE['orange']
            elif construct_type == 'mediator':
                color = WONG_PALETTE['green']
            elif construct_type == 'moderator':
                color = WONG_PALETTE['purple']
            else:
                color = WONG_PALETTE['sky_blue']
            
            # Draw box
            box = FancyBboxPatch(
                (x - 0.1, y - 0.05), 0.2, 0.1,
                boxstyle="round,pad=0.01",
                edgecolor='black',
                facecolor=color,
                alpha=0.7,
                linewidth=2
            )
            ax.add_patch(box)
            
            # Add label
            ax.text(x, y, name, ha='center', va='center',
                   fontsize=self.config.label_size, fontweight='bold')
            
            construct_positions[name] = (x, y)
        
        # Draw relationships as arrows
        for rel in relationships:
            from_name = rel['from']
            to_name = rel['to']
            rel_type = rel.get('type', 'positive')
            label = rel.get('label', '')
            
            if from_name in construct_positions and to_name in construct_positions:
                x1, y1 = construct_positions[from_name]
                x2, y2 = construct_positions[to_name]
                
                # Determine arrow style
                if rel_type == 'positive':
                    arrow_style = '->'
                    color = 'black'
                    linestyle = '-'
                elif rel_type == 'negative':
                    arrow_style = '->'
                    color = 'red'
                    linestyle = '--'
                elif rel_type == 'moderation':
                    arrow_style = '->'
                    color = WONG_PALETTE['purple']
                    linestyle = '-.'
                else:
                    arrow_style = '->'
                    color = 'gray'
                    linestyle = '-'
                
                # Draw arrow
                arrow = FancyArrowPatch(
                    (x1 + 0.1, y1), (x2 - 0.1, y2),
                    arrowstyle=arrow_style,
                    color=color,
                    linestyle=linestyle,
                    linewidth=2,
                    mutation_scale=20
                )
                ax.add_patch(arrow)
                
                # Add label if provided
                if label:
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    ax.text(mid_x, mid_y + 0.03, label,
                           ha='center', va='bottom',
                           fontsize=self.config.legend_size,
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Set limits and remove axes
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        # Add title
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Framework diagram saved to: {output_path}")
        
        self.figures['framework'] = fig
        return fig
    
    def create_interaction_plot(self,
                              data: pd.DataFrame,
                              x_var: str,
                              y_var: str,
                              moderator: str,
                              title: str = "調整効果の可視化",
                              x_label: Optional[str] = None,
                              y_label: Optional[str] = None,
                              output_path: Optional[str] = None) -> plt.Figure:
        """
        調整効果の可視化（Interaction Plot）
        
        Visualizes how a moderator variable affects the relationship between
        an independent and dependent variable.
        
        Parameters:
        -----------
        data : pd.DataFrame
            分析データ
        x_var : str
            独立変数名
        y_var : str
            従属変数名
        moderator : str
            調整変数名
        title : str
            図のタイトル
        x_label : str, optional
            X軸ラベル
        y_label : str, optional
            Y軸ラベル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Standardize variables for interpretation
        x_std = (data[x_var] - data[x_var].mean()) / data[x_var].std()
        mod_std = (data[moderator] - data[moderator].mean()) / data[moderator].std()
        
        # Create moderator levels (+1SD, Mean, -1SD)
        mod_levels = {
            'Low (-1SD)': mod_std <= -1,
            'Mean': (mod_std > -0.5) & (mod_std < 0.5),
            'High (+1SD)': mod_std >= 1
        }
        
        colors = [WONG_PALETTE['blue'], WONG_PALETTE['green'], WONG_PALETTE['orange']]
        
        # Plot regression lines for each moderator level
        x_range = np.linspace(x_std.min(), x_std.max(), 100)
        
        for (level_name, level_mask), color in zip(mod_levels.items(), colors):
            if level_mask.sum() > 10:  # Ensure sufficient data points
                # Fit regression
                x_level = x_std[level_mask]
                y_level = data[y_var][level_mask]
                
                coeffs = np.polyfit(x_level, y_level, 1)
                y_pred = coeffs[0] * x_range + coeffs[1]
                
                # Plot line
                ax.plot(x_range, y_pred, color=color, linewidth=2.5,
                       label=f"{moderator}: {level_name}")
                
                # Add confidence interval (optional)
                # This is a simplified representation
                se = y_level.std() / np.sqrt(len(y_level))
                ax.fill_between(x_range, y_pred - 1.96*se, y_pred + 1.96*se,
                               alpha=0.2, color=color)
        
        # Formatting
        ax.set_xlabel(x_label or x_var, fontsize=self.config.label_size)
        ax.set_ylabel(y_label or y_var, fontsize=self.config.label_size)
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold')
        ax.legend(loc='best', fontsize=self.config.legend_size, frameon=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Interaction plot saved to: {output_path}")
        
        self.figures['interaction'] = fig
        return fig
    
    def create_mediation_diagram(self,
                               direct_effect: float,
                               indirect_effect: float,
                               total_effect: float,
                               paths: Dict[str, float],
                               construct_names: Dict[str, str],
                               title: str = "媒介効果の分析",
                               output_path: Optional[str] = None) -> plt.Figure:
        """
        媒介効果図の作成
        
        Visualizes mediation analysis following Baron & Kenny (1986) framework.
        
        Parameters:
        -----------
        direct_effect : float
            直接効果（c'）
        indirect_effect : float
            間接効果（a*b）
        total_effect : float
            総効果（c）
        paths : Dict[str, float]
            パス係数 {'a': float, 'b': float, 'c': float, 'c_prime': float}
        construct_names : Dict[str, str]
            変数名 {'IV': str, 'MED': str, 'DV': str}
        title : str
            図のタイトル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=(12, 8), dpi=self.config.dpi)
        
        # Define positions
        iv_pos = (0.2, 0.5)
        med_pos = (0.5, 0.7)
        dv_pos = (0.8, 0.5)
        
        # Draw constructs
        constructs = [
            (iv_pos, construct_names.get('IV', 'Independent Var'), WONG_PALETTE['blue']),
            (med_pos, construct_names.get('MED', 'Mediator'), WONG_PALETTE['green']),
            (dv_pos, construct_names.get('DV', 'Dependent Var'), WONG_PALETTE['orange'])
        ]
        
        for pos, name, color in constructs:
            box = FancyBboxPatch(
                (pos[0] - 0.08, pos[1] - 0.05), 0.16, 0.1,
                boxstyle="round,pad=0.01",
                edgecolor='black',
                facecolor=color,
                alpha=0.7,
                linewidth=2
            )
            ax.add_patch(box)
            ax.text(pos[0], pos[1], name, ha='center', va='center',
                   fontsize=self.config.label_size, fontweight='bold')
        
        # Draw paths
        # Path a: IV → Mediator
        arrow_a = FancyArrowPatch(
            (iv_pos[0] + 0.08, iv_pos[1] + 0.05), (med_pos[0] - 0.08, med_pos[1] - 0.05),
            arrowstyle='->',
            color='black',
            linewidth=2,
            mutation_scale=20
        )
        ax.add_patch(arrow_a)
        ax.text(0.32, 0.62, f"a = {paths.get('a', 0):.3f}",
               fontsize=self.config.legend_size,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # Path b: Mediator → DV
        arrow_b = FancyArrowPatch(
            (med_pos[0] + 0.08, med_pos[1] - 0.05), (dv_pos[0] - 0.08, dv_pos[1] + 0.05),
            arrowstyle='->',
            color='black',
            linewidth=2,
            mutation_scale=20
        )
        ax.add_patch(arrow_b)
        ax.text(0.68, 0.62, f"b = {paths.get('b', 0):.3f}",
               fontsize=self.config.legend_size,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # Path c': Direct effect
        arrow_c_prime = FancyArrowPatch(
            (iv_pos[0] + 0.08, iv_pos[1]), (dv_pos[0] - 0.08, dv_pos[1]),
            arrowstyle='->',
            color='red',
            linestyle='--',
            linewidth=2,
            mutation_scale=20
        )
        ax.add_patch(arrow_c_prime)
        ax.text(0.5, 0.42, f"c' = {direct_effect:.3f}",
               fontsize=self.config.legend_size,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # Add summary statistics box
        summary_text = (
            f"Total Effect (c): {total_effect:.3f}\n"
            f"Direct Effect (c'): {direct_effect:.3f}\n"
            f"Indirect Effect (a×b): {indirect_effect:.3f}\n"
            f"Mediation: {(indirect_effect/total_effect*100):.1f}%"
        )
        ax.text(0.5, 0.15, summary_text,
               ha='center', va='center',
               fontsize=self.config.legend_size,
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, pad=0.5))
        
        # Set limits and formatting
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Mediation diagram saved to: {output_path}")
        
        self.figures['mediation'] = fig
        return fig
    
    def create_panel_trajectory_plot(self,
                                    data: pd.DataFrame,
                                    entity_id: str,
                                    time_var: str,
                                    y_var: str,
                                    group_var: Optional[str] = None,
                                    title: str = "パネルデータの推移",
                                    y_label: Optional[str] = None,
                                    output_path: Optional[str] = None) -> plt.Figure:
        """
        パネルデータの軌跡プロット
        
        Visualizes trajectories of entities over time in panel data.
        
        Parameters:
        -----------
        data : pd.DataFrame
            パネルデータ
        entity_id : str
            エンティティID列名
        time_var : str
            時間変数列名
        y_var : str
            プロット対象変数
        group_var : str, optional
            グループ変数
        title : str
            図のタイトル
        y_label : str, optional
            Y軸ラベル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        if group_var:
            groups = data[group_var].unique()
            colors = sns.color_palette("husl", len(groups))
            
            for group, color in zip(groups, colors):
                group_data = data[data[group_var] == group]
                
                for entity in group_data[entity_id].unique():
                    entity_data = group_data[group_data[entity_id] == entity].sort_values(time_var)
                    ax.plot(entity_data[time_var], entity_data[y_var],
                           color=color, alpha=0.3, linewidth=1)
                
                # Plot group mean
                group_mean = group_data.groupby(time_var)[y_var].mean()
                ax.plot(group_mean.index, group_mean.values,
                       color=color, linewidth=3, label=f"Group: {group}")
        else:
            # Plot individual trajectories
            for entity in data[entity_id].unique()[:50]:  # Limit to 50 for visibility
                entity_data = data[data[entity_id] == entity].sort_values(time_var)
                ax.plot(entity_data[time_var], entity_data[y_var],
                       color='gray', alpha=0.3, linewidth=1)
            
            # Plot overall mean
            overall_mean = data.groupby(time_var)[y_var].mean()
            ax.plot(overall_mean.index, overall_mean.values,
                   color='red', linewidth=3, label='Mean Trajectory')
        
        ax.set_xlabel('Time Period', fontsize=self.config.label_size)
        ax.set_ylabel(y_label or y_var, fontsize=self.config.label_size)
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold')
        ax.legend(loc='best', fontsize=self.config.legend_size)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Panel trajectory plot saved to: {output_path}")
        
        self.figures['panel_trajectory'] = fig
        return fig
    
    def create_strategy_position_map(self,
                                    data: pd.DataFrame,
                                    x_var: str,
                                    y_var: str,
                                    label_var: Optional[str] = None,
                                    quadrant_labels: Optional[Dict[str, str]] = None,
                                    title: str = "戦略ポジショニング・マップ",
                                    x_label: Optional[str] = None,
                                    y_label: Optional[str] = None,
                                    output_path: Optional[str] = None) -> plt.Figure:
        """
        戦略ポジショニング・マップの作成
        
        Creates a 2x2 strategic positioning map (e.g., BCG Matrix style).
        
        Parameters:
        -----------
        data : pd.DataFrame
            分析データ
        x_var : str
            X軸変数
        y_var : str
            Y軸変数
        label_var : str, optional
            ラベル変数（企業名など）
        quadrant_labels : Dict[str, str], optional
            象限ラベル {'Q1': str, 'Q2': str, 'Q3': str, 'Q4': str}
        title : str
            図のタイトル
        x_label : str, optional
            X軸ラベル
        y_label : str, optional
            Y軸ラベル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=self.config.figure_size, dpi=self.config.dpi)
        
        # Calculate medians for quadrant division
        x_median = data[x_var].median()
        y_median = data[y_var].median()
        
        # Plot data points
        scatter = ax.scatter(data[x_var], data[y_var],
                           s=100, alpha=0.6,
                           c=data.index, cmap='viridis',
                           edgecolors='black', linewidth=1)
        
        # Add labels if provided
        if label_var and label_var in data.columns:
            for idx, row in data.iterrows():
                ax.annotate(row[label_var],
                          (row[x_var], row[y_var]),
                          xytext=(5, 5), textcoords='offset points',
                          fontsize=8, alpha=0.7)
        
        # Draw quadrant lines
        ax.axvline(x=x_median, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.axhline(y=y_median, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
        
        # Add quadrant labels if provided
        if quadrant_labels:
            x_min, x_max = ax.get_xlim()
            y_min, y_max = ax.get_ylim()
            
            offset = 0.02
            label_positions = {
                'Q1': (x_median + (x_max - x_median) * offset, y_median + (y_max - y_median) * (1 - offset)),
                'Q2': (x_min + (x_median - x_min) * (1 - offset), y_median + (y_max - y_median) * (1 - offset)),
                'Q3': (x_min + (x_median - x_min) * (1 - offset), y_min + (y_median - y_min) * offset),
                'Q4': (x_median + (x_max - x_median) * offset, y_min + (y_median - y_min) * offset)
            }
            
            for q, label in quadrant_labels.items():
                if q in label_positions:
                    ax.text(label_positions[q][0], label_positions[q][1], label,
                           fontsize=self.config.label_size, fontweight='bold',
                           alpha=0.5, ha='left', va='top')
        
        ax.set_xlabel(x_label or x_var, fontsize=self.config.label_size)
        ax.set_ylabel(y_label or y_var, fontsize=self.config.label_size)
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Strategy position map saved to: {output_path}")
        
        self.figures['position_map'] = fig
        return fig
    
    def create_performance_decomposition(self,
                                       components: Dict[str, float],
                                       component_labels: Optional[Dict[str, str]] = None,
                                       title: str = "パフォーマンスの分解",
                                       output_path: Optional[str] = None) -> plt.Figure:
        """
        パフォーマンス分解図の作成（Waterfall Chart Style）
        
        Visualizes how different components contribute to overall performance.
        
        Parameters:
        -----------
        components : Dict[str, float]
            構成要素と値 {'component_name': value}
        component_labels : Dict[str, str], optional
            日本語ラベル
        title : str
            図のタイトル
        output_path : str, optional
            保存先パス
        
        Returns:
        --------
        plt.Figure
            作成された図
        """
        fig, ax = plt.subplots(figsize=(12, 6), dpi=self.config.dpi)
        
        # Prepare data
        labels = list(components.keys())
        values = list(components.values())
        cumulative = np.cumsum([0] + values)
        
        # Create waterfall chart
        colors = [WONG_PALETTE['green'] if v > 0 else WONG_PALETTE['vermillion']
                 for v in values]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            ax.bar(i, value, bottom=cumulative[i], color=colors[i], alpha=0.7,
                  edgecolor='black', linewidth=1)
            
            # Add value labels
            y_pos = cumulative[i] + value / 2
            ax.text(i, y_pos, f"{value:.2f}",
                   ha='center', va='center',
                   fontsize=self.config.legend_size,
                   fontweight='bold')
        
        # Add total bar
        total = sum(values)
        ax.bar(len(labels), total, color=WONG_PALETTE['blue'], alpha=0.7,
              edgecolor='black', linewidth=2)
        ax.text(len(labels), total / 2, f"Total\n{total:.2f}",
               ha='center', va='center',
               fontsize=self.config.legend_size,
               fontweight='bold')
        
        # Formatting
        ax.set_xticks(range(len(labels) + 1))
        ax.set_xticklabels(labels + ['Total'], rotation=45, ha='right')
        ax.set_ylabel('Contribution', fontsize=self.config.label_size)
        ax.set_title(title, fontsize=self.config.title_size, fontweight='bold')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if output_path:
            fig.savefig(output_path, dpi=self.config.dpi,
                       bbox_inches='tight',
                       transparent=self.config.transparent_background)
            print(f"✓ Performance decomposition saved to: {output_path}")
        
        self.figures['performance_decomp'] = fig
        return fig
    
    def close_all(self):
        """すべての図を閉じる"""
        plt.close('all')
        self.figures.clear()

# ==============================================================================
# Command-Line Interface
# ==============================================================================

def main():
    """
    メインエントリポイント
    
    Example Usage:
    -------------
    python strategic_visualizer.py --type framework --config viz_config.yaml --output figures/
    """
    parser = argparse.ArgumentParser(
        description="Strategic Visualizer: 戦略研究特化型可視化システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Visualization Types:
  framework          Theoretical framework diagram
  interaction        Interaction/moderation plot
  mediation          Mediation analysis diagram
  panel              Panel data trajectory plot
  position           Strategic positioning map
  decomposition      Performance decomposition chart

Examples:
  # Create theoretical framework
  python strategic_visualizer.py --type framework --config framework.yaml --output figures/framework.png
  
  # Create interaction plot from data
  python strategic_visualizer.py --type interaction --data results.csv --x capability --y performance --mod uncertainty --output figures/interaction.png

For detailed documentation, see USAGE_GUIDE.md
        """
    )
    
    parser.add_argument('--type', type=str, required=True,
                       choices=['framework', 'interaction', 'mediation', 'panel', 'position', 'decomposition'],
                       help='Visualization type')
    parser.add_argument('--config', type=str,
                       help='Configuration file (YAML/JSON)')
    parser.add_argument('--data', type=str,
                       help='Data file (CSV) for data-driven visualizations')
    parser.add_argument('--output', type=str, required=True,
                       help='Output file path')
    parser.add_argument('--dpi', type=int, default=300,
                       help='Figure DPI (default: 300)')
    parser.add_argument('--title', type=str,
                       help='Custom figure title')
    
    # Interaction plot specific
    parser.add_argument('--x', type=str, help='X variable for interaction plot')
    parser.add_argument('--y', type=str, help='Y variable for interaction plot')
    parser.add_argument('--mod', type=str, help='Moderator variable for interaction plot')
    
    args = parser.parse_args()
    
    try:
        # Initialize visualizer
        config = VisualizationConfig(dpi=args.dpi)
        viz = StrategicVisualizer(config=config)
        
        # Create visualization based on type
        if args.type == 'framework':
            if not args.config:
                raise ValueError("Configuration file required for framework visualization")
            
            with open(args.config, 'r') as f:
                if args.config.endswith('.yaml') or args.config.endswith('.yml'):
                    viz_config = yaml.safe_load(f)
                else:
                    viz_config = json.load(f)
            
            viz.create_theoretical_framework(
                constructs=viz_config.get('constructs', []),
                relationships=viz_config.get('relationships', []),
                title=args.title or viz_config.get('title', '理論的フレームワーク'),
                output_path=args.output
            )
        
        elif args.type == 'interaction':
            if not args.data or not all([args.x, args.y, args.mod]):
                raise ValueError("Data file and variables (--x, --y, --mod) required for interaction plot")
            
            data = pd.read_csv(args.data)
            viz.create_interaction_plot(
                data=data,
                x_var=args.x,
                y_var=args.y,
                moderator=args.mod,
                title=args.title or "調整効果の可視化",
                output_path=args.output
            )
        
        # Add other visualization types as needed...
        
        print("\n" + "="*70)
        print("Strategic Visualization Complete")
        print("="*70)
        print(f"Output: {args.output}")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
