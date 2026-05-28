# Overview

## Nombre

`dash-noc`

## Contexto

El proyecto nace a partir de `proxmox-thermals`, pero cambia de alcance.

`proxmox-thermals` monitoriza temperaturas y metricas del host Proxmox. `dash-noc` sera una pantalla NOC general para una tablet Lenovo Tab 8.

## Alcance inicial

La primera version debe mostrar:

- reloj grande a la derecha, siempre visible
- estado basico de Proxmox:
  - CPU
  - RAM
  - storage
  - VMs/LXC si esta disponible
  - temperaturas importantes si esta disponible
- estado de `JM22W11`:
  - CPU
  - RAM
  - disco
  - red
  - uptime
  - bateria si aplica
- emails y notificaciones importantes:
  - criticas
  - warnings
  - ultimas entradas relevantes
  - estado leido/pendiente si se puede exponer

## Fuera de alcance inicial

- integracion dentro de la UI nativa de Proxmox
- gestion completa de correo
- acciones destructivas desde la tablet
- login multiusuario complejo
- graficas historicas profundas

## Principios

- Disenar primero para Lenovo Tab 8.
- Priorizar legibilidad a distancia corta.
- Mostrar solo informacion accionable o util de un vistazo.
- Usar Proxmox como servidor central por disponibilidad y recursos.
- Obtener datos remotos mediante servicios pequenos, no por scraping fragile.
- Mantener `thermals` como modulo/fuente, no como centro conceptual.

## Arquitectura logica

```text
Lenovo Tab 8
  -> dash-noc frontend servido por Proxmox

Proxmox
  -> dash-noc API central
  -> collector local Proxmox
  -> cliente hacia JM22W11 status API
  -> cliente hacia JM22W11 notifications API

JM22W11
  -> status service
  -> notifications/mail service
```

## Vistas previstas

- `NOC`: pantalla principal para tablet.
- `Thermals`: vista heredada o enlace a `proxmox-thermals`.
- `Alerts/Mail`: vista futura para detalle de notificaciones.

