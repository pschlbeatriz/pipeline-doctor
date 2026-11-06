"""Historico de diagnosticos em SQLite (stdlib). Guarda so o resumo, NUNCA o log:
a URL e publica e o historico e visivel para todos."""
import os
import sqlite3
from contextlib import closing

from .schemas import Diagnostico


def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(os.getenv("DB_PATH", "pipeline_doctor.db"))
    con.row_factory = sqlite3.Row
    con.execute(
        "CREATE TABLE IF NOT EXISTS diagnosticos ("
        "id INTEGER PRIMARY KEY, criado_em TEXT DEFAULT CURRENT_TIMESTAMP,"
        "categoria TEXT, severidade TEXT, causa TEXT)"
    )
    return con


def salvar(d: Diagnostico) -> None:
    with closing(_conn()) as con, con:
        con.execute(
            "INSERT INTO diagnosticos (categoria, severidade, causa) VALUES (?, ?, ?)",
            (d.categoria.value, d.severidade.value, d.causa_provavel),
        )


def recentes(limite: int = 10) -> list[dict]:
    with closing(_conn()) as con:
        linhas = con.execute(
            "SELECT criado_em, categoria, severidade, causa FROM diagnosticos ORDER BY id DESC LIMIT ?",
            (limite,),
        ).fetchall()
    return [dict(l) for l in linhas]
