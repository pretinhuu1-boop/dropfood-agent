import * as React from "react";
import "./tokens.css";
import "./activity-dot.css";

export type BotId = "b1" | "b2" | "b6" | "b7" | "bt" | "op";

export interface ActivityDotProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** qual bot está trabalhando (cor canônica D3) */
  bot?: BotId;
  /** true = animado (trabalhando); false/omit = parado */
  live?: boolean;
}

/* ponto de atividade do bot — quadrado ink que desloca 2px em steps enquanto
   trabalha; parado fica branco com borda (vazio). */
export function ActivityDot({ bot, live = false, className = "", ...props }: ActivityDotProps) {
  const cls = [
    "df-activity-dot",
    bot ? `df-activity-dot--${bot}` : "",
    live ? "df-activity-dot--live" : "df-activity-dot--idle",
    className,
  ].filter(Boolean).join(" ");
  return <span aria-label={live ? "trabalhando" : "ocioso"} className={cls} {...props} />;
}
