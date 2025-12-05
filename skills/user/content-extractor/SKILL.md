---
name: content-extractor
description: |
  URLからコンテンツを自動抽出する統合スキル（旧Tapestry）。以下の機能を包括：
  (1) YouTube動画のトランスクリプト取得
  (2) Web記事・ブログの本文抽出
  (3) PDFドキュメントのテキスト抽出
  (4) アクションプラン作成（Ship-Learn-Next形式）
  トリガー：「tapestry」「weave」「YouTube トランスクリプト」「記事抽出」「PDF抽出」「コンテンツ取得」
allowed-tools: Bash,Read,Write
---

# Content Extractor - コンテンツ抽出統合スキル

## 概要

URLからコンテンツを自動検出・抽出する統合スキルです。YouTube動画、Web記事、PDFドキュメントなど、様々なコンテンツタイプに対応し、クリーンなテキストとして保存します。

**統合元スキル**：
- tapestry（統合オーケストレーター）
- youtube-transcript（YouTube字幕取得）
- article-extractor（記事抽出）

## When to Use This Skill

以下の場合にこのスキルを使用：

- YouTube動画のトランスクリプト取得
- Web記事・ブログ記事の本文抽出
- PDFドキュメントのテキスト変換
- URLからのコンテンツ自動抽出

**トリガーキーワード**：
- 「tapestry [URL]」「weave [URL]」
- 「YouTube トランスクリプト」「字幕取得」
- 「記事抽出」「記事をダウンロード」
- 「PDFからテキスト」
- 「コンテンツ取得」「extract [URL]」

---

# Part 1: コンテンツタイプ自動検出

## 1.1 URL分析ロジック

```bash
URL="$1"

# YouTube検出
if [[ "$URL" =~ youtube\.com/watch || "$URL" =~ youtu\.be/ || "$URL" =~ youtube\.com/shorts ]]; then
    CONTENT_TYPE="youtube"

# PDF検出
elif [[ "$URL" =~ \.pdf$ ]]; then
    CONTENT_TYPE="pdf"

# PDFレスポンスヘッダーチェック
elif curl -sI "$URL" | grep -iq "Content-Type: application/pdf"; then
    CONTENT_TYPE="pdf"

# その他はArticle
else
    CONTENT_TYPE="article"
fi

echo "Detected: $CONTENT_TYPE"
```

## 1.2 サポートするコンテンツタイプ

| タイプ | パターン | 使用ツール |
|--------|----------|------------|
| YouTube | youtube.com/watch, youtu.be/ | yt-dlp |
| Article | http(s)://* (非YouTube, 非PDF) | reader, trafilatura |
| PDF | *.pdf, Content-Type: application/pdf | pdftotext |

---

# Part 2: YouTube トランスクリプト

## 2.1 基本ワークフロー

```bash
# 1. yt-dlpインストール確認
if ! command -v yt-dlp &> /dev/null; then
    echo "Installing yt-dlp..."
    brew install yt-dlp  # macOS
    # または: pip3 install yt-dlp
fi

# 2. 利用可能な字幕を確認
yt-dlp --list-subs "$VIDEO_URL"

# 3. 手動字幕を試行（高品質）
if yt-dlp --write-sub --skip-download --output "transcript" "$VIDEO_URL" 2>/dev/null; then
    echo "Manual subtitles downloaded"
else
    # 4. 自動生成字幕にフォールバック
    yt-dlp --write-auto-sub --skip-download --output "transcript" "$VIDEO_URL"
fi

# 5. テキストに変換（重複除去）
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > "${VIDEO_TITLE}.txt"

# 6. 一時ファイル削除
rm -f transcript.en.vtt
```

## 2.2 完全スクリプト

```bash
#!/bin/bash
# YouTube Transcript Downloader

VIDEO_URL="$1"

if [ -z "$VIDEO_URL" ]; then
    echo "Usage: youtube-transcript <URL>"
    exit 1
fi

# yt-dlp確認
if ! command -v yt-dlp &> /dev/null; then
    echo "Installing yt-dlp..."
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    else
        pip3 install yt-dlp
    fi
fi

# 動画タイトル取得
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')

echo "Downloading transcript for: $VIDEO_TITLE"

# 字幕ダウンロード
OUTPUT_NAME="temp_transcript"
if ! yt-dlp --write-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL" 2>/dev/null; then
    if ! yt-dlp --write-auto-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL" 2>/dev/null; then
        echo "Error: No subtitles available"
        exit 1
    fi
fi

# VTTファイルを検索
VTT_FILE=$(ls ${OUTPUT_NAME}*.vtt 2>/dev/null | head -n 1)
if [ -z "$VTT_FILE" ]; then
    echo "Error: No VTT file found"
    exit 1
fi

# テキスト変換（重複除去）
python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > "${VIDEO_TITLE}.txt"

# クリーンアップ
rm -f "$VTT_FILE"

echo "✓ Saved to: ${VIDEO_TITLE}.txt"
```

## 2.3 Whisper代替（字幕なしの場合）

```bash
# 字幕が利用できない場合のWhisper文字起こし
# ※事前にユーザー確認が必要

# 音声ダウンロード
yt-dlp -x --audio-format mp3 --output "audio_%(id)s.%(ext)s" "$VIDEO_URL"

# Whisper文字起こし
whisper audio_*.mp3 --model base --output_format txt

# クリーンアップ
rm -f audio_*.mp3
```

---

# Part 3: Web記事抽出

## 3.1 抽出ツールの優先順位

```
1. reader (Mozilla Readability) - 推奨
2. trafilatura - 高精度
3. curl + Python fallback - 依存なし
```

## 3.2 基本ワークフロー

```bash
ARTICLE_URL="$1"

# ツール確認
if command -v reader &> /dev/null; then
    TOOL="reader"
elif command -v trafilatura &> /dev/null; then
    TOOL="trafilatura"
else
    TOOL="fallback"
fi

echo "Using: $TOOL"

case $TOOL in
    reader)
        # Mozilla Readabilityベース
        reader "$ARTICLE_URL" > temp_article.txt
        TITLE=$(head -n 1 temp_article.txt | sed 's/^# //')
        ;;

    trafilatura)
        # Python抽出エンジン
        METADATA=$(trafilatura --URL "$ARTICLE_URL" --json)
        TITLE=$(echo "$METADATA" | python3 -c "import json, sys; print(json.load(sys.stdin).get('title', 'Article'))")
        trafilatura --URL "$ARTICLE_URL" --output-format txt --no-comments > temp_article.txt
        ;;

    fallback)
        # 基本的なHTML解析
        TITLE=$(curl -s "$ARTICLE_URL" | grep -oP '<title>\K[^<]+' | head -n 1)
        TITLE=${TITLE%% - *}
        curl -s "$ARTICLE_URL" | python3 -c "
from html.parser import HTMLParser
import sys

class ArticleExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.content = []
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'form'}
        self.in_content = False

    def handle_starttag(self, tag, attrs):
        if tag not in self.skip_tags and tag in {'p', 'article', 'main'}:
            self.in_content = True

    def handle_data(self, data):
        if self.in_content and data.strip():
            self.content.append(data.strip())

    def get_content(self):
        return '\n\n'.join(self.content)

parser = ArticleExtractor()
parser.feed(sys.stdin.read())
print(parser.get_content())
" > temp_article.txt
        ;;
esac

# ファイル名整形
FILENAME=$(echo "$TITLE" | tr '/' '-' | tr ':' '-' | tr '?' '' | tr '"' '' | cut -c 1-80 | sed 's/ *$//')
FILENAME="${FILENAME}.txt"
mv temp_article.txt "$FILENAME"

echo "✓ Saved to: $FILENAME"
```

## 3.3 ツールのインストール

```bash
# reader (npm)
npm install -g @anthropic-ai/reader-cli
# または
npm install -g reader-cli

# trafilatura (pip)
pip3 install trafilatura
```

---

# Part 4: PDF抽出

## 4.1 基本ワークフロー

```bash
PDF_URL="$1"

# PDFダウンロード
PDF_FILENAME=$(basename "$PDF_URL")
curl -L -o "$PDF_FILENAME" "$PDF_URL"

# テキスト抽出
if command -v pdftotext &> /dev/null; then
    pdftotext "$PDF_FILENAME" "${PDF_FILENAME%.pdf}.txt"
    echo "✓ Extracted: ${PDF_FILENAME%.pdf}.txt"
else
    echo "Warning: pdftotext not found"
    echo "Install with: brew install poppler (macOS)"
    echo "            : apt install poppler-utils (Linux)"
fi
```

## 4.2 pdftotext インストール

```bash
# macOS
brew install poppler

# Ubuntu/Debian
apt install poppler-utils

# Windows (Chocolatey)
choco install poppler
```

---

# Part 5: 統合Tapestryワークフロー

## 5.1 完全統合スクリプト

```bash
#!/bin/bash
# Tapestry: Unified Content Extraction

URL="$1"

if [ -z "$URL" ]; then
    echo "Usage: tapestry <URL>"
    exit 1
fi

echo "🧵 Tapestry Starting..."
echo "URL: $URL"
echo ""

# Step 1: コンテンツタイプ検出
if [[ "$URL" =~ youtube\.com/watch || "$URL" =~ youtu\.be/ || "$URL" =~ youtube\.com/shorts ]]; then
    CONTENT_TYPE="youtube"
elif [[ "$URL" =~ \.pdf$ ]] || curl -sI "$URL" | grep -iq "Content-Type: application/pdf"; then
    CONTENT_TYPE="pdf"
else
    CONTENT_TYPE="article"
fi

echo "📍 Detected: $CONTENT_TYPE"
echo ""

# Step 2: コンテンツ抽出
case $CONTENT_TYPE in
    youtube)
        echo "📺 Extracting YouTube transcript..."
        # [YouTube抽出コード]
        ;;

    article)
        echo "📄 Extracting article..."
        # [記事抽出コード]
        ;;

    pdf)
        echo "📑 Extracting PDF..."
        # [PDF抽出コード]
        ;;
esac

echo ""
echo "✅ Tapestry Complete!"
echo "📥 Content saved to: $CONTENT_FILE"
```

## 5.2 出力形式

```
✅ Tapestry Workflow Complete!

📥 Content Extracted:
   ✓ [Content type]: [Title]
   ✓ Saved to: [filename.txt]
   ✓ [X] words extracted

📋 Summary:
   [First 5 lines of content]
```

---

# Part 6: エラーハンドリング

## 6.1 よくある問題と対処

### yt-dlpがインストールされていない
```bash
# 自動インストール試行
if ! command -v yt-dlp &> /dev/null; then
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y yt-dlp
    else
        pip3 install yt-dlp
    fi
fi
```

### 字幕が利用できない
```
1. --list-subsで利用可能な言語を確認
2. 別言語の字幕を試行
3. Whisper文字起こしを提案（ユーザー確認後）
```

### 記事抽出が失敗
```
1. 代替ツールを試行（reader → trafilatura → fallback）
2. ペイウォール/ログイン要件の可能性を通知
3. JavaScriptが多いサイトの制限を説明
```

### PDFテキスト抽出が空
```
1. OCR PDFの可能性（画像ベース）
2. ocrmypdfなどのOCRツールを提案
3. 手動での代替方法を案内
```

---

# Part 7: 起動コマンド

## 基本使用
```
content-extractor [URL]
# または
tapestry [URL]
weave [URL]
```

## YouTube専用
```
youtube-transcript [YouTube URL]
```

## 記事専用
```
article-extract [Article URL]
```

## PDF専用
```
pdf-extract [PDF URL or file path]
```

---

## 依存関係

### 必須
- curl（組み込み）
- Python 3.x

### 推奨
- yt-dlp（YouTube用）
- reader または trafilatura（記事用）
- pdftotext（PDF用、popplerパッケージ）

### オプション
- whisper（字幕なしの場合）
- ocrmypdf（OCR PDF用）

---

## 連携スキル

| スキル名 | 役割 |
|----------|------|
| academic-research-suite | 文献レビュー・論文執筆・引用管理 |
| thinking-toolkit | 抽出コンテンツの分析・理論構築 |
| strategic-research-platform | 研究デザイン・統計分析 |
| document-design-suite | 可視化・図表作成 |

---

**バージョン**: 1.0.0
**統合日**: 2025-11-28
**統合元**: tapestry, youtube-transcript, article-extractor
