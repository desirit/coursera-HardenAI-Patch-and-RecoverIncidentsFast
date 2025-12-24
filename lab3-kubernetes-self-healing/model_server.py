"""
Model Server with Kubernetes Health Probes and Prometheus Metrics

This Flask application demonstrates:
- Liveness probes (is the container alive?)
- Readiness probes (is the container ready for traffic?)
- Prometheus metrics endpoint

Environment Variables:
  MODEL_VERSION - Version string (default: v1.0)
  DEGRADED      - Whether model is in degraded state (default: false)

Endpoints:
  /health   - Liveness probe
  /ready    - Readiness probe
  /metrics  - Prometheus metrics
  /predict  - Model inference

Part of: Harden AI - Patch and Recover Incidents Fast (Coursera)
Lab 3: Kubernetes Self-Healing Systems
"""

from flask import Flask, jsonify, Response, request
import os
import time
import random
from datetime import datetime

app = Flask(__name__)

# Configuration from environment variables
MODEL_VERSION = os.environ.get('MODEL_VERSION', 'v1.0')
DEGRADED = os.environ.get('DEGRADED', 'false').lower() == 'true'


class Metrics:
    """Track service metrics for Prometheus."""

    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.latency_sum = 0.0
        self.latency_count = 0
        self.start_time = time.time()

    def record_request(self, latency_ms, success=True):
        self.request_count += 1
        self.latency_sum += latency_ms
        self.latency_count += 1
        if not success:
            self.error_count += 1

    def get_accuracy(self):
        """Simulated model accuracy based on version."""
        if DEGRADED:
            return 0.72 + random.uniform(-0.05, 0.05)  # v2: poor accuracy
        else:
            return 0.94 + random.uniform(-0.02, 0.02)  # v1: good accuracy

    def get_avg_latency(self):
        if self.latency_count == 0:
            return 0
        return self.latency_sum / self.latency_count

    def get_error_rate(self):
        if self.request_count == 0:
            return 0
        return self.error_count / self.request_count


metrics = Metrics()


# ==============================================================================
# HEALTH PROBES
# ==============================================================================

@app.route('/health')
def health_check():
    """
    LIVENESS PROBE

    Kubernetes uses this to determine if the container should be restarted.

    Returns:
        200: Container is healthy
        503: Container should be restarted
    """
    # In degraded mode, occasionally fail health check
    if DEGRADED and random.random() < 0.3:  # 30% failure rate
        return jsonify({
            'status': 'unhealthy',
            'reason': 'model inference failure',
            'version': MODEL_VERSION,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 503

    return jsonify({
        'status': 'healthy',
        'version': MODEL_VERSION,
        'uptime_seconds': int(time.time() - metrics.start_time),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200


@app.route('/ready')
def readiness_check():
    """
    READINESS PROBE

    Kubernetes uses this to determine if the pod should receive traffic.

    Returns:
        200: Pod is ready for traffic
        503: Pod should be removed from load balancer
    """
    accuracy = metrics.get_accuracy()
    avg_latency = metrics.get_avg_latency()

    # In degraded mode, fail readiness more often
    if DEGRADED and random.random() < 0.4:  # 40% unready
        return jsonify({
            'status': 'not_ready',
            'reason': 'high latency or error rate',
            'latency_ms': round(avg_latency, 1),
            'accuracy': round(accuracy, 3),
            'version': MODEL_VERSION,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 503

    return jsonify({
        'status': 'ready',
        'latency_ms': round(avg_latency, 1),
        'accuracy': round(accuracy, 3),
        'version': MODEL_VERSION,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200


# ==============================================================================
# PROMETHEUS METRICS
# ==============================================================================

@app.route('/metrics')
def prometheus_metrics():
    """
    Expose metrics in Prometheus text format.

    Prometheus scrapes this endpoint to collect metrics.
    """
    accuracy = metrics.get_accuracy()
    avg_latency = metrics.get_avg_latency()
    error_rate = metrics.get_error_rate()
    uptime = time.time() - metrics.start_time

    output = f"""# HELP model_accuracy Current model accuracy (0-1)
# TYPE model_accuracy gauge
model_accuracy{{version="{MODEL_VERSION}"}} {accuracy:.4f}

# HELP model_latency_ms Average inference latency in milliseconds
# TYPE model_latency_ms gauge
model_latency_ms{{version="{MODEL_VERSION}"}} {avg_latency:.2f}

# HELP model_error_rate Current error rate (0-1)
# TYPE model_error_rate gauge
model_error_rate{{version="{MODEL_VERSION}"}} {error_rate:.4f}

# HELP model_requests_total Total number of prediction requests
# TYPE model_requests_total counter
model_requests_total{{version="{MODEL_VERSION}"}} {metrics.request_count}

# HELP model_errors_total Total number of prediction errors
# TYPE model_errors_total counter
model_errors_total{{version="{MODEL_VERSION}"}} {metrics.error_count}

# HELP model_uptime_seconds Time since server started
# TYPE model_uptime_seconds gauge
model_uptime_seconds{{version="{MODEL_VERSION}"}} {uptime:.0f}

# HELP model_degraded Whether model is in degraded state (1=degraded, 0=healthy)
# TYPE model_degraded gauge
model_degraded{{version="{MODEL_VERSION}"}} {1 if DEGRADED else 0}
"""

    return Response(output, mimetype='text/plain')


# ==============================================================================
# INFERENCE ENDPOINT
# ==============================================================================

@app.route('/predict', methods=['POST'])
def predict():
    """Model inference endpoint."""
    start = time.time()

    # Simulate inference time
    if DEGRADED:
        time.sleep(random.uniform(0.15, 0.3))  # v2 is slow
        success = random.random() < 0.72  # 72% accuracy
    else:
        time.sleep(random.uniform(0.02, 0.05))  # v1 is fast
        success = random.random() < 0.94  # 94% accuracy

    latency_ms = (time.time() - start) * 1000
    metrics.record_request(latency_ms, success)

    return jsonify({
        'prediction': 'fraud' if random.random() > 0.5 else 'legitimate',
        'confidence': random.uniform(0.7, 0.99),
        'latency_ms': round(latency_ms, 1),
        'version': MODEL_VERSION,
        'success': success
    })


@app.route('/')
def index():
    """Root endpoint with server info."""
    return jsonify({
        'service': 'model-server',
        'version': MODEL_VERSION,
        'degraded': DEGRADED,
        'endpoints': {
            '/health': 'Liveness probe',
            '/ready': 'Readiness probe',
            '/metrics': 'Prometheus metrics',
            '/predict': 'Model inference (POST)'
        }
    })


if __name__ == '__main__':
    status = "DEGRADED" if DEGRADED else "HEALTHY"
    print("=" * 60)
    print(f"Model Server Starting")
    print(f"  Version: {MODEL_VERSION}")
    print(f"  Status:  {status}")
    print("=" * 60)
    print(f"  /health  - Liveness probe")
    print(f"  /ready   - Readiness probe")
    print(f"  /metrics - Prometheus metrics")
    print(f"  /predict - Inference endpoint")
    print("=" * 60)

    app.run(host='0.0.0.0', port=8080, debug=False)
