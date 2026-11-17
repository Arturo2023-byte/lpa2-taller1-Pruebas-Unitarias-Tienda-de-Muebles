import pytest
from src.models.concretos.silla import Silla

@pytest.mark.parametrize("respaldo,tapizado,esperado", [(False,None,1.0),(True,None,1.1),(True,"cuero",1.3),(True,"tela",1.2)])
def test_factor_comodidad(respaldo,tapizado,esperado):
    silla = Silla("S", "M", "N", 100, respaldo, tapizado)
    assert silla.calcular_factor_comodidad() == pytest.approx(esperado)

def test_altura_y_ruedas():
    s = Silla("S", "M", "N", 100, altura_regulable=True, tiene_ruedas=True)
    assert s.calcular_precio() == pytest.approx(160)
    assert "ajustada" in s.regular_altura(60)
    assert "entre" in s.regular_altura(101)
    s.altura_regulable = False
    assert "no tiene" in s.regular_altura(60)
    s.tiene_ruedas = False
    assert s.tiene_ruedas is False
    assert isinstance(s.es_silla_oficina(), bool)

def test_capacidad_invalida(silla):
    with pytest.raises(ValueError):
        silla.capacidad_personas = 0
    silla.tiene_respaldo = False
    silla.material_tapizado = "tela"
    assert "tela" in silla.obtener_info_asiento().lower()
