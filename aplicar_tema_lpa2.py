"""Reaplica el tema Bootstrap a los HTML que genera pytest-cov.

No modifica archivos de Python dentro de src/ ni archivos de pruebas.
Solo actualiza la presentacion estatica de la carpeta htmlcov/.
"""
from pathlib import Path
import re

REPORTES = Path(__file__).resolve().parent / "htmlcov"

# Una hoja de coverage se mantiene entre las otras dos hojas CSS:
# Bootstrap aporta la cuadricula, coverage conserva su comportamiento visual
# principal, y lpa2-dark.css personaliza los colores del reporte.
BLOQUE_CSS = '''    <!-- Bootstrap local para tarjetas, columnas y barras de progreso. -->
    <link rel="stylesheet" href="bootstrap-5.3.6.min.css" type="text/css">
    <!-- Hoja de estilos original de coverage.py. -->
    <link rel="stylesheet" href="__COVERAGE_STYLESHEET__" type="text/css">
    <!-- Apariencia oscura propia del taller LPA2. -->
    <link rel="stylesheet" href="lpa2-dark.css" type="text/css">'''

TITULOS = {
    "index.html": ("Cobertura por archivo", "Consulta la cobertura de cada modulo de la tienda de muebles."),
    "function_index.html": ("Cobertura por funcion", "Identifica funciones que necesitan escenarios de prueba adicionales."),
    "class_index.html": ("Cobertura por clase", "Explora el comportamiento cubierto de las clases y sus metodos."),
}


def tarjeta(nombre: str, valor: str, detalle: str, cobertura: float | None = None) -> str:
    """Crea una tarjeta responsive usando exclusivamente clases CSS de Bootstrap."""
    barra = ""
    if cobertura is not None:
        barra = (f'<div class="progress" role="progressbar" aria-label="Cobertura" '
                 f'aria-valuenow="{round(cobertura)}" aria-valuemin="0" aria-valuemax="100">'
                 f'<div class="progress-bar" style="width: {cobertura}%"></div></div>')
    acento = " accent" if cobertura is not None else ""
    return (f'<div class="col-12 col-md-6 col-xl-3"><div class="card lpa-stat h-100">'
            f'<div class="card-body"><span class="lpa-stat-label">{nombre}</span>'
            f'<div class="lpa-stat-value{acento}">{valor}</div>'
            f'<span class="lpa-stat-note">{detalle}</span>{barra}</div></div></div>')


def resumen(origen: str, titulo: str, descripcion: str) -> str:
    """Extrae los indicadores existentes sin inventar datos ni ejecutar pruebas."""
    # Se recupera la fila Total ya calculada por coverage.py.
    coincidencia = re.search(r'<tr class="total">(.*?)</tr>', origen, re.S)
    if not coincidencia:
        raise ValueError("No se encontro la fila Total del reporte")
    celdas = re.findall(r'<td\b[^>]*>.*?</td>', coincidencia.group(1), re.S)
    datos = [re.sub(r'<[^>]+>', '', celda).strip() for celda in celdas]
    porcentajes = re.findall(r'data-ratio="(\d+) (\d+)"', coincidencia.group(1))
    if len(datos) < 12 or not porcentajes:
        raise ValueError("La tabla de coverage.py no tiene el formato esperado")
    cubierto, total = map(int, porcentajes[-1])
    porcentaje = 100 * cubierto / total if total else 100.0
    tarjetas = "\n    ".join([
        tarjeta("Cobertura total", f"{porcentaje:.2f} %", "Meta academica: al menos 80 %", porcentaje),
        tarjeta("Sentencias analizadas", datos[3], "Instrucciones registradas por coverage.py"),
        tarjeta("Sentencias no cubiertas", datos[4], "Oportunidades de nuevas pruebas"),
        tarjeta("Ramas analizadas", datos[8], "Decisiones detectadas por el reporte"),
    ])
    return f'''<!-- Panel nuevo: se muestra antes de la tabla original; no sustituye el reporte. -->
<section class="lpa-overview container-fluid" aria-labelledby="lpa-title">
  <!-- Encabezado academico para ubicar al lector. -->
  <div class="lpa-eyebrow">LPA2 / Taller 1 / Quality assurance</div>
  <h2 id="lpa-title" class="lpa-heading">{titulo}</h2>
  <p class="lpa-description">{descripcion} Panel construido con Bootstrap 5 y CSS personalizado, manteniendo el informe de pytest-cov.</p>
  <!-- La clase row y las columnas col-* proceden de Bootstrap. -->
  <div class="row g-3 mb-3">
    {tarjetas}
  </div>
  <!-- Aviso que diferencia datos historicos de una ejecucion nueva. -->
  <div class="lpa-info"><strong>Informe conservado:</strong> el filtro, la ordenacion por columnas, los enlaces de navegacion y la tabla original siguen funcionando. Los valores corresponden al reporte ya generado y no se actualizan hasta volver a ejecutar las pruebas.</div>
</section>
<!-- Fin del panel visual. -->
'''


def aplicar() -> None:
    """Anade estilos y paneles una sola vez aunque se ejecute repetidamente."""
    if not (REPORTES / "bootstrap-5.3.6.min.css").exists():
        raise FileNotFoundError("Falta Bootstrap local dentro de htmlcov")
    if not (REPORTES / "lpa2-dark.css").exists():
        raise FileNotFoundError("Falta lpa2-dark.css dentro de htmlcov")
    total = 0
    for archivo in sorted(REPORTES.glob("*.html")):
        contenido = archivo.read_text(encoding="utf-8")
        # Evita duplicar el panel al ejecutar el script sobre un reporte ya modificado.
        if 'class="lpa-overview' in contenido:
            contenido = re.sub(r'<!-- Resumen visual:.*?<!-- Fin del resumen visual\. -->\s*', '', contenido, flags=re.S)
            contenido = re.sub(r'<!-- Panel nuevo:.*?<!-- Fin del panel visual\. -->\s*', '', contenido, flags=re.S)
        # Se borran solo los enlaces y comentarios agregados por este tema, si existen.
        contenido = re.sub(r'\s*<!-- Bootstrap local[^\n]*-->\s*', '\n', contenido)
        contenido = re.sub(r'\s*<!-- Estilos personalizados[^\n]*-->\s*', '\n', contenido)
        contenido = re.sub(r'\s*<!-- Apariencia oscura[^\n]*-->\s*', '\n', contenido)
        contenido = re.sub(r'\s*<!-- Hoja de estilos original[^\n]*-->\s*', '\n', contenido)
        contenido = re.sub(r'\s*<link rel="stylesheet" href="(?:bootstrap-5\.3\.6\.min\.css|lpa2-dark\.css)" type="text/css">', '', contenido)
        # El nombre de la hoja de coverage.py cambia cuando se regenera htmlcov.
        # Buscamos la referencia efectiva en este HTML para no depender de un hash fijo.
        patron_css = r'<link\s+rel=["\']stylesheet["\']\s+href=["\'](style_cb_[^"\']+\.css)["\']\s+type=["\']text/css["\']\s*/?>'
        coincidencia_css = re.search(patron_css, contenido)
        if not coincidencia_css:
            raise ValueError(f"No se encontro la hoja de coverage.py en {archivo.name}")
        nombre_css = coincidencia_css.group(1)
        if not (REPORTES / nombre_css).is_file():
            raise FileNotFoundError(f"Falta el CSS original: {nombre_css}")
        # Bootstrap carga primero, luego coverage, y por ultimo nuestros estilos.
        bloque_css = BLOQUE_CSS.replace("__COVERAGE_STYLESHEET__", nombre_css)
        contenido = contenido[:coincidencia_css.start()] + bloque_css.strip() + contenido[coincidencia_css.end():]
        if archivo.name in TITULOS:
            titulo, descripcion = TITULOS[archivo.name]
            contenido = contenido.replace('<main id="index">', resumen(contenido, titulo, descripcion) + '<main id="index">', 1)
        archivo.write_text(contenido, encoding="utf-8")
        total += 1
    print(f"Tema oscuro instalado en {total} paginas HTML.")

if __name__ == '__main__':
    aplicar()
