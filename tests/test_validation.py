"""
tests/test_validation.py

Pruebas unitarias para el módulo validation.py
"""

from returns.result import Success, Failure
from src.validation import validate_transaction


def test_validate_transaction_missing_fields():
    """Verifica que devuelve Failure si faltan campos obligatorios."""
    d = {}
    schema = {
        "Merchant_Country": lambda _: Success("ok"),
        "Channel": lambda _: Success("ok"),
        "Amount": lambda _: Success("ok")
    }
    result = validate_transaction(d, schema)
    assert isinstance(result, Failure)
    assert "Missing fields" in result.failure()


def test_validate_transaction_invalid_field():
    """Verifica que devuelve Failure si un campo no pasa la validación."""
    schema = {
        "Merchant_Country": lambda _: Failure("invalid"),
        "Channel": lambda _: Success("ok"),
        "Amount": lambda _: Success("ok")
    }

    d = {
        "Merchant_Country": "dummy",
        "Channel": "POS",
        "Amount": "123.45"
    }

    result = validate_transaction(d, schema)
    assert isinstance(result, Failure)
    assert "Merchant_Country failed" in result.failure()


def test_validate_transaction_success():
    """Verifica que devuelve Success si todos los campos son válidos."""
    schema = {
        "Merchant_Country": lambda _: Success("ok"),
        "Channel": lambda _: Success("ok"),
        "Amount": lambda _: Success("ok")
    }

    d = {
        "Merchant_Country": "MX",
        "Channel": "POS",
        "Amount": "123.45"
    }

    result = validate_transaction(d, schema)
    assert isinstance(result, Success)
    assert result.unwrap() == d
