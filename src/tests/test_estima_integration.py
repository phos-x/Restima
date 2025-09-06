from restima.inputs.from_flowaudit import infer

def test_infer_from_flowaudit():
    metrics = {
        "avg_cpu_percent": 65.2,
        "peak_memory_mb": 1450,
        "total_io_mb": 320,
        "call_depth": 12,
        "branching_factor": 3.1,
        "recursion_detected": True
    }
    features = infer(metrics)
    assert features["size_mb"] == 320
    assert features["duration_sec"] == 24