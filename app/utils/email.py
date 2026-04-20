import requests
from app.core.config import RESEND_API_KEY, EMAIL_FROM, EMAIL_TO


def send_contact_email(name: str, email: str, message: str):
    url = "https://api.resend.com/emails"

    payload = {
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "subject": f"New Contact Message from {name}",
        "html": f"""
            <h3>New Contact Message</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        """
    }

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()