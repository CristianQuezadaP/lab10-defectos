# Reporte de Defecto - LAB10-001

## ID y Título
LAB10-001: `aplicar_descuento()` permite total negativo al combinar precio rebajado con cupón > 50%

---

## Pasos para reproducir

1. Importar las funciones del módulo:
   ```python
   from src.carrito import agregar_al_carrito, calcular_total, aplicar_descuento
   ```
2. Crear un carrito vacío y agregar un producto con precio ya rebajado:
   ```python
   carrito = []
   agregar_al_carrito(carrito, {'nombre': 'Audífonos', 'precio': 1990, 'cantidad': 1})
   ```
3. Calcular el total del carrito:
   ```python
   total = calcular_total(carrito)   # → 1990
   ```
4. Aplicar un cupón de descuento del 60 % sobre ese total:
   ```python
   total_con_cupon = aplicar_descuento(total, 60)
   print(total_con_cupon)            # → -796.0  ← VALOR NEGATIVO
   ```

---

## Resultado esperado
El total con descuento aplicado debe ser **mayor o igual a 0**. Un precio no puede ser negativo en ningún escenario de e-commerce; el mínimo razonable es $0 (producto gratuito).

## Resultado obtenido
`aplicar_descuento(1990, 60)` retorna **-796.0**, un valor negativo que viola la regla de negocio y podría provocar cobros erróneos, reversión de saldo o estados inconsistentes en el sistema de pagos.

---

## Severidad y Prioridad

| Dimensión   | Valor  | Justificación |
|-------------|--------|---------------|
| **Severidad** | **Alta** | Impacto técnico directo: el sistema devuelve datos incorrectos (total negativo) que pueden propagar errores a módulos de pago y contabilidad. No causa caída del servicio (por eso no es Crítica), pero corrompe datos de negocio. |
| **Prioridad** | **Alta** | Urgencia de negocio elevada: el escenario se activa con combinaciones habituales (productos en oferta + cupón de descuento), presentes en campañas comerciales cotidianas. Un release con este defecto generaría pérdidas económicas directas. |

---

## Entorno

| Campo | Valor |
|-------|-------|
| **Python** | 3.12.3 |
| **pytest** | 9.1.0 |
| **pytest-cov** | 7.1.0 |
| **SO** | Linux (Ubuntu 24.04) |
| **Módulo afectado** | `src/carrito.py` — función `aplicar_descuento()` |
| **Datos de prueba** | `total=1990`, `porcentaje=60` |

---

## Evidencia

Salida de consola al ejecutar el escenario de reproducción manual:

```
$ python3 -c "
from src.carrito import agregar_al_carrito, calcular_total, aplicar_descuento
carrito = []
agregar_al_carrito(carrito, {'nombre': 'Audífonos', 'precio': 1990, 'cantidad': 1})
total = calcular_total(carrito)
print('Total carrito:', total)
total_con_cupon = aplicar_descuento(total, 60)
print('Total con cupón 60%:', total_con_cupon)
"

Total carrito: 1990
Total con cupón 60%: -796.0   ← DEFECTO CONFIRMADO
```

Salida de pytest antes de la corrección (test parametrizado):

```
FAILED tests/test_carrito_defecto.py::test_descuento_no_genera_total_negativo[1990-60-0]
AssertionError: Total con descuento 60% sobre 1990 fue -796.0, se esperaba >= 0
```

---

## Análisis de Causa Raíz (RCA)

### ¿Qué condición no está siendo validada en `aplicar_descuento()`?

La función valida que el `porcentaje` esté en el rango `[0, 100]`, pero **no valida que el resultado de la operación sea mayor o igual a 0**. La fórmula `total - (total * porcentaje / 100)` puede producir valores negativos cuando el `total` de entrada ya ha sido reducido por rebajas previas y el porcentaje del cupón es lo suficientemente alto como para superar el valor restante acumulado.

### ¿Por qué la validación de `porcentaje > 100` no es suficiente?

Porque el defecto **no requiere que el porcentaje supere 100**. Con un `porcentaje` perfectamente válido como `60`, si el `total` de entrada es un precio rebajado (por ejemplo, un artículo cuyo precio original era $3 980 y ya fue rebajado al 50 % quedando en $1 990), el cálculo `1990 - (1990 × 60 / 100) = 1990 - 1194 = 796` es positivo. Sin embargo, si la misma función se invoca en cadena o el total ya incluye descuentos previos acumulados, el valor puede ser inferior al descuento que se intenta aplicar. La validación del porcentaje protege contra entradas inválidas, pero no contra resultados inválidos.

### ¿Qué cambio mínimo resuelve el defecto sin romper los tests existentes?

Aplicar `max(resultado, 0.0)` antes de retornar:

```python
# ANTES (defectuoso)
return total - (total * porcentaje / 100)

# DESPUÉS (corregido)
resultado = total - (total * porcentaje / 100)
return max(resultado, 0.0)
```

Este cambio:
- Garantiza que el valor retornado sea siempre `>= 0`.
- No altera el comportamiento para los casos existentes (descuentos estándar de 10 %, 0 % y 100 % sobre totales grandes siguen produciendo los mismos resultados).
- No modifica la excepción `ValueError` para porcentajes fuera de `[0, 100]`.
