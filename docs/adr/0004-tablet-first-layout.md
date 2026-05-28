# ADR 0004: Layout tablet-first

## Estado

Propuesta.

## Contexto

La pantalla objetivo es una Lenovo Tab 8. Los prototipos actuales estan pensados como lienzo fijo de 1920px.

## Decision

Disenar primero una vista NOC para tablet y usar `03-noc.html` solo como direccion visual.

## Consecuencias

- Se reducira densidad respecto al prototipo desktop.
- El reloj y las alertas tendran prioridad visual.
- Los detalles extensos quedaran ocultos o resumidos.
- Habra que validar con capturas en la resolucion real de la tablet.

