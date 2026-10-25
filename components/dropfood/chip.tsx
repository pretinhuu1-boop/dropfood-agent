import * as React from "react";
import "./tokens.css";

export interface ChipProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: "ok" | "warn" | "bad" | "info";
  dot?: boolean;
}

/* chip de estado (preço ok, alerta, radar...) com dot de status */
export function Chip({ tone = "info", dot = false, className = "", children, ...props }: ChipProps) {
  return (
    <span className={`df-chip df-chip--${tone} ${className}`} {...props}>
      {dot && <span className="df-chip__dot" aria-hidden />}
      {children}
    </span>
  );
}
