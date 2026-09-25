## Práctica de Clase 6: Introducción a la programación en CUDA

Este directorio contiene el laboratorio práctico 6, enfocado en expresar paralelismo masivo en GPU mediante tres patrones básicos de paralelismo de datos: suma de vectores, producto punto y *softmax*. En cada ejercicio se practica el manejo explícito de memoria entre CPU y GPU, el lanzamiento de *kernels*, el cálculo de índices con `blockIdx`, `blockDim` y `threadIdx`, y el uso de memoria compartida para reducciones.

### Entorno de pruebas

* **Sistema Operativo:** Ubuntu 24.04.2 LTS
* **Procesador:** 12th Gen Intel(R) Core(TM) i5-12450H
* **GPU:** NVIDIA GeForce GTX 1650 (4 GiB, arquitectura Turing, *compute capability* 7.5)
* **Driver NVIDIA:** 595.91.07 (soporta hasta CUDA 13.2)
* **CUDA Toolkit:** 13.4 (`nvcc` V13.4.92)

---

### Ejercicio A: Suma de vectores

#### 1. Completar el kernel

Se completó `vector_add_kernel` con la línea:

```cuda
c[i] = a[i] + b[i];
```

#### 2. Índice global del hilo

El índice global del hilo se calcula con:

```cuda
int i = blockIdx.x * blockDim.x + threadIdx.x;
```

Tal como se vio en el modelo SIMT, todos los hilos ejecutan el mismo *kernel* y lo único que los diferencia es su índice. De la siguiente manera:

* `threadIdx.x` indica la posición del hilo dentro de su bloque.
* `blockDim.x` es la cantidad de hilos por bloque.
* `blockIdx.x` es el número de bloque dentro del *grid*.

Entonces `blockIdx.x * blockDim.x` da el primer elemento que le corresponde a ese bloque, y al sumarle `threadIdx.x` se obtiene la posición exacta del hilo. Por ejemplo, con bloques de 256 hilos, el hilo 3 del bloque 2 obtiene 2·256 + 3 = 515 y calcula `C[515]`. Así cada hilo tiene un índice único y, entre todos, cubren del 0 al N−1 sin repetir ni dejar huecos.

#### 3. Condición `i < n`

Como la cantidad de bloques se calcula con redondeo hacia arriba, `blocks = (n + 255) / 256`, en caso de que `n` no sea múltiplo de 256 el último bloque tiene hilos cuyo índice es mayor o igual que `n`. Sin la condición, esos hilos leerían y escribirían fuera de los arreglos, lo que puede corromper memoria o provocar un error de acceso ilegal.

#### 4. Compilación y ejecución

```
$ make clean
$ make
$ make run
./vector_add 1048576
vector-add n=1048576: OK
```

#### Preguntas

**1. ¿Cuántos bloques se lanzan cuando N=1048576 y cada bloque tiene 256 hilos?**

(1048576 + 255) / 256 = 4096 bloques. La división es exacta, así que se lanzan 1 048 576 hilos, uno por elemento, y ninguno sobra.

**2. ¿Qué ocurre si N no es múltiplo del tamaño del bloque?**

El redondeo hacia arriba lanza un bloque adicional que queda parcialmente ocupado. Los hilos sobrantes de ese bloque tienen un índice mayor o igual que `n`, pero gracias a la condición `i < n` no hacen nada, por lo que el resultado sigue siendo correcto.

**3. ¿Qué transferencias de memoria ocurren entre CPU y GPU?**

El programa usa memoria controlada: la GPU tiene un espacio de memoria separado, así que se reserva con `cudaMalloc` y los datos se copian de forma explícita con `cudaMemcpy`. En el programa pasa lo siguiente:

1. La CPU crea los vectores `A` y `B` en la RAM.
2. Se copian `A` y `B` a la GPU, básicamente porque la GPU no los puede leer desde la RAM.
3. La GPU calcula `C = A + B` en su propia memoria.
4. Se copia `C` de vuelta a la CPU, para que la CPU pueda revisar si el resultado es correcto.

---

### Ejercicio B: Producto punto

#### 1. Producto local

Cada hilo calcula el producto de su elemento cuando el índice es válido:

```cuda
value = a[i] * b[i];
```

#### 2. Reducción en memoria compartida

Dentro de cada bloque, los productos se suman por mitades hasta que la suma parcial del bloque queda en `cache[0]`:

```cuda
cache[tid] += cache[tid + stride];
```

#### 3. Papel de `__syncthreads()`

`__syncthreads()` hace que todos los hilos de un bloque se esperen entre sí en ese punto. Es necesario porque los hilos no avanzan todos al mismo ritmo, y en la reducción cada hilo usa valores que escribieron otros hilos en la memoria compartida. Sin la sincronización, un hilo podría leer un valor antes de que otro lo haya escrito y el resultado saldría mal.

#### 4. Compilación y ejecución

```
$ make run N=1048576
./dot_product 1048576
dot-product n=1048576: gpu=-21.250000 cpu=-21.250000 error=0.000000 OK
$ make run N=4194304
./dot_product 4194304
dot-product n=4194304: gpu=-0.500000 cpu=-0.500000 error=0.000000 OK
```

#### Preguntas

**1. ¿Por qué este ejercicio no puede resolverse solamente escribiendo un valor independiente por hilo?**

Porque el resultado final es un solo número que depende de todos los elementos del vector. Cada hilo calcula su propio `a[i]·b[i]`, pero luego todos esos productos se tienen que sumar, y para ello los hilos guardan sus productos en memoria compartida y los van sumando entre ellos hasta obtener una suma parcial por bloque. Al final, la CPU suma las sumas parciales de todos los bloques.

**2. ¿Cuántos valores parciales se copian de GPU a CPU?**

Uno por bloque:

| N | Valores parciales |
| :---: | :---: |
| 1048576 | 1048576 / 256 = 4096 |
| 4194304 | 4194304 / 256 = 16384 |

**3. ¿Qué pasaría si se elimina alguna sincronización dentro de la reducción?**

Habría hilos leyendo valores de la memoria compartida antes de que otros hilos los hayan escrito, y sumarían datos incorrectos. El resultado saldría mal y podría cambiar de una ejecución a otra.

---

### Ejercicio C: Softmax

#### 1. Implementación

* Máximo de la fila: cada hilo busca el máximo entre sus columnas con `fmaxf`, y luego se reduce en memoria compartida con `cache[tid] = fmaxf(cache[tid], cache[tid + stride])`.
* Exponenciales desplazadas: cada hilo calcula `expf(input[idx] - row_max)`, lo guarda en `output[idx]` y lo acumula en `local_sum`.
* Suma de exponenciales: se reduce igual que en el producto punto, con `cache[tid] += cache[tid + stride]`.
* Normalización: cada elemento se divide entre la suma de la fila, `output[idx] /= row_sum`.

Además se agregó un `__syncthreads()` después de leer `row_max = cache[0]`. Sin esta barrera, el hilo 0 podría escribir su suma parcial en `cache[0]` y sobrescribir el máximo antes de que los demás hilos lo leyeran.

#### 2. Compilación y ejecución

```
$ make run
./softmax 128 1024
softmax rows=128 cols=1024: OK
$ make run ROWS=256 COLS=2048
./softmax 256 2048
softmax rows=256 cols=2048: OK
```

#### Preguntas

**1. ¿Por qué se calcula primero el máximo de cada fila?**

Porque la exponencial de un número grande puede desbordarse y dar infinito. Al restar el máximo, todos los exponentes quedan en 0 o menos, así que las exponenciales quedan entre 0 y 1. El resultado final no cambia, porque esa resta se cancela al dividir entre la suma.

**2. ¿Qué partes del algoritmo requieren cooperación entre hilos del mismo bloque?**

Encontrar el máximo de la fila y sumar las exponenciales. En ambos casos cada hilo solo conoce sus columnas, así que los hilos tienen que combinar sus valores en memoria compartida con una reducción. En cambio, calcular las exponenciales y normalizar lo hace cada hilo por su cuenta.

**3. ¿Qué limitación tiene usar un solo bloque por fila cuando `cols` crece mucho?**

Un bloque puede tener como máximo 1024 hilos, así que si la fila es muy larga cada hilo tiene que procesar muchas columnas una tras otra, y se pierde paralelismo.

---

### Uso de IA
* **Herramienta utilizada:** Google Gemini.
* **Propósito:** Apoyo en estructura y formato.
* **Enlace de la sesión:** [https://share.gemini.google/b6eamsf9IoYN](https://share.gemini.google/b6eamsf9IoYN)