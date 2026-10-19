import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("dolar_blue_historico.csv")
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

# Acontecimientos electorales
eventos = {
    "Primera vuelta\n22/10/2023": pd.Timestamp("2023-10-22"),
    "Balotaje\n19/11/2023": pd.Timestamp("2023-11-19")
}

periodos = {
    "30 días antes": -30,
    "15 días antes": -15,
    "7 días antes": -7,
    "Día de referencia": 0,
    "7 días después": 7,
    "15 días después": 15,
    "30 días después": 30
}

resultados = {}

for nombre, fecha_evento in eventos.items():

    # Precio de referencia: último precio disponible hasta la elección
    anteriores = df[df["fecha"] <= fecha_evento]

    if anteriores.empty:
        print(f"No hay datos anteriores para {nombre}")
        continue

    precio_base = anteriores.iloc[-1]["venta"]

    variaciones = {}

    for nombre_periodo, dias in periodos.items():

        fecha_objetivo = fecha_evento + pd.Timedelta(days=dias)

        # Buscar el registro más cercano a la fecha objetivo
        datos_cercanos = df[
            df["fecha"] <= fecha_objetivo
        ]

        if datos_cercanos.empty:
            variaciones[nombre_periodo] = None
            continue

        precio = datos_cercanos.iloc[-1]["venta"]

        variaciones[nombre_periodo] = (
            (precio / precio_base) - 1
        ) * 100

    resultados[nombre] = variaciones

# Crear tabla
tabla = pd.DataFrame(resultados).T

# Mostrar mapa de calor
plt.figure(figsize=(12, 4))

sns.heatmap(
    tabla,
    annot=True,
    fmt=".1f",
    cmap="RdYlGn_r",
    center=0,
    linewidths=0.5
)

plt.title("Variación del dólar blue alrededor de las elecciones de 2023")
plt.xlabel("Período")
plt.ylabel("Elección")
plt.tight_layout()

plt.savefig("mapa_elecciones.png", dpi=80)
plt.show()

print("\nVariaciones porcentuales:")
print(tabla.round(2))