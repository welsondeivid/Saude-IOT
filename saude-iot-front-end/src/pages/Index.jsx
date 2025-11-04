import React, { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { getRelatorioDiario } from "@/services/api";
import { logout, getUsername, isAuthenticated } from "@/services/authService";
import { KPICard } from "@/components/KPICard";
import { ClimaSection } from "@/components/ClimaSection";
import { QualidadeArSection } from "@/components/QualidadeArSection";
import { QualidadeAguaSection } from "@/components/QualidadeAguaSection";
import { RiscosPanel } from "@/components/RiscosPanel";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Thermometer, Droplets, Wind, Activity, MapPin, Loader2, AlertCircle, LogOut, User } from "lucide-react";
import { toast } from "@/lib/toast";

const Index = () => {
  const [bairroAtual, setBairroAtual] = useState(null);
  const [dataSelecionada, setDataSelecionada] = useState(null);
  const navigate = useNavigate();
  const username = getUsername();
  const userLoggedIn = isAuthenticated();

  const handleLogout = () => {
    logout();
    toast.success("Logout realizado com sucesso!");
    navigate("/");
  };

  // Busca dados do relatório diário
  const { data: relatorioData, isLoading, error, refetch } = useQuery({
    queryKey: ["relatorio-diario"],
    queryFn: getRelatorioDiario,
    retry: 2,
    refetchInterval: 60000, // Atualiza a cada 60 segundos
  });

  // Extrai lista de bairros e datas disponíveis
  const bairrosDisponiveis = useMemo(() => {
    if (!relatorioData?.bairros) return [];
    return Object.keys(relatorioData.bairros);
  }, [relatorioData]);

  const datasDisponiveis = useMemo(() => {
    if (!relatorioData?.bairros || !bairroAtual) return [];
    const bairro = relatorioData.bairros[bairroAtual];
    if (!bairro) return [];
    return Object.keys(bairro).sort().reverse(); // Mais recente primeiro
  }, [relatorioData, bairroAtual]);

  // Atualiza bairro selecionado quando os dados carregam
  React.useEffect(() => {
    if (bairrosDisponiveis.length > 0 && !bairroAtual) {
      setBairroAtual(bairrosDisponiveis[0]);
    }
  }, [bairrosDisponiveis, bairroAtual]);

  // Atualiza data selecionada quando o bairro muda ou dados carregam
  React.useEffect(() => {
    if (datasDisponiveis.length > 0 && (!dataSelecionada || !datasDisponiveis.includes(dataSelecionada))) {
      setDataSelecionada(datasDisponiveis[0]);
    }
  }, [datasDisponiveis, dataSelecionada]);

  const dadosBairro = useMemo(() => {
    if (!relatorioData?.bairros || !bairroAtual || !dataSelecionada) return null;
    return relatorioData.bairros[bairroAtual]?.[dataSelecionada];
  }, [relatorioData, bairroAtual, dataSelecionada]);

  // Formata data para exibição
  const formatarData = (dataStr) => {
    if (!dataStr) return "";
    const date = new Date(dataStr + "T00:00:00");
    return date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });
  };

  // Estados de loading e erro
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">Carregando dados...</h1>
          <p className="text-muted-foreground mt-2">Buscando informações do servidor</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center max-w-md">
          <AlertCircle className="h-8 w-8 mx-auto mb-4 text-destructive" />
          <h1 className="text-2xl font-bold text-foreground">Erro ao carregar dados</h1>
          <p className="text-muted-foreground mt-2">{error.message || "Não foi possível conectar ao servidor"}</p>
          <button
            onClick={() => refetch()}
            className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  if (!dadosBairro || bairrosDisponiveis.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-foreground">Dados não disponíveis</h1>
          <p className="text-muted-foreground mt-2">
            {bairrosDisponiveis.length === 0
              ? "Nenhum bairro encontrado no sistema."
              : "Não há dados para o bairro e data selecionados."}
          </p>
        </div>
      </div>
    );
  }

  const riscos = dadosBairro.riscos || { clima: [], qualidade_do_ar: [], qualidade_da_agua: [] };
  const totalRiscos =
    (riscos.clima?.length || 0) +
    (riscos.qualidade_do_ar?.length || 0) +
    (riscos.qualidade_da_agua?.length || 0);

  const statusVariant = totalRiscos === 0 ? "success" : totalRiscos <= 2 ? "warning" : "danger";

  // Valores com fallback para evitar erros
  const temperatura = dadosBairro.clima?.temperatura_ar ?? 0;
  const umidade = dadosBairro.clima?.umidade_relativa ?? 0;
  const pm25 = dadosBairro.qualidade_do_ar?.material_particulado_pm25 ?? 0;

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-gradient-card border-b border-border shadow-md">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-1">Dashboard de Predição Ambiental</h1>
              <p className="text-muted-foreground flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                {dataSelecionada ? `Dados de ${formatarData(dataSelecionada)}` : "Carregando..."}
              </p>
            </div>
            {userLoggedIn && (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <User className="h-4 w-4" />
                  <span>{username}</span>
                </div>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-2"
                >
                  <LogOut className="h-4 w-4" />
                  Sair
                </Button>
              </div>
            )}
          </div>
          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <div className="w-full sm:w-64">
                <Select value={bairroAtual || ""} onValueChange={(value) => setBairroAtual(value)}>
                  <SelectTrigger className="bg-card shadow-sm">
                    <SelectValue placeholder="Selecione um bairro" />
                  </SelectTrigger>
                  <SelectContent className="bg-card">
                    {bairrosDisponiveis.map((bairro) => (
                      <SelectItem key={bairro} value={bairro}>
                        {bairro}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              {datasDisponiveis.length > 1 && (
                <div className="w-full sm:w-48">
                  <Select value={dataSelecionada || ""} onValueChange={(value) => setDataSelecionada(value)}>
                    <SelectTrigger className="bg-card shadow-sm">
                      <SelectValue placeholder="Selecione uma data" />
                    </SelectTrigger>
                    <SelectContent className="bg-card">
                      {datasDisponiveis.map((data) => (
                        <SelectItem key={data} value={data}>
                          {formatarData(data)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}
            </div>
          </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPICard
            title="Temperatura"
            value={temperatura.toFixed(1)}
            unit="°C"
            icon={Thermometer}
            variant="info"
          />
          <KPICard
            title="Umidade"
            value={umidade.toFixed(1)}
            unit="%"
            icon={Droplets}
            variant="info"
          />
          <KPICard
            title="Qualidade do Ar"
            value={pm25.toFixed(1)}
            unit="µg/m³"
            icon={Wind}
            variant={pm25 > 25 ? "danger" : pm25 > 17.5 ? "warning" : "success"}
          />
          <KPICard
            title="Status Geral"
            value={totalRiscos === 0 ? "Normal" : totalRiscos <= 2 ? "Atenção" : "Crítico"}
            icon={Activity}
            variant={statusVariant}
          />
        </div>

        <RiscosPanel riscos={riscos} />
        {dadosBairro.clima && <ClimaSection data={dadosBairro.clima} />}
        {dadosBairro.qualidade_do_ar && <QualidadeArSection data={dadosBairro.qualidade_do_ar} />}
        {dadosBairro.qualidade_da_agua && <QualidadeAguaSection data={dadosBairro.qualidade_da_agua} />}
      </main>

      <footer className="bg-gradient-card border-t border-border mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-muted-foreground">
          <p className="text-sm">
            Dashboard de Monitoramento Ambiental • Última atualização: {new Date().toLocaleDateString("pt-BR")}
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
