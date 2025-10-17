#!/bin/bash
# Script para iniciar o servidor Uvicorn com o aplicativo FastAPI

# Instala as dependências (caso não tenham sido instaladas ainda)
pip install -r requirements.txt

# Inicia o servidor. O --reload é bom para o desenvolvimento.
# src.main:app se refere ao arquivo 'main.py' dentro da pasta 'src' e ao objeto 'app' dentro dele.
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload