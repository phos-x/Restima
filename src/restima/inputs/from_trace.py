def infer(trace: dict) -> dict:
    attrs = trace.get("attributes", {})
    return {
        "size_mb": round(attrs.get("input_size_bytes", 0) / 1024 / 1024, 2),
        "duration_sec": attrs.get("audio_duration_sec", 0),
        "channels": attrs.get("channels", 2),
        "bitrate_kbps": attrs.get("bitrate_kbps", 128),
        "model": attrs.get("model", "demucs_v4")
    }