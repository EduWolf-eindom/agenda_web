from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True)
    cliente_nome = Column(String, index=True, nullable=False)
    numero_contrato = Column(String, nullable=False)
    status = Column(String, nullable=True)



class Assunto(Base):
    __tablename__ = "assuntos"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)


class Fase(Base):
    __tablename__ = "fases"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)


class Situacao(Base):
    __tablename__ = "situacoes"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)


class AgendaItem(Base):
    __tablename__ = "agenda"

    id = Column(Integer, primary_key=True, index=True)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    cliente_nome = Column(String, nullable=False)
    contrato_numero = Column(String, nullable=True)

    assunto_id = Column(Integer, ForeignKey("assuntos.id"))
    fase_id = Column(Integer, ForeignKey("fases.id"))
    situacao_id = Column(Integer, ForeignKey("situacoes.id"))

    descricao = Column(Text, nullable=True)

    assunto = relationship("Assunto")
    fase = relationship("Fase")
    situacao = relationship("Situacao")