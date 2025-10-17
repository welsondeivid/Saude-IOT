from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

# Exemplo de Modelo de Dados de Sensor
class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True) # ID do aparelho IoT que enviou
    temperatura = Column(Float)            # Exemplo de dado recebido
    timestamp = Column(DateTime)           # Quando o dado foi enviado
    
    # Se quiser, defina um método de representação
    def __repr__(self):
        return f"SensorData(id={self.id}, sensor_id='{self.sensor_id}')"