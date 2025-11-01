#!/bin/bash
# Script para iniciar o servidor Uvicorn com o aplicativo FastAPI

echo "🚀 Iniciando Backend FastAPI..."

# Vai para a pasta do projeto
cd "$(dirname "$0")" || exit 1

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "💡 Execute primeiro: python -m venv venv"
    exit 1
fi

# Ativa o ambiente virtual (detecta Windows ou Linux/Mac)
echo "📦 Ativando ambiente virtual..."
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Arquivo de ativação do ambiente virtual não encontrado!"
    exit 1
fi

# Verifica se está no ambiente virtual correto
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Falha ao ativar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual ativado: $VIRTUAL_ENV"

# Atualiza pip
echo "🔄 Atualizando pip..."
python -m pip install --upgrade pip

# Instala dependências
echo "📥 Instalando dependências..."
python -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências!"
    exit 1
fi

echo "✅ Dependências instaladas!"

# Inicia o servidor. O --reload é bom para o desenvolvimento.
# src.main:app se refere ao arquivo 'main.py' dentro da pasta 'src' e ao objeto 'app' dentro dele.
echo "🌐 Iniciando servidor FastAPI na porta 8000..."
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload