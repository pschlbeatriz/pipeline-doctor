"""Remove segredos de um log ANTES de ele sair do servidor rumo a IA."""
import re

# (nome, regex). Ordem importa: blocos/formatos especificos antes do generico.
_PADROES = [
    ("chave-privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\b")),
    ("bearer", re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-~+/]{16,}=*")),
    ("url-com-senha", re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)")),
    (
        "atribuicao-segredo",
        re.compile(
            r"(?i)\b([A-Z0-9_.\-]*(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|credential)[A-Z0-9_.\-]*)"
            r"(\s*[=:]\s*)(?!\[REDACTED)(\"[^\"\n]*\"|'[^'\n]*'|[^\s\"']+)"
        ),
    ),
]


def redigir(texto: str) -> tuple[str, int]:
    """Devolve (texto sem segredos, quantidade de trechos removidos)."""
    total = 0
    for nome, rx in _PADROES:
        if nome == "atribuicao-segredo":
            texto, n = rx.subn(r"\1\2[REDACTED]", texto)
        else:
            texto, n = rx.subn(f"[REDACTED:{nome}]", texto)
        total += n
    return texto, total
