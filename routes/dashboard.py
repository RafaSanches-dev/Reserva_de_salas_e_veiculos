from app import app, db
from models.dashboard import *
from models.mydb import *
from flask import render_template, redirect, url_for, session, flash, jsonify, request
from datetime import datetime
from services.reserva_notifications import email_reserva_status
from sqlalchemy import desc


def _perfil_atual() -> str:
    return session.get('cliente_perfil', 'cliente')


def _tem_perfil(*perfis: str) -> bool:
    return _perfil_atual() in perfis

@app.route('/dashboard')
def dashboard():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard/dashboard.html')

@app.route('/dashboard/content/home')
def content_home():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard/home.html')

@app.route('/dashboard/content/perfil', methods = ['GET', 'POST'])
def content_perfil():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    form = PerfilForm()

    # Preencher valores atuais no GET (e também quando o submit falha)
    cliente = Cliente.query.get(session['cliente_id'])
    if cliente:
        if form.cpf.data in (None, ''):
            form.cpf.data = cliente.cpf or ''
        if form.rg.data in (None, ''):
            form.rg.data = cliente.rg or ''

    if form.validate_on_submit():
        cpf = form.cpf.data
        rg = form.rg.data
        # funçao get pega o id do cliente da sessao, pega ja todas as informaçoes(todas as outras session...)
        cliente = Cliente.query.get(session['cliente_id'])
        cliente.cpf = cpf
        cliente.rg = rg
        # atualizar a session
        session['cliente_cpf'] = cpf
        session['cliente_rg'] = rg
        db.session.commit() 
        flash('Cadastro salvo.')
        return redirect(url_for('dashboard'))
    return render_template('dashboard/perfil.html', form = form, 
                           # session.get(), pega a informaçao da sessao, se nao tiver nada, retorno None(nenhum valor)
                           cliente_cpf = session.get('cliente_cpf'), 
                           cliente_rg = session.get('cliente_rg'))

@app.route('/dashboard/content/solicitar_reserva')
def content_solicitar_reserva():
    return render_template('dashboard/solicitacoes_de_reservas.html')

@app.route('/dashboard/content/solicitacoes_pendentes')
def content_solicitacoes_pendentes():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    if not _tem_perfil('aprovador'):
        return render_template('dashboard/sem_permissao.html', message='Você não tem permissão para aprovar/rejeitar reservas.')

    reservas_sala = (ReservaDeSala.query
                    .filter_by(status='pendente')
                    .order_by(ReservaDeSala.data.asc(), ReservaDeSala.inicio.asc())
                    .all())
    reservas_veiculo = (ReservaDeVeiculo.query
                        .filter_by(status='pendente')
                        .order_by(ReservaDeVeiculo.data_saida.asc(), ReservaDeVeiculo.horario_saida.asc())
                        .all())

    return render_template(
        'dashboard/solicitacoes_pendentes.html',
        reservas_sala=reservas_sala,
        reservas_veiculo=reservas_veiculo,
    )


def _get_modelo_reserva(tipo: str):
    if tipo == 'sala':
        return ReservaDeSala
    if tipo == 'veiculo':
        return ReservaDeVeiculo
    return None


def _notificar_status_reserva(tipo: str, reserva, status: str, motivo: str | None = None) -> None:
    cliente = getattr(reserva, 'cliente', None) or Cliente.query.get(getattr(reserva, 'cliente_id', None))
    if not cliente:
        return
    email_reserva_status(tipo, reserva, cliente, status=status, motivo=motivo)


@app.route('/dashboard/api/reservas/<tipo>/<int:reserva_id>/aprovar', methods=['POST'])
def api_aprovar_reserva(tipo: str, reserva_id: int):
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    if not _tem_perfil('aprovador'):
        return jsonify(ok=False, message='Sem permissão.'), 403

    Modelo = _get_modelo_reserva(tipo)
    if Modelo is None:
        return jsonify(ok=False, message='Tipo inválido.'), 400

    reserva = Modelo.query.get(reserva_id)
    if not reserva:
        return jsonify(ok=False, message='Reserva não encontrada.'), 404

    reserva.status = 'aprovado'
    reserva.motivo_rejeicao = None
    reserva.decidido_em = datetime.utcnow()
    reserva.decidido_por = session['cliente_id']
    db.session.commit()

    # Notificação por email (se configurado). Não falha a aprovação se o email falhar.
    _notificar_status_reserva(tipo, reserva, status='aprovada')

    return jsonify(ok=True, message='Reserva aprovada com sucesso.')


@app.route('/dashboard/api/reservas/<tipo>/<int:reserva_id>/rejeitar', methods=['POST'])
def api_rejeitar_reserva(tipo: str, reserva_id: int):
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    if not _tem_perfil('aprovador'):
        return jsonify(ok=False, message='Sem permissão.'), 403

    Modelo = _get_modelo_reserva(tipo)
    if Modelo is None:
        return jsonify(ok=False, message='Tipo inválido.'), 400

    reserva = Modelo.query.get(reserva_id)
    if not reserva:
        return jsonify(ok=False, message='Reserva não encontrada.'), 404

    payload = request.get_json(silent=True) or {}
    motivo = (payload.get('motivo') or '').strip()
    if not motivo:
        return jsonify(ok=False, message='Informe um motivo para rejeitar.'), 400

    reserva.status = 'rejeitado'
    reserva.motivo_rejeicao = motivo
    reserva.decidido_em = datetime.utcnow()
    reserva.decidido_por = session['cliente_id']
    db.session.commit()

    # Notificação por email (se configurado). Não falha a rejeição se o email falhar.
    _notificar_status_reserva(tipo, reserva, status='rejeitada', motivo=motivo)

    return jsonify(ok=True, message='Reserva rejeitada com sucesso.')


@app.route('/dashboard/content/minhas_reservas')
def content_minhas_reservas():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))

    cliente_id = session['cliente_id']
    reservas_sala = (ReservaDeSala.query
                    .filter_by(cliente_id=cliente_id)
                    .order_by(ReservaDeSala.data.desc(), ReservaDeSala.inicio.desc())
                    .all())
    reservas_veiculo = (ReservaDeVeiculo.query
                        .filter_by(cliente_id=cliente_id)
                        .order_by(ReservaDeVeiculo.data_saida.desc(), ReservaDeVeiculo.horario_saida.desc())
                        .all())

    return render_template(
        'dashboard/minhas_reservas.html',
        reservas_sala=reservas_sala,
        reservas_veiculo=reservas_veiculo,
    )

@app.route('/dashboard/content/avisos')
def content_avisos():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))

    avisos = Aviso.query.order_by(desc(Aviso.criado_em)).all()
    return render_template(
        'dashboard/avisos.html',
        avisos=avisos,
        is_aprovador=_tem_perfil('aprovador'),
    )


@app.route('/dashboard/api/avisos', methods=['POST'])
def api_criar_aviso():
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    if not _tem_perfil('aprovador'):
        return jsonify(ok=False, message='Sem permissão.'), 403

    titulo = (request.form.get('titulo') or '').strip()
    mensagem = (request.form.get('mensagem') or '').strip()
    tipo = (request.form.get('tipo') or 'info').strip().lower()

    if not titulo or not mensagem:
        return jsonify(ok=False, message='Preencha título e mensagem.'), 400

    if tipo not in {'info', 'important', 'warning', 'success'}:
        tipo = 'info'

    aviso = Aviso(
        titulo=titulo[:140],
        mensagem=mensagem,
        tipo=tipo,
        criado_em=datetime.utcnow(),
        criado_por=session['cliente_id'],
    )
    db.session.add(aviso)
    db.session.commit()
    return jsonify(ok=True, message='Aviso publicado com sucesso.')


@app.route('/dashboard/api/avisos/<int:aviso_id>/editar', methods=['POST'])
def api_editar_aviso(aviso_id: int):
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    if not _tem_perfil('aprovador'):
        return jsonify(ok=False, message='Sem permissão.'), 403

    aviso = Aviso.query.get(aviso_id)
    if not aviso:
        return jsonify(ok=False, message='Aviso não encontrado.'), 404

    payload = request.get_json(silent=True) or {}
    titulo = (request.form.get('titulo') or payload.get('titulo') or '').strip()
    mensagem = (request.form.get('mensagem') or payload.get('mensagem') or '').strip()
    tipo = (request.form.get('tipo') or payload.get('tipo') or aviso.tipo or 'info').strip().lower()

    if not titulo or not mensagem:
        return jsonify(ok=False, message='Preencha título e mensagem.'), 400

    if tipo not in {'info', 'important', 'warning', 'success'}:
        tipo = 'info'

    aviso.titulo = titulo[:140]
    aviso.mensagem = mensagem
    aviso.tipo = tipo
    db.session.commit()
    return jsonify(ok=True, message='Aviso atualizado com sucesso.')


@app.route('/dashboard/api/avisos/<int:aviso_id>/apagar', methods=['POST'])
def api_apagar_aviso(aviso_id: int):
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    if not _tem_perfil('aprovador'):
        return jsonify(ok=False, message='Sem permissão.'), 403

    aviso = Aviso.query.get(aviso_id)
    if not aviso:
        return jsonify(ok=False, message='Aviso não encontrado.'), 404

    db.session.delete(aviso)
    db.session.commit()
    return jsonify(ok=True, message='Aviso apagado com sucesso.')

@app.route('/dashboard/content/reserva/sala', methods = ['GET', 'POST'])
def content_reserva_sala():
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401
    form = ReservaSalaForm()
    if form.validate_on_submit():
        reserva_sala = ReservaDeSala(
            sala=form.sala.data,
            data=form.data.data,
            inicio=form.inicio.data,
            fim=form.fim.data,
            titulo_da_reserva=form.titulo_da_reserva.data,
            finalidade=form.finalidade.data,
            cliente_id=session['cliente_id'],
        )
        db.session.add(reserva_sala)
        db.session.commit()
        return jsonify(ok=True, message='Reserva de sala solicitada com sucesso.')

    if form.is_submitted():
        return jsonify(ok=False, message='Preencha todos os campos corretamente.'), 400

    return render_template('dashboard/reserva_sala.html', form=form)

@app.route('/dashboard/content/reserva/veiculo', methods = ['GET', 'POST'])
def content_reserva_veiculo():
    if 'cliente_id' not in session:
        return jsonify(ok=False, message='Sessão expirada. Faça login novamente.'), 401

    form = ReservaVeiculoForm()
    if form.validate_on_submit():
        reserva_veiculo = ReservaDeVeiculo(
            veiculo=form.veiculo.data,
            data_saida=form.data_saida.data,
            horario_saida=form.horario_saida.data,
            data_retorno=form.data_retorno.data,
            horario_retorno=form.horario_retorno.data,
            destino=form.destino.data,
            motivo=form.motivo.data,
            cliente_id=session['cliente_id'],
        )
        db.session.add(reserva_veiculo)
        db.session.commit()
        return jsonify(ok=True, message='Reserva de veículo solicitada com sucesso.')

    if form.is_submitted():
        return jsonify(ok=False, message='Preencha todos os campos corretamente.'), 400

    return render_template('dashboard/reserva_veiculo.html', form=form)