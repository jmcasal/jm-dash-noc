# ADR 0001: `dash-noc` como proyecto separado de `proxmox-thermals`

## Estado

Aceptada.

## Contexto

El trabajo inicial partia de una pagina `thermals` para Proxmox. El nuevo objetivo es una pantalla NOC para tablet que muestre Proxmox, `JM22W11`, reloj, emails y notificaciones.

Esto supera el alcance de un dashboard termico.

## Decision

Crear `dash-noc` como proyecto conceptual separado.

`proxmox-thermals` queda como:

- fuente de datos Proxmox
- referencia visual
- modulo reutilizable si conviene

## Consecuencias

- La interfaz ya no se disena como pestaña de Proxmox.
- Proxmox seguira sirviendo el dashboard por disponibilidad.
- La documentacion nueva vivira en `docs/`.
- La memoria para IA vivira en `.ai/`.

