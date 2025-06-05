FROM python:3.10-slim

WORKDIR /app

COPY api_server ./api_server
COPY requirements.txt .

# 実行権限を付与
RUN chmod +x ./api_server/work/PeakSearch

# 必要なパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# Render用ポート
ENV PORT=8000

CMD ["python", "./api_server/Conograph_api.py"]
