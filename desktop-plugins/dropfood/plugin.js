/**
 * DROPFOOD Agent — runtime desktop plugin (D4: camada do produto, zero patch
 * no core). Carregado de $HERMES_HOME/desktop-plugins/dropfood/plugin.js.
 *
 * v1: chip de operação na status bar (portal ativo / OTP pendente / sem
 * sessão) + página de configuração (estado do portal, sobre). As panes de
 * radar/espelho entram em v2 pela mesma porta.
 *
 * Formato: ESM puro com jsx()/jsxs() — contrato de settings verificado no
 * hello-runtime do core (ListRow/SegmentedControl/ToggleRow do SDK).
 */

import { atom, cn, host, ListRow, SegmentedControl, Tip, ToggleRow, useValue } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'dropfood'

const PORTAL_STATES = {
  active: { label: 'portal ativo', color: 'bg-(--df-secondary)' },
  otp: { label: 'OTP pendente', color: 'bg-(--df-warn)' },
  broken: { label: 'sem sessão', color: 'bg-(--df-tertiary)' },
  unknown: { label: 'DROPFOOD', color: 'bg-(--df-primary)' },
  manual: { label: 'login manual', color: 'bg-(--df-primary)' }
}

function OpChip({ prefs }) {
  const { showChip, state } = useValue(prefs)
  if (!showChip) return null
  const s = PORTAL_STATES[state] ?? PORTAL_STATES.unknown
  return jsx(Tip, {
    label: 'DROPFOOD — ' + s.label + '. Portal iFood: login manual do dono (1x); o DROPFOOD nunca pede senha.',
    children: jsxs('span', {
      className: cn(
        'inline-flex h-full items-center gap-1.5 px-1.5 text-[0.6875rem] font-semibold',
        'text-(--ui-text-tertiary)'
      ),
      children: [
        jsx('span', {
          'aria-hidden': true,
          className: cn('inline-block size-2 rounded-[2px] border border-(--ui-border)', s.color)
        }),
        jsx('span', { children: s.label })
      ]
    })
  })
}

export default {
  id: ID,
  name: 'DROPFOOD',
  register(ctx) {
    const prefs = atom({ showChip: true, state: 'manual', ...ctx.storage.get('prefs', {}) })

    const update = patch => {
      prefs.set({ ...prefs.get(), ...patch })
      ctx.storage.set('prefs', prefs.get())
    }

    ctx.register({
      id: 'op-chip',
      area: 'statusBar.right',
      order: 90,
      render: () => jsx(OpChip, { prefs })
    })

    ctx.registerSettingsPage?.({
      id: 'settings',
      title: 'DROPFOOD',
      icon: 'package',
      render: function General() {
        const { showChip } = useValue(prefs)
        return jsx(ToggleRow, {
          checked: showChip,
          description: 'Chip de operação no canto direito da barra de status.',
          label: 'Mostrar chip da operação',
          onChange: on => update({ showChip: on })
        })
      },
      children: [
        {
          id: 'portal',
          title: 'Portal',
          render: function Portal() {
            const { state } = useValue(prefs)
            return jsx(ListRow, {
              action: jsx(SegmentedControl, {
                onChange: value => update({ state: value }),
                options: [
                  { id: 'manual', label: 'manual' },
                  { id: 'active', label: 'ativo' },
                  { id: 'otp', label: 'OTP' },
                  { id: 'broken', label: 'caiu' }
                ],
                value: state
              }),
              description: 'Login manual do dono (1x). ' + (PORTAL_STATES[state]?.label ?? ''),
              title: 'Estado do portal'
            })
          }
        },
        {
          id: 'about',
          title: 'Sobre',
          render: function About() {
            const gateway = useValue(host.state.gateway)
            return jsxs('div', {
              children: [
                jsx(ListRow, {
                  description: 'Camada do produto DROPFOOD Agent sobre o Hermes (core pinado, MIT).',
                  title: 'DROPFOOD'
                }),
                jsx(ListRow, {
                  action: jsx('span', {
                    className: 'text-[length:var(--conversation-caption-font-size)] text-(--ui-text-secondary)',
                    children: String(gateway)
                  }),
                  description: 'Estado da conexão do host (via plugin SDK).',
                  title: 'Gateway'
                })
              ]
            })
          }
        }
      ]
    })
  }
}
