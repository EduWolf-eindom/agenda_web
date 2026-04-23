from sqlalchemy.orm import Session


def listar(model, db: Session):
    return db.query(model).order_by(model.nome).all()


def criar(model, nome: str, db: Session):
    item = model(nome=nome.upper())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def atualizar(model, item_id: int, nome: str, db: Session):
    item = db.query(model).get(item_id)
    if not item:
        return None
    item.nome = nome.upper()
    db.commit()
    return item


def excluir(model, item_id: int, db: Session):
    item = db.query(model).get(item_id)
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True