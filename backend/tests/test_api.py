from app import main

LOG = "npm ERR! Cannot find module 'express' in /home/runner/work/app"


def test_saude(client):
    r = client.get("/saude")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_diagnosticar_ok(client, ia_falsa):
    r = client.post("/diagnosticar", json={"log": LOG})
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["diagnostico"]["categoria"] == "dependencia"
    assert corpo["segredos_removidos"] == 0


def test_segredo_nunca_chega_na_ia(client, ia_falsa):
    log = LOG + "\nGEMINI_API_KEY=AIza" + "x" * 35 + "\nDB_PASSWORD=hunter2"
    r = client.post("/diagnosticar", json={"log": log})
    assert r.json()["segredos_removidos"] == 2
    assert "hunter2" not in ia_falsa[0] and "AIza" not in ia_falsa[0]


def test_log_curto_demais_422(client, ia_falsa):
    assert client.post("/diagnosticar", json={"log": "oi"}).status_code == 422


def test_log_grande_demais_422(client, ia_falsa):
    assert client.post("/diagnosticar", json={"log": "x" * 20_001}).status_code == 422


def test_rate_limit_429(client, ia_falsa, monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_PER_MIN", "2")
    codigos = [client.post("/diagnosticar", json={"log": LOG}).status_code for _ in range(3)]
    assert codigos == [200, 200, 429]


def test_ia_indisponivel_503(client, monkeypatch):
    def falha(_):
        raise main.ia.IAIndisponivel("fora do ar")

    monkeypatch.setattr(main.ia, "diagnosticar", falha)
    r = client.post("/diagnosticar", json={"log": LOG})
    assert r.status_code == 503


def test_frontend_servido(client):
    r = client.get("/")
    assert r.status_code == 200 and "Pipeline Doctor" in r.text
