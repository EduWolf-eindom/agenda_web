from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# =====================================================================
# AGENDA
# =====================================================================
class AgendaCreate(BaseModel):
    start_time: datetime
    cliente_nome: str

    contrato_numero: Optional[str] = None
    assunto_id: Optional[int] = None
    fase_id: Optional[int] = None
    situacao_id: Optional[int] = None
    descricao: Optional[str] = None


class AgendaResponse(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime

    cliente_nome: str
    contrato_numero: Optional[str]

    assunto_id: Optional[int]
    fase_id: Optional[int]
    situacao_id: Optional[int]

    descricao: Optional[str]

    class Config:
        from_attributes = True  # Pydantic v2


# =====================================================================
# CATÁLOGOS (ASSUNTO / FASE / SITUAÇÃO)
# =====================================================================
class BaseNome(BaseModel):
    nome: str


class ItemResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True