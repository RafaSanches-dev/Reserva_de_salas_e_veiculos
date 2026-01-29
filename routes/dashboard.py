from app import app, db
from models.dashboard import *
from models.mydb import *
from flask import render_template, redirect, url_for, session, flash
import os

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
    return render_template('dashboard/solicitacoes_pendentes.html')

@app.route('/dashboard/content/minhas_reservas')
def content_minhas_reservas():
    return render_template('dashboard/minhas_reservas.html')

@app.route('/dashboard/content/avisos')
def content_avisos():
    return render_template('dashboard/avisos.html')

@app.route('/dashboard/content/reserva/sala')
def content_reserva_sala():
    # Ler o arquivo HTML diretamente sem processar Jinja2(usa python em arquivo html)
    with open(os.path.join(app.template_folder, 'dashboard/reserva_sala.html'), 'r', encoding='utf-8') as f:
        return f.read()
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    form = ReservaSalaForm()

@app.route('/dashboard/content/reserva/veiculo')
def content_reserva_veiculo():
    # Ler o arquivo HTML diretamente sem processar Jinja2(usa python em arquivo html)
    with open(os.path.join(app.template_folder, 'dashboard/reserva_veiculo.html'), 'r', encoding='utf-8') as f:
        return f.read()