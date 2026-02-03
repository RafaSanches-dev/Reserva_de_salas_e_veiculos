# API (organização e boas práticas)

Este projeto expõe endpoints JSON em `/api/...` para organizar integrações e separar melhor front/back.

Autenticação: usa a **sessão** do Flask (mesma do site). Se não estiver logado, retorna `401`.

## Endpoints

### Usuário

- `GET /api/me`
  - Retorna dados do usuário logado.

### Reservas (cliente)

- `GET /api/reservas/minhas`
  - Retorna reservas de sala e veículo do usuário.

- `POST /api/reservas/sala`
  - JSON:
    - `sala`, `data` (`YYYY-MM-DD`), `inicio` (`HH:MM`), `fim` (`HH:MM`)
    - `titulo_da_reserva`, `finalidade`

- `POST /api/reservas/veiculo`
  - JSON:
    - `veiculo`, `data_saida`, `horario_saida`, `data_retorno`, `horario_retorno`
    - `destino`, `motivo`

### Reservas (aprovador)

- `GET /api/reservas/pendentes`
  - Apenas `perfil=aprovador`.

- `POST /api/reservas/<tipo>/<id>/aprovar`
- `POST /api/reservas/<tipo>/<id>/rejeitar`
  - JSON: `{ "motivo": "..." }`

## Formato de resposta

- Sucesso: `{ "ok": true, "message": "...", "data": { ... } }`
- Erro: `{ "ok": false, "message": "..." }` com status HTTP adequado.
