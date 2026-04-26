# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY deploy/requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY source/ /app/

EXPOSE 5000

CMD ["python", "app.py"]
