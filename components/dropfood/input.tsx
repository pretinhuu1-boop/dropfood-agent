import * as React from "react";
import "./tokens.css";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  invalid?: boolean;
}

export function Input({ invalid = false, className = "", ...props }: InputProps) {
  return (
    <input
      aria-invalid={invalid || undefined}
      className={`df-input ${invalid ? "df-input--invalid" : ""} ${className}`.trim()}
      {...props}
    />
  );
}
