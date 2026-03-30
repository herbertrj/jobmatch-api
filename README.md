# JobMatch API

Projeto pessoal para praticar FastAPI com um tema de recrutamento.
Aqui eu estou construindo uma API para cadastrar candidatos e vagas, e depois adicionar uma logica de compatibilidade entre eles.

## Tecnologias

- Python
- FastAPI
- Pydantic
- Pytest
- Ruff + Black

## O que ja esta feito

- Endpoint de health check.
- Endpoint de versao.
- Criacao e listagem de candidatos.
- Criacao e listagem de vagas.
- Armazenamento em memoria (por enquanto).

## Proximos passos

- Adicionar score de compatibilidade entre candidatos e vagas.
- Adicionar persistencia com banco de dados relacional.
- Adicionar autenticacao e autorizacao.
- Melhorar a cobertura de testes.

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
