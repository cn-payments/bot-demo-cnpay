FROM python:3.11-slim

# Instala certificados CA para conexões TLS (MySQL via Railway usa TLS por proxy)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot_demo.py"] 