"""
tests/test_validation.py

Pruebas unitarias para el módulo validation.py
"""

import pytest
from returns.result import Success, Failure
from src.validation import validate_transaction
from src.schemas import transaction_schema


def test_validate_transaction_missing_fields():
    """
    Verifica que devuelve Failure si faltan campos obligatorios.
    """
    # Creamos un dict vacío para forzar campos faltantes
    d = {}
    result = validate_transaction(d)
    assert isinstance(result, Failure)
    assert "Missing fields" in result.failure()


def test_validate_transaction_invalid_field(monkeypatch):
    """
    Verifica que devuelve Failure si un campo no pasa la validación.
    """
    # Tomamos un campo del esquema y lo forzamos a fallar
    key = next(iter(transaction_schema.keys()))

    def fake_validator(_):
        return Failure("invalid")

    monkeypatch.setitem(transaction_schema, key, fake_validator)

    d = {k: "dummy" for k in transaction_schema.keys()}
    result = validate_transaction(d)
    assert isinstance(result, Failure)
    assert f"{key} failed" in result.failure()


def test_validate_transaction_success(monkeypatch):
    """
    Verifica que devuelve Success si todos los campos son válidos.
    """
    # Forzamos todos los validadores a devolver Success
    def fake_validator(_):
        return Success("ok")

    for k in transaction_schema.keys():
        monkeypatch.setitem(transaction_schema, k, fake_validator)

    d = {k: "dummy" for k in transaction_schema.keys()}
    result = validate_transaction(d)
    assert isinstance(result, Success)
    assert result.unwrap() == d



