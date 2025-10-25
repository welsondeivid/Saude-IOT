import random
import datetime

# Clima (°C, %, mm/h)
TEMP_AR_MIN, TEMP_AR_MAX = 15.0, 38.0
UMIDADE_MIN, UMIDADE_MAX = 30.0, 95.0
PRECIPITACAO_MIN, PRECIPITACAO_MAX = 0.0, 50.0
COBERTURA_VEGETAL_MIN, COBERTURA_VEGETAL_MAX = 20.0, 90.0

# Qualidade do ar
PM25_MIN, PM25_MAX = 5.0, 120.0
CO_MIN, CO_MAX = 0.0, 6.0

# Qualidade da água
PH_MIN, PH_MAX = 5.5, 9.0
TURBIDEZ_MIN, TURBIDEZ_MAX = 0.1, 10.0
COLIFORMES_MIN, COLIFORMES_MAX = 0, 500
CLORO_RESIDUAL_MIN, CLORO_RESIDUAL_MAX = 0.0, 1.5

def gerar_clima():
    return {
        "temperatura_ar": round(random.uniform(TEMP_AR_MIN, TEMP_AR_MAX), 1),
        "umidade_relativa": round(random.uniform(UMIDADE_MIN, UMIDADE_MAX), 1),
        "precipitacao": round(random.uniform(PRECIPITACAO_MIN, PRECIPITACAO_MAX), 1),
        "cobertura_vegetal": round(random.uniform(COBERTURA_VEGETAL_MIN, COBERTURA_VEGETAL_MAX), 1),
    }

def gerar_qualidade_ar():
    return {
        "material_particulado_pm25": round(random.uniform(PM25_MIN, PM25_MAX), 1),
        "monoxido_carbono": round(random.uniform(CO_MIN, CO_MAX), 1),
    }

def gerar_qualidade_agua():
    return {
        "ph_agua": round(random.uniform(PH_MIN, PH_MAX), 1),
        "turbidez": round(random.uniform(TURBIDEZ_MIN, TURBIDEZ_MAX), 1),
        "coliformes_totais": random.randint(COLIFORMES_MIN, COLIFORMES_MAX),
        "cloro_residual": round(random.uniform(CLORO_RESIDUAL_MIN, CLORO_RESIDUAL_MAX), 1),
    }

def gerar_bairro(nome_bairro: str):
    return {
        "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "clima": gerar_clima(),
        "qualidade_do_ar": gerar_qualidade_ar(),
        "qualidade_da_agua": gerar_qualidade_agua(),
    }