# JobMatch API

Projeto pessoal para praticar FastAPI com um tema de recrutamento.
A ideia e simular um fluxo de selecao completo: cadastrar candidatos, cadastrar vagas e ranquear os candidatos mais aderentes para cada vaga.
O foco do projeto e mostrar uma API backend organizada, com validacao de dados, regras de compatibilidade e testes automatizados.
Hoje a implementacao usa armazenamento em memoria para manter o projeto simples de executar e facil de evoluir.

## Tecnologias

- Python
- FastAPI
- Pydantic
- Pytest
- Ruff + Black

## O que o projeto faz

- Endpoint de health check.
- Endpoint de versao.
- Criacao e listagem de candidatos.
- Criacao e listagem de vagas.
- Ranking de candidatos por vaga com score de compatibilidade (skills + experiencia).
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
