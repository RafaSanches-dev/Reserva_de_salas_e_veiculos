from __future__ import annotations

import html
from typing import Optional

from flask import current_app, url_for


def subject_with_prefix(subject: str) -> str:
    prefix = (current_app.config.get('EMAIL_SUBJECT_PREFIX') or '').strip()
    if not prefix:
        return subject
    return f"{prefix} {subject}".strip()


def _default_logo_url() -> str:
    # Tenta usar uma URL configurada (útil se o app estiver atrás de proxy/domínio)
    explicit = (current_app.config.get('EMAIL_LOGO_URL') or '').strip()
    if explicit:
        return explicit

    try:
        return url_for('static', filename='imagens/Logo_UEMG.png', _external=True)
    except Exception:
        return ''


def wrap_html_email(*, title: str, intro_html: str, content_html: str, footer_html: Optional[str] = None) -> str:
    app_name = (current_app.config.get('APP_NAME') or 'Reserva UEMG').strip()
    primary = (current_app.config.get('EMAIL_BRAND_PRIMARY') or '#0b5ed7').strip()
    logo_url = _default_logo_url()

    safe_title = html.escape(title)
    safe_app_name = html.escape(app_name)

    header_logo = ''
    if logo_url:
        header_logo = (
            f"<img src=\"{html.escape(logo_url)}\" alt=\"{safe_app_name}\" "
            f"style=\"height:52px; width:auto; display:block; margin:0 auto 10px;\">"
        )

    footer_html = footer_html or (
        "<p style=\"margin:0; color:#6c757d; font-size:12px;\">"
        "Se você não solicitou esta ação, ignore este email."
        "</p>"
    )

    return f"""
<!doctype html>
<html lang=\"pt-BR\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>{safe_title}</title>
  </head>
  <body style=\"margin:0; padding:0; background:#f5f7fb; font-family:Arial, Helvetica, sans-serif;\">
    <div style=\"padding:24px 12px;\">
      <div style=\"max-width:620px; margin:0 auto;\">
        <div style=\"text-align:center; margin-bottom:12px;\">
          {header_logo}
          <div style=\"font-weight:700; color:{html.escape(primary)}; font-size:16px;\">{safe_app_name}</div>
        </div>

        <div style=\"background:#ffffff; border-radius:12px; box-shadow:0 4px 20px rgba(15,23,42,0.08); overflow:hidden;\">
          <div style=\"background:{html.escape(primary)}; padding:14px 18px; color:#fff; font-weight:700;\">{safe_title}</div>
          <div style=\"padding:18px; color:#111827;\">
            <div style=\"margin:0 0 12px; color:#374151;\">{intro_html}</div>
            <div style=\"margin:0 0 6px;\">{content_html}</div>
          </div>
          <div style=\"padding:14px 18px; background:#f8fafc;\">{footer_html}</div>
        </div>

        <div style=\"text-align:center; margin-top:12px; color:#9ca3af; font-size:12px;\">
          {safe_app_name}
        </div>
      </div>
    </div>
  </body>
</html>
""".strip()


def button(url: str, text: str) -> str:
    primary = (current_app.config.get('EMAIL_BRAND_PRIMARY') or '#0b5ed7').strip()
    return (
        f"<p style=\"margin:16px 0;\">"
        f"<a href=\"{html.escape(url)}\" "
        f"style=\"display:inline-block; background:{html.escape(primary)}; color:#fff; text-decoration:none; "
        f"padding:10px 14px; border-radius:10px; font-weight:700;\">"
        f"{html.escape(text)}"
        f"</a>"
        f"</p>"
    )
