
## Práctica de Clase 3: Programación de Sistemas Multiprocesador (Multihilos y Afinidad)
Este directorio contiene el laboratorio práctico 3, enfocado en comprender el impacto de la organización física de un computador, específicamente el uso de alineamiento de memoria, multihilos y afinidad de CPU, sobre el rendimiento de un programa.

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
### Ejercicio A: Afinidad de CPU

| Hilos ($p$) | Tiempo `cpu-naive` ($T_p$) en segundos | Tiempo `cpu-affinity` ($T_p$) en segundos |
| :---: | :---: | :---: |
| **1** | 2.323 | 2.415 |
| **2** | 2.473 | 2.431 |
| **4** | 2.761 | 2.525 |
| **8** | 3.626 | 2.749 |
| **10** | 4.393 | 3.558 |
| **12** | 4.984 | 4.704 |

---

### Ejercicio B: OpenMP (Softmax)

| Hilos ($p$) | Tiempo `softmax_openmp` (s) |
| :---: | :---: |
| **1** | 0.600955 |
| **2** | 1.596940 |
| **4** | 2.173842 |
| **8** | 3.120286 |
| **12** | 6.178415 |

---

### Ejercicio B: OpenMP (Matmul Tiled)

| Hilos ($p$) | Tiempo `matmul_tiled_openmp` (s) |
| :---: | :---: |
| **1** | 0.534590 |
| **2** | 0.318765 |
| **4** | 0.322312 |
| **8** | 0.203212 |
| **12** | 0.158092 |
---

### Análisis de Rendimiento

### Uso de IA