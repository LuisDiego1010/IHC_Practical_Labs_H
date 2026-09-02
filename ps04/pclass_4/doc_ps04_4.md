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

### Uso de IA
