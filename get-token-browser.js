// Script para obter token via navegador
// Abra o console do navegador (F12) após fazer login e execute:

// Pegar o token armazenado
const token = localStorage.getItem('access_token');
console.log('Token:', token);

// Copiar automaticamente para clipboard
navigator.clipboard.writeText(token);
console.log('Token copiado para clipboard!');
