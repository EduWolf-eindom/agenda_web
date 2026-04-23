from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app import models
from app.routers import agenda_api, views
import os
from app.services.contratos_importer import importar_contratos
from app.database import SessionLocal
from app.routers import catalogos_api


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agenda Web")

app.mount(
    "/static",
    StaticFiles(directory=os.path.join("static")),
    name="static"
)

# @app.on_event("startup")
# def carregar_contratos():
#    db = SessionLocal()
#    importar_contratos(db)
#    db.close()


app.include_router(agenda_api.router)
app.include_router(views.router)
app.include_router(catalogos_api.router)