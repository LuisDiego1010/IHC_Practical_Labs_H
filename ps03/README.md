# PS03

Este directorio contiene el **laboratorio práctico de la semana 3**, enfocado en comprender el impacto de las **instrucciones SIMD** sobre el rendimiento de un programa.

## Autor

**Luis Diego García Rojas**

## Ejercicios

### Ejercicio A

Multiplicación de vectores de punto flotante utilizando intrinsics de AVX2.

La multiplicación se realiza con `_mm256_mul_ps`, que permite multiplicar 8 valores `float` al mismo tiempo utilizando un registro de 256 bits.

```c
static inline __m256 simd_mul_ps(__m256 a, __m256 b)
{
    return _mm256_mul_ps(a, b);
}
```

### Ejercicio B

Reducción de un vector de punto flotante a un único valor mediante la suma de sus elementos.

Primero se separa el registro de 256 bits en dos registros de 128 bits. Luego se suman ambas mitades y se realizan sumas horizontales hasta obtener un único valor.

```c
static inline float simd_reduce_add_ps(__m256 value)
{
    __m128 low = _mm256_extractf128_ps(value, 0);
    __m128 high = _mm256_extractf128_ps(value, 1);

    __m128 sum = _mm_add_ps(low, high);

    sum = _mm_hadd_ps(sum, sum);
    sum = _mm_hadd_ps(sum, sum);

    return _mm_cvtss_f32(sum);
}
```

### Ejercicio C

Implementación de la multiplicación de matrices utilizando las operaciones vectorizadas desarrolladas en los ejercicios A y B.

Para calcular el producto punto se procesan 8 elementos por iteración. Se cargan ambos vectores, se multiplican utilizando la función del ejercicio A y luego se reducen utilizando la función del ejercicio B.

```c
float dot_product_avx2(const float a[VECTOR_SIZE], const float b[VECTOR_SIZE])
{
    float result = 0.0f;

    for (int i = 0; i < VECTOR_SIZE; i += AVX_FLOATS) {
        __m256 vec_a = simd_loadu_ps(&a[i]);
        __m256 vec_b = simd_loadu_ps(&b[i]);

        __m256 vec_mul = simd_mul_ps(vec_a, vec_b);

        result += simd_reduce_add_ps(vec_mul);
    }

    return result;
}
```

Antes de realizar la multiplicación se transpone la matriz `B`, de manera que sus columnas queden almacenadas de forma contigua en memoria y puedan utilizarse directamente para realizar los productos punto.

```c
void transpose_matrix_1024(
    const float matrix[MATRIX_SIZE][MATRIX_SIZE],
    float transposed[MATRIX_SIZE][MATRIX_SIZE])
{
    for (int row = 0; row < MATRIX_SIZE; ++row) {
        for (int col = 0; col < MATRIX_SIZE; ++col) {
            transposed[col][row] = matrix[row][col];
        }
    }
}
```

Finalmente, cada elemento de la matriz resultado se obtiene mediante el producto punto entre una fila de `A` y una fila de la matriz `B` transpuesta.

```c
void matrix_multiply_avx2_1024(
    const float a[MATRIX_SIZE][MATRIX_SIZE],
    const float b[MATRIX_SIZE][MATRIX_SIZE],
    float result[MATRIX_SIZE][MATRIX_SIZE])
{
    static float b_transposed[MATRIX_SIZE][MATRIX_SIZE];

    transpose_matrix_1024(b, b_transposed);

    for (int row = 0; row < MATRIX_SIZE; ++row) {
        for (int col = 0; col < MATRIX_SIZE; ++col) {
            result[row][col] = dot_product_avx2(a[row], b_transposed[col]);
        }
    }
}
```

## Ejercicio D — Análisis de rendimiento

Se ejecutaron las versiones escalar y AVX2 con una repetición.

### Resultados

| Implementación | Tiempo (s) | Rendimiento (GFLOP/s) |
| -------------- | ---------: | --------------------: |
| Scalar         |   4.136654 |              4.153083 |
| AVX2           |   2.482045 |              6.921658 |

Las dos implementaciones obtuvieron el mismo checksum:

```text
86972906452.000000
```

Esto permite verificar que ambas versiones producen el mismo resultado.

### Speedup

El speedup se calcula como:

```text
Speedup = Tiempo Scalar / Tiempo AVX2
```

Utilizando los tiempos obtenidos:

```text
Speedup = 4.136654 / 2.482045 ≈ 1.67
```

Por lo tanto, la versión AVX2 fue aproximadamente **1.67 veces más rápida**.

La razón principal es que AVX2 utiliza SIMD y puede trabajar con varios valores `float` al mismo tiempo. Como sus registros son de 256 bits y cada `float` tiene 32 bits, puede procesar hasta 8 valores `float` juntos.

Sin embargo, esto no significa que el programa completo sea 8 veces más rápido, ya que también existen accesos a memoria, cargas de datos, reducciones y otras operaciones que no se vectorizan completamente. Por esta razón, el speedup obtenido es menor.
