"""
run_tests.py

Ejecuta todos los tests del proyecto asegurando que el módulo src esté en el PYTHONPATH.
"""

import os
import sys
import subprocess

def main():
    """
    Configura el entorno y ejecuta pytest desde la raíz del proyecto.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")
    sys.path.insert(0, src_path)

    print("🔍 Ejecutando tests con pytest...\n")
    try:
        subprocess.run(["pytest"], cwd=project_root, check=True)
        print("\n✅ Todos los tests pasaron correctamente.")
    except subprocess.CalledProcessError:
        print("\n❌ Algunos tests fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
