from scipy.stats import ks_2samp
import json

def detect_drift(baseline_path, live_path, threshold=0.05):
    with open(baseline_path) as f1, open(live_path) as f2:
        baseline = [json.loads(line) for line in f1]
        live = [json.loads(line) for line in f2]

    report = {}
    for key in baseline[0]:
        b_vals = [x[key] for x in baseline if key in x]
        l_vals = [x[key] for x in live if key in x]
        stat, pval = ks_2samp(b_vals, l_vals)
        report[key] = {"p_value": round(pval, 4), "drift": pval < threshold}
    return report