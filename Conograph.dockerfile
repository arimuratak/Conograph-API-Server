FROM python:3.10-slim

WORKDIR /app

# api_server フォルダをまとめてコピー
COPY ./api_server ./api_server

RUN chmod +x ./api_server/PeakSearch
COPY requirements.txt .

RUN pip install -r requirements.txt

ENV PORT=8000

# 実行ファイルの位置を正しく指定！
CMD ["python", "./api_server/Conograph_API.py"]

