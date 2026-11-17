import pytest
from src.models.concretos.silla import Silla
from src.models.concretos.mesa import Mesa
from src.models.composicion.comedor import Comedor
from src.services.tienda import TiendaMuebles

@pytest.fixture
def silla():
    return Silla("Silla clásica", "Roble", "Marrón", 100)

@pytest.fixture
def mesa():
    return Mesa("Mesa clásica", "Roble", "Marrón", 300)

@pytest.fixture
def comedor(mesa, silla):
    return Comedor("Familiar", mesa, [silla])

@pytest.fixture
def tienda():
    return TiendaMuebles("Tienda de pruebas")
