FROM python:3.10-slim

WORKDIR /app

COPY api_server ./api_server
COPY requirements.txt .

RUN chmod +x ./api_server/PeakSearch
RUN pip install -r requirements.txt

ENV FLASK_APP=api_server.Conograph_API
ENV FLASK_RUN_PORT=8000
ENV FLASK_DEBUG=0

CMD ["python", "api_server/Conograph_API.py"]



