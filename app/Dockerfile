# Python 3.11 の軽量イメージをベースに使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存パッケージファイルをコピー
COPY requirements.txt .

# Python パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# Flask が使用するポートを公開
EXPOSE 5000

# コンテナ起動時に Flask アプリを実行
CMD ["python", "app.py"]
