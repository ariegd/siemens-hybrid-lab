FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias necesarias
RUN pip install --no-cache-dir paho-mqtt requests

COPY main.py .

CMD ["python", "-u", "main.py"]
