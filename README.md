# dash-noc

Dashboard NOC local para mostrar en una tablet Lenovo Tab 8 informacion operativa del homelab.

El dashboard se servira desde Proxmox, pero no formara parte de la interfaz nativa de Proxmox. La vista `thermals` existente queda como fuente de datos y referencia visual, no como alcance completo del nuevo proyecto.

## Objetivo

Crear una pantalla fija, legible y util para supervision diaria:

- reloj grande en tiempo real
- estado basico de Proxmox
- estado de la maquina de trabajo `JM22W11`
- listado filtrado de emails y notificaciones importantes
- alertas visibles sin interaccion

## Documentacion

- [Overview](docs/overview.md)
- [Planning](docs/planning.md)
- [Tasks](docs/tasks.md)
- [API contracts](docs/api-contracts.md)
- [ADRs](docs/adr/)
- [Design previews](docs/design/previews/)

## Desarrollo local

Arrancar la API central mock:

```bash
PYTHONPATH=src scripts/run_api.py
```

Por defecto escucha en `127.0.0.1:8124`.

Variables utiles:

- `DASH_NOC_BIND`: bind HTTP. Por defecto `127.0.0.1`.
- `DASH_NOC_PORT`: puerto HTTP. Por defecto `8124`.
- `DASH_NOC_FRONTEND_HTML`: HTML servido en `/`. Por defecto `docs/design/previews/tablet-noc.html`.
- `DASH_NOC_PROXMOX_CURRENT_JSON`: snapshot local de `proxmox-thermals`. Por defecto `/projects/proxmox-thermals/data/current.json`.
- `DASH_NOC_PROXMOX_MAX_AGE`: edad maxima del snapshot Proxmox antes de refrescar. Por defecto `30`.
- `DASH_NOC_PROXMOX_REFRESH`: `1` refresca con el collector, `0` solo lee el JSON existente. Por defecto `1`.
- `DASH_NOC_PROXMOX_COLLECT_SCRIPT`: script collector. Por defecto `/projects/proxmox-thermals/scripts/collect_once.py`.

Endpoints iniciales:

- `GET /`
- `GET /health`
- `GET /api/noc/current`
- `GET /api/proxmox/status`
- `GET /api/jm22w11/status`
- `GET /api/notifications/important`

## Principio de organizacion

- `.ai/`: memoria para agentes IA.
- `docs/`: documentacion del proyecto.
- `docs/adr/`: decisiones de arquitectura.
- `docs/tasks/` o `docs/tasks.md`: seguimiento de trabajo.
