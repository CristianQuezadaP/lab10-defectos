# Informe de Resumen de Pruebas - Extracto IEEE 829

---

## 1. Identificador del informe

| Campo | Valor |
|-------|-------|
| **Código** | IRP-LAB10-001 |
| **Versión del SUT** | 1.0.1 (post-corrección del defecto LAB10-001) |
| **Alcance** | Módulo `src/carrito.py` — ciclo completo de detección, corrección y verificación del defecto LAB10-001 |
| **Fecha** | 2025-06-16 |

---

## 2. Resumen de variaciones del plan

No se registraron desviaciones respecto al plan original. Todos los tests planificados en `test_carrito.py` (suite base) y `test_carrito_defecto.py` (suite de verificación del defecto) fueron ejecutados en su totalidad. No hubo casos bloqueados ni postponed.

**Adición no planificada:** Se incorporó `test_carrito_defecto.py` como artefacto nuevo durante el ciclo de corrección (Tarea 2), lo que incrementó la cobertura de la función `aplicar_descuento()` para el escenario de valor negativo, ausente en la suite original.

---

## 3. Resumen de actividades

| Elemento | Detalle |
|----------|---------|
| **Herramientas** | pytest 9.1.0, pytest-cov 7.1.0 |
| **Entorno** | Python 3.12.3, Linux Ubuntu 24.04 |
| **Módulos bajo prueba** | `src/carrito.py` (3 funciones: `agregar_al_carrito`, `calcular_total`, `aplicar_descuento`) |
| **Tiempo de ejecución** | 0.08 s (13 tests) |
| **Archivos de test** | `tests/test_carrito.py` (9 casos), `tests/test_carrito_defecto.py` (4 casos parametrizados) |

---

## 4. Resultados — resumen de casos

| Tipo de prueba | Ejecutados | Aprobados | Fallidos | Bloqueados | % Aprobación |
|----------------|:----------:|:---------:|:--------:|:----------:|:------------:|
| Unitarias — suite base (`test_carrito.py`) | 9 | 9 | 0 | 0 | 100 % |
| Unitarias — verificación defecto (`test_carrito_defecto.py`) | 4 | 4 | 0 | 0 | 100 % |
| **TOTAL** | **13** | **13** | **0** | **0** | **100 %** |

> Nota: Los 4 casos parametrizados fallaban con el SUT original (v1.0.0) y pasan con la versión corregida (v1.0.1), confirmando tanto la detección como la corrección del defecto LAB10-001.

---

## 5. Métricas

### DRE — Defect Removal Efficiency

```
DRE = Defectos hallados antes del release ÷ (Defectos antes + Defectos después) × 100
    = 1 ÷ (1 + 0) × 100
    = 100 %
```

**Justificación del denominador:** Se considera `defectos_post_release = 0` porque el test parametrizado `test_carrito_defecto.py` fue creado durante el ciclo de corrección y habría sido integrado al pipeline de CI antes del release, capturando el defecto automáticamente. Por tanto, el defecto LAB10-001 no habría llegado a producción. Un DRE del 100 % indica un proceso de pruebas maduro para este ciclo.

### Densidad de defectos

```
Densidad = N° de defectos ÷ KLOC
         = 1 defecto ÷ 0.014 KLOC   (14 líneas de código ejecutable en carrito.py)
         ≈ 71.4 defectos / KLOC
```

> La densidad alta se explica por el tamaño muy reducido del módulo (14 líneas). En módulos de mayor tamaño este valor se normaliza significativamente.

### % de casos aprobados

```
% Aprobación = Casos aprobados ÷ Casos ejecutados × 100
             = 13 ÷ 13 × 100
             = 100 %
```

### Tasa de reapertura

```
Tasa de reapertura = Defectos reabiertos ÷ Defectos corregidos × 100
                   = 0 ÷ 1 × 100
                   = 0 %
```

La corrección fue validada en primera instancia sin necesidad de reapertura, lo que indica que el análisis de causa raíz (RCA) fue preciso y la corrección atacó la causa real del defecto.

---

## 6. Evaluación general

**El módulo `carrito.py` v1.0.1 está listo para integrarse a la rama principal.**

Justificación basada en métricas:

- **DRE = 100 %**: el defecto fue detectado y corregido antes del release gracias al test parametrizado incorporado al pipeline.
- **% Aprobación = 100 %**: todos los casos —incluyendo los de regresión— pasan sin errores tras la corrección.
- **Tasa de reapertura = 0 %**: la corrección (`max(resultado, 0.0)`) resolvió el defecto en una sola iteración, sin introducir regresiones en la suite existente.
- **Cobertura de código = 100 %** (reportada por pytest-cov): todas las líneas y ramas del módulo están cubiertas por los tests.

El único indicador que merece atención futura es la **densidad de defectos** (71.4 / KLOC), que refleja la pequeña superficie del módulo actual. A medida que el módulo crezca con nuevas funcionalidades, se recomienda mantener la práctica de redactar tests parametrizados para valores límite y escenarios de frontera.

---

## 7. Aprobaciones

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Responsable QA | Estudiante Lab10 | _(firma)_ | 2025-06-16 |
| Docente revisor | Camilo A. Fuentes Beals | _(firma)_ | — |
