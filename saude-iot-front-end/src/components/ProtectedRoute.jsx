import { Navigate } from "react-router-dom";
import { isAuthenticated } from "@/services/authService";

/**
 * Componente que protege rotas privadas
 * Redireciona para login se não autenticado
 */
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
