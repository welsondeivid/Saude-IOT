#!/bin/bash
# Script para iniciar o front-end React/Vite

echo "🚀 Iniciando Front-end..."

cd "$(dirname "$0")" || exit 1
cd saude-iot-front-end || exit 1

echo "📂 Pasta: $(pwd)"

if [ ! -d "node_modules" ]; then
    echo "📦 node_modules não encontrado!"
    echo "💡 Instalando dependências..."
    npm install || { echo "❌ Erro ao instalar dependências!"; exit 1; }
    echo "✅ Dependências instaladas!"
else
    echo "✅ Dependências encontradas!"
fi

echo "🌐 Iniciando servidor de desenvolvimento..."
npm run dev