
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos históricos
df = pd.read_csv("dolar_blue_historico.csv")

# Convertir las fechas
df["fecha"] = pd.to_datetime(df["fecha"])

# Ordenar por fecha
df = df.sort_values("fecha")

# Crear el gráfico
plt.figure(figsize=(12, 6))
plt.plot(df["fecha"], df["venta"], label="Dólar blue - Venta")

plt.title("Evolución del dólar blue en Argentina (2024-2026)")
plt.xlabel("Fecha")
plt.ylabel("Precio en pesos argentinos")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

