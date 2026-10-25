# Biblioteca de componentes DROPFOOD

Componentes **neobrutal escritos do zero** sobre os tokens do
`components/dropfood/tokens.css` (cores oficiais do DESIGN-DROPFOOD).
Nenhum código é copiado de fontes de terceiros — as referências coletadas
(5 libs MIT + docs) vivem no HD externo em
`/Volumes/Arquivo_iMac/dropfood-pesquisa/componentes/` (MANIFESTO.md).

## Estrutura

```
components/
├── registry.json            # registro shadcn-compatível (gerado)
└── dropfood/                # fonte dos componentes
    ├── tokens.css           # 14 variáveis (café, amarelo, verde… sombra dura)
    ├── button.tsx/.css      # 5 variantes, deslocamento no hover/active
    ├── chip.tsx/.css        # estados ok/warn/bad/info com dot
    ├── input.tsx/.css       # aria-invalid, foco amarelo
    ├── alert.tsx/.css       # borda grossa por tom
    └── badge.tsx/.css       # contadores
```

## Adicionar componente (padrão do registro)

1. Escreva `components/dropfood/<nome>.tsx` + `.css` do zero, anotando a
   referência de padrão usada no MANIFESTO do HD (se derivado, atribua).
2. Rode: `python3 scripts/components/build_registry.py` → regenera
   `components/registry.json` (formato spec shadcn).
3. Commit + CI (sanitize audita a camada do produto).

## Instalar componente com o agente (MCP local)

O servidor `scripts/components/mcp_components.py` expõe:
- `list_components` / `search_components` — catálogo
- `get_component` — conteúdo
- `install_component(name, out_dir)` — grava os arquivos (somente sob ~/dev)

Registre no config (usa o python do runtime Hermes — mcp SDK 2.x):

```yaml
mcp_servers:
  dropfood_components:
    command: "<python do runtime>"
    args: ["<repo>/scripts/components/mcp_components.py"]
```

Reinicia o Hermes e as ferramentas aparecem como `mcp_dropfood_components_*`.
