import pytest
from unittest.mock import Mock
from src.models.concretos.silla import Silla
from src.services.tienda import TiendaMuebles

def test_agregar_y_buscar(tienda,silla):
    assert "agregado" in tienda.agregar_mueble(silla)
    assert tienda.buscar_muebles_por_nombre("CLÁSICA")==[silla]
    assert tienda.filtrar_por_material(" ROBLE ")==[silla]
    assert tienda.filtrar_por_precio(0,200)==[silla]
    assert tienda.filtrar_por_precio(300,400)==[]
    assert tienda.filtrar_por_material("")==[]
    assert tienda.nombre=="Tienda de pruebas"

def test_errores_con_mock(tienda):
    assert "Error" in tienda.agregar_mueble(None)
    malo=Mock()
    malo.calcular_precio.return_value=0
    assert "Error" in tienda.agregar_mueble(malo)
    malo.calcular_precio.side_effect=RuntimeError("fallo externo")
    assert "fallo externo" in tienda.agregar_mueble(malo)
    assert "Error" in tienda.agregar_comedor(None)

def test_venta_y_descuento(tienda,silla):
    assert "error" in tienda.realizar_venta(silla)
    tienda.agregar_mueble(silla)
    assert "Error" in tienda.aplicar_descuento("sillas",0)
    assert "aplicado" in tienda.aplicar_descuento("sillas",10)
    venta=tienda.realizar_venta(silla,"Ana")
    assert venta["cliente"]=="Ana"
    assert venta["precio_final"]==pytest.approx(silla.calcular_precio()*.9)
    assert tienda.buscar_muebles_por_nombre("Silla")==[]

def test_integracion_comedor(tienda,comedor):
    assert "agregado" in tienda.agregar_comedor(comedor)
    assert isinstance(tienda.generar_reporte_inventario(),str)
    assert isinstance(tienda.obtener_estadisticas(),dict)
