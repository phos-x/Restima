def export(estimate: dict, name="estima_service") -> str:
    return f"""
resource "aws_instance" "{name}" {{
  instance_type = "t3.medium"
  cpu_core_count = {int(estimate['cpu_cores'])}
  memory_size = "{estimate['ram_mb']}MB"
  tags = {{
    Confidence = "{estimate['confidence']}"
  }}
}}
"""