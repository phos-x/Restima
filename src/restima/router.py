from inputs import from_log, from_trace, from_service

def route(source_type: str, payload: str | dict) -> dict:
    if source_type == "log":
        return from_log.infer(payload)
    elif source_type == "trace":
        return from_trace.infer(payload)
    elif source_type == "service":
        return from_service.infer(payload)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")