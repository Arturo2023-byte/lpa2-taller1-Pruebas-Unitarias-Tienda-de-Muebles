import pytest
from src.models.concretos.sofacama import SofaCama
from src.models.concretos.sofa import Sofa
from src.models.concretos.cama import Cama

def test_herencia_multiple():
    s = SofaCama("Dos usos", "Tela", "Gris", 500)
    assert isinstance(s, Sofa) and isinstance(s, Cama)
    assert s.calcular_precio() > 500
    assert s.modo_actual == "sofa"
    assert isinstance(s.convertir_a_cama(), str)
    assert s.modo_actual == "cama"
    assert isinstance(s.convertir_a_sofa(), str)
    assert s.modo_actual == "sofa"
    assert isinstance(s.obtener_capacidad_total(), dict)
    assert "Dos usos" in str(s)

@pytest.mark.parametrize("tamano,mecanismo", [("queen", "hidraulico"), ("king", "electrico"), ("individual", "plegable")])
def test_variantes(tamano, mecanismo):
    s = SofaCama("S", "T", "C", 500, tamaño_cama=tamano, mecanismo_conversion=mecanismo)
    assert s.calcular_precio() > 500
