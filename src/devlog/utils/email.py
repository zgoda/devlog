from typing import Optional, List

import requests
from flask import current_app


def send_email(
            recipients: List[str], subject: str, html_body: str,
            text_body: Optional[str] = None,
        ) -> bool:
    message_dict = {
        'from': current_app.config['MAIL_FROM'],
        'to': recipients,
        'subject': subject,
        'html': html_body,
    }
    if text_body is not None:
        message_dict['text'] = text_body
    response = requests.post(
        current_app.config['MAILGUN_MESSAGES_URL'],
        auth=current_app.config['MAILGUN_AUTH'],
        data=message_dict
    )
    return response.ok
