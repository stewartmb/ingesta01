# Dockerfile para ingesta desde PostgreSQL
FROM python:3-slim
WORKDIR /app
COPY ingesta01.py .
RUN pip3 install psycopg2-binary boto3
CMD ["python3", "ingesta01.py"]
