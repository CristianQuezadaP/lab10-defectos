# src/carrito.py
# Sistema Bajo Prueba - Laboratorio 10

def agregar_al_carrito(carrito: list, producto: dict) -> list:
    """Agrega un producto al carrito y retorna la lista actualizada.

    Args:
        carrito: lista de productos ya en el carrito.
        producto: dict con claves 'nombre', 'precio' y 'cantidad'.

    Returns:
        Lista actualizada con el producto añadido.
    """
    if not isinstance(producto.get('precio'), (int, float)) or producto['precio'] < 0:
        raise ValueError('El precio debe ser un número no negativo.')
    if not isinstance(producto.get('cantidad'), int) or producto['cantidad'] < 1:
        raise ValueError('La cantidad debe ser un entero positivo.')
    carrito.append(producto)
    return carrito


def calcular_total(carrito: list) -> float:
    """Calcula el total del carrito sin descuentos.

    Returns:
        Suma de precio × cantidad para cada producto.
    """
    return sum(p['precio'] * p['cantidad'] for p in carrito)


def aplicar_descuento(total: float, porcentaje: float) -> float:
    """Aplica un porcentaje de descuento sobre el total.

    Args:
        total: valor total del carrito (debe ser >= 0).
        porcentaje: valor entre 0 y 100 que representa el % de descuento.

    Returns:
        Total con descuento aplicado. Nunca retorna un valor menor a 0.

    Raises:
        ValueError: si el porcentaje está fuera del rango [0, 100].
    """
    if porcentaje < 0 or porcentaje > 100:
        raise ValueError('El porcentaje debe estar entre 0 y 100.')
    # CORRECCIÓN: se garantiza que el resultado nunca sea negativo.
    # El defecto original permitía totales negativos al combinar precios ya
    # rebajados con cupones de descuento altos (ej. total=1990, descuento=60%
    # producía -796.0). La corrección aplica max(..., 0).
    resultado = total - (total * porcentaje / 100)
    return max(resultado, 0.0)
