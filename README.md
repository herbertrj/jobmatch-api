# JobMatch API

JobMatch API e um projeto de portfolio backend construido com FastAPI.  
O objetivo e simular uma API de mercado para gerenciar candidatos e vagas, e depois oferecer recomendacoes de compatibilidade.

## Objetivos do Projeto

- Demonstrar habilidades praticas de backend para vagas de estagio/junior.
- Aplicar fundamentos de boas APIs (validacao, versionamento e testes).
- Evoluir o projeto de forma incremental, com commits claros e realistas.

## Stack Tecnologica

- Python
- FastAPI
- Pydantic
- Pytest
- Ruff + Black

## Escopo Atual (MVP Dia 1)

- Endpoint de health check.
- Endpoint de versao.
- Criacao e listagem de candidatos.
- Criacao e listagem de vagas.
- Armazenamento em memoria para iteracao rapida.

## Proximos Passos Planejados

- Adicionar score de compatibilidade entre candidatos e vagas.
- Adicionar persistencia com banco de dados relacional.
- Adicionar autenticacao e autorizacao.
- Adicionar pipeline de CI e cobertura de testes.

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
pytest
```
