# Pagina `thermals` para Proxmox

## Resumen

`proxmox-thermals` es una pagina local para monitorizar el host Proxmox.

El proyecto recuperado de la memoria del host vive en:

- `/projects/proxmox-thermals`

La pagina expone dos vistas web:

- `/`: `Large View`, vista completa.
- `/simple`: `Simple View`, vista compacta para ver la maxima informacion por pantalla.

La API local sirve por defecto en:

- `127.0.0.1:8123`

## Objetivo

Mostrar de forma rapida:

- temperaturas del host
- temperaturas de discos NVMe y SATA
- sensores CPU por core cuando existen
- uso de CPU y RAM
- uso de filesystems y storages Proxmox
- historico termico ligero local

## Arquitectura

Componentes principales:

- collector Python: recoge metricas del host.
- storage por ficheros JSON/JSONL: guarda snapshot actual e historico.
- API HTTP ligera: sirve datos y frontend estatico.
- frontend HTML/CSS/JS con ECharts: dibuja gauges, barras y graficas.

Rutas relevantes del proyecto vivo:

- `/projects/proxmox-thermals/src/proxmox_thermals/collector.py`
- `/projects/proxmox-thermals/src/proxmox_thermals/api.py`
- `/projects/proxmox-thermals/src/proxmox_thermals/frontend/index.html`
- `/projects/proxmox-thermals/src/proxmox_thermals/frontend/simple.html`
- `/projects/proxmox-thermals/src/proxmox_thermals/frontend/app.js`
- `/projects/proxmox-thermals/src/proxmox_thermals/frontend/simple.js`
- `/projects/proxmox-thermals/src/proxmox_thermals/frontend/styles.css`
- `/projects/proxmox-thermals/data/current.json`
- `/projects/proxmox-thermals/data/history/30s.jsonl`
- `/projects/proxmox-thermals/data/history/90s.jsonl`
- `/projects/proxmox-thermals/data/history/900s.jsonl`

## API

Endpoints conocidos:

- `/health`
- `/api/current`
- `/api/current?fresh=1&max_age=300`
- `/api/history?series=30s&limit=300`
- `/api/history?series=90s&limit=300`
- `/api/history?series=900s&limit=300`

La API tambien sirve:

- `/`
- `/simple`
- `/app.js`
- `/simple.js`
- `/styles.css`

Variables de entorno:

- `PROXMOX_THERMALS_DATA_DIR`: directorio de datos. Por defecto, `./data`.
- `PROXMOX_THERMALS_BIND`: bind de la API. Por defecto, `127.0.0.1`.
- `PROXMOX_THERMALS_PORT`: puerto de la API. Por defecto, `8123`.

## Frontend

Decisiones ya tomadas:

- `Large View` es la vista completa.
- `Simple View` es la vista compacta.
- La preferencia de vista se guarda en `localStorage` con la clave `proxmox-thermals:view`.
- Las temperaturas se muestran con gauges circulares.
- El uso y espacio se muestran con barras.
- Las temperaturas se formatean con un decimal.
- La grafica inferior se construye dinamicamente con todas las temperaturas presentes en el historico, no con una lista fija.

`Simple View` quedo organizada con:

- `Proxmox Summary`
  - `CPU Package`
  - `Motherboard`
  - `CPU Usage`
  - `RAM Usage`
- `Proxmox Disk Usage`
  - `Root FS`
  - `local-lvm`
  - `temp-storage`

## Datos y sensores

Fuentes usadas o previstas:

- `smartctl`
- `lsblk`
- `df`
- `pvesm status`
- `/proc/loadavg`
- `/proc/meminfo`
- `/sys/class/hwmon`

Criterios:

- Identificar discos por serie, no por `sdX` o `nvmeX`.
- Para SATA, usar SMART y fallback por tipo cuando haga falta: `sat`, `scsi`, `nvme`.
- Conservar solo sensores CPU por core realmente expuestos por el host.
- No intentar mostrar ocupacion de particiones SATA no montadas salvo que haya una capa conocida que exponga uso.

Metricas reales documentadas el 2026-03-21:

- SATA:
  - `sda`: `480103981056` bytes, `22.0 C`
  - `sdb`: `4000787030016` bytes, `12.0 C`
  - `sdc`: `960197124096` bytes, `18.0 C`
  - `sdd`: `2000398934016` bytes, `15.0 C`
  - `sde`: `960197124096` bytes, `24.0 C`
  - `sdf`: `250059350016` bytes, `25.0 C`
- NVMe:
  - `nvme0n1`: `41.0 C`, `sensor2 82.0 C`
  - `nvme1n1`: `37.0 C`, `sensor2 66.0 C`
- sensores CPU por core expuestos entonces:
  - `cpu_core_0_c`
  - `cpu_core_4_c`
  - `cpu_core_8_c`
  - `cpu_core_12_c`
  - `cpu_core_16_c`
  - `cpu_core_20_c`
  - `cpu_core_28_c`
  - `cpu_core_29_c`
  - `cpu_core_30_c`
  - `cpu_core_31_c`

## Estado conocido

Segun la bitacora recuperada:

- `current.json` ya reflejaba metricas reales del host.
- El dashboard mostraba temperaturas SATA y NVMe con decimal.
- La grafica inferior ya no estaba limitada a NVMe.
- Los sensores CPU por core visibles eran solo los realmente expuestos por el host.

Pendiente recomendado:

- Revisar visualmente `/` y `/simple` en navegador.
- Decidir si conviene priorizar temperaturas NVMe desde `hwmon` frente a `smartctl` para conservar precision subgrado.
