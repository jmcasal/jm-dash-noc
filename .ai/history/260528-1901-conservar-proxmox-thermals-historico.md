fecha y hora

- 2026-05-28 19:01 CEST

objetivo de la sesion

- corregir la estrategia de renombrado para conservar el path antiguo como historico

acciones realizadas

- se recreo `/root/projects/proxmox-thermals` como directorio historico
- se dejo `/root/projects/dash-noc` como proyecto activo
- se actualizo `~/.codex/config.toml` para incluir ambos proyectos como trusted

criterio

- no borrar referencias antiguas a `proxmox-thermals`
- anadir referencias nuevas a `dash-noc`
- seguir trabajando desde `/root/projects/dash-noc`
