from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class ClimaSchema(BaseModel):
    temperatura_ar: float
    umidade_relativa: float
    precipitacao: float
    cobertura_vegetal: float

class QualidadeArSchema(BaseModel):
    material_particulado_pm25: float
    monoxido_carbono: float

class QualidadeAguaSchema(BaseModel):
    ph_agua: float
    turbidez: float
    coliformes_totais: int
    cloro_residual: float

class MedicaoSchema(BaseModel):
    timestamp: datetime
    clima: ClimaSchema
    qualidade_do_ar: QualidadeArSchema
    qualidade_da_agua: QualidadeAguaSchema

class DadosBairroSchema(BaseModel):
    bairros: Dict[str, List[MedicaoSchema]]