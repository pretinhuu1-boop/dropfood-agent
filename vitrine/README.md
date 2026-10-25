# Vitrine web do DROPFOOD Agent (F6)

Landing estática, autossuficiente (HTML+CSS, zero build, zero framework).
Pode ser servida por qualquer static host (GitHub Pages, Netlify, S3) ou
aberta localmente.

## Como usar

```bash
# preview local
cd vitrine && python3 -m http.server 8080
# → http://localhost:8080
```

## Publicar (GitHub Pages)

1. Repo → Settings → Pages → Source: `main` / pasta `/vitrine`.
2. Ou via gh: `gh api repos/pretinhuu1-boop/dropfood-agent/pages -f source[branch]=main -f source[path]=/vitrine`.

## Conteúdo

- Hero: navegador central + vereditos do radar (mock Adega do Seu João).
- O que faz: 6 cards (radar, espelho, portal, bots, UI, MIT).
- Bots: b1/b2/b6/b7 com cores canônicas.
- Instalar: os 3 comandos + `--com-sdk` opcional.

## Regras

- Nada de dado real (mock fictício). Zero JavaScript. Mesma paleta/
  tipografia da canônica (design/DESIGN.md).
