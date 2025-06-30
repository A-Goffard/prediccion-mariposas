import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Observaciones_limpio.csv', sep=';')

# Número de especies y observaciones
print("Número de observaciones:", len(df))
print("Número de especies distintas:", df['scientificname'].nunique())

# Top 10 especies más observadas
print("\nTop 10 especies más observadas:")
print(df['scientificname'].value_counts().head(10))

# Observaciones por año
plt.figure(figsize=(8,4))
df['yeareventdate'].value_counts().sort_index().plot(kind='bar')
plt.title('Observaciones por año')
plt.xlabel('Año')
plt.ylabel('Nº observaciones')
plt.tight_layout()
plt.show()

# Observaciones por municipio
print("\nTop 10 municipios con más observaciones:")
print(df['municipality'].value_counts().head(10))

# Observaciones por provincia
print("\nObservaciones por provincia:")
print(df['stateprovince'].value_counts())

# Observaciones por mes
plt.figure(figsize=(8,4))
df['montheventdate'].value_counts().sort_index().plot(kind='bar')
plt.title('Observaciones por mes')
plt.xlabel('Mes')
plt.ylabel('Nº observaciones')
plt.tight_layout()
plt.show()
