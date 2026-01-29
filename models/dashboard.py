from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, FieldList
from wtforms.validators import DataRequired, length

class PerfilForm(FlaskForm):
     
     cpf = StringField('CPF:', validators = [DataRequired(), length(max=20)])
     rg = StringField(' RG:', validators = [DataRequired(), length(max=25)])
     submit = SubmitField('Salvar')

class ReservaSalaForm(FlaskForm):

     sala = FieldList(StringField('Sala:', validators = [DataRequired()]), max_entries=1)
     data = DateField('Data:', validators = [DataRequired()])