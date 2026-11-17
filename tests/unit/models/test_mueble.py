import pytest
from src.models.mueble import Mueble

class TestMueble:
    def test_abstracta(self):
        with pytest.raises(TypeError):
            Mueble("Mesa", "Roble", "Negro", 100)

    def test_metodos_abstractos(self):
        assert Mueble.calcular_precio.__isabstractmethod__
        assert Mueble.obtener_descripcion.__isabstractmethod__

    @pytest.mark.parametrize("atributo,valor", [("nombre", ""), ("material", "  "), ("color", ""), ("precio_base", -1)])
    def test_validaciones(self, silla, atributo, valor):
        with pytest.raises(ValueError):
            setattr(silla, atributo, valor)

    def test_getters_setters(self, silla):
        silla.nombre = "  Nueva silla  "
        silla.material = "Metal"
        silla.color = "Negro"
        silla.precio_base = 150
        assert (silla.nombre, silla.material, silla.color, silla.precio_base) == ("Nueva silla", "Metal", "Negro", 150)
        assert "Nueva silla" in str(silla)
        assert "Mueble" in repr(silla)
