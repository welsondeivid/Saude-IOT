// Configuração da API
const MIDDLEWARE_URL = import.meta.env.VITE_MIDDLEWARE_URL || "http://localhost:5000";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

// Dependências de autenticação do front (token após login)
import { getToken as getStoredToken } from "./authService";

/**
 * Obtém um token de autenticação do backend
 * @param {string} username - Nome de usuário (padrão: "admin")
 * @param {string} password - Senha (padrão: "admin123")
 * @returns {Promise<string>} Token de acesso
 * @note Certifique-se de criar um usuário no backend antes de usar.
 *       Use POST /users/ para criar um novo usuário se necessário.
 */
export async function getAuthToken() {
    const token = getStoredToken();
    if (!token) {
        throw new Error("Não autenticado. Faça login para obter o token.");
    }
    return token;
}

/**
 * Busca o relatório diário do middleware
 * @param {string} token - Token de autenticação (opcional, usa cache se não fornecido)
 * @returns {Promise<Object>} Dados do relatório diário
 */
export async function getRelatorioDiario() {
    const authToken = getStoredToken();

    if (!authToken) {
        throw new Error("Não autenticado. Faça login para acessar o dashboard.");
    }

    try {
        const response = await fetch(`${MIDDLEWARE_URL}/relatorio-diario`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${authToken}`,
                "Content-Type": "application/json",
            },
        });

        if (response.status === 401) {
            throw new Error("Sessão expirada ou inválida. Faça login novamente.");
        }

        if (!response.ok) {
            throw new Error(`Erro ao buscar relatório: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro ao buscar relatório diário:", error);
        throw error;
    }
}

/**
 * Lista os bairros disponíveis
 * @returns {Promise<Array>} Lista de bairros
 */
export async function listBairros() {
    try {
        const response = await fetch(`${MIDDLEWARE_URL}/bairros`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Erro ao buscar bairros: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro ao buscar bairros:", error);
        throw error;
    }
}

