# Lab10 — Gestión de Defectos, Corrección y Elaboración de Informes de Prueba

**Asignatura:** Especialidad I: Calidad de Software  
**Docente:** Camilo Alejandro Fuentes Beals - PhD  
**Universidad Autónoma de Chile — Campus Talca**

## Estructura

```
lab10-defectos/
├── src/
│   └── carrito.py              # SUT v1.0.1 (defecto LAB10-001 corregido)
├── tests/
│   ├── test_carrito.py         # Suite base (9 casos)
│   └── test_carrito_defecto.py # Suite verificación defecto (4 casos parametrizados)
├── docs/
│   ├── REPORTE_DEFECTO.md      # Reporte + RCA del defecto LAB10-001
│   └── INFORME_PRUEBAS.md      # Informe IEEE 829 post-corrección
└── README.md
```

## Ejecutar los tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=src --cov-report=term-missing
```

Resultado esperado: **13 passed, cobertura 100 %**.

## Defecto corregido: LAB10-001

`aplicar_descuento()` permitía retornar totales negativos al combinar un precio ya rebajado con un cupón de descuento alto. Corrección: `return max(resultado, 0.0)`.
