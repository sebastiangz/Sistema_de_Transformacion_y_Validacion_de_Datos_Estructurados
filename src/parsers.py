"""
parsers.py

Contiene clases y funciones para construir parsers funcionales que procesan texto de forma segura.
"""

from typing import Callable, Tuple, Any
from returns.result import Success, Failure

class Parser:
    """
    Clase base para construir parsers funcionales.
    """
    def __init__(self, fn: Callable[[str], Tuple[Any, str]]):
        self.parse = fn

    def __call__(self, text: str):
        """
        Ejecuta el parser sobre el texto dado.

        Args:
            text (str): Texto de entrada.

        Returns:
            Success(resultado) si el parseo es exitoso.
            Failure(mensaje) si ocurre un error.
        """
        try:
            return Success(self.parse(text))
        except ValueError as e:
            return Failure(str(e))

    def map(self, fn: Callable[[Any], Any]) -> 'Parser':
        """
        Aplica una transformación al resultado del parser.

        Args:
            fn (Callable): Función que transforma el resultado.

        Returns:
            Parser: Nuevo parser con la transformación aplicada.
        """
        return Parser(lambda txt: (fn(self.parse(txt)[0]), self.parse(txt)[1]))

def char(c: str) -> Parser:
    """
    Parser que consume un carácter específico.

    Args:
        c (str): Carácter esperado.

    Returns:
        Parser: Parser que valida y consume ese carácter.
    """
    def parse(t: str) -> Tuple[str, str]:
        if t and t[0] == c:
            return t[0], t[1:]
        raise ValueError(f"Expected '{c}'")
    return Parser(parse)

def digit() -> Parser:
    """
    Parser que consume un dígito.

    Returns:
        Parser: Parser que valida y consume un dígito.
    """
    def parse(t: str) -> Tuple[str, str]:
        if t and t[0].isdigit():
            return t[0], t[1:]
        raise ValueError("Expected digit")
    return Parser(parse)
