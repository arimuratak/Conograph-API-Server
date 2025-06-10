FROM python:3.10-slim

# WORKDIRはプロジェクトルート（ルートから見てapi_serverがある前提）
WORKDIR /app

# ✅ ここで api_server 配下のファイルを「そのまま」コピー
COPY api_server/ ./api_server
COPY requirements.txt .

# ✅ 実行ファイルのパス修正（api_server直下）
RUN chmod +x ./api_server/PeakSearch

RUN pip install -r requirements.txt

ENV PORT=8000

# ✅ CMDでは明示的にパス指定する（WORKDIRからの相対）
CMD ["python", "api_server/Conograph_API.py"]




