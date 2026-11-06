import pytest
from fastapi.testclient import TestClient

from app import main
from app.schemas import Categoria, Diagnostico, Severidade

FALSO = Diagnostico(
    causa_provavel="Dependencia ausente",
    categoria=Categoria.dependencia,
    severidade=Severidade.media,
    confianca=0.9,
    comandos_verificar=["npm ls express"],
    correcao_sugerida="npm install express",
    resumo_postmortem="Build falhou por modulo ausente.",
)


@pytest.fixture(autouse=True)
def _limpa_estado(monkeypatch, tmp_path):
    main._acessos.clear()
    monkeypatch.setenv("DB_PATH", str(tmp_path / "teste.db"))
    monkeypatch.setenv("RATE_LIMIT_PER_MIN", "10")


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture
def ia_falsa(monkeypatch):
    """Mock da IA: nenhuma chamada de rede nos testes. Guarda o que seria enviado."""
    enviados = []

    def falsa(log):
        enviados.append(log)
        return FALSO

    monkeypatch.setattr(main.ia, "diagnosticar", falsa)
    return enviados
