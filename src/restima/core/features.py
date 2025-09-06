def extract_features(metrics: dict) -> list:
    return [
        metrics.get("avg_cpu_percent", 0),
        metrics.get("peak_memory_mb", 0),
        metrics.get("total_io_mb", 0),
        metrics.get("call_depth", 0),
        metrics.get("branching_factor", 0),
        int(metrics.get("recursion_detected", False)),
        metrics.get("avg_latency_sec", 0)
    ]