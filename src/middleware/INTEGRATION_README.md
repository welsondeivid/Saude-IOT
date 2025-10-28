# Integração Middleware → Backend

## Resumo das Mudanças

A rota `/ingest` no middleware foi modificada para fazer requisições HTTP para a rota `/importar-dados` no backend, em vez de salvar diretamente no banco de dados local.

## Arquivos Modificados

### `src/middleware/app.py`
- ✅ Adicionado import da biblioteca `requests`
- ✅ Configurada URL do backend (`BACKEND_URL = "http://localhost:8000"`)
- ✅ Modificada rota `/ingest` para fazer requisição HTTP
- ✅ Modificada rota `/ingest_v2` para fazer requisição HTTP
- ✅ Adicionado tratamento de erros robusto (timeout, conexão, etc.)

### `src/middleware/requirements.txt`
- ✅ Adicionada dependência `requests==2.31.0`

## Como Funciona Agora

1. **Cliente** envia dados para `/ingest` no middleware
2. **Middleware** valida os dados recebidos
3. **Middleware** faz requisição HTTP para `/importar-dados` no backend
4. **Backend** processa e salva os dados no banco
5. **Middleware** retorna resposta baseada no resultado do backend

## Tratamento de Erros

O middleware agora trata os seguintes cenários:

- ✅ **503 Service Unavailable**: Backend não está disponível
- ✅ **504 Gateway Timeout**: Backend demorou muito para responder (>30s)
- ✅ **500 Internal Server Error**: Erros internos do middleware
- ✅ **Outros códigos**: Repassa o status code do backend

## Como Testar

### 1. Instalar dependências
```bash
cd src/middleware
pip install -r requirements.txt
```

### 2. Iniciar os serviços

**Backend (FastAPI):**
```bash
cd src/backend
uvicorn main:app --reload --port 8000
```

**Middleware (Flask):**
```bash
cd src/middleware
python app.py
```

### 3. Executar teste automatizado
```bash
cd src/middleware
python test_integration.py
```

### 4. Teste manual com curl
```bash
curl -X POST http://localhost:5000/ingest \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Configuração

A URL do backend pode ser alterada modificando a variável `BACKEND_URL` no arquivo `app.py`:

```python
BACKEND_URL = "http://localhost:8000"  # Altere conforme necessário
```

## Vantagens da Nova Arquitetura

1. **Separação de responsabilidades**: Middleware apenas roteia, backend processa
2. **Escalabilidade**: Backend pode ser escalado independentemente
3. **Manutenibilidade**: Lógica de negócio centralizada no backend
4. **Flexibilidade**: Fácil troca de backend sem afetar clientes
5. **Monitoramento**: Melhor rastreamento de erros e performance
