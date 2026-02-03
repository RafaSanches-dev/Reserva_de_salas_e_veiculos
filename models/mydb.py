from app import db

class Cliente(db.Model):

    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)  # Aumentado para 255 (hash é grande)
    cpf = db.Column(db.String(25), nullable=True, unique=True) # Nullable=True (preenche depois)
    rg = db.Column(db.String(20), nullable=True, unique=True)  # Nullable=True (preenche depois)
    # perfil define permissões dentro do sistema
    # valores esperados: 'cliente' | 'aprovador'
    perfil = db.Column(db.String(20), nullable=False, default='cliente')

class ReservaDeSala(db.Model):

    __tablename__ = 'reserva_de_sala'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sala = db.Column(db.Text, nullable=False)
    data = db.Column(db.Date, nullable=False)
    inicio = db.Column(db.Time, nullable=False)
    fim = db.Column(db.Time, nullable=False)
    titulo_da_reserva = db.Column(db.Text, nullable=False)
    finalidade = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    motivo_rejeicao = db.Column(db.Text, nullable=True)
    decidido_em = db.Column(db.DateTime, nullable=True)
    decidido_por = db.Column(db.Integer, nullable=True)
    # foreignkey tem que colocar no modelo do banco de dados, nesse caso ela guarda qual cliente esta fazendo a reserva(o id do cliente)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', foreign_keys=[cliente_id])

class ReservaDeVeiculo(db.Model):

    __tablename__ = 'reserva_de_veiculo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    veiculo = db.Column(db.Text, nullable=False)
    data_saida = db.Column(db.Date, nullable=False)
    horario_saida = db.Column(db.Time, nullable=False)
    data_retorno = db.Column(db.Date, nullable=False)
    horario_retorno = db.Column(db.Time, nullable=False)
    destino = db.Column(db.Text, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    motivo_rejeicao = db.Column(db.Text, nullable=True)
    decidido_em = db.Column(db.DateTime, nullable=True)
    decidido_por = db.Column(db.Integer, nullable=True)
    # forignkey, nessa caso, vai guardar o id do cliente lá da tabela cliente na variável cliente_id
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cliente = db.relationship('Cliente', foreign_keys=[cliente_id])


class Aviso(db.Model):

    __tablename__ = 'aviso'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    titulo = db.Column(db.String(140), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    # valores esperados: 'info' | 'important' | 'warning' | 'success'
    tipo = db.Column(db.String(20), nullable=False, default='info')
    criado_em = db.Column(db.DateTime, nullable=False)
    criado_por = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    autor = db.relationship('Cliente', foreign_keys=[criado_por])