# Control de Errores (Bug Tracker)

## 🔴 Pendientes

* **[Kanban] No se actualiza el estado al arrastrar propiedades**
  * *Descripción:* En la vista Kanban del módulo de propiedades, al mover una tarjeta de una columna a otra, la marca de 'Reservado' no se actualiza
  * *Ubicación:* Modelo `realeste_property`, campo `available` (selection), vista `views/realestate_property_views.xml`.
  * *Comportamiento esperado:* Al mover fuera de la columna "Reservado", el campo `available` debería actualizarse. Solo se cambia el campo `state`. Quizá hay que aclarar cual debe ser el comportamiento del campo `available`. ¿Solo esta 'disponible' si no esta ni reservado ni vendiido ni alquilado? ¿Se debe BLOQUEAR los movimientos del kanban, o la selecion de estado en ciertas circunstancias?
  * *Prioridad:* Alta