import * as React from "react";
import "./tokens.css";
import "./bot-avatar.css";
import type { BotId } from "./activity-dot";

export interface BotAvatarProps extends React.HTMLAttributes<HTMLSpanElement> {
  bot: BotId;
  size?: "sm" | "md" | "lg";
}

const INITIAL: Record<BotId, string> = {
  b1: "B1", b2: "B2", b6: "B6", b7: "B7", bt: "BT", op: "OP",
};

/* avatar de bot: quadrado neobrutal com a cor canônica do bot + iniciais.
   Contraste: a cor é fundo, as iniciais são ink (AA sobre pink/mint/etc.). */
export function BotAvatar({ bot, size = "md", className = "", ...props }: BotAvatarProps) {
  return (
    <span className={`df-bot-avatar df-bot-avatar--${bot} ${size !== "md" ? `df-bot-avatar--${size}` : ""} ${className}`.trim()} {...props}>
      {INITIAL[bot]}
    </span>
  );
}
