"""
send_requests.py - Test Traffic Generator

Send test requests to the canary deployment server and visualize results.

Usage:
  python send_requests.py send 20   # Send 20 requests
  python send_requests.py metrics   # Show current metrics
  python send_requests.py canary 10 # Set canary to 10%
  python send_requests.py fail      # Enable failure simulation
  python send_requests.py rollback  # Check rollback trigger
  python send_requests.py reset     # Reset system

Part of: Harden AI - Patch and Recover Incidents Fast (Coursera)
Lab 1: Canary Deployments for ML Models
"""

import requests
import time
import random

BASE_URL = "http://127.0.0.1:8080"

# Test data with known sentiment labels
TEST_DATA = [
    {"text": "This product is amazing, love it!", "actual_label": 1},
    {"text": "Terrible quality, very disappointed", "actual_label": 0},
    {"text": "Great value for money, highly recommend", "actual_label": 1},
    {"text": "Worst purchase I ever made", "actual_label": 0},
    {"text": "Excellent service and fast delivery", "actual_label": 1},
    {"text": "Complete waste of money", "actual_label": 0},
    {"text": "Best thing I bought this year", "actual_label": 1},
    {"text": "Poor quality, broke immediately", "actual_label": 0},
    {"text": "Absolutely fantastic experience", "actual_label": 1},
    {"text": "Would not recommend to anyone", "actual_label": 0},
]


def send_requests(n=20, delay=0.3):
    """Send n requests with a delay between each."""
    print("\n" + "=" * 60)
    print(f"Sending {n} requests to canary deployment...")
    print("=" * 60 + "\n")

    for i in range(n):
        sample = random.choice(TEST_DATA)

        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=sample
            )
            result = response.json()

            # Visual indicator
            if result['model_version'] == 'canary':
                version = "CANARY    "
            else:
                version = "PRODUCTION"

            correct = "OK" if result['prediction'] == sample['actual_label'] else "WRONG"

            print(f"  {i+1:3}. [{version}] Pred: {result['prediction']} | {correct} | {result['latency_ms']:.1f}ms")

        except Exception as e:
            print(f"  {i+1:3}. ERROR: {e}")

        time.sleep(delay)

    print("\n" + "-" * 60)
    print("Fetching metrics...")
    show_metrics()


def show_metrics():
    """Display current metrics."""
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        metrics = response.json()

        print("\n" + "=" * 60)
        print("CURRENT METRICS")
        print("=" * 60)
        print(f"\n  Canary Traffic: {metrics['canary_percentage']}%")
        print()
        print("  +-------------+----------+----------+-------------+")
        print("  |   Model     | Requests | Accuracy | Avg Latency |")
        print("  +-------------+----------+----------+-------------+")

        for version in ["production", "canary"]:
            m = metrics[version]
            print(f"  | {version:11} | {m['requests']:>8} | {m['accuracy']:>7.1f}% | {m['avg_latency_ms']:>9.1f}ms |")

        print("  +-------------+----------+----------+-------------+")
        print()

    except Exception as e:
        print(f"ERROR fetching metrics: {e}")


def check_rollback():
    """Check if rollback should trigger."""
    try:
        response = requests.post(f"{BASE_URL}/check_rollback")
        result = response.json()

        if result['status'] == 'rollback':
            print("\n" + "!" * 60)
            print("  ROLLBACK TRIGGERED!")
            print(f"  Reason: Canary accuracy {result['canary_accuracy']}% < {result['threshold']}%")
            print("!" * 60 + "\n")
        elif result['status'] == 'waiting':
            print(f"\n  Waiting for more data: {result['message']}\n")
        else:
            print(f"\n  System healthy. Canary accuracy: {result.get('canary_accuracy', 'N/A')}%\n")

    except Exception as e:
        print(f"ERROR: {e}")


def set_canary(percentage):
    """Change canary percentage."""
    try:
        response = requests.post(f"{BASE_URL}/set_canary/{percentage}")
        result = response.json()
        print(f"\nCanary percentage set to: {result['canary_percentage']}%\n")
    except Exception as e:
        print(f"ERROR: {e}")


def enable_failure():
    """Enable failure simulation (for rollback demo)."""
    try:
        response = requests.post(f"{BASE_URL}/simulate_failure/1")
        print("\nFailure simulation ENABLED - canary will make bad predictions\n")
    except Exception as e:
        print(f"ERROR: {e}")


def disable_failure():
    """Disable failure simulation."""
    try:
        response = requests.post(f"{BASE_URL}/simulate_failure/0")
        print("\nFailure simulation DISABLED\n")
    except Exception as e:
        print(f"ERROR: {e}")


def reset():
    """Reset all metrics and settings."""
    try:
        response = requests.post(f"{BASE_URL}/reset")
        print("\nSystem reset complete\n")
    except Exception as e:
        print(f"ERROR: {e}")


def print_usage():
    """Print usage instructions."""
    print("""
Canary Deployment Test Client
=============================

Usage:
  python send_requests.py send [n]    Send n requests (default: 20)
  python send_requests.py metrics     Show current metrics
  python send_requests.py canary <n>  Set canary percentage to n%
  python send_requests.py fail        Enable failure simulation
  python send_requests.py nofail      Disable failure simulation
  python send_requests.py rollback    Check if rollback should trigger
  python send_requests.py reset       Reset all metrics and settings

Examples:
  python send_requests.py send 50     # Send 50 test requests
  python send_requests.py canary 10   # Set 10% traffic to canary
  python send_requests.py fail        # Make canary produce bad predictions
  python send_requests.py rollback    # Trigger rollback check
    """)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "send":
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            send_requests(n=n)
        elif cmd == "metrics":
            show_metrics()
        elif cmd == "rollback":
            check_rollback()
        elif cmd == "canary":
            if len(sys.argv) > 2:
                set_canary(int(sys.argv[2]))
            else:
                print("Usage: python send_requests.py canary <percentage>")
        elif cmd == "fail":
            enable_failure()
        elif cmd == "nofail":
            disable_failure()
        elif cmd == "reset":
            reset()
        else:
            print(f"Unknown command: {cmd}")
            print_usage()
    else:
        print_usage()
