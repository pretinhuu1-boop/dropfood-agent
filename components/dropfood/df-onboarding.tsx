import * as React from "react";
import "./tokens.css";
import "./df-onboarding.css";

export interface OnboardingStep {
  /** 1..n */
  n: number;
  title: string;
  detail?: string;
  /** done = mint · now = canary · else paper */
  state?: "done" | "now" | "todo";
}

export interface DfOnboardingProps extends React.HTMLAttributes<HTMLDivElement> {
  logoUrl?: string;
  title?: string;
  subtitle?: string;
  steps?: OnboardingStep[];
  actionLabel?: string;
  onAction?: () => void;
  foot?: string;
}

/* tela de entrada DROPFOOD (F1): logo + passos para conectar a loja.
   Login do portal = manual do dono (regra de ouro) — o passo "entrar" abre
   o portal, nunca pede senha. */
export function DfOnboarding({
  logoUrl = "assets/logo-dropfood.svg",
  title = "DROPFOOD Agent",
  subtitle = "Conecte a sua loja do iFood Mercado e comece a operar com o seu time de bots.",
  steps = [
    { n: 1, title: "Rode o install.sh", detail: "A camada do produto é copiada para ~/.hermes", state: "done" as const },
    { n: 2, title: "Wizard da loja", detail: "python3 wizard.py — nome, modelo, fornecedor, markup", state: "now" as const },
    { n: 3, title: "Login manual no portal", detail: "1x, pelo dono — o DROPFOOD nunca pede senha", state: "todo" as const },
  ],
  actionLabel = "Começar operação",
  onAction,
  foot = "fork do Hermes · core pinado · MIT",
  className = "", ...props
}: DfOnboardingProps) {
  return (
    <div className={`df-onboarding ${className}`.trim()} {...props}>
      {logoUrl && <img className="df-onboarding__logo" src={logoUrl} alt="DROPFOOD" />}
      <h1 className="df-onboarding__title">{title}</h1>
      {subtitle && <p className="df-onboarding__sub">{subtitle}</p>}
      {steps.length > 0 && (
        <div className="df-onboarding__steps">
          {steps.map(s => (
            <div key={s.n} className={`df-onboarding__step df-onboarding__step--${s.state ?? "todo"}`}>
              <span className={`df-onboarding__stepb ${s.state === "done" ? "df-onboarding__stepb--done" : s.state === "now" ? "df-onboarding__stepb--now" : ""}`}>
                {s.state === "done" ? "✓" : s.n}
              </span>
              <div className="df-onboarding__stept">
                {s.title}
                {s.detail && <small>{s.detail}</small>}
              </div>
            </div>
          ))}
        </div>
      )}
      {actionLabel && (
        <button type="button" className="df-onboarding__action" onClick={onAction}>
          {actionLabel}
        </button>
      )}
      {foot && <div className="df-onboarding__foot">{foot}</div>}
    </div>
  );
}
