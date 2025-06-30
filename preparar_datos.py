import pandas as pd
import re

# Diccionario de coordenadas corregido
municipios_coords = {
    "Amurrio": (43.0531, -2.9986),
    "Urduña/Orduña": (43.0467, -3.0086),
    "Vitoria-Gasteiz": (42.8467, -2.6727),
    "Laguardia": (42.5547, -2.6197),
    "Arraia-Maeztu": (42.7575, -2.4547),
    "Zambrana": (42.6600, -2.8792),
    "Ayala/Aiara": (43.0500, -3.0667),
    "Agurain/Salvatierra": (42.8524, -2.3894),
    "Kuartango": (42.8714, -2.8856),
    "Oñati": (43.0326, -2.4111),
    "Lagrán": (42.6264, -2.5839),
    "Elciego": (42.5153, -2.6186),
    "Lapuebla de Labarca": (42.4931, -2.5714),
    "Peñacerrada-Urizaharra": (42.6442, -2.7133),
    "Barrundia": (42.9167, -2.4917),
    "San Millán/Donemiliaga": (42.8736, -2.3758),
    "Alegría-Dulantzi": (42.8401, -2.5127),
    "Asparrena": (42.8958, -2.3219),
    "Harana/Valle de Arana": (42.7567, -2.3219),
    "Zuia": (42.9819, -2.8430),
    "Zigoitia": (42.9678, -2.7178),
    "Urkabustaiz": (42.9722, -2.9217),
    "Campezo/Kanpezu": (42.6722, -2.3667),
    "Donostia/San Sebastián": (43.3183, -1.9811),
    "Amezketa": (43.0500, -2.0833),
    "Arantzazu": (43.0010, -2.3980),
    "Artzentales": (43.2406, -3.2417),
    "Astigarraga": (43.2808, -1.9478),
    "Berastegi": (43.1236, -1.9786),
    "Gordexola": (43.1806, -3.0736),
    "Leioa": (43.3269, -2.9875),
    "Muskiz": (43.3167, -3.1167),
    "Oiartzun": (43.2992, -1.8583),
    "Urnieta": (43.2467, -1.9908),
    "Zalla": (43.2142, -3.1317),
    "Aretxabaleta": (43.0361, -2.5056),
    "Fruiz": (43.3286, -2.7833),
    "Gernika-Lumo": (43.3167, -2.6833),
    "Igorre": (43.1658, -2.7767),
    "Larrabetzu": (43.2608, -2.7967),
    "Mungia": (43.3542, -2.8467),
    "Legutio": (42.9786, -2.6425),
    "Zarautz": (43.2804, -2.1715),
    "Iruña Oka/Iruña de Oca": (42.8139, -2.8036),
    "Valdegovía/Gaubea": (42.8481, -3.0986),
    "Erriberagoitia/Ribera Alta": (42.8281, -2.4167),
    "Elburgo/Burgelu": (42.8497, -2.5456),
    "Baños de Ebro/Mañueta": (42.5306, -2.6833),
    "Ubide": (43.0278, -2.6861),
    "Orozko": (43.1667, -2.9167),
    "Alkiza": (43.1722, -2.1083),
    "Azpeitia": (43.1833, -2.2667),
    "Karrantza Harana/Valle de Carranza": (43.2250, -3.3667),
    "Aulesti": (43.2958, -2.5633),
    "Mundaka": (43.4083, -2.6967),
    "Arratzua-Ubarrundia": (42.8903, -2.6392),
    "Lantarón": (42.7569, -2.9833),
    "Bernedo": (42.6267, -2.4975)
}

# Cargar el dataset original
df = pd.read_csv('Observaciones.csv', sep=';')

# Seleccionar columnas relevantes
columnas = [
    'scientificname', 'yeareventdate', 'montheventdate', 'dayeventdate',
    'stateprovince', 'county', 'municipality',
    'minimumelevationinmeters', 'decimallatitude', 'decimalLongitude'
]
df = df[columnas]

# Convertir columnas numéricas
for col in ['yeareventdate', 'montheventdate', 'dayeventdate', 'minimumelevationinmeters']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Normalizar nombres de municipios en el DataFrame
def normalize_municipality(name):
    if pd.isna(name):
        return name
    # Eliminar espacios adicionales alrededor de la barra
    name = re.sub(r'\s*/\s*', '/', name.strip())
    return name

df['municipality'] = df['municipality'].apply(normalize_municipality)

# Validar coordenadas
def is_valid_coord(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False

# Rellenar coordenadas vacías o inválidas usando el diccionario
def get_coords(row):
    lat, lon = row['decimallatitude'], row['decimalLongitude']
    if pd.isna(lat) or pd.isna(lon) or not is_valid_coord(lat, lon):
        return municipios_coords.get(row['municipality'], (None, None))
    return (lat, lon)

# Aplicar la función para rellenar coordenadas
df[['decimallatitude', 'decimalLongitude']] = df.apply(get_coords, axis=1, result_type='expand')

# Mostrar cuántos registros siguen sin coordenadas
sin_coords = df['decimallatitude'].isnull().sum()
print(f"Registros sin coordenadas tras rellenar: {sin_coords}")

# Eliminar filas sin especie, año, mes, provincia o municipio
df = df.dropna(subset=['scientificname', 'yeareventdate', 'montheventdate', 'stateprovince', 'municipality'])

# Guardar el dataset limpio con formato decimal consistente
df.to_csv('Observaciones_limpio.csv', index=False, sep=';', float_format="%.6f")
print("Archivo Observaciones_limpio.csv guardado.")

# Resumen rápido
print(df[['scientificname', 'municipality', 'decimallatitude', 'decimalLongitude']].head())