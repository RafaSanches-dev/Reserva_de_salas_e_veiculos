from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length

class PerfilForm(FlaskForm):
     
     cpf = StringField('CPF:', validators = [DataRequired(), length(max=20)])
     rg = StringField(' RG:', validators = [DataRequired(), length(max=25)])
     submit = SubmitField('Salvar')

class ReservaSalaForm(FlaskForm):

     # precisa ser SelectField para criar um campo de seleção
     # [], lista, (), tupla, {} dicionario
     sala = SelectField(
          'Sala:',
          choices=[
               # valor que vai ser salvo no banco, texto que vai aparece na tela do usuário
               ('Laboratório 01', 'Laboratório 01'),
               ('Laboratório 02', 'Laboratório 02'),
               ('Sala de Reunião', 'Sala de Reunião'),
          ],
          validators=[DataRequired()]
     )
     data = DateField('Data:', validators = [DataRequired()])
     inicio = TimeField('Início:', validators = [DataRequired()])
     fim = TimeField('Fim:', validators = [DataRequired()])
     titulo_da_reserva = TextAreaField('Título da reserva:', validators = [DataRequired()])
     finalidade = TextAreaField('Finalidade:', validators = [DataRequired()])
     submit = SubmitField('Solicitar Reserva')

class ReservaVeiculoForm(FlaskForm):

     veiculo = SelectField(
     'Veículo:', 
     choices=[
          ('Van Escolar', 'Van Escolar'),
          ('Carro Administrativo', 'Carro Administrativo'),
          ('Ônibus Universitário', 'Ônibus Universitário')    
          ], validators=[DataRequired()]

     )
     data_saida = DateField('Data de Saída:', validators = [DataRequired()])
     horario_saida = TimeField('Horário de Saída:', validators = [DataRequired()])
     data_retorno = DateField('Data de Retorno:', validators = [DataRequired()])
     horario_retorno = TimeField('Horario de Retorno:', validators = [DataRequired()])
     destino = TextAreaField('Destino:', validators = [DataRequired()])
     motivo = TextAreaField('Motivo:', validators = [DataRequired()])
     submit = SubmitField('Solicitar Reserva')
    