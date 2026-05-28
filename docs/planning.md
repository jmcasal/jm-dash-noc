# Planning

## Fase 0: Definicion

Objetivo:

- cerrar alcance de `dash-noc`
- documentar decisiones base
- elegir layout tablet

Entregables:

- README inicial
- overview
- ADRs iniciales
- backlog de tareas
- contratos JSON iniciales

Estado: cerrada salvo confirmacion de resolucion real de la tablet.

## Fase 1: Prototipo estatico tablet

Objetivo:

- convertir la direccion visual de `03-noc.html` en una pantalla NOC para Lenovo Tab 8
- reducir datos inventados
- priorizar Proxmox, `JM22W11`, reloj y notificaciones

Entregables:

- preview HTML estatica `tablet-noc`
- capturas renderizadas
- decision de layout base

Estado: preview inicial creada asumiendo `1280x800` en horizontal.

## Fase 2: API central en Proxmox

Objetivo:

- servir frontend y endpoints agregados desde Proxmox
- exponer datos mock primero y reales despues

Endpoints previstos:

- `/api/noc/current`
- `/api/proxmox/status`
- `/api/jm22w11/status`
- `/api/notifications/important`
- `/health`

Stack inicial:

- Python 3.11+
- libreria estandar HTTP/JSON
- frontend estatico servido por el proceso central

Estado: esqueleto mock creado con endpoints contractuales iniciales.
El endpoint Proxmox ya puede leer `/projects/proxmox-thermals/data/current.json` y cae a mock si no existe.

## Fase 3: Collector Proxmox

Objetivo:

- reutilizar o adaptar datos de `proxmox-thermals`
- exponer CPU, RAM, storage, VMs/LXC y temperaturas principales

## Fase 4: Servicio `JM22W11`

Objetivo:

- crear servicio ligero en la maquina de trabajo para estado basico
- definir contrato JSON estable

Datos deseados:

- hostname
- uptime
- CPU
- RAM
- discos principales
- red
- bateria si existe
- timestamp de ultima lectura

## Fase 5: Servicio de notificaciones

Objetivo:

- exponer emails/notificaciones importantes desde `JM22W11`
- filtrar ruido antes de enviar al dashboard

Datos deseados:

- severidad
- origen
- asunto/titulo
- resumen corto
- timestamp
- estado pendiente/leido si existe

## Fase 6: Hardening tablet

Objetivo:

- modo pantalla fija
- refresco automatico robusto
- estados de error visibles
- no quemar CPU ni bateria de la tablet
