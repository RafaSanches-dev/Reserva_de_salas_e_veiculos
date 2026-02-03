<!-- cspell:ignore cliente perfil reserva reservas reserva_de_sala reserva_de_veiculo motivo_rejeicao decidido_em decidido_por -->

# Passo a Passo

# Aprovação de reservas (usuário e aprovador)

O sistema tem 2 perfis (coluna `cliente.perfil`):

- `cliente`: pode solicitar reservas e ver as próprias reservas.
- `aprovador`: pode ver solicitações pendentes e aprovar/rejeitar.

## 1) Definir o primeiro aprovador (bootstrap)

Como ainda não existe tela pública para “virar aprovador”, você promove um usuário via SQL.

Exemplo (MySQL):

```sql
UPDATE cliente
SET perfil = 'aprovador'
WHERE email = 'SEU_EMAIL@exemplo.com';
```

Depois disso, faça logout/login para atualizar a sessão.

## 2) Aprovar/rejeitar

Usuários com perfil `aprovador`:

- Abrem `Solicitações Pendentes`
- Clicam em `Aprovar` ou `Rejeitar`
- Se rejeitar, o sistema pede o motivo e salva na reserva
