// Configuração da API
const MIDDLEWARE_URL = import.meta.env.VITE_MIDDLEWARE_URL || "http://localhost:5000";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

// Armazena o token em memória (em produção, considere usar localStorage ou um gerenciador de estado)
let cachedToken = null;

/**
 * Obtém um token de autenticação do backend
 * @param {string} username - Nome de usuário (padrão: "admin")
 * @param {string} password - Senha (padrão: "admin123")
 * @returns {Promise<string>} Token de acesso
 * @note Certifique-se de criar um usuário no backend antes de usar.
 *       Use POST /users/ para criar um novo usuário se necessário.
 */
export async function getAuthToken(
    username = import.meta.env.VITE_API_USERNAME,
    password = import.meta.env.VITE_API_PASSWORD
) {
    try {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${BACKEND_URL}/token`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error("Credenciais inválidas. Verifique se o usuário existe no backend.");
            }
            throw new Error(`Erro ao obter token: ${response.statusText}`);
        }

        const data = await response.json();
        cachedToken = data.access_token;
        return cachedToken;
    } catch (error) {
        console.error("Erro ao obter token:", error);
        throw error;
    }
}

/**
 * Busca o relatório diário do middleware
 * @param {string} token - Token de autenticação (opcional, usa cache se não fornecido)
 * @returns {Promise<Object>} Dados do relatório diário
 */
export async function getRelatorioDiario(token = null) {
    // Tenta usar token do localStorage primeiro, depois o passado, depois o cache, depois pega um novo
    const storedToken = typeof window !== 'undefined' ? localStorage.getItem("access_token") : null;
    const authToken = storedToken || token || cachedToken;

    if (!authToken) {
        // Tenta obter token automaticamente
        try {
            await getAuthToken();
        } catch (error) {
            throw new Error("Não foi possível autenticar. Verifique se o backend está rodando.");
        }
    }

    try {
        const response = await fetch(`${MIDDLEWARE_URL}/relatorio-diario`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${authToken || cachedToken}`,
                "Content-Type": "application/json",
            },
        });

        if (response.status === 401) {
            // Token expirado ou inválido, tenta obter um novo
            await getAuthToken();
            return getRelatorioDiario(cachedToken);
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

