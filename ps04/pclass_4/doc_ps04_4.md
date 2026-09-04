## Práctica de Clase 4: Bibliotecas dinámicas y estáticas en C

Este directorio contiene el laboratorio práctico 4, enfocado en comprender el impacto de utilizar bibliotecas estáticas, bibliotecas dinámicas y funciones inline sobre el desempeño en tiempo de ejecución y el tamaño final de un programa en C.

### Entorno de pruebas

* **Sistema Operativo:** Ubuntu 24.04.2 LTS
* **Kernel:** 7.0.0-30-generic
* **Procesador:** 12th Gen Intel(R) Core(TM) i5-12450H
* **Arquitectura:** x86_64
* **Topología NUMA:** 1 Nodo
* **Núcleos:** 8 núcleos físicos / 12 hilos lógicos
* **Memoria RAM:** 15 GiB
* **Caché (L1d / L2 / L3):** 320 KiB / 7 MiB / 12 MiB

---

### Resultados Ejercicios A y B: Biblioteca Estática vs. Dinámica

| Versión | fill A (µs/iter) | fill B (µs/iter) | add (µs/iter) | Tiempo Total (s) | Tamaño Archivo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Estática** (`bench-static`) | 369.555 | 418.020 | 1443.418 | ~2.23 | 1.8 K (`libvectorops.a`) |
| **Dinámica** (`bench-dynamic`) | 961.917 | 1001.733 | 1562.130 | ~3.53 | 16 K (`libvectorops.so`) |

---

### Análisis de Rendimiento

Al observar los resultados, se evidencian diferencias notorias en los tiempos de ejecución. La versión dinámica tarda considerablemente más que la estática, pasando de ~2.23 a ~3.53 segundos en su tiempo total. Esta penalización también se refleja claramente en los tiempos de las funciones `fill A` y `fill B`, donde la versión dinámica tarda más del doble: de ~369 µs aumenta a ~961 µs por iteración, y de ~418 µs a ~1001 µs.

Esta diferencia de rendimiento radica en cómo se gestionan las llamadas a memoria. En la versión estática, el código de las funciones se copia directamente dentro del ejecutable, logrando que las llamadas sean directas y muy rápidas. Sin embargo, en la versión dinámica, el ejecutable depende de un archivo externo. Esto obliga al programa a buscar y resolver la dirección de memoria de esa función en plena ejecución, añadiendo latencia cada vez que el ciclo itera.

Finalmente, al analizar el tamaño de los archivos generados, se nota que la biblioteca estática es mucho más ligera (1.8 K), mientras que la dinámica tiene un tamaño significativamente mayor (16 K). Básicamente, el archivo `.a` es un empaquetado puro del código objeto. En contraste, el archivo `.so` necesita incluir estructuras adicionales en su interior, como tablas de símbolos dinámicos y metadatos, para poder ser enlazado correctamente por el sistema operativo en tiempo de ejecución.

---

### Uso de IA
* **Herramienta utilizada:** Google Gemini.
* **Propósito:** Apoyo en la estructuración de explicaciones teóricas y depuración del análisis de rendimiento.
* **Enlace de la sesión:** [https://share.gemini.google/sD7BX1QcDxUL](https://share.gemini.google/sD7BX1QcDxUL)