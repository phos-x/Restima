import argparse
from restima.core.trainer import train_model
from restima.core.estimator import estimate
from pathlib import Path
import json
from restima.core.monitor_service import collect_metrics
from restima.core.evaluator import evaluate_model
from restima.core.drift_detector import detect_drift

def main():
    parser = argparse.ArgumentParser(description="🧠 restima CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("drift").add_argument("--baseline", required=True).add_argument("--live", required=True)
    
    monitor_cmd = subparsers.add_parser("monitor")
    monitor_cmd.add_argument("--duration", type=int, default=60)
    monitor_cmd.add_argument("--output", default="data/live_metrics.jsonl")

    eval_cmd = subparsers.add_parser("evaluate-model")
    eval_cmd.add_argument("--model", default="models/latest_model.pkl")
    eval_cmd.add_argument("--data", required=True)

    inspect_cmd = subparsers.add_parser("inspect-model")
    inspect_cmd.add_argument("--model", default="models/latest_model.pkl")

    drift_cmd = subparsers.add_parser("retrain-on-drift")
    drift_cmd.add_argument("--baseline", required=True)
    drift_cmd.add_argument("--live", required=True)
    drift_cmd.add_argument("--threshold", type=float, default=0.05)
    drift_cmd.add_argument("--data", required=True)
    drift_cmd.add_argument("--output", default="models/latest_model.pkl")


    train_cmd = subparsers.add_parser("train-model")
    train_cmd.add_argument("--data", required=True)
    train_cmd.add_argument("--output", default="models/latest_model.pkl")

    estimate_cmd = subparsers.add_parser("estimate")
    estimate_cmd.add_argument("--metrics", required=True)
    estimate_cmd.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "monitor":
        collect_metrics(args.duration)

    elif args.command == "train":
        train_model(args.data)

    elif args.command == "evaluate":
        result = evaluate_model(args.model, args.data)
        print("📊 Evaluation:", result)

    elif args.command == "drift":
        report = detect_drift(args.baseline, args.live)
        print("📈 Drift Report:", report)
    
    if args.command == "train-model":
        train_model(args.data, args.output)

    elif args.command == "estimate":
        metrics = json.loads(Path(args.metrics).read_text())
        result = estimate(metrics)
        Path(args.output).write_text(json.dumps(result, indent=2))
    
    elif args.command == "monitor":
        collect_metrics(args.duration, output_path=args.output)

    elif args.command == "evaluate-model":
        result = evaluate_model(args.model, args.data)
        print("📊 Evaluation:", result)

    elif args.command == "inspect-model":
        import pickle
        model = pickle.load(open(args.model, "rb"))
        print("📦 Model Coefficients:", model.coef_)

    elif args.command == "retrain-on-drift":
        drift = detect_drift(args.baseline, args.live, args.threshold)
        if any(v["drift"] for v in drift.values()):
            print("⚠️ Drift detected. Retraining...")
            train_model(args.data, args.output)
        else:
            print("✅ No significant drift. Model retained.")

if __name__ == "__main__":
    main()