# ADR 0002: Proxmox sirve el dashboard NOC

## Estado

Aceptada.

## Contexto

La tablet solo debe consumir una URL. Proxmox esta siempre encendido, tiene CPU suficiente y ya es una fuente principal de datos.

## Decision

Servir `dash-noc` desde Proxmox como aplicacion web propia, fuera de la UI nativa de Proxmox.

## Consecuencias

- El dashboard podra estar en una URL propia.
- No dependera de parches del frontend de Proxmox.
- Se podra reiniciar/actualizar sin tocar `pveproxy`.
- Habra que crear un servicio API/web propio.

