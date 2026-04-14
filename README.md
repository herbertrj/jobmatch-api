# JobMatch API

Projeto pessoal para praticar FastAPI com um cenario de recrutamento.
A API simula um fluxo real: cadastrar candidatos, cadastrar vagas e calcular compatibilidade
entre os dois lados para gerar rankings.

O objetivo aqui e ter um backend organizado e claro, com autenticacao JWT, validacao de dados,
persistencia local em SQLite e testes automatizados cobrindo os fluxos principais.

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT (PyJWT)
- Pytest
- Ruff + Black

## Funcionalidades implementadas

- Health check da aplicacao (`GET /health`).
- Endpoint de versao (`GET /version`).
- Registro e login de usuario com token JWT.
- Consulta do usuario autenticado (`GET /api/v1/auth/me`).
- Criacao de candidatos (rota protegida por token).
- Listagem de candidatos com paginacao.
- Busca de candidatos com filtros (`skill` e `min_experience`).
- Criacao de vagas (rota protegida por token).
- Listagem de vagas com paginacao.
- Ranking de candidatos para uma vaga.
- Ranking de vagas para um candidato.
- Retorno detalhado no matching (score, skills atendidas/faltantes e experiencia).

## Estrutura do projeto

```text
app/
  api/routes/     # endpoints
  core/           # autenticacao e seguranca
  db/             # sessao e base SQLAlchemy
  models/         # modelos de banco
  schemas/        # contratos de entrada/saida
tests/
```

## Como rodar localmente

1. Crie e ative o ambiente virtual.
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Rode a API:

```bash
uvicorn app.main:app --reload
```

4. Acesse a documentacao:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Como rodar os testes

```bash
venv\Scripts\python -m pytest
```
