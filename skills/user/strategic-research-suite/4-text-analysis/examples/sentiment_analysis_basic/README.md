# Sentiment Analysis Basic Example

## 概要
企業の決算説明会トランスクリプトのセンチメント分析の基本例です。

## 機能
- VADERセンチメント分析
- Loughran-McDonaldセンチメント分析
- 時系列トレンドの可視化

## 実行方法

```bash
cd 4-text-analysis/examples/sentiment_analysis_basic/
python3 analyze_earnings_calls.py
```

## 必要なライブラリ

```bash
pip install pandas numpy vaderSentiment matplotlib
```

## 出力ファイル
- `output/sentiment_analysis_results.csv`: 分析結果（CSV）
- `output/sentiment_trend.png`: センチメント推移グラフ

## 実行時間
約5秒（サンプルデータ4件）

## 次のステップ
実際のデータを使用する場合：
1. 決算説明会トランスクリプトをダウンロード（Seeking Alpha, Bloombergなど）
2. テキストファイルをCSV形式に変換
3. `df = pd.read_csv('your_transcripts.csv')` で読み込み
4. 同様に分析実行

## 参考文献
- VADER: Hutto & Gilbert (2014). "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text"
- Loughran-McDonald: https://sraf.nd.edu/loughranmcdonald-master-dictionary/
