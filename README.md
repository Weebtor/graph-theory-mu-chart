# graph-theory-mu-chart
Trabajo de teoría de grafos sobre MU charts en videojuegos

## Eliminación de hojas generalizada (GLR) es un proceso iterativo
Como el orden de complejidad de fuerza bruta es demasiado grande
### Regla 1: 
Si un vértice i no tiene padre se marca ocupado y sus hijos cómo observados.
### Regla 2: 
Si un vértice j tiene solo un padre k y no tiene hijos, k se marca ocupado y sus hijos cómo observados.
### Regla 3: 
Si un vértice l está ocupado y tiene un único hijo m, se elimina la arista que une l y m


## Como implementar GLR a nuestro problema
* Debido a la naturaleza de nuestro grafo y las suposiciones de nuestro problema, se tiene que ningun personaje no puede ser dominado.
* Esto implica que no se puede aplicar ninguna de las reglas de GLR de forma directa, por lo que hay que adaptar un poco lo que es el algoritmo.
* A partir de esto se debe elegir un vertice de forma arbitraria, marcarlo como dominante y eliminar todas las aristas relacionadas.
* Hay que aplicar este proceso de forma iterativa hasta que se le pueda aplicar algunas de las reglas de lo que es GLR.


* Ademas como el objetivo es encontrar todos los MDS, hay que considerar de que hay que iterar sobre diferentes posibles instancias y en base a las reglas de GLR se debe determinar que elementos son atractivos.


####

###############
Repo flex reponer productos en puestos de ventas
Administrar a los reponedores de productos para 
hacer un sitio web de
plan de reposición -> lo ingresa al sistema ->
ticket = peticiones de los clientes en el sitio web (en este caso el gerente de algo)
ticket tiene multiples acciones
    sacar foto


la web se encarga de crear tickets
    candelarizar (especificaciones)

-> genera tareas

Tareas

los tickets vienen en listas

el gestor del cliente debe visualisar el resultado