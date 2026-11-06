import os
import time
from collections import defaultdict, deque
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles

from . import ia
from .redator import redigir
from .schemas import PedidoDiagnostico, RespostaDiagnostico

load_dotenv()

app = FastAPI(title="Pipeline Doctor", version="1.0.0")

# ponytail: rate limit em memoria (1 processo). Usar Redis se escalar para varias instancias.
_acessos: dict[str, deque] = defaultdict(deque)


def _limitar(ip: str) -> None:
    limite = int(os.getenv("RATE_LIMIT_PER_MIN", "10"))
    agora = time.monotonic()
    fila = _acessos[ip]
    while fila and agora - fila[0] > 60:
        fila.popleft()
    if len(fila) >= limite:
        raise HTTPException(429, "Muitas requisicoes. Tente novamente em instantes.")
    fila.append(agora)


@app.get("/saude")
def saude():
    return {"status": "ok", "ia_configurada": bool(os.getenv("GEMINI_API_KEY"))}


@app.post("/diagnosticar", response_model=RespostaDiagnostico)
def diagnosticar(pedido: PedidoDiagnostico, request: Request):
    _limitar(request.client.host if request.client else "?")
    log_limpo, removidos = redigir(pedido.log)
    try:
        diag = ia.diagnosticar(log_limpo)
    except ia.IAIndisponivel as e:
        raise HTTPException(503, str(e))
    return RespostaDiagnostico(diagnostico=diag, segredos_removidos=removidos)


# Frontend servido pelo mesmo servico: 1 URL publica, sem CORS. Montado por ultimo.
_front = Path(__file__).resolve().parents[2] / "frontend"
if _front.is_dir():
    app.mount("/", StaticFiles(directory=_front, html=True), name="frontend")
