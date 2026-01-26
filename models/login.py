from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# o validador Email do wtf.validators já verifica se o email está em um formato válido, 
# e ele precisa da biblioteca email_validator instalada

class CadastroForm(FlaskForm):

    nome = StringField('Nome completo:', validators = [DataRequired()])
    email = StringField('Email:', validators = [DataRequired(), Email()])
    senha = PasswordField('Senha:', validators = [DataRequired()])
    confirmar_senha = PasswordField('Confirmar Senha:', validators = [DataRequired(), EqualTo('senha', message = 'As senhas devem coincidir.')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):

    email = StringField('Email:', validators = [DataRequired(), Email()])
    senha = PasswordField('Senha', validators = [DataRequired()])
    submit = SubmitField('Entrar')

