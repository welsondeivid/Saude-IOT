from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import engine, get_db

# Cria as tabelas no banco de dados (SQLite) se elas não existirem
models.Base.metadata.create_all(bind=engine) 

app = FastAPI(title="IoT Microservice API")

# --- Configuração CORS (Essencial para o Frontend React) ---
# Permite que o frontend (ex: rodando na porta 3000) acesse o backend
origins = [
    "http://localhost:3000", # Adicione a porta que o React for usar
    "http://127.0.0.1:3000",
    # Adicione aqui o domínio do front em produção, se tiver
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# 1. ENDPOINT DE INGESTÃO (DADOS QUE VIRÃO DA EQUIPE SD)
# @ ELIS
# ----------------------------------------------------------------------

@app.post("/data/ingest/", response_model=schemas.SensorData)
def receive_iot_data(data: schemas.SensorDataCreate, db: Session = Depends(get_db)):
    """Recebe, valida e salva um novo JSON de dados do sensor no SQLite."""
    
    # Cria a instância do modelo de banco de dados
    db_record = models.SensorData(**data.model_dump())
    
    # Persiste no banco
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record

# ----------------------------------------------------------------------
# 2. ENDPOINT DE EXPOSIÇÃO (Para o Frontend de Exibição)
# ----------------------------------------------------------------------

@app.get("/data/latest/", response_model=list[schemas.SensorData])
def get_latest_data(limit: int = 10, db: Session = Depends(get_db)):
    """Retorna os registros de dados mais recentes para exibição."""
    
    # Consulta no SQLite: Ordena por timestamp decrescente e limita o número de resultados
    latest_records = db.query(models.SensorData) \
                       .order_by(desc(models.SensorData.timestamp)) \
                       .limit(limit) \
                       .all()
    
    return latest_records

# Rota de Status Simples
@app.get("/")
def read_root():
    return {"status": "API is running", "framework": "FastAPI"}