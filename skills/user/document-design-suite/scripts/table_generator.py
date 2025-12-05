#!/usr/bin/env python3
"""
Table Craftsman - プロフェッショナル表生成スクリプト

多様な用途（学術論文、プレゼンテーション、ビジネス文書、一般文書）に
対応した高品質な表を生成する。

Usage:
    from table_generator import TableCraftsman

    table = TableCraftsman(data, style='academic')
    table.to_html('output.html')
    table.to_pdf('output.pdf')

Author: Research Project
Version: 1.0.0
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    from jinja2 import Template
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False


class TableCraftsman:
    """プロフェッショナル表生成クラス"""

    STYLES = ['academic', 'presentation', 'business', 'minimal']
    SIZES = ['auto', 'a4', '16:9', '4:3', 'custom']
    FORMATS = ['html', 'pdf', 'png', 'markdown']

    def __init__(
        self,
        data: Union[Dict, List, 'pd.DataFrame', None] = None,
        style: str = 'minimal',
        size: str = 'auto',
        theme: str = 'light'
    ):
        """
        初期化

        Args:
            data: 表データ（dict, list, DataFrame）
            style: スタイル名（academic, presentation, business, minimal）
            size: サイズ（auto, a4, 16:9, 4:3, custom）
            theme: テーマ（light, dark）
        """
        self.style = style if style in self.STYLES else 'minimal'
        self.size = size if size in self.SIZES else 'auto'
        self.theme = theme

        self.headers: List[str] = []
        self.rows: List[List[str]] = []
        self.alignments: Dict[str, str] = {}
        self.title: str = ''
        self.table_number: str = ''
        self.notes: Dict[str, str] = {}
        self.highlights: List[Tuple[int, int, str]] = []
        self.column_widths: Dict[int, str] = {}
        self.css_classes: List[str] = []

        if data is not None:
            self._parse_data(data)

        self._base_path = Path(__file__).parent.parent
        self._styles_path = self._base_path / 'styles'
        self._templates_path = self._base_path / 'templates'

    def _parse_data(self, data: Union[Dict, List, 'pd.DataFrame']) -> None:
        """データをパース"""
        if HAS_PANDAS and isinstance(data, pd.DataFrame):
            self.headers = list(data.columns)
            self.rows = data.astype(str).values.tolist()
        elif isinstance(data, dict):
            if 'headers' in data:
                self.headers = data['headers']
                self.rows = data.get('rows', [])
            else:
                self.headers = list(data.keys())
                max_len = max(len(v) if isinstance(v, list) else 1 for v in data.values())
                self.rows = []
                for i in range(max_len):
                    row = []
                    for h in self.headers:
                        vals = data[h]
                        if isinstance(vals, list) and i < len(vals):
                            row.append(str(vals[i]))
                        elif not isinstance(vals, list) and i == 0:
                            row.append(str(vals))
                        else:
                            row.append('')
                    self.rows.append(row)
        elif isinstance(data, list):
            if len(data) > 0:
                if isinstance(data[0], dict):
                    self.headers = list(data[0].keys())
                    self.rows = [[str(row.get(h, '')) for h in self.headers] for row in data]
                else:
                    self.headers = [f'Col{i+1}' for i in range(len(data[0]))]
                    self.rows = [[str(cell) for cell in row] for row in data]

    def set_data(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> 'TableCraftsman':
        """データを直接設定"""
        self.headers = headers
        self.rows = [[str(cell) for cell in row] for row in rows]
        return self

    def set_title(
        self,
        table_number: str = '',
        title: str = ''
    ) -> 'TableCraftsman':
        """表タイトルを設定"""
        self.table_number = table_number
        self.title = title
        return self

    def set_alignment(
        self,
        alignments: Dict[str, str]
    ) -> 'TableCraftsman':
        """
        列の配置を設定

        Args:
            alignments: {'列名': 'left'|'center'|'right'}
        """
        self.alignments = alignments
        return self

    def add_note(
        self,
        note_type: str,
        content: str
    ) -> 'TableCraftsman':
        """
        注釈を追加

        Args:
            note_type: 'general', 'specific', 'probability'
            content: 注釈内容
        """
        self.notes[note_type] = content
        return self

    def highlight_cells(
        self,
        cells: List[Tuple[int, int]],
        color: str = '#fff3cd'
    ) -> 'TableCraftsman':
        """
        セルをハイライト

        Args:
            cells: [(行, 列), ...] 0-indexed
            color: ハイライト色
        """
        for row, col in cells:
            self.highlights.append((row, col, color))
        return self

    def add_css_class(self, class_name: str) -> 'TableCraftsman':
        """CSSクラスを追加"""
        self.css_classes.append(class_name)
        return self

    def set_column_width(
        self,
        col: int,
        width: str
    ) -> 'TableCraftsman':
        """列幅を設定（例: '100px', '20%'）"""
        self.column_widths[col] = width
        return self

    def _get_cell_class(self, row_idx: int, col_idx: int, value: str) -> str:
        """セルのCSSクラスを取得"""
        classes = []

        # 配置
        if col_idx < len(self.headers):
            header = self.headers[col_idx]
            if header in self.alignments:
                align = self.alignments[header]
                if align == 'right':
                    classes.append('numeric')
                elif align == 'center':
                    classes.append('center')

        # 数値判定（自動）
        if not classes:
            try:
                float(value.replace(',', '').replace('%', ''))
                classes.append('numeric')
            except (ValueError, AttributeError):
                pass

        # ハイライト
        for h_row, h_col, _ in self.highlights:
            if h_row == row_idx and h_col == col_idx:
                classes.append('highlight')

        return ' '.join(classes)

    def _get_cell_style(self, row_idx: int, col_idx: int) -> str:
        """セルのインラインスタイルを取得"""
        styles = []

        # ハイライト色
        for h_row, h_col, color in self.highlights:
            if h_row == row_idx and h_col == col_idx:
                styles.append(f'background-color: {color}')

        return '; '.join(styles)

    def _load_css(self) -> str:
        """スタイルシートを読み込み"""
        css_file = self._styles_path / f'{self.style}.css'
        if css_file.exists():
            return css_file.read_text(encoding='utf-8')
        return ''

    def _generate_html(self) -> str:
        """HTML生成"""
        css = self._load_css()

        # クラス構築
        container_classes = ['table-container', self.style]
        table_classes = ['craftsman-table', self.style]
        figure_classes = ['table-figure', self.style]

        if self.theme:
            container_classes.append(self.theme)
            table_classes.append(self.theme)

        for cls in self.css_classes:
            container_classes.append(cls)
            table_classes.append(cls)

        # サイズ設定
        container_style = ''
        if self.size == '16:9':
            container_classes.append('ratio-16-9')
        elif self.size == '4:3':
            container_classes.append('ratio-4-3')
        elif self.size == 'a4':
            container_classes.append('a4')

        # ヘッダー生成
        header_html = '<tr>'
        for i, h in enumerate(self.headers):
            th_class = self._get_cell_class(-1, i, h)
            th_style = f' width="{self.column_widths[i]}"' if i in self.column_widths else ''
            header_html += f'<th class="{th_class}"{th_style}>{h}</th>'
        header_html += '</tr>'

        # ボディ生成
        body_html = ''
        for row_idx, row in enumerate(self.rows):
            body_html += '<tr>'
            for col_idx, cell in enumerate(row):
                td_class = self._get_cell_class(row_idx, col_idx, cell)
                td_style = self._get_cell_style(row_idx, col_idx)
                style_attr = f' style="{td_style}"' if td_style else ''
                body_html += f'<td class="{td_class}"{style_attr}>{cell}</td>'
            body_html += '</tr>'

        # 注釈生成
        notes_html = ''
        if self.notes:
            notes_html = f'<div class="table-notes {self.style}">'
            if 'general' in self.notes:
                notes_html += f'<p class="note-general"><em>Note.</em> {self.notes["general"]}</p>'
            if 'specific' in self.notes:
                notes_html += f'<p class="note-specific">{self.notes["specific"]}</p>'
            if 'probability' in self.notes:
                notes_html += f'<p class="note-probability">{self.notes["probability"]}</p>'
            notes_html += '</div>'

        # キャプション
        caption_html = ''
        if self.table_number or self.title:
            caption_html = '<figcaption class="table-caption">'
            if self.table_number:
                caption_html += f'<span class="table-number">{self.table_number}</span>'
            if self.title:
                caption_html += f'<span class="table-title">{self.title}</span>'
            caption_html += '</figcaption>'

        html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{self.title or "Table"}</title>
  <style>
{css}
  </style>
</head>
<body>
  <div class="{' '.join(container_classes)}"{f' style="{container_style}"' if container_style else ''}>
    <figure class="{' '.join(figure_classes)}">
      {caption_html}
      <table class="{' '.join(table_classes)}">
        <thead>
          {header_html}
        </thead>
        <tbody>
          {body_html}
        </tbody>
      </table>
      {notes_html}
    </figure>
  </div>
</body>
</html>'''

        return html

    def _generate_markdown(self) -> str:
        """Markdown生成"""
        lines = []

        # タイトル
        if self.table_number or self.title:
            title_parts = []
            if self.table_number:
                title_parts.append(f'**{self.table_number}**')
            if self.title:
                title_parts.append(self.title)
            lines.append(' '.join(title_parts))
            lines.append('')

        # ヘッダー
        lines.append('| ' + ' | '.join(self.headers) + ' |')

        # 区切り線（配置対応）
        separators = []
        for i, h in enumerate(self.headers):
            align = self.alignments.get(h, 'left')
            if align == 'center':
                separators.append(':---:')
            elif align == 'right':
                separators.append('---:')
            else:
                separators.append('---')
        lines.append('| ' + ' | '.join(separators) + ' |')

        # データ行
        for row in self.rows:
            lines.append('| ' + ' | '.join(row) + ' |')

        # 注釈
        if self.notes:
            lines.append('')
            if 'general' in self.notes:
                lines.append(f'*Note.* {self.notes["general"]}')
            if 'specific' in self.notes:
                lines.append(self.notes['specific'])
            if 'probability' in self.notes:
                lines.append(self.notes['probability'])

        return '\n'.join(lines)

    def to_html(self, path: Optional[str] = None) -> str:
        """
        HTML出力

        Args:
            path: 保存先パス（Noneの場合は文字列を返す）

        Returns:
            HTML文字列
        """
        html = self._generate_html()
        if path:
            Path(path).write_text(html, encoding='utf-8')
        return html

    def to_markdown(self, path: Optional[str] = None) -> str:
        """
        Markdown出力

        Args:
            path: 保存先パス（Noneの場合は文字列を返す）

        Returns:
            Markdown文字列
        """
        md = self._generate_markdown()
        if path:
            Path(path).write_text(md, encoding='utf-8')
        return md

    def to_pdf(self, path: str, engine: str = 'weasyprint') -> None:
        """
        PDF出力

        Args:
            path: 保存先パス
            engine: 'weasyprint' または 'puppeteer'
        """
        html = self._generate_html()
        html_path = Path(path).with_suffix('.html')
        html_path.write_text(html, encoding='utf-8')

        if engine == 'weasyprint':
            try:
                from weasyprint import HTML
                HTML(string=html).write_pdf(path)
            except ImportError:
                raise ImportError("weasyprint が必要です: pip install weasyprint")
        elif engine == 'puppeteer':
            self._puppeteer_pdf(str(html_path), path)
        else:
            raise ValueError(f"Unknown engine: {engine}")

    def to_png(
        self,
        path: str,
        width: int = 1920,
        height: int = 1080
    ) -> None:
        """
        PNG出力

        Args:
            path: 保存先パス
            width: 画像幅
            height: 画像高さ
        """
        html = self._generate_html()
        html_path = Path(path).with_suffix('.html')
        html_path.write_text(html, encoding='utf-8')
        self._puppeteer_screenshot(str(html_path), path, width, height)

    def _puppeteer_pdf(self, html_path: str, pdf_path: str) -> None:
        """Puppeteerを使用してPDF生成"""
        js_code = f'''
const puppeteer = require('puppeteer');
(async () => {{
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('file://{Path(html_path).absolute()}', {{waitUntil: 'networkidle0'}});
    await page.pdf({{
        path: '{pdf_path}',
        format: 'A4',
        printBackground: true,
        margin: {{top: '20mm', bottom: '20mm', left: '20mm', right: '20mm'}}
    }});
    await browser.close();
}})();
'''
        subprocess.run(['node', '-e', js_code], check=True)

    def _puppeteer_screenshot(
        self,
        html_path: str,
        png_path: str,
        width: int,
        height: int
    ) -> None:
        """Puppeteerを使用してスクリーンショット生成"""
        js_code = f'''
const puppeteer = require('puppeteer');
(async () => {{
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport({{width: {width}, height: {height}}});
    await page.goto('file://{Path(html_path).absolute()}', {{waitUntil: 'networkidle0'}});
    await page.screenshot({{path: '{png_path}', fullPage: false}});
    await browser.close();
}})();
'''
        subprocess.run(['node', '-e', js_code], check=True)


# 便利関数
def create_academic_table(
    data: Any,
    table_number: str = 'Table 1',
    title: str = '',
    note: str = ''
) -> TableCraftsman:
    """学術論文用表を簡単に作成"""
    table = TableCraftsman(data, style='academic')
    table.set_title(table_number, title)
    if note:
        table.add_note('general', note)
    return table


def create_presentation_table(
    data: Any,
    title: str = '',
    theme: str = 'light'
) -> TableCraftsman:
    """プレゼンテーション用表を簡単に作成"""
    table = TableCraftsman(data, style='presentation', size='16:9', theme=theme)
    if title:
        table.set_title('', title)
    return table


def create_business_table(
    data: Any,
    title: str = '',
    color: str = 'blue'
) -> TableCraftsman:
    """ビジネス文書用表を簡単に作成"""
    table = TableCraftsman(data, style='business')
    if title:
        table.set_title('', title)
    table.add_css_class('striped')
    if color != 'blue':
        table.add_css_class(color)
    return table


if __name__ == '__main__':
    # サンプル実行
    sample_data = {
        'headers': ['変数', 'N', 'M', 'SD'],
        'rows': [
            ['年齢', '120', '34.5', '8.2'],
            ['経験年数', '120', '5.3', '3.1'],
            ['年収（万円）', '118', '450.2', '120.5'],
        ]
    }

    # 学術論文用
    academic = create_academic_table(
        sample_data,
        'Table 1',
        '記述統計量',
        'N = サンプルサイズ, M = 平均, SD = 標準偏差'
    )
    academic.set_alignment({'N': 'right', 'M': 'right', 'SD': 'right'})
    print(academic.to_markdown())
