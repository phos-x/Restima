import json

def infer(log_line: str) -> dict:
    data = json.loads(log_line)
    return {
        "size_mb": data.get("size_mb", 0),
        "duration_sec": data.get("duration_sec", 0),
        "channels": data.get("channels", 2),
        "bitrate_kbps": data.get("bitrate_kbps", 128),
        "model": data.get("model", "demucs_v4")
    }