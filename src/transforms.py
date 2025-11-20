# src/transforms.py

from datetime import datetime

def normalize_country(d: dict) -> dict:
    """
    Normaliza el campo 'Merchant_Country' a códigos estándar.

    Args:
        d (dict): Diccionario con los datos de la transacción.

    Returns:
        dict: Diccionario actualizado con el país normalizado.
    """
    country_map = {
        'México': 'MX',
        'Mexico': 'MX',
        'United States': 'US',
        'USA': 'US',
        'India': 'IN',
        'Germany': 'DE',
        'France': 'FR',
        'Canada': 'CA',
        'UK': 'GB',
        'United Kingdom': 'GB',
        'UAE': 'AE',
        'Singapore': 'SG'
    }
    country = str(d.get('Merchant_Country') or '')
    d['Merchant_Country'] = country_map.get(country, country)
    return d

def enrich_channel(d: dict) -> dict:
    """
    Agrega el campo 'Channel_Type' según el valor de 'Channel'.

    Args:
        d (dict): Diccionario con los datos de la transacción.

    Returns:
        dict: Diccionario enriquecido con el tipo de canal.
    """
    channel = d.get('Channel', '').upper()
    d['Channel_Type'] = (
        'Presencial' if channel == 'POS' else
        'Digital' if channel == 'ONLINE' else
        'Cajero' if channel == 'ATM' else
        'Otro'
    )
    return d

def add_timestamp(d: dict) -> dict:
    """
    Agrega el campo 'Processed_At' con la fecha y hora actual en formato ISO.

    Args:
        d (dict): Diccionario con los datos de la transacción.

    Returns:
        dict: Diccionario con la marca de tiempo agregada.
    """
    d['Processed_At'] = datetime.utcnow().isoformat()
    return d

def transform_transaction(d: dict) -> dict:
    """
    Aplica todas las transformaciones a una transacción.

    Args:
        d (dict): Diccionario original.

    Returns:
        dict: Diccionario transformado.
    """
    return add_timestamp(
        enrich_channel(
            normalize_country(d)
        )
    )
