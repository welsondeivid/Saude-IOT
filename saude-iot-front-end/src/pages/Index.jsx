import React, { useState } from "react";
import { mockEnvironmentalData } from "@/data/mock-data";
import { KPICard } from "@/components/KPICard";
import { ClimaSection } from "@/components/ClimaSection";
import { QualidadeArSection } from "@/components/QualidadeArSection";
import { QualidadeAguaSection } from "@/components/QualidadeAguaSection";
import { RiscosPanel } from "@/components/RiscosPanel";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Thermometer, Droplets, Wind, Activity, MapPin } from "lucide-react";

const Index = () => {
  const [bairroAtual, setBairroAtual] = useState("Cleto Marques");
  const dataFixa = "2025-10-27";
  const dadosBairro = mockEnvironmentalData.bairros[bairroAtual]?.[dataFixa];

  if (!dadosBairro) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-foreground">Dados não disponíveis</h1>
          <p className="text-muted-foreground mt-2">Não há dados para o bairro e data selecionados.</p>
        </div>
      </div>
    );
  }

  const totalRiscos =
    dadosBairro.riscos.clima.length +
    dadosBairro.riscos.qualidade_do_ar.length +
    dadosBairro.riscos.qualidade_da_agua.length;

  const statusVariant = totalRiscos === 0 ? "success" : totalRiscos <= 2 ? "warning" : "danger";

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-gradient-card border-b border-border shadow-md">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-1">Dashboard de Predição Ambiental</h1>
              <p className="text-muted-foreground flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                Dados de 27 de Outubro de 2025
              </p>
            </div>
            <div className="w-full md:w-64">
              <Select value={bairroAtual} onValueChange={(value) => setBairroAtual(value)}>
                <SelectTrigger className="bg-card shadow-sm">
                  <SelectValue placeholder="Selecione um bairro" />
                </SelectTrigger>
                <SelectContent className="bg-card">
                  <SelectItem value="Cleto Marques">Cleto Marques</SelectItem>
                  <SelectItem value="São Jorge">São Jorge</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPICard
            title="Temperatura"
            value={dadosBairro.clima.temperatura_ar.toFixed(1)}
            unit="°C"
            icon={Thermometer}
            variant="info"
          />
          <KPICard
            title="Umidade"
            value={dadosBairro.clima.umidade_relativa.toFixed(1)}
            unit="%"
            icon={Droplets}
            variant="info"
          />
          <KPICard
            title="Qualidade do Ar"
            value={dadosBairro.qualidade_do_ar.material_particulado_pm25.toFixed(1)}
            unit="µg/m³"
            icon={Wind}
            variant={
              dadosBairro.qualidade_do_ar.material_particulado_pm25 > 25
                ? "danger"
                : dadosBairro.qualidade_do_ar.material_particulado_pm25 > 17.5
                ? "warning"
                : "success"
            }
          />
          <KPICard
            title="Status Geral"
            value={totalRiscos === 0 ? "Normal" : totalRiscos <= 2 ? "Atenção" : "Crítico"}
            icon={Activity}
            variant={statusVariant}
          />
        </div>

        <RiscosPanel riscos={dadosBairro.riscos} />
        <ClimaSection data={dadosBairro.clima} />
        <QualidadeArSection data={dadosBairro.qualidade_do_ar} />
        <QualidadeAguaSection data={dadosBairro.qualidade_da_agua} />
      </main>

      <footer className="bg-gradient-card border-t border-border mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-muted-foreground">
          <p className="text-sm">Dashboard de Monitoramento Ambiental • Última atualização: 27/10/2025</p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
