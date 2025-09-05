import requests

def notify(estimate: dict, webhook_url: str):
    message = (
        f"*Estima Resource Summary*\n"
        f"> RAM: {estimate['ram_mb']} MB\n"
        f"> CPU: {estimate['cpu_cores']} cores\n"
        f"> I/O: {estimate['io_mb']} MB\n"
        f"> Confidence: {estimate['confidence']}"
    )
    requests.post(webhook_url, json={"text": message})