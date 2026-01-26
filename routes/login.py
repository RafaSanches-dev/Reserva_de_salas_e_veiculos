from app import app, db
from models.login import *
from models.mydb import Cliente
from flask import render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = form.senha.data
        # criptografar a senha
        senha_criptografada = generate_password_hash(senha)
        # novo cliente  
        novo_cliente = Cliente( nome = nome, email = email, senha = senha_criptografada)
        db.session.add(novo_cliente)
        db.session.commit()
        flash('Cadastro realizado com sucesso!')
        return redirect( url_for('cadastro'))
    return render_template('login/cadastro.html', 
                           form = form)

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): 
        email = form.email.data
        senha = form.senha.data
        # buscar cliente pelo email      colouna do banco = email digitado, e o first() é o primeiro registro do banco
        cliente = Cliente.query.filter_by(email = email).first()
        if cliente:
            # email existe, verificar senha(senha criptografada, senha)
            if check_password_hash(cliente.senha, senha):
                # login bem-sucedido
                # aqui você pode criar sessão, redirecionar para dashboard, etc
                # criar sessão, importar session do flask
                session['cliente_id'] = cliente.id
                session['cliente_nome'] = cliente.nome
                session['cliente_email'] = cliente.email
                return redirect( url_for('dashboard') )
            else:
                # senha incorreta
                flash('Senha incorreta. Tente Novamente.')
                return render_template('login/login.html', form = form)
        else:
            # email não cadastrado
            flash('Email não cadastrado. Por favor, cadastre-se')
            return render_template('login/login.html', form = form)
    
    return render_template('login/login.html', form = form)

@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('login/recuperacao_de_senha.html')