#!/usr/bin/env python3
"""
Script de teste para verificar a integração entre middleware e backend.
"""

import requests
import json
import time

# URLs dos serviços
MIDDLEWARE_URL = "http://localhost:5000"
BACKEND_URL = "http://localhost:8000"

# Dados de teste
test_data = {
    "bairros": {
        "Centro": [
            {
                "timestamp": "2025-01-20T10:00:00Z",
                "clima": {
                    "temperatura_ar": 25.5,
                    "umidade_relativa": 60.0,
                    "precipitacao": 0.0,
                    "cobertura_vegetal": 15.0
                },
                "qualidade_do_ar": {
                    "material_particulado_pm25": 20.0,
                    "monoxido_carbono": 2.0
                },
                "qualidade_da_agua": {
                    "ph_agua": 7.0,
                    "turbidez": 1.0,
                    "coliformes_totais": 100,
                    "cloro_residual": 0.5
                }
            }
        ]
    }
}

def test_backend_connection():
    """Testa se o backend está rodando."""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está rodando")
            return True
        else:
            print(f"❌ Backend retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está disponível")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com backend: {e}")
        return False

def test_middleware_connection():
    """Testa se o middleware está rodando."""
    try:
        response = requests.get(f"{MIDDLEWARE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Middleware está rodando")
            return True
        else:
            print(f"❌ Middleware retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Middleware não está disponível")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar com middleware: {e}")
        return False

def test_ingest_flow():
    """Testa o fluxo completo de ingest."""
    print("\n🔄 Testando fluxo de ingest...")
    
    try:
        response = requests.post(
            f"{MIDDLEWARE_URL}/ingest",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Dados enviados com sucesso!")
            return True
        else:
            print("❌ Falha ao enviar dados")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de ingest: {e}")
        return False

def main():
    """Executa todos os testes."""
    print("🧪 Iniciando testes de integração...")
    
    # Testa conexões
    backend_ok = test_backend_connection()
    middleware_ok = test_middleware_connection()
    
    if not backend_ok or not middleware_ok:
        print("\n❌ Serviços não estão rodando. Inicie os serviços antes de testar.")
        print("Backend: uvicorn src.backend.main:app --reload --port 8000")
        print("Middleware: python src/middleware/app.py")
        return
    
    # Testa fluxo de ingest
    ingest_ok = test_ingest_flow()
    
    if ingest_ok:
        print("\n🎉 Todos os testes passaram! A integração está funcionando.")
    else:
        print("\n❌ Alguns testes falharam. Verifique os logs dos serviços.")

if __name__ == "__main__":
    main()
