import * as React from "react";
import "./tokens.css";
import "./bot-avatar.css";
import "./bot-chat-open.css";
import { BotAvatar } from "./bot-avatar";
import type { BotId } from "./activity-dot";

export interface BotChatOpenProps extends React.HTMLAttributes<HTMLButtonElement> {
  /** bots participantes da conversa (2) */
  bots: [BotId, BotId];
  /** abrir o modal de conversa (D2: por clique, nunca automático) */
  onOpen?: () => void;
  label?: string;
}

/* chip de abertura do modal de conversa entre bots — avatares sobrepostos
   + "conversa bX ⇄ bY". Aparece junto da mensagem inter-bot no thread. */
export function BotChatOpen({ bots, onOpen, label, className = "", ...props }: BotChatOpenProps) {
  const [a, b] = bots;
  return (
    <button
      type="button"
      className={`df-bot-chat-open ${className}`.trim()}
      onClick={onOpen}
      title={label ?? "Abrir conversa entre bots"}
      {...props}
    >
      <span className="df-bot-chat-open__avs">
        <BotAvatar bot={a} size="sm" />
        <BotAvatar bot={b} size="sm" />
      </span>
      <span className="df-bot-chat-open__arrow">⇄</span>
      conversa {a.toUpperCase()} ⇄ {b.toUpperCase()}
    </button>
  );
}
