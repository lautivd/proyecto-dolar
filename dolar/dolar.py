
import requests
import pandas as pd

url = "https://api.argentinadatos.com/v1/cotizaciones/dolares/blue"

print("Descargando historial del dólar blue...")

try:
    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()

    datos = respuesta.json()
    df = pd.DataFrame(datos)

    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df[df["fecha"] >= "2024-01-01"]
    df = df.sort_values("fecha")

    df.to_csv("dolar_blue_historico.csv", index=False)

    print("Descarga terminada.")
    print("Registros obtenidos:", len(df))
    print(df.tail())
    print("Archivo guardado: dolar_blue_historico.csv")

except requests.RequestException as error:
    print("Error al descargar los datos:", error)

except (ValueError, KeyError) as error:
    print("Error al procesar los datos:", error)

