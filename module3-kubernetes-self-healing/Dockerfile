# Dockerfile for Model Server v1 (Stable)
# This version passes all health checks

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY model_server.py .

# Environment variables for stable version
ENV MODEL_VERSION=v1.0
ENV DEGRADED=false

EXPOSE 8080

# Health check at Docker level (K8s probes override this)
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "model_server.py"]
