# -*- coding: utf-8 -*-
from typing import Optional
import click
import logging
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv
import tkinter as tk
from tkinter import filedialog
import pandas as pd


def get_filepath() -> Optional[str]:
    root = tk.Tk()
    root.withdraw()

    # Abrir a janela de diálogo para selecionar o arquivo CSV
    csv_file = filedialog.askopenfilename(
        title="Selecione um arquivo CSV",
        filetypes=[("Arquivos CSV", "*.csv")],
    )

    # Verificar se o usuário cancelou a seleção
    if not csv_file:
        print("Seleção de arquivo cancelada pelo usuário.")
        return None

    return csv_file


def make_time_series_dataset(
    df: pd.DataFrame,
    id_variable: str = "Procedimentos realizados",
) -> pd.DataFrame:
    # Drop the 'total' row
    df = df[df[f"{id_variable}"] != "Total"]

    # Save the csv file with the totals
    df.to_csv("totals.csv", columns=[f"{id_variable}", "Total"])

    # Convert to long format
    df = df.drop(columns=["Total"])
    unique_values = df[f"{id_variable}"].unique()
    mapping_dict = {value: value[:10] for value in unique_values}
    df[f"{id_variable}"] = df[f"{id_variable}"].map(mapping_dict)
    long_df = pd.melt(df, id_vars=[f"{id_variable}"], var_name="ds", value_name="y")

    def parse_custom_date(date_str):
        month_mapping = {
            "Janeiro": "Jan",
            "Fevereiro": "Feb",
            "Março": "Mar",
            "Abril": "Apr",
            "Maio": "May",
            "Junho": "Jun",
            "Julho": "Jul",
            "Agosto": "Aug",
            "Setembro": "Sep",
            "Outubro": "Oct",
            "Novembro": "Nov",
            "Dezembro": "Dec",
        }
        month_str, year_str = date_str.split("/")
        month_str = month_mapping.get(month_str, month_str)
        return pd.to_datetime(f"{month_str}/{year_str}", format="mixed")

    long_df["ds"] = long_df["ds"].apply(parse_custom_date)
    # long_df.rename(columns={"Procedimentos realizados": "unique_id"}, inplace=True) # Not used anymore
    long_df.sort_values(by=[f"{id_variable}", "ds"], inplace=True)

    return long_df


# @click.command()
# @click.argument("input_filepath", type=click.Path(exists=True))
def main():
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in 'dataset.csv').
    """
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")

    input_filepath = get_filepath()
    raw_df = pd.read_csv(input_filepath, delimiter=",", encoding="latin-1")
    id_variable = raw_df.columns[0]
    df = make_time_series_dataset(raw_df, id_variable)
    df.to_csv("./dataset.csv", index=False)


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
