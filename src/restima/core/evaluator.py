from sklearn.metrics import mean_squared_error, r2_score
import json, pickle

def evaluate_model(model_path, eval_data_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    X, y_true = [], []
    with open(eval_data_path) as f:
        for line in f:
            record = json.loads(line)
            X.append(record["features"])
            y_true.append(record["targets"])

    y_pred = model.predict(X)
    return {
        "mse": round(mean_squared_error(y_true, y_pred), 3),
        "r2": round(r2_score(y_true, y_pred), 3)
    }