"""TDD: pruebas escritas antes de implementar los métodos pendientes."""
import pytest
from unittest.mock import Mock
from src.models.concretos.silla import Silla
from src.models.concretos.mesa import Mesa


def test_filtrar_muebles_por_tipo(tienda, silla, mesa):
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)
    assert tienda.obtener_muebles_por_tipo(Silla) == [silla]
    assert tienda.obtener_muebles_por_tipo(Mesa) == [mesa]


def test_inventario_vacio(tienda):
    assert tienda.calcular_valor_inventario() == 0


def test_valor_inventario_incluye_comedores(tienda, silla, comedor):
    tienda.agregar_mueble(silla)
    tienda.agregar_comedor(comedor)
    esperado = silla.calcular_precio() + comedor.calcular_precio_total()
    assert tienda.calcular_valor_inventario() == pytest.approx(esperado)


def test_valor_inventario_omite_error_de_precio(tienda):
    mueble = Mock()
    mueble.calcular_precio.side_effect = RuntimeError('Error de cálculo')
    tienda._inventario.append(mueble)
    assert tienda.calcular_valor_inventario() == 0
