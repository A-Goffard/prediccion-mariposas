import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Cargar datos y modelos
@st.cache_data
def load_data():
    df = pd.read_csv('Observaciones_limpio.csv', sep=';')
    return df

@st.cache_resource
def load_model():
    modelo = joblib.load('modelo_mariposas.joblib')
    le_muni = joblib.load('encoder_municipio.joblib')
    le_species = joblib.load('encoder_especie.joblib')
    le_county = joblib.load('encoder_county.joblib')
    le_season = joblib.load('encoder_season.joblib')
    scaler = joblib.load('scaler.joblib')
    return modelo, le_muni, le_species, le_county, le_season, scaler

df = load_data()
modelo, le_muni, le_species, le_county, le_season, scaler = load_model()

# Sidebar para navegación
st.sidebar.title("Mariposas del País Vasco")
page = st.sidebar.radio("Ir a:", ["Estadísticas", "Predicción"])

if page == "Estadísticas":
    st.title("Estadísticas del dataset")
    st.write("Número de observaciones:", len(df))
    st.write("Número de especies distintas:", df['scientificname'].nunique())

    st.subheader("Top 10 especies más observadas")
    st.dataframe(df['scientificname'].value_counts().head(10))

    st.subheader("Observaciones por año")
    fig, ax = plt.subplots()
    df['yeareventdate'].value_counts().sort_index().plot(kind='bar', ax=ax)
    st.pyplot(fig)

    st.subheader("Top 10 municipios con más observaciones")
    st.dataframe(df['municipality'].value_counts().head(10))

    st.subheader("Observaciones por provincia")
    st.dataframe(df['stateprovince'].value_counts())

    st.subheader("Observaciones por mes")
    fig2, ax2 = plt.subplots()
    df['montheventdate'].value_counts().sort_index().plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

elif page == "Predicción":
    st.title("Predicción de especies probables")
    st.write("Selecciona el municipio y el mes para ver las especies más probables:")

    muni = st.selectbox("Municipio", sorted(df['municipality'].unique()))
    mes = st.slider("Mes", 1, 12, 6)

    # Obtener valores únicos asociados al municipio seleccionado
    datos_muni = df[df['municipality'] == muni].iloc[0]
    county = datos_muni['county']
    alt = datos_muni['minimumelevationinmeters']
    lat = datos_muni['decimallatitude']
    lon = datos_muni['decimalLongitude']

    # Mostrar datos asociados (solo lectura)
    st.markdown(f"**Comarca:** {county}")
    st.markdown(f"**Altitud:** {alt} m")
    st.markdown(f"**Latitud:** {lat}")
    st.markdown(f"**Longitud:** {lon}")

    # Derivar estación
    def get_season(month):
        if month in [12, 1, 2]:
            return 'invierno'
        elif month in [3, 4, 5]:
            return 'primavera'
        elif month in [6, 7, 8]:
            return 'verano'
        else:
            return 'otoño'
    season = get_season(mes)

    if st.button("Predecir especies"):
        # Codificar y escalar
        X_pred = pd.DataFrame([{
            'municipality_enc': le_muni.transform([muni])[0],
            'county_enc': le_county.transform([county])[0],
            'montheventdate': mes,
            'season_enc': le_season.transform([season])[0],
            'minimumelevationinmeters': alt,
            'decimallatitude': lat,
            'decimalLongitude': lon
        }])
        X_pred[['minimumelevationinmeters', 'decimallatitude', 'decimalLongitude']] = scaler.transform(
            X_pred[['minimumelevationinmeters', 'decimallatitude', 'decimalLongitude']]
        )
        # Predicción de probabilidades
        probs = modelo.predict_proba(X_pred)[0]
        top_idx = probs.argsort()[::-1][:5]
        top_species = le_species.inverse_transform(top_idx)
        st.subheader("Especies más probables")
        for i, esp in enumerate(top_species):
            st.write(f"{i+1}. {esp} (prob: {probs[top_idx[i]]:.2f})")
