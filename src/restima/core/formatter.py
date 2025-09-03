def format_output(estimate: dict) -> str:
    return (
        f"\n📊 Resource Estimation Summary\n"
        f"• Estimated RAM: {estimate['ram_mb']} MB\n"
        f"• Estimated CPU: {estimate['cpu_cores']} cores\n"
        f"• Estimated I/O: {estimate['io_mb']} MB\n"
        f"• Confidence Level: {estimate['confidence']}\n"
    )