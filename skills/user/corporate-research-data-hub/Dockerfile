# Corporate Research Data Hub - Docker Environment
# =================================================
# 完全な環境再現性を担保するためのDockerコンテナ
#
# Build:
#   docker build -t corporate-research-hub:2.0 .
#
# Run:
#   docker run -it -v $(pwd)/data:/workspace/data corporate-research-hub:2.0

FROM python:3.10-slim

# メタデータ
LABEL maintainer="Corporate Research Data Hub"
LABEL version="2.0"
LABEL description="Reproducible research environment for corporate empirical research"

# システムパッケージ
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    curl \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /workspace

# Python依存関係（固定バージョン）
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# プロジェクトファイル
COPY . /workspace/

# 環境変数（再現性）
ENV PYTHONHASHSEED=42
ENV PYTHONUNBUFFERED=1
ENV CUBLAS_WORKSPACE_CONFIG=:4096:8

# データディレクトリ作成
RUN mkdir -p /workspace/data/raw \
             /workspace/data/clean \
             /workspace/results \
             /workspace/reports

# 実行権限
RUN chmod +x scripts/*.py 2>/dev/null || true

# デフォルトコマンド
CMD ["/bin/bash"]
