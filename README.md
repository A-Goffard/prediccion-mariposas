# Mariposas del País Vasco

Aplicación para explorar y predecir especies de mariposas en el País Vasco.

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/mariposas-euskadi.git
   cd mariposas-euskadi
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución de la aplicación

Lanza la app web con:
```bash
python -m streamlit run app.py
```
Se abrirá en tu navegador en http://localhost:8501

## Archivos importantes

- `app.py`: aplicación web principal (Streamlit)
- `Observaciones_limpio.csv`: datos limpios
- `modelo_mariposas.joblib` y encoders: modelo entrenado y transformadores

## Entrenamiento del modelo (opcional)

Si quieres reentrenar el modelo:
```bash
python entrenar_modelo.py
```

## Dependencias principales

- streamlit
- pandas
- scikit-learn
- matplotlib
- joblib
- imbalanced-learn

## Notas

- Si usas Windows y el comando `streamlit` no funciona, usa:  
  `python -m streamlit run app.py`
- Añade tus datos en `Observaciones_limpio.csv` si quieres usar otros.

---

**¡Disfruta explorando las mariposas del País Vasco!**
