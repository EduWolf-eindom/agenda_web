from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services import catalogo_service

router = APIRouter(prefix="/api/catalogos", tags=["Catálogos"])


# ---------- ASSUNTOS ----------
@router.get("/assuntos", response_model=list[schemas.ItemResponse])
def listar_assuntos(db: Session = Depends(get_db)):
    return catalogo_service.listar(models.Assunto, db)


@router.post("/assuntos", response_model=schemas.ItemResponse)
def criar_assunto(payload: schemas.BaseNome, db: Session = Depends(get_db)):
    return catalogo_service.criar(models.Assunto, payload.nome, db)


@router.put("/assuntos/{id}", response_model=schemas.ItemResponse)
def atualizar_assunto(id: int, payload: schemas.BaseNome, db: Session = Depends(get_db)):
    item = catalogo_service.atualizar(models.Assunto, id, payload.nome, db)
    if not item:
        raise HTTPException(status_code=404, detail="Assunto não encontrado")
    return item


@router.delete("/assuntos/{id}")
def excluir_assunto(id: int, db: Session = Depends(get_db)):
    if not catalogo_service.excluir(models.Assunto, id, db):
        raise HTTPException(status_code=404, detail="Assunto não encontrado")
    return {"ok": True}


# ---------- FASES ----------
@router.get("/fases", response_model=list[schemas.ItemResponse])
def listar_fases(db: Session = Depends(get_db)):
    return catalogo_service.listar(models.Fase, db)


@router.post("/fases", response_model=schemas.ItemResponse)
def criar_fase(payload: schemas.BaseNome, db: Session = Depends(get_db)):
    return catalogo_service.criar(models.Fase, payload.nome, db)


@router.put("/fases/{id}", response_model=schemas.ItemResponse)
def atualizar_fase(id: int, payload: schemas.BaseNome, db: Session = Depends(get_db)):
    item = catalogo_service.atualizar(models.Fase, id, payload.nome, db)
    if not item:
        raise HTTPException(status_code=404, detail="Fase não encontrada")
    return item


@router.delete("/fases/{id}")
def excluir_fase(id: int, db: Session = Depends(get_db)):
    if not catalogo_service.excluir(models.Fase, id, db):
        raise HTTPException(status_code=404, detail="Fase não encontrada")
    return {"ok": True}


# ---------- SITUACOES ----------
@router.get("/situacoes", response_model=list[schemas.ItemResponse])
def listar_situacoes(db: Session = Depends(get_db)):
    return catalogo_service.listar(models.Situacao, db)


@router.post("/situacoes", response_model=schemas.ItemResponse)
def criar_situacao(payload: schemas.BaseNome, db: Session = Depends(get_db)):
    return catalogo_service.criar(models.Situacao, payload.nome, db)


@router.put("/situacoes/{id}", response_model=schemas.ItemResponse)
def atualizar_situacao(id: int, payload: schemas.BaseNome, db: Session = Depends(get_db)):
    item = catalogo_service.atualizar(models.Situacao, id, payload.nome, db)
    if not item:
        raise HTTPException(status_code=404, detail="Situação não encontrada")
    return item


@router.delete("/situacoes/{id}")
def excluir_situacao(id: int, db: Session = Depends(get_db)):
    if not catalogo_service.excluir(models.Situacao, id, db):
        raise HTTPException(status_code=404, detail="Situação não encontrada")
    return {"ok": True}
