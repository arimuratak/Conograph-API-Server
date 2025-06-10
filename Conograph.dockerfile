FROM python:3.10-slim

# 作業ディレクトリを明示的に /app に設定
WORKDIR /app

# ✅ api_server フォルダを /app/api_server にコピー
COPY api_server ./api_server
COPY requirements.txt .

# ✅ 実行ファイルに絶対パスで実行権限を与える（renderで反映されやすい）
RUN chmod +x /app/api_server/PeakSearch

# ✅ Pythonパッケージのインストール
RUN pip install -r requirements.txt

# ✅ Flask の再起動誤動作を防ぐための環境変数
ENV FLASK_APP=api_server.Conograph_API
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=0

# ✅ 確実なパスで実行（api_serverが2重にならないように）
CMD ["python", "api_server/Conograph_API.py"]



