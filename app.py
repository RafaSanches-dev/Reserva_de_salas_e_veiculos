import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

# criar o app
app = Flask(__name__)

# configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg://postgres:CHANGE_ME@db.urvhsfehuhgbygiwpwaj.supabase.co:5432/postgres',
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# criar o banco de dados(conexão)
db = SQLAlchemy(app)

# importar as rotas das telas, depois de criar o app
# importar as rotas primeiro, depois os modelos do banco de dados, se não dá erro(conflito)
from routes.login import *
from routes.dashboard import *

# importar os modelos de banco de dados depois das rotas(rota primeiro depois os modelos)
from models.mydb import *

# iniciar o app
if __name__ == '__main__':
    app.run(debug=True)