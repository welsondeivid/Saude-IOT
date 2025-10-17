from pydantic import BaseModel
from datetime import datetime

# ----------------------------------------------------------------------
# ESQUEMAS DE ENTRADA (Input - O que a equipe de IoT envia)
# ----------------------------------------------------------------------

class SensorDataCreate(BaseModel):
    # Campos que esperamos receber no POST/JSON
    sensor_id: str
    temperatura: float
    timestamp: datetime

# ----------------------------------------------------------------------
# ESQUEMAS DE SAÍDA (Output - O que o front recebe)
# ----------------------------------------------------------------------

class SensorData(SensorDataCreate):
    # Inclui o ID gerado pelo banco de dados
    id: int

    # Configuração necessária para o Pydantic ler os objetos do SQLAlchemy
    class Config:
        from_attributes = True