import pytest

@pytest.mark.integration
def test_flujo_completo(tienda,mesa,silla,comedor):
    tienda.agregar_mueble(silla)
    tienda.agregar_mueble(mesa)
    tienda.agregar_comedor(comedor)
    assert len(tienda.buscar_muebles_por_nombre("Silla"))==1
    venta=tienda.realizar_venta(silla,"Comprador")
    assert venta["precio_final"]>0
    assert len(tienda.buscar_muebles_por_nombre("Silla"))==0
    assert len(tienda.buscar_muebles_por_nombre("Mesa"))==1
