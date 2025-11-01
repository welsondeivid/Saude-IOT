import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Droplet, AlertTriangle } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export const QualidadeAguaSection = ({ data }) => {
  if (!data) return null;

  // Normaliza campos para suportar mock antigo (ph) e novo (ph_agua)
  const phAgua = Number(data.ph_agua ?? data.ph ?? 0);
  const turbidez = Number(data.turbidez ?? 0);
  const cloroResidual = Number(data.cloro_residual ?? 0);
  const coliformesTotais = Number(data.coliformes_totais ?? 0);

  const chartData = [
    { name: "pH", pH: phAgua, turbidez: 0, cloro: 0 },
    { name: "Turbidez", pH: 0, turbidez: turbidez, cloro: 0 },
    { name: "Cloro", pH: 0, turbidez: 0, cloro: cloroResidual },
  ];

  const coliformesStatus =
    coliformesTotais > 200
      ? "danger"
      : coliformesTotais > 100
      ? "warning"
      : "success";
  const statusColors = {
    success: "bg-success text-success-foreground",
    warning: "bg-warning text-warning-foreground",
    danger: "bg-danger text-danger-foreground",
  };

  return (
    <div className="space-y-6">
      <Card className="bg-gradient-card shadow-lg">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Droplet className="h-5 w-5" />
            Qualidade da Água
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="w-full h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="hsl(var(--border))"
                />
                <XAxis
                  dataKey="name"
                  tick={{ fill: "hsl(var(--foreground))" }}
                />
                <YAxis tick={{ fill: "hsl(var(--muted-foreground))" }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "var(--radius)",
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="pH"
                  stroke="hsl(var(--info))"
                  strokeWidth={2}
                  name="pH"
                  dot={{ fill: "hsl(var(--info))", r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="turbidez"
                  stroke="hsl(var(--warning))"
                  strokeWidth={2}
                  name="Turbidez (NTU)"
                  dot={{ fill: "hsl(var(--warning))", r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="cloro"
                  stroke="hsl(var(--success))"
                  strokeWidth={2}
                  name="Cloro (mg/L)"
                  dot={{ fill: "hsl(var(--success))", r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 rounded-lg border border-border bg-card">
              <p className="text-sm text-muted-foreground mb-1">pH da Água</p>
              <p className="text-2xl font-bold">{phAgua.toFixed(2)}</p>
              <p className="text-xs text-muted-foreground mt-1">
                Ideal: 6.5 - 8.5
              </p>
            </div>

            <div className="p-4 rounded-lg border border-border bg-card">
              <p className="text-sm text-muted-foreground mb-1">Turbidez</p>
              <p className="text-2xl font-bold">
                {turbidez.toFixed(2)} <span className="text-sm">NTU</span>
              </p>
              <p className="text-xs text-muted-foreground mt-1">Máx: 5 NTU</p>
            </div>

            <div className="p-4 rounded-lg border border-border bg-card">
              <p className="text-sm text-muted-foreground mb-1">
                Cloro Residual
              </p>
              <p className="text-2xl font-bold">
                {cloroResidual.toFixed(2)} <span className="text-sm">mg/L</span>
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Ideal: 0.2 - 2.0 mg/L
              </p>
            </div>

            <div className={`p-4 rounded-lg ${statusColors[coliformesStatus]}`}>
              <div className="flex items-center gap-2 mb-1">
                <p className="text-sm font-medium">Coliformes Totais</p>
                {coliformesStatus !== "success" && (
                  <AlertTriangle className="h-4 w-4" />
                )}
              </div>
              <p className="text-2xl font-bold">
                {coliformesTotais} <span className="text-sm">UFC/100mL</span>
              </p>
              <p className="text-xs mt-1 opacity-90">Máx: 200 UFC/100mL</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
