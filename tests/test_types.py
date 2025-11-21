"""
Tests para las utilidades funcionales definidas en types.py:
- compose: composición de funciones
- Result: manejo explícito de éxito/fallo
"""

from src.types import compose, Result

def test_compose_applies_functions_in_order():
    """Verifica que compose aplica funciones en el orden correcto."""
    def double(x):
        return x * 2

    def increment(x):
        return x + 1

    pipeline = compose(double, increment)
    assert pipeline(3) == 7  # (3 * 2) + 1

def test_result_success_map():
    """Aplica map sobre un resultado exitoso."""
    r = Result(10)
    mapped = r.map(lambda x: x * 2)
    assert mapped.is_success()
    assert mapped.unwrap() == 20

def test_result_failure_map():
    """Aplica map sobre un resultado fallido."""
    r = Result(None, is_success=False)
    mapped = r.map(lambda x: x * 2)
    assert mapped.is_failure()
    assert mapped.unwrap() is None

def test_result_map_with_exception():
    """Map lanza excepción y convierte el resultado en fallo."""
    r = Result("abc")
    mapped = r.map(int)  # reemplaza lambda innecesaria
    assert mapped.is_failure()
    assert mapped.unwrap() is None

def test_result_bind_success_chain():
    """Encadena operaciones exitosas con bind."""
    def to_upper(s: str) -> Result[str]:
        return Result(s.upper())

    def add_exclamation(s: str) -> Result[str]:
        return Result(s + "!")

    r = Result("hello")
    chained = r.bind(to_upper).bind(add_exclamation)
    assert chained.is_success()
    assert chained.unwrap() == "HELLO!"

def test_result_bind_failure_chain():
    """Encadena una operación fallida con bind."""
    def fail(_: str) -> Result[str]:  # evita advertencia por argumento no usado
        return Result(None, False)

    r = Result("hello")
    chained = r.bind(fail).bind(lambda x: Result(x + "!"))
    assert chained.is_failure()
    assert chained.unwrap() is None

def test_result_match_success():
    """Match ejecuta la rama de éxito."""
    r = Result(5)
    outcome = r.match(lambda x: x * 2, lambda _: 0)
    assert outcome == 10

def test_result_match_failure():
    """Match ejecuta la rama de fallo."""
    r = Result(None, is_success=False)
    outcome = r.match(lambda x: x * 2, lambda _: 0)
    assert outcome == 0

def test_result_value_or_success():
    """value_or devuelve el valor si es exitoso."""
    r = Result("data")
    assert r.value_or("default") == "data"

def test_result_value_or_failure():
    """value_or devuelve el valor por defecto si falló."""
    r = Result(None, is_success=False)
    assert r.value_or("default") == "default"
