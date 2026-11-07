# 🩺 Pipeline Doctor

[![CI](https://github.com/pschlbeatriz/pipeline-doctor/actions/workflows/ci.yml/badge.svg)](https://github.com/pschlbeatriz/pipeline-doctor/actions/workflows/ci.yml)

Cole o log de uma falha de CI/CD (GitHub Actions, Docker, pytest, npm...) e receba um diagnóstico de SRE gerado por IA Generativa (Gemini): causa provável, severidade, comandos para verificar, correção sugerida e rascunho de post-mortem.

**Aplicação online:** https://pipeline-doctor-ogp9.onrender.com

## O diferencial: segurança de ponta a ponta

| Risco | Defesa | Onde |
|---|---|---|
| Log contém senha/token e vai para uma API externa | **Redator** remove AWS keys, tokens GitHub/Google/Slack, JWT, Bearer, chaves privadas, senhas em URL e `VAR=segredo` *antes* da chamada | `backend/app/redator.py` |
| Log malicioso tenta mandar na IA ("ignore as regras...") | Log é tratado como dado não confiável, isolado em `<log>…</log>`, com delimitador sanitizado | `backend/app/ia.py` |
| IA devolve lixo | Saída forçada por schema (Pydantic) e validada; erro vira 503 limpo | `backend/app/schemas.py` |
| Abuso consome a cota gratuita | Rate limit por IP e tamanho máximo de log | `backend/app/main.py` |
| Chave vazar | `.env` no `.gitignore`; chave só no painel do Render | `.env.example` |

## API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/saude` | Health check |
| POST | `/diagnosticar` | `{"log": "..."}` → diagnóstico estruturado + `segredos_removidos` |
| GET | `/historico` | Últimos 10 diagnósticos (SQLite; só resumo, nunca o log) |

Docs interativas em `/docs`.

## Rodar localmente

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp ../.env.example .env   # preencha GEMINI_API_KEY
uvicorn app.main:app --reload
```

Abra http://127.0.0.1:8000 (o backend serve o frontend).

## Docker

```bash
docker build -t pipeline-doctor .
docker run -p 8000:8000 -e GEMINI_API_KEY=sua_chave pipeline-doctor
```

## Testes

```bash
cd backend && python -m pytest
```

A chamada ao Gemini é simulada (mock); nenhum teste usa rede nem chave. O build falha se a cobertura ficar abaixo de 70%.

## Estrutura

```
backend/   FastAPI, redator, integração com IA, histórico SQLite, testes
frontend/  HTML/JS puro (sem build)
.github/   pipeline de CI
Dockerfile  imagem da aplicação (validada no CI)
render.yaml  deploy no Render
```

## Ideias futuras

- GitHub App que comenta o diagnóstico direto no PR que falhou
- Detecção de falhas recorrentes (flaky tests) sobre o histórico, com banco persistente (Postgres)
- Redator com lista de padrões configurável

Veja [DECISOES.md](DECISOES.md) para as escolhas técnicas.
