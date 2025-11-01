import React from "react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export const KPICard = ({
  title,
  value,
  unit,
  icon: Icon,
  variant = "info",
}) => {
  const variantStyles = {
    success: "bg-gradient-success text-success-foreground",
    warning: "bg-gradient-warning text-warning-foreground",
    danger: "bg-gradient-danger text-danger-foreground",
    info: "bg-gradient-info text-info-foreground",
  };

  return (
    <Card className="overflow-hidden transition-all duration-300 hover:shadow-lg hover:scale-105">
      <div className={cn("p-6", variantStyles[variant])}>
        <div className="flex items-center justify-between mb-2">
          {Icon && <Icon className="h-8 w-8 opacity-90" />}
        </div>
        <div className="space-y-1">
          <p className="text-sm font-medium opacity-90">{title}</p>
          <p className="text-3xl font-bold">
            {value}
            {unit && <span className="text-lg ml-1">{unit}</span>}
          </p>
        </div>
      </div>
    </Card>
  );
};
