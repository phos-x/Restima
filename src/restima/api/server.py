from flask import Flask, request, jsonify
from restima.router import route
from restima.core.predictor import normalize_metrics
from restima.core.estimator import estimate_resources

app = Flask(__name__)

@app.route("/estimate", methods=["POST"])
def estimate():
    data = request.json
    features = route(data["source"], data["payload"])
    metrics = normalize_metrics(data["metrics"])
    result = estimate_resources(metrics, features)
    return jsonify(result)