import pytest

from app.redator import redigir

CASOS = [
    ("aws", "key=AKIAIOSFODNN7EXAMPLE", "AKIAIOSFODNN7EXAMPLE"),
    ("github", "token ghp_" + "a" * 36, "ghp_" + "a" * 36),
    ("google", "AIza" + "B" * 35, "AIza" + "B" * 35),
    ("bearer", "Authorization: Bearer abcdefghijklmnop1234567890", "abcdefghijklmnop1234567890"),
    ("jwt", "eyJhbGciOi.eyJzdWIiOiIx.SflKxwRJSMeKKF2QT4fw", "SflKxwRJSMeKKF2QT4fw"),
    ("url", "git clone https://user:s3nh4@github.com/x/y.git", "s3nh4"),
    ("var", "DB_PASSWORD=hunter2", "hunter2"),
    ("var-aspas", 'api_key: "abc 123"', "abc 123"),
    ("chave-privada", "-----BEGIN RSA PRIVATE KEY-----\nMIIabc\n-----END RSA PRIVATE KEY-----", "MIIabc"),
]


@pytest.mark.parametrize("nome,entrada,segredo", CASOS, ids=[c[0] for c in CASOS])
def test_remove_segredo(nome, entrada, segredo):
    saida, n = redigir(entrada)
    assert segredo not in saida
    assert n >= 1


def test_preserva_log_sem_segredo():
    log = "ERROR: Cannot find module 'express'\n  at Function.Module._load"
    assert redigir(log) == (log, 0)


def test_nome_da_variavel_continua_visivel():
    saida, _ = redigir("NPM_TOKEN=abc123")
    assert saida == "NPM_TOKEN=[REDACTED]"


def test_nao_conta_duas_vezes():
    _, n = redigir("SECRET=[REDACTED]")
    assert n == 0
