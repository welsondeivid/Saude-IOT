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

@app.post("/importar-dados/")
def importar_dados_bairros(dados: schemas.DadosBairroSchema, db: Session = Depends(get_db)):
    """
    Recebe os dados de saúde urbana dos bairros, valida com os schemas
    e insere de forma estruturada no banco de dados.
    """
    
    for nome_bairro, medicoes_list in dados.bairros.items():
        
        # 1. Encontra o bairro no banco de dados ou cria um novo se não existir
        bairro_db = db.query(models.Bairro).filter(models.Bairro.nome == nome_bairro).first()
        if not bairro_db:
            bairro_db = models.Bairro(nome=nome_bairro)
            db.add(bairro_db)
            db.commit()
            db.refresh(bairro_db)

        # 2. Itera sobre cada registro de medição (cada hora) para aquele bairro
        for medicao_item in medicoes_list:
            
            # 3. Cria o registro principal da "Medicao"
            nova_medicao = models.Medicao(
                id_bairro=bairro_db.id_bairro,
                data_hora=medicao_item.timestamp
            )
            db.add(nova_medicao)
            db.commit()
            db.refresh(nova_medicao)
            
            # Dicionário para facilitar a iteração
            all_data = {
                'clima': medicao_item.clima.dict(),
                'qualidade_do_ar': medicao_item.qualidade_do_ar.dict(),
                'qualidade_da_agua': medicao_item.qualidade_da_agua.dict()
            }

            for nome_categoria, indicadores in all_data.items():
                for nome_indicador, valor in indicadores.items():
                    
                    # Busca o ID do indicador no banco (ex: busca por "temperatura_ar")
                    indicador_db = db.query(models.Indicador).filter(models.Indicador.nome == nome_indicador).first()
                    
                    if indicador_db:
                        # Cria o registro do valor medido associado à medição principal
                        novo_valor = models.ValorMedido(
                            id_medicao=nova_medicao.id_medicao,
                            id_indicador=indicador_db.id_indicador,
                            valor=valor
                        )
                        db.add(novo_valor)

    db.commit()
    return {"status": "Dados importados com sucesso!"}

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