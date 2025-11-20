"""
csv_processing.py

Carga y procesa transacciones desde un archivo CSV usando transforms y validation.
"""

import csv
from typing import List, Dict
from returns.result import Success
from src.transforms import transform_transaction
from src.validation import validate_transaction

def load_csv(path: str) -> List[Dict]:
    """
    Carga un archivo CSV y devuelve una lista de diccionarios.

    Args:
        path (str): Ruta al archivo CSV.

    Returns:
        List[Dict]: Lista de transacciones como diccionarios.
    """
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def process_csv_transactions(path: str) -> Dict[str, List]:
    """
    Procesa y valida todas las transacciones en un archivo CSV.

    Args:
        path (str): Ruta al archivo CSV.

    Returns:
        Dict[str, List]: Diccionario con listas de transacciones válidas y errores.
    """
    transactions = load_csv(path)
    valid: List[Dict] = []
    errors: List[str] = []

    for tx in transactions:
        transformed = transform_transaction(tx)
        result = validate_transaction(transformed)
        if isinstance(result, Success):
            valid.append(result.unwrap())
        else:
            errors.append(result.failure())

    return {"valid": valid, "errors": errors}
