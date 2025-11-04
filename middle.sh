#!/bin/bash
# Script para iniciar o middleware Flask

echo "🚀 Iniciando Middleware Flask..."

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
if [[ "$VIRTUAL_ENV" != *"Saude-IOT"* ]]; then
    echo "❌ Falha ao ativar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual ativado: $VIRTUAL_ENV"

# Atualiza pip
echo "🔄 Atualizando pip..."
python -m pip install --upgrade pip

# Instala dependências do middleware
echo "📥 Instalando dependências do middleware..."
python -m pip install -r src/middleware/requirements.txt

# Vai para a pasta do middleware
cd src/middleware || exit 1

# Configura variáveis de ambiente do Flask
export FLASK_APP=app
export FLASK_ENV=development

# Inicia o servidor Flask
python -m flask run --debug --port 5000 --host 0.0.0.0
