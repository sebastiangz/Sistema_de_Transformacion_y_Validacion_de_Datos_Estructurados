# src/validation.py

from returns.result import Success, Failure
from src.schemas import transaction_schema

def validate_transaction(d: dict):
    """
    Valida un diccionario de datos de transacción según el esquema definido.

    Args:
        d (dict): Diccionario con los datos de una transacción.

    Returns:
        Success(d) si todos los campos son válidos.
        Failure(str) con el motivo si hay errores.
    """
    missing = [k for k in transaction_schema if k not in d]
    if missing:
        return Failure(f"Missing fields: {missing}")

    for k, validator in transaction_schema.items():
        result = validator(d[k])
        if isinstance(result, Failure):
            return Failure(f"{k} failed: {result.failure()}")
    return Success(d)
