import * as React from "react";
import "./tokens.css";
import "./step-progress.css";

export interface StepProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  total: number;
  done: number;
  /** true = o passo ATUAL pisca pink (está rodando agora) */
  live?: boolean;
  label?: string;
}

/* progresso neobrutal em passos: feito = ink, atual = pink piscando,
   futuro = vazio. Nunca uma barra — passos são discretos. */
export function StepProgress({ total, done, live = false, label, className = "", ...props }: StepProgressProps) {
  const squares = Array.from({ length: Math.max(0, total) }, (_, i) => (
    <span
      key={i}
      className={
        i < done ? "df-steps__sq df-steps__sq--done" :
        i === done && live ? "df-steps__sq df-steps__sq--live" :
        "df-steps__sq"
      }
    />
  ));
  return (
    <div className={`df-steps ${className}`.trim()} role="progressbar" aria-valuemin={0} aria-valuemax={total} aria-valuenow={done} {...props}>
      {squares}
      {label && <span className="df-steps__label">{label}</span>}
    </div>
  );
}
