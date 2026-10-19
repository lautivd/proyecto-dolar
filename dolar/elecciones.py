import pandas as pd
import matplotlib.pyplot as plt
 
df = pd.read_csv("dolar_blue_historico.csv")

df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

print("Primera fecha:", df["fecha"].min())
print("Última fecha:", df["fecha"].max())
 
# Cargar los datos
df = pd.read_csv("dolar_blue_historico.csv")

df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

# Acontecimientos que vamos a analizar
eventos = {
    "Primera vuelta": "2023-10-22",
    "Balotaje": "2023-11-19"
}

plt.figure(figsize=(12, 6))

for nombre, fecha_evento in eventos.items():
    fecha_evento = pd.Timestamp(fecha_evento)

    # Buscar el precio del dólar en la fecha del acontecimiento
    precio_evento = df.loc[
        df["fecha"] <= fecha_evento, "venta"
    ].iloc[-1]

    # Seleccionar los datos de los 30 días anteriores y posteriores
    periodo = df[
        (df["fecha"] >= fecha_evento - pd.Timedelta(days=30)) &
        (df["fecha"] <= fecha_evento + pd.Timedelta(days=30))
    ].copy()

    # Calcular los días respecto del acontecimiento
    periodo["dias"] = (periodo["fecha"] - fecha_evento).dt.days

    # Calcular la variación porcentual respecto del precio de referencia
    periodo["variacion"] = (
        (periodo["venta"] / precio_evento) - 1
    ) * 100

    plt.plot(
        periodo["dias"],
        periodo["variacion"],
        label=nombre
    )

plt.axvline(0, linestyle="--", label="Día de la elección")
plt.axhline(0, linestyle=":")
plt.title("Dólar blue alrededor de las elecciones presidenciales de 2023")
plt.xlabel("Días respecto de la elección")
plt.ylabel("Variación respecto del precio de referencia (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("elecciones_2023.png", dpi=300)
plt.show()