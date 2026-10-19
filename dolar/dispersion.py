
import requests
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cargar el historial del dólar blue
df_dolar = pd.read_csv("dolar_blue_historico.csv")

df_dolar["fecha"] = pd.to_datetime(df_dolar["fecha"])
df_dolar = df_dolar.sort_values("fecha")

# 2. Tomar el último precio de venta de cada mes
df_dolar["mes"] = df_dolar["fecha"].dt.to_period("M")

dolar_mensual = (
    df_dolar.groupby("mes")["venta"]
    .last()
    .reset_index()
)

# 3. Calcular cuánto varió el dólar porcentualmente cada mes
dolar_mensual["variacion_dolar"] = (
    dolar_mensual["venta"].pct_change() * 100
)

# 4. Descargar la inflación mensual
url = "https://api.argentinadatos.com/v1/finanzas/indices/inflacion"

respuesta = requests.get(url, timeout=30)
respuesta.raise_for_status()

df_inflacion = pd.DataFrame(respuesta.json())

df_inflacion["fecha"] = pd.to_datetime(df_inflacion["fecha"])
df_inflacion["mes"] = df_inflacion["fecha"].dt.to_period("M")

df_inflacion = df_inflacion.rename(
    columns={"valor": "inflacion"}
)

# 5. Unir ambas series por mes
df = pd.merge(
    dolar_mensual,
    df_inflacion[["mes", "inflacion"]],
    on="mes",
    how="inner"
)

df = df[
    (df["mes"] >= pd.Period("2024-01", freq="M")) &
    (df["mes"] <= pd.Period("2026-10", freq="M"))
]

df = df.dropna(
    subset=["variacion_dolar", "inflacion"]
)

# 6. Calcular correlación
correlacion = df["variacion_dolar"].corr(df["inflacion"])

# 7. Crear gráfico de dispersión
plt.figure(figsize=(10, 6))

plt.scatter(
    df["inflacion"],
    df["variacion_dolar"],
    alpha=0.8
)

plt.title("Dólar blue vs. inflación mensual")
plt.xlabel("Inflación mensual (%)")
plt.ylabel("Variación mensual del dólar blue (%)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("Meses comparados:", len(df))
print(f"Correlación: {correlacion:.3f}")

# Guardar los datos comparados
df.to_csv("dolar_vs_inflacion.csv", index=False)

print("Datos guardados en dolar_vs_inflacion.csv")

