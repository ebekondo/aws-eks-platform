import os
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(
        {
            "message": "AWS EKS Platform API",
            "status": "running",
            "hostname": socket.gethostname(),
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/ready")
def ready():
    return jsonify(
        {
            "status": "ready",
        }
    )


@app.get("/info")
def info():
    return jsonify(
        {
            "application": "eks-platform-api",
            "environment": os.getenv("APP_ENV", "local"),
            "version": os.getenv("APP_VERSION", "development"),
            "hostname": socket.gethostname(),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)