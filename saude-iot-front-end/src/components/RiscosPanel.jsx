import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Cloud, Wind, Droplet } from "lucide-react";

export const RiscosPanel = ({ riscos }) => {
  if (!riscos) return null;

  const totalRiscos =
    (riscos.clima?.length || 0) +
    (riscos.qualidade_do_ar?.length || 0) +
    (riscos.qualidade_da_agua?.length || 0);

  const riscosCategories = [
    {
      title: "Clima",
      icon: Cloud,
      items: riscos.clima || [],
      color: "bg-info text-info-foreground",
    },
    {
      title: "Qualidade do Ar",
      icon: Wind,
      items: riscos.qualidade_do_ar || [],
      color: "bg-warning text-warning-foreground",
    },
    {
      title: "Qualidade da Água",
      icon: Droplet,
      items: riscos.qualidade_da_agua || [],
      color: "bg-danger text-danger-foreground",
    },
  ];

  if (totalRiscos === 0) {
    return (
      <Card className="bg-gradient-success text-success-foreground shadow-lg">
        <CardContent className="flex align-center p-0">
          <div className="flex items-center gap-4 p-6">
            <div className="p-3 rounded-full bg-white/20">
              <AlertTriangle className="h-8 w-8" />
            </div>
            <div className="flex flex-col align-center">
              <h3 className="text-xl font-bold">Nenhum Risco Detectado</h3>
              <p className="text-sm opacity-90">
                Todos os parâmetros estão dentro dos limites seguros.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-gradient-card shadow-lg border-l-4 border-danger">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-danger">
          <AlertTriangle className="h-5 w-5" />
          Alertas e Riscos ({totalRiscos})
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {riscosCategories.map(({ title, icon: Icon, items, color }) =>
          items.length > 0 ? (
            <div key={title} className="space-y-2">
              <div className="flex items-center gap-2">
                <Icon className="h-4 w-4 text-muted-foreground" />
                <h4 className="font-semibold text-sm">{title}</h4>
                <Badge variant="outline" className="ml-auto">
                  {items.length}
                </Badge>
              </div>
              <div className="flex flex-wrap gap-2">
                {items.map((risco, index) => (
                  <Badge key={index} className={color}>
                    {risco}
                  </Badge>
                ))}
              </div>
            </div>
          ) : null
        )}
      </CardContent>
    </Card>
  );
};
