# JobMatch API

API REST desenvolvida em Python com FastAPI para simular um fluxo de recrutamento:
cadastro de candidatos, cadastro de vagas e ranking de compatibilidade entre os dois lados.

Este projeto foi construido como item de portfolio para demonstrar dominio de backend,
com foco em modelagem de dados, autenticacao com JWT, boas praticas de API e testes automatizados.

## O que este projeto resolve

Em processos seletivos, uma dor comum e comparar rapidamente os perfis com as vagas abertas.
Esta API organiza esse fluxo e entrega:

- cadastro e manutencao de candidatos e vagas;
- filtros para busca de candidatos;
- score de compatibilidade com explicacao do resultado;
- endpoints protegidos por autenticacao para operacoes sensiveis.

## Stack e ferramentas utilizadas

- `Python 3.11+`
- `FastAPI` (web framework)
- `Pydantic` (validacao e contratos de entrada/saida)
- `SQLAlchemy` (ORM)
- `SQLite` (persistencia local)
- `PyJWT` + `passlib` (autenticacao e hash de senha)
- `Pytest` + `httpx` (testes de integracao da API)
- `Ruff` e `Black` (qualidade e padronizacao de codigo)

## Funcionalidades implementadas

- **Observabilidade basica**
  - `GET /health`
  - `GET /version`
- **Autenticacao**
  - `POST /api/v1/auth/register`
  - `POST /api/v1/auth/login`
  - `GET /api/v1/auth/me`
- **Candidatos**
  - `POST /api/v1/candidates` (protegido)
  - `GET /api/v1/candidates` (com `skip` e `limit`)
  - `GET /api/v1/candidates/search` (filtros `skill` e `min_experience`)
  - `GET /api/v1/candidates/{candidate_id}`
  - `PUT /api/v1/candidates/{candidate_id}` (protegido)
  - `DELETE /api/v1/candidates/{candidate_id}` (protegido)
- **Vagas**
  - `POST /api/v1/jobs` (protegido)
  - `GET /api/v1/jobs` (com `skip` e `limit`)
  - `GET /api/v1/jobs/{job_id}`
  - `PUT /api/v1/jobs/{job_id}` (protegido)
  - `DELETE /api/v1/jobs/{job_id}` (protegido)
- **Matching e ranking**
  - `GET /api/v1/match/jobs/{job_id}/candidates`
  - `GET /api/v1/match/candidates/{candidate_id}/jobs`

## Regra de compatibilidade (matching)

A API aplica uma regra simples e explicavel para o score:

- cada skill obrigatoria atendida soma `20` pontos;
- se a experiencia do candidato atende o minimo da vaga, soma `20` pontos;
- score final limitado a `100`.

O retorno inclui:

- `score`
- `matched_skills`
- `missing_skills`
- `experience_ok`

Isso permite justificar por que um candidato (ou vaga) ficou acima no ranking.

## Arquitetura do projeto

```text
app/
  api/routes/     # endpoints HTTP por dominio (auth, candidates, jobs, match, health)
  core/           # autenticacao e seguranca (JWT e autorizacao)
  db/             # conexao, engine e sessao SQLAlchemy
  models/         # entidades persistidas no banco
  schemas/        # contratos Pydantic de request/response
tests/
  test_main.py    # cenarios de integracao da API
```

## Como executar localmente

### 1) Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd jobmatch_api
```

### 2) Criar e ativar ambiente virtual

No Windows (PowerShell):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4) Subir a API

```bash
uvicorn app.main:app --reload
```

API disponivel em `http://127.0.0.1:8000`.

## Documentacao interativa

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Fluxo rapido de uso

1. Registrar usuario em `POST /api/v1/auth/register`.
2. Fazer login em `POST /api/v1/auth/login` e copiar o `access_token`.
3. Enviar token no header:
   - `Authorization: Bearer <token>`
4. Criar candidatos e vagas.
5. Consultar os endpoints de matching para visualizar o ranking.

## Qualidade e testes

Executar testes:

```bash
py -m pytest -q
```

Executar lint:

```bash
py -m ruff check .
```

Executar formatacao:

```bash
py -m black .
```

Atualmente, a suite cobre fluxos principais de:

- health/version;
- autenticacao (registro, login, rota protegida);
- CRUD de candidatos e vagas;
- paginacao e filtros;
- ranking de compatibilidade.

## Proximos passos (evolucao)

- adicionar migrations com Alembic;
- separar configuracoes por ambiente (`.env`);
- incluir testes de casos limite do algoritmo de score;
- adicionar CI para rodar testes e lint automaticamente.
