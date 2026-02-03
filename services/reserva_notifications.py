from __future__ import annotations

import html
from typing import Optional

from flask import url_for

from services.email_service import send_email
from services.email_templates import subject_with_prefix, wrap_html_email


def email_reserva_status(tipo: str, reserva, cliente, status: str, motivo: Optional[str] = None) -> None:
    """Envia email de status (aprovada/rejeitada) para o cliente.

    `cliente` deve ter `nome` e `email`.
    Não levanta exceção (falhas de email não devem quebrar o fluxo principal).
    """

    if not cliente or not getattr(cliente, 'email', None):
        return

    tipo_label = 'Sala' if tipo == 'sala' else 'Veículo'
    subject = subject_with_prefix(f"Reserva de {tipo_label} {status}")

    detalhes_text = ""
    detalhes_html = ""

    if tipo == 'sala':
        detalhes_text = (
            f"Sala: {reserva.sala}\n"
            f"Data: {reserva.data.strftime('%d/%m/%Y')}\n"
            f"Horário: {reserva.inicio.strftime('%H:%M')} - {reserva.fim.strftime('%H:%M')}\n"
            f"Título: {reserva.titulo_da_reserva}\n"
            f"Finalidade: {reserva.finalidade}\n"
        )
        detalhes_html = (
            f"<ul>"
            f"<li><strong>Sala:</strong> {html.escape(str(reserva.sala))}</li>"
            f"<li><strong>Data:</strong> {html.escape(reserva.data.strftime('%d/%m/%Y'))}</li>"
            f"<li><strong>Horário:</strong> {html.escape(reserva.inicio.strftime('%H:%M'))} - {html.escape(reserva.fim.strftime('%H:%M'))}</li>"
            f"<li><strong>Título:</strong> {html.escape(str(reserva.titulo_da_reserva))}</li>"
            f"<li><strong>Finalidade:</strong> {html.escape(str(reserva.finalidade))}</li>"
            f"</ul>"
        )
    elif tipo == 'veiculo':
        detalhes_text = (
            f"Veículo: {reserva.veiculo}\n"
            f"Destino: {reserva.destino}\n"
            f"Saída: {reserva.data_saida.strftime('%d/%m/%Y')} {reserva.horario_saida.strftime('%H:%M')}\n"
            f"Retorno: {reserva.data_retorno.strftime('%d/%m/%Y')} {reserva.horario_retorno.strftime('%H:%M')}\n"
            f"Motivo: {reserva.motivo}\n"
        )
        detalhes_html = (
            f"<ul>"
            f"<li><strong>Veículo:</strong> {html.escape(str(reserva.veiculo))}</li>"
            f"<li><strong>Destino:</strong> {html.escape(str(reserva.destino))}</li>"
            f"<li><strong>Saída:</strong> {html.escape(reserva.data_saida.strftime('%d/%m/%Y'))} {html.escape(reserva.horario_saida.strftime('%H:%M'))}</li>"
            f"<li><strong>Retorno:</strong> {html.escape(reserva.data_retorno.strftime('%d/%m/%Y'))} {html.escape(reserva.horario_retorno.strftime('%H:%M'))}</li>"
            f"<li><strong>Motivo:</strong> {html.escape(str(reserva.motivo))}</li>"
            f"</ul>"
        )

    dashboard_link = url_for('dashboard', _external=True)

    body_text = (
        f"Olá, {cliente.nome}.\n\n"
        f"Sua reserva de {tipo_label} foi {status}.\n\n"
        f"{detalhes_text}"
    )
    if motivo:
        body_text += f"\nMotivo: {motivo}\n"
    body_text += f"\nAcesse o sistema: {dashboard_link}"

    intro_html = (
        f"Olá, <strong>{html.escape(str(cliente.nome))}</strong>. "
        f"Sua reserva de <strong>{html.escape(tipo_label)}</strong> foi <strong>{html.escape(status)}</strong>."
    )
    content_html = detalhes_html
    if motivo:
        content_html += f"<p><strong>Motivo:</strong> {html.escape(str(motivo))}</p>"
    content_html += f"<p><a href=\"{html.escape(dashboard_link)}\">Acessar o sistema</a></p>"

    body_html = wrap_html_email(
        title=f"Reserva de {tipo_label} {status}",
        intro_html=intro_html,
        content_html=content_html,
    )

    send_email(subject=subject, recipients=[cliente.email], body_text=body_text, body_html=body_html)
