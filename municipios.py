import pandas as pd

# Carga el CSV (cambia la ruta si lo tienes en otro sitio)
df = pd.read_csv("Observaciones.csv", sep=';')

# Extraer solo la columna de municipios, eliminando NaN y duplicados
municipios = (
    df['municipality']
    .dropna()
    .str.encode('latin1')
    .str.decode('utf8', errors='ignore')
    .drop_duplicates()
    .tolist()
)

# Imprimir la lista de municipios
print(municipios)

