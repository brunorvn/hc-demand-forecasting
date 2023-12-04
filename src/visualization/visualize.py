import os

import pandas as pd
import matplotlib.pyplot as plt

import pymannkendall

path = os.path.join(
    "C:/Users/brvn/Documents/github/projects/HC/tcc_brvn/src",
    "data",
    "subgroups-dataset.csv",
)

# Importar os dados
df = pd.read_csv(path)

# Pegar somente os dois uids
df = df[(df["unique_id"] == int("0202")) | (df["unique_id"] == int("0301"))]

# Mudar as categorias
df["unique_id"] = df["unique_id"].astype("category")
df.set_index("unique_id", inplace=True)  # Mudar o unique_id para index
df["ds"] = pd.to_datetime(df["ds"])  # Mudar pra datetime


# Plotar os dados
plt.title("Tendência da série temporal")
plt.plot(df["ds"], df["y"])
plt.show()

# Calcular a média móvel
media_movel = df["y"].rolling(window=5).mean()

# Plotar a média móvel
plt.title("Tendência da série temporal após suavização")
plt.plot(df["ds"], media_movel)
plt.show()

# Realizar o teste de Mann-Kendall
teste_mann_kendall = pymannkendall.correlated_seasonal_test()
