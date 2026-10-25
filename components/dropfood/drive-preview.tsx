import * as React from "react";
import "./tokens.css";
import "./drive-preview.css";
import { BrowserSession, type SessionState } from "./browser-session";

export interface DrivePreviewProps extends React.HTMLAttributes<HTMLDivElement> {
  /** URL atual do pane */
  url?: string;
  loading?: boolean;
  session?: SessionState;
  onBack?: () => void;
  onReload?: () => void;
  onOpenPortal?: () => void;
}

/* barra de navegação do navegador central — wrapper do preview-pane nativo.
   Comporta o chip browser-session (D9: na barra do navegador). */
export function DrivePreview({
  url = "portal.ifood.com.br/mercado",
  loading = false,
  session = "active",
  onBack, onReload, onOpenPortal,
  className = "", ...props
}: DrivePreviewProps) {
  return (
    <div className={`df-drive ${className}`.trim()} {...props}>
      <button type="button" className="df-drive__btn" onClick={onBack} title="voltar">←</button>
      <button type="button" className="df-drive__btn" onClick={onReload} title="recarregar">↻</button>
      <span className={`df-drive__url ${loading ? "df-drive__url--loading" : ""}`} title={url}>{url}</span>
      <BrowserSession state={session} onClick={onOpenPortal} />
    </div>
  );
}
