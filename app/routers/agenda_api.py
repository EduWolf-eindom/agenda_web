from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas, crud
from datetime import datetime
from fastapi import HTTPException
from datetime import timedelta
from app.services.contratos_importer import importar_contratos

router = APIRouter(prefix="/api/agenda", tags=["Agenda API"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contratos/importar")
def importar_contratos_manual(db: Session = Depends(get_db)):
    resultado = importar_contratos(db)
    return resultado


@router.get("/contratos")
def listar_contratos(cliente: str, db: Session = Depends(get_db)):
    cliente = cliente.upper()

    contratos = (
        db.query(models.Contrato)
        .filter(models.Contrato.cliente_nome.contains(cliente))
        .all()
    )

    return [
        c.numero_contrato
        for c in contratos
    ]

@router.get("/")
def list_events(db: Session = Depends(get_db)):
    items = db.query(models.AgendaItem).all()

    return [
        {
            "id": item.id,
            "title": item.title,
            "start": item.start_time,
            "end": item.end_time
        }
        for item in items
    ]

@router.post("/", response_model=schemas.AgendaResponse)
def create_agenda(item: schemas.AgendaCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

from datetime import timedelta

# ========== CRIAR EVENTO ================

@router.post("/")
def create_event(item: schemas.AgendaCreate, db: Session = Depends(get_db)):
    start = item.start_time

    db_item = models.AgendaItem(
        start_time=start,
        end_time=start + timedelta(minutes=10),

        cliente_nome=item.cliente_nome.upper(),
        contrato_numero=item.contrato_numero.upper() if item.contrato_numero else None,

        assunto_id=item.assunto_id,
        fase_id=item.fase_id,
        situacao_id=item.situacao_id,

        descricao=item.descricao.upper() if item.descricao else None
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ============ EDITAR EVENTO =============

@router.put("/{item_id}")
def update_event(item_id: int, item: schemas.AgendaCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.AgendaItem).get(item_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    start = item.start_time

    db_item.start_time = start
    db_item.end_time = start + timedelta(minutes=10)

    db_item.cliente_nome = item.cliente_nome.upper()
    db_item.contrato_numero = item.contrato_numero.upper() if item.contrato_numero else None

    db_item.assunto_id = item.assunto_id
    db_item.fase_id = item.fase_id
    db_item.situacao_id = item.situacao_id

    db_item.descricao = item.descricao.upper() if item.descricao else None

    db.commit()
    db.refresh(db_item)
    return db_item


# =============== EXCLUIR EVENTO =================


@router.delete("/{item_id}")
def delete_event(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.AgendaItem).get(item_id)

    if not db_item:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    db.delete(db_item)
    db.commit()
    return {"ok": True}




