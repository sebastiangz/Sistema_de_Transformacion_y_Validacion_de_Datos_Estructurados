"""
tests/test_transforms.py

Pruebas unitarias para el módulo transforms.py
"""

import pytest
from src import transforms


def test_normalize_country_known():
    """
    Verifica que normalize_country convierte correctamente un país conocido.
    """
    d = {"Merchant_Country": "Mexico"}
    result = transforms.normalize_country(d.copy())
    assert result["Merchant_Country"] == "MX"


def test_normalize_country_unknown():
    """
    Verifica que normalize_country deja intacto un país desconocido.
    """
    d = {"Merchant_Country": "Brazil"}
    result = transforms.normalize_country(d.copy())
    assert result["Merchant_Country"] == "Brazil"


def test_enrich_channel_pos():
    """
    Verifica que enrich_channel asigna 'Presencial' para POS.
    """
    d = {"Channel": "POS"}
    result = transforms.enrich_channel(d.copy())
    assert result["Channel_Type"] == "Presencial"


def test_enrich_channel_online():
    """
    Verifica que enrich_channel asigna 'Digital' para ONLINE.
    """
    d = {"Channel": "ONLINE"}
    result = transforms.enrich_channel(d.copy())
    assert result["Channel_Type"] == "Digital"


def test_enrich_channel_atm():
    """
    Verifica que enrich_channel asigna 'Cajero' para ATM.
    """
    d = {"Channel": "ATM"}
    result = transforms.enrich_channel(d.copy())
    assert result["Channel_Type"] == "Cajero"


def test_enrich_channel_other():
    """
    Verifica que enrich_channel asigna 'Otro' para valores desconocidos.
    """
    d = {"Channel": "MOBILE"}
    result = transforms.enrich_channel(d.copy())
    assert result["Channel_Type"] == "Otro"


def test_add_timestamp():
    """
    Verifica que add_timestamp agrega el campo 'Processed_At' en formato ISO.
    """
    d = {}
    result = transforms.add_timestamp(d.copy())
    assert "Processed_At" in result
    assert result["Processed_At"][:4].isdigit()


def test_transform_transaction_full():
    """
    Verifica que transform_transaction aplica todas las transformaciones.
    """
    d = {"Merchant_Country": "México", "Channel": "POS"}
    result = transforms.transform_transaction(d.copy())
    assert result["Merchant_Country"] == "MX"
    assert result["Channel_Type"] == "Presencial"
    assert "Processed_At" in result
