from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Bairro(Base):
    __tablename__ = "bairro"

    id_bairro = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # Relação com Medicao
    medicoes = relationship("Medicao", back_populates="bairro")

class Medicao(Base):
    __tablename__ = "medicao"

    id_medicao = Column(Integer, primary_key=True, index=True)
    id_bairro = Column(Integer, ForeignKey("bairro.id_bairro"))
    data_hora = Column(DateTime, nullable=False)

    # Relações
    bairro = relationship("Bairro", back_populates="medicoes")
    valores = relationship("ValorMedido", back_populates="medicao")

class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    # Relação com Indicador
    indicadores = relationship("Indicador", back_populates="categoria")

class Indicador(Base):
    __tablename__ = "indicador"

    id_indicador = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    unidade_medida = Column(String, nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria"))

    # Relações
    categoria = relationship("Categoria", back_populates="indicadores")
    valores = relationship("ValorMedido", back_populates="indicador")

class ValorMedido(Base):
    __tablename__ = "valor_medido"

    id_valor = Column(Integer, primary_key=True, index=True)
    id_medicao = Column(Integer, ForeignKey("medicao.id_medicao"))
    id_indicador = Column(Integer, ForeignKey("indicador.id_indicador"))
    valor = Column(Float, nullable=False)

    # Relações
    medicao = relationship("Medicao", back_populates="valores")
    indicador = relationship("Indicador", back_populates="valores")



