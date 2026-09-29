# Especificación funcional

## Alcance actual

El módulo permite gestionar propiedades, categorías, imágenes, visitas, ofertas,
incidencias y contratos. Esta especificación describe el comportamiento actual
de los modelos, vistas y automatizaciones. Las reglas y decisiones de negocio
están en [BUSINESS_RULES.md](BUSINESS_RULES.md), los defectos conocidos en
[BUGS.md](BUGS.md) y las tareas pendientes en [TODO.md](TODO.md).

## Propiedades

Una propiedad reúne la información del inmueble y sirve de punto de acceso a sus
imágenes, visitas, ofertas e incidencias.

### Información

- Nombre (obligatorio), referencia (única), descripción y precio.
- Categoría, seleccionada de las categorías configuradas.
- Usuario responsable, que por defecto es el usuario actual.
- Disponibilidad, un booleano que por defecto está activado.
- Etapa configurable, usada como estado visual y como agrupación del kanban.
- Color para la vista kanban.
- Próxima visita programada, calculada a partir de la visita en estado
  «Programada» con la fecha más próxima. El cálculo no excluye visitas pasadas.
- Recuento de visitas e incidencias, mostrado como accesos rápidos.

No hay campos implementados para superficie, número de habitaciones, propietario
o modalidad de venta/alquiler.

### Etapas y disponibilidad

La etapa es un registro configurable con nombre y secuencia; no existe una lista
cerrada de etapas ni se cargan etapas predeterminadas desde los datos del módulo.
Las etapas se muestran en el kanban, que se agrupa por ellas.

La disponibilidad es independiente de la etapa. Se puede cambiar desde la vista
de lista o el formulario; la acción «Reservar» la desactiva. Aceptar una oferta
también ejecuta esa acción. Cambiar la etapa, finalizar un contrato o cancelar un
contrato no actualiza automáticamente la disponibilidad. El filtro «Reservadas»
de la búsqueda realmente filtra propiedades no disponibles, cualquiera que sea
la causa.

### Acciones

- Crear visita: crea una visita para la propiedad, con fecha y usuario responsable
  por defecto, y estado «Borrador».
- Cancelar visitas pendientes: cambia a «Cancelada» las visitas de la propiedad
  en estado «Borrador» o «Programada».
- Crear oferta: crea una oferta por el precio de la propiedad y la pasa
  inmediatamente a «Enviada».
- Aceptar mejor oferta: busca entre las ofertas «Enviadas» de la propiedad la de
  mayor importe y la acepta. Si no hay ninguna, no realiza cambios.
- Eliminar ofertas rechazadas: elimina las ofertas de la propiedad en estado
  «Rechazada».
- Abrir visitas e incidencias: muestra los registros relacionados con la
  propiedad y permite acceder a su lista y formulario.

### Vistas

La acción de propiedades ofrece kanban, lista, pivote, gráfico y formulario. La
lista permite edición múltiple. El kanban agrupa por etapa y muestra nombre,
referencia, categoría, precio, usuario y una marca cuando la propiedad no está
disponible. El pivote y el gráfico permiten analizar el precio por categoría y
usuario.

El formulario organiza los datos en las pestañas Información, Imágenes, Visitas,
Ofertas e Incidencias. Las imágenes, visitas, ofertas e incidencias se gestionan
desde listas relacionadas; las imágenes, ofertas e incidencias admiten edición
en línea. Las visitas usan una lista relacionada editable en línea. Los botones
de las acciones anteriores están en la cabecera del formulario.

## Categorías

Una categoría tiene nombre obligatorio y descripción. Puede seleccionarse en una
propiedad y se muestra también en las ofertas como dato relacionado. Dispone de
vistas de lista y formulario.

## Imágenes de propiedades

Una imagen pertenece a una propiedad y contiene nombre obligatorio, descripción,
archivo de imagen obligatorio y secuencia para ordenar su presentación. Al
eliminar la propiedad, se eliminan sus imágenes relacionadas.

## Visitas

Una visita pertenece obligatoriamente a una propiedad y puede incluir visitante
(contacto), usuario responsable, fecha, teléfono y correo electrónico. La fecha
se inicializa con la fecha y hora actuales, y el estado inicial es «Borrador».
Al seleccionar un contacto, se copian su teléfono y correo electrónico a la
visita; esos campos son datos propios de la visita, no campos relacionados.

### Estados y acciones

- Borrador: estado inicial; se puede programar.
- Programada: indica una visita concertada; se puede marcar como realizada o
  cancelada.
- Realizada: visita completada.
- Cancelada: visita anulada.

Desde el formulario se puede programar, marcar como realizada, cancelar o volver
a borrador. Cada día, una tarea programada cambia a «Realizada» las visitas
«Programadas» cuya fecha ya haya pasado. La cancelación masiva desde la propiedad
solo afecta a las visitas en borrador o programadas.

La acción de visitas ofrece kanban, lista, calendario, pivote, gráfico y
formulario. También se puede gestionar la lista de visitas desde la propiedad.

## Ofertas

Una propiedad puede tener varias ofertas. Cada oferta puede incluir propiedad,
comprador (contacto), importe, fecha, nota y color. La propiedad, el usuario
responsable y la categoría se muestran como datos relacionados; el usuario y la
categoría se obtienen de la propiedad. El estado inicial es «Borrador».

El importe no puede ser negativo. No se exige que el importe, comprador o fecha
estén informados. El nombre visible de una oferta se basa en el comprador.

### Estados y acciones

- Borrador: permite enviar, aceptar o rechazar.
- Enviada: permite aceptar o rechazar. La interfaz la denomina «Enviada»; el
  código no implementa un envío real al propietario.
- Aceptada: reserva la propiedad, desactivando su disponibilidad. Desde el
  formulario se muestra la acción para crear un contrato.
- Rechazada: se puede volver a borrador o eliminar mediante la acción de la
  propiedad.

La acción «Aceptar mejor oferta» de la propiedad selecciona la oferta enviada de
mayor importe; aceptar una oferta en otro estado también está permitido desde el
formulario. No se rechazan automáticamente las demás ofertas ni se impide que se
creen o envíen ofertas para una propiedad no disponible fuera del selector de la
vista de formulario.

La acción de ofertas ofrece kanban, lista, calendario, formulario, pivote y
gráfico. La vista de búsqueda permite filtrar por estado y agrupar por propiedad.

## Contratos

Un contrato vincula una propiedad con un cliente (contacto) e incluye nombre,
tipo, fechas de inicio y fin, renta, depósito y estado. El tipo puede ser venta o
alquiler; por defecto es alquiler. La fecha de inicio se establece por defecto en
el día actual.

La duración se calcula en días cuando existen ambas fechas. «Días hasta el fin»
se calcula respecto a la fecha actual si hay fecha de fin; «Días en curso» se
calcula desde el inicio solo cuando el estado es «En curso». «Tiene depósito» se
activa si el depósito es mayor que cero. Al seleccionar una propiedad, el campo
de renta se inicializa con el precio de dicha propiedad. Se valida que la fecha
de inicio no sea posterior a la fecha de fin, y el nombre del contrato debe ser
único cuando se informa.

### Estados y acciones

- Borrador: estado inicial; se puede pasar a «En curso».
- En curso: se puede finalizar.
- Finalizado: estado de contrato completado.
- Cancelado: estado de contrato cancelado.

El formulario permite volver a borrador y cancelar según las acciones visibles.
Una tarea diaria finaliza los contratos en curso cuya fecha de fin haya llegado.
Hay vistas de lista y formulario. Los contratos se gestionan desde su propio
menú; la ficha de propiedad no tiene una pestaña ni una relación de contratos.

Desde una oferta aceptada, la interfaz permite crear un contrato de venta con la
propiedad y el comprador de la oferta, y fecha de inicio actual. Aunque el botón
solo se muestra para ofertas aceptadas, el método que crea el contrato no
comprueba por sí mismo ese estado.

## Incidencias

Una incidencia pertenece a una propiedad y contiene nombre obligatorio,
descripción, prioridad, estado, fecha y hora de registro y usuario asignado. La
prioridad puede ser baja, media, alta o crítica (por defecto, media). El estado
puede ser nueva, en curso, resuelta o cerrada (por defecto, nueva). Se gestiona
desde la pestaña Incidencias de la propiedad y desde su contador de acceso
rápido. Al eliminar la propiedad, se eliminan sus incidencias relacionadas.

## Acceso

El módulo define los grupos Usuario y Responsable; el grupo Responsable incluye
al grupo Usuario. Los usuarios tienen lectura, creación y modificación, pero no
eliminación, para propiedades, visitas, categorías, ofertas y contratos. Los
responsables también pueden eliminar esos registros. Para las propiedades, los
usuarios ven las asignadas a su usuario o las que no tienen usuario; los
responsables ven todas. Las etapas, imágenes e incidencias tienen permisos de
lectura, creación, modificación y eliminación para los usuarios internos.
