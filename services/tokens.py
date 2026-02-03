from __future__ import annotations

from typing import Optional

from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.secret_key)


def generate_password_reset_token(email: str) -> str:
    salt = current_app.config.get("SECURITY_PASSWORD_RESET_SALT", "password-reset")
    return _serializer().dumps({"email": email}, salt=salt)


def verify_password_reset_token(token: str) -> Optional[str]:
    salt = current_app.config.get("SECURITY_PASSWORD_RESET_SALT", "password-reset")
    max_age = int(current_app.config.get("SECURITY_PASSWORD_RESET_MAX_AGE_SECONDS", 3600))

    try:
        payload = _serializer().loads(token, salt=salt, max_age=max_age)
        email = (payload or {}).get("email")
        if isinstance(email, str) and email.strip():
            return email.strip()
        return None
    except (SignatureExpired, BadSignature):
        return None
