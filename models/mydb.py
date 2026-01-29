from app import db

class Cliente(db.Model):

    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)  # Aumentado para 255 (hash é grande)
    cpf = db.Column(db.String(25), nullable=True, unique=True) # Nullable=True (preenche depois)
    rg = db.Column(db.String(20), nullable=True, unique=True)  # Nullable=True (preenche depois)

class ReservaDeSala(db.Model):

    __tablename__ = 'reserva_de_sala'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sala = db.Column(db.Text, nullable=False)
    data = db.Column(db.Date, nullable=False)
    inicio = db.Column(db.Time, nullable=False)
    fim = db.Column(db.Time, nullable=False)
    titulo_da_reserva = db.Column(db.Text, nullable=False)
    finalidade = db.Column(db.Text, nullable=False)
    # foreignkey tem que colocar no modelo do banco de dados, nesse caso ela guarda qual cliente esta fazendo a reserva(o id do cliente)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)