# 🔄 Proyecto 3: Sistema de Transformación y Validación de Datos Estructurados  26

## 📋 Descripción del Proyecto

Sistema funcional para transformar, validar y sanitizar datos estructurados mediante composición de funciones puras, schemas funcionales y pipelines de validación inmutables.

**Universidad de Colima - Ingeniería en Computación Inteligente**  
**Materia**: Programación Funcional  
**Profesor**: Gonzalez Zepeda Sebastian  
**Semestre**: noviembre 2026 - Enero 2027

## Mejoras realizadas por el equipo

Se realizaron modificaciones al sistema original
para mejorar el procesamiento de datos estructurados.

### Mejoras implementadas

- Normalización de correos electrónicos.
- Integración de nuevas funciones al pipeline.
- Limpieza de espacios innecesarios.
- Conversión de correos a minúsculas.
- Actualización de la documentación.
---

## 🎯 Objetivos

- Implementar **schemas funcionales** para validación de datos
- Desarrollar **transformadores composables** inmutables
- Aplicar **pattern matching** para manejo de casos
- Crear **parsers funcionales** usando combinadores
- Utilizar **Either/Maybe monads** para manejo de errores
- Practicar **railway-oriented programming**

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.11+
- **Paradigma**: Programación Funcional
- **Librerías**:
  - `pydantic` - Validación de esquemas
  - `marshmallow` - Serialización funcional
  - `toolz` - Utilidades funcionales
  - `returns` - Monads y tipos funcionales
  - `jsonschema` - Validación JSON

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/data-validation-funcional.git
cd data-validation-funcional

# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### requirements.txt
```
pydantic>=2.5.0
marshmallow>=3.20.0
toolz>=0.12.0
returns>=0.22.0
jsonschema>=4.20.0
typing-extensions>=4.8.0
```

---

## 🚀 Uso del Sistema

```python
from src.validation import create_validator, ValidationPipeline
from src.transforms import compose_transforms

# Definir esquema de validación
user_schema = {
    'name': str,
    'email': EmailValidator(),
    'age': IntRange(18, 120),
    'tags': ListOf(str)
}

# Crear pipeline de validación
validator = create_validator(user_schema)

# Pipeline de transformación
pipeline = ValidationPipeline(
    sanitize_input,
    validate_schema(user_schema),
    transform_dates,
    normalize_fields,
    enrich_data
)

# Procesar datos
result = pipeline.run(raw_data)
result.match(
    success=lambda data: save_to_db(data),
    failure=lambda errors: log_errors(errors)
)
```

---

## 📂 Estructura del Proyecto

```
data-validation-funcional/
├── src/
│   ├── __init__.py
│   ├── validation.py       # Sistema de validación funcional
│   ├── transforms.py       # Transformaciones de datos
│   ├── schemas.py          # Definición de esquemas
│   ├── parsers.py          # Parsers combinatorios
│   ├── sanitizers.py       # Sanitización de datos
│   └── types.py            # Types funcionales (Maybe, Either)
├── tests/
│   ├── test_validation.py
│   ├── test_transforms.py
│   └── test_parsers.py
├── examples/
│   ├── json_validation.py
│   ├── csv_processing.py
│   └── api_validation.py
├── docs/
│   ├── api_reference.md
│   └── patterns.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔑 Características Principales

### 1. Validación Funcional con Either Monad
```python
from returns.result import Result, Success, Failure
from typing import Dict, Any

def validate_user(data: Dict[str, Any]) -> Result[Dict, str]:
    """Validación funcional que retorna Either"""
    return (
        Success(data)
        .bind(validate_email)
        .bind(validate_age)
        .bind(validate_required_fields)
    )

# Uso
result = validate_user(user_data)
result.value_or(default_user)  # Safe unwrapping
```

### 2. Composición de Transformadores
```python
from toolz import compose, pipe

# Transformadores puros
def uppercase_name(data):
    return {**data, 'name': data['name'].upper()}

def add_timestamp(data):
    return {**data, 'created_at': now()}

def hash_password(data):
    return {**data, 'password': bcrypt.hash(data['password'])}

# Pipeline composable
transform_user = compose(
    hash_password,
    add_timestamp,
    uppercase_name
)

# Aplicar transformación
processed = transform_user(raw_user)
```

### 3. Parsers Combinatorios
```python
from typing import Callable, TypeVar

T = TypeVar('T')

class Parser:
    """Parser funcional composable"""
    
    def __init__(self, parser_fn: Callable[[str], tuple]):
        self.parse = parser_fn
    
    def map(self, fn: Callable[[T], T]) -> 'Parser':
        """Functor map para parsers"""
        def new_parser(input_str):
            result, rest = self.parse(input_str)
            return fn(result), rest
        return Parser(new_parser)
    
    def bind(self, fn: Callable[[T], 'Parser']) -> 'Parser':
        """Monad bind para parsers"""
        def new_parser(input_str):
            result, rest = self.parse(input_str)
            return fn(result).parse(rest)
        return Parser(new_parser)

# Uso
date_parser = combine(
    digit.many(4),  # año
    char('-'),
    digit.many(2),  # mes
    char('-'),
    digit.many(2)   # día
).map(construct_date)
```

---

## 📊 Funcionalidades Implementadas

### Validación
- ✅ Validación de esquemas composable
- ✅ Validadores custom funcionales
- ✅ Reglas de negocio como funciones
- ✅ Mensajes de error descriptivos

### Transformación
- ✅ Transformadores inmutables
- ✅ Pipeline de transformación
- ✅ Normalización de datos
- ✅ Enriquecimiento funcional

### Sanitización
- ✅ Limpieza de datos
- ✅ Escape de caracteres especiales
- ✅ Validación de tipos
- ✅ Conversión segura

### Parsing
- ✅ Parsers combinatorios
- ✅ JSON/CSV/XML funcional
- ✅ Manejo de errores elegant
- ✅ Validación durante parsing

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Tests de validación
pytest tests/test_validation.py

# Tests con property-based testing
pytest tests/ -k "property"

# Cobertura
pytest --cov=src tests/
```

---

## 📈 Pipeline de Desarrollo

### Semana 1: Fundamentos (30 Oct - 5 Nov)
- Sistema básico de validación
- Transformadores puros
- Either/Maybe monads

### Semana 2: Parsers Avanzados (6 Nov - 12 Nov)
- Parsers combinatorios
- Railway-oriented programming
- Composición avanzada

### Semana 3: Integración (13 Nov - 19 Nov)
- API de validación completa
- Documentación exhaustiva
- Casos de uso reales

---

## 💼 Componente de Emprendimiento

**Aplicación Real**: Servicio de validación de datos para APIs empresariales

**Propuesta de Valor**:
- Reducción del 90% en errores de datos
- Validación en tiempo real
- Schemas reutilizables y compartibles
- SDK para múltiples lenguajes

**Ventaja Competitiva**: 
- Enfoque funcional = código más mantenible
- Composición = flexibilidad sin complejidad
- Type-safe = menos bugs en producción

---

## 📚 Referencias

- **Pydantic Documentation**: https://docs.pydantic.dev/
- **Returns Library**: https://returns.readthedocs.io/
- **Railway Oriented Programming**: https://fsharpforfunandprofit.com/rop/
- Hutton, G. (2016). *Programming in Haskell*

---

## 🏆 Criterios de Evaluación

- **Validación Funcional (30%)**: Schemas completos, manejo de errores
- **Transformadores Composables (25%)**: Inmutabilidad, composición elegante
- **Parsers (20%)**: Combinadores funcionales, robustez
- **Testing (15%)**: Property-based testing, cobertura
- **Documentación (10%)**: API clara, ejemplos útiles

---
Aportación Individual - Aron Ulises

Normalización de correos electrónicos

Descripción:

Mi aportación al Proyecto 3 consistió en implementar la normalización de correos electrónicos dentro del sistema de transformación y validación de datos estructurados.

Archivos modificados

- "src/sanitizers.py"
- "src/pipeline.py"

Funciones implementadas

1. normalize_email():

Esta función elimina los espacios innecesarios al inicio y al final de un correo electrónico y convierte las letras mayúsculas a minúsculas.

2. normalize_user_email():

Esta función permite aplicar la normalización al correo electrónico de un usuario sin modificar directamente los datos originales.

Ejemplo de funcionamiento

Entrada:

""  ARON@GMAIL.COM  ""

Salida:

""aron@gmail.com""

Integración al sistema

Se agregó la normalización de correos electrónicos al pipeline de procesamiento, después de la limpieza de datos y antes de la validación.

Conclusión

Con esta aportación se busca mejorar la calidad y consistencia de los datos, aplicando principios de programación funcional como las funciones puras y la inmutabilidad.

## 👥 Autor

**Nombre**: [Aron Ulises Gutierrez Cardenas]  
**Email**: [agutierrez121@ucol.mx]  
**GitHub**: [@Alexis1102lr06](https://github.com/Alexis1102lr06)

**Nombre**: [Diego Francisco Vazquez Casillas]  
**Email**: [dvazquez51@ucol.mx]  
**GitHub**: [@josephllerenas8-eng](https://github.com/josephllerenas8-eng)

**Nombre**: [Adrian]  
**Email**: [adrianriverarebolledo@gmail.com]  
**GitHub**: [@adrianRR15](https://github.com/adrianRR15)

Link del video: https://youtu.be/cF8wRCYz7Tg?si=IOxHbq8d-PS30iyg


---

## 📄 Licencia

Proyecto académico - Universidad de Colima © 2025
