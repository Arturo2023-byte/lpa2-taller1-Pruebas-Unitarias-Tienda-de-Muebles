import pytest
from src.models.composicion.comedor import Comedor
from src.models.concretos.silla import Silla

def test_composicion(comedor, mesa, silla):
    assert comedor.mesa is mesa
    assert len(comedor) == 2
    assert comedor.calcular_precio_total() == pytest.approx(mesa.calcular_precio()+silla.calcular_precio())
    assert "FAMILIAR" in comedor.obtener_descripcion_completa()
    assert isinstance(comedor.obtener_resumen(), dict)
    assert "Familiar" in str(comedor)

def test_agregar_y_quitar(comedor):
    otra = Silla("Extra", "Roble", "Marrón", 100)
    assert "agregada" in comedor.agregar_silla(otra)
    assert len(comedor) == 3
    assert "removida" in comedor.quitar_silla()
    assert "inválido" in comedor.quitar_silla(999)

def test_comedor_vacio(mesa):
    c = Comedor("Vacío", mesa)
    assert "No hay" in c.quitar_silla()
    assert c.calcular_precio_total() == mesa.calcular_precio()

def test_descuento_por_cuatro_sillas(mesa, silla):
    c = Comedor("Cuatro", mesa, [silla]*4)
    esperado = round((mesa.calcular_precio()+4*silla.calcular_precio())*.95,2)
    assert c.calcular_precio_total() == esperado
