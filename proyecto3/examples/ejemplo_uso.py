from src.pipeline import ValidationPipeline

usuario = {'name': '  Carlos Perez ', 'email': ' CARLOS@EJEMPLO.COM ', 'age': 25}
resultado = ValidationPipeline().run(usuario)
resultado.match(
    success=lambda data: print('Correcto:', data),
    failure=lambda errores: print('Errores:', errores),
)
