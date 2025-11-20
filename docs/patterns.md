"""
transaction_pipeline.py

Proyecto unificado que incluye parsers, transformaciones, validación,
procesamiento desde JSON y CSV, y validación estilo API.
"""

import json
import csv
from datetime import datetime
from typing import Callable, Tuple, Any, Dict, List
from returns.result import Success, Failure

# -------------------------------
# PARSERS
# -------------------------------

class Parser:
    def __init__(self, fn: Callable[[str], Tuple[Any, str]]):
        self.parse = fn

    def __call__(self, text: str):
        try:
            return Success(self.parse(text))
        except ValueError as e:
            return Failure(str(e))

    def map(self, fn: Callable[[Any], Any]) -> 'Parser':
        return Parser(lambda txt: (fn(self.parse(txt)[0]), self.parse(txt)[1]))

def char(c: str) -> Parser:
    def parse(t: str) -> Tuple[str, str]:
        if t and t[0] == c:
            return t[0], t[1:]
        raise ValueError(f"Expected '{c}'")
    return Parser(parse)

def digit() -> Parser:
    def parse(t: str) -> Tuple[str, str]:
        if t and t[0].isdigit():
            return t[0], t[1:]
        raise ValueError("Expected digit")
    return Parser(parse)

# -------------------------------
# TRANSFORMACIONES
# -------------------------------

def normalize_country(d: dict) -> dict:
    country_map = {
        "Mexico": "MX",
        "Brazil": "BR",
        "Argentina": "AR"
    }
    d["Merchant_Country"] = country_map.get(d.get("Merchant_Country", ""), d.get("Merchant_Country", ""))
    return d

def enrich_channel(d: dict) -> dict:
    channel_type = {
        "POS": "Presencial",
        "ONLINE": "Digital"
    }
    d["Channel_Type"] = channel_type.get(d.get("Channel", ""), "Desconocido")
    return d

def add_timestamp(d: dict) -> dict:
    d["Processed_At"] = datetime.utcnow().isoformat()
    return d

def transform_transaction(d: dict) -> dict:
    d = normalize_country(d)
    d = enrich_channel(d)
    d = add_timestamp(d)
    return d

# -------------------------------
# VALIDACIÓN
# -------------------------------

def amount_validator(value: str):
    try:
        float(value)
        return Success(value)
    except ValueError:
        return Failure("Amount must be a number")

def country_validator(value: str):
    if value in {"MX", "BR", "AR"}:
        return Success(value)
    return Failure("Invalid country code")

def channel_validator(value: str):
    if value in {"POS", "ONLINE"}:
        return Success(value)
    return Failure("Invalid channel")

transaction_schema = {
    "Merchant_Country": country_validator,
    "Channel": channel_validator,
    "Amount": amount_validator
}

def validate_transaction(d: dict):
    missing = [k for k in transaction_schema if k not in d]
    if missing:
        return Failure(f"Missing fields: {missing}")

    for k, validator in transaction_schema.items():
        result = validator(d[k])
        if isinstance(result, Failure):
            return Failure(f"{k} failed: {result.failure()}")
    return Success(d)

# -------------------------------
# JSON VALIDATION
# -------------------------------

def load_json(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_json_transactions(path: str) -> Dict[str, List]:
    transactions = load_json(path)
    valid, errors = [], []

    for tx in transactions:
        transformed = transform_transaction(tx)
        result = validate_transaction(transformed)
        if isinstance(result, Success):
            valid.append(result.unwrap())
        else:
            errors.append(result.failure())

    return {"valid": valid, "errors": errors}

# -------------------------------
# CSV PROCESSING
# -------------------------------

def load_csv(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def process_csv_transactions(path: str) -> Dict[str, List]:
    transactions = load_csv(path)
    valid, errors = [], []

    for tx in transactions:
        transformed = transform_transaction(tx)
        result = validate_transaction(transformed)
        if isinstance(result, Success):
            valid.append(result.unwrap())
        else:
            errors.append(result.failure())

    return {"valid": valid, "errors": errors}

# -------------------------------
# API VALIDATION
# -------------------------------

def validate_api_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    transformed = transform_transaction(payload)
    result = validate_transaction(transformed)
    if isinstance(result, Success):
        return {"status": "success", "data": result.unwrap()}
    else:
        return {"status": "failure", "error": result.failure()}


