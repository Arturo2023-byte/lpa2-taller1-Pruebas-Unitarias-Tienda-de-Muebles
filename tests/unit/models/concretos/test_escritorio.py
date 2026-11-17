import pytest
from src.models.concretos.escritorio import Escritorio

@pytest.fixture
def producto():
    return Escritorio("Ejemplo", "Madera", "Azul", 100)

class TestEscritorio:
    def test_construccion(self, producto):
        assert producto.nombre == "Ejemplo"
        assert producto.material == "Madera"
        assert producto.precio_base == 100

    def test_precio(self, producto):
        assert isinstance(producto.calcular_precio(), (int, float))
        assert producto.calcular_precio() >= 100

    def test_descripcion(self, producto):
        assert "Ejemplo" in producto.obtener_descripcion()

    @pytest.mark.parametrize("precio", [1, 100, 1000])
    def test_varios_precios(self, precio):
        producto = Escritorio("Ejemplo", "Madera", "Azul", precio)
        assert producto.calcular_precio() >= precio
