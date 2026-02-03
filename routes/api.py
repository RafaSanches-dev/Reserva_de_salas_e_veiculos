from __future__ import annotations

from datetime import date, datetime, time

from flask import jsonify, request, session

from app import app, db
from models.mydb import Cliente, ReservaDeSala, ReservaDeVeiculo
from services.reserva_notifications import email_reserva_status


def _perfil_atual() -> str:
    return session.get('cliente_perfil', 'cliente')


def _tem_perfil(*perfis: str) -> bool:
    return _perfil_atual() in perfis


def _api_response(*, ok: bool, message: str | None = None, data=None, status: int = 200):
    payload = {'ok': ok}
    if message is not None:
        payload['message'] = message
    if data is not None:
        payload['data'] = data
    return jsonify(payload), status


def _require_login():
    if 'cliente_id' not in session:
        return _api_response(ok=False, message='Sessão expirada. Faça login novamente.', status=401)
    return None


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _parse_time(value: str) -> time:
    # aceita HH:MM ou HH:MM:SS
    return time.fromisoformat(value)


def _modelo_por_tipo(tipo: str):
    if tipo == 'sala':
        return ReservaDeSala
    if tipo == 'veiculo':
        return ReservaDeVeiculo
    return None


def _notificar(tipo: str, reserva, status: str, motivo: str | None = None) -> None:
    cliente = getattr(reserva, 'cliente', None) or Cliente.query.get(getattr(reserva, 'cliente_id', None))
    if not cliente:
        return
    email_reserva_status(tipo, reserva, cliente, status=status, motivo=motivo)


@app.route('/api/me', methods=['GET'])
def api_me():
    not_logged = _require_login()
    if not_logged:
        return not_logged

    cliente = Cliente.query.get(session['cliente_id'])
    if not cliente:
        return _api_response(ok=False, message='Usuário não encontrado.', status=404)

    return _api_response(
        ok=True,
        data={
            'id': cliente.id,
            'nome': cliente.nome,
            'email': cliente.email,
            'perfil': getattr(cliente, 'perfil', 'cliente'),
        },
    )


@app.route('/api/reservas/minhas', methods=['GET'])
def api_minhas_reservas():
    not_logged = _require_login()
    if not_logged:
        return not_logged

    cid = session['cliente_id']
    reservas_sala = (ReservaDeSala.query
                    .filter_by(cliente_id=cid)
                    .order_by(ReservaDeSala.data.desc(), ReservaDeSala.inicio.desc())
                    .all())
    reservas_veiculo = (ReservaDeVeiculo.query
                        .filter_by(cliente_id=cid)
                        .order_by(ReservaDeVeiculo.data_saida.desc(), ReservaDeVeiculo.horario_saida.desc())
                        .all())

    return _api_response(
        ok=True,
        data={
            'reservas_sala': [
                {
                    'id': r.id,
                    'sala': r.sala,
                    'data': r.data.isoformat(),
                    'inicio': r.inicio.strftime('%H:%M:%S'),
                    'fim': r.fim.strftime('%H:%M:%S'),
                    'titulo_da_reserva': r.titulo_da_reserva,
                    'finalidade': r.finalidade,
                    'status': r.status,
                    'motivo_rejeicao': r.motivo_rejeicao,
                    'decidido_em': r.decidido_em.isoformat() if r.decidido_em else None,
                    'decidido_por': r.decidido_por,
                }
                for r in reservas_sala
            ],
            'reservas_veiculo': [
                {
                    'id': r.id,
                    'veiculo': r.veiculo,
                    'destino': r.destino,
                    'data_saida': r.data_saida.isoformat(),
                    'horario_saida': r.horario_saida.strftime('%H:%M:%S'),
                    'data_retorno': r.data_retorno.isoformat(),
                    'horario_retorno': r.horario_retorno.strftime('%H:%M:%S'),
                    'motivo': r.motivo,
                    'status': r.status,
                    'motivo_rejeicao': r.motivo_rejeicao,
                    'decidido_em': r.decidido_em.isoformat() if r.decidido_em else None,
                    'decidido_por': r.decidido_por,
                }
                for r in reservas_veiculo
            ],
        },
    )


@app.route('/api/reservas/pendentes', methods=['GET'])
def api_reservas_pendentes():
    not_logged = _require_login()
    if not_logged:
        return not_logged
    if not _tem_perfil('aprovador'):
        return _api_response(ok=False, message='Sem permissão.', status=403)

    reservas_sala = (ReservaDeSala.query
                    .filter_by(status='pendente')
                    .order_by(ReservaDeSala.data.asc(), ReservaDeSala.inicio.asc())
                    .all())
    reservas_veiculo = (ReservaDeVeiculo.query
                        .filter_by(status='pendente')
                        .order_by(ReservaDeVeiculo.data_saida.asc(), ReservaDeVeiculo.horario_saida.asc())
                        .all())

    return _api_response(
        ok=True,
        data={
            'reservas_sala': [
                {
                    'id': r.id,
                    'sala': r.sala,
                    'data': r.data.isoformat(),
                    'inicio': r.inicio.strftime('%H:%M:%S'),
                    'fim': r.fim.strftime('%H:%M:%S'),
                    'titulo_da_reserva': r.titulo_da_reserva,
                    'finalidade': r.finalidade,
                    'cliente_id': r.cliente_id,
                    'cliente_nome': r.cliente.nome if getattr(r, 'cliente', None) else None,
                    'cliente_email': r.cliente.email if getattr(r, 'cliente', None) else None,
                }
                for r in reservas_sala
            ],
            'reservas_veiculo': [
                {
                    'id': r.id,
                    'veiculo': r.veiculo,
                    'destino': r.destino,
                    'data_saida': r.data_saida.isoformat(),
                    'horario_saida': r.horario_saida.strftime('%H:%M:%S'),
                    'data_retorno': r.data_retorno.isoformat(),
                    'horario_retorno': r.horario_retorno.strftime('%H:%M:%S'),
                    'motivo': r.motivo,
                    'cliente_id': r.cliente_id,
                    'cliente_nome': r.cliente.nome if getattr(r, 'cliente', None) else None,
                    'cliente_email': r.cliente.email if getattr(r, 'cliente', None) else None,
                }
                for r in reservas_veiculo
            ],
        },
    )


@app.route('/api/reservas/<tipo>', methods=['POST'])
def api_criar_reserva(tipo: str):
    not_logged = _require_login()
    if not_logged:
        return not_logged

    payload = request.get_json(silent=True) or {}

    if tipo == 'sala':
        required = ['sala', 'data', 'inicio', 'fim', 'titulo_da_reserva', 'finalidade']
        missing = [k for k in required if not (payload.get(k) or '').strip()]
        if missing:
            return _api_response(ok=False, message=f"Campos obrigatórios: {', '.join(missing)}", status=400)

        try:
            reserva = ReservaDeSala(
                sala=payload['sala'].strip(),
                data=_parse_date(payload['data'].strip()),
                inicio=_parse_time(payload['inicio'].strip()),
                fim=_parse_time(payload['fim'].strip()),
                titulo_da_reserva=payload['titulo_da_reserva'].strip(),
                finalidade=payload['finalidade'].strip(),
                cliente_id=session['cliente_id'],
            )
            db.session.add(reserva)
            db.session.commit()
            return _api_response(ok=True, message='Reserva de sala solicitada com sucesso.', data={'id': reserva.id})
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            return _api_response(ok=False, message=str(exc), status=400)

    if tipo == 'veiculo':
        required = [
            'veiculo', 'data_saida', 'horario_saida', 'data_retorno', 'horario_retorno', 'destino', 'motivo'
        ]
        missing = [k for k in required if not (payload.get(k) or '').strip()]
        if missing:
            return _api_response(ok=False, message=f"Campos obrigatórios: {', '.join(missing)}", status=400)

        try:
            reserva = ReservaDeVeiculo(
                veiculo=payload['veiculo'].strip(),
                data_saida=_parse_date(payload['data_saida'].strip()),
                horario_saida=_parse_time(payload['horario_saida'].strip()),
                data_retorno=_parse_date(payload['data_retorno'].strip()),
                horario_retorno=_parse_time(payload['horario_retorno'].strip()),
                destino=payload['destino'].strip(),
                motivo=payload['motivo'].strip(),
                cliente_id=session['cliente_id'],
            )
            db.session.add(reserva)
            db.session.commit()
            return _api_response(ok=True, message='Reserva de veículo solicitada com sucesso.', data={'id': reserva.id})
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            return _api_response(ok=False, message=str(exc), status=400)

    return _api_response(ok=False, message='Tipo inválido.', status=400)


@app.route('/api/reservas/<tipo>/<int:reserva_id>/aprovar', methods=['POST'])
def api_aprovar(tipo: str, reserva_id: int):
    not_logged = _require_login()
    if not_logged:
        return not_logged
    if not _tem_perfil('aprovador'):
        return _api_response(ok=False, message='Sem permissão.', status=403)

    Modelo = _modelo_por_tipo(tipo)
    if Modelo is None:
        return _api_response(ok=False, message='Tipo inválido.', status=400)

    reserva = Modelo.query.get(reserva_id)
    if not reserva:
        return _api_response(ok=False, message='Reserva não encontrada.', status=404)

    reserva.status = 'aprovado'
    reserva.motivo_rejeicao = None
    reserva.decidido_em = datetime.utcnow()
    reserva.decidido_por = session['cliente_id']
    db.session.commit()

    _notificar(tipo, reserva, status='aprovada')

    return _api_response(ok=True, message='Reserva aprovada com sucesso.')


@app.route('/api/reservas/<tipo>/<int:reserva_id>/rejeitar', methods=['POST'])
def api_rejeitar(tipo: str, reserva_id: int):
    not_logged = _require_login()
    if not_logged:
        return not_logged
    if not _tem_perfil('aprovador'):
        return _api_response(ok=False, message='Sem permissão.', status=403)

    Modelo = _modelo_por_tipo(tipo)
    if Modelo is None:
        return _api_response(ok=False, message='Tipo inválido.', status=400)

    reserva = Modelo.query.get(reserva_id)
    if not reserva:
        return _api_response(ok=False, message='Reserva não encontrada.', status=404)

    payload = request.get_json(silent=True) or {}
    motivo = (payload.get('motivo') or '').strip()
    if not motivo:
        return _api_response(ok=False, message='Informe um motivo para rejeitar.', status=400)

    reserva.status = 'rejeitado'
    reserva.motivo_rejeicao = motivo
    reserva.decidido_em = datetime.utcnow()
    reserva.decidido_por = session['cliente_id']
    db.session.commit()

    _notificar(tipo, reserva, status='rejeitada', motivo=motivo)

    return _api_response(ok=True, message='Reserva rejeitada com sucesso.')
