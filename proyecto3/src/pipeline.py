"""Railway-oriented pipeline: errores detienen el flujo."""
from dataclasses import dataclass
from .types import Success, Failure
from .sanitizers import sanitize_input, normalize_email
from .transforms import transform_user
from .validation import validate_user

def coerce_user(data):
    """Convierte edad numérica de CSV/XML sin conversiones peligrosas."""
    if not isinstance(data, dict):
        return data
    age = data.get('age')
    if isinstance(age, str) and age.isdecimal():
        return {**data, 'age': int(age)}
    return dict(data)
def normalize_user_email(data):
    if not isinstance(data, dict):
        return data
    if "email" not in data:
        return data
    return {
        **data,
        "email": normalize_email(data["email"])
    }

@dataclass(frozen=True)
class ValidationPipeline:
    def run(self, raw_data):
        return (Success(raw_data)
                .map(sanitize_input)
                .map(coerce_user)
                .map(normalize_user_email)
                .bind(validate_user)
                .map(transform_user))

    def run_many(self, records):
        if not isinstance(records, list):
            return Failure(('Se esperaba una lista de registros',))
        results = [self.run(record) for record in records]
        errors = tuple(f'Registro {i + 1}: {err}' for i, result in enumerate(results)
                       if isinstance(result, Failure) for err in result.errors)
        return Failure(errors) if errors else Success([result.value for result in results])
