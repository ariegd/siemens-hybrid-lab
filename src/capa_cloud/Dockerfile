FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app2.py .

EXPOSE 8000

# Usar Gunicorn como servidor WSGI de producción en lugar del servidor dev de Flask
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8000", "app2:app"]
