# API Reference

Este documento describe los endpoints y funciones disponibles para validar y procesar transacciones en el proyecto.

---

## 1. Validación de Transacciones

### Función: `validate_transaction(d: dict)`
Valida un diccionario de datos de transacción según el esquema definido.

- **Entrada (dict)**:
  ```json
  {
    "Merchant_Country": "Mexico",
    "Channel": "POS",
    "Amount": "123.45"
  }

# Salida (Success)
{
  "Merchant_Country": "MX",
  "Channel": "POS",
  "Amount": "123.45"
}

# Salida (Failure)
{
  "error": "Missing fields: ['Amount']"
}

## 2. Validación desde JSON
### Función: validate_json_transactions(path: str)

# Entrada (archivo JSON)
[
  {"Merchant_Country": "Mexico", "Channel": "POS", "Amount": "123.45"},
  {"Merchant_Country": "Brazil", "Channel": "ONLINE"}
]

# Salida
{
  "valid": [
    {"Merchant_Country": "MX", "Channel": "POS", "Amount": "123.45"}
  ],
  "errors": [
    "Missing fields: ['Amount']"
  ]
}

## 3. Procesamiento desde CSV
### Función: process_csv_transactions(path: str)

# Entrada (archivo CSV)
Merchant_Country,Channel,Amount
Mexico,POS,123.45
Brazil,ONLINE,99.99

# Salida
{
  "valid": [
    {"Merchant_Country": "MX", "Channel": "POS", "Amount": "123.45"}
  ],
  "errors": [
    "Missing fields: [...]"
  ]
}

## 4. Validación vía API
### Función: validate_api_payload(payload: dict)

# Entrada
{
  "Merchant_Country": "Mexico",
  "Channel": "POS",
  "Amount": "123.45"
}

# Salida (Success)
{
  "status": "success",
  "data": {
    "Merchant_Country": "MX",
    "Channel": "POS",
    "Amount": "123.45",
    "Channel_Type": "Presencial",
    "Processed_At": "2025-11-19T22:14:00.123456"
  }
}

# Salida (Failure)
{
  "status": "failure",
  "error": "Missing fields: ['Amount']"
}

## 5. Transformaciones
### Función: transform_transaction(d: dict)

# Entrada
{
  "Merchant_Country": "Mexico",
  "Channel": "POS",
  "Amount": "123.45"
}

# Salida
{
  "Merchant_Country": "MX",
  "Channel": "POS",
  "Amount": "123.45",
  "Channel_Type": "Presencial",
  "Processed_At": "2025-11-19T22:14:00.123456"
}

