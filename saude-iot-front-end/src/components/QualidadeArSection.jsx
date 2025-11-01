import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Wind } from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Cell,
} from "recharts";

export const QualidadeArSection = ({ data }) => {
  if (!data) return null;

  const pm25 = Number(data.material_particulado_pm25 ?? 0);
  // Suporte a campo legado `co` ou novo `monoxido_carbono`
  const monoxidoCarbono = Number(data.monoxido_carbono ?? data.co ?? 0);

  const chartData = [
    {
      name: "PM2.5",
      value: pm25,
      limite: 25, // OMS
      unit: "µg/m³",
    },
    {
      name: "Monóxido de Carbono",
      value: monoxidoCarbono,
      limite: 9, // OMS
      unit: "ppm",
    },
  ];

  const getColor = (value, limite) => {
    if (value > limite) return "hsl(var(--danger))";
    if (value > limite * 0.7) return "hsl(var(--warning))";
    return "hsl(var(--success))";
  };

  return (
    <Card className="bg-gradient-card shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Wind className="h-5 w-5" />
          Qualidade do Ar
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="w-full h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="hsl(var(--border))"
              />
              <XAxis dataKey="name" tick={{ fill: "hsl(var(--foreground))" }} />
              <YAxis tick={{ fill: "hsl(var(--muted-foreground))" }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "var(--radius)",
                }}
                formatter={(value, _name, props) => [
                  `${value} ${props.payload.unit}`,
                  "Medição",
                ]}
              />
              <Legend />
              <Bar dataKey="value" name="Medição" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={getColor(entry.value, entry.limite)}
                  />
                ))}
              </Bar>
              <Bar
                dataKey="limite"
                name="Limite OMS"
                fill="hsl(var(--muted))"
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          {chartData.map((item) => {
            const status =
              item.value > item.limite
                ? "danger"
                : item.value > item.limite * 0.7
                ? "warning"
                : "success";
            const statusColors = {
              success: "bg-success/10 text-success border-success/20",
              warning: "bg-warning/10 text-warning border-warning/20",
              danger: "bg-danger/10 text-danger border-danger/20",
            };
            return (
              <div
                key={item.name}
                className={`p-4 rounded-lg border ${statusColors[status]}`}
              >
                <p className="text-sm font-medium mb-1">{item.name}</p>
                <p className="text-2xl font-bold">
                  {item.value} <span className="text-sm">{item.unit}</span>
                </p>
                <p className="text-xs mt-1 opacity-80">
                  Limite: {item.limite} {item.unit}
                </p>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
};
