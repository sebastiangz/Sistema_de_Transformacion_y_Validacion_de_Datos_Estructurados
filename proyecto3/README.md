
# Proyecto 3: Sistema de Transformación y Validación de Datos Estructurados

**Materia:** Programación Funcional  
**Proyecto académico:** ejemplo original inspirado en los requisitos proporcionados.
Responsabilidad individual – Aron Ulises

Área: Limpieza y transformación de datos.

Me encargaré de implementar y mejorar funciones puras para limpiar y transformar información, eliminar espacios innecesarios, normalizar nombres y aplicar composición de funciones.

También realizaré pruebas para comprobar que las transformaciones funcionen correctamente.

Archivos a mi cargo:

- "src/transforms.py"
- "src/sanitizers.py"

## Objetivo
Validar, limpiar y transformar registros estructurados JSON, CSV y XML mediante funciones puras, composición, resultados tipo Either (Success/Failure), valores tipo Maybe (Some/Nothing), combinadores de parsers y un pipeline estilo railway-oriented.

## Requisitos
- Python 3.11 o superior.
- El núcleo **no necesita instalar librerías externas**.
- `requirements.txt` contiene librerías opcionales de la temática del curso; no son necesarias para ejecutar el programa.

## Cómo ejecutar (desde la carpeta principal)

```bash
python run_pipeline.py data/usuarios.json
python run_pipeline.py data/usuarios.csv
python run_pipeline.py data/usuarios.xml
python run_pipeline.py data/usuarios_invalidos.json
python run_pipeline.py data/usuarios.json --salida resultado.json
```

En Windows, si `python` no funciona, probar `py`.

## Pruebas
```bash
python run_tests.py
```

Opcional, si se instaló pytest:
```bash
python -m pytest tests/ -v
```

## Estructura
- `src/types.py`: Success, Failure, Some y Nothing.
- `src/schemas.py`: esquema de usuario.
- `src/validation.py`: reglas de campos y validación.
- `src/sanitizers.py`: limpieza de espacios sin mutación.
- `src/transforms.py`: transformaciones y composición.
- `src/parsers.py`: lectores JSON, CSV, XML y combinadores.
- `src/pipeline.py`: flujo de procesamiento con errores controlados.
- `data/`: archivos de ejemplo.
- `tests/`: pruebas automáticas.
- `docs/`: explicación de arquitectura.
- `examples/`: ejemplo sencillo.

## Reglas de usuario
- `name`: texto obligatorio.
- `email`: correo válido obligatorio.
- `age`: entero entre 18 y 120.
- `tags`: lista opcional de textos.

## Funcionamiento
1. Se lee un archivo y se interpreta según su extensión.
2. Se limpian espacios de forma recursiva.
3. Se convierte la edad textual numérica (CSV/XML) a entero.
4. Se valida el esquema y se acumulan mensajes de error.
5. Si es válido, se transforma el nombre a mayúsculas, el correo a minúsculas y las etiquetas a minúsculas.
6. Se imprime el resultado o se informa el error sin modificar el objeto original.

## Limitaciones y ampliaciones
- XML admite registros sencillos sin atributos ni elementos anidados complejos.
- La validación usa un esquema declarativo propio, sin integrar directamente Pydantic o JSON Schema.
- Los combinadores de parser son básicos (`map_parser`, `then`).
- Para un sistema productivo agregar validaciones de seguridad, límites de tamaño y modelos de datos específicos.
