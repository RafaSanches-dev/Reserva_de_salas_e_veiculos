from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# criar o app
app = Flask(__name__)

# configurações
app.config.from_object(Config)

# criar o banco de dados(conexão)
db = SQLAlchemy(app)

# importar as rotas das telas, depois de criar o app
# importar as rotas primeiro, depois os modelos do banco de dados, se não dá erro(conflito)
from routes.login import *
from routes.dashboard import *
from routes.api import *

# importar os modelos de banco de dados depois das rotas(rota primeiro depois os modelos)
from models.mydb import *

# iniciar o app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)