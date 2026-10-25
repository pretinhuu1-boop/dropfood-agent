import * as React from "react";
import "./tokens.css";
import "./bot-chat-badge.css";

export interface BotChatBadgeProps extends React.HTMLAttributes<HTMLButtonElement> {
  /** quantos bots estão em conversa não aberta */
  count?: number;
  onClick?: () => void;
}

/* badge "N bots conversando" — visível sem abrir o modal (D2). Clique = abre. */
export function BotChatBadge({ count = 2, onClick, className = "", ...props }: BotChatBadgeProps) {
  return (
    <button
      type="button"
      className={`df-bot-chat-badge ${className}`.trim()}
      onClick={onClick}
      title={`${count} bots conversando — abrir`}
      {...props}
    >
      <span className={count > 1 ? "df-bot-chat-badge__dot--x2" : "df-bot-chat-badge__dot"} />
      {count} bots conversando
    </button>
  );
}
