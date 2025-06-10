FROM python:3.10-slim

WORKDIR /app

COPY api_server ./api_server
COPY requirements.txt .

RUN chmod +x ./api_server/PeakSearch
RUN pip install -r requirements.txt

CMD ["python", "api_server/Conograph_API.py"]




