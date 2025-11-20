"""
sanitizers.py

Contiene funciones para limpiar, convertir y normalizar campos de entrada en transacciones.
"""

import re
from html import escape
from typing import Any

def sanitize_text_fields(d: dict[str, Any]) -> dict[str, Any]:
    """
    Elimina espacios innecesarios y saltos de línea en campos de texto.
    """
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = v.strip().replace('\n', ' ').replace('\r', '')
    return d

def escape_html(d: dict[str, Any]) -> dict[str, Any]:
    """
    Escapa caracteres HTML peligrosos en campos de texto.
    """
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = escape(v, quote=True)
    return d

def convert_numeric_fields(d: dict[str, Any]) -> dict[str, Any]:
    """
    Convierte strings que parecen números en floats.
    """
    for k, v in d.items():
        if isinstance(v, str) and re.match(r'^-?\d+(\.\d+)?$', v.strip()):
            try:
                d[k] = float(v)
            except ValueError:
                continue
    return d

def convert_booleans(d: dict[str, Any]) -> dict[str, Any]:
    """
    Convierte strings como 'true', 'yes', '1' en True, y 'false', 'no', '0' en False.
    """
    true_set = {'true', 'yes', '1'}
    false_set = {'false', 'no', '0'}
    for k, v in d.items():
        if isinstance(v, str):
            s = v.strip().lower()
            if s in true_set:
                d[k] = True
            elif s in false_set:
                d[k] = False
    return d

def normalize_country(d: dict[str, Any]) -> dict[str, Any]:
    """
    Normaliza nombres de países a códigos esperados por el esquema.
    """
    country_map = {
        'India': 'IN',
        'México': 'MX',
        'Mexico': 'MX',
        'USA': 'US',
        'United States': 'US',
        'UK': 'GB',
        'United Kingdom': 'GB',
        'Canada': 'CA',
        'Deutschland': 'DE',
        'Germany': 'DE',
        'France': 'FR',
        'UAE': 'AE',
        'United Arab Emirates': 'AE',
        'Singapore': 'SG'
    }
    country = str(d.get('Merchant_Country') or '')
    d['Merchant_Country'] = country_map.get(country, country)
    return d

def sanitize_input(d: dict[str, Any]) -> dict[str, Any]:
    """
    Aplica todos los sanitizadores en orden funcional.
    """
    return normalize_country(
        convert_booleans(
            convert_numeric_fields(
                escape_html(
                    sanitize_text_fields(d)
                )
            )
        )
    )
