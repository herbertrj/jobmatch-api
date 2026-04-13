# JobMatch API

Projeto pessoal para praticar FastAPI com um tema de recrutamento.
A ideia e simular um fluxo de selecao completo: cadastrar candidatos, cadastrar vagas e ranquear os candidatos mais aderentes para cada vaga.
O foco do projeto e mostrar uma API backend organizada, com validacao de dados, regras de compatibilidade e testes automatizados.
Hoje a implementacao usa SQLite para persistir dados localmente de forma simples.

## Tecnologias

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT (PyJWT)
- Pytest
- Ruff + Black

## O que o projeto faz

- Endpoint de health check.
- Endpoint de versao.
- Cadastro e login de usuario com token JWT.
- Consulta do usuario logado via token (`/auth/me`).
- Criacao e listagem de candidatos.
- Busca de candidatos com filtros por skill e experiencia minima.
- Criacao e listagem de vagas.
- Rotas de criacao protegidas por token.
- Listagens com paginacao via parametros `skip` e `limit`.
- Ranking de candidatos por vaga com score de compatibilidade (skills + experiencia).
- Ranking de vagas por candidato com score de compatibilidade.
- Retorno detalhado do matching: pontuacao, skills atendidas, skills faltantes e status de experiencia.

## Como Rodar Localmente

1. Crie e ative um ambiente virtual.
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

## Como Rodar os Testes

```bash
venv\Scripts\python -m pytest
```
