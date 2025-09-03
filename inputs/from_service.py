def infer(service_payload: dict) -> dict:
    return {
        "size_mb": service_payload["size_mb"],
        "duration_sec": service_payload["duration_sec"],
        "channels": service_payload.get("channels", 2),
        "bitrate_kbps": service_payload.get("bitrate_kbps", 128),
        "model": service_payload.get("model", "demucs_v4")
    }