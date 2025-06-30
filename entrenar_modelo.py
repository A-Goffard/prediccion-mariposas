import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

# Cargar datos limpios
df = pd.read_csv('Observaciones_limpio.csv', sep=';')

# Variable derivada: estación del año
def get_season(month):
    if month in [12, 1, 2]:
        return 'invierno'
    elif month in [3, 4, 5]:
        return 'primavera'
    elif month in [6, 7, 8]:
        return 'verano'
    else:
        return 'otoño'
df['season'] = df['montheventdate'].apply(get_season)

# Seleccionar columnas relevantes y eliminar nulos
df = df[['scientificname', 'municipality', 'county', 'montheventdate', 'minimumelevationinmeters', 'decimallatitude', 'decimalLongitude', 'season']].dropna()

# Codificar variables categóricas
le_muni = LabelEncoder()
le_species = LabelEncoder()
le_county = LabelEncoder()
le_season = LabelEncoder()
df['municipality_enc'] = le_muni.fit_transform(df['municipality'])
df['county_enc'] = le_county.fit_transform(df['county'])
df['season_enc'] = le_season.fit_transform(df['season'])
df['species_enc'] = le_species.fit_transform(df['scientificname'])

# Variables de entrada y salida (añadimos county y season)
X = df[['municipality_enc', 'county_enc', 'montheventdate', 'season_enc', 'minimumelevationinmeters', 'decimallatitude', 'decimalLongitude']]
y = df['species_enc']

# Estandarizar variables numéricas (sin warning)
scaler = StandardScaler()
X.loc[:, ['minimumelevationinmeters', 'decimallatitude', 'decimalLongitude']] = scaler.fit_transform(
    X[['minimumelevationinmeters', 'decimallatitude', 'decimalLongitude']]
)

# División estratificada
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Ajustar k_neighbors de SMOTE según la clase minoritaria
min_class_size = y_train.value_counts().min()
k_neighbors = min(5, min_class_size - 1) if min_class_size > 1 else 1
smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Ajuste de hiperparámetros con validación cruzada
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=cv, n_jobs=-1)
clf.fit(X_train_res, y_train_res)

print("Mejores parámetros encontrados:", clf.best_params_)

# Evaluar modelo
y_pred = clf.predict(X_test)
labels = le_species.transform(le_species.classes_)
print(classification_report(y_test, y_pred, labels=labels, target_names=le_species.classes_))

# Guardar modelo y transformadores
joblib.dump(clf.best_estimator_, 'modelo_mariposas.joblib')
joblib.dump(le_muni, 'encoder_municipio.joblib')
joblib.dump(le_species, 'encoder_especie.joblib')
joblib.dump(le_county, 'encoder_county.joblib')
joblib.dump(le_season, 'encoder_season.joblib')
joblib.dump(scaler, 'scaler.joblib')
print("Modelo y transformadores guardados.")
