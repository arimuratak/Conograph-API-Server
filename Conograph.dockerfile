FROM python:3.10-slim

# 作業ディレクトリを変更
WORKDIR /app/api_server

# 必要なファイルをコピー
COPY ./api_server ./        # ← ここでカレントにコピーされるようにする
COPY requirements.txt ../requirements.txt

# 実行ファイルに実行権限を与える（相対パスが変わる点に注意）
RUN chmod +x ./PeakSearch

RUN pip install -r ../requirements.txt

ENV PORT=8000

CMD ["python", "Conograph_API.py"]


