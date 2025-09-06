import json
from pathlib import Path

REGISTRY_PATH = Path("models/registry.json")

def update_registry(model_path: str, metrics: dict):
    registry = {
        "model_path": model_path,
        "trained_on": metrics.get("timestamp"),
        "features": list(metrics.keys())
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))