from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage
from typing import Iterable, Optional, Tuple

from flask import current_app


def send_email(
    *,
    subject: str,
    recipients: Iterable[str],
    body_text: str,
    body_html: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """Envia email via SMTP usando configurações do Flask app.

    Retorna (ok, error_message).
    """

    recipients_list = [r.strip() for r in recipients if (r or "").strip()]
    if not recipients_list:
        return False, "Nenhum destinatário informado."

    if current_app.config.get("MAIL_SUPPRESS_SEND", False):
        current_app.logger.info(
            "MAIL_SUPPRESS_SEND=True; email suprimido: subject=%s to=%s",
            subject,
            recipients_list,
        )
        return True, None

    mail_server = (current_app.config.get("MAIL_SERVER") or "").strip()
    mail_port = int(current_app.config.get("MAIL_PORT") or 0)
    mail_username = (current_app.config.get("MAIL_USERNAME") or "").strip()
    mail_password = (current_app.config.get("MAIL_PASSWORD") or "").strip()
    use_tls = bool(current_app.config.get("MAIL_USE_TLS", True))
    use_ssl = bool(current_app.config.get("MAIL_USE_SSL", False))
    default_sender = (current_app.config.get("MAIL_DEFAULT_SENDER") or mail_username).strip()
    from_name = (current_app.config.get("MAIL_FROM_NAME") or "Reserva UEMG").strip()

    if not mail_server or not mail_port:
        return False, "Config de email incompleta (MAIL_SERVER/MAIL_PORT)."

    if not default_sender:
        return False, "Config de email incompleta (MAIL_DEFAULT_SENDER/MAIL_USERNAME)."

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{default_sender}>" if from_name else default_sender
    msg["To"] = ", ".join(recipients_list)
    msg.set_content(body_text or "")
    if body_html:
        msg.add_alternative(body_html, subtype="html")

    mail_server = (current_app.config.get("MAIL_SERVER") or "").strip()
    mail_port = int(current_app.config.get("MAIL_PORT") or 0)
    mail_username = (current_app.config.get("MAIL_USERNAME") or "").strip()
    mail_password = (current_app.config.get("MAIL_PASSWORD") or "").strip()
    use_tls = bool(current_app.config.get("MAIL_USE_TLS", True))
    use_ssl = bool(current_app.config.get("MAIL_USE_SSL", False))
    default_sender = (current_app.config.get("MAIL_DEFAULT_SENDER") or mail_username).strip()
    from_name = (current_app.config.get("MAIL_FROM_NAME") or "Reserva UEMG").strip()

    try:
        context = ssl.create_default_context()

        if use_ssl:
            with smtplib.SMTP_SSL(mail_server, mail_port, context=context) as smtp:
                if mail_username and mail_password:
                    smtp.login(mail_username, mail_password)
                smtp.send_message(msg)
        else:
            with smtplib.SMTP(mail_server, mail_port) as smtp:
                smtp.ehlo()
                if use_tls:
                    smtp.starttls(context=context)
                    smtp.ehlo()
                if mail_username and mail_password:
                    smtp.login(mail_username, mail_password)
                smtp.send_message(msg)

        return True, None
    except Exception as exc:  # noqa: BLE001
        current_app.logger.exception("Falha ao enviar email")
        return False, str(exc)
