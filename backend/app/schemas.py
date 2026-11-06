from enum import Enum

from pydantic import BaseModel, Field


class Categoria(str, Enum):
    dependencia = "dependencia"
    teste = "teste"
    build = "build"
    configuracao = "configuracao"
    permissao = "permissao"
    rede = "rede"
    infraestrutura = "infraestrutura"
    outro = "outro"


class Severidade(str, Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"
    critica = "critica"


class Diagnostico(BaseModel):
    """Formato que a IA e OBRIGADA a devolver (validado antes de chegar ao usuario)."""

    causa_provavel: str = Field(description="Causa raiz mais provavel, em 1-2 frases")
    categoria: Categoria
    severidade: Severidade
    confianca: float = Field(ge=0, le=1, description="0 a 1")
    comandos_verificar: list[str] = Field(max_length=6, description="Comandos para confirmar a hipotese")
    correcao_sugerida: str
    resumo_postmortem: str = Field(description="2-3 frases para registrar o incidente")


class PedidoDiagnostico(BaseModel):
    log: str = Field(min_length=20, max_length=20_000)


class RespostaDiagnostico(BaseModel):
    diagnostico: Diagnostico
    segredos_removidos: int
