"""
validation.py

Este módulo valida transacciones contra un esquema definido.
Utiliza validadores que devuelven Success o Failure usando returns.result.
"""

from typing import Optional, Dict, Any
from returns.result import Success, Failure
from src.schemas import transaction_schema

def validate_transaction(d: Dict[str, Any], schema: Optional[Dict[str, Any]] = None):
    """
    Valida una transacción contra el esquema dado.

    Args:
        d (dict): Transacción a validar.
        schema (dict, optional):
        Esquema de validación. Si no se proporciona, se usa transaction_schema.

    Returns:
        Success(dict) si es válida, Failure(str) si hay errores.
    """
    if schema is None:
        schema = transaction_schema

    missing = [k for k in schema if k not in d]
    if missing:
        return Failure(f"Missing fields: {missing}")

    for k, validator in schema.items():
        result = validator(d[k])
        if isinstance(result, Failure):
            return Failure(f"{k} failed: {result.failure()}")
    return Success(d)
