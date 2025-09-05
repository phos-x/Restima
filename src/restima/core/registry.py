_registry = {}

def register_model(name: str, version: str, metadata: dict):
    _registry[f"{name}:{version}"] = metadata

def get_model(name: str, version: str):
    return _registry.get(f"{name}:{version}", {})