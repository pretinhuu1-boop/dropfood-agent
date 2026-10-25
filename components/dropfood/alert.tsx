import * as React from "react";
import "./tokens.css";

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  tone?: "info" | "warn" | "bad" | "ok";
}

/* alerta com borda dura — feedback de operação (preço, ban, erro) */
export function Alert({ tone = "info", className = "", children, ...props }: AlertProps) {
  return (
    <div role="alert" className={`df-alert df-alert--${tone} ${className}`.trim()} {...props}>
      {children}
    </div>
  );
}
