import * as React from "react";
import "./tokens.css";
import "./bot-avatar.css";
import "./bot-chat-modal.css";
import { BotAvatar } from "./bot-avatar";
import type { BotId } from "./activity-dot";

export interface BotChatMessage {
  /** quem falou */
  bot: BotId;
  text: string;
  time?: string;
  /** pensando (lilac) vs entregue (canary) */
  tone?: "thinking" | "sent";
}

export interface BotChatModalProps extends React.HTMLAttributes<HTMLDivElement> {
  open: boolean;
  onClose: () => void;
  /** participantes, em ordem de coluna esquerda → direita */
  bots: [BotId, BotId];
  messages: BotChatMessage[];
  onOpenThread?: () => void;
}

const WHO: Record<BotId, string> = {
  b1: "estratégia", b2: "radar", b6: "revisão", b7: "controle", bt: "treinador", op: "operador",
};

/* modal de conversa entre bots (Zona C): corredor 2 colunas, cada bot com
   avatar/cor, mensagens em cronologia paralela. D2: abre por clique. */
export function BotChatModal({
  open, onClose, bots, messages, onOpenThread,
  className = "", ...props
}: BotChatModalProps) {
  if (!open) return null;
  const [left, right] = bots;
  const rows: Array<[typeof left | typeof right, number]> = [];
  for (let i = 0; i < messages.length; i++) {
    const m = messages[i];
    if (m.bot === left) rows.push([left, i]);
    if (m.bot === right) rows.push([right, i]);
  }
  return (
    <div className="df-bot-chat-overlay" role="dialog" aria-modal="true" aria-label={`Conversa ${left.toUpperCase()} ⇄ ${right.toUpperCase()}`} onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
      <div className={`df-bot-chat-modal ${className}`.trim()} {...props}>
        <div className="df-bot-chat-modal__titlebar">
          <b>Conversa entre bots</b>
          <button type="button" className="df-modal-close" onClick={onClose}>fechar ✕</button>
        </div>
        <div className="df-bot-chat-modal__participants">
          <span className="df-participant"><BotAvatar bot={left} size="sm" /> {left.toUpperCase()} · {WHO[left]}</span>
          <span className="df-participant__vs">⇄</span>
          <span className="df-participant"><BotAvatar bot={right} size="sm" /> {right.toUpperCase()} · {WHO[right]}</span>
        </div>
        <div className="df-bot-chat-modal__corridor">
          <div className="df-bot-chat-col">
            <div className="df-bot-chat-col__head">coluna {left.toUpperCase()}</div>
            {rows.filter(([b]) => b === left).map(([, i]) => {
              const m = messages[i];
              return (
                <div key={i} className={`df-bot-chat-msg ${m.tone ? `df-bot-chat-msg--${m.tone}` : ""}`}>
                  {m.text}
                  {m.time && <span className="df-bot-chat-msg__time">{m.time}</span>}
                </div>
              );
            })}
          </div>
          <div className="df-bot-chat-col">
            <div className="df-bot-chat-col__head">coluna {right.toUpperCase()}</div>
            {rows.filter(([b]) => b === right).map(([, i]) => {
              const m = messages[i];
              return (
                <div key={i} className={`df-bot-chat-msg ${m.tone ? `df-bot-chat-msg--${m.tone}` : ""}`}>
                  {m.text}
                  {m.time && <span className="df-bot-chat-msg__time">{m.time}</span>}
                </div>
              );
            })}
          </div>
        </div>
        <div className="df-bot-chat-modal__foot">
          <span className="df-foot-live">● ao vivo</span>
          <span>pipeline nativo: hermes -p bX chat -q "Message from…"</span>
          {onOpenThread && (
            <button type="button" className="df-modal-close" style={{ marginLeft: "auto", border: "2px solid var(--df-ink)", color: "var(--df-ink)", background: "var(--df-bg)" }} onClick={onOpenThread}>
              ver no thread ↗
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
