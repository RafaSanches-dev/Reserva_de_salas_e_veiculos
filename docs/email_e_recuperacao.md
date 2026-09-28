# Email e recuperação de senha

Este projeto envia emails por SMTP para:

- Notificar o usuário quando uma reserva é **aprovada** ou **rejeitada**.
- Enviar link de **recuperação de senha** (token com expiração).

## Variáveis de ambiente

Defina estas variáveis (ex.: no Windows, nas variáveis do sistema; ou usando um `.env` via seu método preferido):

- `SECRET_KEY` (obrigatório em produção)
- `SQLALCHEMY_DATABASE_URI` (obrigatório; por exemplo, `mysql+pymysql://usuario:senha@localhost:3306/reserva_uemg`)

### SMTP

- `MAIL_SERVER` (ex.: `smtp.gmail.com`)
- `MAIL_PORT` (ex.: `587` com TLS ou `465` com SSL)
- `MAIL_USE_TLS` (`true/false`, padrão `true`)
- `MAIL_USE_SSL` (`true/false`, padrão `false`)
- `MAIL_USERNAME` (seu email/login SMTP)
- `MAIL_PASSWORD` (senha/app password do SMTP)
- `MAIL_DEFAULT_SENDER` (opcional; padrão = `MAIL_USERNAME`)
- `MAIL_FROM_NAME` (opcional; padrão = `Reserva UEMG`)


### Identidade visual / assunto

- `APP_NAME` (opcional; padrão `Reserva UEMG`)
- `EMAIL_SUBJECT_PREFIX` (opcional; padrão `[Reserva UEMG]`)
- `EMAIL_LOGO_URL` (opcional; se vazio tenta usar `static/imagens/Logo_UEMG.png`)
- `EMAIL_BRAND_PRIMARY` (opcional; cor principal, padrão `#0b5ed7`)

### DEV (não enviar de verdade)

- `MAIL_SUPPRESS_SEND=true`

### Token de redefinição

- `SECURITY_PASSWORD_RESET_SALT` (opcional)
- `SECURITY_PASSWORD_RESET_MAX_AGE_SECONDS` (opcional; padrão `3600` = 1 hora)

## Fluxo de recuperação

- Tela: `/esqueceu_senha`
- O sistema envia um link: `/redefinir_senha/<token>`
- Ao definir uma nova senha, o token expira por tempo.
