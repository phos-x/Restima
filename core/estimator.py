def estimate_resources(metrics: dict, features: dict) -> dict:
    ram = metrics["peak_memory_mb"] + features["size_mb"] * 0.1 + features["channels"] * 50
    cpu = metrics["avg_cpu_percent"] / 100 + features["duration_sec"] * 0.01 + features["channels"] * 0.05
    io = metrics["total_io_mb"] + features["size_mb"] * 0.05 + features["bitrate_kbps"] * 0.001

    return {
        "ram_mb": round(ram, 2),
        "cpu_cores": round(cpu, 2),
        "io_mb": round(io, 2),
        "confidence": "High" if features["duration_sec"] > 30 else "Medium"
    }