from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# criar o app
app = Flask(__name__)

# configurações
app.config['SECRET_KEY'] = 'haha'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:EAEACDF099@localhost/reserva_uemg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# criar o banco de dados(conexão)
db = SQLAlchemy(app)

# importar os modelos, depois as rotas do banco de dados
from models.login import *

# importar as rotas das telas, depois de criar o app
from routes.login import *
from routes.dashboard import *

# iniciar o app
if __name__ == '__main__':
    app.run(debug=True)