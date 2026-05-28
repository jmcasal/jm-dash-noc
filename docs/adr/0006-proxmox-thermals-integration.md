# ADR 0006: Integracion con `proxmox-thermals` por contrato, no por copia completa

## Estado

Aceptada.

## Contexto

`dash-noc` necesita datos termicos y metricas Proxmox que ya existen en `/projects/proxmox-thermals`.

Copiar todo el proyecto historico dentro de `dash-noc` mezclaria alcances: `proxmox-thermals` monitoriza un host y `dash-noc` agrega estado NOC para tablet.

## Decision

Mantener `dash-noc` como proyecto limpio.

Para Proxmox, la primera integracion leera una de estas fuentes:

- `proxmox-thermals` `/api/current`, si el servicio esta activo.
- `/projects/proxmox-thermals/data/current.json`, si se decide integrar por fichero local.

`dash-noc` transformara esos datos al contrato propio documentado en `docs/api-contracts.md`.

## Consecuencias

- `proxmox-thermals` queda como fuente/adaptador, no como nucleo conceptual.
- La UI tablet no depende de la forma interna de `proxmox-thermals`.
- Los cambios futuros en sensores Proxmox solo deben tocar el adaptador.
- Se evita duplicar collector termico hasta que haya una razon concreta.
