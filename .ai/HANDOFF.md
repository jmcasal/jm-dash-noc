# HANDOFF: dash-noc

## Fecha

- 2026-05-28 19:12 CEST

## Motivo

Esta sesion de Codex se abrio originalmente con `cwd` en `/root/projects/proxmox-thermals`.

Durante la sesion el proyecto cambio de alcance y se movio el trabajo activo a:

- `/root/projects/dash-noc`

Para evitar que Codex siga registrando turnos contra el directorio antiguo, abrir una sesion nueva desde `/root/projects/dash-noc` y leer este archivo.

## Estado actual

Proyecto activo:

- `/root/projects/dash-noc`

Directorio historico conservado:

- `/root/projects/proxmox-thermals`

Implementacion historica real de termicas:

- `/projects/proxmox-thermals`

Config Codex actualizada:

- `~/.codex/config.toml` contiene trusted para:
  - `/root/projects/proxmox-thermals`
  - `/root/projects/dash-noc`

## Contexto del proyecto

Nombre:

- `dash-noc`

Descripcion GitHub propuesta:

> Tablet-first NOC dashboard for a homelab, served from Proxmox, showing live clock, Proxmox health, workstation status, and important alerts/notifications.

Objetivo:

- pantalla NOC para Lenovo Tab 8
- servida desde Proxmox
- fuera de la UI nativa de Proxmox
- reutilizando `proxmox-thermals` solo como fuente/referencia

Contenido principal deseado:

- reloj grande en tiempo real a la derecha
- estado Proxmox: CPU, RAM, storage, VMs/LXC, temperaturas principales
- estado `JM22W11`: CPU, RAM, disco, red, uptime, bateria si aplica
- emails/notificaciones importantes desde un servicio en `JM22W11`
- alertas visibles y filtradas

## Archivos importantes

Leer primero:

- `README.md`
- `docs/overview.md`
- `docs/planning.md`
- `docs/tasks.md`
- `.ai/dash-noc.md`

ADRs:

- `docs/adr/0001-project-scope.md`
- `docs/adr/0002-proxmox-serves-dashboard.md`
- `docs/adr/0003-agent-services-for-remote-data.md`
- `docs/adr/0004-tablet-first-layout.md`

Previews:

- `docs/design/previews/03-noc.html`: mejor direccion visual para la pantalla NOC.
- `docs/design/previews/04-mail.html`: buena referencia futura para vista de alertas/mail.

Capturas renderizadas:

- `docs/design/previews/screenshots/01-dual-host.png`
- `docs/design/previews/screenshots/02-side-by-side.png`
- `docs/design/previews/screenshots/03-noc.png`
- `docs/design/previews/screenshots/04-mail.png`

## Decision visual

La mejor base es `03-noc.html`.

Motivo:

- densa pero operativa
- escaneable
- encaja con panel NOC
- compara bien sistemas
- prioriza tablas y alertas sobre tarjetas decorativas

`04-mail.html` queda como futura vista de alertas/notificaciones, no como pantalla principal.

## Pendiente inmediato

1. Confirmar resolucion/orientacion real del Lenovo Tab 8.
2. Crear preview `tablet-noc` basada en `03-noc.html`.
3. Reducir metricas no reales:
   - `Power`
   - `Net I/O` si no hay fuente real
   - `Backups` si no se va a exponer todavia
4. Definir contrato JSON de:
   - `/api/noc/current`
   - `JM22W11 /status`
   - `JM22W11 /notifications`
5. Decidir stack inicial para API central.

## Nota operativa

Al abrir la nueva sesion:

```bash
cd /root/projects/dash-noc
codex
```

Primer mensaje recomendado:

```text
leer .ai/HANDOFF.md
```

