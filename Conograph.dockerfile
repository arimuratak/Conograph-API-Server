FROM python:3.10-slim

WORKDIR /app/api_server

# 👇 api_server配下のファイル・フォルダを直接コピー（階層崩さない）
COPY api_server/ ./

# 👇 requirements.txt は1つ上に置く前提
COPY requirements.txt ../requirements.txt

# 👇 実行ファイルに権限付与（workは既に廃止）
RUN chmod +x ./PeakSearch

RUN pip install -r ../requirements.txt

ENV PORT=8000

# 👇 実行は現在のWORKDIRから直接指定
CMD ["python", "Conograph_API.py"]



