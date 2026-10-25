import * as React from "react";
import "./tokens.css";
import "./working-card.css";
import "./activity-dot.css";
import { ActivityDot, type BotId } from "./activity-dot";
import { StepProgress } from "./step-progress";

export interface WorkingCardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** bot que está trabalhando (cor e rótulo D3) */
  bot: BotId;
  title: string;
  stepsDone?: number;
  stepsTotal?: number;
  meta?: string;      // ex.: "3 de 7 concorrentes"
  duration?: string;  // ex.: "12s"
  children?: React.ReactNode;
}

/* card expandido de trabalho: quem, o quê, progresso em passos e foot com
   duração. Base do modo expandido da atividade (working-card do mapa). */
export function WorkingCard({
  bot, title, stepsDone = 0, stepsTotal = 0, meta, duration,
  children, className = "", ...props
}: WorkingCardProps) {
  return (
    <div className={`df-working-card ${className}`.trim()} {...props}>
      <div className="df-working-card__head">
        <ActivityDot bot={bot} live />
        <span className="df-working-card__title">{title}</span>
        {meta && <span className="df-working-card__meta">{meta}</span>}
      </div>
      {stepsTotal > 0 && (
        <StepProgress total={stepsTotal} done={stepsDone} live label={duration} />
      )}
      {children && <div className="df-working-card__body">{children}</div>}
      {duration && !stepsTotal && (
        <div className="df-working-card__foot">{duration}</div>
      )}
    </div>
  );
}
