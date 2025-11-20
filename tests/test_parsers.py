"""
tests/test_parsers.py

Pruebas unitarias para el módulo parsers.py
"""

from returns.result import Success, Failure
from src.parsers import char, digit


def test_char_success():
    """Verifica que char consume correctamente el carácter esperado."""
    parser = char('A')
    result = parser("ABC")
    assert isinstance(result, Success)
    value, rest = result.unwrap()
    assert value == 'A'
    assert rest == "BC"


def test_char_failure():
    """Verifica que char falla si el carácter no coincide."""
    parser = char('X')
    result = parser("ABC")
    assert isinstance(result, Failure)
    assert "Expected 'X'" in result.failure()


def test_digit_success():
    """Verifica que digit consume correctamente un dígito."""
    parser = digit()
    result = parser("9abc")
    assert isinstance(result, Success)
    value, rest = result.unwrap()
    assert value == '9'
    assert rest == "abc"


def test_digit_failure():
    """Verifica que digit falla si el primer carácter no es un dígito."""
    parser = digit()
    result = parser("abc")
    assert isinstance(result, Failure)
    assert "Expected digit" in result.failure()


def test_parser_map_success():
    """Verifica que map transforma el resultado exitoso."""
    parser = digit().map(int)
    result = parser("7xyz")
    assert isinstance(result, Success)
    value, rest = result.unwrap()
    assert value == 7
    assert rest == "xyz"


def test_parser_map_failure():
    """Verifica que map propaga el fallo si el parser falla."""
    parser = digit().map(int)
    result = parser("abc")
    assert isinstance(result, Failure)
    assert "Expected digit" in result.failure()
