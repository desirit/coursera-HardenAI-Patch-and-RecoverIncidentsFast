"""
setup_models.py - MLflow Model Registration

This script creates and registers two model versions in MLflow:
- Version 1: Production model (stable)
- Version 2: Staging/Canary model (being tested)

Run this script ONCE before starting the lab exercises.

Part of: Harden AI - Patch and Recover Incidents Fast (Coursera)
Lab 1: Canary Deployments for ML Models
"""

import mlflow
from mlflow.tracking import MlflowClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np

# Connect to MLflow server
mlflow.set_tracking_uri("http://127.0.0.1:5001")
mlflow.set_experiment("sentiment-classifier")

# Sample training data for sentiment classification
texts = [
    "I love this product, it's amazing!",
    "Terrible experience, would not recommend",
    "Great quality and fast shipping",
    "Worst purchase ever, complete waste",
    "Excellent service, very happy",
    "Disappointed with the results",
    "Best thing I've bought this year",
    "Poor quality, broke after one day",
    "Highly recommend to everyone",
    "Not worth the money at all"
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1=positive, 0=negative


def create_model(version_name, accuracy_modifier=0):
    """Create and log a sentiment model to MLflow."""

    # Create a simple text classification pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100)),
        ('clf', LogisticRegression(random_state=42 + accuracy_modifier))
    ])

    # Train the model
    model.fit(texts, labels)

    # Log to MLflow
    with mlflow.start_run(run_name=version_name):
        # Log parameters
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("version", version_name)

        # Calculate and log accuracy
        predictions = model.predict(texts)
        accuracy = np.mean(predictions == labels)
        mlflow.log_metric("training_accuracy", accuracy)

        # Log the model to the registry
        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="sentiment"
        )

        print(f"Created {version_name} with accuracy: {accuracy:.2%}")
        return mlflow.active_run().info.run_id


def setup_model_registry():
    """Register models and set their stages (Production vs Staging)."""
    client = MlflowClient()

    print("\nSetting up MLflow Model Registry...")
    print("-" * 50)

    # Create version 1 (production model)
    print("\nCreating Version 1 (Production)...")
    create_model("v1-production")

    # Create version 2 (canary model)
    print("\nCreating Version 2 (Canary)...")
    create_model("v2-canary", accuracy_modifier=1)

    # Get model versions
    versions = client.search_model_versions("name='sentiment'")

    if len(versions) >= 2:
        # Set stages (oldest = production, newest = staging)
        sorted_versions = sorted(versions, key=lambda x: int(x.version))

        # Version 1 -> Production
        client.transition_model_version_stage(
            name="sentiment",
            version=sorted_versions[0].version,
            stage="Production"
        )
        print(f"Version {sorted_versions[0].version} set to Production")

        # Version 2 -> Staging (Canary)
        client.transition_model_version_stage(
            name="sentiment",
            version=sorted_versions[1].version,
            stage="Staging"
        )
        print(f"Version {sorted_versions[1].version} set to Staging (Canary)")

    print("\n" + "=" * 50)
    print("Setup complete!")
    print("View models at: http://127.0.0.1:5001")
    print("=" * 50)


if __name__ == "__main__":
    setup_model_registry()
