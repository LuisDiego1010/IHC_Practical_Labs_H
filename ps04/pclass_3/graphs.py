import matplotlib.pyplot as plt
# EJERCICIO A: Impacto de la afinidad de CPU en el tiempo de ejecución
"""
hilos = [1, 2, 4, 8, 10, 12]
tiempo_naive = [2.323, 2.473, 2.761, 3.626, 4.393, 4.984]
tiempo_affinity = [2.415, 2.431, 2.525, 2.749, 3.558, 4.704]

plt.figure(figsize=(10, 6))

plt.plot(hilos, tiempo_naive, marker='o', linestyle='-', color='red', label='CPU-Naive')
plt.plot(hilos, tiempo_affinity, marker='s', linestyle='--', color='blue', label='CPU-Affinity')

plt.title('Ejercicio A: Impacto de la afinidad de CPU en el tiempo de ejecución', fontsize=14)
plt.xlabel('Número de Hilos (p)', fontsize=12)
plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=12)

plt.xticks(hilos)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)

# plt.savefig('ejercicio_a_tiempos.png', dpi=300, bbox_inches='tight')
plt.show()

"""
# EJERCICIO B: Comparación de tiempos de ejecución para Softmax y Matmul Tiled

# 1. Definición de los datos
# p: Número de hilos
hilos = [1, 2, 4, 8, 12]

# Tiempos de ejecución en segundos para OpenMP
tiempo_softmax = [0.600955, 1.596940, 2.173842, 3.120286, 6.178415]
tiempo_matmul = [0.534590, 0.318765, 0.322312, 0.203212, 0.158092]

# 2. Configuración de la figura (dos subgráficas para comparar ambas tareas)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# 3. Gráfica 1: Softmax (Degradación de rendimiento)
ax1.plot(hilos, tiempo_softmax, marker='o', linestyle='-', color='purple', label='softmax_openmp')
ax1.set_title('Ejercicio B: Softmax (OpenMP)', fontsize=13)
ax1.set_xlabel('Número de Hilos (p)', fontsize=11)
ax1.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=11)
ax1.set_xticks(hilos)
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend(fontsize=11)

# 4. Gráfica 2: Matmul Tiled (Escalabilidad positiva)
ax2.plot(hilos, tiempo_matmul, marker='s', linestyle='-', color='green', label='matmul_tiled_openmp')
ax2.set_title('Ejercicio B: Matmul Tiled (OpenMP)', fontsize=13)
ax2.set_xlabel('Número de Hilos (p)', fontsize=11)
ax2.set_ylabel('Tiempo de Ejecución (segundos)', fontsize=11)
ax2.set_xticks(hilos)
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend(fontsize=11)

plt.tight_layout()

# Salida: puedes descomentar la siguiente línea para guardar la imagen
# plt.savefig('ejercicio_b_openmp.png', dpi=300, bbox_inches='tight')
plt.show()