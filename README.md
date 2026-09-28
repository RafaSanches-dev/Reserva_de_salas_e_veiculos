# Sistema de Reserva de Salas e Veículos

Sistema web desenvolvido para facilitar o gerenciamento de reservas de **salas e veículos** para atividades acadêmicas e eventos.

O projeto foi desenvolvido durante a graduação em **Engenharia da Computação na UEMG – Unidade Ituiutaba**, com o objetivo de aplicar na prática conceitos de desenvolvimento web, banco de dados e organização de software.

## 📌 Sobre o projeto

A aplicação busca centralizar o processo de solicitação e gerenciamento de reservas, permitindo que usuários realizem solicitações e que responsáveis pelo sistema possam gerenciá-las.

O back-end foi desenvolvido em **Python utilizando Flask**, com integração a um banco de dados **MySQL através do SQLAlchemy**.

A aplicação também possui uma estrutura separada entre **rotas, modelos, serviços, templates e arquivos estáticos**, facilitando a organização e manutenção do código.

## 🚀 Funcionalidades

* 🔐 Autenticação de usuários
* 👤 Gerenciamento de perfil
* 🏫 Solicitação de reserva de salas
* 🚐 Solicitação de reserva de veículos
* 📋 Visualização e gerenciamento de reservas
* 🛠️ Área administrativa
* ✅ Aprovação de solicitações
* ❌ Rejeição de solicitações
* 📢 Sistema de avisos
* 📧 Estrutura para envio de e-mails
* 🔑 Recuperação de senha

## 🛠️ Tecnologias utilizadas

### Back-end

* Python
* Flask
* Flask-SQLAlchemy
* SQLAlchemy
* PyMySQL

### Front-end

* HTML
* CSS
* JavaScript
* Jinja2

### Banco de dados

* MySQL

### Bibliotecas e ferramentas

* Flask-WTF
* WTForms
* python-dotenv
* email-validator
* itsdangerous
* Git
* GitHub

As principais dependências utilizadas no projeto estão disponíveis no arquivo [`requirements.txt`](requirements.txt).

## 🏗️ Estrutura do projeto

```text
Reserva_de_salas_e_veiculos/
│
├── docs/                   # Documentação do projeto
│
├── models/                 # Modelos do banco de dados
│
├── routes/                 # Rotas da aplicação
│
├── services/               # Serviços e regras da aplicação
│
├── static/                 # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── ...
│
├── templates/              # Templates HTML
│
├── app.py                  # Inicialização da aplicação
├── config.py               # Configurações
├── requirements.txt        # Dependências do projeto
└── .gitignore              # Arquivos ignorados pelo Git
```

## ⚙️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/RafaSanches-dev/Reserva_de_salas_e_veiculos.git
```

Entre na pasta:

```bash
cd Reserva_de_salas_e_veiculos
```

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

Exemplo:

```env
SECRET_KEY=sua_chave_secreta
SQLALCHEMY_DATABASE_URI=mysql+pymysql://usuario:senha@localhost:3306/reserva_uemg

MAIL_SERVER=
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_USE_TLS=true
MAIL_USE_SSL=false
```

> **Importante:** não compartilhe o arquivo `.env` nem coloque senhas ou outras credenciais diretamente no código-fonte.

O arquivo `.env` já está configurado no `.gitignore` para não ser enviado ao repositório.

### 5. Configure o banco de dados

O projeto utiliza **MySQL**.

Crie um banco chamado `reserva_uemg` ou utilize outro nome e ajuste a variável `SQLALCHEMY_DATABASE_URI` no `.env`.

### 6. Execute a aplicação

```bash
python app.py
```

A aplicação estará disponível em:

```text
http://127.0.0.1:5000
```

## 🧩 Organização do código

O projeto foi organizado buscando separar diferentes responsabilidades da aplicação:

**Models**
Responsáveis pela representação das entidades e dados utilizados pelo sistema.

**Routes**
Responsáveis pelas rotas e pelo tratamento das requisições da aplicação.

**Services**
Concentram operações e regras utilizadas pelas diferentes partes do sistema.

**Templates**
Contêm as páginas HTML renderizadas pela aplicação.

**Static**
Armazena arquivos como CSS, JavaScript e outros recursos utilizados pela interface.

**Config**
Centraliza as configurações da aplicação e o carregamento das variáveis de ambiente.

## 🗄️ Banco de dados

A aplicação utiliza **MySQL** como banco de dados e **SQLAlchemy** como ORM.

A conexão é realizada através do `Flask-SQLAlchemy`, permitindo que os modelos da aplicação sejam utilizados para representar e manipular os dados do sistema.

## 📚 Objetivos do projeto

O desenvolvimento do sistema permitiu colocar em prática conhecimentos de:

* Desenvolvimento web com Python
* Framework Flask
* Banco de dados relacionais
* MySQL
* ORM com SQLAlchemy
* Autenticação de usuários
* Gerenciamento de sessões
* Organização de aplicações web
* Separação de responsabilidades
* Controle de versão com Git e GitHub
* Configuração de aplicações através de variáveis de ambiente

## 🔄 Próximos passos

Algumas possibilidades de evolução do projeto:

* [ ] Implementação de testes automatizados
* [ ] Melhorias na experiência do usuário
* [ ] Dashboard com estatísticas de reservas
* [ ] Controle mais detalhado de permissões
* [ ] Melhorias no sistema de notificações
* [ ] Deploy da aplicação em ambiente de produção
* [ ] Documentação mais detalhada da API
* [ ] Melhorias de segurança e validação

## 👨‍💻 Autor

**Rafael Sanches Rosolen**

Estudante de Engenharia da Computação na UEMG – Unidade Ituiutaba.

[GitHub](https://github.com/RafaSanches-dev) • [LinkedIn](https://www.linkedin.com/in/rafael-sanches-rosolen-705284259/)

---

⭐ Projeto desenvolvido como parte da minha formação acadêmica e do meu portfólio de desenvolvimento de software.
