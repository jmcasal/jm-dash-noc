# Tasks

## Now

- [x] Crear estructura documental inicial.
- [x] Nombrar proyecto como `dash-noc`.
- [x] Separar memoria IA en `.ai` y documentacion en `docs`.
- [ ] Definir resolucion/orientacion real del Lenovo Tab 8.
- [x] Crear preview `tablet-noc` basada en `03-noc.html`.
- [x] Eliminar de la preview metricas no reales o marcarlas como futuras.

## Next

- [ ] Definir contrato JSON de `/api/noc/current`.
- [ ] Definir contrato JSON de `JM22W11 /status`.
- [ ] Definir contrato JSON de `JM22W11 /notifications`.
- [ ] Decidir stack inicial de API central.
- [ ] Decidir si se reutiliza codigo de `/projects/proxmox-thermals` o se crea proyecto limpio.

## Later

- [ ] Implementar API central en Proxmox.
- [ ] Implementar collector Proxmox.
- [ ] Implementar servicio `JM22W11`.
- [ ] Implementar servicio de notificaciones/email.
- [ ] Crear servicio systemd para API central.
- [ ] Crear servicio systemd para agente `JM22W11`.
- [ ] Preparar modo kiosk en Lenovo Tab 8.

## Open Questions

- Resolucion exacta y orientacion del Lenovo Tab 8.
- Sistema operativo actual de `JM22W11`.
- Fuente real de emails/notificaciones en `JM22W11`.
- Si el dashboard sera accesible solo en LAN o tambien via VPN.
- Si necesita autenticacion o basta restriccion de red.
