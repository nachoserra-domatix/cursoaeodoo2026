# Control de errores (Bug Tracker)

Aquí se registran defectos observables y riesgos de implementación, no decisiones
de producto. Las reglas relacionadas están en [BUSINESS_RULES.md](BUSINESS_RULES.md)
y las acciones para corregirlos en [TODO.md](TODO.md).

## Pendientes

### BUG-001 — Etapa del kanban y disponibilidad no están sincronizadas

- **Prioridad:** Alta
- **Ubicación:** `models/realestate_property.py` (`stage_id`, `availability`, `action_reserve`); `views/realestate_property_views.xml`.
- **Comportamiento actual:** El kanban agrupa por `stage_id`, que apunta a etapas configurables (`realestate.property.stage`). Arrastrar una tarjeta cambia la etapa, pero no el booleano `availability`. La marca «Reserved» depende exclusivamente de que `availability` sea falso. No existe un estado de selección llamado `state` ni una columna «Reservado» garantizada.
- **Corrección necesaria:** Definir primero si la disponibilidad se deriva de la etapa o es un dato independiente. Si se deriva, acordar qué etapas significan disponible/no disponible y sincronizarlo también en servidor. No basta con volver a marcar disponible al salir de una etapa «Reservada»: una propiedad vendida o alquilada tampoco debería volver a estar disponible.

### BUG-002 — Acceso a registros relacionados no sigue el ámbito de propiedades

- **Prioridad:** Alta si se pretende que cada usuario trabaje solo con sus propiedades.
- **Ubicación:** `security/real_estate_security.xml`; modelos `realestate.visit`, `realestate.offer` y `realestate.contract`.
- **Comportamiento actual:** La regla «Personal Properties» limita los registros de `realestate.property` al usuario asignado o a propiedades sin asignar. No hay reglas equivalentes para visitas, ofertas ni contratos; sus permisos de lectura permiten a los usuarios del módulo consultar registros de otros comerciales desde sus menús.
- **Comportamiento esperado:** Si el ámbito personal debe proteger también los datos asociados, limitar esos modelos a registros cuya propiedad sea accesible para el usuario, y dejar al grupo Responsable el acceso global. Verificar además que las reglas no impidan acceder a los registros desde la ficha de una propiedad propia.

### BUG-003 — Se pueden aceptar varias ofertas para la misma propiedad

- **Prioridad:** Alta si una propiedad solo puede tener una oferta aceptada/reserva activa.
- **Ubicación:** `models/realestate_offer.py` (`action_accept`).
- **Comportamiento actual:** Aceptar una oferta solo marca esa oferta como aceptada y desactiva la disponibilidad de la propiedad. No comprueba si la propiedad ya está reservada ni si existe otra oferta aceptada; las demás ofertas tampoco se rechazan automáticamente. La acción se puede ejecutar desde una oferta aunque la propiedad ya no esté disponible.
- **Comportamiento esperado:** Definir la regla para ofertas posteriores a una aceptación y hacer cumplir en el modelo que no haya aceptaciones incompatibles. La validación no debe depender únicamente de que un botón esté oculto en la vista.

### BUG-004 — La creación de contrato no valida que la oferta esté aceptada

- **Prioridad:** Alta
- **Ubicación:** `models/realestate_offer.py` (`action_create_contract`); `views/realestate_offer_views.xml`.
- **Comportamiento actual:** La vista solo muestra «Create Contract» cuando la oferta está aceptada, pero el método del modelo crea el contrato sin comprobar el estado. La ocultación del botón no es una validación de servidor.
- **Comportamiento esperado:** Rechazar en el método la creación desde una oferta que no esté aceptada y validar que la oferta tenga propiedad y comprador, conforme a BR-003.

### BUG-005 — «Eliminar ofertas rechazadas» falla para usuarios normales

- **Prioridad:** Media
- **Ubicación:** `models/realestate_property.py` (`action_delete_refused_offers`); `security/ir.model.access.csv`; `views/realestate_property_views.xml`.
- **Comportamiento actual:** El botón está disponible en la ficha de propiedad para los usuarios del módulo, pero el permiso de ofertas solo concede `unlink` al grupo Responsable. Un usuario normal que ejecute la acción recibirá un error de acceso al intentar borrar las ofertas.
- **Comportamiento esperado:** Hacer coincidir la interfaz y los permisos: restringir el botón a responsables o conceder explícitamente la eliminación a usuarios si esa es la política deseada.

### BUG-006 — La fecha de próxima visita puede mostrar una visita pasada

- **Prioridad:** Media
- **Ubicación:** `models/realestate_property.py` (`_compute_next_visit_date`).
- **Comportamiento actual:** Se toma la visita programada con la fecha más temprana, sin filtrar fechas anteriores a la actual. Por tanto, una visita programada cuya fecha ya pasó puede seguir figurando como «Next Visit Date» si el cron aún no la ha marcado como realizada.
- **Comportamiento esperado:** Si el campo representa realmente la próxima visita, excluir fechas pasadas y asegurar su recálculo cuando el tiempo avance, además de cuando cambien las visitas.

### BUG-007 — «Crear oferta» la envía sin comprador ni fecha

- **Prioridad:** Media; confirmar los datos obligatorios del proceso comercial.
- **Ubicación:** `models/realestate_property.py` (`action_create_offer`); `models/realestate_offer.py`.
- **Comportamiento actual:** La acción crea una oferta con propiedad e importe, deja comprador y fecha vacíos, y la cambia inmediatamente a «Enviada». El modelo no exige esos datos y «Enviar» no realiza un envío externo.
- **Comportamiento esperado:** Antes de marcarla enviada, solicitar o validar al menos el comprador y los datos que el negocio considere necesarios; si aún está incompleta, mantenerla en borrador.