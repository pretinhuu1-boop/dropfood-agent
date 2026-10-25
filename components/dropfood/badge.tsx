import * as React from "react";
import "./tokens.css";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: "primary" | "brand" | "warn" | "bad";
}

/* badge numerico (contador de tarefas, notificacoes) */
export function Badge({ tone = "primary", className = "", children, ...props }: BadgeProps) {
  return (
    <span className={`df-badge df-badge--${tone} ${className}`.trim()} {...props}>
      {children}
    </span>
  );
}
