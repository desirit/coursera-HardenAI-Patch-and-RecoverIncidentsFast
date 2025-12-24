"""
app.py - Canary Deployment Router for ML Models

This Flask application demonstrates canary deployment patterns:
- Traffic splitting between production and canary models
- Real-time metrics tracking (accuracy, latency)
- Automatic rollback when canary performance degrades

Part of: Harden AI - Patch and Recover Incidents Fast (Coursera)
Lab 1: Canary Deployments for ML Models
"""

from flask import Flask, request, jsonify
import mlflow
import random
import time
from datetime import datetime

app = Flask(__name__)

# ============================================================
# MLFLOW MODEL LOADING
# ============================================================
mlflow.set_tracking_uri("http://127.0.0.1:5001")

print("Loading models from MLflow...")
production_model = mlflow.pyfunc.load_model("models:/sentiment/Production")
canary_model = mlflow.pyfunc.load_model("models:/sentiment/Staging")
print("Models loaded successfully!")

# ============================================================
# CANARY CONFIGURATION
# ============================================================
CANARY_PERCENTAGE = 20  # Percentage of traffic routed to canary model

# Rollback thresholds - trigger rollback if canary performance drops below these
ACCURACY_THRESHOLD = 85  # Minimum accuracy percentage
LATENCY_THRESHOLD = 100  # Maximum P95 latency in milliseconds

# ============================================================
# METRICS TRACKING
# ============================================================
metrics = {
    "production": {"requests": 0, "correct": 0, "latencies": []},
    "canary": {"requests": 0, "correct": 0, "latencies": []}
}

# For demonstration: simulate canary failure
SIMULATE_CANARY_FAILURE = False


# ============================================================
# CORE ROUTING LOGIC
# ============================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint with canary routing.

    The routing decision is simple:
    - Generate a random number between 0-100
    - If less than CANARY_PERCENTAGE, route to canary
    - Otherwise, route to production
    """
    global CANARY_PERCENTAGE

    data = request.json
    text = data.get('text', '')
    actual_label = data.get('actual_label')  # For accuracy tracking

    start_time = time.time()

    # CANARY ROUTING DECISION
    if random.random() * 100 < CANARY_PERCENTAGE:
        model_version = "canary"
        model = canary_model
    else:
        model_version = "production"
        model = production_model

    # Make prediction
    try:
        prediction = model.predict([text])[0]

        # Simulate failure for demonstration
        if SIMULATE_CANARY_FAILURE and model_version == "canary":
            if random.random() > 0.6:  # 40% wrong predictions
                prediction = 1 - prediction

    except Exception as e:
        prediction = -1

    # Calculate latency
    latency_ms = (time.time() - start_time) * 1000

    # Track metrics
    metrics[model_version]["requests"] += 1
    metrics[model_version]["latencies"].append(latency_ms)

    if actual_label is not None:
        if prediction == actual_label:
            metrics[model_version]["correct"] += 1

    # Log for terminal visibility
    icon = "[CANARY]" if model_version == "canary" else "[PROD]  "
    print(f"{icon} Prediction: {prediction} | Latency: {latency_ms:.1f}ms")

    return jsonify({
        'prediction': int(prediction),
        'model_version': model_version,
        'latency_ms': round(latency_ms, 2)
    })


# ============================================================
# METRICS ENDPOINT
# ============================================================
@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Return current metrics for both model versions."""
    result = {}

    for version in ["production", "canary"]:
        m = metrics[version]
        total = m["requests"]
        correct = m["correct"]

        accuracy = (correct / total * 100) if total > 0 else 0
        avg_latency = sum(m["latencies"]) / len(m["latencies"]) if m["latencies"] else 0

        result[version] = {
            "requests": total,
            "accuracy": round(accuracy, 1),
            "avg_latency_ms": round(avg_latency, 1)
        }

    result["canary_percentage"] = CANARY_PERCENTAGE
    return jsonify(result)


# ============================================================
# ROLLBACK CHECK - AUTOMATIC PROTECTION
# ============================================================
@app.route('/check_rollback', methods=['POST'])
def check_rollback():
    """
    Check if canary metrics warrant a rollback.

    Rollback is triggered when:
    - Canary accuracy drops below ACCURACY_THRESHOLD
    - (Optional) Canary latency exceeds LATENCY_THRESHOLD
    """
    global CANARY_PERCENTAGE

    canary_metrics = metrics["canary"]

    if canary_metrics["requests"] < 5:
        return jsonify({"status": "waiting", "message": "Not enough data yet"})

    accuracy = (canary_metrics["correct"] / canary_metrics["requests"]) * 100

    if accuracy < ACCURACY_THRESHOLD:
        # TRIGGER ROLLBACK
        old_percentage = CANARY_PERCENTAGE
        CANARY_PERCENTAGE = 0

        message = f"ROLLBACK TRIGGERED! Canary accuracy {accuracy:.1f}% < {ACCURACY_THRESHOLD}% threshold"
        print("\n" + "=" * 60)
        print(message)
        print(f"Canary traffic: {old_percentage}% -> 0%")
        print("All traffic now routed to Production")
        print("=" * 60 + "\n")

        return jsonify({
            "status": "rollback",
            "reason": "accuracy_below_threshold",
            "canary_accuracy": round(accuracy, 1),
            "threshold": ACCURACY_THRESHOLD
        })

    return jsonify({
        "status": "healthy",
        "canary_accuracy": round(accuracy, 1)
    })


# ============================================================
# CONTROL ENDPOINTS
# ============================================================
@app.route('/set_canary/<int:percentage>', methods=['POST'])
def set_canary_percentage(percentage):
    """Adjust the canary traffic percentage (0-100)."""
    global CANARY_PERCENTAGE
    old = CANARY_PERCENTAGE
    CANARY_PERCENTAGE = min(100, max(0, percentage))
    print(f"\nCanary percentage changed: {old}% -> {CANARY_PERCENTAGE}%\n")
    return jsonify({"canary_percentage": CANARY_PERCENTAGE})


@app.route('/simulate_failure/<int:enable>', methods=['POST'])
def toggle_failure(enable):
    """Toggle canary failure simulation (for demonstration)."""
    global SIMULATE_CANARY_FAILURE
    SIMULATE_CANARY_FAILURE = bool(enable)
    status = "ENABLED" if enable else "DISABLED"
    print(f"\nFailure simulation: {status}\n")
    return jsonify({"simulate_failure": SIMULATE_CANARY_FAILURE})


@app.route('/reset', methods=['POST'])
def reset_metrics():
    """Reset all metrics and settings to initial state."""
    global metrics, CANARY_PERCENTAGE, SIMULATE_CANARY_FAILURE
    metrics = {
        "production": {"requests": 0, "correct": 0, "latencies": []},
        "canary": {"requests": 0, "correct": 0, "latencies": []}
    }
    CANARY_PERCENTAGE = 20
    SIMULATE_CANARY_FAILURE = False
    print("\nMetrics and settings reset (canary at 20%)\n")
    return jsonify({"status": "reset"})


# ============================================================
# STATUS PAGE
# ============================================================
@app.route('/', methods=['GET'])
def status():
    """Display current system status."""
    return f"""
    <h1>Canary Deployment Lab</h1>
    <h2>Current Configuration</h2>
    <ul>
        <li><b>Canary Traffic:</b> {CANARY_PERCENTAGE}%</li>
        <li><b>Production Traffic:</b> {100 - CANARY_PERCENTAGE}%</li>
        <li><b>Accuracy Threshold:</b> {ACCURACY_THRESHOLD}%</li>
        <li><b>Failure Simulation:</b> {'ON' if SIMULATE_CANARY_FAILURE else 'OFF'}</li>
    </ul>
    <h2>Endpoints</h2>
    <ul>
        <li><code>POST /predict</code> - Make prediction</li>
        <li><code>GET /metrics</code> - View metrics</li>
        <li><code>POST /check_rollback</code> - Check rollback trigger</li>
        <li><code>POST /set_canary/&lt;n&gt;</code> - Set canary %</li>
        <li><code>POST /simulate_failure/1</code> - Enable failure</li>
        <li><code>POST /reset</code> - Reset everything</li>
    </ul>
    """


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("CANARY DEPLOYMENT LAB SERVER")
    print("=" * 60)
    print(f"Canary Traffic: {CANARY_PERCENTAGE}%")
    print(f"Accuracy Threshold: {ACCURACY_THRESHOLD}%")
    print("=" * 60 + "\n")

    app.run(host='0.0.0.0', port=8080, debug=False)
