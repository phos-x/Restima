import pickle
from pathlib import Path
from restima.core.features import extract_features
from restima.utils.logger import log_info

MODEL_PATH = Path("models/latest_model.pkl")

def formula_based_estimate(metrics: dict) -> dict:
    ram = metrics["peak_memory_mb"] + metrics["call_depth"] * 10
    cpu = metrics["avg_cpu_percent"] + metrics["branching_factor"] * 0.5
    io = metrics["total_io_mb"]
    return {
        "ram_mb": round(ram, 2),
        "cpu_cores": round(cpu, 2),
        "io_mb": round(io, 2),
        "confidence": "Medium"
    }

def model_based_estimate(metrics: dict) -> dict:
    if not MODEL_PATH.exists():
        log_info("No trained model found. Falling back to formula.")
        return formula_based_estimate(metrics)

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    features = extract_features(metrics)
    prediction = model.predict([features])[0]
    return {
        "ram_mb": round(prediction[0], 2),
        "cpu_cores": round(prediction[1], 2),
        "io_mb": round(prediction[2], 2),
        "confidence": "High"
    }

def estimate(metrics: dict) -> dict:
    try:
        return model_based_estimate(metrics)
    except Exception as e:
        log_info(f"Model estimation failed: {e}")
        return formula_based_estimate(metrics)
    
