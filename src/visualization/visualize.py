import pandas as pd
import matplotlib.pyplot as plt
import os


def create_plots(path):
    """
    Cria plots para a tendência da série temporal e salva na pasta /reports/figures.

    Parameters:
    - path (str): Caminho para o arquivo CSV com os dados.
    """
    df = pd.read_csv(path)
    df["unique_id"] = df["unique_id"].astype("category")

    for unique_id in df["unique_id"].cat.categories:
        df_id = df[df["unique_id"] == unique_id]
        df_id["ds"] = pd.to_datetime(df_id["ds"])
        df_id.set_index("unique_id", inplace=True)

        plt.figure()
        plt.title(f"Tendência da série temporal para ID {unique_id}")
        plt.plot(df_id["ds"], df_id["y"])
        plt.xlabel("Data")
        plt.ylabel("Valores")
        plt.grid(True)
        plt.tight_layout()

        # Ajuste do caminho para salvar na pasta correta
        save_path = os.path.join("reports", "figures", f"plot_{unique_id}.png")
        plt.savefig(save_path)
        plt.close()


def main():
    # dataset_path = os.path.join("..", "data", "interim", "oftalmo_ts.csv")

    create_plots(r"C:\Users\brvn\Documents\github\hc-demand-forecasting\data\processed\forecasted-df.csv")



if __name__ == "__main__":
    main()
