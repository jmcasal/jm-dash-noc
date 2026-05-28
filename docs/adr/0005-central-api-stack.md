# ADR 0005: API central Python sin framework inicialmente

## Estado

Aceptada.

## Contexto

`dash-noc` debe servirse desde Proxmox y exponer una API pequena para una tablet en LAN.

`proxmox-thermals` ya funciona con Python 3, `http.server` y ficheros JSON/JSONL, sin dependencias web externas. Ese enfoque reduce el coste operativo en Proxmox y facilita arrancar con datos mock o ficheros existentes.

## Decision

Implementar la API central inicial con Python 3.11+ y libreria estandar:

- `ThreadingHTTPServer` para HTTP local.
- JSON desde libreria estandar.
- frontend estatico servido por el mismo proceso.
- variables de entorno para bind, puerto, rutas de datos y URLs de agentes.

No introducir FastAPI, Flask, Node, bundlers ni base de datos en la primera version.

## Consecuencias

- Menos dependencias que instalar en Proxmox.
- La API sera facil de empaquetar como servicio systemd.
- Los contratos JSON deben estar bien documentados porque no habra OpenAPI generado automaticamente al principio.
- Si la API crece en complejidad, se podra migrar a FastAPI manteniendo los contratos.
