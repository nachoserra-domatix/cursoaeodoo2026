# Control de Errores (Bug Tracker)

## 🔴 Pendientes

* **[Kanban] No se actualiza el estado al arrastrar propiedades**
  * *Descripción:* En la vista Kanban del módulo de propiedades, al mover una tarjeta de una columna a otra, la marca de 'Reservado' no se actualiza
  * *Ubicación:* Modelo `realeste_property`, campo `available` (selection), vista `views/realestate_property_views.xml`.
  * *Comportamiento esperado:* Al mover fuera de la columna "Reservado", el campo `available` debería actualizarse. Solo se cambia el campo `state`.
  * *Prioridad:* Alta