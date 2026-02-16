# Multi-stage build for Flask API Gateway
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

# Non-root user for security
RUN useradd -m -u 1000 apiuser

WORKDIR /app
COPY --from=builder /root/.local /home/apiuser/.local
COPY app.py powershell_executor.py ./
COPY config/ ./config/

RUN chown -R apiuser:apiuser /app
USER apiuser

ENV PATH=/home/apiuser/.local/bin:$PATH
ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
