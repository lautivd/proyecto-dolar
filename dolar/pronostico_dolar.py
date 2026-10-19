import pandas as pd
import matplotlib.pyplot as plt

# Preparar una tabla de ejemplo
datos = {
    "Tipo": ["Oficial", "Blue", "MEP"],
    "Precio": [1450, 1480, 1465]
}

df = pd.DataFrame(datos)

print(df)