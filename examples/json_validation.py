"""
json_validation.py

Carga y valida transacciones desde un archivo JSON usando el esquema definido en validation.py.
"""

import json
from typing import List, Dict
from returns.result import Success, Failure
from src.validation import validate_transaction


def load_json(path: str) -> List[Dict]:
    """
    Carga un archivo JSON que contiene una lista de transacciones.

    Args:
        path (str): Ruta al archivo JSON.

    Returns:
        List[Dict]: Lista de transacciones.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_json_transactions(path: str) -> Dict[str, List]:
    """
    Valida todas las transacciones en un archivo JSON.

    Args:
        path (str): Ruta al archivo JSON.

    Returns:
        Dict[str, List]: Diccionario con listas de transacciones válidas y errores.
    """
    transactions = load_json(path)
    valid: List[Dict] = []
    errors: List[str] = []

    for tx in transactions:
        result = validate_transaction(tx)
        if isinstance(result, Success):
            valid.append(result.unwrap())
        else:
            errors.append(result.failure())

    return {"valid": valid, "errors": errors}
