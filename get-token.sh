#!/bin/bash
# Script para obter token de autenticação

BACKEND_URL="http://localhost:8000"

# Verifica se username e password foram passados
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Uso: ./get-token.sh <username> <password>"
    echo "Exemplo: ./get-token.sh admin admin123"
    exit 1
fi

USERNAME="$1"
PASSWORD="$2"

echo "🔐 Obtendo token de autenticação..."
echo "Usuario: $USERNAME"
echo ""

# Faz a requisição para obter o token
RESPONSE=$(curl -s -X POST "${BACKEND_URL}/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=${USERNAME}&password=${PASSWORD}")

# Extrai o token da resposta
TOKEN=$(echo $RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ Erro ao obter token!"
    echo "Resposta do servidor: $RESPONSE"
    exit 1
fi

echo "✅ Token obtido com sucesso!"
echo ""
echo "═══════════════════════════════════════════════════════"
echo "$TOKEN"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "💡 Use este token nas requisições com o header:"
echo "   Authorization: Bearer $TOKEN"
echo ""
echo "📝 Exemplo de uso com curl:"
echo "   curl -H \"Authorization: Bearer $TOKEN\" http://localhost:5000/relatorio-diario"
