import * as React from "react";
import "./tokens.css";
import "./activity-dot.css";
import "./activity-strip.css";
import { ActivityDot, type BotId } from "./activity-dot";

export interface ActivityStripProps extends React.HTMLAttributes<HTMLDivElement> {
  /** bot trabalhando — dita cor e rótulo (D3) */
  bot: BotId;
  /** verbo vivo: "escaneando concorrentes…" */
  verb?: string;
  /** conteúdo rolável — o ticker nativo do Hermes passa aqui */
  children?: React.ReactNode;
}

const WHO: Record<BotId, string> = {
  b1: "b1 estrategista",
  b2: "b2 radar",
  b6: "b6 revisor",
  b7: "b7 controle",
  bt: "bt treinador",
  op: "operador",
};

/* faixa 1-linha de atividade por bot: dot animado + quem + verbo + conteúdo
   (ticker). Onde o run-ticker do Hermes é wrapper para dar identidade. */
export function ActivityStrip({ bot, verb, children, className = "", ...props }: ActivityStripProps) {
  return (
    <div className={`df-activity-strip df-activity-strip--${bot} ${className}`.trim()} {...props}>
      <ActivityDot bot={bot} live />
      <span className="df-activity-strip__who">{WHO[bot]}</span>
      {verb && <span className="df-activity-strip__verb">{verb}</span>}
      <span className="df-activity-strip__inner">{children}</span>
    </div>
  );
}
