import psutil
import time
import json
from datetime import datetime

def collect_metrics(duration=60, interval=1, output_path="data/live_metrics.jsonl"):
    with open(output_path, "w") as f:
        for _ in range(duration):
            snapshot = {
                "timestamp": datetime.utcnow().isoformat(),
                "avg_cpu_percent": psutil.cpu_percent(),
                "peak_memory_mb": psutil.virtual_memory().used / 1024 / 1024,
                "total_io_mb": psutil.disk_io_counters().write_bytes / 1024 / 1024,
                "call_depth": 5,  # placeholder
                "branching_factor": 2.0,
                "recursion_detected": False,
                "avg_latency_sec": 0.1
            }
            f.write(json.dumps(snapshot) + "\n")
            time.sleep(interval)

