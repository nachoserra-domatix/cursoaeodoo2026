# Tareas pendientes

Este es el backlog de decisiones por resolver y trabajo por implementar. Las
reglas y decisiones de dominio se detallan en [BUSINESS_RULES.md](BUSINESS_RULES.md),
los defectos observados en [BUGS.md](BUGS.md), y el comportamiento actual en
[SPECIFICATION.md](SPECIFICATION.md).

## Decisiones por resolver

- [ ] Resolver la fuente y el ciclo de disponibilidad definidos en BR-001/BR-016
  antes de implementar BUG-001.
- [ ] Resolver la cardinalidad de ofertas aceptadas y las operaciones permitidas
  sobre propiedades no disponibles (BR-013/BR-014; BUG-003).
- [ ] Acordar los datos requeridos y el significado del estado «Enviada» (BR-006;
  BUG-007).
- [ ] Definir el ciclo de contratos de alquiler y su efecto sobre la propiedad
  (BR-015/BR-016).
- [ ] Confirmar la política de acceso por comercial descrita en BUG-002.

## Propiedades

- [ ] Implementar el ciclo de etapas acordado para la propiedad y sincronizar en el
  modelo la etapa con `availability`; impedir combinaciones incoherentes desde
  cualquier punto de entrada, no solo desde el kanban (BR-001, BUG-001).
- [ ] Añadir los campos aún ausentes de superficie, habitaciones y propietario;
  decidir si la modalidad de venta/alquiler pertenece a la propiedad o al
  contrato.
- [ ] Añadir en las etapas la opción de plegado y persistir el estado plegado de
  cada columna del kanban, si se mantiene como requisito de uso.
- [ ] Reorganizar los botones de acciones dentro de las pestañas relacionadas
  (visitas y ofertas) para que estén junto a los registros a los que afectan.

## Ofertas

- [ ] Validar en el modelo las transiciones permitidas de oferta; aceptar solo
  ofertas en estados válidos y aplicar la regla acordada sobre ofertas aceptadas
  y disponibilidad (BR-002, BR-013, BUG-003).
- [ ] Validar en servidor la creación de contratos desde ofertas: exigir estado
  aceptado, propiedad y comprador; impedir crear repetidamente contratos para la
  misma oferta si esa es la regla deseada (BR-003, BUG-004).
- [ ] Revisar «Crear oferta»: no pasar a `sent` hasta completar los datos
  obligatorios acordados; establecer fecha y comprador cuando corresponda
  (BR-006, BUG-007).
- [ ] Corregir el botón «Eliminar ofertas rechazadas»: ocultarlo a usuarios sin
  permiso de borrado o ajustar los permisos según la política acordada (BUG-005).
- [ ] Definir y probar un criterio estable para desempatar ofertas con el mismo
  importe en «Aceptar mejor oferta» (BR-005).

## Seguridad

- [ ] Implementar reglas de registro para visitas, ofertas y contratos según la
  política de acceso por comercial; mantener acceso global para responsables y
  probar el acceso desde las fichas de propiedad (BUG-002).

## Visitas

- [ ] Corregir `next_visit_date` para excluir visitas pasadas si debe representar
  la próxima visita, y recalcularlo cuando el paso del tiempo haga que cambie el
  resultado (BUG-006).
- [ ] Validar en el modelo las transiciones de visita si deben impedirse cambios
  directos entre estados que no sean válidos para el flujo.

## Contratos

- [ ] Definir e implementar las reglas específicas de contratos de alquiler y su
  relación con la disponibilidad de la propiedad (BR-015, BR-016).
- [ ] Añadir la relación y acceso a los contratos desde la ficha de propiedad si
  se requiere consultar allí su historial.
- [ ] Definir y validar en servidor los datos obligatorios y las transiciones de
  estado del contrato; revisar también límites como renta o depósito negativos.
- [ ] Completar las pruebas del ciclo de vida: contrato creado desde oferta
  aceptada, vencimiento automático y efecto de cancelación/finalización sobre la
  disponibilidad.

## Incidencias

- [ ] Añadir menú y vistas propias para incidencias si deben gestionarse fuera de
  la ficha de propiedad; actualmente se gestionan desde la pestaña y el contador
  de cada propiedad.

## Pruebas y documentación

- [ ] Añadir pruebas automatizadas para disponibilidad, aceptación de ofertas,
  permisos, creación de contratos, fechas de visitas y automatizaciones diarias.
- [ ] Actualizar `SPECIFICATION.md`, `BUSINESS_RULES.md` y `DATA_MODEL.md` al
  implementar cambios de flujo, campos o relaciones.

