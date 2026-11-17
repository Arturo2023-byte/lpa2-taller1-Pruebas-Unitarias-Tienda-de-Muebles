import pytest
from src.models.categorias.almacenamiento import Almacenamiento
from src.models.categorias.asientos import Asiento
from src.models.categorias.superficies import Superficie
from src.models.concretos.mesa import Mesa
from src.models.concretos.silla import Silla

@pytest.mark.parametrize("cls", [Almacenamiento,Asiento,Superficie])
def test_categorias_abstractas(cls):
    assert bool(cls.__abstractmethods__)

@pytest.mark.parametrize("atributo,valor", [("largo",0),("ancho",-1),("altura",0)])
def test_superficie_invalida(mesa, atributo, valor):
    with pytest.raises(ValueError):
        setattr(mesa,atributo,valor)

def test_superficie_calculos(mesa):
    assert mesa.calcular_area()>0
    assert mesa.calcular_factor_tamaño()>0
    assert "Mesa" in mesa.obtener_info_superficie() or isinstance(mesa.obtener_info_superficie(),str)
    mesa.largo=200
    mesa.ancho=100
    mesa.altura=80
    assert mesa.largo==200

def test_mesa_capacidad_y_forma(mesa):
    mesa.forma="redonda"
    mesa.capacidad_personas=6
    assert mesa.forma=="redonda"
    assert mesa.capacidad_personas==6
    with pytest.raises(ValueError):
        mesa.capacidad_personas=0
