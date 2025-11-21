"""
Script para ejecutar el pipeline de sanitización, validación y visualización de transacciones.
"""

from collections import Counter  # standard library

import pandas as pd  # third-party
from returns.result import Success  # third-party
import matplotlib.pyplot as plt
import seaborn as sns # type: ignore

from src.sanitizers import sanitize_input  # first-party
from src.validation import validate_transaction  # first-party


def main():
    """Lee el CSV, aplica sanitización y validación,
    guarda resultados, muestra resumen y genera visualizaciones."""
    df = pd.read_csv("data/skimming_transaction_data_CSV.csv")

    processed_rows = []
    errors = []
    error_counts = Counter()

    for idx, row in df.iterrows():
        data = row.to_dict()
        s = sanitize_input(data)
        v = validate_transaction(s)

        if isinstance(v, Success):
            processed_rows.append(v.unwrap())
        else:
            error_msg = str(v.failure())
            error_counts[error_msg] += 1
            errors.append({"row": idx, "error": error_msg})

    if processed_rows:
        pd.DataFrame(processed_rows).to_csv("data/transacciones_validas.csv", index=False)

    if errors:
        pd.DataFrame(errors).to_csv("data/errores.csv", index=False)

    print("\n Resumen del procesamiento")
    print(f"Total de transacciones leídas: {len(df)}")
    print(f" Transacciones válidas: {len(processed_rows)}")
    print(f" Transacciones con errores: {len(errors)}")

    print("\n Tipos de error:")
    for err, count in error_counts.most_common():
        print(f"- {err}: {count}")

    if processed_rows:
        df_validas = pd.DataFrame(processed_rows)

        # Distribución de montos
        plt.figure(figsize=(8, 4))
        sns.histplot(df_validas["Amount"], bins=30, kde=True)
        plt.title("Distribución de montos")
        plt.xlabel("Monto")
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        plt.show()

        # Dispersión geográfica
        plt.figure(figsize=(6, 6))
        sns.scatterplot(data=df_validas, x="Longitude", y="Latitude", hue="Merchant_Country", s=30)
        plt.title("Ubicación geográfica de transacciones")
        plt.tight_layout()
        plt.show()

        # Frecuencia por país
        plt.figure(figsize=(8, 4))
        sns.countplot(
            data=df_validas,
            x="Merchant_Country",
            order=df_validas["Merchant_Country"].value_counts().index)
        plt.title("Transacciones por país")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
