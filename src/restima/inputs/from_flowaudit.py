def infer(metrics: dict) -> dict:
    return {
        "size_mb": metrics.get("total_io_mb", 0),
        "duration_sec": metrics.get("call_depth", 0) * 2,
        "channels": 2,
        "bitrate_kbps": 128,
        "model": "unknown"
    }