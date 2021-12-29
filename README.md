# graph-theory-mu-chart

  Proyecto semestral Grafos y Algoritmos

## Integrantes

* Lino Cisternas
* Pablo Muñoz
* Victor Sanchez

## Forma de Uso

* Desde la carpeta base crear el entorno virtual e instalar los requerimientos.
  * `pip install -r requirements.txt`
* Finalizada la instalacion de librerias, ejecutar el archivo `main.py` ubicado en la carpeta `src` e incluir en la terminal el modo a utilizar junto a la ruta del dataset.
* Los modos disponibles son:
  * -Fb para Fuerza bruta.
  * -Ts para Búsqueda en árbol.
  * -A para utilizar ambos modos.
  * -P para generar una imagen del grafo a partir del matchup chart.
* Los dataset tienen tamaños de:
  * `10-1.csv` incluye 10 personajes.
  * `16-char-sf2.csv` incluye 16 personajes extraidos de Street Fighter 2.
  * `17-char-gg.csv` incluye 17 personajes extraidos de Guilty Gear.
  * `84-char-smash.csv` incluye 84 personajes extraidos de Smash Bros.
  * `100.csv` incluye 100 personajes.
  * `150.csv` incluye 150 personajes.
  * `200.csv` incluye 200 personajes.
  * `455.csv` incluye 455 personajes.
* De esta forma si se desea ejecutar el modo por fuerza bruta con un dataset de tamaño 10 el comando sera:
  * `python src/main.py -A datasets/10-1.csv`
