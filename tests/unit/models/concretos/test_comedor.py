from src.models.concretos.comedor import Comedor

def test_comedor_concreto(mesa,silla):
    c=Comedor(mesa,[silla])
    assert c.cantidad_sillas()==1
    assert c.calcular_precio_total()==mesa.calcular_precio()+silla.calcular_precio()
    assert isinstance(c.descripcion(),str)
    c.agregar_silla(silla)
    assert c.cantidad_sillas()==2
    c.quitar_silla(silla)
    assert c.cantidad_sillas()==1
