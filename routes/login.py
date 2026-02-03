from app import app, db
from models.login import *
from models.mydb import Cliente
from flask import render_template, redirect, url_for, flash, session
from services.email_service import send_email
from services.tokens import generate_password_reset_token, verify_password_reset_token
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import html
from services.email_templates import subject_with_prefix, wrap_html_email, button

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
        novo_cliente = Cliente(nome=nome, email=email, senha=senha_criptografada, perfil='cliente')
        try:
            db.session.add(novo_cliente)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Não foi possível finalizar o cadastro: email/CPF/RG já cadastrado.')
            return render_template('login/cadastro.html', form=form)
        flash('Cadastro realizado com sucesso.')
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
                session['cliente_cpf'] = cliente.cpf
                session['cliente_rg'] = cliente.rg
                session['cliente_perfil'] = getattr(cliente, 'perfil', 'cliente')
                flash('Login realizado com sucesso.')
                return redirect( url_for('dashboard') )
            else:
                # senha incorreta
                flash('Senha incorreta. Tente novamente.')
                return render_template('login/login.html', form = form)
        else:
            # email não cadastrado
            flash('Email não cadastrado. Por favor, cadastre-se.')
            return render_template('login/login.html', form = form)
    
    return render_template('login/login.html', form = form)

@app.route('/esqueceu_senha', methods=['GET', 'POST'])
def esqueceu_senha():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = (form.email.data or '').strip().lower()
        cliente = Cliente.query.filter_by(email=email).first()

        # Mensagem sempre genérica para não vazar se o email existe.
        flash('Se este email estiver cadastrado, enviaremos um link para redefinir a senha.')

        if cliente:
            token = generate_password_reset_token(cliente.email)
            link = url_for('redefinir_senha', token=token, _external=True)
            subject = subject_with_prefix('Recuperação de senha')
            expira_em_min = int(app.config.get('SECURITY_PASSWORD_RESET_MAX_AGE_SECONDS', 3600)) // 60

            body_text = (
                f"Olá, {cliente.nome}.\n\n"
                f"Recebemos um pedido para redefinir sua senha.\n"
                f"Use o link abaixo para criar uma nova senha (expira em ~{expira_em_min} min):\n"
                f"{link}\n\n"
                f"Se você não solicitou, ignore este email."
            )

            intro_html = f"Olá, <strong>{html.escape(str(cliente.nome))}</strong>."
            content_html = (
                f"<p>Recebemos um pedido para redefinir sua senha.</p>"
                f"<p>Este link expira em aproximadamente <strong>{expira_em_min} minutos</strong>.</p>"
                f"{button(link, 'Redefinir minha senha')}"
                f"<p>Se o botão não funcionar, copie e cole este link no navegador:<br>"
                f"<a href=\"{html.escape(link)}\">{html.escape(link)}</a></p>"
            )

            body_html = wrap_html_email(
                title='Recuperação de senha',
                intro_html=intro_html,
                content_html=content_html,
            )

            ok, err = send_email(
                subject=subject,
                recipients=[cliente.email],
                body_text=body_text,
                body_html=body_html,
            )
            if not ok:
                app.logger.warning('Falha ao enviar email de recuperação: %s', err)

        return redirect(url_for('login'))

    return render_template('login/recuperacao_de_senha.html', form=form)


@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token: str):
    email = verify_password_reset_token(token)
    if not email:
        flash('Link inválido ou expirado. Solicite novamente a recuperação de senha.')
        return redirect(url_for('esqueceu_senha'))

    cliente = Cliente.query.filter_by(email=email).first()
    if not cliente:
        flash('Link inválido. Solicite novamente a recuperação de senha.')
        return redirect(url_for('esqueceu_senha'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        nova_senha = form.nova_senha.data
        cliente.senha = generate_password_hash(nova_senha)
        db.session.commit()
        flash('Senha redefinida com sucesso. Faça login novamente.')
        return redirect(url_for('login'))

    return render_template('login/redefinir_senha.html', form=form)

@app.route('/logout')
def logout():
    # session.clear(), limpa toda a session(ou como tem os if na dashboard o usuario volta para o login)
    session.clear()
    flash('Você saiu com sucesso.')
    return redirect( url_for('login') )