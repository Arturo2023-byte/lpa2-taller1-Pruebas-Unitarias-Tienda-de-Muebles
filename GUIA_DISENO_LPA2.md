# LPA2 - Informe tecnologico oscuro con Bootstrap

## Archivos creados

- `htmlcov/bootstrap-5.3.6.min.css`: copia local de Bootstrap 5.3.6 (MIT).
- `htmlcov/lpa2-dark.css`: reglas propias, documentadas por secciones y declaraciones.
- `htmlcov/*.html`: todos los reportes conservan su estructura y scripts originales, con estilos nuevos.
- `GUIA_DISENO_LPA2.md`: esta guia para conservar el disenio.

## Como abrir

1. Descomprimir el ZIP y abrir `lpa2-taller1-main` en Visual Studio Code.
2. Abrir `htmlcov/index.html` con el navegador (doble clic o extensiones de VS Code).
3. Usar **Files**, **Functions**, **Classes**, ordenar columnas, filtrar y abrir archivos.
4. Abrir `htmlcov/class_index.html` para ver la cobertura por clases.

Bootstrap es local: no hace falta internet. No se requiere JavaScript de Bootstrap
porque las tarjetas, columnas y barras usan unicamente clases CSS de Bootstrap.
El JavaScript de `coverage.py` se mantiene intacto.

## Cuidado al regenerar cobertura

La carpeta `htmlcov` se reconstruye con `pytest --cov=src --cov-report=html`.
Al hacerlo, coverage.py puede reemplazar los HTML y eliminar estos cambios visuales.
Para aplicar de nuevo el tema sobre el nuevo reporte, ejecuta desde la raiz:

    python aplicar_tema_lpa2.py

El script conserva la tabla y extrae los valores del nuevo reporte. No altera
el codigo fuente de la tienda ni su conjunto de pruebas.

## Publicacion en GitHub

Se desactivo la regla `htmlcov/` del `.gitignore` raiz y el patron `*` dentro de `htmlcov/.gitignore` para que Git incluya el informe. Tras regenerar con coverage.py, revisa nuevamente ambos archivos `.gitignore`. Antes de hacer commit, revisa los cambios.

## Verificaciones

- Las cifras visibles provienen del propio informe preexistente.
- Los archivos Python y de tests no se modificaron con el redisenio.
- El CSS original y el JS original de coverage.py tampoco se modificaron.
- La cantidad de pruebas y la cobertura deben verificarse de nuevo al ejecutar pytest
  en el entorno local correspondiente.
