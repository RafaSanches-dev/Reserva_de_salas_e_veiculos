from app import app
from models.dashboard import *
from flask import render_template, redirect, url_for, session
import os

@app.route('/dashboard')
def dashboard():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard/dashboard.html')

@app.route('/dashboard/content/home')
def content_home():
    return render_template('dashboard/home.html')

@app.route('/dashboard/content/perfil')
def content_perfil():
    return render_template('dashboard/perfil.html')

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
    # Ler o arquivo HTML diretamente sem processar Jinja2
    with open(os.path.join(app.template_folder, 'dashboard/reservas_sala.html'), 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/dashboard/content/reserva/veiculo')
def content_reserva_veiculo():
    # Ler o arquivo HTML diretamente sem processar Jinja2
    with open(os.path.join(app.template_folder, 'dashboard/reservas_veiculo.html'), 'r', encoding='utf-8') as f:
        return f.read()