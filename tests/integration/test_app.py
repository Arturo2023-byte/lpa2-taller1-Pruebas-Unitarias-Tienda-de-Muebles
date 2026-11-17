import pytest
from unittest.mock import patch
from src import main
from src.ui.menu import MenuTienda

@pytest.mark.integration
def test_preparacion_catalogo_y_menu(tienda, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *args: "")
    monkeypatch.setattr("src.ui.menu.Confirm.ask", lambda *args, **kwargs: False)
    # Evitar esperas por confirmaciones interactivas

    main.crear_catalogo_inicial(tienda)
    main.crear_comedores_ejemplo(tienda)
    main.aplicar_descuentos_ejemplo(tienda)
    main.mostrar_estadisticas_iniciales(tienda)
    assert tienda.buscar_muebles_por_nombre('Silla')
    menu = MenuTienda(tienda)
    menu.mostrar_banner()
    menu.mostrar_catalogo_completo()
    menu.mostrar_comedores()
    menu.mostrar_estadisticas()
    menu.generar_reporte_interactivo()

@pytest.mark.integration
def test_main_con_menu_simulado(monkeypatch):
    monkeypatch.setattr('builtins.input',lambda *args:'')
    with patch('src.main.MenuTienda.ejecutar') as run:
        main.main()
    run.assert_called_once()

@pytest.mark.integration
def test_menu_vacio(tienda):
    menu = MenuTienda(tienda)
    menu.mostrar_catalogo_completo()
    menu.mostrar_comedores()
    menu._mostrar_lista_muebles([])
    with patch('src.ui.menu.IntPrompt.ask', return_value=0):
        assert menu.mostrar_menu_principal()==0
    with patch('src.ui.menu.IntPrompt.ask', return_value=0):
        menu.ejecutar()

@pytest.mark.integration
def test_busquedas_interactivas(tienda, silla, monkeypatch):
    tienda.agregar_mueble(silla)
    menu = MenuTienda(tienda)
    monkeypatch.setattr('src.ui.menu.time.sleep', lambda _: None)
    with patch('src.ui.menu.Prompt.ask', side_effect=['Silla', 'Inexistente', '', 'Roble', 'Desconocido', '']):
        menu.buscar_muebles_interactivo()
        menu.buscar_muebles_interactivo()
        menu.buscar_muebles_interactivo()
        menu.filtrar_por_material_interactivo()
        menu.filtrar_por_material_interactivo()
        menu.filtrar_por_material_interactivo()
    with patch('src.ui.menu.IntPrompt.ask', side_effect=[0, 0, 200, 300, 500, 200, 0]):
        menu.filtrar_por_precio_interactivo()
        menu.filtrar_por_precio_interactivo()
        menu.filtrar_por_precio_interactivo()

@pytest.mark.integration
def test_ventas_interactivas(tienda, silla, monkeypatch):
    menu = MenuTienda(tienda)
    menu.realizar_venta_interactiva()
    tienda.agregar_mueble(silla)
    with patch('src.ui.menu.IntPrompt.ask', return_value=1), patch('src.ui.menu.Confirm.ask', side_effect=[False, True]), patch('src.ui.menu.Prompt.ask', return_value='Cliente'):
        menu.realizar_venta_interactiva()
        assert tienda.buscar_muebles_por_nombre('Silla')
        menu.realizar_venta_interactiva()
    assert not tienda.buscar_muebles_por_nombre('Silla')

@pytest.mark.integration
def test_descuento_interactivo(tienda):
    menu=MenuTienda(tienda)
    with patch('src.ui.menu.IntPrompt.ask', side_effect=[1, 10]):
        menu.aplicar_descuentos_interactivo()
    assert 'Silla' in tienda._descuentos_activos
