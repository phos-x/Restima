import json
import pickle
from sklearn.linear_model import LinearRegression
from restima.core.features import extract_features
from restima.utils.logger import log_info

def train_model(data_path: str, output_path: str = "models/predictor_model.pkl"):
    X, y = [], []
    with open(data_path) as f:
        for line in f:
            record = json.loads(line)
            features = extract_features(record["metrics"])
            targets = [
                record["targets"]["ram_mb"],
                record["targets"]["cpu_cores"],
                record["targets"]["io_mb"]
            ]
            X.append(features)
            y.append(targets)

    model = LinearRegression()
    model.fit(X, y)
    with open(output_path, "wb") as f:
        pickle.dump(model, f)

    log_info(f"✅ Model trained and saved to {output_path}")