
Para encontrar la ruta mas corta entre dos estaciones, se debe ejecutar lo siguiente en la ruta de los archivos adjuntos:

```
python3 main.py path_archivo_red estacion_inicial estacion_final [color_tren]
```

El color del tren es opcional, y debe ser `red` o `green`. 

Por ejemplo, para encontrar la ruta entre las estaciones `A` y `F` en una red definida en el archivo `network.txt`, en un tren de color rojo, se debe ejecutar lo siguiente:

```
python3 main.py network.txt A F red
```

Mientras que, para encontrar la ruta en un tren sin color, se debe ejecutar lo siguiente:

```
python3 main.py network.txt A F
```


Finalmente, el archivo que define la red esta organizado de la siguiente forma:

**Primero**, tantas filas como estaciones existan, cada una de la forma `nombre_estacion,color_estacion`. El color debe ser `red`, `green` o `white` (esta ultima para estaciones sin color).
**Segundo**, una linea en blanco.
**Tercero**, tantas filas como conexiones entre estaciones existan, cada una de la forma `nombre_estacion_1,nombre_estacion_2`.

Se adjunta como ejemplo el archivo correspondiente a la red del enunciado del problema.