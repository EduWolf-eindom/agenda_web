from sqlalchemy.orm import Session
from datetime import timedelta
from app import models, schemas

def create_item(db: Session, item: schemas.AgendaCreate):
    end_time = item.start_time + timedelta(minutes=10)

    db_item = models.AgendaItem(
        start_time=item.start_time,
        end_time=end_time,
        title=item.title,
        description=item.description
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item