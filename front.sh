#!/bin/bash
# Script para iniciar o front-end React/Vite

echo "🚀 Iniciando Front-end..."

# Vai para a pasta do projeto
cd "$(dirname "$0")" || exit 1

# Vai para a pasta do front-end
cd saude-iot-front-end || exit 1

echo "📂 Pasta: $(pwd)"

# Verifica se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 node_modules não encontrado!"
    echo "💡 Instalando dependências..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências!"
        exit 1
    fi
    echo "✅ Dependências instaladas!"
else
    echo "✅ Dependências encontradas!"
fi

# Inicia o servidor de desenvolvimento
echo "🌐 Iniciando servidor de desenvolvimento..."
npm run dev

