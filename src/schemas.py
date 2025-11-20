# src/schemas.py

from returns.result import Success, Failure
from datetime import datetime
from typing import Any

class PositiveFloat:
    """
    Valida que el valor sea un float positivo.
    """
    def __call__(self, v: Any):
        try:
            v = float(v)
            return Success(v) if v > 0 else Failure("Amount must be positive")
        except ValueError:
            return Failure("Invalid float")

class DateValidator:
    """
    Valida que la fecha tenga uno de los formatos aceptados.
    """
    def __init__(self, fmt: str = '%m/%d/%Y %H:%M'):
        self.fmts = [fmt, '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S']

    def __call__(self, v: Any):
        for f in self.fmts:
            try:
                datetime.strptime(str(v), f)
                return Success(v)
            except ValueError:
                continue
        return Failure(f"Date must match one of: {self.fmts}")

class CountryWhitelist:
    """
    Valida que el país esté en la lista permitida.
    """
    def __init__(self, allowed: list[str]):
        self.allowed = allowed

    def __call__(self, v: Any):
        return Success(v) if v in self.allowed else Failure(f"Country {v} not allowed")

transaction_schema: dict[str, Any] = {
    'Transaction_ID': str,
    'Card_ID': str,
    'Timestamp': DateValidator('%m/%d/%Y %H:%M'),
    'Amount': PositiveFloat(),
    'Merchant_City': str,
    'Merchant_Country': CountryWhitelist(['IN', 'GB', 'US', 'AE', 'MX', 'CA', 'SG']),
    'Latitude': float,
    'Longitude': float,
    'Device_ID': str,
    'Channel': str,
    'Entry_Mode': str,
    'Auth_Method': str,
    'Merchant_Category': str,
    'Transaction_Status': str
}
