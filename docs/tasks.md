# Tasks

## Now

- [x] Crear estructura documental inicial.
- [x] Nombrar proyecto como `dash-noc`.
- [x] Separar memoria IA en `.ai` y documentacion en `docs`.
- [ ] Confirmar en dispositivo real la resolucion/orientacion del Lenovo Tab 8.
- [x] Crear preview `tablet-noc` basada en `03-noc.html`.
- [x] Eliminar de la preview metricas no reales o marcarlas como futuras.
- [x] Definir contrato JSON de `/api/noc/current`.
- [x] Definir contrato JSON de `JM22W11 /status`.
- [x] Definir contrato JSON de `JM22W11 /notifications`.
- [x] Decidir stack inicial de API central.
- [x] Decidir si se reutiliza codigo de `/projects/proxmox-thermals` o se crea proyecto limpio.

## Done in current pass

- [x] Crear esqueleto de API central con datos mock.
- [x] Servir `tablet-noc` desde la API central.
- [x] Implementar `/health`.
- [x] Implementar `/api/noc/current` con payload mock conforme a contrato.
- [x] Crear adaptador Proxmox desde `/projects/proxmox-thermals/data/current.json`.
- [x] Hacer que `tablet-noc` consuma `/api/noc/current` en vez de datos estaticos.

## Next

- [ ] Convertir alertas/notificaciones de la preview a render dinamico completo.
- [ ] Crear servicio systemd para API central.
- [ ] Definir contrato interno del agente `JM22W11`.
- [ ] Implementar agente `JM22W11 /status`.
- [ ] Implementar agente `JM22W11 /notifications`.

## Later

- [ ] Crear servicio systemd para agente `JM22W11`.
- [ ] Preparar modo kiosk en Lenovo Tab 8.

## Open Questions

- Resolucion exacta y orientacion del Lenovo Tab 8.
- Sistema operativo actual de `JM22W11`.
- Fuente real de emails/notificaciones en `JM22W11`.
- Si el dashboard sera accesible solo en LAN o tambien via VPN.
- Si necesita autenticacion o basta restriccion de red.
