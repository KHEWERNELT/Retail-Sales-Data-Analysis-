import pandas as pd
from pathlib import Path

# Definimos la carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

def main():

    # Cargamos el dataset original
    data = pd.read_excel(BASE_DIR / "data" / "raw" / "OnlineRetail.xlsx")

    # Identificamos los registros con precio cero y sin CustomerID
    registros_no_comerciales = data[
    (data['UnitPrice'] == 0) &
    (data['CustomerID'].isnull())
    ]

    # Creamos una copia del dataset original para realizar la limpieza
    data_clean = data.copy()

    # Eliminamos los registros identificados como no comerciales
    data_clean = data_clean[
        ~data_clean.index.isin(registros_no_comerciales.index)
    ]

    # Convertimos InvoiceDate a formato fecha
    data_clean['InvoiceDate'] = pd.to_datetime(data_clean['InvoiceDate'])

    # Creamos el período mensual
    data_clean['Mes'] = data_clean['InvoiceDate'].dt.to_period('M')

    # Calculamos los ingresos
    data_clean['Revenue'] = data_clean['Quantity'] * data_clean['UnitPrice']

    # Guardamos el dataset limpio
    data_clean.to_csv(BASE_DIR / "data" / "processed" / "data_clean.csv", index=False)

if __name__ == "__main__":
    main()