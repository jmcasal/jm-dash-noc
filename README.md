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
- [ADRs](docs/adr/)
- [Design previews](docs/design/previews/)

## Principio de organizacion

- `.ai/`: memoria para agentes IA.
- `docs/`: documentacion del proyecto.
- `docs/adr/`: decisiones de arquitectura.
- `docs/tasks/` o `docs/tasks.md`: seguimiento de trabajo.

