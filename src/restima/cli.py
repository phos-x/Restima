import argparse
from router import route
from core.predictor import normalize_metrics
from core.estimator import estimate_resources
from core.formatter import format_output

def main():
    parser = argparse.ArgumentParser(description="estima: Estimate resource usage from logs, traces, or service input.")
    parser.add_argument("--source", choices=["log", "trace", "service"], required=True)
    parser.add_argument("--payload", required=True, help="Path to JSON file containing input")
    parser.add_argument("--metrics", required=True, help="Path to JSON file with raw metrics")

    args = parser.parse_args()

    import json
    with open(args.payload) as f:
        payload = json.load(f)
    with open(args.metrics) as f:
        raw_metrics = json.load(f)

    features = route(args.source, payload)
    normalized = normalize_metrics(raw_metrics)
    estimate = estimate_resources(normalized, features)
    print(format_output(estimate))

if __name__ == "__main__":
    main()