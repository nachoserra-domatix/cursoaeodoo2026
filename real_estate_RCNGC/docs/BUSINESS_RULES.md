# Reglas de negocio

Este documento recoge las reglas del proceso inmobiliario y su grado de
implementación actual. «Implementada» significa que el modelo ejecuta la regla;
«Parcial» indica que solo se cubre parte del flujo o que la vista la sugiere sin
validarla en servidor; «Pendiente» requiere una decisión o desarrollo. Los
síntomas concretos se registran en [BUGS.md](BUGS.md) y el trabajo accionable en
[TODO.md](TODO.md).

## Propiedades y disponibilidad

### BR-001 — Disponibilidad según situación de la propiedad

Una propiedad reservada, vendida o alquilada no debe estar disponible para nuevas
operaciones.

**Estado:** Parcial. El modelo no tiene estados de propiedad «Reservada»,
«Vendida» o «Alquilada»: usa una etapa configurable (`stage_id`) y un booleano
independiente (`availability`). «Reservar» y aceptar una oferta desactivan el
booleano, pero cambiar de etapa no lo modifica.

**Pendiente:** Definir si la disponibilidad se deriva de etapas/contratos o si
es un dato independiente, y establecer cómo se reactiva una propiedad.

### BR-002 — Aceptación de una oferta

Al aceptar una oferta:

- La oferta pasa a `accepted`.
- La propiedad asociada deja de estar disponible.
- La propiedad queda reservada para el comprador.

**Estado:** Parcial. La acción cambia la oferta a `accepted` y pone
`availability` a falso, pero no cambia la etapa de la propiedad a «Reservada».
Tampoco impide aceptar ofertas adicionales para esa propiedad.

## Ofertas y contratos

### BR-003 — Creación de contrato desde una oferta

Solo una oferta aceptada puede originar un contrato. El contrato se crea con:

- Estado `draft`.
- La propiedad de la oferta.
- El comprador de la oferta como cliente.
- Tipo `sale`.
- Fecha de inicio igual a la fecha actual.

**Estado:** Parcial. La vista solo muestra el botón para ofertas aceptadas, pero
el método del modelo no valida el estado ni que existan propiedad y comprador.
La restricción debe aplicarse en servidor.

### BR-004 — Importe de una oferta

El importe de una oferta no puede ser negativo.

**Estado:** Implementada. Se rechazan importes menores que cero; se permite
importe cero.

### BR-005 — Aceptar la mejor oferta

La acción «Aceptar mejor oferta» de una propiedad selecciona la oferta en estado
`sent` con el mayor importe y la acepta. Si no hay ofertas enviadas, no cambia
nada.

**Estado:** Implementada para esa acción. No se resuelven empates de forma
explícita y la aceptación directa desde la ficha de oferta no exige que esté
enviada.

### BR-006 — Crear oferta desde una propiedad

La acción de creación rápida toma el precio de la propiedad como importe inicial
y pasa la oferta directamente a `sent`.

**Estado:** Implementada, pero la oferta puede quedar enviada sin comprador ni
fecha porque esos datos no son obligatorios.

**Pendiente:** Decidir qué datos deben ser obligatorios antes de enviar una
oferta y si «Enviar» debe producir una notificación real.

## Visitas

### BR-007 — Cancelación de visitas pendientes

Al cancelar las visitas pendientes de una propiedad, las visitas en estado
`draft` o `scheduled` pasan a `canceled`. Las visitas realizadas o ya canceladas
no se modifican.

**Estado:** Implementada por la acción de la propiedad.

### BR-008 — Finalización automática de visitas

Una visita `scheduled` cuya fecha y hora ya haya pasado debe pasar a `done`.

**Estado:** Implementada mediante una tarea programada diaria. La tarea actúa
sobre fechas anteriores al momento de ejecución; una visita puede seguir
apareciendo como programada hasta la siguiente ejecución.

## Contratos

### BR-009 — Coherencia de fechas del contrato

Si se informa una fecha de fin, la fecha de inicio debe ser anterior o igual a
ella.

**Estado:** Implementada. Se rechaza el contrato cuando la fecha de inicio es
posterior a la fecha de fin.

### BR-010 — Finalización automática de contratos

Un contrato `progress` cuya fecha de fin sea hoy o anterior pasa a `done`.

**Estado:** Implementada mediante una tarea programada diaria.

### BR-011 — Renta inicial del contrato

Al seleccionar una propiedad en un contrato, el campo de renta se inicializa con
el precio de la propiedad.

**Estado:** Implementada como actualización de formulario (`onchange`); no es
una validación del modelo y el valor puede modificarse después.

## Integridad de datos

### BR-012 — Unicidad de referencias y nombres

Si se informa una referencia de propiedad o un nombre de contrato, ese valor no
puede repetirse.

**Estado:** Implementada mediante restricciones de unicidad en base de datos.

## Decisiones pendientes

- **BR-013 — Una sola oferta aceptada por propiedad:** decidir si aceptar una
  oferta debe rechazar las restantes y bloquear nuevas aceptaciones. Actualmente
  no se impide que haya varias ofertas aceptadas.
- **BR-014 — Operaciones sobre propiedades no disponibles:** decidir si se deben
  bloquear nuevas ofertas o contratos cuando una propiedad ya no está disponible.
  El selector de propiedad de la oferta filtra las disponibles, pero esa
  restricción no cubre todos los puntos de entrada ni está validada en servidor.
- **BR-015 — Contratos de alquiler:** definir cómo se crean y qué efecto tienen
  sobre la disponibilidad de la propiedad. El modelo admite contratos `rent`,
  pero la creación desde ofertas solo genera contratos de venta.
- **BR-016 — Disponibilidad al terminar o cancelar un contrato:** definir si una
  propiedad alquilada vuelve a estar disponible al finalizar/cancelar el contrato
  y qué ocurre con una venta. Actualmente los cambios de estado del contrato no
  modifican `availability`.