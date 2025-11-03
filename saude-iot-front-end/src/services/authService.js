// Serviço de autenticação
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

/**
 * Faz login e retorna o token
 */
export async function login(username, password) {
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
                throw new Error("Credenciais inválidas");
            }
            throw new Error(`Erro ao fazer login: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Salva o token no localStorage
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("username", username);
        
        return data.access_token;
    } catch (error) {
        console.error("Erro ao fazer login:", error);
        throw error;
    }
}

/**
 * Registra um novo usuário
 */
export async function register(username, password) {
    try {
        const response = await fetch(`${BACKEND_URL}/users/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username,
                password,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 400) {
                throw new Error(errorData.detail || "Usuário já existe");
            }
            throw new Error(`Erro ao registrar: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Erro ao registrar:", error);
        throw error;
    }
}

/**
 * Faz logout
 */
export function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("username");
}

/**
 * Verifica se o usuário está autenticado
 */
export function isAuthenticated() {
    return !!localStorage.getItem("access_token");
}

/**
 * Obtém o token armazenado
 */
export function getToken() {
    return localStorage.getItem("access_token");
}

/**
 * Obtém o username armazenado
 */
export function getUsername() {
    return localStorage.getItem("username");
}
