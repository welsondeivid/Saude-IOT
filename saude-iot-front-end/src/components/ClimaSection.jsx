import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Cloud, Droplets, Leaf, Thermometer } from "lucide-react";
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Tooltip } from "recharts";

export const ClimaSection = ({ data }) => {
  if (!data) return null;

  // Fallbacks caso valores não existam
  const coberturaVegetal = Number(data.cobertura_vegetal ?? 0);
  const precipitacao = Number(data.precipitacao ?? 0);
  const temperatura = Number(data.temperatura_ar ?? 0);
  const umidade = Number(data.umidade_relativa ?? 0);

  const radarData = [
    { subject: "Cobertura Vegetal", value: coberturaVegetal, fullMark: 100 },
    { subject: "Precipitação", value: precipitacao * 5, fullMark: 100 }, // escala simples
    { subject: "Temperatura", value: temperatura * 2.5, fullMark: 100 }, // escala simples
    { subject: "Umidade", value: umidade, fullMark: 100 },
  ];

  const climaItems = [
    { icon: Leaf, label: "Cobertura Vegetal", value: coberturaVegetal, unit: "%" },
    { icon: Droplets, label: "Precipitação", value: precipitacao, unit: "mm" },
    { icon: Thermometer, label: "Temperatura", value: temperatura, unit: "°C" },
    { icon: Cloud, label: "Umidade", value: umidade, unit: "%" },
  ];

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-card shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cloud className="h-5 w-5" />
            Condições Climáticas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="w-full h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData} outerRadius={110}>
                <PolarGrid stroke="hsl(var(--border))" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "hsl(var(--foreground))", fontSize: 12 }} />
                <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }} />
                <Radar
                  name="Valores"
                  dataKey="value"
                  stroke="hsl(var(--primary))"
                  fill="hsl(var(--primary))"
                  fillOpacity={0.5}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                    fontSize: 12,
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {climaItems.map(({ icon: Icon, label, value, unit }) => (
          <Card key={label} className="bg-gradient-card shadow-md hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="p-3 rounded-lg bg-primary/10">
                  <Icon className="h-6 w-6 text-primary" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">{label}</p>
                  <p className="text-2xl font-bold">
                    {Number(value).toFixed(2)}
                    <span className="text-sm ml-1">{unit}</span>
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
