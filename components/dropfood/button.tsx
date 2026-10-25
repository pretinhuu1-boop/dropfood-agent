import * as React from "react";
import "./tokens.css";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "paper" | "primary" | "brand" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
}

/* neobrutal: borda 2px ink, sombra dura que "desloca" no hover/active */
export function Button({ variant = "paper", size = "md", className = "", ...props }: ButtonProps) {
  const base = [
    "df-btn",
    `df-btn--${variant}`,
    `df-btn--${size}`,
    className,
  ].join(" ");
  return <button className={base} {...props} />;
}
