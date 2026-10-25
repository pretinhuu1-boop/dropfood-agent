import * as React from "react";
import "./tokens.css";
import "./handoff-timeline.css";
import type { BotId } from "./activity-dot";

export interface HandoffStep {
  bot: BotId;
  title: string;
  detail?: string;
  time?: string;
}

export interface HandoffTimelineProps extends React.HTMLAttributes<HTMLDivElement> {
  steps: HandoffStep[];
}

/* linha do tempo dos gates: quem fez o quê e quando (b1 → b2 → b7…). */
export function HandoffTimeline({ steps, className = "", ...props }: HandoffTimelineProps) {
  return (
    <div className={`df-handoff ${className}`.trim()} {...props}>
      {steps.map((s, i) => (
        <div key={i} className="df-handoff__item">
          <span className={`df-handoff__dot df-handoff__dot--${s.bot}`} />
          <div className="df-handoff__body">
            <b>{s.title}</b>
            {s.detail && <p>{s.detail}</p>}
            {s.time && <span className="df-handoff__time">{s.time}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}
