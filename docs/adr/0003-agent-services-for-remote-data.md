# ADR 0003: Servicios agentes para datos remotos

## Estado

Propuesta.

## Contexto

`dash-noc` necesita datos de `JM22W11` y notificaciones/emails que no viven en Proxmox.

Consultar datos remotos por SSH o scraping desde Proxmox puede ser fragil y dificil de mantener.

## Decision

Crear servicios pequenos en `JM22W11` para exponer datos mediante HTTP local.

Servicios previstos:

- status service
- notifications/mail service

## Consecuencias

- Hace falta instalar y mantener un agente en `JM22W11`.
- El contrato JSON puede ser estable y facil de testear.
- Proxmox solo agrega y cachea datos.

