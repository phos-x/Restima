from collections import deque

def normalize_metrics(raw_stream: list) -> dict:
    cpu = deque(maxlen=10)
    memory = deque(maxlen=10)
    io = deque(maxlen=10)

    for sample in raw_stream:
        cpu.append(sample["cpu"])
        memory.append(sample["memory"])
        io.append(sample["io"])

    return {
        "avg_cpu_percent": sum(cpu) / len(cpu),
        "peak_memory_mb": max(memory),
        "total_io_mb": sum(io)
    }