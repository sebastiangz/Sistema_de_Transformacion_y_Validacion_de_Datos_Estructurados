"""
types.py

Utilidades funcionales:
composición de funciones y clase Result para manejar éxito o fallo explícitamente.
"""

from typing import Callable, TypeVar, Generic, Optional

T = TypeVar('T')
U = TypeVar('U')

def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    """
    Composición funcional: aplica funciones en orden sobre un valor.
    """
    def f(x: T) -> T:
        for fn in functions:
            x = fn(x)
        return x
    return f

class Result(Generic[T]):
    """
    Representa un resultado que puede ser exitoso o fallido.
    """
    def __init__(self, value: Optional[T], is_success: bool = True):
        self._value: Optional[T] = value
        self._is_success: bool = is_success

    def map(self, fn: Callable[[T], U]) -> 'Result[Optional[U]]':
        """
        Aplica una función al valor si es exitoso.
        """
        if self._is_success and self._value is not None:
            try:
                return Result(fn(self._value))
            except (ValueError, TypeError):
                return Result(None, False)
        return Result(None, False)

    def bind(self, fn: Callable[[T], 'Result[U]']) -> 'Result[Optional[U]]':
        """
        Encadena otra operación que devuelve un Result.
        """
        if self._is_success and self._value is not None:
            result = fn(self._value)
            return Result(result.unwrap(), result.is_success())
        return Result(None, False)

    def match(self, s: Callable[[T], U], f: Callable[[Optional[T]], U]) -> U:
        """
        Ejecuta una función según el estado del resultado.
        """
        if self._is_success and self._value is not None:
            return s(self._value)
        return f(self._value)

    def is_success(self) -> bool:
        """
        Indica si el resultado fue exitoso.
        """
        return self._is_success

    def is_failure(self) -> bool:
        """
        Indica si el resultado fue fallido.
        """
        return not self._is_success

    def unwrap(self) -> Optional[T]:
        """
        Devuelve el valor interno, sea exitoso o fallido.
        """
        return self._value

    def value_or(self, default: T) -> T:
        """
        Devuelve el valor si es exitoso, o el valor por defecto si falló.
        """
        return self._value if self._is_success and self._value is not None else default
