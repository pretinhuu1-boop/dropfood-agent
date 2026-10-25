import * as React from "react";
import "./tokens.css";
import "./browser-session.css";

export type SessionState = "active" | "otp" | "broken";

export interface BrowserSessionProps extends React.HTMLAttributes<HTMLButtonElement> {
  state?: SessionState;
  onClick?: () => void;
}

const LABEL: Record<SessionState, string> = {
  active: "portal ativo",
  otp: "OTP pendente",
  broken: "sessão quebrou",
};
const TITLE: Record<SessionState, string> = {
  active: "Sessão do portal iFood ativa (login manual do dono, 1x)",
  otp: "Re-OTP manual do dono necessário",
  broken: "Sessão quebrada — relogue manualmente",
};

/* chip de estado da sessão do portal — vive na barra do navegador (D9).
   Três estados: ativa/OTP/quebrada. Login SEMPRE manual do dono. */
export function BrowserSession({ state = "active", onClick, className = "", ...props }: BrowserSessionProps) {
  return (
    <button
      type="button"
      className={`df-browser-session df-browser-session--${state} ${className}`.trim()}
      title={TITLE[state]}
      onClick={onClick}
      {...props}
    >
      <span className="df-browser-session__dot" />
      {LABEL[state]}
    </button>
  );
}
