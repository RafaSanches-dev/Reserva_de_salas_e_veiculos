# os significa opereting system
import os

try:
    from dotenv import load_dotenv

    # Carrega variáveis a partir de um arquivo .env na raiz do projeto.
    # Não sobrescreve variáveis já definidas no ambiente.
    load_dotenv(override=False)
except Exception:
    # python-dotenv é opcional; se não estiver instalado, apenas ignora.
    pass


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


class Config:
    # Segurança
    SECRET_KEY = os.getenv("SECRET_KEY", "EAEACDF099")

    # Banco
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("Defina a variável de ambiente SQLALCHEMY_DATABASE_URI.")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email (SMTP)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", True)
    MAIL_USE_SSL = _env_bool("MAIL_USE_SSL", False)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Reserva UEMG")

    # Se True, não envia de verdade (útil em DEV)
    MAIL_SUPPRESS_SEND = _env_bool("MAIL_SUPPRESS_SEND", False)

    # Identidade visual de emails
    APP_NAME = os.getenv("APP_NAME", "Reserva UEMG")
    EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX", "[Reserva UEMG]")
    EMAIL_LOGO_URL = os.getenv("EMAIL_LOGO_URL", "")
    EMAIL_BRAND_PRIMARY = os.getenv("EMAIL_BRAND_PRIMARY", "#0b5ed7")

    # Tokens
    SECURITY_PASSWORD_RESET_SALT = os.getenv(
        "SECURITY_PASSWORD_RESET_SALT", "password-reset"
    )
    SECURITY_PASSWORD_RESET_MAX_AGE_SECONDS = int(
        os.getenv("SECURITY_PASSWORD_RESET_MAX_AGE_SECONDS", "3600")
    )
