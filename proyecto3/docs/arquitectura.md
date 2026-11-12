# Arquitectura y conceptos funcionales

## Pipeline
Archivo -> Parser -> Sanitización -> Conversión -> Validación -> Transformación -> Resultado

## Funciones puras
`sanitize_input`, `uppercase_name`, `normalize_email` y `normalize_tags` producen valores nuevos sin modificar sus argumentos.

## Composición
`compose(f, g)(x)` equivale a `f(g(x))`. `pipe(x, f, g)` equivale a `g(f(x))`.

## Either / railway-oriented
`Success(valor)` continúa el proceso con `.map()` o `.bind()`. `Failure(errores)` detiene las transformaciones siguientes. `.match()` permite tratar ambos casos sin ramificaciones externas.

## Maybe
`Some(valor)` y `Nothing()` representan la presencia o ausencia de un valor opcional.

## Parser combinators
`map_parser(parser, funcion)` transforma un resultado correcto. `then(parser, funcion)` encadena parsers que devuelven Success o Failure.

## Pattern matching
El proyecto incluye los tipos Success y Failure, que también pueden utilizarse con `match/case` en Python 3.11+:

```python
from src.types import Success, Failure
match resultado:
    case Success(value):
        print('Éxito:', value)
    case Failure(errors):
        print('Errores:', errors)
```
