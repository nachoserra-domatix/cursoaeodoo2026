En este commit:

CODIGO:
 - Seguimos reorganizando el código, y arregalando algunos comentarios (los XML los habia comentado por error con #)
 - No toco código por mi cuenta para seguir siempre las indicaciones del profesor y no implementar nada imprevisto que pudiera entrar en conflicto con las tareas de clase

DOCUMENTACION
 - Empiezo a crear una serie de documentos para llevar un mejor control y entendimiento del modulo, que empieza a crecer mucho. He dejado que el Agente de Copilot (usando GPT-6 Luna) revisara el código y me propusiera los contenidos
   - **README.md:** ¿Qué es lo que hace la aplicacion?
   - **SPECIFICATION.md:** Especificación funcional de cada modelo
   - **DATA_MODEL.md:** Modelo de datos, para llevar control de relaciones (ER) y herencias
   - **BUSINESS RULES.md:** Reglas a tener en cuenta como que una propiedad debe dejar de aparecer como disponible si su estado pasa a Reservada, Vendida o Alquilada
   - **BUGS.md:** Errores que se encuentran en el funcionamiento del módulo, como, por ejemplo, que en este momento la regla de negocio anteriormente indicada no se esta cumpliendo
   - **TODO.md:** Lista de cosas que hay que ir haciendo, a veces para corregir un bug, a veces para añadir funcionalidades (nuevas o descritas en las 'business rules). Óptimamente se debería usar algo como BDD (Behavior-Driven Development), o FDD (Behavior-Driven Development). Pero ni hay tiempo de expresar todo en Gherkin ni de implementar un 'backlog' de historias de uduario con criterios de aceptacion.
 - Los 'BUGS' y 'TODO' indicados veré si trabajar en ellos, para, como ya comenté, no interferir con el desarrollo de las clases
 - NOTA: Los bugs encontrados no son resultados de errores de programación, sino que 