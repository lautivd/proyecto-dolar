import requests
import pandas as pd

url = "https://api.argentinadatos.com/v1/cotizaciones/dolares/blue"

respuesta = requests.get(url, timeout=30)
respuesta.raise_for_status()

datos = respuesta.json()

df = pd.DataFrame(datos)
df["fecha"] = pd.to_datetime(df["fecha"])

# Conservar los datos desde enero de 2023
df = df[df["fecha"] >= "2023-01-01"]

df = df.sort_values("fecha")
df.to_csv("dolar_blue_historico.csv", index=False)

print("Historial descargado correctamente.")
print("Primera fecha:", df["fecha"].min())
print("Última fecha:", df["fecha"].max())
print("Cantidad de registros:", len(df))
