from app import db

class Cliente(db.Model):

    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)  # Aumentado para 255 (hash é grande)
    rg = db.Column(db.String(20), nullable=True, unique=True)  # Nullable=True (preenche depois)
    cpf = db.Column(db.String(25), nullable=True, unique=True) # Nullable=True (preenche depois)

