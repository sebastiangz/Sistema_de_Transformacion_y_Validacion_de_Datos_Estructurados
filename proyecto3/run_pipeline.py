"""CLI: python run_pipeline.py data/usuarios.json"""
import argparse
import json
from pathlib import Path
from src.parsers import parse_by_extension
from src.pipeline import ValidationPipeline

def main():
    cli = argparse.ArgumentParser(description='Validar y transformar JSON, CSV o XML')
    cli.add_argument('archivo', nargs='?', default='data/usuarios.json')
    cli.add_argument('--salida', help='Ruta para guardar el resultado JSON')
    args = cli.parse_args()
    path = Path(args.archivo)
    try:
        content = path.read_text(encoding='utf-8-sig')
    except OSError as exc:
        print(f'ERROR: No se pudo leer el archivo: {exc}')
        return 1
    parsed = parse_by_extension(content, path.suffix)
    if hasattr(parsed, 'errors'):
        print('ERROR:', '; '.join(parsed.errors))
        return 1
    pipeline = ValidationPipeline()
    result = pipeline.run_many(parsed.value) if isinstance(parsed.value, list) else pipeline.run(parsed.value)
    if hasattr(result, 'errors'):
        print('VALIDACIÓN FALLIDA:')
        for error in result.errors:
            print('-', error)
        return 1
    output = json.dumps(result.value, ensure_ascii=False, indent=2)
    print('VALIDACIÓN EXITOSA\n' + output)
    if args.salida:
        try:
            Path(args.salida).write_text(output + '\n', encoding='utf-8')
        except OSError as exc:
            print(f'ERROR al guardar: {exc}')
            return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
