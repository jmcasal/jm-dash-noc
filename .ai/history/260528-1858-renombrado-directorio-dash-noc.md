fecha y hora

- 2026-05-28 18:58 CEST

objetivo de la sesion

- renombrar la carpeta local para que refleje el nuevo alcance `dash-noc`

acciones realizadas

- se movio `/root/projects/proxmox-thermals` a `/root/projects/dash-noc`
- se revisaron referencias internas al nombre antiguo
- se actualizo `.ai/README.md` para describir `dash-noc`

decisiones

- se renombra en vez de copiar porque este directorio no era un repositorio git y no contenia la implementacion viva antigua
- la implementacion historica de termicas sigue referenciada en `/projects/proxmox-thermals`

siguiente paso

- continuar trabajando desde `/root/projects/dash-noc`
