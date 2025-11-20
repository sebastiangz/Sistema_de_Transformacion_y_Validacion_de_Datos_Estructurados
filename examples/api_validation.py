"""
api_validation.py

Valida transacciones recibidas como payloads de una API.
Usa la lógica de validation.py y devuelve respuestas listas para API.
"""

from typing import Dict, Any
from returns.result import Success, Failure
from src.validation import validate_transaction
from src.transforms import transform_transaction


def validate_api_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida un payload de transacción recibido por API.

    Args:
        payload (dict): Datos de la transacción.

    Returns:
        dict: Respuesta con estado y datos o error.
    """
    # Aplica transformaciones antes de validar
    transformed = transform_transaction(payload)

    result = validate_transaction(transformed)
    if isinstance(result, Success):
        return {"status": "success", "data": result.unwrap()}
    else:
        return {"status": "failure", "error": result.failure()}


