fecha y hora

- 2026-05-28 18:56 CEST

objetivo de la sesion

- iniciar el cambio de alcance desde `proxmox-thermals` hacia `dash-noc`

acciones realizadas

- se acepta `dash-noc` como nombre del proyecto
- se crea documentacion base en `docs/`
- se crean ADRs iniciales
- se crea backlog inicial de tareas
- se deja memoria IA especifica en `.ai/dash-noc.md`

archivos creados

- `README.md`
- `docs/overview.md`
- `docs/planning.md`
- `docs/tasks.md`
- `docs/adr/0001-project-scope.md`
- `docs/adr/0002-proxmox-serves-dashboard.md`
- `docs/adr/0003-agent-services-for-remote-data.md`
- `docs/adr/0004-tablet-first-layout.md`
- `.ai/dash-noc.md`
- `.ai/history/260528-1856-dash-noc-bootstrap.md`

decisiones

- `dash-noc` es proyecto separado conceptualmente de `proxmox-thermals`
- Proxmox servira el dashboard, pero fuera de la UI nativa de Proxmox
- `JM22W11` deberia exponer datos mediante servicios/agentes propios
- la vista debe disenarse primero para Lenovo Tab 8

siguiente paso

- definir resolucion/orientacion de la tablet
- crear preview `tablet-noc` basada en `03-noc.html`
