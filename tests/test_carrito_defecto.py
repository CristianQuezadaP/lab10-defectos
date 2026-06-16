# tests/test_carrito_defecto.py
import pytest
from src.carrito import aplicar_descuento


@pytest.mark.parametrize('total,porcentaje,esperado_minimo', [
    # (total original, % descuento, valor mínimo aceptable)
    (1990,  60, 0),   # precio ya rebajado 50% + cupón 60% → negativo sin corrección
    (500,   80, 0),   # caso límite: descuento agresivo sobre total bajo
    (1000, 100, 0),   # descuento total: resultado exactamente 0
    (2000,  50, 0),   # 50% exacto → frontera entre positivo y negativo
])
def test_descuento_no_genera_total_negativo(total, porcentaje, esperado_minimo):
    # Arrange
    # (parámetros ya definidos en @parametrize)

    # Act
    resultado = aplicar_descuento(total, porcentaje)

    # Assert
    assert resultado >= esperado_minimo, (
        f'Total con descuento {porcentaje}% sobre {total} fue {resultado}, '
        f'se esperaba >= {esperado_minimo}'
    )
